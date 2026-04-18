import pickle
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

# 下載資料集（只取一小部分）
print("下載資料集...")
# 改這段
dataset = load_dataset("stanfordnlp/sst2", split="train")

texts = [d["sentence"] for d in dataset]
labels = ["positive" if d["label"] == 1 else "negative" for d in dataset]

# 切分訓練/測試集
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

# 訓練
print("訓練中...")
vectorizer = TfidfVectorizer(max_features=10000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# 評估
y_pred = model.predict(X_test_vec)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"F1-score: {f1_score(y_test, y_pred, average='weighted'):.4f}")

# 存檔
with open("model.pkl", "wb") as f:
    pickle.dump({"vectorizer": vectorizer, "model": model}, f)

print("模型已存成 model.pkl")