"""
🌐 LIVE Crypto Portfolio Tracker - REAL DATA FROM INTERNET
============================================================

This example demonstrates AGENTIC AI with REAL internet data:
- 🤖 AI AGENT decides HOW to fetch data (agentic approach)
- 🌐 Fetches LIVE cryptocurrency prices from free APIs
- 💰 Analyzes your portfolio autonomously
- 📊 Provides investment insights based on real market data

Agentic Approach:
- Give the agent GOALS, not step-by-step instructions
- AI figures out HOW to fetch and analyze data
- Demonstrates true AI autonomy with code execution
- Production-ready pattern for AI-powered apps
"""

import os
import time
import asyncio
from datetime import datetime
from agents import Agent, Runner, function_tool
from cognitora import Cognitora

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Get API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COGNITORA_API_KEY = os.getenv("COGNITORA_API_KEY")

# Initialize Cognitora client
cognitora_client = Cognitora(api_key=COGNITORA_API_KEY)

# ANSI Colors
class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


@function_tool
def execute_code_with_network(code: str, language: str = "python") -> str:
    """
    Execute code with NETWORKING ENABLED to fetch real data from internet.
    
    Args:
        code: The code to execute
        language: Programming language (python, javascript, bash)
    
    Returns:
        The execution result including output and any errors
    """
    try:
        # Execute code with networking enabled
        result = cognitora_client.code_interpreter.execute(
            code=code,
            language=language,
            networking=True  # ✅ ENABLE NETWORKING for real API calls
        )
        
        # Check execution status
        status = result.data.status
        if status == "error" or status == "failed":
            return f"Execution failed with status: {status}"
        
        # Extract outputs
        output_lines = []
        error_lines = []
        
        for output_item in result.data.outputs:
            if output_item.type == "stdout":
                output_lines.append(output_item.data)
            elif output_item.type == "stderr":
                error_lines.append(output_item.data)
        
        # Format response
        result_parts = []
        if output_lines:
            result_parts.append("\n".join(output_lines))
        if error_lines:
            result_parts.append(f"Errors:\n" + "\n".join(error_lines))
        
        if result_parts:
            return "\n\n".join(result_parts)
        else:
            return f"Code executed successfully (status: {status}) but produced no output."
    
    except Exception as e:
        return f"Error executing code: {str(e)}"


def print_header():
    """Print header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{' ' * 78}║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.ENDC}  {Colors.BOLD}🌐 LIVE CRYPTO PORTFOLIO TRACKER{Colors.ENDC}                                     {Colors.BOLD}{Colors.CYAN}║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{' ' * 78}║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.ENDC}  {Colors.GREEN}Fetching REAL data from the internet in real-time!{Colors.ENDC}                  {Colors.BOLD}{Colors.CYAN}║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{' ' * 78}║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 80}{Colors.ENDC}\n")


def print_section(title, emoji="📊"):
    """Print section separator"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{emoji} {title}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'─' * 80}{Colors.ENDC}\n")


async def main():
    """Run live crypto portfolio analysis with AGENTIC approach"""
    
    # Check API keys
    if not OPENAI_API_KEY or not COGNITORA_API_KEY:
        print(f"{Colors.RED}❌ Error: API keys not set{Colors.ENDC}")
        print(f"{Colors.YELLOW}Please set OPENAI_API_KEY and COGNITORA_API_KEY{Colors.ENDC}")
        return
    
    # Initialize AI agent
    print(f"{Colors.DIM}Initializing AI agent with GPT-4o...{Colors.ENDC}")
    agent = Agent(
        name="CryptoAnalyst",
        model="gpt-4o",
        instructions="You are a helpful cryptocurrency analyst that can fetch live data and analyze portfolios.",
        tools=[execute_code_with_network]
    )
    
    print_header()
    
    # User's crypto holdings
    portfolio = {
        "bitcoin": 0.5,      # 0.5 BTC
        "ethereum": 3.2,     # 3.2 ETH
        "cardano": 5000,     # 5000 ADA
    }
    
    print(f"{Colors.BOLD}💼 YOUR CRYPTO HOLDINGS:{Colors.ENDC}\n")
    print(f"{'Cryptocurrency':<20} {'Holdings':<15}")
    print(f"{Colors.DIM}{'─' * 40}{Colors.ENDC}")
    for crypto, amount in portfolio.items():
        print(f"{crypto.title():<20} {amount:<15,.4f}")
    print(f"{Colors.DIM}{'─' * 40}{Colors.ENDC}\n")
    
    print(f"{Colors.YELLOW}🌐 AI Agent working autonomously...{Colors.ENDC}\n")
    
    # AGENTIC APPROACH: Give the agent a GOAL, not step-by-step instructions
    print_section("🤖 AGENTIC TASK: Analyze My Portfolio", "🎯")
    
    query = f"""Analyze my crypto portfolio: {portfolio}

Fetch LIVE prices from CoinGecko API and analyze.
API: https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,cardano&vs_currencies=usd&include_24hr_change=true

Write Python code using only urllib and json (built-in).
Calculate: total value, biggest holding, 24h changes.

CRITICAL: Use print() to display ALL results with labels.
Show: current prices, total portfolio value, biggest position, 24h price changes."""
    
    print(f"{Colors.DIM}🤖 AI Agent analyzing portfolio autonomously...{Colors.ENDC}\n")
    start = time.time()
    result = await Runner.run(agent, input=query)
    print(f"{Colors.GREEN}✓ Analysis complete ({time.time()-start:.1f}s){Colors.ENDC}\n")
    print(result.final_output)
    
    # Second agentic task: Investment recommendation
    print_section("🤖 AGENTIC TASK: Investment Recommendation", "💡")
    
    query2 = f"""Give me investment advice for my portfolio: {portfolio}

Task: Fetch top 5 cryptos by market cap and compare to my holdings.
API: https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1

Write Python code with urllib and json.
Analyze: which top coins I'm missing, if I should diversify.

CRITICAL: Use print() to show:
- Top 5 cryptos by market cap
- Which ones I own vs don't own
- Specific buy/sell/hold recommendations
- Diversification advice

Print everything with clear labels!"""
    
    print(f"{Colors.DIM}🤖 AI Agent generating investment strategy...{Colors.ENDC}\n")
    start = time.time()
    result2 = await Runner.run(agent, input=query2)
    print(f"{Colors.GREEN}✓ Recommendations ready ({time.time()-start:.1f}s){Colors.ENDC}\n")
    print(result2.final_output)
    
    # Final Summary
    print(f"\n{Colors.BOLD}{Colors.GREEN}✅ LIVE CRYPTO ANALYSIS COMPLETE!{Colors.ENDC}")
    print(f"{Colors.DIM}Agentic AI with REAL internet data (networking enabled){Colors.ENDC}")
    print(f"{Colors.YELLOW}💡 Run again to see updated live prices!{Colors.ENDC}\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Analysis interrupted{Colors.ENDC}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.ENDC}")
        print(f"{Colors.DIM}Please check your API keys and internet connection.{Colors.ENDC}\n")

