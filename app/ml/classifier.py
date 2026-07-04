import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


DOMAIN_KEYWORDS = {
    "AI/ML": ["machine learning", "deep learning", "artificial intelligence", "neural network",
              "computer vision", "nlp", "natural language", "predictive", "recommendation",
              "classification", "regression", "tensorflow", "pytorch", "cnn", "rnn", "gan",
              "llm", "large language model", "gpt", "chatbot", "intelligent"],
    "Blockchain": ["blockchain", "smart contract", "ethereum", "hyperledger", "web3",
                   "decentralized", "distributed ledger", "crypto", "nft", "solidity"],
    "IoT": ["iot", "internet of things", "sensor", "embedded", "raspberry pi", "arduino",
            "firmware", "smart device", "connected device", "telemetry"],
    "Web3": ["web3", "dapp", "decentralized application", "metaverse", "defi"],
    "Mobile": ["mobile app", "android", "ios", "flutter", "react native", "kotlin",
               "swift", "cross-platform"],
    "Cloud Computing": ["cloud", "aws", "azure", "gcp", "kubernetes", "docker",
                        "container", "serverless", "microservice", "devops", "ci/cd"],
    "Cybersecurity": ["security", "cyber", "encryption", "authentication", "firewall",
                      "intrusion detection", "malware", "ransomware", "zero trust",
                      "penetration testing", "vulnerability"],
    "EdTech": ["education", "learning", "e-learning", "edtech", "student", "curriculum",
               "online course", "assessment", "skill development"],
    "HealthTech": ["health", "healthcare", "medical", "diagnostic", "patient", "hospital",
                   "telemedicine", "abdm", "ehr", "electronic health record", "disease"],
    "FinTech": ["payment", "banking", "finance", "insurance", "lending", "upi",
                "digital payment", "financial inclusion", "credit scoring"],
    "AgriTech": ["agriculture", "farming", "crop", "irrigation", "soil", "farmer",
                 "agritech", "food supply", "cold chain"],
    "Smart Cities": ["smart city", "urban", "traffic", "waste management", "smart parking",
                     "public transport", "municipal", "governance"],
}

DIFFICULTY_KEYWORDS = {
    "Beginner": ["basic", "simple", "introductory", "fundamental", "easy", "starter",
                  "beginner-friendly", "entry-level", "first-time"],
    "Advanced": ["advanced", "complex", "scalable", "enterprise-grade", "real-time",
                 "high-performance", "distributed", "large-scale", "production-grade",
                 "optimization", "sophisticated"],
}

PLATFORM_KEYWORDS = {
    "Smart India Hackathon": ["sih", "smart india hackathon", "sih 2024", "sih 2025"],
    "Devfolio": ["devfolio", "devfolio hackathon"],
    "HackerEarth": ["hackerearth", "hacker earth"],
    "Unstop": ["unstop", "dare2compete", "d2c"],
    "D2C": ["d2c", "do it code", "doitcode"],
    "HackerRank": ["hackerrank", "hacker rank"],
    "CodeChef": ["codechef", "code chef"],
    "MLH": ["mlh", "major league hacking"],
}


def classify_domain(title: str, description: str) -> str:
    text = f"{title} {description}".lower()
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', text))
        if score:
            scores[domain] = score
    if scores:
        return max(scores, key=scores.get)
    return "General"


def classify_difficulty(title: str, description: str) -> str:
    text = f"{title} {description}".lower()
    for difficulty, keywords in DIFFICULTY_KEYWORDS.items():
        if any(re.search(r'\b' + re.escape(kw) + r'\b', text) for kw in keywords):
            return difficulty
    return "Intermediate"


def extract_tags(title: str, description: str) -> list[str]:
    text = f"{title} {description}".lower()
    all_keywords = set()
    for domain_keywords in DOMAIN_KEYWORDS.values():
        for kw in domain_keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                all_keywords.add(kw)

    tech_tags = ["python", "javascript", "java", "react", "node", "flask", "django",
                 "sql", "nosql", "mongodb", "redis", "api", "rest", "graphql",
                 "mobile", "web", "app", "dashboard", "analytics", "automation"]
    for tag in tech_tags:
        if re.search(r'\b' + re.escape(tag) + r'\b', text):
            all_keywords.add(tag)

    return sorted(list(all_keywords))[:10]


def detect_platform(source_link: str, title: str = "", description: str = "") -> str:
    text = f"{source_link} {title} {description}".lower()
    for platform, keywords in PLATFORM_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return platform
    if "sih" in source_link.lower() or "sih" in title.lower():
        return "Smart India Hackathon"
    return "General"
