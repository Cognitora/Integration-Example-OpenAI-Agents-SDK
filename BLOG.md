# Building Autonomous AI Agents with OpenAI Agents SDK and Cognitora

**The perfect marriage of intelligent agents and secure code execution**

---

## TL;DR

We built a production-ready integration combining [OpenAI's Agents SDK](https://openai.github.io/openai-agents-python/) with [Cognitora's secure sandbox](https://cognitora.dev) to create truly autonomous AI agents that can write and execute code safely. This isn't just another LLM wrapper—it's a complete framework for building AI systems that actually *do things* in the real world.

**Jump to:** [Why This Matters](#why-this-matters) • [The Architecture](#the-architecture) • [Live Examples](#what-we-built) • [Try It Yourself](#get-started)

---

## The Problem: Bridging Intelligence and Action

Large Language Models are brilliant at reasoning and planning. They can analyze complex problems, break them into steps, and generate sophisticated code. But here's the catch: **they can't execute that code themselves.**

This is where most AI applications hit a wall. You have two bad options:
1. **Run AI-generated code locally** (dangerous, unsandboxed, security nightmare)
2. **Don't execute code at all** (safe but severely limited)

We needed a third option: **secure, isolated, production-ready code execution that AI agents can use autonomously.**

---

## The Solution: OpenAI Agents SDK + Cognitora

### OpenAI Agents SDK: Intelligence Layer

The [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) is OpenAI's official framework for building agentic AI applications. It's the production-ready evolution of Swarm, designed with simplicity and power in mind.

**Why we chose it:**
- ✅ **Minimal abstractions** - Agent, Handoffs, Guardrails, Sessions. That's it.
- ✅ **Python-first design** - Use native Python patterns, not a new DSL
- ✅ **Built-in tracing** - Visualize, debug, and optimize agent workflows
- ✅ **Multi-agent orchestration** - Agents that delegate to specialized agents
- ✅ **Provider agnostic** - Works with OpenAI, and 100+ LLMs via LiteLLM

```python
from agents import Agent, Runner

agent = Agent(
    name="DataAnalyst",
    instructions="You analyze data and provide insights",
    tools=[your_custom_tools]
)

result = await Runner.run(agent, "Analyze Q4 sales trends")
```

### Cognitora: Execution Layer

[Cognitora](https://cognitora.dev) is an enterprise-grade code execution platform built specifically for AI agents. It provides isolated sandboxes with:

- ⚡ **Sub-second cold starts** - No waiting for containers
- 🔒 **Military-grade isolation** - Every execution is completely sandboxed
- 🌐 **Configurable networking** - Enable/disable internet access per execution
- 📦 **Multi-language support** - Python, JavaScript, Bash, and more
- 💾 **File operations** - Upload data, generate files, download results
- 🚀 **Production-ready** - Built for scale, not just prototypes

```python
from cognitora import Cognitora

client = Cognitora(api_key=os.environ["COGNITORA_API_KEY"])

result = client.run(
    code="import numpy as np\nprint(np.mean([1,2,3,4,5]))",
    language="python",
    enable_networking=True  # Optional: for API calls
)
```

---

## The Architecture

Here's how these pieces work together:

```
┌─────────────────────────────────────────────────────┐
│  User: "Analyze AAPL stock and predict next week"   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│         OpenAI Agents SDK (Intelligence)            │
│  • Understands intent                               │
│  • Plans approach                                   │
│  • Generates Python code                            │
│  • Decides when to use tools                        │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│        execute_code Tool (Integration Layer)        │
│  • Validates code                                   │
│  • Wraps Cognitora API                              │
│  • Handles errors gracefully                        │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│           Cognitora (Execution Layer)               │
│  • Spins up isolated sandbox                        │
│  • Executes code securely                           │
│  • Captures output/errors                           │
│  • Returns results                                  │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Output: "AAPL trading at $252.29                   │
│          Predicted: +4.99% growth                   │
│          Recommendation: BUY 🟢"                     │
└─────────────────────────────────────────────────────┘
```

### The Integration: execute_code Tool

The magic happens in our custom tool that bridges both platforms:

```python
async def execute_code(
    code: str,
    language: Literal["python", "javascript", "bash"],
    enable_networking: bool = False
) -> str:
    """
    Execute code in a secure Cognitora sandbox.
    
    The AI agent can call this tool to run any code it generates.
    """
    client = Cognitora(api_key=os.environ["COGNITORA_API_KEY"])
    
    result = client.run(
        code=code,
        language=language,
        enable_networking=enable_networking
    )
    
    if result.exit_code == 0:
        return f"✅ Success:\n{result.output}"
    else:
        return f"❌ Error:\n{result.stderr}"
```

This simple interface gives AI agents the superpower of code execution without any security compromises.

---

## What We Built

We created **6 production-ready examples** that showcase what's possible when intelligence meets secure execution:

### 1️⃣ **Agentic Task Automation** ([1-example-basic-tasks.py](https://github.com/Cognitora/Integration-Example-OpenAI-Agents-SDK/blob/main/1-example-basic-tasks.py))

8 autonomous tasks demonstrating goal-oriented problem solving:
- 💼 Sales analysis with ML predictions
- 🔢 Prime number generation
- 💰 Financial calculations
- 📊 Statistical analysis
- 🔐 Password generation

**The agentic approach:**
```
❌ Traditional: "Use pandas to load CSV, calculate mean, plot graph"
✅ Agentic: "Analyze my sales data and predict January revenue"
```

The agent figures out *how* to solve it. You just provide the *what*.

![Agentic Task Automation Demo](https://raw.githubusercontent.com/Cognitora/Integration-Example-OpenAI-Agents-SDK/main/screencast/demo1.gif)

### 2️⃣ **Interactive AI Chat** ([2-example-interactive.py](https://github.com/Cognitora/Integration-Example-OpenAI-Agents-SDK/blob/main/2-example-interactive.py))

Natural language interface with real-time code execution:
- 💬 Ask questions in plain English
- 🎨 Beautiful terminal UI
- ⚡ Instant code generation and execution
- 📊 Session statistics

```
You: "Calculate compound interest on $5000 at 6% for 10 years"
AI:  *writes Python code* → *executes* → "$8,954.24"
```

### 3️⃣ **Stock Market Analyst** 📈 ([3-example-stock-analyst.py](https://github.com/Cognitora/Integration-Example-OpenAI-Agents-SDK/blob/main/3-example-stock-analyst.py))

**This is where it gets serious.** A fully autonomous financial analyst that:
- 📊 Fetches real stock data (Yahoo Finance API)
- 🤖 Applies machine learning (linear regression)
- 📈 Generates 10-day price predictions
- 💡 Provides investment recommendations
- 📝 Creates professional markdown reports

**Output:** `stock_analysis_20251018_120315.md` with complete analysis, predictions, and actionable insights.

![Stock Market Analyst Demo](https://raw.githubusercontent.com/Cognitora/Integration-Example-OpenAI-Agents-SDK/main/screencast/demo3.gif)

### 4️⃣ **Live Crypto Tracker** 🌐 ([4-example-live-crypto-tracker.py](https://github.com/Cognitora/Integration-Example-OpenAI-Agents-SDK/blob/main/4-example-live-crypto-tracker.py))

AI agents with internet access—safely:
- 🌐 Networking enabled in sandbox
- 💰 Fetches live crypto prices (CoinGecko API)
- 📈 Analyzes portfolio value
- 💡 Provides investment advice

**Security note:** Networking is *optional* and *configurable*. Only enable it when needed.

![Live Crypto Tracker Demo](https://raw.githubusercontent.com/Cognitora/Integration-Example-OpenAI-Agents-SDK/main/screencast/demo4.gif)

### 5️⃣ **Multi-Agent Research System** 🤖 ([5-example-multi-agent-research.py](https://github.com/Cognitora/Integration-Example-OpenAI-Agents-SDK/blob/main/5-example-multi-agent-research.py))

**The future of AI:** Multiple specialized agents collaborating:

```
    Master Orchestrator
           ↓
    ┌──────┴──────┐
    ↓             ↓
Data Analyst   Statistician
(Python code)  (Advanced stats)
           ↘     ↙
        Report Writer
```

Each agent has specialized knowledge and tools. The orchestrator decides which specialist to delegate to. All agents can execute code via Cognitora.

**Use cases:**
- E-commerce analysis with growth projections
- A/B test statistical significance
- Customer segmentation and LTV calculation

![Multi-Agent Research System Demo](https://raw.githubusercontent.com/Cognitora/Integration-Example-OpenAI-Agents-SDK/main/screencast/demo5.gif)

### 6️⃣ **Data Visualization Pipeline** 📊 ([6-example-data-visualization.py](https://github.com/Cognitora/Integration-Example-OpenAI-Agents-SDK/blob/main/6-example-data-visualization.py))

Complete file upload → analysis → chart generation → download workflow:
- 📄 Upload CSV data to sandbox
- 🤖 AI analyzes and identifies insights
- 📊 Generates 4 professional charts (matplotlib)
- ⬇️ Downloads all files to local filesystem

**Output:** 4 beautiful visualizations saved to `output_charts/`

![Data Visualization Pipeline Demo](https://raw.githubusercontent.com/Cognitora/Integration-Example-OpenAI-Agents-SDK/main/screencast/demo6.gif)

---

## Why This Integration is Powerful

### 1. **True Autonomy**

Traditional AI: *"Here's some code to solve your problem"*  
Our integration: *"Here's the solution. I ran the code and verified it works."*

The agent doesn't just generate code—it executes it, checks results, and iterates until it works.

### 2. **Production-Ready Security**

Running AI-generated code is scary. Cognitora makes it safe:
- ✅ Complete isolation from your infrastructure
- ✅ No access to your filesystem (unless explicitly provided)
- ✅ Configurable networking (disabled by default)
- ✅ Resource limits prevent runaway processes
- ✅ Every execution is a fresh, clean environment

### 3. **Multi-Agent Workflows**

OpenAI Agents SDK's handoff system + Cognitora's execution = powerful orchestration:

```python
# Data Analyst agent can delegate to Statistician
statistician = Agent(
    name="Statistician",
    instructions="You perform advanced statistical analysis",
    tools=[execute_code]
)

analyst = Agent(
    name="DataAnalyst",
    instructions="You analyze data and delegate complex stats",
    tools=[execute_code],
    handoff_to=[statistician]
)
```

Each specialist agent can execute code independently. The orchestrator coordinates them.

### 4. **Real-World Data Integration**

Enable networking in Cognitora, and suddenly your agents can:
- 🌐 Fetch live data from APIs
- 💰 Get real-time market prices
- 🗺️ Access geographic data
- 🔬 Pull research papers
- 📊 Query public datasets

All while remaining sandboxed and secure.

### 5. **Iterative Refinement**

The agent loop handles failures gracefully:

1. Generate code
2. Execute in Cognitora
3. Check output
4. If error → analyze error → generate fix → retry
5. If success → continue with result

This isn't scripted error handling—the LLM reasons about errors and fixes them autonomously.

---

## Real-World Use Cases

This integration pattern unlocks entirely new categories of AI applications:

### 🤖 **Autonomous Data Analysis**
Upload a CSV, ask questions, get insights with charts. The agent handles data cleaning, statistical tests, and visualization—completely autonomously.

### 💼 **Financial Advisors**
Real-time market analysis, predictive modeling, portfolio optimization. All with live data and transparent calculations.

### 🔬 **Research Assistants**
Multi-agent systems that can search, analyze, compute statistics, and write comprehensive reports—all backed by real code execution.

### 📊 **Business Intelligence**
Natural language queries that generate SQL, fetch data, perform analysis, and create executive-ready reports.

### 🎓 **Educational Platforms**
Interactive coding tutors that can run student code, analyze errors, and provide guided debugging—safely sandboxed.

### 🤝 **Customer Support**
Agents that can actually *do* things: run diagnostics, generate reports, process refunds, update databases—not just chat.

---

## The Code: Clean and Simple

Here's the complete integration (simplified):

```python
import os
from agents import Agent, Runner
from cognitora import Cognitora

# Initialize Cognitora client
cognitora_client = Cognitora(api_key=os.environ["COGNITORA_API_KEY"])

async def execute_code(
    code: str,
    language: str = "python",
    enable_networking: bool = False
) -> str:
    """Execute code securely in Cognitora sandbox."""
    result = cognitora_client.run(
        code=code,
        language=language,
        enable_networking=enable_networking
    )
    return result.output if result.exit_code == 0 else result.stderr

# Create an agent with code execution superpower
agent = Agent(
    name="CodeExecutor",
    model="gpt-4o",
    instructions="You can write and execute code to solve problems.",
    tools=[execute_code]
)

# Give it a complex task
result = await Runner.run(
    agent, 
    "Fetch live Bitcoin price and predict next week's trend using linear regression"
)

print(result.final_output)
```

That's it. **~30 lines of code** for a fully autonomous AI agent that can write and execute code safely.

---

## Performance & Scale

### Speed
- **Cognitora cold start:** <500ms
- **Code execution:** Depends on code (typically <2s)
- **Full agent loop:** 5-15s for complex tasks

### Cost
- **OpenAI API:** $0.002-0.015 per request (GPT-4o)
- **Cognitora:** Pay-per-execution, starting at $0.001 per run
- **Total:** ~$0.01-0.05 per autonomous task

### Scale
- **Concurrent executions:** Unlimited (Cognitora handles load)
- **Agent instances:** Stateless, scale horizontally
- **Session management:** Built into Agents SDK

---

## Get Started

### Prerequisites
- Python `>=3.10.0, <3.13.0`
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Cognitora API key ([sign up here](https://cognitora.dev/home/api-keys))

### Quick Setup (2 minutes)

```bash
# Clone the repo
git clone https://github.com/Cognitora/Integration-Example-OpenAI-Agents-SDK.git
cd Integration-Example-OpenAI-Agents-SDK

# Install dependencies
pip install -r requirements.txt

# Set your API keys
export OPENAI_API_KEY="sk-your-key-here"
export COGNITORA_API_KEY="cgk-your-key-here"

# Run examples
python 1-example-basic-tasks.py
python 3-example-stock-analyst.py
python 5-example-multi-agent-research.py
```

### Try Each Example

| Example | Description | Complexity |
|---------|-------------|------------|
| **Example 1** | Basic agentic tasks | ⭐ Beginner |
| **Example 2** | Interactive chat | ⭐ Beginner |
| **Example 3** | Stock analyst (ML) | ⭐⭐⭐ Advanced |
| **Example 4** | Live crypto data | ⭐⭐ Intermediate |
| **Example 5** | Multi-agent system | ⭐⭐⭐ Advanced |
| **Example 6** | Data visualization | ⭐⭐ Intermediate |

---

## Why Choose Cognitora?

### Built for AI Agents, Not Just Code Execution

Cognitora was designed from the ground up for agentic AI workflows:

✅ **AI-Native API**  
Simple, intuitive interface that LLMs can use autonomously

✅ **Error Messages That LLMs Understand**  
Clear, actionable error messages that agents can reason about and fix

✅ **Predictable Behavior**  
Consistent environments mean agents learn and improve over time

✅ **Production-Ready from Day One**  
No "scale this later" surprises—it just works at any volume

✅ **File Operations**  
Upload data, generate reports, download results—full filesystem support

✅ **Multi-Language Support**  
Python, JavaScript, Bash—let agents choose the right tool

### Enterprise-Grade Security

- 🔒 **Isolated Sandboxes** - Complete isolation per execution
- 🛡️ **No Persistent State** - Fresh environment every time
- 🚦 **Network Controls** - Granular control over internet access
- 📊 **Audit Logs** - Full visibility into what code ran and when
- 💼 **SOC2 Compliant** - Enterprise security standards

### Developer Experience

```python
from cognitora import Cognitora

client = Cognitora(api_key="cgk-...")

# That's it. You're ready to execute code.
result = client.run(code="print('Hello, World!')", language="python")
```

No Docker. No K8s. No infrastructure headaches. Just code execution that works.

---

## Join the Agentic Revolution

We're at an inflection point in AI development. The combination of:
- 🧠 **Intelligent reasoning** (LLMs like GPT-4o)
- 🤖 **Agentic frameworks** (OpenAI Agents SDK)
- ⚡ **Secure execution** (Cognitora)

...unlocks a new category of applications that can truly understand *and act* autonomously.

### Start Building Today

🚀 **Try Cognitora Free:** [cognitora.dev/home/api-keys](https://cognitora.dev/home/api-keys)

📚 **Explore the Integration:** [github.com/Cognitora/Integration-Example-OpenAI-Agents-SDK](https://github.com/Cognitora/Integration-Example-OpenAI-Agents-SDK)

📖 **OpenAI Agents SDK Docs:** [openai.github.io/openai-agents-python](https://openai.github.io/openai-agents-python/)

💬 **Questions? Ideas?** Open an issue on GitHub or reach out to our team

---

## What Will You Build?

The examples in this repo are just the beginning. We've seen developers build:
- 📊 Autonomous business analysts that generate weekly reports
- 🤖 Trading bots that analyze markets and execute strategies
- 🔬 Research assistants that process datasets and write papers
- 🎓 Educational platforms with AI tutors that debug student code
- 💼 Internal tools that turn natural language into database queries

**The only limit is your imagination.**

Start with our examples, modify them, extend them, and build something amazing.

---

## Technical Resources

- **GitHub Repository:** [Integration-Example-OpenAI-Agents-SDK](https://github.com/Cognitora/Integration-Example-OpenAI-Agents-SDK)
- **OpenAI Agents SDK:** [Documentation](https://openai.github.io/openai-agents-python/)
- **Cognitora Platform:** [Website](https://cognitora.dev)
- **Cognitora Dashboard:** [API Keys](https://cognitora.dev/home/api-keys)

---

## About This Integration

This integration was built to demonstrate production-ready patterns for combining intelligent AI agents with secure code execution. All code is open source and production-ready. Use it as:
- 📚 **Learning resource** for agentic AI development
- 🏗️ **Starting point** for your own applications
- 🎓 **Reference implementation** for best practices

---

**Built with ❤️ by the Cognitora team**

*Making AI agents safe, powerful, and production-ready—one execution at a time.*

---

### Call to Action

Ready to add autonomous code execution to your AI agents?

🎯 **Get Started in 60 Seconds:**
1. Sign up at [cognitora.dev](https://cognitora.dev/home/api-keys)
2. Get your API key (starts with `cgk_`)
3. Run the examples: `python 1-example-basic-tasks.py`

💡 **Have Questions?** We're here to help. Open an issue or contact us through our website.

🚀 **Share What You Build!** We'd love to see what you create with this integration. Tag us or open a PR with your examples.

---

*Last updated: October 2025*

