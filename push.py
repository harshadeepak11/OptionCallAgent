# push.py

import json
import requests
from typing import Any, List

def notify_ios_clients(call_data: List[Any]):
    """
    Stub: send the calls to iOS clients. Replace with real push (APNs/FCM) or webhook logic.
    """
    print("🔔 Notifying iOS clients with payload:")
    print(json.dumps(call_data, indent=2))

    # Example: POST to your iOS listener endpoint (if you have one)
    try:
        response = requests.post(
            "https://your-ios-endpoint.example.com/receive-call",
            headers={"Content-Type": "application/json"},
            data=json.dumps(call_data)
        )
        print(f"Notification endpoint response: {response.status_code}")
    except Exception as e:
        print("Failed to push to iOS endpoint:", e)
