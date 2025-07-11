from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
#from memory.memory_manager import MemoryManager
#from docker.sandbox_runner import run_code_in_docker
from memory_manager import MemoryManager
from sandbox_runner import run_code_in_docker


@CrewBase
class LeetCodeTutorCrew:
    """LeetCode Tutor Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    memory: MemoryManager = MemoryManager()

    @agent
    def problem_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['problem_generator'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def code_executor(self) -> Agent:
        return Agent(
            config=self.agents_config['code_executor'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def code_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_reviewer'],  # type: ignore[index]
            verbose=True
        )

    @task
    def generate_problem_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_problem_task'],  # type: ignore[index]
            context={"weaknesses": self.memory.get_weaknesses()},
            output_key="problem"
        )

    @task
    def execute_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['execute_code_task'],  # type: ignore[index]
            input_keys=["user_code", "problem"],
            context={"run_code": run_code_in_docker},
            output_key="execution_result"
        )

    @task
    def review_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_code_task'],  # type: ignore[index]
            input_keys=["user_code", "execution_result"],
            context={"memory": self.memory},
            output_key="feedback"
        )

    @crew
    def crew(self) -> Crew:
        """Assemble the Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
