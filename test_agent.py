from app.agents.cost_agent import create_cost_agent

agent = create_cost_agent()

response = agent(
    "A cloud account spent $120 this month. "
    "EC2 cost $70, RDS cost $35, and S3 cost $15. "
    "Investigate the spending and give recommendations."
)

print(response)