import json
import random
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "platform_problems.json")

random.seed(123)

popular_platforms = {
    "Unstop": {
        "link": "https://unstop.com/hackathons",
        "orgs": [
            "Unstop", "Ministry of Education", "DST", "ISRO", "BHEL", "ONGC", "ICMR",
            "Ministry of Women and Child Development", "Ministry of Defence", "DRDO",
            "Indian Navy", "Indian Army", "Indian Air Force", "Coal India", "SAIL",
            "NTPC", "Indian Oil", "BPCL", "HPCL", "GAIL", "Power Grid", "LIC",
            "SBI", "RBI", "SEBI", "IRDAI", "PFRDA", "NSDC", "Skill India",
            "Startup India", "Invest India", "GeM", "UIDAI", "NHA", "CDAC",
        ],
        "domains": ["SpaceTech", "Robotics", "GreenTech", "HealthTech", "IoT", "Smart Cities", "Quantum", "EdTech", "AI/ML", "FinTech", "Blockchain", "Cybersecurity", "AgriTech", "MedTech"],
    },
    "Devpost": {
        "link": "https://devpost.com/hackathons",
        "orgs": [
            "Devpost", "Esri", "Algolia", "Twilio", "SendGrid", "Auth0", "Mapbox",
            "Unreal", "Redis", "MongoDB", "Cloudflare", "PlanetScale", "Fly.io",
            "Netlify", "Vercel", "GitHub", "Microsoft", "Google Cloud", "AWS",
            "Meta", "Apple", "Intel", "AMD", "NVIDIA", "Spotify", "Stripe",
            "Shopify", "Figma", "Notion", "Linear", "Supabase",
        ],
        "domains": ["AI/ML", "Web", "Mobile", "Gaming", "AR/VR", "Smart Cities", "Cybersecurity", "EdTech", "FinTech", "HealthTech"],
    },
    "MLH": {
        "link": "https://mlh.io/seasons/2026/events",
        "orgs": [
            "MLH", "Netlify", "Vercel", "AWS", "GitPod", "Codesandbox", "Polygon",
            "Filecoin", "Solana", "Railway", "Slack", "Twilio", "Algolia", "Esri",
            "SendGrid", "Mapbox", "GitHub", "DigitalOcean", "MongoDB", "Auth0",
            "Stripe", "Cloudflare", "Figma", "Linear", "Supabase",
        ],
        "domains": ["Web3", "Cloud", "AI/ML", "Mobile", "AR/VR", "Quantum", "DevOps", "EdTech", "Open Source", "Hardware"],
    },
    "HackerEarth": {
        "link": "https://hackerearth.com/hackathons",
        "orgs": [
            "HackerEarth", "Flipkart", "Swiggy", "Nykaa", "PhonePe", "Razorpay",
            "Capgemini", "Cognizant", "Infosys", "Wipro", "TCS", "Tech Mahindra",
            "Zomato", "Ola", "Paytm", "IBM", "Microsoft", "Google", "Intel",
            "Dell", "Accenture", "LTI", "Mindtree", "Mphasis", "HCL",
        ],
        "domains": ["AI/ML", "FinTech", "Cloud", "IoT", "Cybersecurity", "DevOps", "EdTech", "HealthTech", "AgriTech"],
    },
    "CodeChef": {
        "link": "https://codechef.com/contests",
        "orgs": ["CodeChef", "DigitalOcean", "MongoDB", "PlanetScale", "Redis", "Cloudflare", "Fly.io", "Algozenith", "Coding Ninjas", "Unacademy", "Physics Wallah", "Byju's"],
        "domains": ["Competitive Programming", "Algorithms", "Data Structures", "AI/ML", "Cloud", "Blockchain", "Smart Cities", "FinTech", "IoT"],
    },
    "HackerRank": {
        "link": "https://hackerrank.com/contests",
        "orgs": ["HackerRank", "Shopify", "Atlassian", "Goldman Sachs", "Barclays", "AMD", "Neon"],
        "domains": ["FinTech", "IoT", "Mobile", "Cybersecurity", "DevOps", "GreenTech", "HealthTech", "Robotics", "Algorithms", "Data Structures"],
    },
    "D2C": {
        "link": "https://dare2compete.com/hackathons",
        "orgs": ["Dare2Compete", "Schneider", "PwC", "KPMG", "Honeywell", "L&T", "BHEL", "GE", "Adobe", "ONGC", "Infosys", "ICMR", "ISRO", "DRDO"],
        "domains": ["GreenTech", "Robotics", "IoT", "AI/ML", "Cybersecurity", "Quantum", "HealthTech", "Energy", "Manufacturing"],
    },
    "Devfolio": {
        "link": "https://devfolio.com/hackathons",
        "orgs": ["Devfolio", "Polygon", "Filecoin", "Lens Protocol", "Ceramic", "Livepeer", "TheGraph", "Huddle01", "IPFS", "XMTP", "Push Protocol", "Ethereum Foundation", "Solana", "Chainlink", "Aave", "Uniswap"],
        "domains": ["Blockchain", "Web3", "DeFi", "Open Source", "NFT", "DAOs", "Zero Knowledge"],
    },
    "LeetCode": {
        "link": "https://leetcode.com/contest",
        "orgs": ["LeetCode", "Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix", "Uber", "Stripe", "Atlassian"],
        "domains": ["Algorithms", "Data Structures", "System Design", "Database", "Shell Scripting", "Concurrency"],
    },
    "Codeforces": {
        "link": "https://codeforces.com/contests",
        "orgs": ["Codeforces", "Telegram", "Tinkoff", "Yandex", "JetBrains", "VK", "Sberbank"],
        "domains": ["Competitive Programming", "Algorithms", "Mathematics", "Data Structures", "Graph Theory", "Number Theory", "Combinatorics", "Dynamic Programming"],
    },
    "ETHGlobal": {
        "link": "https://ethglobal.com/events",
        "orgs": ["ETHGlobal", "Ethereum Foundation", "Optimism", "Arbitrum", "Polygon", "Chainlink", "Uniswap", "Aave", "ENS", "Lens Protocol"],
        "domains": ["Blockchain", "Web3", "DeFi", "NFT", "DAOs", "Zero Knowledge", "Smart Contracts", "Layer 2"],
    },
}

titles_by_domain = {
    "AI/ML": [
        "AI-powered {focus} System", "Machine Learning {focus} Model", "Deep Learning {focus} Pipeline",
        "Intelligent {focus} Assistant", "Predictive {focus} Engine", "Automated {focus} Classifier",
    ],
    "Blockchain": [
        "Decentralized {focus} Platform", "Blockchain {focus} Protocol", "Smart Contract {focus} System",
        "Web3 {focus} DApp", "Trustless {focus} Network", "Tokenized {focus} Marketplace",
    ],
    "Web3": [
        "Decentralized {focus} Application", "Web3 {focus} Integration", "On-chain {focus} Protocol",
        "Decentralized {focus} Network", "Blockchain {focus} Aggregator",
    ],
    "FinTech": [
        "Digital {focus} Platform", "Automated {focus} System", "Real-time {focus} Engine",
        "Smart {focus} Solution", "AI-driven {focus} Tool", "Mobile {focus} Application",
    ],
    "IoT": [
        "Smart {focus} Monitoring System", "IoT-enabled {focus} Network", "Connected {focus} Platform",
        "Intelligent {focus} Sensor Array", "Real-time {focus} Tracking System",
    ],
    "Cybersecurity": [
        "AI-based {focus} Detection System", "Automated {focus} Prevention Platform",
        "Intelligent {focus} Monitoring Tool", "Zero Trust {focus} Framework",
        "Real-time {focus} Threat Analyzer",
    ],
    "EdTech": [
        "Adaptive {focus} Learning Platform", "Gamified {focus} Education App",
        "Interactive {focus} Training System", "Personalized {focus} Tutor",
        "Collaborative {focus} Classroom Tool",
    ],
    "HealthTech": [
        "AI-powered {focus} Diagnostic Tool", "Digital {focus} Health Platform",
        "Remote {focus} Monitoring System", "Smart {focus} Healthcare Solution",
        "ML-based {focus} Screening System",
    ],
    "GreenTech": [
        "Smart {focus} Management System", "Sustainable {focus} Monitoring Platform",
        "AI-optimized {focus} Solution", "IoT-based {focus} Conservation Tool",
        "Automated {focus} Efficiency System",
    ],
    "Robotics": [
        "Autonomous {focus} Robot", "Intelligent {focus} Navigation System",
        "AI-driven {focus} Manipulator", "Smart {focus} Automation Platform",
        "Computer Vision {focus} Robot",
    ],
    "Mobile": [
        "Cross-platform {focus} Mobile App", "Mobile-first {focus} Solution",
        "Real-time {focus} Mobile Platform", "Smart {focus} Mobile Assistant",
    ],
    "Cloud": [
        "Cloud-native {focus} Platform", "Scalable {focus} Microservice",
        "Distributed {focus} System", "Serverless {focus} Architecture",
        "Multi-cloud {focus} Management Tool",
    ],
    "Quantum": [
        "Quantum {focus} Algorithm", "Hybrid Quantum {focus} System",
        "Quantum-resistant {focus} Protocol", "Quantum {focus} Simulator",
    ],
    "AR/VR": [
        "Immersive {focus} AR Experience", "VR-based {focus} Training System",
        "Mixed Reality {focus} Platform", "AR {focus} Visualization Tool",
    ],
    "Gaming": [
        "Multiplayer {focus} Game", "AI-powered {focus} Game Engine",
        "Procedural {focus} Generation Tool", "Cloud {focus} Gaming Platform",
    ],
    "Smart Cities": [
        "Smart {focus} Management Platform", "Urban {focus} Monitoring System",
        "Intelligent {focus} Infrastructure", "Connected {focus} City Solution",
    ],
    "AgriTech": [
        "Smart {focus} Farming Solution", "AI-powered {focus} Crop System",
        "IoT-based {focus} Monitoring", "Drone-based {focus} Agriculture Platform",
    ],
    "SpaceTech": [
        "Satellite {focus} Data Platform", "Space {focus} Monitoring System",
        "AI-based {focus} Space Solution", "Autonomous {focus} Spacecraft Tool",
    ],
    "DeFi": [
        "Decentralized {focus} Protocol", "Automated {focus} Liquidity System",
        "Yield {focus} Optimization Platform", "Cross-chain {focus} Bridge",
        "On-chain {focus} Lending Protocol",
    ],
    "Algorithms": [
        "Efficient {focus} Algorithm Implementation", "Optimized {focus} Data Structure",
        "High-Performance {focus} Solver", "Parallel {focus} Computation Framework",
    ],
    "Data Structures": [
        "Efficient {focus} Data Structure", "Scalable {focus} Storage System",
        "Optimized {focus} Index Structure", "Distributed {focus} Data Layer",
    ],
    "Competitive Programming": [
        "Competitive {focus} Problem Solver", "Algorithmic {focus} Optimization",
        "Multi-threaded {focus} Solution", "Online {focus} Judge Integration",
    ],
    "System Design": [
        "Scalable {focus} System Architecture", "Distributed {focus} Backend Service",
        "High-availability {focus} Infrastructure", "Fault-tolerant {focus} Platform",
    ],
}

focuses = [
    "Fraud Detection", "Sentiment Analysis", "Anomaly Detection", "Object Detection",
    "Face Recognition", "Speech Recognition", "Language Translation", "Text Summarization",
    "Question Answering", "Recommendation Engine", "Personalized Search", "Content Moderation",
    "Image Classification", "Video Analytics", "Time Series Forecasting", "Demand Prediction",
    "Inventory Optimization", "Supply Chain Tracking", "Price Optimization", "Risk Assessment",
    "Credit Scoring", "Portfolio Management", "Algorithmic Trading", "Insurance Claim",
    "Customer Churn", "User Segmentation", "A/B Testing", "Conversion Rate", "Ad Targeting",
    "Network Intrusion", "Phishing Detection", "Malware Analysis", "Vulnerability Scanning",
    "Access Control", "Identity Verification", "Data Encryption", "Privacy Preserving",
    "Secure Multi-party", "Zero Knowledge Proof", "Consensus Mechanism", "Sharding",
    "Cross-chain Communication", "Layer 2 Scaling", "State Channel", "Oracle Integration",
    "Automated Market Making", "Liquidity Provision", "Yield Aggregation", "Flash Loan",
    "NFT Marketplace", "Token Gating", "DAO Governance", "Soulbound Token",
    "Attendance Tracking", "Proctoring", "Grade Prediction", "Plagiarism Detection",
    "Skill Assessment", "Career Path", "Adaptive Testing", "Curriculum Planning",
    "Medical Diagnosis", "Drug Discovery", "Genomic Sequencing", "Protein Folding",
    "Patient Monitoring", "Health Records", "Appointment Scheduling", "Telemedicine",
    "Triage System", "Epidemic Tracking", "Vaccine Distribution", "Mental Health",
    "Energy Optimization", "Carbon Tracking", "Waste Management", "Water Conservation",
    "Emissions Monitoring", "Renewable Integration", "Smart Grid", "Building Efficiency",
    "Autonomous Navigation", "Path Planning", "Manipulation Control", "Humanoid Locomotion",
    "Drone Swarm", "SLAM Mapping", "Grasp Planning", "Force Control",
    "Air Quality", "Water Quality", "Noise Mapping", "Traffic Flow",
    "Parking Management", "Waste Collection", "Street Lighting", "Urban Planning",
    "Crop Disease", "Yield Prediction", "Soil Analysis", "Irrigation Scheduling",
    "Pest Detection", "Weed Removal", "Harvest Optimization", "Quality Grading",
    "Satellite Imagery", "Remote Sensing", "Orbit Determination", "Space Debris",
]

for d in ["Algorithms", "Data Structures", "Competitive Programming", "System Design"]:
    focuses.extend([
        "Binary Search", "Dynamic Programming", "Graph Traversal", "Shortest Path",
        "Minimum Spanning Tree", "String Matching", "Sorting", "Searching",
        "Hash Table", "Segment Tree", "Fenwick Tree", "Trie", "Union Find",
        "Heap", "Stack", "Queue", "Linked List", "Tree", "Graph",
    ])

descriptions_pool = [
    "Develop {an} {adj} {solution} that {purpose}. The platform should support {feat1}, {feat2}, and {feat3}. Participants will build a working prototype and present their solution to a panel of industry experts.",
    "Build {an} {adj} {solution} for {purpose}. Key requirements include {feat1}, {feat2}, and {feat3}. Winning teams receive mentorship, cash prizes, and potential incubation opportunities.",
    "Create {an} {adj} {solution} to {purpose}. The solution must demonstrate {feat1}, {feat2}, and {feat3}. Organized in partnership with leading industry experts and investors.",
    "Design {an} {adj} {solution} focused on {purpose}. Your implementation should cover {feat1}, {feat2}, and {feat3}. Top teams will get a chance to pitch to venture capitalists.",
    "Architect {an} {adj} {solution} that {purpose}. This includes implementing {feat1}, {feat2}, and {feat3}. Winners receive exciting prizes, mentorship, and recognition.",
]

solutions = [
    "platform", "system", "application", "solution", "tool", "framework",
    "pipeline", "service", "engine", "dashboard", "network", "protocol",
    "dapp", "contract", "interface", "api", "library", "sdk",
]

adjectives = [
    "scalable", "secure", "efficient", "intelligent", "robust", "resilient",
    "production-ready", "enterprise-grade", "user-centric", "high-performance",
    "fault-tolerant", "real-time", "cloud-native", "cross-platform", "open-source",
    "decentralized", "privacy-preserving", "energy-efficient", "low-latency", "modular",
]

features_pool = [
    "real-time data processing and analytics",
    "RESTful API design with comprehensive documentation",
    "microservices architecture for modularity and scaling",
    "role-based access control with JWT authentication",
    "responsive UI supporting mobile, tablet, and desktop",
    "integration with third-party APIs and services",
    "end-to-end encryption for data in transit and at rest",
    "automated CI/CD pipeline with testing and deployment",
    "containerized deployment using Docker and Kubernetes",
    "support for multiple concurrent users with session management",
    "audit logging with complete traceability",
    "interactive data visualization with charts and graphs",
    "geospatial mapping and location-based services",
    "push notifications via email, SMS, and in-app",
    "offline-first capability with data synchronization",
    "multi-language and localization support",
    "search functionality with full-text indexing and filters",
    "automated backup and disaster recovery mechanisms",
    "rate limiting and API throttling for security",
    "event-driven architecture using message queues",
]

target = 5000
print(f"Generating {target} problems for popular platforms...")

generated = []
for i in range(target):
    platform_name = random.choice(list(popular_platforms.keys()))
    platform = popular_platforms[platform_name]
    org = random.choice(platform["orgs"])
    domain = random.choice(platform["domains"])
    year = random.choice([2022, 2023, 2024, 2025, 2026])
    difficulty = random.choice(["Beginner", "Intermediate", "Advanced"])

    is_open = random.choice([True, False])
    if difficulty == "Beginner":
        is_open = True

    focus = random.choice(focuses)
    adj = random.choice(adjectives)
    solution = random.choice(solutions)
    an = "an" if adj[0] in "aeiou" else "a"
    purpose = random.choice([
        f"helps {org.lower()} automate {focus.lower()} workflows",
        f"enables real-time {focus.lower()} monitoring and analysis",
        f"provides intelligent {focus.lower()} recommendations",
        f"optimizes {focus.lower()} processes for better efficiency",
        f"detects and prevents {focus.lower()}-related issues",
        f"transforms legacy {focus.lower()} systems into modern digital platforms",
        f"empowers users with actionable {focus.lower()} insights",
        f"streamlines complex {focus.lower()} operations",
        f"enhances decision-making through {focus.lower()} analytics",
        f"democratizes access to {focus.lower()} capabilities",
    ])

    feat1, feat2, feat3 = random.sample(features_pool, 3)
    desc_template = random.choice(descriptions_pool)
    description = desc_template.format(an=an, adj=adj, solution=solution, purpose=purpose, feat1=feat1, feat2=feat2, feat3=feat3)

    domain_titles = titles_by_domain.get(domain, ["{focus} Platform"])
    title_template = random.choice(domain_titles)
    title = title_template.replace("{focus}", focus)
    title = title.replace("{prefix}", random.choice(["AI-powered", "Smart", "Automated", "Intelligent", "Connected", "Adaptive", "Scalable"]))
    title = title.replace("{suffix}", random.choice(["Platform", "System", "Solution", "Tool", "Framework", "Engine", "Service", "Network"]))

    domain_tag = domain.lower().replace("/", "-").replace(" ", "-").replace("&", "and")
    tags = list(set([
        domain_tag,
        focus.lower().replace(" ", "-"),
        random.choice(["ai", "ml", "blockchain", "web3", "cloud", "iot", "mobile", "api", "data", "automation"]),
        random.choice(["security", "scalability", "analytics", "real-time", "open-source", "devops", "saas", "microservices"]),
    ]))[:5]

    problem = {
        "title": title,
        "description": description,
        "domain": domain,
        "organization": org,
        "category": "Software",
        "source_platform": platform_name,
        "source_year": year,
        "source_link": platform["link"],
        "tags": tags,
        "difficulty": difficulty,
        "is_open": is_open,
    }
    generated.append(problem)

    if (i + 1) % 1000 == 0:
        print(f"  Generated {i + 1}/{target}...")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(generated, f, indent=2, ensure_ascii=False)

print(f"\nDone! {len(generated)} problems saved to platform_problems.json")
print(f"Platforms covered: {', '.join(popular_platforms.keys())}")
