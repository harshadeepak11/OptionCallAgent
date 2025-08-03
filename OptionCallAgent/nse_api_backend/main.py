#
//  main.py
//  OptionCallAgent
//
//  Created by Harsha on 03/08/25.
//

from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS so your iOS app can talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # use specific domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/nifty-options")
def get_nifty_options():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com"
    }
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)  # Get cookies
    response = session.get("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY", headers=headers)
    return response.json()
