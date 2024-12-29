from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
 
@CrewBase
class Crewbot():
	"""Crewbot crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def curriculum_designer(self) -> Agent:
		return Agent(
			config=self.agents_config['curriculum_designer'],
			verbose=True
		)

	@agent
	def resource_curator(self) -> Agent:
		return Agent(
			config=self.agents_config['resource_curator'],
			verbose=True
		)

	@agent
	def progress_tracker(self) -> Agent:
		return Agent(
			config=self.agents_config['progress_tracker'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def design_curriculum(self) -> Task:
		return Task(
			config=self.tasks_config['design_curriculum'],
			output_file='output/design_curriculum.md'
		)

	@task
	def curate_resources(self) -> Task:
		return Task(
			config=self.tasks_config['curate_resources'],
			output_file='output/curate_resources.md'
		)

	@task
	def create_assessments(self) -> Task:
		return Task(
			config=self.tasks_config['create_assessments'],
			output_file='output/create_assessments.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Crewbot crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
