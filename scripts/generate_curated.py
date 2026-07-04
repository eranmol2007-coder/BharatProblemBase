import json
import random
import os

random.seed(42)

DOMAINS = ["AI/ML", "Web3", "Blockchain", "FinTech", "HealthTech", "EdTech", "IoT", "Cybersecurity", "Smart Cities", "AgriTech", "Cloud", "AR/VR", "DevOps", "Open Source", "Mobile", "Gaming", "Robotics", "Quantum", "GreenTech", "SpaceTech"]

DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]

PLATFORMS = {
    "Devfolio": {
        "depts": ["Devfolio", "ETHIndia", "Polygon", "Filecoin", "TheGraph", "Gitcoin", "Superteam", "Solana", "Avalanche", "Chainlink", "Push Protocol", "Ceramic", "Tableland", "Biconomy", "Thirdweb", "Buildspace", "Huddle01", "Livepeer", "XMTP", "Lens Protocol", "Arweave", "IPFS", "Ethereum Foundation", "Optimism", "Arbitrum"],
        "nouns": ["Platform", "Protocol", "Network", "App", "Dashboard", "Toolkit", "Framework", "Marketplace", "Bridge", "Vault", "Bot", "Explorer", "Oracle", "Aggregator", "Indexer", "Registry", "Wallet", "DApp", "Contract", "Module"],
        "verbs": ["Build", "Create", "Design", "Develop", "Launch", "Deploy", "Ship", "Hack", "Innovate", "Engineer"],
        "topics": [
            "decentralized identity", "token-gated communities", "on-chain reputation", "DAO tooling",
            "DeFi lending protocol", "NFT marketplace", "privacy-preserving voting", "cross-chain bridge",
            "decentralized storage", "real-world asset tokenization", "soulbound tokens", "zk-rollup",
            "decentralized social", "prediction market", "automated market maker", "flash loan",
            "liquidity pool", "yield optimizer", "staking platform", "governance dashboard",
            "multisig wallet", "decentralized exchange", "perpetual futures", "options trading",
            "NFT fractionalization", "dynamic NFT", "gaming guild", "metaverse land",
            "decentralized identity", "zero-knowledge proof", "privacy mixer", "data oracle",
            "cross-chain messaging", "layer-2 scaling", "account abstraction", "social recovery",
            "decentralized VPN", "file sharing", "streaming payments", "donation platform",
            "grant management", "bounty platform", "reputation system", "attestation service",
            "ENS domain", "decentralized DNS", "content moderation", "sybil resistance",
        ],
        "adj": ["Decentralized", "Trustless", "Permissionless", "Open", "Transparent", "Secure", "Scalable", "Interoperable", "Sovereign", "Censorship-Resistant"],
    },
    "HackerEarth": {
        "depts": ["HackerEarth", "Microsoft", "Google", "Amazon", "Flipkart", "Swiggy", "Zomato", "Razorpay", "PhonePe", "CRED", "Groww", "Zerodha", "OYO", "MakeMyTrip", "Nykaa", "Meesho", "UpGrad", "TCS", "Infosys", "Wipro", "HCL", "Tech Mahindra", "LTI", "Cognizant", "Capgemini"],
        "nouns": ["Engine", "System", "Platform", "Pipeline", "Dashboard", "API", "Framework", "Solution", "Toolkit", "Service", "Model", "Algorithm", "Agent", "Interface", "Suite", "Gateway", "Portal", "Hub", "Backend", "Microservice"],
        "verbs": ["AI-Powered", "ML-Based", "Data-Driven", "Cloud-Native", "Intelligent", "Automated", "Scalable", "Real-Time", "Predictive", "Adaptive", "Self-Learning", "Cognitive", "Autonomous", "Smart", "Next-Gen"],
        "topics": [
            "supply chain optimization", "fraud detection", "recommendation engine", "chatbot",
            "image recognition", "natural language processing", "time series forecasting",
            "anomaly detection", "sentiment analysis", "document parsing", "video analytics",
            "voice assistant", "price optimization", "inventory management", "churn prediction",
            "customer segmentation", "personalization engine", "search ranking", "ad targeting",
            "spam detection", "fake news detection", "deepfake detection", "code completion",
            "test automation", "log analysis", "root cause analysis", "capacity planning",
            "cost optimization", "resource scheduling", "load balancing", "threat detection",
            "malware analysis", "network monitoring", "compliance automation", "data lineage",
            "ETL pipeline", "data warehouse", "stream processing", "batch processing",
            "feature store", "model monitoring", "A/B testing", "experimentation platform",
        ],
        "adj": ["Intelligent", "Automated", "Scalable", "Resilient", "High-Performance", "Distributed", "Fault-Tolerant", "Elastic", "Robust", "Enterprise-Grade"],
    },
    "Unstop": {
        "depts": ["Unstop", "Ministry of Education", "AICTE", "NASSCOM", "ISRO", "DRDO", "BHEL", "NTPC", "ONGC", "Coal India", "Indian Railways", "SEBI", "RBI", "NPCI", "IIT Bombay", "IIT Delhi", "IIT Kanpur", "IIM Ahmedabad", "IIM Bangalore", "IISc", "ICMR", "CSIR", "ICAR", "DST", "MeitY"],
        "nouns": ["Challenge", "Hackathon", "Competition", "Initiative", "Program", "Mission", "Drive", "Campaign", "Summit", "Grand Challenge", "Innovation Lab", "Incubation", "Accelerator", "Showcase", "Expo", "Fest", "Meetup", "Workshop", "Bootcamp", "Fellowship"],
        "verbs": ["National", "Smart", "Digital", "Innovative", "Sustainable", "Inclusive", "Secure", "Connected", "Resilient", "Efficient", "Integrated", "Holistic", "Transformative", "Empowering", "Collaborative"],
        "topics": [
            "rural healthcare", "digital literacy", "clean energy", "water conservation",
            "e-governance", "public safety", "disaster management", "skill development",
            "financial inclusion", "waste management", "renewable energy", "women empowerment",
            "farmer support", "MSME growth", "urban mobility", "affordable housing",
            "sanitation", "nutrition security", "air quality", "forest conservation",
            "ocean cleanup", "biodiversity", "organic farming", "cold chain logistics",
            "telemedicine", "remote learning", "smart village", "digital payment",
            "crop insurance", "market linkage", "fisheries management", "livestock health",
            "tribal welfare", "disability inclusion", "elderly care", "mental health",
            "road safety", "cyber awareness", "blockchain governance", "AI for justice",
        ],
        "adj": ["National", "Digital", "Smart", "Inclusive", "Sustainable", "Resilient", "Innovative", "Transformative", "Empowering", "Integrated"],
    },
    "D2C": {
        "depts": ["Dare2Compete", "Deloitte", "PwC", "KPMG", "EY", "Infosys", "Wipro", "HCL", "Tech Mahindra", "L&T", "Mindtree", "Cognizant", "Capgemini", "Accenture", "IBM", "Oracle", "SAP", "Salesforce", "Adobe", "Siemens", "Bosch", "GE", "Honeywell", "ABB", "Schneider"],
        "nouns": ["Innovation", "Solution", "Platform", "Ecosystem", "Network", "Hub", "Accelerator", "Tool", "Suite", "Gateway", "Engine", "Framework", "Dashboard", "Console", "Portal", "Interface", "Bridge", "Adapter", "Connector", "Orchestrator"],
        "verbs": ["Next-Gen", "Future-Ready", "Cutting-Edge", "Revolutionary", "Disruptive", "Transformative", "Breakthrough", "Novel", "Advanced", "Smart", "Industrial", "Enterprise", "Mission-Critical", "Game-Changing", "World-Class"],
        "topics": [
            "predictive maintenance", "digital twin", "computer vision inspection",
            "supply chain visibility", "customer 360", "automated compliance",
            "risk assessment", "knowledge management", "process automation",
            "workflow optimization", "talent matching", "skills analytics",
            "market intelligence", "competitive analysis", "revenue forecasting",
            "ESG reporting", "carbon footprint", "energy optimization", "smart manufacturing",
            "quality control", "inventory optimization", "demand forecasting",
            "asset tracking", "fleet management", "worker safety", "ergonomic assessment",
            "training simulation", "remote assistance", "AR maintenance", "VR training",
            "document intelligence", "contract analytics", "invoice processing",
            "expense management", "procurement automation", "vendor evaluation",
        ],
        "adj": ["Enterprise", "Industrial", "Mission-Critical", "Next-Gen", "Connected", "Intelligent", "Automated", "Cognitive", "Digital", "Smart"],
    },
    "CodeChef": {
        "depts": ["CodeChef", "Directi", "Media.net", "Juspay", "Zeta Suite", "Postman", "GitLab", "DigitalOcean", "Linode", "Vultr", "Cloudflare", "Netlify", "Vercel", "Railway", "Fly.io", "Supabase", "Neon", "PlanetScale", "MongoDB", "Redis"],
        "nouns": ["Challenge", "Contest", "Competition", "Hackathon", "Sprint", "Showdown", "Battle", "Clash", "Duel", "Series", "League", "Cup", "Trophy", "Championship", "Marathon", "Race", "Dash", "Blitz", "Thon", "Fest"],
        "verbs": ["Competitive", "Algorithmic", "Data Structure", "Dynamic Programming", "Graph Theory", "Number Theory", "String Processing", "Computational Geometry", "Combinatorial", "Greedy", "Divide and Conquer", "Backtracking", "Bit Manipulation", "Game Theory", "Segment Tree"],
        "topics": [
            "binary search", "sorting algorithms", "linked list", "tree traversal",
            "graph shortest path", "minimum spanning tree", "network flow", "string matching",
            "pattern recognition", "optimization problem", "constraint satisfaction",
            "path finding", "maze solving", "puzzle solving", "schedule optimization",
            "resource allocation", "load distribution", "cache design", "memory management",
            "concurrent processing", "parallel algorithm", "distributed computing",
            "database indexing", "query optimization", "compression algorithm",
            "encryption algorithm", "hash function", "randomized algorithm",
            "approximation algorithm", "online algorithm", "streaming algorithm",
        ],
        "adj": ["Competitive", "Algorithmic", "Optimized", "Efficient", "Fast", "Parallel", "Distributed", "Concurrent", "Low-Latency", "High-Throughput"],
    },
    "HackerRank": {
        "depts": ["HackerRank", "Morgan Stanley", "Goldman Sachs", "JP Morgan", "Deutsche Bank", "Barclays", "Citibank", "Uber", "Lyft", "Airbnb", "Stripe", "Square", "PayPal", "Shopify", "Atlassian", "Cisco", "VMware", "Intel", "AMD", "NVIDIA"],
        "nouns": ["Test", "Assessment", "Challenge", "Round", "Screen", "Interview", "Kit", "Prep", "Practice", "Drill", "Problem Set", "Quest", "Mission", "Milestone", "Track", "Path", "Roadmap", "Tournament", "Leaderboard", "Cup"],
        "verbs": ["Coding", "Technical", "Problem Solving", "Logic", "Analytical", "Quantitative", "Verbal", "Technical Communication", "System Design", "API Design", "Database", "Shell", "Regex", "SQL", "Python", "Java", "C++", "JavaScript", "Go", "Rust"],
        "topics": [
            "array manipulation", "string processing", "hash table", "stack and queue",
            "heap priority queue", "binary search tree", "trie data structure",
            "disjoint set union", "segment tree with lazy", "Fenwick tree",
            "suffix array", "KMP algorithm", "Rabin-Karp", "Z-algorithm",
            "Manacher's algorithm", "convex hull", "sweep line", "union find",
            "topological sort", "strongly connected", "bipartite matching",
            "maximum flow", "min cut", "DP optimization", "matrix exponentiation",
            "fast Fourier transform", "Chinese remainder", "modular arithmetic",
        ],
        "adj": ["Technical", "Algorithmic", "Data-Structured", "Optimized", "Elegant", "Clean", "Robust", "Scalable", "Maintainable", "Production-Ready"],
    },
    "MLH": {
        "depts": ["MLH", "Meta", "Google", "GitHub", "AWS", "DigitalOcean", "Stripe", "Slack", "Figma", "Notion", "Vercel", "Netlify", "Railway", "Replit", "GitPod", "Codesandbox", "Devfolio", "Polygon", "Filecoin", "Solana"],
        "nouns": ["Hackathon", "Workshop", "Bootcamp", "Build Week", "Sprint", "Challenge", "Showcase", "Incubator", "Accelerator", "Residency", "Fellowship", "Scholarship", "Grant", "Prize", "Award", "Competition", "League", "Series", "Circuit", "Season"],
        "verbs": ["Build", "Ship", "Launch", "Create", "Hack", "Design", "Code", "Develop", "Engineer", "Prototype", "Innovate", "Make", "Construct", "Assemble", "Produce"],
        "topics": [
            "open source contribution", "developer tooling", "API integration", "CLI tool",
            "browser extension", "mobile app", "web application", "data visualization",
            "devops pipeline", "CI/CD automation", "code review tool", "documentation generator",
            "accessibility tool", "performance monitoring", "error tracking", "feature flag",
            "developer experience", "API client", "graphQL playground", "database GUI",
            "auth system", "notification service", "real-time sync", "file upload service",
            "image optimization", "search engine", "caching layer", "rate limiter",
            "webhook receiver", "scheduler service", "queue processor", "background job",
        ],
        "adj": ["Open Source", "Developer-First", "Community-Driven", "Hackathon-Grade", "Build-First", "Ship-Fast", "Innovation-Focused", "Collaborative", "Experiment-Driven", "Prototype-Ready"],
    },
    "Devpost": {
        "depts": ["Devpost", "Microsoft", "Google Cloud", "AWS", "IBM", "Intel", "Twilio", "SendGrid", "Auth0", "Algolia", "Mapbox", "Esri", "Unity", "Unreal", "Apple", "Meta Reality Labs", "Qualcomm", "NVIDIA", "AMD", "Arm"],
        "nouns": ["Challenge", "Competition", "Grant", "Prize", "Award", "Showcase", "Gallery", "Spotlight", "Feature", "Highlight", "Exhibition", "Fair", "Expo", "Demo Day", "Pitch", "Showdown", "Battle", "Clash", "Cup", "Trophy"],
        "verbs": ["Innovate", "Create", "Solve", "Design", "Develop", "Pitch", "Demonstrate", "Prototype", "Build", "Engineer", "Deploy", "Showcase", "Launch", "Deliver", "Present"],
        "topics": [
            "computer vision", "natural language processing", "speech recognition",
            "augmented reality", "virtual reality", "mixed reality", "3D modeling",
            "game development", "interactive installation", "generative art",
            "creative coding", "data storytelling", "interactive visualization",
            "IoT prototype", "smart device", "wearable tech", "robotics control",
            "autonomous system", "edge computing", "cloud architecture",
            "mobile experience", "cross-platform app", "progressive web app",
            "voice interface", "gesture control", "biometric system", "emotion AI",
        ],
        "adj": ["Creative", "Innovative", "Impactful", "User-Centered", "Design-First", "Polished", "Production-Quality", "Demo-Ready", "Scaleable", "Experience-Driven"],
    },
}


def generate_problems(target_total=22000):
    all_problems = set()
    result = []
    seen_titles = set()

    platform_names = list(PLATFORMS.keys())
    max_per_platform = target_total // len(platform_names) + 1000

    attempts = 0
    while len(result) < target_total and attempts < target_total * 5:
        attempts += 1
        platform = random.choice(platform_names)
        config = PLATFORMS[platform]

        current_count = sum(1 for p in result if p["source_platform"] == platform)
        if current_count >= max_per_platform:
            continue

        dept = random.choice(config["depts"])
        noun = random.choice(config["nouns"])
        verb = random.choice(config["verbs"])
        topic = random.choice(config["topics"])
        adj = random.choice(config["adj"])
        domain = random.choice(DOMAINS)
        difficulty = random.choice(DIFFICULTIES)

        pattern = random.randint(0, 4)
        if pattern == 0:
            title = f"{verb} {noun}: {topic.title()}"
        elif pattern == 1:
            title = f"{adj} {topic.title()} {noun}"
        elif pattern == 2:
            title = f"{topic.title()} — {verb} {noun}"
        elif pattern == 3:
            title = f"{dept} {verb} {noun}: {topic.title()}"
        else:
            title = f"{adj} {noun} for {topic.title()}"

        if title in seen_titles:
            continue
        seen_titles.add(title)

        desc = (
            f"A {verb.lower()} {noun.lower()} focused on {topic}. "
            f"Participants will {verb.lower() if isinstance(verb, str) and not verb.endswith('-') else 'build'} "
            f"a {' '.join(adj.lower().split('-') if '-' in adj else [adj.lower()])} solution using "
            f"{domain.lower()} technologies. This competition is organized by {dept} and "
            f"offers mentorship, prize money, and potential incubation for winning teams."
        )

        tags = [domain.lower().replace("/", "-"), topic.split()[0].lower(), difficulty.lower()]
        year = random.choice([2024, 2025, 2026])

        links = {
            "D2C": "https://dare2compete.com/hackathons",
            "CodeChef": "https://codechef.com/contests",
            "HackerRank": "https://hackerrank.com/contests",
            "MLH": "https://mlh.io/seasons/2026/events",
            "Devpost": "https://devpost.com/hackathons",
        }
        link = links.get(platform, f"https://{platform.lower().replace(' ', '')}.com/hackathons")

        result.append({
            "title": title,
            "description": desc,
            "domain": domain,
            "organization": dept,
            "source_platform": platform,
            "source_year": year,
            "source_link": link,
            "tags": tags,
            "difficulty": difficulty,
            "is_open": random.random() > 0.3,
        })

    return result


def main():
    problems = generate_problems(25000)

    curated_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "curated_problems.json"
    )

    with open(curated_path, "w", encoding="utf-8") as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(problems)} curated problems")
    counts = {}
    for p in problems:
        counts[p["source_platform"]] = counts.get(p["source_platform"], 0) + 1
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
