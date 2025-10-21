#!/usr/bin/env python3
"""
🤖 Multi-Agent Data Science Research System
===========================================

This example demonstrates ADVANCED AGENTIC CAPABILITIES:
- Multi-agent collaboration (agents as tools pattern)
- Code execution via Cognitora sandbox
- Autonomous data analysis workflow
- Agent specialization and coordination

Architecture:
    Master Orchestrator
           ↓
    ┌──────┴──────┐
    ↓             ↓
Data Analyst   Statistician
(Python Code)  (Advanced Stats)
           ↘     ↙
        Report Writer

Each agent has specialized capabilities and they collaborate autonomously!
"""

import os
import time
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from cognitora import Cognitora

from agents import Agent, Runner, function_tool

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COGNITORA_API_KEY = os.getenv("COGNITORA_API_KEY")

# Initialize Cognitora client (for code execution)
cognitora_client = Cognitora(api_key=COGNITORA_API_KEY)

# ============================================================================
# TOOLS FOR CODE EXECUTION
# ============================================================================

@function_tool
def execute_python_analysis(code: str) -> str:
    """
    Execute Python code for data analysis in secure sandbox.
    Use this for: data processing, calculations, visualizations, ML models.
    
    CRITICAL: You MUST use print() statements to display ALL results!
    Code without print() will execute but show no output!
    
    EXAMPLES:
    
    ❌ WRONG - No output:
    total = 100 + 200
    average = total / 2
    
    ✅ RIGHT - Shows results:
    total = 100 + 200
    average = total / 2
    print(f"Total: {total}")
    print(f"Average: {average}")
    
    ❌ WRONG - Returns value (doesn't work in sandbox):
    def calculate():
        return 5 + 5
    result = calculate()
    
    ✅ RIGHT - Prints value:
    def calculate():
        return 5 + 5
    result = calculate()
    print(f"Result: {result}")
    
    Args:
        code: Python code to execute (MUST include print() statements!)
    
    Returns:
        Execution results and output
    """
    try:
        result = cognitora_client.code_interpreter.execute(
            code=code,
            language="python",
            networking=False
        )
        
        # Check execution status
        status = result.data.status
        if status == "error" or status == "failed":
            return f"❌ Execution failed with status: {status}"
        
        # Extract outputs from the outputs array (same as 1-example-basic-tasks.py)
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
            error_text = "\n".join(error_lines)
            result_parts.append(f"Errors:\n{error_text}")
        
        if result_parts:
            return "✅ Analysis complete:\n" + "\n".join(result_parts)
        else:
            return "⚠️ Code executed but no output captured. Make sure to use print() statements!"
        
    except Exception as e:
        return f"❌ Execution failed: {str(e)}"


@function_tool
def save_finding(title: str, finding: str) -> str:
    """
    Save important research findings for the final report.
    
    Args:
        title: Short title for the finding
        finding: The actual finding or insight
    
    Returns:
        Confirmation message
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    return f"📝 Saved finding '{title}' at {timestamp}"


# ============================================================================
# ANSI COLORS FOR BEAUTIFUL OUTPUT
# ============================================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


def print_agent_header(name: str, role: str, emoji: str):
    """Print a beautiful agent header"""
    print(f"\n{Colors.CYAN}{'═' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{emoji} {name.upper()} - {role}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'═' * 80}{Colors.ENDC}")


def print_section(title: str, emoji: str = "🎯"):
    """Print a section header"""
    print(f"\n{Colors.YELLOW}{emoji} {title}{Colors.ENDC}")
    print(f"{Colors.DIM}{'─' * 80}{Colors.ENDC}")


# ============================================================================
# MULTI-AGENT SYSTEM SETUP
# ============================================================================

def create_multi_agent_system():
    """
    Create a multi-agent research system with specialized agents.
    
    This demonstrates OpenAI Agents SDK's multi-agent capabilities where:
    - Each agent has specialized skills
    - Agents can be used as tools by other agents
    - Agents collaborate autonomously to solve complex tasks
    """
    
    # ========================================================================
    # AGENT 1: DATA ANALYST (with code execution capabilities)
    # ========================================================================
    data_analyst = Agent(
        name="data_analyst",
        model="gpt-4o",
        instructions="""You are an expert Data Analyst with Python code execution capabilities.

YOUR CAPABILITIES:
- Execute Python code using execute_python_analysis() tool
- Perform data analysis, calculations, and statistical operations
- Create data visualizations (describe them, as images can't be shown)
- Work with pandas, numpy, statistics libraries

CRITICAL RULES:
1. ALWAYS use print() statements in your code to display results
2. Write clean, well-commented code
3. Break complex analysis into logical steps
4. Explain your findings clearly

When analyzing data:
- Start with exploratory analysis
- Calculate relevant statistics
- Identify patterns and trends
- Provide actionable insights""",
        tools=[execute_python_analysis, save_finding]
    )
    
    # ========================================================================
    # AGENT 2: STATISTICIAN (advanced statistical analysis)
    # ========================================================================
    statistician = Agent(
        name="statistician",
        model="gpt-4o",
        instructions="""You are an expert Statistician specializing in advanced analytics.

YOUR CAPABILITIES:
- Hypothesis testing and statistical inference
- Correlation and regression analysis
- Distribution analysis and probability
- Statistical significance testing
- Predictive modeling

CRITICAL RULES:
1. Use execute_python_analysis() for all calculations
2. ALWAYS include print() statements to show results
3. Explain statistical concepts clearly
4. Provide confidence intervals and p-values where relevant

When conducting analysis:
- State your hypotheses clearly
- Show your statistical tests
- Interpret results in plain language
- Highlight significant findings""",
        tools=[execute_python_analysis, save_finding]
    )
    
    # ========================================================================
    # AGENT 3: REPORT WRITER (synthesizes findings)
    # ========================================================================
    report_writer = Agent(
        name="report_writer",
        model="gpt-4o",
        instructions="""You are an expert Technical Writer specializing in data science reports.

YOUR ROLE:
- Synthesize findings from multiple sources
- Create clear, actionable summaries
- Highlight key insights and recommendations
- Structure information logically

WRITING STYLE:
- Clear and concise
- Use bullet points for key findings
- Include specific numbers and statistics
- Provide actionable recommendations

Format your reports with:
📊 Key Findings
💡 Insights
🎯 Recommendations""",
        tools=[save_finding]
    )
    
    # ========================================================================
    # AGENT 4: MASTER ORCHESTRATOR (coordinates all agents using them as tools)
    # ========================================================================
    master_orchestrator = Agent(
        name="research_director",
        model="gpt-4o",
        instructions="""You are the Research Director coordinating a team of specialists.

YOUR TEAM (available as tools):
- data_analyst_tool: Performs data analysis and Python code execution
- statistician_tool: Conducts advanced statistical analysis
- report_writer_tool: Creates summaries and reports

YOUR ROLE:
- Break down complex research tasks
- Delegate to appropriate specialists using their tools
- Synthesize findings from multiple agents
- Ensure thorough analysis

WORKFLOW:
1. Understand the research question
2. Identify what analysis is needed
3. Call data_analyst_tool for exploratory analysis
4. Call statistician_tool for advanced statistical tests
5. Call report_writer_tool to synthesize findings
6. Provide final comprehensive answer

Use the specialist tools strategically to solve complex problems!""",
        tools=[
            data_analyst.as_tool(
                tool_name="data_analyst_tool",
                tool_description="Expert Data Analyst - performs data analysis and Python code execution"
            ),
            statistician.as_tool(
                tool_name="statistician_tool",
                tool_description="Expert Statistician - conducts advanced statistical analysis"
            ),
            report_writer.as_tool(
                tool_name="report_writer_tool",
                tool_description="Expert Technical Writer - creates summaries and reports"
            ),
            save_finding
        ]
    )
    
    return master_orchestrator, data_analyst, statistician, report_writer


# ============================================================================
# MAIN DEMO
# ============================================================================

async def main():
    """
    Demonstrate multi-agent research system with real data analysis tasks.
    """
    
    # Print header
    print(f"\n{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("     🤖 MULTI-AGENT DATA SCIENCE RESEARCH SYSTEM 🤖")
    print(f"{Colors.ENDC}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")
    
    print(f"{Colors.GREEN}✨ POWERED BY:{Colors.ENDC}")
    print(f"   • OpenAI Agents SDK - Multi-agent orchestration")
    print(f"   • Cognitora - Secure Python code execution")
    print(f"   • OpenAI GPT-4o - Advanced reasoning\n")
    
    print(f"{Colors.YELLOW}🎯 DEMONSTRATION:{Colors.ENDC}")
    print(f"   Watch autonomous agents collaborate to solve complex research tasks!")
    print(f"   Each agent has specialized skills and can call other agents.\n")
    
    # Validate API keys
    if not OPENAI_API_KEY:
        print(f"{Colors.RED}❌ Error: OPENAI_API_KEY not set{Colors.ENDC}")
        return
    
    if not COGNITORA_API_KEY:
        print(f"{Colors.RED}❌ Error: COGNITORA_API_KEY not set{Colors.ENDC}")
        return
    
    # Create multi-agent system
    print(f"{Colors.DIM}🔧 Initializing multi-agent system...{Colors.ENDC}")
    master, analyst, statistician, writer = create_multi_agent_system()
    print(f"{Colors.GREEN}✅ Multi-agent system ready!{Colors.ENDC}\n")
    
    print(f"{Colors.CYAN}{'═' * 80}{Colors.ENDC}\n")
    
    # ========================================================================
    # RESEARCH TASK 1: E-commerce Sales Analysis
    # ========================================================================
    
    print_agent_header("RESEARCH TASK 1", "E-commerce Sales Analysis", "📊")
    
    task1 = """Calculate total Q4 2024 e-commerce performance and growth rates:

DATA:
- October: 1,247 orders, $89,342 revenue
- November: 1,589 orders, $124,567 revenue  
- December: 2,834 orders, $267,891 revenue

CALCULATE:
1. Total Q4 orders and revenue
2. Month-over-month growth rates (orders and revenue)
3. Average order value trend

Write Python code and MUST print() all results with clear labels!"""

    print(f"\n{Colors.BOLD}📋 Research Request:{Colors.ENDC}")
    print(f"{Colors.DIM}{task1}{Colors.ENDC}\n")
    
    print(f"{Colors.YELLOW}🤖 Master Orchestrator delegating to specialist agents...{Colors.ENDC}\n")
    
    start_time = time.time()
    result1 = await Runner.run(master, input=task1)
    duration1 = time.time() - start_time
    
    print(f"\n{Colors.GREEN}{'─' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}📊 FINAL RESEARCH REPORT:{Colors.ENDC}")
    print(f"{Colors.GREEN}{'─' * 80}{Colors.ENDC}\n")
    print(result1.final_output)
    
    print(f"\n{Colors.DIM}⏱️  Analysis completed in {duration1:.1f}s{Colors.ENDC}")
    
    # ========================================================================
    # RESEARCH TASK 2: A/B Test Analysis
    # ========================================================================
    
    print_agent_header("RESEARCH TASK 2", "A/B Test Statistical Analysis", "🧪")
    
    task2 = """Analyze A/B test results for checkout button color:

DATA:
- Control (Blue): 2,450 visitors, 186 conversions
- Variant (Green): 2,528 visitors, 221 conversions

CALCULATE using Python (MUST print() all results):
1. Conversion rates for both variants
2. Absolute and relative improvement
3. Chi-square test for statistical significance
4. Clear recommendation (roll out or not)

Show all calculations with print() statements!"""

    print(f"\n{Colors.BOLD}📋 Research Request:{Colors.ENDC}")
    print(f"{Colors.DIM}{task2}{Colors.ENDC}\n")
    
    print(f"{Colors.YELLOW}🤖 Master Orchestrator delegating to specialist agents...{Colors.ENDC}\n")
    
    start_time = time.time()
    result2 = await Runner.run(master, input=task2)
    duration2 = time.time() - start_time
    
    print(f"\n{Colors.GREEN}{'─' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}📊 FINAL RESEARCH REPORT:{Colors.ENDC}")
    print(f"{Colors.GREEN}{'─' * 80}{Colors.ENDC}\n")
    print(result2.final_output)
    
    print(f"\n{Colors.DIM}⏱️  Analysis completed in {duration2:.1f}s{Colors.ENDC}")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    
    total_time = duration1 + duration2
    
    print(f"\n{Colors.CYAN}{'═' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ ALL RESEARCH TASKS COMPLETED{Colors.ENDC}")
    print(f"{Colors.CYAN}{'═' * 80}{Colors.ENDC}\n")
    
    print(f"{Colors.YELLOW}📊 Session Summary:{Colors.ENDC}")
    print(f"   • Research tasks completed: 2")
    print(f"   • Total analysis time: {total_time:.1f}s")
    print(f"   • Agents collaborated autonomously")
    print(f"   • Code executed securely in Cognitora sandbox\n")
    
    print(f"{Colors.GREEN}✨ This demonstrates:{Colors.ENDC}")
    print(f"   ✅ Multi-agent collaboration (agents calling agents)")
    print(f"   ✅ Specialized agent roles (analyst, statistician, writer)")
    print(f"   ✅ Autonomous task decomposition and delegation")
    print(f"   ✅ Code execution via Cognitora sandbox")
    print(f"   ✅ Complex data science workflows\n")
    
    print(f"{Colors.CYAN}🚀 Try other examples:{Colors.ENDC}")
    print(f"   • 1-example-basic-tasks.py - Basic agentic tasks")
    print(f"   • 3-example-stock-analyst.py - ML stock predictions")
    print(f"   • 4-example-live-crypto-tracker.py - Live data from internet")
    print(f"   • 6-example-data-visualization.py - File upload & charts\n")


if __name__ == "__main__":
    asyncio.run(main())

