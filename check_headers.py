import pandas as pd
try:
    df = pd.read_excel("data/d360hubspot.xlsx")
    print("Columns:", list(df.columns))
    print("First row:", df.iloc[0].to_dict())
except Exception as e:
    print(e)
