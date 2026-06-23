import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import StructuredTool
from langchain_core.messages import HumanMessage, AIMessage

# Import skills
from src.skills.mac_cleanup import list_mac_applications, delete_mac_application
from src.skills.document_cleaner import trigger_document_cleanup

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

# Define tools
tools = [
    StructuredTool.from_function(
        func=list_mac_applications,
        name="list_mac_applications",
        description="Lists all user-installed macOS applications in the /Applications directory. Returns application name, path, size, and approximate last used date as a JSON string. Filters out system applications.",
    ),
    StructuredTool.from_function(
        func=delete_mac_application,
        name="delete_mac_application",
        description="Deletes a specified macOS application folder. Requires the full application path (e.g., '/Applications/AppName.app') and an explicit 'confirm=True' flag to proceed with deletion. Returns a success or failure message.",
        args_schema={
            "app_path": {"type": "string", "description": "The full path to the .app bundle to delete (e.g., /Applications/MyCoolApp.app)."},
            "confirm": {"type": "boolean", "description": "A flag that MUST be set to True to confirm the deletion action. The tool will not execute without this confirmation."}
        }
    ),
    StructuredTool.from_function(
        func=trigger_document_cleanup,
        name="trigger_document_cleanup",
        description="Initiates an interactive CLI process to help the user clean up least-used documents from their machine. It scans ~/Documents by default, categorizes files by access time, and allows the user to interactively select files for deletion. The user will be prompted directly in the terminal for confirmation.",
        args_schema={
            "directory": {"type": "string", "description": "Optional: The directory to scan for documents. Defaults to ~/Documents if not provided.", "default": os.path.expanduser("~/Documents")}
        }
    )
]

# Configure the system prompt
system_prompt_template = """
You are an intelligent macOS optimization companion. Your goal is to help the user manage their applications and documents, identify unused or large items, and assist with their removal when explicitly confirmed.

When listing applications, summarize the information clearly, ideally in a markdown table format.

When the user asks to delete an application, you MUST explicitly ask the user for typed confirmation before issuing the 'delete_mac_application' tool call.
For example, if the user wants to delete 'App.app', you should respond with something like: "Are you sure you want to delete /Applications/App.app? Please type 'yes' to confirm."
Only if the user types 'yes' should you proceed with the deletion tool call with 'confirm=True'.

When the user requests to clean up documents, you should use the 'trigger_document_cleanup' tool. This tool will initiate an interactive process directly with the user in the terminal. Inform the user that an interactive session will begin.
"""

# Create the agent prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_template),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Create the agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# CLI chat loop
def run_agent_chat():
    print("Welcome to your macOS Optimization Companion! Type 'exit' to quit.")
    chat_history = [] # Stores previous messages for context

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Exiting chat. Goodbye!")
            break

        try:
            # Invoke the agent with the current user input and the full chat history
            response = agent_executor.invoke(
                {"input": user_input, "chat_history": chat_history}
            )
            agent_output = response['output']
            print(f"Agent: {agent_output}")

            # Update chat history
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=agent_output))

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again or type 'exit' to quit.")

if __name__ == "__main__":
    run_agent_chat()
