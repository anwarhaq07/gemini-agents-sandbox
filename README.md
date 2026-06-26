# Omni Mac Agent with Independent Task Tracker Sandbox

A modular development sandbox demonstrating the integration of a **Single-Agent ReAct (Reason + Act) Loop** powered by **LangChain** and **Google Gemini**, interacting natively with a decoupled local CLI tool.

---

## 🏗️ Architecture Design

The project is structured as a self-contained monorepo splitting logic between autonomous orchestration and deterministic execution:

```text
[ User Prompt ] ──> [ LangChain ReAct Agent Loop ] ──> [ Gemini LLM ]
                           │             ▲
            Determines     │             │ Returns
            Tool Call      ▼             │ Structured Output
                     [ python main.py <args> ]
                           │
                           ▼
                  [ tasks.json (Storage) ]

Components
	1. Orchestration Layer (omni-mac-agent/): Utilizes LangChain to instantiate a state-managed execution agent. It consumes user intent and reasons through which tool parameters to invoke via the Gemini Flash API.

	2. Execution Layer (independent-task-tracker/): A strict, deterministic Python CLI app driving CRUD operations on a local JSON data engine, complete with isolated virtual environments (.venv).

	3. The Bridge (Tools API): Functional wrappers using Python type hinting and explicit docstrings that expose CLI entry points natively to the LLM's function-calling engine.

As an open-source public repository, this project strictly adheres to local sandbox security patterns:

	--> Zero Hardcoded Credentials: All authentication relies on native environment variable resolution (GEMINI_API_KEY) loaded into the shell architecture (~/.zshrc).

	--> Path Obfuscation: Global shortcuts and scripts leverage decoupled shell execution structures ($PWD buffers) to mask local MacBook file path directories during code execution.

	--> Ignored Runtime Artifacts: Data persistence layers (.data/tasks.json) and environment binaries (.venv/) are strict citizens of .gitignore to prevent data leakage and tracking pollution.

[x] Milestone 1: Deterministic Engine Build

	[x] Develop modular Python core for task tracking operations.

	[x] Configure robust argument parsing via argparse.

	[x] Abstract statistics calculations to an isolated analytics module.

	[x] Implement local JSON state persistence.

[x] Milestone 2: Environment Optimization

	[x] Write an automated environment configuration shell script (setup.sh).

	[x] Establish a global terminal execution layer (Zsh runtime function wrapper).

[ ] Milestone 3: Bridge & Tool Integration

	[ ] Initialize LangChain framework structures within the orchestration space.

	[ ] Wrap CLI core functions using LangChain @tool decorators.

	[ ] Define bulletproof string schemas and docstrings for safe LLM parameter injection.

[ ] Milestone 4: The ReAct Execution Loop

	[ ] Connect the Gemini Developer API through Google AI Studio variables.

	[ ] Construct the active create_react_agent execution cycle.

	[ ] Implement protective guardrails (Max loop iterations & explicit validation).

	[ ] Conduct system verification (e.g., "Agent, close out task ID 3 and display my updated stats").
