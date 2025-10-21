"""
OpenAI Agents SDK + Cognitora Sandbox Integration Example
==========================================================

This example demonstrates how to create an AI agent that can execute code
in a secure sandbox environment using OpenAI Agents SDK and Cognitora SDK.

The agent can perform real-life tasks like:
- Data analysis and visualization
- File processing and text manipulation
- Mathematical calculations and simulations
- Web scraping and API data processing
- Report generation and data transformation
"""

import os
import asyncio
from typing import Literal
from agents import Agent, Runner, function_tool
from cognitora import Cognitora

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use system environment variables

# Get API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COGNITORA_API_KEY = os.getenv("COGNITORA_API_KEY")

# Initialize Cognitora client with SDK
cognitora_client = Cognitora(api_key=COGNITORA_API_KEY)


@function_tool
def execute_code(
    code: str,
    language: Literal["python", "javascript", "bash"] = "python"
) -> str:
    """
    Execute code in a secure sandbox environment using Cognitora SDK.
    
    CRITICAL: You MUST use print() (Python), console.log() (JavaScript), or echo (Bash) 
    to display ALL results. Code that doesn't print anything will return no output!
    
    EXAMPLES OF CORRECT USAGE:
    
    ❌ WRONG (Python):
    result = 5 + 5
    
    ✅ RIGHT (Python):
    result = 5 + 5
    print(f"Result: {result}")
    
    ❌ WRONG (JavaScript):
    let result = 5 + 5;
    
    ✅ RIGHT (JavaScript):
    let result = 5 + 5;
    console.log("Result:", result);
    
    ❌ WRONG (Bash):
    RESULT=$((5 + 5))
    
    ✅ RIGHT (Bash):
    RESULT=$((5 + 5))
    echo "Result: $RESULT"
    
    Args:
        code: The code to execute (MUST include print/console.log/echo statements!)
        language: Programming language (python, javascript, or bash). Default: python
    
    Returns:
        The execution result including output and any errors
    """
    try:
        # Execute code using Cognitora SDK
        result = cognitora_client.code_interpreter.execute(
            code=code,
            language=language,
            networking=False  # Disable internet for security
        )
        
        # Check execution status
        status = result.data.status
        if status == "error" or status == "failed":
            return f"Execution failed with status: {status}"
        
        # Extract outputs from the outputs array
        output_lines = []
        error_lines = []
        
        for output_item in result.data.outputs:
            if output_item.type == "stdout":
                output_lines.append(output_item.data)
            elif output_item.type == "stderr":
                error_lines.append(output_item.data)
        
        # Format the response
        result_parts = []
        if output_lines:
            result_parts.append("\n".join(output_lines))
        if error_lines:
            result_parts.append(f"Errors:\n" + "\n".join(error_lines))
        
        if result_parts:
            return "\n\n".join(result_parts)
        else:
            exec_time = getattr(result.data, 'execution_time_ms', 0)
            return f"Code executed successfully (status: {status}, execution time: {exec_time}ms) but produced no output."
    
    except Exception as e:
        return f"Error executing code: {str(e)}"


@function_tool
def save_result(filename: str, content: str) -> str:
    """
    Save results to a file (simulated - in the sandbox environment).
    
    Args:
        filename: Name of the file to save
        content: Content to save
    
    Returns:
        Confirmation message
    """
    # In a real application, this would save to the sandbox or cloud storage
    return f"✓ Results saved to {filename} ({len(content)} characters)"


async def main():
    """Run interactive examples demonstrating AI + Code Execution for Real-Life Tasks."""
    
    # Check for API keys
    if not OPENAI_API_KEY:
        print("⚠️  Error: OPENAI_API_KEY not set")
        print("Please set it as an environment variable:")
        print('  export OPENAI_API_KEY="your-key-here"')
        print("Or create a .env file (see env_template.txt)")
        return
    
    if not COGNITORA_API_KEY:
        print("⚠️  Error: COGNITORA_API_KEY not set")
        print("Get your API key at: https://www.cognitora.dev/home/api-keys")
        print('Then set it: export COGNITORA_API_KEY="your-key-here"')
        print("Or add it to your .env file")
        return
    
    agent = Agent(
        name="TaskExecutor",
        model="gpt-4o",
        instructions="""You are a helpful AI assistant that executes code to solve problems.

MANDATORY RULE: When you use execute_code tool, you MUST ALWAYS include print() statements 
(or console.log() for JavaScript, echo for Bash) to display results.

Code without print statements will execute but produce NO output, which is useless!

ALWAYS format your code output with:
- print() for all variables you want to show
- print() for all calculations and results
- print() for explanations and labels

Example: If calculating 5 + 5, write:
result = 5 + 5
print(f"The result is: {result}")

NOT just: 5 + 5""",
        tools=[execute_code, save_result]
    )
    
    print("=" * 80)
    print("🤖 OpenAI Agents SDK + 🔒 Cognitora: Real-Life Task Automation")
    print("=" * 80)
    print()
    print("Watch as an AI agent EXECUTES CODE to solve practical, real-world tasks!")
    print()
    
    # Example 1: Sales Data Analysis
    print("💼 Task 1: Analyze Monthly Sales Data")
    print("-" * 80)
    query1 = """GOAL: Analyze my Q4 2024 sales and predict January.
Sales data: Oct=$45,230, Nov=$52,180, Dec=$68,950

Figure out how to calculate total sales, average, growth rates, and predict January.
Write Python code and MUST use print() for all results."""
    
    print(f"Query: {query1}")
    print()
    result1 = await Runner.run(agent, input=query1)
    print(f"✅ Result: {result1.final_output}")
    print()
    
    # Example 2: Prime Numbers
    print("🔢 Task 2: Find Prime Numbers")
    print("-" * 80)
    query2 = """GOAL: Find all prime numbers between 100 and 150.
Write Python code to solve this. print() each prime number."""
    
    print(f"Query: {query2}")
    print()
    result2 = await Runner.run(agent, input=query2)
    print(f"✅ Result: {result2.final_output}")
    print()
    
    # Example 3: Financial Calculator
    print("💰 Task 3: Compound Interest Calculator")
    print("-" * 80)
    query3 = """GOAL: Calculate compound interest for my savings.
$5,000 principal, 6% annual rate, 10 years, compounded monthly.

Write Python code to calculate final amount and interest earned. print() results."""
    
    print(f"Query: {query3}")
    print()
    result3 = await Runner.run(agent, input=query3)
    print(f"✅ Result: {result3.final_output}")
    print()
    
    # Example 4: Data Statistics
    print("📊 Task 4: Statistical Analysis")
    print("-" * 80)
    query4 = """GOAL: Analyze this dataset: [23, 45, 67, 12, 89, 34, 56, 78, 90, 23]
Calculate mean, median, standard deviation, min, max.

Write Python code (no numpy). MUST print() all statistics with labels."""
    
    print(f"Query: {query4}")
    print()
    result4 = await Runner.run(agent, input=query4)
    print(f"✅ Result: {result4.final_output}")
    print()
    
    # Example 5: Password Generator
    print("🔐 Task 5: Generate Secure Password")
    print("-" * 80)
    query5 = """GOAL: Generate 3 secure passwords for me.
Requirements: 16 characters, mixed case, numbers, special characters.

Write Python code using random and string. print() each password."""
    
    print(f"Query: {query5}")
    print()
    result5 = await Runner.run(agent, input=query5)
    print(f"✅ Result: {result5.final_output}")
    print()
    
    # Example 6: Fibonacci Sequence
    print("🔢 Task 6: Fibonacci Sequence")
    print("-" * 80)
    query6 = """GOAL: Show me the first 15 Fibonacci numbers.
Write Python code to generate the sequence. print() all 15 numbers."""
    
    print(f"Query: {query6}")
    print()
    result6 = await Runner.run(agent, input=query6)
    print(f"✅ Result: {result6.final_output}")
    print()
    
    # Example 7: String Processing with JavaScript
    print("📝 Task 7: String Analysis (JavaScript)")
    print("-" * 80)
    query7 = """GOAL: Analyze this string: "Hello World from Cognitora"
Count total characters, vowels, consonants. Show uppercase version.

Write JavaScript code. console.log() all results with labels."""
    
    print(f"Query: {query7}")
    print()
    result7 = await Runner.run(agent, input=query7)
    print(f"✅ Result: {result7.final_output}")
    print()
    
    # Example 8: Date Calculator with Bash
    print("📅 Task 8: System Date Info (Bash)")
    print("-" * 80)
    query8 = """GOAL: Show me current date info and calculate future date.
Get: current date/time, day of week, what date is 30 days from now.

Write Bash commands. Echo all results with labels."""
    
    print(f"Query: {query8}")
    print()
    result8 = await Runner.run(agent, input=query8)
    print(f"✅ Result: {result8.final_output}")
    print()
    
    print("=" * 80)
    print("✅ All Tasks Executed Successfully!")
    print("=" * 80)
    print("\n🚀 Try: python 2-example-interactive.py (Interactive mode)")
    print("       python 4-example-live-crypto-tracker.py (Live data!)\n")


if __name__ == "__main__":
    asyncio.run(main())

