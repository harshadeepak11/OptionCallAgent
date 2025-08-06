# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from agent_scheduler_backend import start_scheduler, get_latest_calls
from agent import run_agent_on_nse_data
from nse import fetch_nse_data

app = FastAPI()

# CORS (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response model for generated calls
class OptionCallResponse(BaseModel):
    type: str
    strikePrice: float
    targetPrice: float
    stopLoss: float
    expiry: str
    accuracy: float
    reason: str
    index: str

@app.on_event("startup")
def on_startup():
    start_scheduler()

@app.get("/latest-calls", response_model=List[OptionCallResponse])
def latest_calls_endpoint():
    return get_latest_calls()

@app.get("/generate-calls", response_model=List[OptionCallResponse])
async def generate_calls_now(index: str = "NIFTY"):
    """
    Manual trigger: generate calls for a given index immediately.
    """
    try:
        nse_data = await fetch_nse_data(index)
        calls = await run_agent_on_nse_data(nse_data, index_name=index)
        high_conf = [c for c in calls if c.get("accuracy", 0) >= 95.0]
        return high_conf[:5]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test-nse")
async def test_nse(symbol: str = "NIFTY"):
    try:
        data = await fetch_nse_data(symbol)
        # return a small slice for sanity
        return {"message": f"Fetched {symbol}", "underlyingValue": data.get("records", {}).get("underlyingValue")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
