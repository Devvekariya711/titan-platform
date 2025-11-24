from google.adk.tools import FunctionTool, AgentTool
from google.adk.agents import Agent
import yfinance as yf
from duckduckgo_search import DDGS

LLM = "gemini-2.5-flash-lite"

# --- 1. Function Tool: Get Hard Market Data ---
def get_stock_price(ticker: str):
    """
    Fetches the current stock price and basic info for a given ticker symbol.
    Args:
        ticker (str): The stock ticker (e.g., AAPL, TSLA, BTC-USD).
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if hist.empty:
            return f"No data found for {ticker}."
        price = hist['Close'].iloc[-1]
        return f"Current price of {ticker}: ${price:.2f}"
    except Exception as e:
        return f"Error fetching data for {ticker}: {str(e)}"

# Wrap it in ADK's FunctionTool
market_data_tool = FunctionTool(func=get_stock_price)

# --- 2. Agent Tool: Search for News/Sentiment ---
# We create a mini-agent that knows how to search, then wrap it as a tool.
search_worker = Agent(
    model= LLM , # Or your preferred model
    name="search_worker",
    description="A helper that searches the web for financial news.",
    instruction="You are a search assistant. Use the provided python function to search DuckDuckGo and summarize results."
)

# We need the actual python function for the search worker to use
def search_web(query: str):
    """Searches the web for financial news and trends."""
    results = DDGS().text(query, max_results=5)
    return str(results)

# Give the worker the capability to search
search_worker.tools = [FunctionTool(func=search_web)]

# Now wrap the AGENT as a TOOL for the higher-level agents
news_search_tool = AgentTool(agent=search_worker)