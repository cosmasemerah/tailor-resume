from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from .tools.resume_tools import ResumeTools
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ResumeTailor():
	"""ResumeTailor crew for job application assistance"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self, resume_path='./fake_resume.md'):
		"""Initialize the crew with tools"""
		# Initialize Gemini LLM with Google AI Studio configuration
		self.llm = LLM(
			model="gemini/gemini-1.5-pro-latest",
			temperature=0.7,
			api_key=os.getenv("GEMINI_API_KEY")
		)
		self.tools = ResumeTools(resume_path=resume_path)

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=self.tools.get_researcher_tools(),
			llm=self.llm,
			verbose=True
		)

	@agent
	def profiler(self) -> Agent:
		return Agent(
			config=self.agents_config['profiler'],
			tools=self.tools.get_profile_tools(),
			llm=self.llm,
			verbose=True
		)

	@agent
	def resume_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['resume_strategist'],
			tools=self.tools.get_resume_tools(),
			llm=self.llm,
			verbose=True
		)

	@agent
	def interview_preparer(self) -> Agent:
		return Agent(
			config=self.agents_config['interview_preparer'],
			tools=self.tools.get_interview_tools(),
			llm=self.llm,
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task']
		)

	@task
	def profile_task(self) -> Task:
		return Task(
			config=self.tasks_config['profile_task']
		)

	@task
	def resume_strategy_task(self) -> Task:
		return Task(
			config=self.tasks_config['resume_strategy_profile_task'],
			output_file='tailored_resume.md'
		)

	@task
	def interview_preparation_task(self) -> Task:
		return Task(
			config=self.tasks_config['interview_preparation_task'],
			output_file='interview_materials.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ResumeTailor crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
