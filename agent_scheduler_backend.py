# agent_scheduler_backend.py

import asyncio
import json
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from nse import fetch_nse_data
from agent import run_agent_on_nse_data
from push import notify_ios_clients

# In-memory store for latest high-confidence calls
latest_calls = []

scheduler = BackgroundScheduler()


async def _auto_generate_calls_async():
    print(f"[{datetime.now()}] Running scheduled job...")

    aggregated: list = []

    for index in ["NIFTY", "BANKNIFTY", "FINNIFTY", "NIFTYNXT50", "MIDCPNIFTY", "BANKEX"]:
        try:
            nse_data = await fetch_nse_data(index)
            calls = await run_agent_on_nse_data(nse_data, index_name=index)

            # Filter high accuracy (>=95) and take up to 5 per index
            high_conf = [c for c in calls if c.get("accuracy", 0) >= 95.0]
            aggregated.extend(high_conf[:5])

        except Exception as e:
            print(f"Error processing {index}: {e}")

    # Final global filtering / dedup if needed
    filtered = aggregated  # you could add further logic here

    if filtered:
        latest_calls.clear()
        latest_calls.extend(filtered)
        notify_ios_clients(filtered)
        print(f"✅ {len(filtered)} calls pushed to iOS")
    else:
        print("⚠️ No high-accuracy calls found in this cycle.")


def auto_generate_calls():
    asyncio.run(_auto_generate_calls_async())


def start_scheduler():
    # Run every 5 minutes during market hours (you can add time-of-day guard)
    scheduler.add_job(auto_generate_calls, "interval", minutes=5)
    scheduler.start()
    print("✅ Scheduler started (interval: 30 seconds)")


def get_latest_calls():
    return latest_calls
