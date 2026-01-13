# 📧 Intelligent Email Outreach Agent

A smart tool that writes and sends personalized outreach emails using AI. It reads your company profile and leads list, then generates unique emails for each prospect.

## ✨ Features

-   **Smart Writing**: Uses AI (Gemini) to write emails based on your company profile and the lead's challenges.
-   **Reliable Sending**: Uses Hostinger SMTP to send emails efficiently.
-   **No Duplicates**: Automatically remembers who you've emailed (logs in `output/sent_log.csv`) so you don't spam.
-   **Attachments**: Automatically attaches your `Company profile.pdf` to every email.
-   **Multi-Source**: Can load leads from `leads.csv` and `test_leads.csv` simultaneously.

---

## 🚀 How to Run

### 1. Setup
Make sure you have your `.env` file set up with your API keys and SMTP details.
Place your leads in `data/leads.csv` and your profile in `data/Company profile.pdf`.

### 2. Available Workflows
We have built-in workflows to make running the agent easy. You can run these commands in your terminal:

*   **Dry Run** (Check what emails will look like without sending):
    ```bash
    python -m src.main --dry-run
    ```

*   **Run Campaign** (Send to all new leads):
    ```bash
    python -m src.main
    ```

*   **Test Leads Only** (Send only to test leads):
    ```bash
    python -m src.main --leads "none" --test-leads "data/test_leads.csv"
    ```

*   **Force Send** (Re-send to everyone, ignoring duplicates):
    ```bash
    python -m src.main --force
    ```

### 3. Check Your Data
If you're having trouble with your CSV files, run this checker:
```bash
python check_headers.py
```

---

## 📂 Files & Folders

-   `data/`: Put your `leads.csv` and `Company profile.pdf` here.
-   `output/`: Check `sent_log.csv` here to see who has been emailed.
-   `src/`: The source code for the agent.

