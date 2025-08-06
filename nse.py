# nse.py

import asyncio
import random
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


async def fetch_nse_data(symbol: str = "NIFTY", max_retries: int = 3) -> Dict:
    """
    Fetch NSE Option Chain data for the given index, with retries, backoff, and proper cookie/session priming.
    """
    url = OPTION_CHAIN_URL + symbol.upper()

    for attempt in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient(headers=DEFAULT_HEADERS, timeout=10.0, follow_redirects=True) as client:
                # Step 1: Hit homepage to obtain session cookies
                homepage_resp = await client.get(NSE_BASE_URL)
                if homepage_resp.status_code != 200:
                    raise Exception(f"Homepage fetch failed: {homepage_resp.status_code}")

                # Small pause to let NSE set cookies server-side
                await asyncio.sleep(0.5)

                # Step 2: Actual option chain request using the same client (cookies preserved)
                resp = await client.get(url)

                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 401:
                    # Likely bot detection; backoff and retry
                    print(f"[fetch_nse_data] Attempt {attempt}: 401 Unauthorized, retrying...")
                else:
                    # Unexpected status
                    raise Exception(f"NSE API error {resp.status_code}: {resp.text[:300]}")
        except Exception as e:
            print(f"[fetch_nse_data] Attempt {attempt} failed for {symbol}: {e}")
            if attempt == max_retries:
                # Last attempt, rethrow
                raise
        # Exponential backoff with jitter before next try
        backoff = (2 ** attempt) + random.uniform(0, 1)
        await asyncio.sleep(backoff)

    raise Exception(f"Failed to fetch NSE data for {symbol} after {max_retries} attempts")
