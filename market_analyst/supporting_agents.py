from google.adk.agents import Agent
from .tools import market_data_tool, news_search_tool

# --- Sub-Agent 1: Data Scout ---
# This agent gathers the raw intel.

LLM = "gemini-2.5-flash-lite"

data_scout_agent = Agent(
    model= LLM,
    name="data_scout",
    description="Responsible for scraping financial news and gathering stock data.",
    instruction="""
    You are the Data Scout.
    1. Your job is to gather raw data. Do not analyze deep trends yet, just get the facts.
    2. Use 'market_data_tool' for specific stock prices.
    3. Use 'news_search_tool' to find recent news, social sentiment, and rumors.
    4. Return a structured list of findings.
    """,
    tools=[market_data_tool, news_search_tool]
)

# --- Sub-Agent 2: Risk & Insight Assessor ---
# This agent looks at the data and finds the risks.
risk_agent = Agent(
    model= LLM,
    name="risk_assessor",
    description="Evaluates market trends for risks and sentiment shifts.",
    instruction="""
    You are the Risk and Insight Assessor.
    1. You receive raw data from the Data Scout.
    2. Analyze it for: Emerging trends, Potential investment risks, and Sentiment shifts.
    3. Assign a 'Confidence Level' to your assessment.
    4. Be critical. Look for anomalies.
    """
)