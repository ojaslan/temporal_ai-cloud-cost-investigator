import asyncio

from temporalio.client import Client

from app.workflows.cost_workflow import CostInvestigationWorkflow


async def main():
    client = await Client.connect("localhost:7233")

    query = input("\nWhat do you want to investigate?\n> ")

    result = await client.execute_workflow(
        CostInvestigationWorkflow.run,
        query,
        id="cost-investigation-005",
        task_queue="cost-investigator",
    )

    print("\n========== INVESTIGATION REPORT ==========\n")
    print(result)
    print("\n==========================================\n")


if __name__ == "__main__":
    asyncio.run(main())