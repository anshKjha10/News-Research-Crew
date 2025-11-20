from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class NewsResearchCrew():
    """NewsResearchCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'


    @agent
    def storage_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['storage_agent'], 
            memory=True,
            verbose=True
        )

    @agent
    def collector_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['collector_agent'],
            memory=True,
            verbose=True
        )
    
    @agent
    def summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer_agent'],
            memory=True,
            verbose=True
        )
    
    @agent
    def bias_detector_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['bias_detector_agent'],
            memory=True,
            verbose=True
        )
    
    @agent
    def stance_equalizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['stance_equalizer_agent'],
            memory=True,
            verbose=True
        )
    
    @agent
    def reporter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter_agent'],
            memory=True,
            verbose=True
        )
    
    @agent
    def semantic_filter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['semantic_filter_agent'],
            memory=True,
            verbose=True
        )

    
    @task
    def reuse_previous_news_task(self) -> Task:
        return Task(
            config=self.tasks_config['reuse_previous_news_task'],
            agent=self.storage_agent()
        )

    @task
    def collection_task(self) -> Task:
        return Task(
            config=self.tasks_config['collection_task'],
            agent=self.collector_agent()
        )
    
    @task
    def persist_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config['persist_collection_task'],
            agent=self.storage_agent()
        )
    
    @task
    def semantic_filter_task(self) -> Task:
        return Task(
            config=self.tasks_config['semantic_filter_task'],
            agent=self.semantic_filter_agent()
        )
    
    @task
    def summarization_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarization_task'],
            agent=self.summarizer_agent()
        )
    
    @task
    def bias_detection_task(self) -> Task:
        return Task(
            config=self.tasks_config['bias_detection_task'],
            agent=self.bias_detector_agent()
        )
    
    @task
    def neutralization_task(self) -> Task:
        return Task(
            config=self.tasks_config['neutralization_task'],
            agent=self.stance_equalizer_agent()
        )
    
    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            agent=self.reporter_agent(),
            output_file='news_digest.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the NewsResearchCrew crew"""
  

        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            memory=True,
            verbose=True,
           
        )
