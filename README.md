# 📧 Customer Support Triage System

An automated pipeline to **classify, prioritize, and organize customer support emails**.  
The goal is to help support teams focus on the **most critical tickets first**, reduce response time, and provide agents with **ready-to-use response templates**.

---

## 📑 Table of Contents
1. [Problem Statement](#-problem-statement)  
2. [Solution](#-solution)  
3. [Features](#-features)  
4. [Tech Stack](#-tech-stack)  
5. [Dataset](#-dataset)  
6. [Project Structure](#-project-structure)  
7. [Setup](#-setup)  
8. [Usage](#-usage)  
9. [Outputs](#-outputs)  
10. [Visualization](#-visualization)  
11. [Future Improvements](#-future-improvements)  


---

## ❓ Problem Statement
Customer support teams often receive **hundreds of emails daily** — ranging from *billing errors* to *system outages*.  

Key challenges:
- Emails are **unstructured** and come in different formats.  
- Support staff must manually **read, understand, and categorize** every request.  
- Critical issues (like **downtime**) may get delayed if hidden in the inbox.  
- Customers expect **fast responses**, but manual triage wastes valuable time.  

---

## 💡 Solution
This project introduces an **automated triage system** that:
1. Reads raw support emails from a dataset (`inbox.csv`).  
2. Classifies them into **categories** (e.g., Login Issue, Billing Error, Outage, API Integration, etc.).  
3. Assigns **priority levels** (P1 Critical → P4 Low) using rule-based logic.  
4. Deduplicates repeated issues to reduce noise.  
5. Generates multiple **outputs** for agents and managers:  
   - CSVs for queues and summaries.  
   - Response templates for quick replies.  
   - A visualization chart for category distribution.  

This ensures that:
- **Critical tickets** (e.g., downtime, billing errors) are handled first.  
- **Repetitive issues** are grouped.  
- **Agents save time** with pre-written replies.  

---

## ✨ Features
- **Automated Classification** → Regex-based rules for categories.  
- **Priority Assignment** → Urgent keywords + category logic.  
- **Triage Queue** → Sorted by priority & recency.  
- **Latest Threads** → Shows the latest message per sender & category.  
- **Summary Reports** → Category-wise counts and priority breakdown.  
- **Visualization** → Bar chart for quick overview.  
- **Response Templates** → Pre-written, professional templates with placeholders.  

---

## 🛠 Tech Stack
- **Python 3.10+**  
- **pandas** → Data cleaning & processing  
- **matplotlib** → Visualization  
- **Regex (re)** → Rule-based classification  

---

## 📂 Dataset
The dataset (`inbox.csv`) contains support emails with the following fields:
- **sender** → Email address of customer  
- **subject** → Email subject line  
- **body** → Email body (free text)  
- **sent_date** → Timestamp  

---

## 📁 Project Structure
customer-support-triage/
├── data/
│   └── inbox.csv
├── src/
│   └── triage.py
├── outputs/
│   ├── all_messages_classified.csv
│   ├── triage_queue.csv
│   ├── latest_threads.csv
│   ├── summary_by_category.csv
│   ├── category_counts.png
│   └── response_templates.md
├── requirements.txt
└── README.md


---





## ⚙️ Setup
Clone this repository:
```bash
git clone https://github.com/<your-username>/customer-support-triage.git
cd customer-support-triage


Install dependencies:

pip install -r requirements.txt

▶️ Usage

Run the main script:

python src/triage.py


This will:

Read data/inbox.csv

Classify and prioritize messages

Generate outputs inside the outputs/ folder

📂 Outputs

all_messages_classified.csv → All emails with category & priority labels

triage_queue.csv → Sorted queue of tickets (by priority & recency)

latest_threads.csv → Latest ticket per sender & category

summary_by_category.csv → Count of tickets per category + priority breakdown

category_counts.png → Bar chart visualization

response_templates.md → Ready-to-use email replies

📊 Visualization

Example bar chart of email categories:

🚀 Future Improvements

Machine Learning: Replace regex rules with an NLP classifier (e.g., BERT).

Real-Time Integration: Connect directly to Gmail / Outlook APIs for live triage.

Dashboard: Build an interactive dashboard using Streamlit or Flask.

Multi-Language Support: Extend classification to non-English support emails.

Feedback Loop: Allow support agents to give feedback to improve classification.
