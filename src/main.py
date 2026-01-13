import os
import argparse
from dotenv import load_dotenv

# Load env immediately to ensure imports (like langsmith) check env
load_dotenv()

from src.data_loader import load_profile, load_leads
# configure_gemini, generate_email imported AFTER dotenv loads
# configure_gemini, generate_email imported AFTER dotenv loads
# from src.generator import configure_gemini, generate_email
from src.generator import ContentGenerator
from src.sender import HostingerSender, send_bulk_emails
import pandas as pd
import time
import random

import csv
from datetime import datetime

# ... (Logging function remains same) ...
def log_result(lead_name, email, subject, status, body=""):
    """Logs the email status to a CSV file."""
    log_file = "output/sent_log.csv"
    file_exists = os.path.exists(log_file)
    
    with open(log_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Lead Name", "Email", "Subject", "Status", "Body"])
        
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), lead_name, email, subject, status, body])

def main():
    load_dotenv()
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Argument parser
    parser = argparse.ArgumentParser(description="Email Outreach Agent")
    parser.add_argument("--profile", default="data/Company profile.pdf", help="Path to company profile")
    parser.add_argument("--leads", default="data/leads.csv", help="Primary leads file")
    parser.add_argument("--test-leads", default="data/test_leads.csv", help="Test leads file")
    parser.add_argument("--dry-run", action="store_true", help="Generate emails but do not send")
    parser.add_argument("--delay", type=int, default=5, help="Delay between emails in seconds")
    parser.add_argument("--limit", type=int, help="Limit number of leads to process")
    parser.add_argument("--force", action="store_true", help="Force send (ignore duplicate check)")
    args = parser.parse_args()

    # Check keys (Basic check)
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GROQ_API_KEY"):
        print("Error: No API Keys (GOOGLE_API_KEY or GROQ_API_KEY) found in env.")
        return

    # Initialize Generator (Loads keys and maintains state)
    generator = ContentGenerator()
    
    # Load Sent Emails to prevent duplicates
    sent_emails = set()
    if not args.force:
        log_file = "output/sent_log.csv"
        if os.path.exists(log_file):
            try:
                with open(log_file, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get("Status") == "Sent" and row.get("Email"):
                            sent_emails.add(row["Email"].strip().lower())
                print(f"Loaded {len(sent_emails)} already sent emails from log.")
            except Exception as e:
                print(f"Warning: Could not read log file: {e}")
    else:
        print("Force mode enabled: Ignoring duplicate checks.")

    # Load Data
    try:
        profile = load_profile(args.profile)
        
        # Load both leads files
        leads_main = pd.DataFrame()
        leads_test = pd.DataFrame()
        
        if os.path.exists(args.leads):
            leads_main = load_leads(args.leads)
            print(f"Loaded {len(leads_main)} leads from {args.leads}")
            
        if os.path.exists(args.test_leads):
            leads_test = load_leads(args.test_leads)
            print(f"Loaded {len(leads_test)} leads from {args.test_leads}")
            
        # Combine them
        leads = pd.concat([leads_main, leads_test], ignore_index=True)
        
        if leads.empty:
            print("No leads found in either file.")
            return

        if args.limit:
            leads = leads.head(args.limit)
            print(f"Limiting to first {args.limit} leads.")
            
        print(f"Total leads to process: {len(leads)}")
        print(f"Loaded profile length: {len(profile)} chars")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Initialize Sender (if not dry run)
    sender = None
    if not args.dry_run:
        try:
            sender = HostingerSender()
            print("Connected to Hostinger SMTP.")
        except Exception as e:
            print(f"Error connecting to SMTP: {e}")
            return

    # Process Leads
    print("Starting outreach...")
    for index, row in leads.iterrows():
        # Normalize keys for convenience
        n = row.get('Name')
        if pd.isna(n): n = row.get('First Name')
        lead_name = n if not pd.isna(n) else 'Unknown'
        
        e = row.get('Email')
        if pd.isna(e): e = row.get('email')
        lead_email_addr = e

        
        if not lead_email_addr:
            print(f"Skipping row {index}: No email found.")
            continue
            
        # Check if already sent
        if lead_email_addr.strip().lower() in sent_emails:
            print(f"[{index+1}/{len(leads)}] Skipping {lead_name} ({lead_email_addr}) - Already Sent.")
            continue
            
        print(f"[{index+1}/{len(leads)}] Processing {lead_name} ({lead_email_addr})...")
        
        # Generate content using the Persistent Generator
        email_body = generator.generate_email(profile, row)
        
        if not email_body:
            print("Skipping: Failed to generate email content (Likely quota or model error).")
            if not args.dry_run:
                log_result(lead_name, lead_email_addr, "N/A", "Failed (Generation Error)", body="")
            continue

        # Hardcoded subject for now, or extract from body if generator supports it
        # Simple heuristic: first line is subject if it starts with 'Subject:'
        lines = email_body.strip().split('\n')
        subject = "Partnership Opportunity" # Default
        body_content = email_body
        
        if lines[0].lower().startswith('subject:'):
            subject = lines[0].split(':', 1)[1].strip()
            body_content = '\n'.join(lines[1:]).strip()
        
        if args.dry_run:
            print(f"--- DRY RUN: Email to {lead_email_addr} ---\nSubject: {subject}\nBody:\n{body_content}\n[Attachment: {args.profile}]\n-----------------------------")
        else:
            # Attach the profile if it is a PDF
            attachment = args.profile if args.profile.lower().endswith('.pdf') else None
            
            if sender.send_email(lead_email_addr, subject, body_content, attachment_path=attachment):
                print(f"Sent to {lead_email_addr}")
                log_result(lead_name, lead_email_addr, subject, "Sent", body=body_content)
            else:
                print(f"Failed to send to {lead_email_addr}")
                log_result(lead_name, lead_email_addr, subject, "Failed (SMTP Error)", body=body_content)
            
            # User requested 20-30s gap
            sleep_time = random.uniform(20, 30)
            print(f"Sleeping for {sleep_time:.1f} seconds...")
            time.sleep(sleep_time)

    print("Outreach completed. Check output/sent_log.csv for details.")

if __name__ == "__main__":
    main()
