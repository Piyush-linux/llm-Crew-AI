# """
# The Agent will keep executng and testing the code till get pass  
# """

from crewai import Agent, Task, Crew, Process 
from crewai_tools import CodeInterpreterTool 
from dotenv import load_dotenv 
load_dotenv() 
tool = CodeInterpreterTool() 

agent = Agent( 
    role="Code Execution Agent" ,
    goal="You will execute the code and return the output" , 
    backstory="""You are a master at executing code.""" , 
    tools=[tool] , 
    verbose=True , 
    allow_delegation=False
) 

task = Task( 
    description="Answer the following question: {question}", 
    expected_output="The actual code used to get the answer to the file.", 
    agent=agent, 
    output_file="output/code_execution_tool.md"
)

crew = Crew( 
    agents=[agent],
    tasks=[task], 
    verbose=True, 
    process=Process.sequential, 
) 


question = input("Enter your code question: ")
result = crew.kickoff(inputs={"question": question}) 
print(result)