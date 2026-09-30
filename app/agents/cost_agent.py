import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.openai import OpenAIModel

# Load variables from .env
load_dotenv()


SYSTEM_PROMPT = """
You are an AI Cloud Cost Investigator.

Your job is to investigate cloud spending data.

You must:

1. Identify services with the highest costs.
2. Compare the costs of different services.
3. Detect unusual or potentially wasteful spending.
4. Explain possible reasons for high costs.
5. Give practical cloud cost optimization recommendations.
6. Clearly separate facts from assumptions.
7. Never claim that an action was performed unless a tool actually performed it.

When analyzing costs:
- Be concise.
- Use numbers when available.
- Explain the reasoning behind recommendations.
- Prioritize recommendations by potential impact.
"""


def create_cost_agent() -> Agent:
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY was not found. "
            "Make sure it is present in the .env file."
        )

    model = OpenAIModel(
        client_args={
            "api_key": groq_api_key,
            "base_url": "https://api.groq.com/openai/v1",
        },
        model_id="openai/gpt-oss-20b",
    )

    agent = Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
    )

    return agent