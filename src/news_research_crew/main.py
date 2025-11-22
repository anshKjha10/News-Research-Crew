#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

from news_research_crew.crew import NewsResearchCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def inputs_from_env():
    """Build inputs from environment variables.

    Required:
      - TOPIC: the news topic to research
    Optional:
      - REFINED_QUERY: optional refined query for more specific news
      - CURRENT_YEAR: override current year (default: now)
      
    """
    topic = os.getenv("TOPIC")
    if not topic:
        raise Exception(
            "Missing topic. Set TOPIC env var or call run_with_trigger with a JSON payload."
        )
    refined_query = os.getenv("REFINED_QUERY", "")
    current_year = os.getenv("CURRENT_YEAR", str(datetime.now().year))
    return{
        "topic" : topic,
        "refined_query" : refined_query,
        "current_year" : current_year
    }

def run():
    """
    Run the crew.
    """
    inputs = inputs_from_env()

    try:
        NewsResearchCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = inputs_from_env()
    try:
        NewsResearchCrew().crew().train(n_iterations=3, filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        NewsResearchCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = inputs_from_env()

    try:
        NewsResearchCrew().crew().test(n_iterations=3, eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": trigger_payload.get("topic", ""),
        "refined_query": trigger_payload.get("refined_query", ""),
        "current_year": trigger_payload.get("current_year", str(datetime.now().year))
    }

    try:
        result = NewsResearchCrew().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
