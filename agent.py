# agent.py

import json
from datetime import datetime
from typing import Any, Dict, List

from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Indices you want to cover
INDICES = ["NIFTY", "BANKNIFTY", "FINNIFTY", "NIFTYNXT50", "MIDCPNIFTY", "BANKEX"]

# Build prompt template: ask for up to 5 high-confidence option calls with required fields
PROMPT_TEMPLATE = """
You are an expert Indian stock options analyst. Given the live market data for {index_name} on {date}, analyze the option chain and produce up to 5 actionable option calls.
Each call must be a JSON object with these keys:
- type: \"CALL\", \"PUT\", or \"SELL\"
- strikePrice: number
- targetPrice: number
- stopLoss: number
- expiry: date in dd-MMM-yyyy format (e.g., 08-Aug-2025)
- accuracy: estimated confidence percentage (must be between 95 and 100)
- reason: brief rationale (1-2 sentences)

Return a JSON array of such objects only. Example output:
[
  {{
    "type": "CALL",
    "strikePrice": 24500.0,
    "targetPrice": 24700.0,
    "stopLoss": 24300.0,
    "expiry": "08-Aug-2025",
    "accuracy": 96.5,
    "reason": "Bullish breakout with high open interest and rising volume."
  }}
]
"""

prompt = PromptTemplate(input_variables=["index_name", "date"], template=PROMPT_TEMPLATE)

# Ollama local model (ensure `ollama` is running and llama3 model is available)
llm = ChatOllama(model="llama3", temperature=0.3)

llm_chain = LLMChain(prompt=prompt, llm=llm)


async def run_agent_on_nse_data(nse_data: Dict[str, Any], index_name: str = "NIFTY") -> List[Dict[str, Any]]:
    """
    Given raw NSE option chain data, run the LLM agent to produce structured option calls.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    # You may summarize or include relevant parts of nse_data in the system prompt if needed.
    # For simplicity, pass index_name and date; you could extend to include underlying value.
    result = llm_chain.run({"index_name": index_name, "date": today})

    try:
        calls = json.loads(result)
        if not isinstance(calls, list):
            raise ValueError("LLM output is not a list")
    except Exception:
        # Try to recover by extracting the first JSON array in text
        import re

        match = re.search(r"\[.*\]", result, re.DOTALL)
        if match:
            try:
                calls = json.loads(match.group(0))
            except Exception as ex:
                print("Failed to parse recovered JSON:", ex)
                calls = []
        else:
            print("LLM output:", result)
            calls = []

    # Normalize and clamp accuracy, ensure structure
    normalized = []
    for c in calls:
        try:
            # Basic validation and type conversions
            call_type = c.get("type", "").upper()
            strike = float(c.get("strikePrice", 0))
            target = float(c.get("targetPrice", 0))
            stop_loss = float(c.get("stopLoss", 0))
            expiry = c.get("expiry", "")
            accuracy = float(c.get("accuracy", 0))
            reason = c.get("reason", "").strip()

            if call_type not in {"CALL", "PUT", "SELL"}:
                continue
            if accuracy < 0 or accuracy > 100:
                continue

            normalized.append({
                "type": call_type,
                "strikePrice": strike,
                "targetPrice": target,
                "stopLoss": stop_loss,
                "expiry": expiry,
                "accuracy": accuracy,
                "reason": reason,
                "index": index_name
            })
        except Exception:
            continue

    return normalized
