from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


@CrewBase
class Qpik:
    """Qpik crew"""

    def __init__(self):
        # Get the current file's directory
        current_dir = Path(__file__).parent

        # Set paths relative to the current directory
        self.agents_config_path = str(current_dir / 'config' / 'agents.yaml')
        self.tasks_config_path = str(current_dir / 'config' / 'tasks.yaml')

        # Load configurations
        with open(current_dir / 'config' / 'agents.yaml') as f:
            self.agents_config = yaml.safe_load(f)

        with open(current_dir / 'config' / 'tasks.yaml') as f:
            self.tasks_config = yaml.safe_load(f)

        # Set the PDF file path
        self.pdf_file_path = str(
            current_dir / 'knowledge/wiertarka.pdf')

    # Initialize LLM
    ollama_llm = LLM(
        model="ollama/llama2:7b",
        base_url="http://localhost:11434",
        config={
            "context_window": 4096,
            "max_tokens": 204,
            "temperature": 0.1
        }
    )

    @agent
    def researcher(self) -> Agent:
        """Create a researcher agent."""
        return Agent(
            role=self.agents_config['researcher']['role'],
            goal=self.agents_config['researcher']['goal'],
            backstory=self.agents_config['researcher']['backstory'],
            verbose=True,
            llm=self.ollama_llm
        )

    @agent
    def reporting_analyst(self) -> Agent:
        """Create a reporting analyst agent."""
        return Agent(
            role=self.agents_config['reporting_analyst']['role'],
            goal=self.agents_config['reporting_analyst']['goal'],
            backstory=self.agents_config['reporting_analyst']['backstory'],
            verbose=True,
            llm=self.ollama_llm
        )

    @task
    def research_task(self) -> Task:
        """Create a research task."""
        task_config = self.tasks_config['research_task']
        return Task(
            description=task_config['description'],
            expected_output=task_config['expected_output'],
            agent=self.researcher(),  # Pass the actual agent instance
            output_file=task_config['output']['file_path'],
            input_file=self.pdf_file_path
        )

    @task
    def reporting_task(self) -> Task:
        """Create a reporting task."""
        task_config = self.tasks_config['reporting_task']
        return Task(
            description=task_config['description'],
            expected_output=task_config['expected_output'],
            agent=self.reporting_analyst(),  # Pass the actual agent instance
            output_file=task_config['output']['file_path']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Qpik crew"""
        return Crew(
            agents=[self.researcher(), self.reporting_analyst()],
            tasks=[self.research_task(), self.reporting_task()],
            process=Process.sequential,
            verbose=True,
        )
