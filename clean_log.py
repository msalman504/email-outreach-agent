import pandas as pd
import os

log_file = "output/sent_log.csv"
if os.path.exists(log_file):
    try:
        df = pd.read_csv(log_file)
        # Remove test emails
        test_emails = ['msalman2001400@gmail.com', 'msalmanpf@gmail.com', 'msalman_token_test@gmail.com']
        # Normalize to lower case for comparison
        df = df[~df['Email'].str.lower().isin([e.lower() for e in test_emails])]
        df.to_csv(log_file, index=False)
        print("Cleaned test emails from log.")
    except Exception as e:
        print(f"Error cleaning log: {e}")
