import os
import sys
from dotenv import load_dotenv
from google import genai

# 1. Load your local API key safely into memory
load_dotenv()

def start_interactive_cli():
    # 2. Safety check: make sure the key exists
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found in your .env file.")
        sys.exit(1)

    # 3. Initialize the Google Developer GenAI client
    client = genai.Client()
    
    # 4. Create a chat session (this auto-tracks your rolling conversation history)
    print("⚡ Connecting to Gemini...")
    chat = client.chats.create(model="gemini-2.5-flash")
    
    print("\n=======================================================")
    print("🚀 Custom Gemini Terminal CLI Active")
    print("Type your question and press Enter.")
    print("Commands: /exit (Close utility), /clear (Wipe history)")
    print("=======================================================\n")

    # 5. Persistent Terminal REPL Loop
    while True:
        try:
            # Capture user terminal input cleanly
            user_input = input("🤖 You > ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == '/exit':
                print("👋 Closing AI session. Goodbye!")
                break
                
            if user_input.lower() == '/clear':
                # Reset the chat instance to wipe short-term RAM context
                chat = client.chats.create(model="gemini-2.5-flash")
                print("清理 🧹 Conversation context cleared.\n")
                continue

            print("🧠 Thinking...")
            response = chat.send_message(user_input)
            
            print(f"\n✨ Gemini:\n{response.text}\n")
            print("-" * 60)

        except KeyboardInterrupt:
            # Catch Ctrl+C gracefully without printing ugly tracebacks
            print("\n👋 Exiting session cleanly...")
            break
        except Exception as e:
            print(f"\n❌ Loop Error: {e}\n")

if __name__ == "__main__":
    start_interactive_cli()