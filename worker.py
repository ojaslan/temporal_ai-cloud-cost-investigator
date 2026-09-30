import asyncio
import os

from dotenv import load_dotenv
from temporalio.client import Client
from temporalio.contrib.strands import StrandsPlugin
from temporalio.worker import Worker
from strands.models.openai import OpenAIModel

from app.activities.cost_data import get_cost_data
from app.workflows.cost_workflow import CostInvestigationWorkflow


load_dotenv()


def create_groq_model():
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY not found in .env")

    return OpenAIModel(
        client_args={
            "api_key": groq_api_key,
            "base_url": "https://api.groq.com/openai/v1",
        },
        model_id="openai/gpt-oss-20b",
    )


async def main():
    plugin = StrandsPlugin(
        models={
            "groq": create_groq_model,
        }
    )

    client = await Client.connect(
        os.getenv("TEMPORAL_ADDRESS", "localhost:7233"),
        plugins=[plugin],
    )

    worker = Worker(
        client,
        task_queue="cost-investigator",
        workflows=[
            CostInvestigationWorkflow,
        ],
        activities=[
            get_cost_data,
        ],
    )

    print("========================================")
    print("AI Cloud Cost Investigator Worker")
    print("Temporal + Strands + Groq")
    print("Task Queue: cost-investigator")
    print("========================================")
    print("Worker started. Waiting for workflows...")

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())