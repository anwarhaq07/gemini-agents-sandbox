import subprocess
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage


def _run_task_tracker_command(command_args: list) -> str:
    """Runs a command against the independent-task-tracker CLI utility."""
    # This file lives inside omni-mac-agent/src/, so it needs to step up two
    # directories to find the tracker at independent-task-tracker/main.py.
    tracker_path = os.path.join(
        os.path.dirname(__file__),
        "../../independent-task-tracker/main.py"
    )
    command = ["python", tracker_path] + command_args
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    except FileNotFoundError:
        return "Error: independent-task-tracker/main.py not found. Make sure the path is correct and the file exists."


@tool
def add_task(task_title: str) -> str:
    """Adds a new task to the task tracker with the given title."""
    return _run_task_tracker_command(["add", task_title])


@tool
def list_tasks() -> str:
    """Lists all current tasks in the task tracker, including their IDs, titles, and statuses."""
    return _run_task_tracker_command(["list"])


@tool
def complete_task(task_id: int) -> str:
    """Marks a task as complete using its numerical ID."""
    return _run_task_tracker_command(["complete", str(task_id)])


@tool
def view_stats() -> str:
    """Shows statistics about tasks, such as the total number of tasks and completed tasks."""
    return _run_task_tracker_command(["stats"])


if __name__ == "__main__":
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # Define the tools
    tools = [add_task, list_tasks, complete_task, view_stats]

    # Define the prompt for the ReAct agent
    prompt = PromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are a helpful assistant that manages a task tracker. "
                    "You have access to tools to add, list, complete tasks, and view statistics. "
                    "Always try to use the tools to answer questions about tasks. "
                    "If the user asks to add a task, confirm the task was added successfully. "
                    "When listing tasks, clearly present the task ID, title, and status. "
                    "When completing a task, confirm the task was completed using the provided ID. "
                    "If a task ID is needed and not provided, ask for it."
                )
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Change your old initialization to look exactly like this:
    app = create_react_agent(model, tools)

    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    print("Task Agent: Hello! How can I help you with your tasks today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Task Agent: Goodbye!")
            break
        
        # For this simple console loop, chat_history is kept empty.
        # For persistent conversation, you would manage a list of messages here.
        response = agent_executor.invoke({"input": user_input, "chat_history": []})
        print(f"Task Agent: {response['output']}")
