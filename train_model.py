import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
accuracy_score,
precision_score,
recall_score,
f1_score,
classification_report,
ConfusionMatrixDisplay
)

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.ensemble import (
RandomForestClassifier,
GradientBoostingClassifier,
AdaBoostClassifier,
ExtraTreesClassifier
)

from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
# =========================

# LOAD DATASET

# =========================

df = pd.read_csv("dataset/Phishing_Legitimate_full.csv")

X = df.drop(["CLASS_LABEL", "id"], axis=1)
y = df["CLASS_LABEL"]

# =========================

# TRAIN TEST SPLIT

# =========================

X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.20,
random_state=42
)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# =========================

# MODELS

# =========================

models = {


"Decision Tree":
    DecisionTreeClassifier(
        random_state=42
    ),

"Logistic Regression":
    LogisticRegression(
        max_iter=3000,
        solver="lbfgs"
    ),
"KNN":
    KNeighborsClassifier(
        n_neighbors=5
    ),

"SVM":
    SVC(),

"Random Forest":
    RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ),

"Gradient Boosting":
    GradientBoostingClassifier(
        random_state=42
    ),

"AdaBoost":
    AdaBoostClassifier(
        random_state=42
    ),

"Extra Trees":
    ExtraTreesClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ),

"XGBoost":
    XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss"
    )


}

# =========================

# TRAIN ALL MODELS

# =========================

results = {}

best_accuracy = 0
best_model = None
best_model_name = ""

print("\n========== MODEL COMPARISON ==========\n")

for name, model in models.items():

    print(f"\nTraining: {name}")

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    acc = accuracy_score(
        y_test,
        y_pred
    )

    results[name] = acc

    print(
        f"{name} Accuracy: {acc*100:.2f}%"
    )

    if acc > best_accuracy:

        best_accuracy = acc
        best_model = model
        best_model_name = name

# =========================

# SAVE BEST MODEL

# =========================

joblib.dump(
best_model,
"models/phishing_model.pkl"
)

print("\n==============================")
print("BEST MODEL :", best_model_name)
print("BEST ACCURACY :", round(best_accuracy*100,2), "%")
print("==============================")

# =========================

# FINAL REPORT

# =========================

y_pred = best_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\n========== FINAL REPORT ==========\n")

print(
classification_report(
y_test,
y_pred
)
)

# =========================

# SAVE METRICS

# =========================

with open("model_metrics.txt", "w") as f:

    f.write(f"Best Model: {best_model_name}\n")
    f.write(f"Accuracy: {accuracy*100:.2f}%\n")
    f.write(f"Precision: {precision*100:.2f}%\n")
    f.write(f"Recall: {recall*100:.2f}%\n")
    f.write(f"F1 Score: {f1*100:.2f}%\n\n")

    f.write("Model Comparison:\n")

    for model_name, score in results.items():

        f.write(
            f"{model_name}: {score*100:.2f}%\n"
    )


# =========================

# CONFUSION MATRIX

# =========================

ConfusionMatrixDisplay.from_predictions(
y_test,
y_pred
)

plt.title(
f"{best_model_name} Confusion Matrix"
)

plt.savefig(
"static/confusion_matrix.png",
bbox_inches="tight"
)

plt.close()

print("Confusion Matrix Saved!")

# =========================

# MODEL COMPARISON GRAPH

# =========================

plt.figure(figsize=(12,6))

names = list(results.keys())
scores = [v * 100 for v in results.values()]

plt.bar(names, scores)

plt.ylabel("Accuracy (%)")
plt.xlabel("Models")
plt.title("Machine Learning Model Comparison")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
"static/model_comparison.png",
bbox_inches="tight"
)

plt.close()

print("Model Comparison Graph Saved!")
print("Training Complete!")
