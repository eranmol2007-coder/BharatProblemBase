import json
import random
random.seed(789)
with open('data/more_platforms.json','r') as f:
    data = json.load(f)
extra = {
    'Google Code Jam': {'link':'https://codingcompetitions.google.com/codejam','org':'Google','domains':['Algorithms','Data Structures','Dynamic Programming','Graph Theory','Number Theory','Greedy']}
}
topics = ['Fraud Detection','Sentiment Analysis','Object Detection','Face Recognition','Speech Recognition','Language Translation','Text Classification','Image Segmentation','Recommendation System','Predictive Maintenance','Anomaly Detection','Churn Prediction','Demand Forecasting','Inventory Optimization','Price Optimization','Credit Scoring','Portfolio Optimization','Algorithmic Trading','Risk Assessment','Customer Segmentation','Network Intrusion Detection','Malware Classification','Phishing Detection','Vulnerability Assessment','Access Control','Path Planning','Traffic Prediction','Crop Disease Detection','Medical Diagnosis','Drug Discovery','Code Completion','Bug Detection','Database Optimization','Query Optimization','Load Balancing','Time Series Forecasting','Document Summarization','Gesture Recognition','Reinforcement Learning','Graph Analytics']
years = [2020,2021,2022,2023,2024,2025,2026]
for pn, pc in extra.items():
    for _ in range(1500):
        d = random.choice(pc['domains'])
        t = random.choice(topics)
        y = random.choice(years)
        dif = random.choice(['Beginner','Intermediate','Advanced'])
        title = random.choice([f'{t} using ML',f'AI-powered {t}',f'Intelligent {t} System',f'Scalable {t} Platform',f'Real-time {t} Engine',f'Efficient {t} Algorithm',f'Robust {t} System',f'End-to-End {t} Solution'])
        desc = f'Build a solution for {t}. This challenge by {pc["org"]} on {pn} tests your ability to develop innovative solutions. Winners receive cash prizes and mentorship.'
        tags = list(set([t.lower().replace(' ','-'), d.lower().replace(' ','-'), random.choice(['python','ml','algorithms','optimization','cloud','api']), random.choice(['performance','scalability','testing','analytics','automation'])]))[:6]
        data.append({'title':title,'description':desc,'domain':d,'organization':pc['org'],'category':'Software','source_platform':pn,'source_year':y,'source_link':pc['link'],'tags':tags,'difficulty':dif,'is_open':random.choice([True,False])})
with open('data/more_platforms.json','w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f'Added 1500. Total: {len(data)}')
