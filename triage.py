# src/triage.py

import pandas as pd
import re
import matplotlib.pyplot as plt
from textwrap import dedent
from pathlib import Path

# -----------------------------
# 1. Load dataset
# -----------------------------
data_path = Path("data/inbox.csv")
df = pd.read_csv(data_path)
df['sent_date'] = pd.to_datetime(df['sent_date'])

# -----------------------------
# 2. Classification helpers
# -----------------------------
def classify_category(subject, body):
    text = f"{subject} {body}".lower()
    rules = [
        ("Outage/Downtime", r"\bservers? (are )?down\b|downtime|system .*inaccessible|completely inaccessible"),
        ("Billing Error (Charged Twice)", r"billing error|charged twice"),
        ("Login/Access Issue", r"unable to log in|system access blocked|cannot reset my password|reset link doesn.?t work"),
        ("Account Verification", r"verif(y|ication)|verification email"),
        ("Pricing Information", r"pricing tiers|product pricing|pricing"),
        ("API/Integration", r"\bintegration\b|third-party apis|crm"),
        ("Refund/Chargeback", r"\brefund\b"),
    ]
    for cat, pattern in rules:
        if re.search(pattern, text):
            return cat
    return "Other"

def detect_urgency(subject, body, category):
    text = f"{subject} {body}".lower()
    urgent_kw = any(k in text for k in ["urgent", "immediate", "critical", "highly critical"])

    # Base priority by category
    if "Outage/Downtime" in category:
        base = 1
    elif "Billing Error" in category:
        base = 1
    elif "Login/Access Issue" in category:
        base = 2
    elif "Refund" in category:
        base = 2
    elif "Account Verification" in category or "API/Integration" in category:
        base = 3
    elif "Pricing" in category:
        base = 4
    else:
        base = 4

    # Bump priority if urgent keywords
    if urgent_kw and base > 1:
        base -= 1

    return base, urgent_kw

def normalize_body(text):
    t = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    return re.sub(r"\s+", " ", t)

# -----------------------------
# 3. Classify and prioritize
# -----------------------------
df["category"] = df.apply(lambda r: classify_category(r["subject"], r["body"]), axis=1)
df[["priority", "has_urgent_kw"]] = df.apply(
    lambda r: pd.Series(detect_urgency(r["subject"], r["body"], r["category"])),
    axis=1
)
priority_map = {1:"P1 - Critical", 2:"P2 - High", 3:"P3 - Medium", 4:"P4 - Low"}
df["priority_label"] = df["priority"].map(priority_map)
df["body_norm"] = df["body"].apply(normalize_body)

# Deduplicate exact same messages across senders
dupe_counts = df.groupby("body_norm")["sender"].nunique().reset_index(name="unique_senders_with_same_body")
df = df.merge(dupe_counts, on="body_norm", how="left")

# -----------------------------
# 4. Build outputs
# -----------------------------
# Triage queue: sorted by priority + most recent
triage = df.sort_values(by=["priority", "sent_date"], ascending=[True, False])

# Latest message per sender & category
latest_by_sender_cat = (
    df.sort_values("sent_date")
      .groupby(["sender","category"], as_index=False)
      .last()
      .sort_values(by=["priority","sent_date"], ascending=[True, False])
)

# Summary stats
summary = df.groupby("category").agg(
    total=("category","count"),
    p1=("priority", lambda s: (s==1).sum()),
    p2=("priority", lambda s: (s==2).sum()),
    p3=("priority", lambda s: (s==3).sum()),
    p4=("priority", lambda s: (s==4).sum()),
).reset_index().sort_values("total", ascending=False)

# -----------------------------
# 5. Save outputs
# -----------------------------
out_dir = Path("outputs")
out_dir.mkdir(exist_ok=True)

df.drop(columns=["body_norm"]).to_csv(out_dir / "all_messages_classified.csv", index=False)
triage.to_csv(out_dir / "triage_queue.csv", index=False)
latest_by_sender_cat.to_csv(out_dir / "latest_threads.csv", index=False)
summary.to_csv(out_dir / "summary_by_category.csv", index=False)

# Bar chart: counts by category
counts = df["category"].value_counts()
plt.figure(figsize=(8,4))
counts.plot(kind="bar")
plt.title("Message Count by Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(out_dir / "category_counts.png")
plt.close()

# -----------------------------
# 6. Templates
# -----------------------------
templates = {
"Outage/Downtime": dedent("""\
Subject: We're on it — investigating your outage now

Hi {name},

Thanks for flagging the outage. Our team is actively investigating.
Incident ID: {incident_id}.
We'll update you every {cadence} until resolved.

— {agent_name}
"""),
"Billing Error (Charged Twice)": dedent("""\
Subject: Billing correction in progress

Hi {name},

Sorry about the duplicate charge. I’ve opened a billing ticket {ticket_id}.
Refund will be processed within {sla} business days.

— {agent_name}
"""),
"Login/Access Issue": dedent("""\
Subject: Help with login/access

Hi {name},

Sorry you’re locked out. Use this reset link: {reset_link}.
If it fails, share the exact error and timestamp.

— {agent_name}
"""),
"Account Verification": dedent("""\
Subject: Verification assistance

Hi {name},

I’ve re-sent the verification email to {email}. 
If you don’t receive it in {ttl} minutes, let me know.

— {agent_name}
"""),
"Pricing Information": dedent("""\
Subject: Pricing tiers — detailed breakdown

Hi {name},

Here’s the breakdown of tiers and billing cadence. 
Would you like a 15-min walk-through?

— {agent_name}
"""),
"API/Integration": dedent("""\
Subject: CRM/API integrations

Hi {name},

Yes — we support REST and OAuth integrations. 
I’ve attached docs and a sample Postman collection.

— {agent_name}
"""),
"Refund/Chargeback": dedent("""\
Subject: Refund request — next steps

Hi {name},

I see your refund request from {request_date}. Ticket {ticket_id} is in progress.
Refunds complete within {sla} business days.

— {agent_name}
"""),
"Other": dedent("""\
Subject: Thanks for reaching out

Hi {name},

Thanks for contacting us. Could you share more detail so I can route this to the right specialist?

— {agent_name}
""")
}

with open(out_dir / "response_templates.md", "w", encoding="utf-8") as f:
    f.write("# Response Templates\n\n")
    for cat, txt in templates.items():
        f.write(f"## {cat}\n\n```\n{txt}\n```\n\n")

print("✅ Outputs generated in 'outputs/' folder")
