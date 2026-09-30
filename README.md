# 🤖 Autonomous E-Commerce Operations Agent

An intelligent, autonomous multi-agent system designed to understand goals, plan multi-step tasks, call secure tools, and execute real operational workflows within an e-commerce simulation environment. Built on the **Olist Brazilian E-Commerce Dataset** and powered by local open-source LLMs.

> **Core Principle:** The user describes what they want or the problem they face — the system itself draws the optimal path to the result.

---

## 📑 Table of Contents

- [1. Project Definition](#1-project-definition)
- [2. Data Used](#2-data-used)
- [3. System Capabilities](#3-system-capabilities)
- [4. Agent Workflow](#4-agent-workflow)
- [5. Expected Task Types](#5-expected-task-types)
- [6. Operational Environment & Tools](#6-operational-environment--tools)
- [7. Failure & Change Cases](#7-failure--change-cases)
- [8. Evaluation](#8-evaluation)
- [9. Execution Constraints](#9-execution-constraints)
- [10. Final Deliverables](#10-final-deliverables)
- [11. Decisions Left to Team](#11-decisions-left-to-team)
- [12. Data Reference](#12-data-reference)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)

---

## 1. Project Definition

This project revolves around building a system capable of accomplishing real operational tasks within an e-commerce environment. The user is **not** required to describe steps in detail — it suffices to clarify what they want or the problem they face, and the system takes over drawing the optimal path to the result.

The system's role is **not limited to analysis or answering questions** — some tasks require data analysis, while others necessitate executing procedures inside a simulated operational environment. Some tasks require temporarily pausing to obtain user approval before proceeding.

### Main Goal

Reach a system capable of:
- **Goal Understanding** — comprehending what the user needs
- **Planning** — building a plan when needed
- **Tool Selection** — choosing appropriate tools
- **Step Execution** — carrying out the plan
- **Result Monitoring** — observing outcomes
- **Failure Handling** — dealing with errors and edge cases
- **Presenting a clear, reviewable result**

### Scope of Use

| ✅ In Scope | ❌ Out of Scope |
|---|---|
| Order analysis & delivery status tracking | Retrieval-Augmented Generation (RAG) |
| Seller performance review | Vector Databases |
| Payment study & cancellation cases | Semantic search in documents |
| Customer review monitoring | Pre-configured static Q&A mapping |
| Detecting cases requiring intervention | Dependence on paid services as core solution |
| Executing operational actions in simulation environment | |
| Handling open-ended goals requiring multiple steps | |

---

## 2. Data Used

### Olist Brazilian E-Commerce Public Dataset

The core version of the project relies on the **Olist** dataset, which contains approximately **100,000 orders** with anonymized data, covering the Brazilian market during the period from **2016 to 2018**, spanning various stages of the order lifecycle.

Data is downloaded from **Kaggle** and organized in a **local relational database** that the team controls.

| Table | Content |
|---|---|
| `customers` | Customer data, geographic locations, and identifiers |
| `orders` | Order status, purchase/approval/shipping/delivery dates |
| `order_items` | Order elements: product, seller, price, shipping cost |
| `order_payments` | Payment methods, installment count, paid amount |
| `order_reviews` | Customer ratings, texts, and dates |
| `products` | Products, categories, and properties |
| `sellers` | Sellers and their locations |
| `geolocation` | Geographic data linked to postal codes |
| `product_category_name_translation` | Category name translations |

### Simulation Data

Since Olist is **historical data** (not a live system), a local operational layer can be added that includes new elements such as:
- Tasks
- Alerts
- Approval requests
- Action logs
- Changing events

> **Key Principle:** These simulated data remain **separate** from the original data, and each source remains clearly labeled.

---

## 3. System Capabilities

The project is expected to cover a wide spectrum of operational states — not merely become an analysis interface. The final form (number of agents, role distribution, solution approach) is a **design decision** the team determines after research and experimentation.

| Capability | Term | What Must Appear in Implementation |
|---|---|---|
| Goal Understanding | `Goal Understanding` | Comprehending the goal, constraints, and available information |
| Planning | `Planning` | Preparing a plan when the task involves multiple steps |
| Task Decomposition | `Task Decomposition` | Splitting a large task into smaller steps |
| Tool Calling | `Tool Calling` | Selecting appropriate tools and passing correct inputs |
| Routing | `Routing` | Determining the appropriate path for the task |
| Multi-Agent | `Multi-Agent` | Cooperation between multiple agents or task handoff when needed |
| State Management | `State Management` | Preserving execution state: what's done and what remains |
| Memory | `Memory` | Retaining information needed for task continuity and interaction |
| Reflection | `Reflection` | Evaluating the result and determining need for modification or new attempt |
| Re-planning | `Re-planning` | Adjusting the plan when a step fails or conditions change |
| Human in the Loop | `Human in the Loop` | Requesting user approval before executing specific actions |
| Failure Recovery | `Failure Recovery` | Handling errors, timeouts, and invalid results |
| Guardrails | `Guardrails` | Restricting permissions and allowed actions |
| Observability | `Observability` | Logging execution steps, decisions, and tools used |
| Evaluation | `Evaluation` | Measuring system success on repeatable tasks |

---

## 4. Agent Workflow

The following table illustrates the general work cycle for the system. This path does **not** impose a specific structure — phases can be merged or separated according to the final design.

| Step | Action |
|---|---|
| 1 | Receive user request or operational goal |
| 2 | Understand the goal, context, and constraints |
| 3 | Determine if the task requires a plan |
| 4 | Decompose the task and arrange its steps |
| 5 | Select the appropriate agent or tool |
| 6 | Execute the action and receive the result |
| 7 | Verify the correctness of the result |
| 8 | Continue, retry, or re-plan |
| 9 | Request user approval when needed |
| 10 | Update task state and complete execution |
| 11 | Present final result and action log |

### Core Cycle

```
Understand → Plan → Select → Act → Observe → Evaluate → Continue/Re-plan → Finish
```

---

## 5. Expected Task Types

The following examples illustrate the expected level of work from the system — they represent a **descriptive list**, not an exhaustive one.

### Direct Queries
- How many orders arrived after the expected date?
- Which sellers have the highest delay rate?
- What are the best-selling categories during a specific period?

### Analysis & Investigation
- Sales declined during a specific period — investigate the factors associated with this decline.
- Analyze the relationship between delivery delay and customer ratings.
- Identify sellers whose performance requires review, with evidence clarification.

### Open-Ended Goals
- Investigate the most prominent operational problems that deserve management intervention.
- Work on improving delivery performance within user-defined constraints.
- Create a plan to handle critical orders and prioritize them.

### Multi-Step Tasks
- Discover delayed orders, identify associated sellers, compare their performance, then prepare a follow-up plan.
- Test more than one hypothesis about a specific problem, then choose the most appropriate action based on results.

### Conditional Tasks
- If a certain indicator exceeds a threshold, create a review case.
- Execute the action only when required conditions are met, otherwise explain the reason for non-execution.

### Tasks Requiring Approval
- Prepare the necessary actions, but do not execute the sensitive action before user approval.
- Present the expected impact of the proposed action, then pause execution until acceptance or rejection.

---

## 6. Operational Environment & Tools

The real value of the project manifests when agents possess **actual tools** that enable access to information and execute actions. What is required is building a **permissioned, traceable tool layer**.

| Tool Category | Term | Purpose |
|---|---|---|
| Data Tools | `Data Tools` | Read data and execute queries and analyses |
| Analysis Tools | `Analysis Tools` | Perform calculations, aggregations, and analytical logic |
| Operational Tools | `Operational Tools` | Create alert, task, or action within simulation environment |
| State Tools | `State Tools` | Read task state, update it, and complete it |
| Approval Tools | `Approval Tools` | Log approval requests and user decisions |
| Validation Tools | `Validation Tools` | Check outputs and constraints before action adoption |
| MCP | `Model Context Protocol` | Expose some tools in a standardized manner |

### Tool Layer Properties

- ✅ Clear definition for each tool's inputs and outputs
- ✅ Verify input correctness before execution
- ✅ Return understandable error messages the system can handle
- ✅ Separation between read operations and write operations
- ✅ Log every tool call (`Tool Call`) and its result
- ✅ Apply permissions before executing any action
- ✅ Provide test cases including: tool failure, timeout, invalid results
- ✅ **Do not grant the model open access to the device or database**

### Traceability

Every effective action must leave a **log** that includes:
- The request
- The tool used
- The inputs
- The result
- The approval status (if any)

---

## 7. Failure & Change Cases

The ability to deal with failure is a **fundamental part** of the project — the system is tested under non-ideal conditions.

| Case | Term | Description |
|---|---|---|
| Tool Failure | `Tool Failure` | Tool malfunctions during execution |
| Timeout | `Timeout` | Time runs out before obtaining a result |
| Invalid Output | `Invalid Output` | Incomplete result or doesn't match expected format |
| Missing Data | `Missing Data` | Insufficient information for decision-making |
| Conflicting Constraints | `Conflicting Constraints` | Constraints exist that cannot be achieved simultaneously |
| Permission Denied | `Permission Denied` | Attempt to execute action outside permission boundaries |
| Human Rejection | `Human Rejection` | User rejects the proposed action |
| Changed Environment | `Changed Environment` | Environment state changes during task execution |
| Wrong Assumption | `Wrong Assumption` | Discovery that a previous assumption was incorrect |
| Repeated Failure | `Repeated Failure` | Repeated failure and need to prevent infinite loops |
| Partial Success | `Partial Success` | Part of the plan succeeds while another part fails |
| Ambiguous Request | `Ambiguous Request` | Request has more than one possible interpretation |

### Expected Behavior Upon Failure

- Detect that the result is invalid
- Assess whether retrying the attempt is worthwhile
- Change the tool or strategy when needed
- Re-plan when task conditions change
- Request additional information when a safe decision cannot be made
- Stop in an organized manner when the goal becomes unachievable
- **Refrain from fabricating data to fill gaps**

---

## 8. Evaluation

A set of **repeatable test tasks** with varying difficulty levels is prepared, each with clear success criteria. This enables comparing results between different designs or configurations.

| Metric | Term | What It Measures |
|---|---|---|
| Task Success Rate | `Task Success Rate` | Degree of achieving the final goal |
| Tool Selection Accuracy | `Tool Selection Accuracy` | Degree of selecting the correct tool |
| Tool Argument Accuracy | `Tool Argument Accuracy` | Correctness of inputs passed to the tool |
| Planning Quality | `Planning Quality` | Logic of the plan and its feasibility for execution |
| Recovery Rate | `Recovery Rate` | Ability to recover from errors |
| Re-planning Success | `Re-planning Success` | Success of plan adjustment after state change |
| Policy Violation Rate | `Policy Violation Rate` | Attempts to exceed constraints or permissions |
| Human Intervention | `Human Intervention` | Cases that required user intervention |
| Step Efficiency | `Step Efficiency` | Number of steps needed to reach the result |
| Latency | `Latency` | Time taken to execute the task |
| Loop Rate | `Loop Rate` | Non-useful or non-productive repetition |
| Trace Completeness | `Trace Completeness` | Clarity and completeness of the execution log |

### Useful Comparisons During Experimentation

| Comparison A | Comparison B |
|---|---|
| Single Agent | Multi-Agent |
| Direct Execution | Execution After Planning |
| Without Reflection | With Reflection |
| Without Re-planning | With Re-planning |
| Different strategies for handling tool failures | |

---

## 9. Execution Constraints

| Constraint | Details |
|---|---|
| Hardware | Project runs on personal devices |
| Dependencies | Rely on open-source components as much as possible |
| Paid Services | No paid service shall be a core requirement for system operation |
| Model | Use a local language model with size appropriate to available hardware |
| Architecture | Separate agent logic from user interface and data layer |
| Modularity | Design the system to allow model or tool replacement without rebuilding the entire project |
| Secrets | Store settings and secret data outside source code |
| Documentation | Document important technical decisions with justifications |

---

## 10. Final Deliverables

| # | Deliverable |
|---|---|
| 1 | Runnable application from the moment of receiving the request until reaching the result |
| 2 | Clear execution path for agents |
| 3 | Set of tools operating on the database and simulation environment |
| 4 | Clear management of task state and memory needed by the system |
| 5 | Human oversight mechanism (Human in the Loop) for sensitive actions |
| 6 | Reviewable execution log (Execution Trace) |
| 7 | Failure scenarios and recovery tests (including Re-planning) |
| 8 | Evaluation set including diverse tasks and measurable results |
| 9 | Comprehensive documentation of design, experiments, and results |
| 10 | Final demo including: multi-step task, failure case, re-planning case, and human approval case |

---

## 11. Decisions Left to Team

This document focuses on defining the goal, scope, and core capabilities. Architectural and implementation decisions remain open for the team to test alternatives and choose what suits the project:

- Number of agents and their roles
- Framework used to build agents
- Planning approach
- Routing approach
- State design and Memory design
- Self-review mechanism (Reflection)
- Prompt formulation for the model
- Degree of reliance on MCP
- Permission and approval policies
- Mechanism for preventing infinite loops
- Evaluation suite design
- Local model selection and size

### Questions to Be Resolved During Implementation

- When do we need an **Agent**, and when does a **Function** suffice as a tool?
- When does **Multi-Agent** achieve real benefit?
- How do we know that the current plan is no longer valid?
- When do we retry, and when do we re-plan?
- What information must be preserved in **State**?
- What deserves to remain in **Memory**?
- How do we prevent unsafe actions?
- How do we measure system success objectively, far from personal impression?

---

## 12. Data Reference

| Field | Value |
|---|---|
| Dataset Name | Olist Brazilian E-Commerce Public Dataset by Olist |
| Source | Kaggle |
| URL | [kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) |
| Orders | ~100,000 |
| Period | 2016 – 2018 |
| Market | Brazil |
| Tables | 9 (customers, orders, order_items, order_payments, order_reviews, products, sellers, geolocation, category_translation) |

---

## 🛠️ Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| Database | PostgreSQL 16 (via Docker/Podman) | Concurrency for multi-agent, MVCC, advanced analytics, JSONB support |
| Language | Python 3.10+ | Ecosystem for AI/ML and data engineering |
| LLM | Local models via Ollama (Llama 3 / Qwen 2.5) | No paid APIs, runs on personal hardware |
| Dataset | Olist Brazilian E-Commerce | Real-world relational e-commerce data |
| OS | Optimized for CachyOS / Arch Linux | Performance-tuned development environment |
| Agent Framework | TBD (LangGraph / Custom / CrewAI) | Decision left to team |
| Protocol | MCP (Model Context Protocol) | Optional exploration |
| Containerization | Docker / Podman | Reproducible environment |

---

## 📁 Project Structure

```
autonomous-ecommerce-operations-agent/
├── Datasets/Olist/              # Raw CSV files (gitignored, ~150MB)
│   ├── olist_customers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
│   └── product_category_name_translation.csv
│
├── database/
│   ├── schema.sql               # Final table definitions (mart layer)
│   ├── staging_load.sql         # Raw data ingestion (staging layer)
│   ├── transform.sql            # Cleaning & transformation logic
│   ├── indexes.sql              # Performance indexes for agent queries
│   └── migrations/              # Alembic version control
│
├── src/
│   ├── agent/                   # Agent logic, planning, routing, reflection
│   │   ├── __init__.py
│   │   ├── planner.py           # Task decomposition & planning
│   │   ├── router.py            # Task routing logic
│   │   ├── reflector.py         # Self-review & re-planning
│   │   └── state.py             # State management
│   │
│   ├── tools/                   # Tool layer (Data, Analysis, Ops, State, Validation)
│   │   ├── __init__.py
│   │   ├── data_tools.py        # Read queries
│   │   ├── analysis_tools.py    # Aggregations & calculations
│   │   ├── ops_tools.py         # Simulation actions
│   │   ├── state_tools.py       # Task state management
│   │   ├── approval_tools.py    # Human-in-the-loop logging
│   │   └── validation_tools.py  # Constraint checking
│   │
│   └── core/                    # Infrastructure
│       ├── __init__.py
│       ├── db.py                # PostgreSQL connection pool
│       ├── llm.py               # Ollama client
│       ├── logger.py            # Execution trace logging
│       └── config.py            # Environment configuration
│
├── tests/                       # Evaluation suite & recovery scenarios
│   ├── test_data_tools.py
│   ├── test_failure_recovery.py
│   ├── test_replanning.py
│   └── evaluation_suite.py
│
├── docs/                        # Architecture decisions & design notes
│   ├── system-design.md
│   ├── database-design.md
│   └── decisions-log.md
│
├── .env.example                 # Secrets template (never commit .env)
├── .gitignore                   # Protection rules
├── docker-compose.yml           # PostgreSQL + Ollama infrastructure
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Docker or Podman
- Python 3.10+
- Git
- Ollama installed locally (`curl -fsSL https://ollama.com/install.sh | sh`)

### 1. Clone & Configure

```bash
git clone https://github.com/YOUR_USERNAME/autonomous-ecommerce-operations-agent.git
cd autonomous-ecommerce-operations-agent
cp .env.example .env
# Edit .env with your PostgreSQL credentials and Ollama settings
```

### 2. Download Dataset

Download the Olist dataset from Kaggle and place the CSV files in `Datasets/Olist/`:
```bash
mkdir -p Datasets/Olist
# Extract archive.zip contents into Datasets/Olist/
```

### 3. Start Infrastructure

```bash
docker compose up -d
```

### 4. Load & Transform Dataset

```bash
# Load raw data into staging tables
psql -h localhost -U olist -d olist_ecommerce -f database/staging_load.sql

# Transform and clean into final tables
psql -h localhost -U olist -d olist_ecommerce -f database/transform.sql

# Create indexes for agent performance
psql -h localhost -U olist -d olist_ecommerce -f database/indexes.sql
```

### 5. Run Agent

```bash
python -m src.main
```

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_NAME` | Database name | `olist_ecommerce` |
| `DB_USER` | Database user | `olist` |
| `DB_PASSWORD` | Database password | — |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Model name | `llama3.1:8b` |
| `AGENT_MAX_RETRIES` | Max retry attempts | `3` |
| `AGENT_TIMEOUT_SECONDS` | Tool call timeout | `30` |
| `LOG_LEVEL` | Logging level | `INFO` |

---

## 📚 References

- [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- System Design Document (Internal Report)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Ollama Documentation](https://ollama.com/docs)

---

## 📄 License

This project is developed for Learning purposes as part of my training stage for building real agents.

---

*Built with precision on CachyOS • PostgreSQL • Local LLMs*
