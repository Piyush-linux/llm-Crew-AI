from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools import yt_tool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Youblog():
	"""Youblog crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def research_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['research_analyst'],
			verbose=True
		)

	@agent
	def content_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['content_writer'],
			verbose=True
		)

	@agent
	def content_editor(self) -> Agent:
		return Agent(
			config=self.agents_config['content_editor'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			tools=[yt_tool],
		)

	@task
	def writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['writing_task'],
		)

	@task
	def editing_task(self) -> Task:
		return Task(
			config=self.tasks_config['editing_task'],
			output_file='blog.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Youblog crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
