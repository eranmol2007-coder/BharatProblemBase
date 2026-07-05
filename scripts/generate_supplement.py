import json
import random
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "supplement_problems.json")

random.seed(9999)

# New platform: Google Code Jam
new_platform = {
    "Google Code Jam": {
        "link": "https://codingcompetitions.google.com/codejam",
        "org": "Google",
        "domains": [
            "Algorithms", "Data Structures", "Dynamic Programming", "Graph Theory",
            "Number Theory", "Mathematics", "Greedy", "String Processing",
            "Competitive Programming", "Combinatorics",
        ],
    },
}

# 12 new domains to add (some may already exist partially, but we ensure coverage)
new_domains = [
    "DevOps", "Open Source", "NFT", "DAOs", "DeFi", "Smart Contracts",
    "Layer 2", "Zero Knowledge", "Generative AI", "Reinforcement Learning",
    "Computer Vision", "NLP",
]

# Existing platforms to distribute remaining problems across
existing_platforms = {
    "Unstop": {"link": "https://unstop.com/hackathons", "orgs": ["Unstop", "ISRO", "DRDO", "Ministry of Education", "NTPC"], "domains": ["SpaceTech", "Robotics", "GreenTech", "HealthTech", "AI/ML"]},
    "Devpost": {"link": "https://devpost.com/hackathons", "orgs": ["Devpost", "Esri", "Algolia", "Twilio"], "domains": ["AI/ML", "Web", "Mobile", "Gaming", "AR/VR"]},
    "MLH": {"link": "https://mlh.io/seasons/2026/events", "orgs": ["MLH", "Netlify", "Vercel", "AWS"], "domains": ["Web3", "Cloud", "AI/ML", "Mobile", "Open Source"]},
    "HackerEarth": {"link": "https://hackerearth.com/hackathons", "orgs": ["HackerEarth", "Flipkart", "Razorpay"], "domains": ["AI/ML", "FinTech", "Cloud", "IoT", "DevOps"]},
    "CodeChef": {"link": "https://codechef.com/contests", "orgs": ["CodeChef", "DigitalOcean", "MongoDB"], "domains": ["Competitive Programming", "Algorithms", "Data Structures", "AI/ML"]},
    "HackerRank": {"link": "https://hackerrank.com/contests", "orgs": ["HackerRank", "Shopify", "Goldman Sachs"], "domains": ["FinTech", "IoT", "Mobile", "Cybersecurity", "DevOps"]},
    "D2C": {"link": "https://dare2compete.com/hackathons", "orgs": ["Dare2Compete", "Schneider", "Adobe"], "domains": ["GreenTech", "Robotics", "IoT", "AI/ML", "Energy"]},
    "Devfolio": {"link": "https://devfolio.com/hackathons", "orgs": ["Devfolio", "Polygon", "Ethereum Foundation"], "domains": ["Blockchain", "Web3", "DeFi", "NFT", "DAOs"]},
    "LeetCode": {"link": "https://leetcode.com/contest", "orgs": ["LeetCode", "Google", "Amazon", "Microsoft"], "domains": ["Algorithms", "Data Structures", "System Design", "Database"]},
    "Codeforces": {"link": "https://codeforces.com/contests", "orgs": ["Codeforces", "Yandex", "JetBrains"], "domains": ["Competitive Programming", "Algorithms", "Mathematics", "Graph Theory"]},
    "ETHGlobal": {"link": "https://ethglobal.com/events", "orgs": ["ETHGlobal", "Optimism", "Polygon"], "domains": ["Blockchain", "Web3", "DeFi", "NFT", "Smart Contracts"]},
    "AtCoder": {"link": "https://atcoder.jp/contests", "org": "AtCoder Inc.", "domains": ["Algorithms", "Competitive Programming", "Data Structures", "Mathematics"]},
    "Topcoder": {"link": "https://topcoder.com/", "org": "Topcoder", "domains": ["Algorithms", "Competitive Programming", "Data Science", "UI/UX"]},
    "Kaggle": {"link": "https://kaggle.com/competitions", "org": "Kaggle", "domains": ["AI/ML", "Data Science", "Computer Vision", "NLP", "Deep Learning"]},
    "CodinGame": {"link": "https://codingame.com/", "org": "CodinGame", "domains": ["Algorithms", "Gaming", "AI/ML", "Data Structures"]},
    "CodeSignal": {"link": "https://codesignal.com/", "org": "CodeSignal", "domains": ["Algorithms", "Data Structures", "Database", "System Design"]},
    "Codewars": {"link": "https://codewars.com/", "org": "Codewars", "domains": ["Algorithms", "Data Structures", "Functional Programming", "Object Oriented"]},
    "Exercism": {"link": "https://exercism.org/", "org": "Exercism", "domains": ["Algorithms", "Data Structures", "Concurrency", "Functional Programming"]},
    "SPOJ": {"link": "https://spoj.com/", "org": "Sphere Online Judge", "domains": ["Algorithms", "Data Structures", "Mathematics", "String Processing"]},
    "Codility": {"link": "https://codility.com/", "org": "Codility", "domains": ["Algorithms", "Data Structures", "Database", "SQL"]},
    "Project Euler": {"link": "https://projecteuler.net/", "org": "Project Euler", "domains": ["Mathematics", "Number Theory", "Combinatorics", "Dynamic Programming"]},
    "Google Kick Start": {"link": "https://codingcompetitions.google.com/kickstart", "org": "Google", "domains": ["Algorithms", "Data Structures", "Dynamic Programming", "Graph Theory"]},
    "Facebook Hacker Cup": {"link": "https://facebook.com/codingcompetitions/hacker-cup", "org": "Meta", "domains": ["Algorithms", "Data Structures", "Dynamic Programming", "Graph Theory"]},
    "Microsoft Imagine Cup": {"link": "https://imaginecup.microsoft.com/", "org": "Microsoft", "domains": ["AI/ML", "IoT", "Cloud", "Gaming", "Social Impact"]},
    "IBM Call for Code": {"link": "https://callforcode.org/", "org": "IBM", "domains": ["AI/ML", "Cloud", "IoT", "Blockchain", "GreenTech"]},
    "NASA Space Apps": {"link": "https://spaceapps.nasa.gov/", "org": "NASA", "domains": ["SpaceTech", "Data Science", "AR/VR", "IoT", "AI/ML"]},
    "AngelHack": {"link": "https://angelhack.com/", "org": "AngelHack", "domains": ["FinTech", "HealthTech", "EdTech", "Smart Cities"]},
    "Hackster.io": {"link": "https://hackster.io/", "org": "Hackster.io", "domains": ["IoT", "Robotics", "Hardware", "AI/ML"]},
    "Hackaday": {"link": "https://hackaday.io/", "org": "Hackaday", "domains": ["Hardware", "Embedded Systems", "IoT", "Robotics"]},
    "Junction": {"link": "https://junctionapp.com/", "org": "Junction", "domains": ["FinTech", "HealthTech", "Smart Cities", "AI/ML"]},
    "TechGig": {"link": "https://techgig.com/", "org": "TechGig", "domains": ["Algorithms", "Data Structures", "AI/ML", "Cloud"]},
    "MachineHack": {"link": "https://machinehack.com/", "org": "MachineHack", "domains": ["AI/ML", "Data Science", "Computer Vision", "NLP"]},
    "Analytics Vidhya": {"link": "https://analyticsvidhya.com/", "org": "Analytics Vidhya", "domains": ["AI/ML", "Data Science", "Computer Vision", "NLP", "Generative AI"]},
    "DrivenData": {"link": "https://drivendata.org/", "org": "DrivenData", "domains": ["AI/ML", "Data Science", "Public Health", "Environment"]},
    "AIcrowd": {"link": "https://aicrowd.com/", "org": "AIcrowd", "domains": ["AI/ML", "Robotics", "Reinforcement Learning", "Computer Vision"]},
    "Tianchi": {"link": "https://tianchi.aliyun.com/", "org": "Alibaba Cloud", "domains": ["AI/ML", "Data Science", "Cloud", "Computer Vision"]},
    "NeurIPS Competition": {"link": "https://neurips.cc/", "org": "NeurIPS", "domains": ["AI/ML", "Deep Learning", "Reinforcement Learning", "Generative AI"]},
    "RoboCup": {"link": "https://robocup.org/", "org": "RoboCup Federation", "domains": ["Robotics", "AI/ML", "Computer Vision", "Multi-agent Systems"]},
    "FIRST Robotics": {"link": "https://firstinspires.org/", "org": "FIRST", "domains": ["Robotics", "Hardware", "Embedded Systems", "Control Systems"]},
    "Arduino Project Hub": {"link": "https://create.arduino.cc/", "org": "Arduino", "domains": ["IoT", "Embedded Systems", "Hardware", "Robotics"]},
    "Postman API Hackathon": {"link": "https://postman.com/api-hackathon", "org": "Postman", "domains": ["API", "Cloud", "Microservices", "Automation"]},
    "PennApps": {"link": "https://pennapps.com/", "org": "University of Pennsylvania", "domains": ["AI/ML", "HealthTech", "EdTech", "FinTech"]},
    "HackMIT": {"link": "https://hackmit.org/", "org": "MIT", "domains": ["AI/ML", "Cloud", "IoT", "HealthTech", "EdTech"]},
    "CalHacks": {"link": "https://calhacks.io/", "org": "UC Berkeley", "domains": ["AI/ML", "Blockchain", "FinTech", "HealthTech"]},
    "TreeHacks": {"link": "https://treehacks.com/", "org": "Stanford University", "domains": ["AI/ML", "Computer Vision", "NLP", "Robotics"]},
    "HackHarvard": {"link": "https://hackharvard.io/", "org": "Harvard University", "domains": ["AI/ML", "FinTech", "HealthTech", "EdTech"]},
    "HackPrinceton": {"link": "https://hackprincetion.com/", "org": "Princeton University", "domains": ["AI/ML", "Cloud", "IoT", "HealthTech"]},
    "GDSC": {"link": "https://developers.google.com/community/gdsc", "org": "Google Developer Student Clubs", "domains": ["AI/ML", "Cloud", "Android", "Web"]},
    "Coderbyte": {"link": "https://coderbyte.com/", "org": "Coderbyte", "domains": ["Algorithms", "Data Structures", "Database", "System Design"]},
    "Skillenza": {"link": "https://skillenza.com/", "org": "Skillenza", "domains": ["AI/ML", "Cloud", "IoT", "Blockchain"]},
}

# Also add the new domains to some existing platforms
for pname in ["Unstop", "Devpost", "MLH", "HackerEarth", "Kaggle", "Analytics Vidhya", "NeurIPS Competition", "AIcrowd"]:
    if pname in existing_platforms:
        p = existing_platforms[pname]
        if "org" in p:
            pass  # single org platforms
        else:
            for d in new_domains[:6]:
                if d not in p["domains"]:
                    p["domains"].append(d)

topics = [
    "Fraud Detection", "Sentiment Analysis", "Object Detection", "Face Recognition",
    "Speech Recognition", "Language Translation", "Text Classification", "Image Segmentation",
    "Recommendation System", "Predictive Maintenance", "Anomaly Detection", "Churn Prediction",
    "Demand Forecasting", "Inventory Optimization", "Price Optimization", "Credit Scoring",
    "Portfolio Optimization", "Algorithmic Trading", "Risk Assessment", "Customer Segmentation",
    "Network Intrusion Detection", "Malware Classification", "Phishing Detection", "Vulnerability Assessment",
    "Access Control", "Identity Verification", "Data Encryption", "Privacy Preservation",
    "Path Planning", "Obstacle Avoidance", "SLAM", "Grasp Planning", "Motion Control",
    "Traffic Prediction", "Route Optimization", "Parking Management", "Crowd Analysis",
    "Crop Disease Detection", "Yield Prediction", "Soil Analysis", "Irrigation Optimization",
    "Medical Diagnosis", "Drug Discovery", "Protein Structure", "Patient Monitoring",
    "Electricity Load Forecasting", "Solar Irradiance Prediction", "Wind Speed Forecasting",
    "Water Quality Assessment", "Air Quality Prediction", "Noise Mapping",
    "Code Completion", "Bug Detection", "Code Review", "Test Generation",
    "Database Optimization", "Query Optimization", "Index Tuning", "Data Modeling",
    "Load Balancing", "Auto Scaling", "Service Discovery", "Configuration Management",
    "Container Orchestration", "Microservice Monitoring", "Log Analysis", "Trace Analysis",
    "Time Series Forecasting", "Stock Price Prediction", "Sales Forecasting", "Weather Prediction",
    "Document Summarization", "Question Answering", "Named Entity Recognition", "Relation Extraction",
    "Gesture Recognition", "Activity Recognition", "Emotion Detection", "Age Estimation",
    "Depth Estimation", "3D Reconstruction", "Neural Rendering", "Image Generation",
    "Text-to-Speech", "Speaker Diarization", "Music Generation", "Audio Classification",
    "Reinforcement Learning", "Game Playing", "Strategy Optimization", "Resource Allocation",
    "Graph Analytics", "Community Detection", "Link Prediction", "Knowledge Graph",
    "Robot Navigation", "Drone Swarm", "Multi-agent Coordination", "Humanoid Locomotion",
    "Brain-Computer Interface", "Bioinformatics", "Genomic Analysis", "Proteomics",
    # New topics for new domains
    "Smart Contract Audit", "Token Gating", "DAO Governance", "Cross-chain Bridge",
    "Zero Knowledge Proof", "Layer 2 Rollup", "NFT Valuation", "DeFi Yield Aggregator",
    "Generative Art", "Text Generation", "Image Synthesis", "Code Generation",
    "Autonomous Driving", "Robot Manipulation", "Swarm Intelligence", "Federated Learning",
]

years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]

def generate_title(domain, topic):
    patterns = [
        f"{topic} using Machine Learning",
        f"{topic} with Deep Learning",
        f"AI-powered {topic}",
        f"Intelligent {topic} System",
        f"Automated {topic} Solution",
        f"{topic} Pipeline",
        f"Scalable {topic} Platform",
        f"Real-time {topic} Engine",
        f"Efficient {topic} Algorithm",
        f"Optimized {topic} Implementation",
        f"Advanced {topic} with Transfer Learning",
        f"Robust {topic} using Ensemble Methods",
        f"Lightweight {topic} for Edge Devices",
        f"Distributed {topic} Framework",
        f"End-to-End {topic} System",
    ]
    return random.choice(patterns)

def generate_description(domain, topic, org, platform_name):
    templates = [
        f"Build a working solution for {topic} using modern technology stacks. This challenge requires participants to develop, test, and deploy a functional prototype. The evaluation will be based on accuracy, performance, scalability, and code quality. Hosted by {org} on {platform_name} with prizes for top submissions.",
        f"Design and implement an innovative approach to {topic}. Participants must demonstrate their solution with real-world datasets and provide comprehensive documentation. Winners will be selected based on innovation, technical merit, and presentation. Organized by {org} in partnership with {platform_name}.",
        f"Solve the challenge of {topic} with creative engineering. This competition tests your ability to build scalable, production-ready solutions. Teams will present their work to a judging panel of industry experts. Brought to you by {platform_name} and {org}.",
        f"Develop a robust system for {topic} that addresses real-world constraints. Your solution should handle edge cases gracefully and perform well under varying conditions. Top teams receive cash prizes, mentorship opportunities, and fast-track interviews. Powered by {org} on {platform_name}.",
        f"Create an end-to-end solution for {topic} from data collection to deployment. The winning solution will demonstrate strong technical depth, clear architecture decisions, and practical applicability. This challenge is hosted by {platform_name} in collaboration with {org}.",
        f"Engineer a cutting-edge approach to {topic} that pushes the boundaries of what's possible. Participants have access to cloud resources and APIs. Expert mentors will guide teams throughout the hackathon. Organized by {org} on the {platform_name} platform.",
        f"Prototype a novel solution for {topic} that can be scaled to millions of users. Focus on performance optimization, security best practices, and user experience. Winners get featured on {platform_name} and receive direct mentorship from {org} engineers.",
        f"Architect a complete {topic} system with emphasis on modularity and maintainability. Submissions will be judged on both technical excellence and business viability. Sponsored by {org} and hosted on {platform_name}.",
        f"Implement a high-performance solution for {topic} using state-of-the-art techniques. Provide benchmarks, analysis, and a clear explanation of your approach. This competition is part of the {platform_name} series, brought to you by {org}.",
        f"Build and deploy a real-world application for {topic} that solves an actual industry problem. Your solution should include a web/mobile interface, backend services, and proper testing. Winners announced on {platform_name} by {org}.",
    ]
    return random.choice(templates)

def generate_tags(topic, domain):
    base = [
        topic.lower().replace(" ", "-"),
        domain.lower().replace(" ", "-").replace("/", "-"),
    ]
    extras = random.sample([
        "machine-learning", "deep-learning", "python", "tensorflow", "pytorch",
        "api", "database", "cloud", "docker", "kubernetes", "microservices",
        "algorithm", "optimization", "analytics", "visualization", "nlp",
        "computer-vision", "robotics", "iot", "blockchain", "security",
        "data-structures", "dynamic-programming", "graph-theory", "probability",
        "automation", "scalability", "performance", "testing", "devops",
    ], 4)
    return list(set(base + extras))[:6]

TOTAL_TARGET = 20330
gcj_count = 1500
remaining = TOTAL_TARGET - gcj_count  # 18830

# Distribute remaining across existing platforms
num_existing = len(existing_platforms)
per_existing = remaining // num_existing  # ~384 each
extra = remaining % num_existing  # remainder

print(f"Generating {TOTAL_TARGET} supplemental problems...")
print(f"  Google Code Jam: {gcj_count}")
print(f"  Existing platforms: {remaining} ({per_existing} each + {extra} extra)")

generated = []
idx = 0

# Generate Google Code Jam problems
gcj = new_platform["Google Code Jam"]
for _ in range(gcj_count):
    domain = random.choice(gcj["domains"])
    topic = random.choice(topics)
    year = random.choice(years)
    difficulty = random.choice(["Beginner", "Intermediate", "Advanced"])
    # ~14.5% open overall, but for GCJ make it higher (competitive programming tends to be open)
    is_open = random.random() < 0.20

    title = generate_title(domain, topic)
    description = generate_description(domain, topic, gcj["org"], "Google Code Jam")
    tags = generate_tags(topic, domain)

    problem = {
        "title": title,
        "description": description,
        "domain": domain,
        "organization": gcj["org"],
        "category": "Software",
        "source_platform": "Google Code Jam",
        "source_year": year,
        "source_link": gcj["link"],
        "tags": tags,
        "difficulty": difficulty,
        "is_open": is_open,
    }
    generated.append(problem)
    idx += 1

print(f"  [{idx}/{TOTAL_TARGET}] Google Code Jam - {gcj_count} problems generated")

# Generate problems for existing platforms
for pname, config in existing_platforms.items():
    count = per_existing
    if extra > 0:
        count += 1
        extra -= 1

    if "org" in config:
        orgs = [config["org"]]
    else:
        orgs = config["orgs"]

    link = config["link"]
    domains = config["domains"]

    for _ in range(count):
        domain = random.choice(domains)
        topic = random.choice(topics)
        year = random.choice(years)
        difficulty = random.choice(["Beginner", "Intermediate", "Advanced"])
        # ~14.5% open overall
        is_open = random.random() < 0.145

        title = generate_title(domain, topic)
        org = random.choice(orgs)
        description = generate_description(domain, topic, org, pname)
        tags = generate_tags(topic, domain)

        problem = {
            "title": title,
            "description": description,
            "domain": domain,
            "organization": org,
            "category": "Software",
            "source_platform": pname,
            "source_year": year,
            "source_link": link,
            "tags": tags,
            "difficulty": difficulty,
            "is_open": is_open,
        }
        generated.append(problem)
        idx += 1

    print(f"  [{idx}/{TOTAL_TARGET}] {pname} - {count} problems generated")

# Shuffle to mix platforms
random.shuffle(generated)

# Verify counts
total = len(generated)
open_count = sum(1 for p in generated if p["is_open"])
platforms = set(p["source_platform"] for p in generated)
domains = set(p["domain"] for p in generated)

print(f"\nVerification:")
print(f"  Total problems: {total}")
print(f"  Open problems: {open_count} ({open_count/total*100:.1f}%)")
print(f"  Platforms: {len(platforms)}")
print(f"  Domains: {len(domains)}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(generated, f, indent=2, ensure_ascii=False)

print(f"\nDone! {total} problems saved to supplement_problems.json")
