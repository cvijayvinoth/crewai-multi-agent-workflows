import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.tools import tool
from crewai_tools import FileReadTool, FileWriterTool

load_dotenv()
os.makedirs("output", exist_ok=True)


# 1. Custom Python Tool using @tool decorator
@tool("Calculate Reading Time")
def estimate_reading_time(text: str) -> str:
    """Calculates estimated reading time in seconds assuming 200 words per minute."""
    words = len(text.split())
    seconds = max(1, round((words / 200) * 60))
    return f"{words} words (~{seconds} seconds read time)"


# 2. Built-in File Processing Tools
file_reader = FileReadTool(file_path="knowledge/editorial_guidelines.txt")
file_writer = FileWriterTool()

auditor = Agent(
    role="Content & File Operations Specialist",
    goal="Read local guidelines, audit a sample draft for reading time, and save a report to disk.",
    backstory="You automate editorial QA checks and write clean markdown reports.",
    tools=[file_reader, estimate_reading_time, file_writer],
    verbose=True,
)

audit_task = Task(
    description=(
        "1. Read 'knowledge/editorial_guidelines.txt' using FileReadTool.\n"
        "2. Use 'Calculate Reading Time' on this draft: "
        "'PostgreSQL 18 introduces asynchronous I/O, boosting read throughput by 40% for cloud workloads.'\n"
        "3. Save a short audit report to 'output/audit_report.md' using FileWriterTool."
    ),
    expected_output="Confirmation that 'output/audit_report.md' was written, along with the reading time metric.",
    agent=auditor,
)

crew = Crew(
    agents=[auditor],
    tasks=[audit_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    print(crew.kickoff())
