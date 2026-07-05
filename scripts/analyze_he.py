import requests
from bs4 import BeautifulSoup

url = "https://www.hackerearth.com/challenges/hackathon/"
resp = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})
soup = BeautifulSoup(resp.text, "lxml")

# Pagination
for sel in ["[class*=page]", "[class*=pagination]", "nav a", "a[rel*=next]", "a[class*=next]"]:
    els = soup.select(sel)
    for e in els:
        txt = e.get_text(strip=True)[:60]
        href = e.get("href", "")
        if "page" in href.lower() or "page" in txt.lower() or "next" in txt.lower() or "next" in href.lower() or "»" in txt or "›" in txt:
            print(f"PAGINATION: <{e.name} class={e.get('class')}> href={href} text={txt}")

# Load more
for sel in ["[class*=load]", "[class*=more]", "button", "[data-page]", "a[href*='?']"]:
    els = soup.select(sel)
    for e in els:
        txt = e.get_text(strip=True)[:60]
        if "load" in txt.lower() or "more" in txt.lower() or "page" in txt.lower() or "next" in txt.lower() or "show" in txt.lower():
            print(f"LOAD: <{e.name} class={e.get('class')}> href={e.get('href','')} text={txt}")

# API endpoints
scripts = soup.find_all("script")
for s in scripts:
    if s.string and ("api" in s.string.lower() or "page" in s.string.lower()):
        print(f"SCRIPT (api/page): {s.string[:200]}")

# Check URL params
print(f"\nPage URL: {resp.url}")
print(f"Challenges found: {len(soup.select('.challenge-card-modern'))}")

# Check if there's a total count text
for tag in soup.find_all(["div", "span", "p", "h1", "h2", "h3"]):
    txt = tag.get_text(strip=True)
    if any(w in txt.lower() for w in ["challenge", "hackathon"]) and any(c.isdigit() for c in txt):
        if len(txt) < 100:
            print(f"COUNT: {txt}")
