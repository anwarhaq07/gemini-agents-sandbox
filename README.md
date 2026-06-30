# Omni Mac Agent with Independent Task Tracker Sandbox

A modular development sandbox demonstrating the integration of a **Single-Agent ReAct (Reason + Act) Loop** powered by **LangChain** and **Google Gemini**, interacting natively with a decoupled local CLI tool.

---

## 🏗️ Architecture Design

Omni Mac Agent with Independent Task Tracker Sandbox

A modular development sandbox demonstrating the integration of a Single-Agent ReAct (Reason + Act) Loop powered by LangGraph and Google Gemini, interacting natively with a decoupled local CLI tool.

🏗️ Architecture Design

The project is structured as a self-contained monorepo splitting logic between autonomous orchestration and deterministic execution, orchestrated via a localized container network:

[ User Prompt ] ──> [ LangGraph ReAct Agent Service ] ──> [ Gemini LLM API ]
                                  │             ▲
                   Executes CLI   │             │ Returns
                   Over Network   ▼             │ Stdout/Data
                          [ Task Tracker Service ]
                                  │
                                  ▼
                       [ tasks.json (Volume Mount) ]


Components
	
	1. Orchestration Layer (omni-mac-agent/): Utilizes LangGraph to instantiate a state-managed execution agent. It consumes user intent and reasons through which tool parameters to invoke via the Gemini Flash API.

	2. Execution Layer (independent-task-tracker/): A strict, deterministic Python CLI app driving CRUD operations on a local JSON data engine.

	3. The Container Plane (Docker & Docker Compose): Isolates both layers into distinct microservices, forcing communication over a secure, shared virtual bridge network while keeping the host machine clean.

As an open-source public repository, this project strictly adheres to local sandbox security patterns:

	--> Zero Hardcoded Credentials: All authentication relies on native environment variable resolution (GEMINI_API_KEY) loaded into the shell architecture or passed into containers via .env files.

	--> Path Obfuscation: Local paths are fully relative or contained within Docker volumes, completely decoupling execution from specific host MacBook file path configurations.

	--> Ignored Runtime Artifacts: Data persistence layers (.data/tasks.json) and environment binaries are strict citizens of .gitignore to prevent data leakage and tracking pollution.

🗂️ Project Milestones

[x] Milestone 1: Deterministic Engine Build

	[x] Develop modular Python core for task tracking operations.
	
	[x] Configure robust argument parsing via argparse.
	
	[x] Abstract statistics calculations to an isolated analytics module.
	
	[x] Implement local JSON state persistence.

[x] Milestone 2: Environment Optimization

	[x] Write an automated environment configuration shell script (setup.sh).
	
	[x] Establish a global terminal execution layer (Zsh runtime function wrapper).

[x] Milestone 3: Bridge & Tool Integration

	[x] Initialize LangChain framework structures within the orchestration space.
	
	[x] Wrap CLI core functions using LangChain @tool decorators.
	
	[x] Define bulletproof string schemas and docstrings for safe LLM parameter injection.

[x] Milestone 4: The ReAct Execution Loop

	[x] Connect the Gemini Developer API through Google AI Studio variables.
	
	[x] Upgrade the core agent architecture to compile a modern LangGraph execution cycle.
	
	[x] Implement protective guardrails and structural message parsing.
	
	[x] Conduct system verification (e.g., "Agent, close out task ID 3 and display my updated stats").

[ ] Milestone 5: Containerization & Service Orchestration

	[ ] Write a Dockerfile for the `independent-task-tracker` engine.
	
	[ ] Write a Dockerfile for the `omni-mac-agent` runtime environment.
	
	[ ] Architect a global `docker-compose.yml` file to stitch both services together over a dedicated virtual network network.
	
	[ ] Implement Docker Named Volumes to preserve your `tasks.json` database file even if the containers are turned off or destroyed.
	
	[ ] Run system verification directly through container terminal attachments.