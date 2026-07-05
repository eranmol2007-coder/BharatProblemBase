import requests

BASE = "http://localhost:8000/api"

def test():
    h = requests.get(f"{BASE}/health", timeout=5)
    print(f"Health: {h.json()}")

    s = requests.get(f"{BASE}/problems/stats", timeout=5)
    print(f"Stats: {s.json()}")

    p = requests.get(f"{BASE}/problems?page_size=2", timeout=5)
    d = p.json()
    print(f"Total problems: {d['total']}, returned: {len(d['items'])}")
    if d['items']:
        print(f"First: {d['items'][0]['title'][:50]}...")

    pl = requests.get(f"{BASE}/problems/platforms", timeout=5)
    print(f"Platforms: {pl.json()}")

    dom = requests.get(f"{BASE}/problems/domains", timeout=5)
    print(f"Domains: {dom.json()}")

    print("\nAll API tests passed!")

if __name__ == "__main__":
    test()
