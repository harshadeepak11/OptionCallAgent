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
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%dT%H:%M:%SZ')
        }

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

@app.get("/option-calls", response_model=List[OptionCall])
def get_option_calls():
    raw_calls = generate_option_calls()
    parsed_calls = []

    for call in raw_calls:
        # You might need to improve this parsing logic
        parsed_calls.append(OptionCall(
            type="CALL",  # extract from call["recommendation"]
            strikePrice=25000.0,  # extract or parse
            expiry=datetime(2025, 8, 8),  # parse from string
            reason=call["recommendation"]
        ))

    return parsed_calls
