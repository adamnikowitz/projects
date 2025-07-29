from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any
from memory_manager import MemoryManager
from sandbox_runner import run_code_in_docker
from tools import docker_code_executor
from openai import OpenAI
from dotenv import load_dotenv
import os
import traceback
import yaml

@CrewBase
class LeetCodeTutorCrew:
    """LeetCode Tutor Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    agents: List[BaseAgent]
    tasks: List[Task]
    memory: MemoryManager = MemoryManager()

    def __init__(self):
        print(f"DEBUG: Loading agents_config from {self.agents_config}")
        print(f"DEBUG: Loading tasks_config from {self.tasks_config}")
        print(f"DEBUG: Loaded tool: {docker_code_executor}")
        load_dotenv()
        print(f"DEBUG: OPENAI_API_KEY set: {bool(os.getenv('OPENAI_API_KEY'))}")
        
        # Load config files
        try:
            with open(self.agents_config, 'r') as f:
                self._agents_config = yaml.safe_load(f)
            with open(self.tasks_config, 'r') as f:
                self._tasks_config = yaml.safe_load(f)
        except Exception as e:
            print(f"ERROR: Failed to load config files: {str(e)}")
            raise
            
        super().__init__()

    @agent
    def problem_generator(self) -> Agent:
        print("DEBUG: Creating problem_generator agent")
        try:
            agent = Agent(
                config=self._agents_config['problem_generator'],
                verbose=True
            )
            print("DEBUG: Testing LLM response for problem_generator")
            # Test LLM connection
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Generate a simple coding problem title."}]
            )
            print(f"DEBUG: LLM test response: {response.choices[0].message.content}")
            return agent
        except Exception as e:
            print(f"ERROR: Failed to create problem_generator agent: {str(e)}")
            traceback.print_exc()
            raise

    @agent
    def code_executor(self) -> Agent:
        print(f"DEBUG: Assigning docker_code_executor to code_executor: {docker_code_executor}")
        try:
            return Agent(
                config=self._agents_config['code_executor'],
                tools=[docker_code_executor],
                verbose=True
            )
        except Exception as e:
            print(f"ERROR: Failed to create code_executor agent: {str(e)}")
            traceback.print_exc()
            raise

    @agent
    def code_reviewer(self) -> Agent:
        print(f"DEBUG: Assigning docker_code_executor to code_reviewer: {docker_code_executor}")
        try:
            return Agent(
                config=self._agents_config['code_reviewer'],
                tools=[docker_code_executor],
                verbose=True
            )
        except Exception as e:
            print(f"ERROR: Failed to create code_reviewer agent: {str(e)}")
            traceback.print_exc()
            raise

    @task
    def generate_problem_task(self) -> Task:
        print("DEBUG: Starting generate_problem_task")
        try:
            task = Task(
                config=self._tasks_config['generate_problem_task'],
                agent=self.problem_generator()
            )
            print(f"DEBUG: Created generate_problem_task: {task.description[:50]}")
            return task
        except Exception as e:
            print(f"ERROR: Failed to create generate_problem_task: {str(e)}")
            traceback.print_exc()
            raise

    @task
    def execute_code_task(self) -> Task:
        print(f"DEBUG: Creating execute_code_task")
        try:
            task = Task(
                config=self._tasks_config['execute_code_task'],
                agent=self.code_executor(),
                context=[self.generate_problem_task()]  # This task depends on the problem generation
            )
            print(f"DEBUG: Created execute_code_task: {task.description[:50]}")
            return task
        except Exception as e:
            print(f"ERROR: Failed to create execute_code_task: {str(e)}")
            traceback.print_exc()
            raise

    @task
    def review_code_task(self) -> Task:
        print(f"DEBUG: Creating review_code_task")
        try:
            task = Task(
                config=self._tasks_config['review_code_task'],
                agent=self.code_reviewer(),
                context=[self.generate_problem_task(), self.execute_code_task()]  # Depends on both previous tasks
            )
            print(f"DEBUG: Created review_code_task: {task.description[:50]}")
            return task
        except Exception as e:
            print(f"ERROR: Failed to create review_code_task: {str(e)}")
            traceback.print_exc()
            raise

    @crew
    def crew(self) -> Crew:
        """Assemble the Crew"""
        print(f"DEBUG: Assembling crew with {len(self.agents)} agents and {len(self.tasks)} tasks")
        print(f"DEBUG: Agents: {[agent.role for agent in self.agents]}")
        print(f"DEBUG: Tasks: {[task.description[:50] for task in self.tasks]}")
        try:
            crew_instance = Crew(
                agents=self.agents,
                tasks=self.tasks,
                process=Process.sequential,
                verbose=True
            )
            print("DEBUG: Crew assembled successfully")
            return crew_instance
        except Exception as e:
            print(f"ERROR: Failed to assemble crew: {str(e)}")
            traceback.print_exc()
            raise