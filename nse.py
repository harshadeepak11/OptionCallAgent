# nse.py

import asyncio
import httpx
from typing import Dict

NSE_BASE_URL = "https://www.nseindia.com"
OPTION_CHAIN_URL = NSE_BASE_URL + "/api/option-chain-indices?symbol="

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/option-chain",
    "Origin": "https://www.nseindia.com",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate, br",
}


async def fetch_nse_data(symbol: str = "NIFTY") -> Dict:
    """
    Fetch NSE Option Chain data (NIFTY, BANKNIFTY, etc.) with headers & cookies.
    Retries a couple of times to bypass occasional 401 due to bot-protection timing.
    """
    url = OPTION_CHAIN_URL + symbol.upper()

    for attempt in range(3):
        try:
            async with httpx.AsyncClient(
                headers=DEFAULT_HEADERS, timeout=10.0, follow_redirects=True
            ) as client:
                # Preliminary hit to get cookies
                homepage_resp = await client.get(NSE_BASE_URL)
                if homepage_resp.status_code != 200:
                    raise Exception(f"Failed to fetch homepage: {homepage_resp.status_code}")

                # Actual option-chain request
                resp = await client.get(url)
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 401:
                    # small backoff and retry
                    await asyncio.sleep(1 + attempt)
                    continue
                else:
                    raise Exception(f"NSE API error {resp.status_code}: {resp.text[:300]}")
        except Exception as e:
            if attempt == 2:
                raise
            await asyncio.sleep(1)
    raise Exception("Failed to fetch NSE data after retries")
