#!/usr/bin/env python3
"""
📊 AI Data Visualization with File Upload/Download
===================================================

This example demonstrates ADVANCED FILE OPERATIONS:
- Creating and uploading CSV data to Cognitora
- AI agent analyzing data and generating charts
- Downloading generated visualizations
- Multi-chart analysis workflow

Features:
- File upload to Cognitora sandbox
- AI-powered data analysis
- Chart generation (matplotlib, seaborn)
- File download from sandbox
- Automated visualization workflow
"""

import os
import io
import csv
import time
import base64
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from cognitora import Cognitora, FileUpload

from agents import Agent, Runner, function_tool

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COGNITORA_API_KEY = os.getenv("COGNITORA_API_KEY")

# Initialize Cognitora client
cognitora_client = Cognitora(api_key=COGNITORA_API_KEY)

# ============================================================================
# ANSI COLORS
# ============================================================================

class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


# ============================================================================
# SAMPLE DATA GENERATION
# ============================================================================

# Global variable to store CSV content
csv_content = None

def create_sample_sales_data():
    """Create sample sales data CSV"""
    data = [
        ["Date", "Product", "Category", "Units_Sold", "Revenue", "Region"],
        ["2024-10-01", "Laptop", "Electronics", "15", "22500", "North"],
        ["2024-10-01", "Mouse", "Electronics", "45", "1350", "North"],
        ["2024-10-01", "Desk", "Furniture", "8", "3200", "South"],
        ["2024-10-02", "Laptop", "Electronics", "12", "18000", "South"],
        ["2024-10-02", "Chair", "Furniture", "20", "6000", "North"],
        ["2024-10-02", "Keyboard", "Electronics", "30", "2400", "East"],
        ["2024-10-03", "Laptop", "Electronics", "18", "27000", "East"],
        ["2024-10-03", "Monitor", "Electronics", "25", "12500", "West"],
        ["2024-10-03", "Desk", "Furniture", "10", "4000", "North"],
        ["2024-10-04", "Chair", "Furniture", "15", "4500", "South"],
        ["2024-10-04", "Mouse", "Electronics", "60", "1800", "East"],
        ["2024-10-04", "Keyboard", "Electronics", "40", "3200", "West"],
        ["2024-10-05", "Laptop", "Electronics", "20", "30000", "West"],
        ["2024-10-05", "Monitor", "Electronics", "30", "15000", "North"],
        ["2024-10-05", "Desk", "Furniture", "12", "4800", "East"],
        ["2024-10-06", "Chair", "Furniture", "25", "7500", "West"],
        ["2024-10-06", "Mouse", "Electronics", "50", "1500", "South"],
        ["2024-10-06", "Keyboard", "Electronics", "35", "2800", "North"],
        ["2024-10-07", "Laptop", "Electronics", "22", "33000", "North"],
        ["2024-10-07", "Monitor", "Electronics", "28", "14000", "East"],
    ]
    
    # Convert to CSV string
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(data)
    csv_content = output.getvalue()
    output.close()
    
    return csv_content


# ============================================================================
# TOOLS FOR AI AGENT
# ============================================================================

def download_file_from_sandbox(filename: str, local_path: str) -> bool:
    """
    Download a file from Cognitora sandbox to local filesystem.
    
    Args:
        filename: File path in sandbox (e.g., '/tmp/chart.png')
        local_path: Local path to save file (e.g., 'output/chart.png')
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get the file content from sandbox
        result = cognitora_client.code_interpreter.execute(
            code=f"""
import base64
import os

# Check if file exists
if not os.path.exists('{filename}'):
    print("ERROR: File not found")
else:
    with open('{filename}', 'rb') as f:
        content = f.read()
        encoded = base64.b64encode(content).decode('utf-8')
        print("BASE64_START")
        print(encoded)
        print("BASE64_END")
""",
            language="python",
            networking=False
        )
        
        # Extract the base64 content between markers
        for output_item in result.data.outputs:
            if output_item.type == "stdout":
                output = output_item.data
                
                # Check for error
                if "ERROR: File not found" in output:
                    print(f"   ⚠️  File not found in sandbox: {filename}")
                    return False
                
                # Extract base64 content between markers
                if "BASE64_START" in output and "BASE64_END" in output:
                    start = output.index("BASE64_START") + len("BASE64_START")
                    end = output.index("BASE64_END")
                    encoded_content = output[start:end].strip()
                    
                    decoded_content = base64.b64decode(encoded_content)
                    
                    # Save to local filesystem
                    os.makedirs(os.path.dirname(local_path) if os.path.dirname(local_path) else '.', exist_ok=True)
                    with open(local_path, 'wb') as f:
                        f.write(decoded_content)
                    return True
        
        return False
        
    except Exception as e:
        print(f"   ⚠️  Download error: {str(e)}")
        return False


@function_tool
def analyze_data_and_create_chart(chart_type: str, analysis_description: str, output_filename: str) -> str:
    """
    Analyze uploaded data and create a visualization chart.
    
    The sales data CSV is already available with these columns:
    - Date, Product, Category, Units_Sold, Revenue, Region
    
    This tool generates Python code to create charts from the pre-loaded CSV data.
    The code will be executed in Cognitora sandbox.
    
    CRITICAL RULES:
    1. The CSV has columns: Date, Product, Category, Units_Sold, Revenue, Region
    2. MUST use print() to show analysis results
    3. Save chart as PNG using plt.savefig('/tmp/{output_filename}')
    4. Use matplotlib and seaborn for visualizations
    5. Make charts professional and visually appealing
    
    Args:
        chart_type: Type of chart (bar, line, scatter, heatmap, pie, etc.)
        analysis_description: What analysis/insight to visualize
        output_filename: Name for the output PNG file (e.g., 'revenue_by_category.png')
    
    Returns:
        Analysis results and confirmation of chart generation
    """
    
    # Always use the global CSV content
    global csv_content
    csv_data = csv_content
    
    # Generate Python code for visualization
    # First, write the CSV data to a file in the sandbox
    code = f"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io

# Set style for professional charts (use simpler style for faster rendering)
plt.style.use('default')
sns.set_palette("husl")

# Write CSV data to /tmp directory (has write permissions)
import io
csv_content = '''{csv_data}'''
# Use StringIO to ensure proper parsing
df = pd.read_csv(io.StringIO(csv_content))

print("=" * 60)
print("DATA ANALYSIS: {analysis_description}")
print("=" * 60)
print(f"\\nDataset Shape: {{df.shape[0]}} rows, {{df.shape[1]}} columns")
print(f"\\nColumns: {{', '.join(df.columns.tolist())}}")
print(f"\\nFirst few rows:")
print(df.head())

# Analysis description: {analysis_description}
# Chart type: {chart_type}

# Create the visualization based on chart type
plt.figure(figsize=(10, 6), dpi=100)  # Reduced size and DPI for faster rendering

"""

    # Add specific chart code based on type
    if "revenue" in analysis_description.lower() and "category" in analysis_description.lower():
        code += """
# Revenue by Category Analysis
revenue_by_category = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
print(f"\\nRevenue by Category:")
for category, revenue in revenue_by_category.items():
    print(f"  {category}: ${revenue:,.2f}")

# Create bar chart
colors = sns.color_palette("husl", len(revenue_by_category))
bars = plt.bar(revenue_by_category.index, revenue_by_category.values, color=colors, edgecolor='black', linewidth=1.5)
plt.xlabel('Category', fontsize=14, fontweight='bold')
plt.ylabel('Total Revenue ($)', fontsize=14, fontweight='bold')
plt.title('Total Revenue by Product Category', fontsize=16, fontweight='bold', pad=20)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
            f'${height:,.0f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
"""
    
    elif "region" in analysis_description.lower():
        code += """
# Revenue by Region Analysis
revenue_by_region = df.groupby('Region')['Revenue'].sum().sort_values(ascending=False)
print(f"\\nRevenue by Region:")
for region, revenue in revenue_by_region.items():
    print(f"  {region}: ${revenue:,.2f}")

# Create bar chart
colors = sns.color_palette("Set2", len(revenue_by_region))
bars = plt.bar(revenue_by_region.index, revenue_by_region.values, color=colors, edgecolor='black', linewidth=1.5)
plt.xlabel('Region', fontsize=14, fontweight='bold')
plt.ylabel('Total Revenue ($)', fontsize=14, fontweight='bold')
plt.title('Total Revenue by Region', fontsize=16, fontweight='bold', pad=20)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
            f'${height:,.0f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
"""
    
    elif "product" in analysis_description.lower() and "top" in analysis_description.lower():
        code += """
# Top Products Analysis
product_revenue = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(5)
print(f"\\nTop 5 Products by Revenue:")
for i, (product, revenue) in enumerate(product_revenue.items(), 1):
    print(f"  {i}. {product}: ${revenue:,.2f}")

# Create horizontal bar chart
colors = sns.color_palette("coolwarm", len(product_revenue))
bars = plt.barh(range(len(product_revenue)), product_revenue.values, color=colors, edgecolor='black', linewidth=1.5)
plt.yticks(range(len(product_revenue)), product_revenue.index, fontsize=12)
plt.xlabel('Total Revenue ($)', fontsize=14, fontweight='bold')
plt.ylabel('Product', fontsize=14, fontweight='bold')
plt.title('Top 5 Products by Revenue', fontsize=16, fontweight='bold', pad=20)
plt.xticks(fontsize=12)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, product_revenue.values)):
    plt.text(value, i, f' ${value:,.0f}', 
            va='center', fontsize=11, fontweight='bold')

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
"""
    
    elif "trend" in analysis_description.lower() or "time" in analysis_description.lower():
        code += """
# Daily Revenue Trend
df['Date'] = pd.to_datetime(df['Date'])
daily_revenue = df.groupby('Date')['Revenue'].sum().sort_index()
print(f"\\nDaily Revenue Trend:")
for date, revenue in daily_revenue.items():
    print(f"  {date.strftime('%Y-%m-%d')}: ${revenue:,.2f}")

# Create line chart
plt.plot(daily_revenue.index, daily_revenue.values, marker='o', linewidth=3, 
        markersize=8, color='#2E86AB', markerfacecolor='#A23B72', markeredgecolor='white', markeredgewidth=2)
plt.xlabel('Date', fontsize=14, fontweight='bold')
plt.ylabel('Total Revenue ($)', fontsize=14, fontweight='bold')
plt.title('Daily Revenue Trend', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right', fontsize=11)
plt.yticks(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
"""
    
    else:
        # Default: Revenue by Category
        code += """
# Default Analysis: Revenue by Category
revenue_by_category = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
print(f"\\nRevenue by Category:")
for category, revenue in revenue_by_category.items():
    print(f"  {category}: ${revenue:,.2f}")

colors = sns.color_palette("husl", len(revenue_by_category))
plt.bar(revenue_by_category.index, revenue_by_category.values, color=colors)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Total Revenue ($)', fontsize=12)
plt.title('Revenue Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
"""
    
    # Add save command (save to /tmp directory)
    code += f"""
# Save the chart to /tmp directory (lower DPI for faster save)
print("\\nSaving chart...")
plt.savefig('/tmp/{output_filename}', dpi=150, bbox_inches='tight', facecolor='white', format='png')
plt.close()  # Close to free memory
print(f"✅ Chart saved as '/tmp/{output_filename}'")
print("=" * 60)
"""
    
    try:
        # Execute the code in Cognitora sandbox
        result = cognitora_client.code_interpreter.execute(
            code=code,
            language="python",
            networking=False
        )
        
        # Check execution status
        status = result.data.status
        if status == "error" or status == "failed":
            error_msgs = []
            for output_item in result.data.outputs:
                if output_item.type == "stderr":
                    error_msgs.append(output_item.data)
            return f"❌ Execution failed: {status}\n" + "\n".join(error_msgs)
        
        # Extract output
        output_lines = []
        error_lines = []
        for output_item in result.data.outputs:
            if output_item.type == "stdout":
                output_lines.append(output_item.data)
            elif output_item.type == "stderr":
                error_lines.append(output_item.data)
        
        result_text = ""
        if output_lines:
            result_text = "✅ Chart created successfully!\n\n" + "\n".join(output_lines)
        else:
            result_text = "⚠️ Chart created but no analysis output captured."
        
        if error_lines:
            result_text += "\n\n⚠️ Warnings/Errors:\n" + "\n".join(error_lines)
            
        return result_text
            
    except Exception as e:
        import traceback
        return f"❌ Error: {str(e)}\n{traceback.format_exc()}"


# ============================================================================
# MAIN DEMO
# ============================================================================

async def main():
    """Demonstrate file upload, AI analysis, and chart download"""
    
    print(f"\n{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("     📊 AI DATA VISUALIZATION WITH FILE UPLOAD/DOWNLOAD 📊")
    print(f"{Colors.ENDC}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")
    
    print(f"{Colors.GREEN}✨ POWERED BY:{Colors.ENDC}")
    print(f"   • OpenAI Agents SDK - Agentic data analysis")
    print(f"   • Cognitora - File upload/download & code execution")
    print(f"   • OpenAI GPT-4o - Intelligent chart generation\n")
    
    print(f"{Colors.YELLOW}🎯 WORKFLOW:{Colors.ENDC}")
    print(f"   1. Create sample sales data (CSV)")
    print(f"   2. Upload data to Cognitora sandbox")
    print(f"   3. AI analyzes data and generates visualizations")
    print(f"   4. Download generated charts to local filesystem\n")
    
    # Validate API keys
    if not OPENAI_API_KEY:
        print(f"{Colors.RED}❌ Error: OPENAI_API_KEY not set{Colors.ENDC}")
        return
    
    if not COGNITORA_API_KEY:
        print(f"{Colors.RED}❌ Error: COGNITORA_API_KEY not set{Colors.ENDC}")
        return
    
    print(f"{Colors.CYAN}{'=' * 80}{Colors.ENDC}\n")
    
    # ========================================================================
    # STEP 1: Create Sample Data & Output Directory
    # ========================================================================
    
    print(f"{Colors.YELLOW}📝 STEP 1: Creating Sample Sales Data{Colors.ENDC}")
    print(f"{Colors.DIM}{'─' * 80}{Colors.ENDC}")
    
    # Create output directory
    output_dir = "output_charts"
    os.makedirs(output_dir, exist_ok=True)
    
    global csv_content
    csv_content = create_sample_sales_data()
    
    # Save CSV to output folder
    csv_output_path = os.path.join(output_dir, "sales_data.csv")
    with open(csv_output_path, 'w') as f:
        f.write(csv_content)
    
    print(f"{Colors.GREEN}✅ Created sales data CSV with 20 rows{Colors.ENDC}")
    print(f"{Colors.DIM}   Columns: Date, Product, Category, Units_Sold, Revenue, Region{Colors.ENDC}")
    print(f"{Colors.GREEN}✅ Saved to: {csv_output_path}{Colors.ENDC}\n")
    
    # ========================================================================
    # STEP 2: Data Ready for Analysis
    # ========================================================================
    
    print(f"{Colors.YELLOW}☁️  STEP 2: Preparing Data for Cognitora Sandbox{Colors.ENDC}")
    print(f"{Colors.DIM}{'─' * 80}{Colors.ENDC}")
    
    print(f"{Colors.DIM}   Data will be written to sandbox during code execution...{Colors.ENDC}")
    print(f"{Colors.GREEN}✅ CSV data ready for analysis{Colors.ENDC}\n")
    
    # ========================================================================
    # STEP 3: Create AI Agent for Data Visualization
    # ========================================================================
    
    print(f"{Colors.YELLOW}🤖 STEP 3: Initializing AI Visualization Agent{Colors.ENDC}")
    print(f"{Colors.DIM}{'─' * 80}{Colors.ENDC}")
    
    viz_agent = Agent(
        name="data_visualizer",
        model="gpt-4o",
        instructions="""You are an expert Data Visualization Specialist.

YOUR CAPABILITIES:
- Analyze CSV data and create insightful visualizations
- Generate professional charts using matplotlib and seaborn
- Provide clear analysis summaries with key insights

CRITICAL RULES:
1. The data file will be written to /tmp/sales_data.csv in the sandbox
2. Use the analyze_data_and_create_chart tool to create visualizations
3. Each chart should tell a clear story about the data
4. Provide business insights along with visualizations

CHART TYPES AVAILABLE:
- Bar charts for comparisons
- Line charts for trends over time
- Horizontal bar charts for rankings
- And more!

Be creative and insightful in your analysis!""",
        tools=[analyze_data_and_create_chart]
    )
    
    print(f"{Colors.GREEN}✅ AI agent ready!{Colors.ENDC}\n")
    
    # ========================================================================
    # STEP 4: Generate Visualizations
    # ========================================================================
    
    print(f"{Colors.CYAN}{'═' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}📊 GENERATING VISUALIZATIONS{Colors.ENDC}")
    print(f"{Colors.CYAN}{'═' * 80}{Colors.ENDC}\n")
    
    visualizations = [
        {
            "name": "Revenue by Category",
            "query": """Analyze the sales data and create a bar chart showing total revenue by product category.
            
Use the analyze_data_and_create_chart tool with:
- chart_type: "bar"
- analysis_description: "Total revenue by product category"
- output_filename: "revenue_by_category.png"

Show the exact revenue numbers for each category."""
        },
        {
            "name": "Revenue by Region",
            "query": """Create a visualization showing how revenue is distributed across different regions.
            
Use the analyze_data_and_create_chart tool with:
- chart_type: "bar"
- analysis_description: "Total revenue by region"
- output_filename: "revenue_by_region.png"

Which region performs best?"""
        },
        {
            "name": "Top Products",
            "query": """Identify and visualize the top 5 products by revenue.
            
Use the analyze_data_and_create_chart tool with:
- chart_type: "horizontal_bar"
- analysis_description: "Top 5 products by total revenue"
- output_filename: "top_products.png"

Show me the winners!"""
        },
        {
            "name": "Daily Trend",
            "query": """Show the daily revenue trend over time.
            
Use the analyze_data_and_create_chart tool with:
- chart_type: "line"
- analysis_description: "Daily revenue trend over time"
- output_filename: "daily_trend.png"

Is revenue growing or declining?"""
        },
    ]
    
    results = []
    total_time = 0
    downloaded_files = []
    
    for i, viz in enumerate(visualizations, 1):
        print(f"{Colors.YELLOW}📈 Visualization {i}/{len(visualizations)}: {viz['name']}{Colors.ENDC}")
        print(f"{Colors.DIM}{'─' * 80}{Colors.ENDC}")
        
        start_time = time.time()
        
        # Have AI agent create the visualization
        # Note: The CSV file will be uploaded to Cognitora before execution
        result = await Runner.run(viz_agent, input=viz['query'])
        
        duration = time.time() - start_time
        total_time += duration
        
        print(f"\n{Colors.GREEN}{result.final_output}{Colors.ENDC}")
        print(f"{Colors.DIM}⏱️  Chart generated in {duration:.1f}s{Colors.ENDC}\n")
        
        # Extract filename from the query (look for output_filename parameter)
        import re
        filename_match = re.search(r'output_filename:\s*"([^"]+)"', viz['query'])
        if filename_match:
            chart_filename = filename_match.group(1)
            sandbox_path = f"/tmp/{chart_filename}"
            local_path = os.path.join(output_dir, chart_filename)
            
            # Download the file from sandbox
            print(f"{Colors.DIM}   📥 Downloading {chart_filename} from sandbox...{Colors.ENDC}")
            download_start = time.time()
            
            if download_file_from_sandbox(sandbox_path, local_path):
                download_time = time.time() - download_start
                file_size = os.path.getsize(local_path)
                print(f"{Colors.GREEN}   ✅ Downloaded to {local_path} ({file_size:,} bytes, {download_time:.1f}s){Colors.ENDC}\n")
                downloaded_files.append({
                    "name": chart_filename,
                    "path": local_path,
                    "size": file_size
                })
            else:
                print(f"{Colors.RED}   ❌ Failed to download {chart_filename}{Colors.ENDC}\n")
        
        results.append({
            "name": viz['name'],
            "result": str(result.final_output),
            "duration": duration
        })
    
    # ========================================================================
    # STEP 5: Summary
    # ========================================================================
    
    print(f"\n{Colors.CYAN}{'═' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ VISUALIZATION COMPLETE!{Colors.ENDC}")
    print(f"{Colors.CYAN}{'═' * 80}{Colors.ENDC}\n")
    
    print(f"{Colors.YELLOW}📊 Generated & Downloaded Files:{Colors.ENDC}")
    print(f"\n   📄 CSV Data:")
    print(f"      📁 {csv_output_path}")
    csv_size = os.path.getsize(csv_output_path)
    print(f"      📊 {csv_size:,} bytes")
    
    print(f"\n   🖼️  Chart Images:")
    for i, (result, file_info) in enumerate(zip(results, downloaded_files), 1):
        print(f"      {i}. {result['name']}")
        print(f"         📁 {file_info['path']}")
        print(f"         📊 {file_info['size']:,} bytes ({result['duration']:.1f}s)")
    
    print(f"\n{Colors.YELLOW}⏱️  Total Time: {total_time:.1f}s{Colors.ENDC}\n")
    
    print(f"{Colors.GREEN}✨ This demonstrates:{Colors.ENDC}")
    print(f"   ✅ CSV data creation and local storage")
    print(f"   ✅ Data upload to Cognitora sandbox")
    print(f"   ✅ AI-powered data analysis")
    print(f"   ✅ Automated chart generation (matplotlib/seaborn)")
    print(f"   ✅ Professional visualizations with insights")
    print(f"   ✅ File download from sandbox to local filesystem\n")
    
    print(f"{Colors.BLUE}📁 All Output Files Saved To:{Colors.ENDC}")
    print(f"{Colors.BOLD}   {os.path.abspath(output_dir)}/{Colors.ENDC}")
    print(f"{Colors.DIM}   • sales_data.csv (source data)")
    print(f"   • revenue_by_category.png")
    print(f"   • revenue_by_region.png")
    print(f"   • top_products.png")
    print(f"   • daily_trend.png{Colors.ENDC}\n")
    
    print(f"{Colors.CYAN}🚀 Try other examples:{Colors.ENDC}")
    print(f"   • 1-example-basic-tasks.py - Basic agentic tasks")
    print(f"   • 3-example-stock-analyst.py - ML stock predictions")
    print(f"   • 4-example-live-crypto-tracker.py - Live data from internet")
    print(f"   • 5-example-multi-agent-research.py - Multi-agent collaboration\n")


if __name__ == "__main__":
    asyncio.run(main())

