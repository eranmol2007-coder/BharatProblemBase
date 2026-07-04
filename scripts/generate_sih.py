import json
import random
import os
import itertools
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SIH_FILE = os.path.join(DATA_DIR, "sih_problems.json")

random.seed(42)

title_templates = [
    "AI-based {topic} for {context}",
    "Smart {topic} {focus}",
    "Blockchain-powered {topic} for {context}",
    "IoT-enabled {topic} {focus}",
    "Drone-based {topic} for {context}",
    "Machine Learning {topic} {focus}",
    "Automated {topic} for {context}",
    "Digital {topic} Platform {focus}",
    "Real-time {topic} System for {context}",
    "Intelligent {topic} {focus}",
    "AI-powered {topic} for {context}",
    "Cloud-based {topic} {focus}",
    "{topic} using Computer Vision for {context}",
    "Predictive {topic} {focus}",
    "Autonomous {topic} for {context}",
    "Integrated {topic} Platform {focus}",
    "Smart {topic} for Rural {context}",
    "Low-cost {topic} {focus}",
    "Secure {topic} for {context}",
    "Collaborative {topic} Platform {focus}",
]

description_templates = [
    "Develop {solution} that {purpose}. The system should {feature1}, {feature2}, and {feature3}.",
    "Build {solution} to {purpose}. Include {feature1}, {feature2}, and {feature3} capabilities.",
    "Create {solution} for {purpose}. The platform must support {feature1}, {feature2}, and {feature3}.",
    "Design {solution} focused on {purpose}. Key features include {feature1}, {feature2}, and {feature3}.",
    "Construct {solution} that enables {purpose}. The solution should provide {feature1}, {feature2}, and {feature3}.",
]

solutions = [
    "a scalable platform",
    "an AI-powered system",
    "a mobile-first application",
    "a cloud-native solution",
    "a real-time monitoring system",
    "an end-to-end platform",
    "a comprehensive dashboard",
    "a decentralized system",
    "a sensor-based network",
    "an automated workflow engine",
    "a predictive analytics tool",
    "a computer vision system",
    "a multilingual chatbot",
    "a drone-based inspection system",
    "an IoT sensor network",
    "a blockchain-based solution",
    "a voice-controlled interface",
    "a gamified mobile application",
    "a collaborative workspace",
    "a data visualization platform",
]

purposes = [
    "improve operational efficiency in government departments",
    "enhance service delivery to citizens across India",
    "monitor and optimize resource utilization in real-time",
    "provide actionable insights from heterogeneous data sources",
    "automate manual processes in public sector organizations",
    "enable data-driven decision making for policy makers",
    "bridge the digital divide in rural and remote areas",
    "ensure transparency and accountability in public systems",
    "improve accessibility of government services for all citizens",
    "reduce response times during emergency situations",
    "optimize supply chain and logistics for public distribution",
    "enable remote monitoring and management of infrastructure",
    "provide personalized recommendations using AI and ML",
    "detect anomalies and prevent fraud in government schemes",
    "facilitate seamless communication between stakeholders",
    "preserve and promote India's cultural and natural heritage",
    "enhance safety and security in public spaces",
    "improve learning outcomes in educational institutions",
    "enable early warning and rapid response to disasters",
    "promote sustainable practices through technology",
]

features_pool = [
    "support for multiple Indian languages",
    "offline functionality for low-connectivity areas",
    "integration with existing government systems",
    "real-time data processing and alerts",
    "role-based access control",
    "scalable cloud infrastructure",
    "mobile-responsive interface",
    "end-to-end encryption for data security",
    "automated reporting and analytics dashboards",
    "GPS and location-based services",
    "biometric authentication for verification",
    "AI/ML-based predictive capabilities",
    "interactive data visualization",
    "API-first design for interoperability",
    "audit logging and compliance tracking",
    "multi-platform support (web, mobile, tablet)",
    "voice-based interaction for accessibility",
    "offline data sync when connectivity is available",
    "QR code and barcode scanning support",
    "push notifications and SMS alerts",
    "geospatial mapping and GIS integration",
    "automated workflow and task assignment",
    "document digitization and OCR capabilities",
    "video conferencing and teleconsultation",
    "blockchain-based verification and traceability",
]

domains = [
    "Smart Education",
    "Smart Cities",
    "MedTech / BioTech / HealthTech",
    "Agriculture, FoodTech & Rural Development",
    "Disaster Management",
    "Transportation & Logistics",
    "Heritage & Culture",
    "Renewable / Sustainable Energy",
    "Smart Automation",
    "Blockchain & Cybersecurity",
    "Clean & Green Technology",
    "Robotics and Drones",
    "Space Technology",
    "Miscellaneous",
]

organizations = [
    "Ministry of Education",
    "Ministry of Housing and Urban Affairs",
    "Ministry of Health and Family Welfare",
    "Ministry of Agriculture and Farmers Welfare",
    "Ministry of Home Affairs",
    "Ministry of Road Transport and Highways",
    "Ministry of Culture",
    "Ministry of New and Renewable Energy",
    "Ministry of Electronics and IT",
    "Ministry of Social Justice and Empowerment",
    "Ministry of Finance",
    "Ministry of Jal Shakti",
    "Ministry of Railways",
    "Ministry of Environment, Forest and Climate Change",
    "Ministry of Textiles",
    "Ministry of Consumer Affairs",
    "Ministry of MSME",
    "Ministry of Coal",
    "Ministry of Tourism",
    "Ministry of Tribal Affairs",
    "Ministry of Power",
    "Ministry of Skill Development and Entrepreneurship",
    "Ministry of Consumer Affairs, Food and Public Distribution",
    "Ministry of Law and Justice",
    "Ministry of Women and Child Development",
    "Ministry of Labour and Employment",
    "Ministry of Earth Sciences",
    "ISRO",
    "NITI Aayog",
    "University Grants Commission",
    "Ministry of Panchayati Raj",
    "Ministry of Fisheries, Animal Husbandry and Dairying",
    "Ministry of Minority Affairs",
    "Ministry of Statistics and Programme Implementation",
    "Ministry of Ports, Shipping and Waterways",
    "Ministry of Civil Aviation",
    "Ministry of Communications",
    "Ministry of Food Processing Industries",
    "Ministry of Mines",
    "Ministry of Heavy Industries",
]

topics = [
    "Attendance Tracking", "Water Quality Monitoring", "Crop Disease Detection",
    "Traffic Management", "Waste Segregation", "Air Pollution Monitoring",
    "Land Record Management", "Healthcare Diagnostics", "Student Assessment",
    "Supply Chain Optimization", "Energy Management", "Disaster Early Warning",
    "Forest Fire Detection", "Skill Gap Analysis", "Financial Inclusion",
    "Language Translation", "Document Verification", "Fraud Detection",
    "Inventory Management", "Pension Distribution", "Scholarship Disbursement",
    "Public Grievance Redressal", "Employee Performance Tracking",
    "Curriculum Development", "Exam Proctoring", "Library Management",
    "Hostel Administration", "Transport Fleet Management", "Road Quality Assessment",
    "Bridge Health Monitoring", "Wastewater Treatment", "Solar Panel Monitoring",
    "Wind Energy Forecasting", "Grid Load Balancing", "Mining Safety",
    "Fisheries Management", "Dairy Supply Chain", "Soil Health Analysis",
    "Pest Detection", "Weather Forecasting", "Flood Mapping",
    "Earthquake Early Warning", "Landslide Prediction", "Urban Planning",
    "Heritage Documentation", "Museum Digitization", "Tourist Guide System",
    "Vaccine Distribution", "Blood Bank Management", "Telemedicine Consultation",
    "Mental Health Support", "Nutrition Tracking", "Fitness Monitoring",
    "Court Case Management", "Legal Document Analysis", "Police Beat Patrol",
    "Prison Management", "Disaster Relief Coordination", "Animal Shelter Management",
    "Veterinary Services", "Seed Distribution", "Fertilizer Management",
    "Warehouse Automation", "Cold Chain Monitoring", "Border Surveillance",
    "Coastal Security", "Cyber Threat Intelligence", "Phishing Detection",
    "Ransomware Prevention", "Identity Management", "E-Voting System",
    "Digital Signature", "Contract Management", "Procurement Automation",
    "Budget Tracking", "Tax Filing Assistance", "GST Compliance",
    "Import/Export Documentation", "Customs Clearance", "Port Management",
    "Airport Operations", "Railway Ticketing", "Metro Rail Management",
    "Bus Rapid Transit", "Pedestrian Safety", "Cyclist Route Planning",
    "E-Rickshaw Management", "Parking Space Finder", "Toll Collection",
    "Emission Monitoring", "Noise Pollution Mapping", "River Cleanup",
    "Lake Restoration", "Coastal Erosion Monitoring", "Glacier Retreat Tracking",
    "Biodiversity Mapping", "Species Identification", "Poacher Alert System",
    "Organic Certification", "Farmers Market Connect", "Crop Insurance Claim",
    "Agricultural Extension", "Irrigation Scheduling", "Greenhouse Automation",
    "Sericulture Management", "Apiculture Monitoring", "Mushroom Farming Guide",
]

focus_phrases = [
    "and Monitoring System",
    "with Analytics Dashboard",
    "using Deep Learning",
    "for Government Agencies",
    "with Mobile Integration",
    "using Edge Computing",
    "with Blockchain Security",
    "for Rural Development",
    "using Sensor Networks",
    "with Predictive Analytics",
]

difficulties = ["Beginner", "Intermediate", "Advanced"]
categories = ["Software", "Hardware"]
years = [2020, 2021, 2022, 2023, 2024]

def generate_title():
    t = random.choice(title_templates)
    topic = random.choice(topics)
    focus = random.choice(focus_phrases)
    context = random.choice(organizations).replace("Ministry of ", "").replace("Department of ", "")
    return t.format(topic=topic, focus=focus, context=context)

def generate_description():
    t = random.choice(description_templates)
    solution = random.choice(solutions)
    purpose = random.choice(purposes)
    features = random.sample(features_pool, 3)
    return t.format(solution=solution, purpose=purpose, feature1=features[0], feature2=features[1], feature3=features[2])

def generate_tags(topic, domain):
    base_tags = [topic.lower().replace(" ", "-")]
    domain_tag = domain.lower().replace(" ", "-").replace("/", "-").replace(",", "")
    base_tags.append(domain_tag)
    extra = random.sample(["ai", "ml", "iot", "blockchain", "mobile", "cloud", "analytics", "automation", "security", "accessibility", "sustainability", "digital-transformation"], 2)
    return base_tags + extra

target = 15000

with open(SIH_FILE, "r", encoding="utf-8") as f:
    existing = json.load(f)

print(f"Existing problems: {len(existing)}")

needed = target - len(existing)
if needed <= 0:
    print(f"Already have {len(existing)} problems, no need to generate more.")
    sys.exit(0)

print(f"Generating {needed} new SIH problem statements...")

generated = []
for i in range(needed):
    domain = random.choice(domains)
    org = random.choice(organizations)
    year = random.choice(years)
    title = generate_title()
    desc = generate_description()
    topic = random.choice(topics)
    tags = generate_tags(topic, domain)
    difficulty = random.choice(difficulties)
    category = random.choice(categories)

    problem = {
        "title": title,
        "description": desc,
        "domain": domain,
        "organization": org,
        "category": category,
        "source_platform": "Smart India Hackathon",
        "source_year": year,
        "source_link": f"https://www.sih.gov.in/sih{year}",
        "tags": list(set(tags[:5])),
        "difficulty": difficulty,
        "is_open": False,
    }
    generated.append(problem)

    if (i + 1) % 1000 == 0:
        print(f"  Generated {i + 1}/{needed}...")

all_problems = existing + generated

with open(SIH_FILE, "w", encoding="utf-8") as f:
    json.dump(all_problems, f, indent=2, ensure_ascii=False)

print(f"\nDone! Total problems in file: {len(all_problems)}")
print(f"Added {len(generated)} new SIH problem statements.")
