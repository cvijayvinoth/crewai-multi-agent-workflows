import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task

load_dotenv()

analyst = Agent(
    role="Market Analyst",
    goal="Identify key business risks and opportunities in a given topic.",
    backstory="You specialize in evaluating technical viability and market adoption.",
    verbose=True,
)

copywriter = Agent(
    role="Executive Copywriter",
    goal="Write concise executive briefings from analytical notes.",
    backstory="You turn complex risk assessments into 3-sentence leadership summaries.",
    verbose=True,
)

briefing_task = Task(
    description="Evaluate the pros and cons of adopting open-source LLMs on-premise for a mid-sized fintech company, then produce a 3-sentence executive summary.",
    expected_output="A polished 3-sentence executive briefing covering cost, privacy, and operational trade-offs.",
    # Note: In hierarchical mode, the manager assigns and reviews work dynamically
)

crew = Crew(
    agents=[analyst, copywriter],
    tasks=[briefing_task],
    process=Process.hierarchical,
    manager_llm=os.getenv("MODEL", "openai/gpt-4o-mini"),  # Required for hierarchical process
    verbose=True,
)

if __name__ == "__main__":
    print(crew.kickoff())
