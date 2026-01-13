import pandas as pd
import os
import glob

def check_file(file_path):
    print(f"\n--- Checking {file_path} ---")
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            print("Skipping: Unsupported file type")
            return

        print(f"Columns: {list(df.columns)}")
        if not df.empty:
            print(f"First row sample: {df.iloc[0].to_dict()}")
        else:
            print("File is empty.")
            
    except Exception as e:
        print(f"Error reading file: {e}")

def main():
    # Check specific known files
    known_files = ["data/leads.csv", "data/test_leads.csv"]
    for f in known_files:
        if os.path.exists(f):
            check_file(f)
        else:
            print(f"\nFile not found: {f}")

    # Check any other CSV/Excel in data/
    print("\n--- Scanning data/ folder for other files ---")
    for f in glob.glob("data/*.*"):
        if f.replace("\\", "/") not in known_files and f.endswith(('.csv', '.xlsx', '.xls')):
            check_file(f)

if __name__ == "__main__":
    main()
