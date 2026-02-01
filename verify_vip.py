import requests

def check_vip():
    url = "http://127.0.0.1:8000/health"
    
    # 1. Test Anonymous (Should have limit 100)
    print("🕵️  Testing Anonymous...")
    res = requests.get(url)
    limit = res.headers.get("X-RateLimit-Limit")
    print(f"   Limit: {limit} (Expected: 100)")
    
    # 2. Test VIP (Should have limit 1000)
    print("\n👑 Testing VIP...")
    headers = {"Authorization": "Bearer my_secret_token_123"}
    res = requests.get(url, headers=headers)
    limit = res.headers.get("X-RateLimit-Limit")
    print(f"   Limit: {limit} (Expected: 1000)")

if __name__ == "__main__":
    check_vip()