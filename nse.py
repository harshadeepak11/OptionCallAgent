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
    url = OPTION_CHAIN_URL + symbol.upper()

    for attempt in range(1, 4):  # Attempts 1 to 3
        try:
            print(f"[fetch_nse_data] Attempt {attempt} for {symbol}...")

            async with httpx.AsyncClient(
                headers=DEFAULT_HEADERS,
                timeout=15.0,
                follow_redirects=True,
                http2=True  # Enables HTTP/2
            ) as client:
                # Hit homepage to set cookies
                homepage_resp = await client.get(NSE_BASE_URL)
                homepage_resp.raise_for_status()

                # Hit option chain
                response = await client.get(url)
                if response.status_code == 200:
                    print(f"[fetch_nse_data] ✅ Success on attempt {attempt} for {symbol}")
                    return response.json()
                elif response.status_code == 401:
                    print(f"[fetch_nse_data] 401 Unauthorized on attempt {attempt}, retrying...")
                    await asyncio.sleep(1 + attempt)
                else:
                    print(f"[fetch_nse_data] Unexpected status {response.status_code}")
                    response.raise_for_status()

        except Exception as e:
            print(f"[fetch_nse_data] Attempt {attempt} failed for {symbol}: {e}")
            await asyncio.sleep(1 + attempt)

    raise Exception(f"[fetch_nse_data] ❌ Failed to fetch NSE data for {symbol} after 3 attempts")
