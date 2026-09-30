from datetime import timedelta

from temporalio import workflow
from temporalio.contrib.strands import TemporalAgent

with workflow.unsafe.imports_passed_through():
    from app.activities.cost_data import get_cost_data


@workflow.defn
class CostInvestigationWorkflow:

    def __init__(self) -> None:
        self.agent = TemporalAgent(
            model="groq",
            start_to_close_timeout=timedelta(seconds=60),
        )

    @workflow.run
    async def run(self, query: str) -> str:

        # Get cloud cost data through a Temporal Activity
        cost_data = await workflow.execute_activity(
            get_cost_data,
            start_to_close_timeout=timedelta(seconds=30),
        )

        # Give both the user's question and cost data to the AI agent
        prompt = f"""
You are investigating cloud costs.

USER QUESTION:
{query}

CLOUD COST DATA:
{cost_data}

Analyze the provided cloud cost data and answer the user's question.

You must:
- Identify the highest-cost service.
- Calculate each service's percentage of total cost.
- Identify potentially wasteful or unusual spending.
- Explain possible causes.
- Give practical optimization recommendations.
- Clearly distinguish facts from assumptions.
- Do not claim that any action was performed.
"""

        result = await self.agent.invoke_async(prompt)

        return str(result)