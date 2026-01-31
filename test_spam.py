import requests
import time

# Function to spam the API
def hammer_api(count=110):
    url = "http://127.0.0.1:8000/health"
    print(f"🔥 Firing {count} requests at {url}...")
    
    blocked = 0
    allowed = 0
    
    start = time.time()
    
    for i in range(count):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                allowed += 1
                symbol = "✅"
            elif res.status_code == 429:
                blocked += 1
                symbol = "⛔"
            else:
                symbol = f"❓({res.status_code})"
                
            print(f"\rRequest {i+1}: {symbol} (Allowed: {allowed}, Blocked: {blocked})", end="")
        except Exception as e:
            print(f"Error: {e}")
            
    print(f"\n\n🏁 Finished in {time.time() - start:.2f}s")
    print(f"Allowed: {allowed}")
    print(f"Blocked: {blocked}")

if __name__ == "__main__":
    hammer_api()