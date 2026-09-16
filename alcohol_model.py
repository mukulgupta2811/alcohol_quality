import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("alcohol_quality_dataset.csv")

# Features and target
X = df[
    [
        "Alcohol",
        "pH",
        "Citric_Acid",
        "Sulphates",
        "Volatile_Acidity",
        "Residual_Sugar"
    ]
]

y = df["Quality"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Scaling + Logistic Regression
model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)

# Evaluation
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:")
print(classification_report(y_test, predictions))

def predict_quality(
    alcohol,
    ph,
    citric_acid,
    sulphates,
    volatile_acidity,
    residual_sugar
):
    input_data = pd.DataFrame([{
        "Alcohol": alcohol,
        "pH": ph,
        "Citric_Acid": citric_acid,
        "Sulphates": sulphates,
        "Volatile_Acidity": volatile_acidity,
        "Residual_Sugar": residual_sugar
    }])

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]
    confidence = max(probabilities) * 100

    return prediction, round(confidence, 2)


if __name__ == "__main__":
    print("Model trained successfully!")
    print("Test Accuracy:", round(accuracy * 100, 2), "%")
