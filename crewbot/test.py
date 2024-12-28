from crewai import Agent, Task, Crew
from textwrap import dedent

# Create the Curriculum Designer Agent
curriculum_designer = Agent(
    role='Curriculum Designer',
    goal='Design comprehensive and structured learning paths',
    backstory="""You are an experienced curriculum designer with expertise in 
    breaking down complex subjects into manageable learning modules. You understand 
    learning psychology and how to create effective learning sequences.""",
    verbose=True
)

# Create the Resource Curator Agent
resource_curator = Agent(
    role='Resource Curator',
    goal='Find and validate high-quality learning resources',
    backstory="""You are a skilled resource curator with a keen eye for quality 
    educational content. You know how to find and evaluate resources across different 
    formats including videos, articles, interactive exercises, and documentation.""",
    verbose=True
)

# Create the Progress Tracker Agent
progress_tracker = Agent(
    role='Progress Tracker',
    goal='Design assessment methods and track learning progress',
    backstory="""You are an assessment specialist who knows how to measure learning 
    progress effectively. You can create milestones, checkpoints, and evaluation 
    methods to ensure learning goals are being met.""",
    verbose=True
)

def create_learning_path(subject, student_level, goals):
    # Task 1: Design Curriculum Structure
    design_curriculum = Task(
        description=f"""
        Create a structured curriculum for {subject} considering:
        - Student Level: {student_level}
        - Learning Goals: {goals}
        - Break down into modules and sub-topics
        - Estimate time requirements
        - Identify prerequisites
        """,
        agent=curriculum_designer
    )

    # Task 2: Curate Resources
    curate_resources = Task(
        description=f"""
        Based on the curriculum structure, find appropriate learning resources:
        - Find relevant tutorials, documentation, and exercises
        - Ensure resources match the student level
        - Include a mix of theoretical and practical materials
        - Validate resource quality and accessibility
        Use the curriculum from previous task: {{design_curriculum.output}}
        """,
        agent=resource_curator
    )

    # Task 3: Create Assessment Plan
    create_assessments = Task(
        description=f"""
        Design a comprehensive progress tracking system:
        - Create assessment criteria for each module
        - Define success metrics
        - Design practical exercises and projects
        - Create a progress tracking template
        Based on:
        Curriculum: {{design_curriculum.output}}
        Resources: {{curate_resources.output}}
        """,
        agent=progress_tracker
    )

    # Create and run the crew
    crew = Crew(
        agents=[curriculum_designer, resource_curator, progress_tracker],
        tasks=[design_curriculum, curate_resources, create_assessments],
        verbose=2
    )

    result = crew.kickoff()
    return result

# Example usage
if __name__ == "__main__":
    subject = "Python Programming"
    student_level = "Beginner"
    goals = "Build basic web applications and understand core programming concepts"
    
    learning_path = create_learning_path(subject, student_level, goals)
    print("\nGenerated Learning Path:")
    print(learning_path)