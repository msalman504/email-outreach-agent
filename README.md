# 🤖 Autonomous Email Outreach Agent

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

## 🚀 Setup Guide

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file with your keys:
```ini
GOOGLE_API_KEY=your_gemini_key
EMAIL_ADDRESS=your_email@domain.com
EMAIL_PASSWORD=your_password
SMTP_SERVER=smtp.hostinger.com
```

### 3. Your Data
-   **Leads**: Put your list in `data/leads.csv` (Columns: `Name`, `Email`, `Biggest challenge?`).
-   **Profile**: Put your details in `data/Company profile.pdf`.

---

## 🎮 Commands

| Action | Command |
| :--- | :--- |
| **Run Campaign** | `python -m src.main` |
| **Run Test Leads** | `python -m src.main --leads "none" --test-leads "data/test_leads.csv"` |
| **Dry Run** (Preview) | `python -m src.main --dry-run` |
| **Check Data** | `python check_headers.py` |

---

## ✨ Key Features

-   **Auto-Failover**: If one AI key fails, it instantly switches to backup keys (or Groq) to keep sending.
-   **Smart Logging**: Maintains a persistent database of sent emails.
-   **Rate Limiting**: Sleeps between emails to act like a human.
-   **PDF Attachments**: Auto-detects and attaches your profile.

