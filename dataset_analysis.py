import pandas as pd

df = pd.read_csv("dataset/Phishing_Legitimate_full.csv")

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nTarget Distribution:")
print(df["CLASS_LABEL"].value_counts())