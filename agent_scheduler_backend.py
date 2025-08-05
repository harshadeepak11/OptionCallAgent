# Filename: agent_scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.agent import run_agent_on_nse_data  # Your agent logic here
from app.push import notify_ios_clients  # We'll create this too

# In-memory store for now
latest_calls = []


def auto_generate_calls():
    print(f"[{datetime.now()}] Running scheduled job...")
    
    # Step 1: Get live NSE data
    nse_data = fetch_nse_data()  # Define this function properly

    # Step 2: Ask the agent for option calls
    try:
        result = run_agent_on_nse_data(nse_data)
        calls = json.loads(result) if isinstance(result, str) else result

        # Step 3: Filter high-accuracy calls
        filtered = [c for c in calls if float(c.get("accuracy", 0)) >= 95.0]

        # Step 4: Save and push if any
        if filtered:
            latest_calls.clear()
            latest_calls.extend(filtered)
            notify_ios_clients(filtered)
            print(f"✅ {len(filtered)} new calls pushed to iOS")
        else:
            print("⚠️ No high-accuracy calls found")

    except Exception as e:
        print("❌ Error in auto_generate_calls:", e)


# Call this from your main.py or a startup event
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_generate_calls, 'interval', minutes=5)
    scheduler.start()
    print("✅ Scheduler started (interval: 5 min)")


# You can expose this to your API for testing

def get_latest_calls():
    return latest_calls
