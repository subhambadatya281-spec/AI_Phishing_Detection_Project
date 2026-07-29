import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("dataset/Phishing_Legitimate_full.csv")

X = df.drop(["CLASS_LABEL", "id"], axis=1)
y = df["CLASS_LABEL"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

with open("models/phishing_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model Saved Successfully")