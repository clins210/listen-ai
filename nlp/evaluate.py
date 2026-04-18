import re
import time
import pickle
from datasets import load_dataset
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

# ── 舊演算法 ──────────────────────────────────────────
POSITIVE_WORDS = {"good","great","excellent","love","awesome","happy","amazing","nice","best","positive","fast","smooth","reliable"}
NEGATIVE_WORDS = {"bad","terrible","awful","hate","worst","slow","bug","bugs","issue","issues","angry","broken","negative","expensive"}
NEGATION_WORDS = {"not","never","no","hardly"}

def old_classify(text: str) -> str:
    tokens = re.findall(r"[a-zA-Z']+", text.lower())
    score = 0
    prev = ["", ""]
    for token in tokens:
        is_negated = any(p in NEGATION_WORDS for p in prev)
        if token in POSITIVE_WORDS:
            score += -1 if is_negated else 1
        elif token in NEGATIVE_WORDS:
            score += 1 if is_negated else -1
        prev = [prev[-1], token]
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"

# ── 載入資料集 ────────────────────────────────────────
print("載入資料集...")
dataset = load_dataset("stanfordnlp/sst2", split="train")
texts = [d["sentence"] for d in dataset]
labels = ["positive" if d["label"] == 1 else "negative" for d in dataset]

_, X_test, _, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# ── 評估舊演算法 ──────────────────────────────────────
print("\n【舊演算法：Lexicon-based】")
start = time.time()
old_preds = [old_classify(t) for t in X_test]
old_time = time.time() - start
print(f"Accuracy : {accuracy_score(y_test, old_preds):.4f}")
print(f"F1-score : {f1_score(y_test, old_preds, average='weighted', zero_division=0):.4f}")
print(f"推論時間 : {old_time:.4f}s ({len(X_test)} 筆)")

# ── 評估新演算法 ──────────────────────────────────────
print("\n【新演算法：TF-IDF + Logistic Regression】")
with open("model.pkl", "rb") as f:
    artifacts = pickle.load(f)
    vectorizer = artifacts["vectorizer"]
    model = artifacts["model"]

start = time.time()
X_test_vec = vectorizer.transform(X_test)
new_preds = model.predict(X_test_vec)
new_time = time.time() - start
print(f"Accuracy : {accuracy_score(y_test, new_preds):.4f}")
print(f"F1-score : {f1_score(y_test, new_preds, average='weighted', zero_division=0):.4f}")
print(f"推論時間 : {new_time:.4f}s ({len(X_test)} 筆)")