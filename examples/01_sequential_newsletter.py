from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool

load_dotenv()

search_tool = SerperDevTool()

researcher = Agent(
    role="Senior Tech News Researcher",
    goal="Find today's top 3 most impactful technology news stories using live web search.",
    backstory="You are a meticulous tech analyst who filters out clickbait to surface verified engineering and AI breakthroughs.",
    tools=[search_tool],
    verbose=True,
)

writer = Agent(
    role="Tech Newsletter Editor",
    goal="Turn raw research into a crisp, 5-line morning newsletter.",
    backstory="You write high-signal daily briefs for busy engineers. You rely strictly on provided research and never invent facts.",
    tools=[],  # No search tool: forces grounding in Researcher's handoff
    verbose=True,
)

research_task = Task(
    description="Search for today's top 3 tech news stories. Extract the headline, core event, and why it matters.",
    expected_output="A clean 3-item summary with Headline, 2-sentence factual summary, and Source for each story.",
    agent=researcher,
)

newsletter_task = Task(
    description="Using ONLY the Researcher's findings, write a 5-line newsletter: 1 title line, 3 one-line story bullets, and 1 sign-off line.",
    expected_output=(
        "Strictly 5 lines with no blank lines:\n"
        "Line 1: Newsletter Title + Date\n"
        "Line 2: • Story 1 summary\n"
        "Line 3: • Story 2 summary\n"
        "Line 4: • Story 3 summary\n"
        "Line 5: One-line sign-off"
    ),
    agent=writer,
    context=[research_task],  # Explicit handoff from Task 1 -> Task 2
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, newsletter_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    print(crew.kickoff())
