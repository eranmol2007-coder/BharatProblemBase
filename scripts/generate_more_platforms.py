import json
import random
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "more_platforms.json")

random.seed(456)

platforms_config = {
    "AtCoder": {"link": "https://atcoder.jp/contests", "org": "AtCoder Inc.", "domains": ["Algorithms", "Competitive Programming", "Data Structures", "Mathematics", "Dynamic Programming", "Graph Theory"]},
    "Topcoder": {"link": "https://topcoder.com/", "org": "Topcoder", "domains": ["Algorithms", "Competitive Programming", "Data Science", "UI/UX", "Software Development"]},
    "Kaggle": {"link": "https://kaggle.com/competitions", "org": "Kaggle", "domains": ["AI/ML", "Data Science", "Computer Vision", "NLP", "Deep Learning", "Tabular Data"]},
    "CodinGame": {"link": "https://codingame.com/", "org": "CodinGame", "domains": ["Algorithms", "Gaming", "AI/ML", "Data Structures", "Competitive Programming"]},
    "CodeSignal": {"link": "https://codesignal.com/", "org": "CodeSignal", "domains": ["Algorithms", "Data Structures", "Database", "System Design", "Frontend"]},
    "Codewars": {"link": "https://codewars.com/", "org": "Codewars", "domains": ["Algorithms", "Data Structures", "Functional Programming", "Object Oriented", "Refactoring"]},
    "Exercism": {"link": "https://exercism.org/", "org": "Exercism", "domains": ["Algorithms", "Data Structures", "Concurrency", "Functional Programming", "OOP"]},
    "SPOJ": {"link": "https://spoj.com/", "org": "Sphere Online Judge", "domains": ["Algorithms", "Data Structures", "Mathematics", "String Processing", "Graph Theory"]},
    "Codility": {"link": "https://codility.com/", "org": "Codility", "domains": ["Algorithms", "Data Structures", "Database", "SQL", "System Design"]},
    "Project Euler": {"link": "https://projecteuler.net/", "org": "Project Euler", "domains": ["Mathematics", "Number Theory", "Combinatorics", "Dynamic Programming", "Algorithms"]},
    "Google Kick Start": {"link": "https://codingcompetitions.google.com/kickstart", "org": "Google", "domains": ["Algorithms", "Data Structures", "Dynamic Programming", "Graph Theory", "Number Theory"]},
    "Facebook Hacker Cup": {"link": "https://facebook.com/codingcompetitions/hacker-cup", "org": "Meta", "domains": ["Algorithms", "Data Structures", "Dynamic Programming", "Graph Theory", "Greedy"]},
    "Microsoft Imagine Cup": {"link": "https://imaginecup.microsoft.com/", "org": "Microsoft", "domains": ["AI/ML", "IoT", "Cloud", "Gaming", "Social Impact", "EdTech", "HealthTech", "GreenTech"]},
    "IBM Call for Code": {"link": "https://callforcode.org/", "org": "IBM", "domains": ["AI/ML", "Cloud", "IoT", "Blockchain", "GreenTech", "HealthTech", "Cybersecurity"]},
    "NASA Space Apps": {"link": "https://spaceapps.nasa.gov/", "org": "NASA", "domains": ["SpaceTech", "Data Science", "AR/VR", "IoT", "AI/ML", "Robotics"]},
    "AngelHack": {"link": "https://angelhack.com/", "org": "AngelHack", "domains": ["FinTech", "HealthTech", "EdTech", "Smart Cities", "AI/ML", "Cloud"]},
    "Hackster.io": {"link": "https://hackster.io/", "org": "Hackster.io", "domains": ["IoT", "Robotics", "Hardware", "AI/ML", "Edge Computing", "Computer Vision"]},
    "Hackaday": {"link": "https://hackaday.io/", "org": "Hackaday", "domains": ["Hardware", "Embedded Systems", "IoT", "Robotics", "Electronics", "Reverse Engineering"]},
    "Junction": {"link": "https://junctionapp.com/", "org": "Junction", "domains": ["FinTech", "HealthTech", "Smart Cities", "AI/ML", "EdTech", "GreenTech"]},
    "TechGig": {"link": "https://techgig.com/", "org": "TechGig", "domains": ["Algorithms", "Data Structures", "AI/ML", "Cloud", "Cybersecurity", "Database"]},
    "MachineHack": {"link": "https://machinehack.com/", "org": "MachineHack", "domains": ["AI/ML", "Data Science", "Computer Vision", "NLP", "Deep Learning", "Time Series"]},
    "Analytics Vidhya": {"link": "https://analyticsvidhya.com/", "org": "Analytics Vidhya", "domains": ["AI/ML", "Data Science", "Computer Vision", "NLP", "Deep Learning", "Generative AI"]},
    "DrivenData": {"link": "https://drivendata.org/", "org": "DrivenData", "domains": ["AI/ML", "Data Science", "Public Health", "Environment", "Climate", "Social Impact"]},
    "AIcrowd": {"link": "https://aicrowd.com/", "org": "AIcrowd", "domains": ["AI/ML", "Robotics", "Reinforcement Learning", "Computer Vision", "NLP", "Climate"]},
    "Tianchi": {"link": "https://tianchi.aliyun.com/", "org": "Alibaba Cloud", "domains": ["AI/ML", "Data Science", "Cloud", "Computer Vision", "NLP", "IoT"]},
    "NeurIPS Competition": {"link": "https://neurips.cc/", "org": "NeurIPS", "domains": ["AI/ML", "Deep Learning", "Reinforcement Learning", "Computer Vision", "NLP", "Generative AI"]},
    "RoboCup": {"link": "https://robocup.org/", "org": "RoboCup Federation", "domains": ["Robotics", "AI/ML", "Computer Vision", "Multi-agent Systems", "Control Systems"]},
    "FIRST Robotics": {"link": "https://firstinspires.org/", "org": "FIRST", "domains": ["Robotics", "Hardware", "Embedded Systems", "Control Systems", "Automation"]},
    "Arduino Project Hub": {"link": "https://create.arduino.cc/", "org": "Arduino", "domains": ["IoT", "Embedded Systems", "Hardware", "Robotics", "Sensors", "Automation"]},
    "Postman API Hackathon": {"link": "https://postman.com/api-hackathon", "org": "Postman", "domains": ["API", "Cloud", "Microservices", "Automation", "DevOps", "Integration"]},
    "PennApps": {"link": "https://pennapps.com/", "org": "University of Pennsylvania", "domains": ["AI/ML", "HealthTech", "EdTech", "FinTech", "Smart Cities", "Social Impact"]},
    "HackMIT": {"link": "https://hackmit.org/", "org": "MIT", "domains": ["AI/ML", "Cloud", "IoT", "HealthTech", "EdTech", "GreenTech", "Social Impact"]},
    "CalHacks": {"link": "https://calhacks.io/", "org": "UC Berkeley", "domains": ["AI/ML", "Blockchain", "FinTech", "HealthTech", "AR/VR", "Social Impact"]},
    "TreeHacks": {"link": "https://treehacks.com/", "org": "Stanford University", "domains": ["AI/ML", "Computer Vision", "NLP", "Robotics", "HealthTech", "GreenTech"]},
    "HackHarvard": {"link": "https://hackharvard.io/", "org": "Harvard University", "domains": ["AI/ML", "FinTech", "HealthTech", "EdTech", "Social Impact", "Sustainability"]},
    "HackPrinceton": {"link": "https://hackprincetion.com/", "org": "Princeton University", "domains": ["AI/ML", "Cloud", "IoT", "HealthTech", "GreenTech", "Cybersecurity"]},
    "GDSC": {"link": "https://developers.google.com/community/gdsc", "org": "Google Developer Student Clubs", "domains": ["AI/ML", "Cloud", "Android", "Web", "Cybersecurity", "IoT"]},
    "Coderbyte": {"link": "https://coderbyte.com/", "org": "Coderbyte", "domains": ["Algorithms", "Data Structures", "Database", "System Design", "Frontend", "Backend"]},
    "Skillenza": {"link": "https://skillenza.com/", "org": "Skillenza", "domains": ["AI/ML", "Cloud", "IoT", "Blockchain", "Cybersecurity", "EdTech"]},
}

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
]

years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]

def generate_title(platform_name, domain, topic):
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

def generate_description(platform_name, domain, topic, org):
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

total_platforms = len(platforms_config)
problems_per_platform = 1500
target = total_platforms * problems_per_platform

print(f"Generating {target} problems across {total_platforms} platforms ({problems_per_platform} each)...")

generated = []
idx = 0
for platform_name, config in platforms_config.items():
    org = config["org"]
    link = config["link"]
    domains = config["domains"]

    for _ in range(problems_per_platform):
        domain = random.choice(domains)
        topic = random.choice(topics)
        year = random.choice(years)
        difficulty = random.choice(["Beginner", "Intermediate", "Advanced"])
        is_open = random.choice([True, False])

        title = generate_title(platform_name, domain, topic)
        description = generate_description(platform_name, domain, topic, org)
        tags = generate_tags(topic, domain)

        problem = {
            "title": title,
            "description": description,
            "domain": domain,
            "organization": org,
            "category": "Software",
            "source_platform": platform_name,
            "source_year": year,
            "source_link": link,
            "tags": tags,
            "difficulty": difficulty,
            "is_open": is_open,
        }
        generated.append(problem)
        idx += 1

    print(f"  [{idx}/{target}] {platform_name} - {problems_per_platform} problems generated")

random.shuffle(generated)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(generated, f, indent=2, ensure_ascii=False)

print(f"\nDone! Total: {len(generated)} problems saved to more_platforms.json")
print(f"Platforms: {', '.join(platforms_config.keys())}")
