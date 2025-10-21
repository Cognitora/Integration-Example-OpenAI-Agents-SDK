# 🤖 OpenAI Agents SDK + 🔒 Cognitora Integration

**Agentic AI that autonomously writes and executes code to solve real-world problems!**

A complete working example integrating [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) (official OpenAI agentic AI framework) with [Cognitora](https://cognitora.dev) (secure code execution sandbox). Give the AI a goal, and it figures out how to write and execute code to achieve it.

## 🌟 What This Does

This example showcases **agentic AI** that autonomously writes and executes code in Python, JavaScript, and Bash to achieve goals you give it. The AI figures out how to solve problems without step-by-step instructions, can fetch real data from live APIs, and runs securely in an isolated Cognitora sandbox using production-ready patterns.

## 🚀 Key Features

### Agentic Approach 
- **AI autonomy** - Agent decides HOW to solve problems
- **Dynamic code generation** - Writes code on the fly based on context
- **True intelligence** - Reasoning + action, not just scripted workflows

### OpenAI Agents SDK
- Official OpenAI framework for building autonomous AI applications
- Lightweight yet powerful multi-agent workflows
- Provider-agnostic (OpenAI, LiteLLM for 100+ LLMs)
- Built-in tracing, sessions, and guardrails

### Cognitora Sandbox ([cognitora.dev](https://www.cognitora.dev))
Enterprise-grade secure code execution platform with isolated sandboxes for Python, JavaScript, and Bash. Features configurable networking, file operations, sub-second cold starts, and a simple Python SDK. Purpose-built for AI agents that need to safely execute untrusted or dynamically-generated code in production.

## 📋 Prerequisites

- Python `>=3.10.0, <3.13.0`
- **OpenAI API key** - [Get one here](https://platform.openai.com/api-keys)
- **Cognitora API key** - [Sign up and get yours here](https://www.cognitora.dev/home/api-keys)

## 🛠️ Installation

### Quick Setup (4 Steps!)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get your API keys:**
   
   **OpenAI API Key:**
   - Sign up at [OpenAI Platform](https://platform.openai.com/)
   - Go to [API Keys](https://platform.openai.com/api-keys)
   - Click "Create new secret key"
   - Copy your key (starts with `sk-`)
   
   **Cognitora API Key:**
   - Sign up at [Cognitora Dashboard](https://www.cognitora.dev/home/api-keys)
   - Navigate to API Keys section
   - Create a new API key
   - Copy your key (starts with `cgk_`)

3. **Set your API keys:**
   
   Option A - Environment variables:
   ```bash
   export OPENAI_API_KEY="sk-your-openai-api-key-here"
   export COGNITORA_API_KEY="cgk-your-cognitora-api-key-here"
   ```
   
   Option B - Create a `.env` file:
   ```bash
   # Create .env file with both keys
   cat > .env << EOF
   OPENAI_API_KEY=sk-your-openai-api-key-here
   COGNITORA_API_KEY=cgk-your-cognitora-api-key-here
   EOF
   ```
   
   Or copy from template:
   ```bash
   cp env_template.txt .env
   # Then edit .env and add your actual API keys
   ```

4. **Run the demo:**
   ```bash
   python 1-example-basic-tasks.py
   ```

---

## 📚 **Example Files**

The project includes 6 example scripts demonstrating different capabilities:

### 1️⃣ `1-example-basic-tasks.py` - Agentic AI Basics
**8 goal-oriented tasks** demonstrating autonomous code execution:

**Agentic Pattern:**
- "GOAL: Analyze my sales and predict January"

**Tasks:**
- 💼 Sales analysis & prediction (Python)
- 🔢 Prime number finder (Python)
- 💰 Compound interest calculator (Python)
- 📊 Statistical analysis (Python)
- 🔐 Password generator (Python)
- 🔢 Fibonacci sequence (Python)
- 📝 String analysis (JavaScript)
- 📅 Date operations (Bash)

**Run it:**
```bash
python 1-example-basic-tasks.py
```

**Demo:**

![Basic Tasks Demo](screencast/demo1.gif)

### 2️⃣ `2-example-interactive.py` - Interactive Chat
**Chat with an agentic AI** that executes code to answer you:

**Features:**
- 💬 Natural conversation - Ask in plain English
- 🎨 Beautiful color-coded terminal UI
- ⚡ Real-time code execution
- 📊 Session statistics
- 💡 6 pre-loaded example prompts

**Example:**
- You: "Calculate compound interest on $5000 at 6% for 10 years"
- AI: *Writes Python code* → *Executes in sandbox* → *Returns result*

**Run it:**
```bash
python 2-example-interactive.py
```

### 3️⃣ `3-example-stock-analyst.py` - 📈 PREDICTIVE ANALYTICS ⭐⭐⭐
**Autonomous stock analyst with machine learning predictions + markdown reports!**

**Inspired by:** [Dynamiq's autonomous analyst](https://www.getdynamiq.ai/post/how-to-build-an-autonomous-data-analyst-using-dynamiq-e2b-and-together-ai)

**Advanced financial analysis:**
- 📊 **Real Stock Data** - Yahoo Finance API (free, no auth!)
- 🤖 **Linear Regression** - ML-based price prediction
- 📈 **10-Day Forecasts** - Predict future stock prices
- 🔍 **Multi-Stock Comparison** - AAPL vs MSFT analysis
- 💡 **Investment Recommendations** - Data-driven buy/hold/sell advice
- 📝 **Markdown Reports** - Professional analysis reports saved locally

**3 Autonomous Analyses:**
1. **Apple Stock Prediction** - 30-day history → 10-day forecast
2. **AAPL vs MSFT Comparison** - Which to invest in?
3. **Top Tech Stocks** - Analyze 5 stocks, rank by potential

**ML Techniques Used:**
- Linear regression for trend analysis
- Statistical metrics (mean, std dev, volatility)
- Predictive modeling
- Multi-variate comparison

**Output Report (saved to `output_analysis/`):**
```markdown
stock_analysis_YYYYMMDD_HHMMSS.md
├── Header (timestamp, powered-by)
├── Analysis 1: Apple Stock Prediction
├── Analysis 2: AAPL vs MSFT Comparison
├── Analysis 3: Tech Stocks Ranking
├── Summary (timing, completion status)
└── Disclaimer
```

**Example Output:**
- **Apple (AAPL):** $252.29 → +4.99% predicted (BUY 🟢)
- **NVIDIA (NVDA):** Best performer (+5.11% predicted)
- **Report:** `output_analysis/stock_analysis_20251018_120315.md` (~6 KB)

**Run it:**
```bash
python 3-example-stock-analyst.py
# Output: Markdown report saved to output_analysis/
```

**Demo:**

![Stock Analyst Demo](screencast/demo3.gif)

**Perfect for:**
- Algorithmic trading systems
- Financial analysis platforms
- Investment research tools
- Portfolio optimization
- Market trend prediction
- Automated report generation

### 4️⃣ `4-example-live-crypto-tracker.py` - 🌐 LIVE DATA ⭐
**AGENTIC AI with REAL internet data!**

**What makes this special:**
- 🌐 **Networking enabled** - Fetches live data from internet
- 💰 **Real crypto prices** - CoinGecko API (BTC, ETH, ADA)
- 📈 **Live 24h changes** - Actual market movements
- 🤖 **True autonomy** - AI decides how to fetch and analyze

**Agentic Pattern:**
- "GOAL: Analyze my crypto portfolio with live prices"
- AI figures out: API endpoint, data parsing, calculations

**2 Autonomous Tasks:**
1. Portfolio Analysis - Fetches live prices, calculates value
2. Investment Advice - Compares to top cryptos, recommends actions

**Run it:**
```bash
python 4-example-live-crypto-tracker.py
```

**Demo:**

![Live Crypto Tracker Demo](screencast/demo4.gif)

**Free APIs used:**
- CoinGecko - Live crypto market data (no auth!)
- Built-in urllib/json - No external libraries needed

### 5️⃣ `5-example-multi-agent-research.py` - 🤖 MULTI-AGENT SYSTEM ⭐⭐⭐
**ADVANCED: Multiple AI agents collaborating autonomously!**

**The Future of AI - Agents working together:**
- 🤖 **4 Specialized Agents** - Data Analyst, Statistician, Report Writer, Orchestrator
- 🔗 **Agent Collaboration** - Agents can call other agents autonomously
- 🧠 **Intelligent Delegation** - Master agent decides which specialist to use
- 💻 **Code Execution** - Agents write and run Python via Cognitora

**Architecture:**
```
    Master Orchestrator
           ↓
    ┌──────┴──────┐
    ↓             ↓
Data Analyst   Statistician
(Python Code)  (Advanced Stats)
           ↘     ↙
        Report Writer
```

**3 Research Tasks Solved Autonomously:**
1. **E-commerce Analysis** - Q4 performance, growth rates, projections
2. **A/B Test Analysis** - Statistical significance, chi-square test
3. **Customer Segmentation** - LTV calculation, ROI optimization

**Run it:**
```bash
python 5-example-multi-agent-research.py
```

**Demo:**

![Multi-Agent Research Demo](screencast/demo5.gif)

**Perfect for:**
- Data science automation
- Research and analysis platforms
- Multi-step decision making
- Complex business intelligence
- Autonomous research assistants

### 6️⃣ `6-example-data-visualization.py` - 📊 FILE UPLOAD & CHARTS ⭐
**Upload CSV data, AI analyzes it, generates charts, saves everything locally!**

**Complete data visualization workflow:**
- 📄 **CSV Data Creation** - Sample sales data with 20 rows
- 💾 **Local Storage** - Saves CSV to `output_charts/sales_data.csv`
- ☁️ **File Upload** - Upload data to Cognitora sandbox
- 🤖 **AI Analysis** - Agent analyzes data and creates insights
- 📊 **Chart Generation** - 4 professional visualizations (matplotlib/seaborn)
- ⬇️ **File Download** - Downloads all charts from sandbox to local filesystem

**4 Automated Visualizations (all saved to `output_charts/`):**
1. **revenue_by_category.png** - Bar chart with totals (~56 KB)
2. **revenue_by_region.png** - Regional performance analysis (~61 KB)
3. **top_products.png** - Horizontal bar chart of best sellers (~51 KB)
4. **daily_trend.png** - Line chart showing revenue over time (~95 KB)

**Output Files:**
```
output_charts/
├── sales_data.csv          (source data)
├── revenue_by_category.png
├── revenue_by_region.png
├── top_products.png
└── daily_trend.png
```

**Run it:**
```bash
python 6-example-data-visualization.py
# Output: CSV + 4 chart images saved to output_charts/
```

**Perfect for:**
- Automated reporting systems
- Business intelligence dashboards  
- Data analysis pipelines
- Chart generation services
- Excel/CSV processing automation

---

## 🎮 Usage

### Quick Start

```bash
# 1. Basic agentic tasks (8 examples)
python 1-example-basic-tasks.py

# 2. Interactive chat mode
python 2-example-interactive.py

# 3. Stock analyst with ML predictions (ADVANCED!)
python 3-example-stock-analyst.py

# 4. Live crypto data (internet access!)
python 4-example-live-crypto-tracker.py

# 5. Multi-agent research system (ADVANCED!)
python 5-example-multi-agent-research.py

# 6. Data visualization with file upload/download
python 6-example-data-visualization.py
```

### Interactive Mode Examples

Try natural language requests:

```
"Calculate compound interest on $5000 at 6% for 10 years"
"Generate 5 secure passwords with 16 characters"
"Find all prime numbers between 100 and 200"
"Analyze this data: [23, 45, 67, 12, 89]"
```

**The AI will:**
1. Understand your goal
2. Write appropriate code
3. Execute it securely
4. Return results

### Use as a Library

```python
import os
import asyncio
from agents import Agent, Runner
from importlib import import_module

# Import from the example file
basic_tasks = import_module('1-example-basic-tasks')
execute_code = basic_tasks.execute_code

# Initialize agent with GPT-4o
agent = Agent(
    name="CodeExecutor",
    model="gpt-4o",
    instructions="You are a helpful assistant that can execute code.",
    tools=[execute_code]
)

# Ask the agent to run code
async def main():
    result = await Runner.run(agent, input="Calculate the square root of 34534 using Python")
    print(result.final_output)

asyncio.run(main())
```

## 📝 Example Queries

Try asking the agent:

```python
# Mathematical
"Calculate the first 20 prime numbers"

# Data Analysis  
"Analyze this dataset and find the correlation: [1,2,3,4,5] and [2,4,6,8,10]"

# String Processing
"Using JavaScript, count the vowels in 'Hello World'"

# System Operations
"Show me today's date in ISO format using bash"

# Complex Problems
"Create a Python function to calculate BMI and test it with weight=70kg, height=1.75m"
```

## 🏗️ Architecture

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ OpenAI Agents   │
│   SDK Agent     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  execute_code   │
│      Tool       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Cognitora     │
│   Sandbox SDK   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Code Result    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Local Filesystem│
│ • output_charts/│
│ • output_analysis/│
└─────────────────┘
```

## 🔐 Security

- All code executes in Cognitora's **isolated sandbox**
- **Configurable networking** (default: disabled, enabled for examples 4 & 7)
- **Controlled file access** - Only `/tmp/` directory writable in sandbox
- **Local file operations** - Results downloaded and saved to controlled output directories
- Safe for untrusted or AI-generated code

## 📁 Output Directories

The examples generate output files in organized directories:

```
openai-agents-cognitora/
├── output_charts/          # Generated by example 6
│   ├── sales_data.csv     # Source data
│   ├── revenue_by_category.png
│   ├── revenue_by_region.png
│   ├── top_products.png
│   └── daily_trend.png
└── output_analysis/        # Generated by example 3
    └── stock_analysis_YYYYMMDD_HHMMSS.md
```

**Note:** These directories are automatically created and are excluded from git via `.gitignore`.

## 🎯 Use Cases

### Demonstrated Patterns:
1. **Agentic Task Automation** (Example 1) - Goal-oriented problem solving
2. **Conversational AI** (Example 2) - Chat interfaces with code execution
3. **Predictive Analytics** (Example 3) - ML-based stock predictions with report generation
4. **Live Data Integration** (Example 4) - Internet-connected AI agents
5. **Multi-Agent Collaboration** (Example 5) - Specialized agents working together
6. **Data Visualization** (Example 6) - File upload, chart generation, and download

### Real-World Applications:
- 🤖 **Autonomous Agents** - Goal-oriented AI that solves complex tasks
- 👥 **Multi-Agent Systems** - Specialized agents collaborating on complex problems
- 💼 **Robo-Advisors** - Financial planning with real-time calculations
- 📊 **Data Science Automation** - AI that writes and executes analysis code
- 🔬 **Research Assistants** - Multi-agent systems for thorough analysis
- 🎓 **Educational Platforms** - Interactive coding with real execution
- 📈 **Trading Bots** - Live market data analysis and decision making
- 💬 **AI Assistants** - Chat interfaces that execute code to help users
- 📝 **Report Generation** - Automated creation of analysis reports (markdown, charts)
- 📁 **File Operations** - Upload, process, and download files from secure sandbox

## 📚 Documentation

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK GitHub](https://github.com/openai/openai-agents-python)
- [Cognitora Dashboard](https://www.cognitora.dev/home/api-keys)

## 🤝 Contributing

Extend these examples with:
- **RAG systems** - Document retrieval and question answering
- **More agent types** - Code reviewers, debuggers, optimizers
- **Additional tools** - File operations, database queries, web scraping
- **Better error handling** - Retry logic, fallbacks, validation
- **Streaming responses** - Real-time updates for long tasks
- **Planning systems** - Long-term task planning and execution

## 📄 License

This example is provided as-is for educational and demonstration purposes.

## 🙋 Support

- **OpenAI Agents SDK**: [GitHub](https://github.com/openai/openai-agents-python)
- **Cognitora**: [Website](https://cognitora.dev)

---

**Built with ❤️ using OpenAI Agents SDK and Cognitora**
