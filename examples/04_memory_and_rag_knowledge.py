from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

load_dotenv()

# Knowledge Source (RAG): CrewAI loads files from ./knowledge/ by default
editorial_rag = TextFileKnowledgeSource(
    file_paths=["editorial_guidelines.txt"]
)

editor = Agent(
    role="Brand-Aligned Tech Writer",
    goal="Rewrite rough tech notes so they strictly obey Acme Tech Editorial Rules.",
    backstory="You enforce house style guidelines on every piece of engineering content.",
    verbose=True,
)

rewrite_task = Task(
    description=(
        "Rewrite this rough note using our editorial rules from the knowledge base: "
        "'Our revolutionary new caching layer is a game-changer that lets you delve into faster APIs.'"
    ),
    expected_output="A compliant 2-sentence technical update with zero banned buzzwords and a concrete metric.",
    agent=editor,
)

crew = Crew(
    agents=[editor],
    tasks=[rewrite_task],
    process=Process.sequential,
    memory=True,  # Enables unified short-term & long-term memory across tasks/runs
    knowledge_sources=[editorial_rag],  # Attaches RAG knowledge to the entire crew
    verbose=True,
)

if __name__ == "__main__":
    print(crew.kickoff())
