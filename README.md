# Autonomous Email Outreach Agent

A fully autonomous AI agent that manages your entire email outreach campaigns. It reads your leads, understands your company's value, and craft hyper-personalized emails that get replies.

## 🧠 The "Secret Sauce"

This isn't just a script that swaps names. It uses a psychological framework designed to maximize conversions:

### 1. Hormozi's "Grand Slam Offer"
We don't just say "hello". The AI structures the pitch to highlight **High Value** and **Low Effort** for the prospect.
> *"We help [Industry] achieve [Result] without [Pain Point]."*

### 2. "Show Me You Know Me" (SMYKM)
The AI analyzes the lead's specific business challenges (from your data) and proves it understands their world before pitching.
-   **No Generic Spam**: Every email feels hand-written by a human.
-   **Instant Trust**: Validates the prospect's pain point immediately.

---

## 🔄 How It Works (Fully Autonomous)

Once you press "Run", the agent takes over:

1.  **Reads Your Profile**: It studies your `Company profile.pdf` to understand exactly what you sell.
2.  **Analyzes the Lead**: It looks at each lead in your list (e.g., "John from Tech Corp").
3.  **Crafts the Email**: It uses Google Gemini (AI) to write a unique 1-to-1 message combining your offer with their specific needs.
4.  **Attaches Proof**: It automatically attaches your PDF credentials.
5.  **Sends & Logs**: It sends the email via SMTP and records it in `sent_log.csv` so it **never** spams the same person twice.

**You sit back. The agent does the work.**

---

## 🚀 Complete Setup Guide

Follow these steps to get the agent running on your local machine.

### 1. Prerequisites
-   Python 3.8 or higher installed.
-   A generic Gmail/Outlook account or a Hostinger email (recommended).
-   API Keys for Google Gemini (Free tier works).

### 2. Install the Agent
```bash
# Clone the repository
git clone https://github.com/msalman504/email-outreach-agent.git

# Navigate into the folder
cd email-outreach-agent

# (Optional) Create a virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a file named `.env` in the root folder and add your specific details:
```ini
GOOGLE_API_KEY=your_gemini_key_here
# (Optional) Add backup keys if you have them:
GOOGLE_API_KEY_2=secondary_key

# SMTP Settings (Example: Hostinger)
EMAIL_ADDRESS=your_email@domain.com
EMAIL_PASSWORD=your_password
SMTP_SERVER=smtp.hostinger.com
SMTP_PORT=465
```

### 4. Prepare Your Data
-   **Leads**: Save your leads as `data/leads.csv`.
-   **Company Profile**: Save your PDF as `data/Company profile.pdf`.

---

## 🎮 Commands

| Action | Command |
| :--- | :--- |
| **Run Campaign** | `python -m src.main` |
| **Run Test Leads** | `python -m src.main --leads "none" --test-leads "data/test_leads.csv"` |
| **Dry Run** (Preview) | `python -m src.main --dry-run` |
| **Check Data** | `python check_headers.py` |

---

## ✨ Features Breakdown

-   **Auto-Failover**: If one AI key fails, it instantly switches to backup keys (or Groq) to keep sending.
-   **Smart Logging**: Maintains a persistent database of sent emails.
-   **Rate Limiting**: Sleeps between emails to act like a human.
-   **PDF Attachments**: Auto-detects and attaches your profile.

### 🔍 Full Observability (LangSmith)
This agent is integrated with **LangSmith** for enterprise-grade tracing.
-   **Trace Every Step**: See exactly what the AI "thought" before writing the email.
-   **Debug Latency**: Monitor how long each generation takes.
-   **Token Usage**: Track your API costs in real-time.
-   To enable, simply add your `LANGCHAIN_API_KEY` to the `.env` file.

