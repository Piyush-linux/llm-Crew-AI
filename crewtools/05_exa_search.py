from crewai_tools import EXASearchTool
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
load_dotenv()
os.environ["EXA_APLKEY"] = "xxx"
tool = EXASearchTool()

agent = Agent(
    role="EXA Search Agent",
    goal="You will search the EXA file for the answer to the question.  Use the tools to search the EXA file.",
    backstory="""You are a master at searching EXA files.""",
    tools=[tool],
    verbose=True,
    allow_delegation=False
)
task = Task(
    description="Answer the following questions about the EXA file: {question}",
    expected_output="An answer to the question.",
    tools=[tool],
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
)

while True:
    question = input("Enter a question about for EXA: ")
    result = crew.kickoff(inputs={"question": question})
    print(result)