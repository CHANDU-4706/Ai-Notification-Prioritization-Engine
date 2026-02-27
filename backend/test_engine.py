import httpx
import asyncio
import sys

API_BASE = "http://localhost:8001/api/v1"

async def test_scenarios():
    print("--- STARTING CYEPRO ENGINE TEST ---")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # 1. Classification Test
            print("\n[Test 1] AI Classification (Security Context)")
            resp = await client.post(f"{API_BASE}/notify", json={
                "user_id": "tester_01",
                "event_type": "transactional",
                "priority_hint": "medium",
                "message": "Security Alert: New login from London, UK. Was this you?"
            })
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"Decision: {data.get('decision')} | Reasoning: {data.get('reasoning', '')[:100]}...")
            else:
                print(f"Error Response: {resp.text}")

            # 2. Semantic Deduplication Test
            print("\n[Test 2a] Original Message")
            await client.post(f"{API_BASE}/notify", json={
                "user_id": "tester_01",
                "event_type": "transactional",
                "message": "Your package is arriving in 10 minutes."
            })
            
            print("[Test 2b] Semantic Duplicate (slightly different wording)")
            resp = await client.post(f"{API_BASE}/notify", json={
                "user_id": "tester_01",
                "event_type": "transactional",
                "message": "The delivery person will be at your door in 10 mins."
            })
            if resp.status_code == 200:
                data = resp.json()
                print(f"Decision: {data.get('decision')} | Reasoning: {data.get('reasoning')}")
            else:
                print(f"Error Response: {resp.text}")

            # 3. Noise Suppression
            print("\n[Test 3] Promotional Noise Suppression")
            resp = await client.post(f"{API_BASE}/notify", json={
                "user_id": "tester_01",
                "event_type": "promotional",
                "message": "Flash Sale! 50% off on all items for the next hour!"
            })
            if resp.status_code == 200:
                data = resp.json()
                print(f"Decision: {data.get('decision')} | Reasoning: {data.get('reasoning')}")

        except Exception as e:
            print(f"FAILED TO RUN TEST: {e}")

    print("\n--- TEST COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(test_scenarios())
