#
#  main.py
#  OptionCallAgent
#
#  Created by Harsha on 03/08/25.
#

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define response model
class OptionCall(BaseModel):
    type: str  # CALL, PUT, SELL
    strikePrice: float
    expiry: datetime
    reason: str

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

@app.get("/option-calls", response_model=List[OptionCall])
def get_option_calls():
    # Replace this mock logic with real logic later
    calls = [
        OptionCall(
            type="CALL",
            strikePrice=25000.0,
            expiry=datetime(2025, 8, 8),
            reason="Nifty is trending up. Buy near the money CALL option."
        ),
        OptionCall(
            type="SELL",
            strikePrice=25000.0,
            expiry=datetime(2025, 8, 8),
            reason="High implied volatility. Consider selling options."
        )
    ]
    return calls
