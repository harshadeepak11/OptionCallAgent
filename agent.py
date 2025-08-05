# agent.py using Ollama

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOllama
from langchain.tools import tool
from typing import List
import datetime
from nsepython import nse_optionchain_scrapper

# ------------------ INSTRUMENTS ------------------
INDICES = ["NIFTY", "BANKNIFTY", "FINNIFTY", "NIFTYNXT50", "MIDCPNIFTY", "BANKEX"]

# ------------------ TOOL FUNCTION ------------------

@tool
def get_option_chain_data(symbol: str) -> str:
    """
    Get NSE Option Chain data for the given index symbol.
    Returns a summary string.
    """
    try:
        data = nse_optionchain_scrapper(symbol)
        last_price = data['records']['underlyingValue']
        expiry = data['records']['expiryDates'][0]
        msg = f"{symbol} is trading at {last_price}. Expiry on {expiry}. Analyze this data to decide CALL/PUT/SELL options."
        return msg
    except Exception as e:
        return f"Error fetching data for {symbol}: {str(e)}"

# ------------------ LLM & AGENT ------------------

llm = ChatOllama(model="llama3", temperature=0)

tools = [
    Tool.from_function(get_option_chain_data)
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ------------------ MAIN FUNCTION ------------------

def generate_option_calls() -> List[dict]:
    option_calls = []
    for symbol in INDICES:
        result = agent.run(f"Give one option recommendation (CALL/PUT/SELL) for {symbol} with strike price, expiry and reason.")
        option_calls.append({
            "symbol": symbol,
            "recommendation": result
        })
    return option_calls
