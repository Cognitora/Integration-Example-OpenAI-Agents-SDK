"""
Interactive AI Task Executor
============================

An interactive CLI that lets you chat with an AI agent that can execute code
to accomplish real-life tasks. Perfect for exploration and testing!
"""

import os
import time
import sys
import asyncio
from datetime import datetime

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use system environment variables

from importlib import import_module
# Import from the renamed file
basic_tasks = import_module('1-example-basic-tasks')
execute_code = basic_tasks.execute_code
save_result = basic_tasks.save_result
from agents import Agent, Runner

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ANSI color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'

def print_gradient_text(text, delay=0.02):
    """Print text with a typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_box(text, color=Colors.CYAN):
    """Print text in a fancy box"""
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    border = "═" * (max_length + 2)
    
    print(f"{color}╔{border}╗{Colors.ENDC}")
    for line in lines:
        padding = " " * (max_length - len(line))
        print(f"{color}║ {Colors.ENDC}{line}{padding}{color} ║{Colors.ENDC}")
    print(f"{color}╚{border}╝{Colors.ENDC}")

def print_section_header(title, emoji="🎯"):
    """Print a fancy section header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'─' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{emoji} {title}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 80}{Colors.ENDC}\n")


async def main():
    """Run an interactive chat session with the code-executing AI agent."""
    
    # Check for API key
    if not OPENAI_API_KEY:
        print(f"{Colors.RED}❌ Error: OPENAI_API_KEY not set{Colors.ENDC}")
        print(f'{Colors.YELLOW}Please set it: export OPENAI_API_KEY="your-key-here"{Colors.ENDC}')
        print(f"{Colors.DIM}Or create a .env file (see env_template.txt){Colors.ENDC}")
        return
    
    # Initialize agent
    print(f"{Colors.DIM}Initializing AI agent with GPT-4o...{Colors.ENDC}")
    
    # System instruction for the agent
    SYSTEM_INSTRUCTION = """You are a helpful AI assistant with code execution capabilities.

CRITICAL RULES:
1. When users ask questions that require calculations or data processing, you MUST execute code.
2. ALWAYS use print() statements in your code to display results.
3. DO NOT just return values - you MUST print() them.
4. After executing code, explain the results to the user.

Example:
User: "Calculate 5 + 5"
WRONG: code = "5 + 5"
RIGHT: code = "result = 5 + 5\\nprint(f'Result: {result}')"

Always execute code and show the output!"""
    
    agent = Agent(
        name="TaskExecutor",
        model="gpt-4o",
        instructions=SYSTEM_INSTRUCTION,
        tools=[execute_code, save_result]
    )
    
    # Clear screen effect
    print("\n" * 2)
    
    # Animated header
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                                ║")
    print("║      🤖  O P E N A I   A G E N T S   +   🔒  C O G N I T O R A                ║")
    print("║                                                                                ║")
    print("║              ✨  Interactive Code Execution Agent  ✨                          ║")
    print("║                                                                                ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")
    print(Colors.ENDC)
    
    time.sleep(0.5)
    
    # Features showcase
    print(f"{Colors.GREEN}✨ POWERED BY:{Colors.ENDC}")
    print(f"   {Colors.BOLD}OpenAI Agents SDK{Colors.ENDC} - Advanced agent framework with tool integration")
    print(f"   {Colors.BOLD}Cognitora{Colors.ENDC} - Secure code execution sandbox (Python/JS/Bash)")
    print(f"   {Colors.BOLD}OpenAI GPT-4o{Colors.ENDC} - Advanced natural language understanding\n")
    
    # Example prompts with colors
    print(f"{Colors.YELLOW}💡 TRY THESE AMAZING TASKS:{Colors.ENDC}")
    examples = [
        ("💰", "Calculate compound interest on $5000 at 6% for 10 years"),
        ("📊", "Analyze my expenses: rent $1200, food $450, utilities $180"),
        ("🔐", "Generate 5 secure passwords with 16 characters"),
        ("📈", "Find all prime numbers between 100 and 200"),
        ("📅", "Calculate how many days until Christmas 2025"),
        ("🎲", "Simulate 1000 dice rolls and show the distribution"),
    ]
    
    for emoji, example in examples:
        print(f"   {emoji}  {Colors.DIM}{example}{Colors.ENDC}")
    
    print(f"\n{Colors.CYAN}{'─' * 80}{Colors.ENDC}")
    print(f"{Colors.DIM}Type 'exit', 'quit', or 'bye' to end the session.{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 80}{Colors.ENDC}\n")
    
    # Statistics
    tasks_completed = 0
    start_time = datetime.now()
    
    # Chat loop
    while True:
        try:
            # Prompt with color
            user_input = input(f"{Colors.BOLD}{Colors.GREEN}You ➤ {Colors.ENDC}").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                # Show session summary
                session_time = (datetime.now() - start_time).total_seconds()
                print(f"\n{Colors.BOLD}📊 Session: {tasks_completed} tasks in {session_time:.1f}s{Colors.ENDC}")
                print(f"{Colors.GREEN}👋 Goodbye!{Colors.ENDC}\n")
                break
            
            # Show thinking indicator
            print(f"\n{Colors.CYAN}🤖 AI Agent Processing...{Colors.ENDC}")
            print(f"{Colors.DIM}   ⚡ Understanding your request...{Colors.ENDC}")
            
            # Get response from agent
            task_start = time.time()
            result = await Runner.run(agent, input=user_input)
            task_time = time.time() - task_start
            
            # Display response with formatting
            print(f"\n{Colors.BOLD}{Colors.BLUE}{'─' * 80}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.BLUE}🤖 AI Response:{Colors.ENDC}")
            print(f"{Colors.BLUE}{'─' * 80}{Colors.ENDC}\n")
            
            # Check if response contains code execution output
            response_text = str(result.final_output)
            if "Output:" in response_text or "print" in response_text.lower():
                print(f"{Colors.GREEN}✓ Code executed successfully!{Colors.ENDC}\n")
            
            print(response_text)
            
            # Footer with stats
            tasks_completed += 1
            print(f"\n{Colors.DIM}{'─' * 80}{Colors.ENDC}")
            print(f"{Colors.DIM}⏱️  Completed in {task_time:.2f}s  •  Task #{tasks_completed}  •  Session: {(datetime.now() - start_time).total_seconds():.0f}s{Colors.ENDC}")
            print(f"{Colors.DIM}{'─' * 80}{Colors.ENDC}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}⚠️  Session interrupted by user{Colors.ENDC}")
            print(f"{Colors.BOLD}👋 Goodbye!{Colors.ENDC}\n")
            break
        except Exception as e:
            print(f"\n{Colors.RED}❌ Error: {e}{Colors.ENDC}")
            print(f"{Colors.YELLOW}💡 Please try again or type 'exit' to quit.{Colors.ENDC}\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n{Colors.RED}Fatal Error: {e}{Colors.ENDC}")
        print(f"{Colors.DIM}Please check your configuration and try again.{Colors.ENDC}\n")

