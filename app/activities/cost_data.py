from temporalio import activity


@activity.defn
async def get_cost_data() -> dict:
    """
    Temporary cloud cost data source.

    Later this Activity will call AWS Cost Explorer.
    """

    return {
        "period": "2026-09",
        "currency": "USD",
        "services": {
            "EC2": 70.00,
            "RDS": 35.00,
            "S3": 15.00,
        },
        "total": 120.00,
    }