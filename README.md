# Intelligent Email Outreach Agent

A powerful, autonomous agent designed to generate and send high-conversion outreach emails using Google Gemini (AI) and Hostinger SMTP. 

## 🚀 Key Features

### 1. **"Hormozi x SMYKM" Content Framework**
The agent writes high-value emails using a specific psychological formula:
-   **The Hook ("Show Me You Know Me")**: Validates the lead's industry/pain point immediately (e.g., "I know that in the Real Estate sector...").
-   **The Offer (Hormozi Grand Slam)**: States a clear transformation (e.g., "We help [X] achieve [Y]...").
-   **The Proof**: Cites hard stats (**Bolded** for visibility).
-   **The Ask (Low Friction)**: "Would you be opposed to a 10-minute walk-through?"

### 2. **Bulletproof Reliability**
-   **Sticky API Logic**: The agent remembers which API Key (or provider) is currently working and keeps using it for subsequent leads. It does *not* waste time retrying failed keys.
-   **Multi-Provider Failover**: `Gemini Key 1 -> Key 2 -> Key 3 -> Groq (Llama 3.3) -> Sleep`.
-   **12-Hour Auto-Recharge**: If all providers fail, the agent sleeps for 12 hours and resumes automatically.
-   **Strict Validation**: Automatically rejects content with placeholders or errors.

### 3. **Full Observability (Tracing)**
-   **LangSmith Integration**: Every single AI generation call is traced.
-   **What is tracked?**: Input prompts, Output emails, Latency (speed), Token usage, and Errors.
-   **Dashboard**: View your agent's "thought process" in real-time on the LangSmith dashboard.
-   Emails are sent as **HTML**.
-   Markdown (like `**bold**`) is automatically converted to HTML (`<b>bold</b>`) for professional presentation in Gmail/Outlook.

### 4. **Observability**
-   Integrated with **LangSmith** to trace every AI step, latency, and token usage.

---

## 🛠️ Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Configuration**:
    Create a `.env` file with the following:
    ```ini
    # Google Gemini Keys (Rotate for higher limits)
    GOOGLE_API_KEY=AIzaSy...
    GOOGLE_API_KEY_2=AIzaSy...
    GOOGLE_API_KEY_3=AIzaSy...

    # Hostinger SMTP
    EMAIL_ADDRESS=info@d360...
    EMAIL_PASSWORD=...
    SMTP_SERVER=smtp.hostinger.com
    SMTP_PORT=465

    # LangSmith (Optional - for tracing)
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_API_KEY=lsv2_...
    ```

3.  **Data Preparation**:
    -   **Leads**: Place your CSV/Excel at `data/leads.csv`. Must have columns `Name` (or First Name), `Email`, and `Biggest challenge?`.
    -   **Profile**: Place company info at `data/profile.txt` or `.pdf`.

---

## 🖥️ Usage

### Run Full Campaign
```bash
python -m src.main
```
*   Reads `data/d360hubspot.xlsx` (default) or specified file.
*   Skips already sent leads.
*   Sleeps automatically if quotas hit.

### Run with Specific Leads File
```bash
python -m src.main --leads "data/test_leads.csv"
```

### Force Retry (Ignore Logs)
```bash
python -m src.main --leads "data/test_leads.csv" --force
```
*   **Warning**: This will re-send emails to people who already received them.

### Dry Run (No Sending)
```bash
python -m src.main --dry-run
```
*   Generates emails and prints them to console for review.

---

## 📂 Output

-   **`output/sent_log.csv`**: A real-time log of every email sent.
    -   Columns: Timestamp, Lead Name, Email, Subject, Status, Body.
    -   This file acts as the agent's memory to prevent duplicates.
