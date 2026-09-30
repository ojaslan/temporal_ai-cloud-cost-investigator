# AI Cloud Cost Investigator

## Project Overview

**AI Cloud Cost Investigator** is an agentic AI system designed to investigate cloud infrastructure costs and explain why cloud spending is increasing.

The project combines **Temporal** for durable workflow execution, **Strands Agents** for agentic reasoning, and **Groq** as the LLM provider.

The project is being developed incrementally. We first build and verify the complete agentic workflow using controlled cost data, and then extend it toward real AWS cost and monitoring data.

---

# 1. What Are We Building?

The basic problem is:

> A cloud account has unexpectedly high spending. Instead of manually checking multiple cloud services, the user asks an AI system to investigate the spending and explain the possible causes.

For example:

```text
User:
Why is my cloud bill high?
```

The system should eventually be able to:

* Identify expensive cloud services
* Compare service-level costs
* Detect unusual spending
* Investigate possible causes
* Use monitoring data as evidence
* Recommend cost optimizations
* Ask for human approval before risky actions
* Execute approved optimization actions
* Verify whether the optimization actually worked

---

# 2. Technology Stack

```text
Python 3.12
     │
     ├── uv
     │
     ├── Temporal
     │
     ├── Strands Agents
     │
     ├── Groq
     │
     ├── AWS Cost Explorer
     │
     └── AWS CloudWatch
```

### Python

Used as the primary development language.

### uv

Used for Python project initialization, dependency management, and reproducible environments.

### Temporal

Used to orchestrate the investigation as a durable workflow.

Temporal is responsible for coordinating Activities and maintaining workflow state.

### Strands Agents

Used to create the AI agent responsible for reasoning about cloud costs.

### Groq

Used as the LLM inference provider.

### AWS Cost Explorer

Planned as the real source of cloud billing data.

### AWS CloudWatch

Planned for collecting operational metrics that can help explain cost changes.

---

# 3. Create the Project

The project was created locally from scratch.

Create the project directory:

```powershell
mkdir E:\temporal\ai-cloud-cost-investigator
cd E:\temporal\ai-cloud-cost-investigator
```

Initialize the Python project:

```powershell
uv init --python 3.12
```

This creates the basic Python project configuration.

---

# 4. Install Project Dependencies

Install the required packages:

```powershell
uv add temporalio strands-agents strands-agents-tools "strands-agents[openai]" python-dotenv
```

The dependencies provide:

```text
temporalio
    ↓
Temporal Python SDK

strands-agents
    ↓
AI agent framework

strands-agents-tools
    ↓
Agent tools

strands-agents[openai]
    ↓
OpenAI-compatible model provider
    ↓
Groq

python-dotenv
    ↓
Environment configuration
```

After dependencies are installed, they are recorded in:

```text
pyproject.toml
```

and locked in:

```text
uv.lock
```

---

# 5. Install Temporal CLI

Install the Temporal CLI:

```powershell
winget install Temporal.TemporalCLI
```

Close and reopen PowerShell after installation.

Verify:

```powershell
temporal --version
```

The Temporal CLI allows us to run a local Temporal development server.

---

# 6. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
MODEL_ID=openai/gpt-oss-20b
TEMPORAL_ADDRESS=localhost:7233
```

The API key is kept outside the source code.

The `.env` file must never be committed to GitHub.

---

# 7. Project Structure

The application is organized into separate components:

```text
ai-cloud-cost-investigator/
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
│
├── test_agent.py
├── worker.py
├── run_workflow.py
│
└── app/
    │
    ├── __init__.py
    │
    ├── agents/
    │   ├── __init__.py
    │   └── cost_agent.py
    │
    ├── activities/
    │   ├── __init__.py
    │   └── cost_data.py
    │
    └── workflows/
        ├── __init__.py
        └── cost_workflow.py
```

Each component has a specific responsibility.

---

# 8. Build the AI Agent

The first major component is the cloud-cost investigation agent.

File:

```text
app/agents/cost_agent.py
```

The agent is configured with:

* Groq API credentials
* Groq model
* Cloud-cost investigation system prompt
* Strands Agent

The agent is instructed to:

1. Identify the highest-cost service.
2. Compare service costs.
3. Detect potentially wasteful spending.
4. Explain possible causes.
5. Provide optimization recommendations.
6. Separate facts from assumptions.
7. Never claim an action was performed unless a tool actually performed it.

---

# 9. Test the Agent Independently

Before introducing Temporal, the agent is tested independently.

Run:

```powershell
uv run python test_agent.py
```

Example input:

```text
A cloud account spent $120 this month.
EC2 cost $70, RDS cost $35, and S3 cost $15.
Investigate the spending and give recommendations.
```

The expected behavior is an investigation containing:

```text
Highest-cost service
        ↓
Cost comparison
        ↓
Percentage analysis
        ↓
Possible causes
        ↓
Optimization recommendations
```

This isolates the AI layer before adding workflow orchestration.

---

# 10. Introduce Temporal

Once the agent works independently, Temporal is introduced.

The goal is to turn the investigation into a durable workflow.

The workflow contains multiple stages:

```text
Receive User Question
        ↓
Collect Cost Data
        ↓
Send Data to Agent
        ↓
AI Investigation
        ↓
Return Report
```

Temporal coordinates these steps.

---

# 11. Create the Cost Data Activity

File:

```text
app/activities/cost_data.py
```

The first Activity provides controlled cloud-cost data.

Current example:

```python
{
    "period": "2026-09",
    "currency": "USD",
    "services": {
        "EC2": 70.00,
        "RDS": 35.00,
        "S3": 15.00
    },
    "total": 120.00
}
```

At this stage the data is intentionally mocked.

This allows us to verify the architecture before introducing AWS permissions and real billing APIs.

Later, this Activity can be replaced or extended with AWS Cost Explorer.

---

# 12. Create the Temporal Workflow

File:

```text
app/workflows/cost_workflow.py
```

The workflow receives the user's question.

For example:

```text
Why is my cloud bill high?
```

It then executes the cost-data Activity:

```text
Temporal Workflow
       │
       ▼
get_cost_data()
       │
       ▼
Cloud Cost Data
```

The workflow combines the user's question and the collected cost data into an investigation prompt.

That prompt is passed to the Strands Agent.

---

# 13. Connect Temporal and Strands

This is one of the main parts of the project.

The architecture becomes:

```text
                 Temporal
                    │
                    ▼
          CostInvestigationWorkflow
                    │
                    ▼
             Cost Activity
                    │
                    ▼
              Cost Data
                    │
                    ▼
             Strands Agent
                    │
                    ▼
                  Groq
```

Temporal handles the **workflow execution**.

Strands handles the **agent reasoning**.

Groq handles the **LLM inference**.

These are separate responsibilities rather than treating the entire application as one AI call.

---

# 14. Create the Temporal Worker

File:

```text
worker.py
```

The Worker connects to the local Temporal server.

It registers:

```text
Workflow:
CostInvestigationWorkflow

Activity:
get_cost_data
```

The Worker listens on:

```text
cost-investigator
```

task queue.

Start it with:

```powershell
uv run python worker.py
```

Expected:

```text
========================================
AI Cloud Cost Investigator Worker
Temporal + Strands + Groq
Task Queue: cost-investigator
========================================
Worker started. Waiting for workflows...
```

The Worker must remain running while the workflow is executed.

---

# 15. Start the Temporal Server

Open another PowerShell terminal:

```powershell
temporal server start-dev
```

Temporal runs locally at:

```text
localhost:7233
```

Temporal Web UI:

```text
http://localhost:8233
```

The Web UI can be used to inspect workflow executions.

---

# 16. Run the Workflow

Open a third PowerShell terminal:

```powershell
cd E:\temporal\ai-cloud-cost-investigator
uv run python run_workflow.py
```

The program asks:

```text
What do you want to investigate?
>
```

Enter:

```text
Why is my cloud bill high?
```

The complete execution becomes:

```text
User
 │
 ▼
run_workflow.py
 │
 ▼
Temporal Server
 │
 ▼
CostInvestigationWorkflow
 │
 ▼
get_cost_data Activity
 │
 ▼
Cost Data
 │
 ▼
Strands Agent
 │
 ▼
Groq
 │
 ▼
Investigation Report
```

---

# 17. Why Temporal Is Used

Without Temporal, the application could simply call the AI agent:

```text
User
 ↓
AI Agent
 ↓
Response
```

That works for a simple prototype.

However, the planned system contains multiple operations:

```text
Get Billing Data
      ↓
Get Monitoring Data
      ↓
Investigate
      ↓
Ask for Approval
      ↓
Execute Action
      ↓
Verify Result
```

These operations can take time and may involve failures.

Temporal provides durable workflow execution so the system can manage these multi-step processes more reliably.

---
