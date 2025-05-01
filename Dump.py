import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt

# 1. Download data
ticker = "AAPL"
data = yf.download(ticker, start="2015-01-01", end="2022-12-31")

# 2. Feature Engineering
data["SMA_14"] = data["Close"].rolling(window=14).mean()
data["SMA_50"] = data["Close"].rolling(window=50).mean()
data["Returns"] = data["Close"].pct_change()
data["Close_Lag1"] = data["Close"].shift(1)
data["Volume_Lag1"] = data["Volume"].shift(1)

# 3. Create Direction Target
data["CloseTomorrow"] = data["Close"].shift(-1)
data["Direction"] = (data["CloseTomorrow"] > data["Close"])

# 4. Clean Data
data.dropna(inplace=True)

# 5. Prepare Features and Label
feature_cols = ["Close", "Volume", "SMA_14", "SMA_50", "Returns", "Close_Lag1", "Volume_Lag1"]
X = data[feature_cols]
y = data["Direction"]

# 6. Train/Test Split
split_date = '2021-01-01'
train = data.loc[:split_date]
test = data.loc[split_date:]

X_train = train[feature_cols]
y_train = train["Direction"]
X_test = test[feature_cols]
y_test = test["Direction"]

# 7. Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 8. Predict
predictions = model.predict(X_test)

# 9. Evaluate
# acc = accuracy_score(y_test, predictions)
cm = confusion_matrix(y_test, predictions)
cr = classification_report(y_test, predictions)

# print(f"Accuracy: {acc:.3f}")
print("Confusion Matrix:")
print(cm)
print("Classification Report:")
print(cr)

# (Optional) 10. Plot something like the distribution of predictions or cumulative returns, etc.
# For simplicity, just an example confusion matrix plot
import seaborn as sns

plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Down","Up"], yticklabels=["Down","Up"])
plt.title("Confusion Matrix")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.show()