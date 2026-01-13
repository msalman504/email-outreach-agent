---
description: How to run the Email Outreach Agent
---

This workflow guides you through running the email outreach agent.

## 1. Dry Run (Recommended First)
Run a dry run to verify email generation without sending.

```bash
python -m src.main --dry-run
```

## 2. Run Campaign (Standard)
Run the agent using the main leads file (`data/leads.csv`). It will skip emails already in `output/sent_log.csv`.

```bash
// turbo
python -m src.main
```

## 3. Run Test Leads Only
Run the agent using only the test leads file.

```bash
python -m src.main --leads "none" --test-leads "data/test_leads.csv"
```

## 4. Force Send (Ignore Duplicates)
Force the agent to send emails even if they are in the sent log. **Use with caution.**

```bash
python -m src.main --force
```

## 5. Check Data Headers
Verify your CSV/Excel files are readable.

```bash
// turbo
python check_headers.py
```
