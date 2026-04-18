import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "./data/listenai.db"

platforms = ["twitter", "instagram", "facebook", "threads", "ptt"]
authors = [f"user_{i}" for i in range(1000)]
keywords = ["機器人", "AI", "科技", "手機", "遊戲", "音樂", "美食", "旅遊", "電影", "運動"]
templates = [
    "今天看到關於{}的新聞，真的很{}！",
    "{}真的越來越厲害了，大家覺得呢？",
    "分享一下我對{}的看法：非常{}",
    "最近{}的話題很熱，你們怎麼看？",
    "{}讓我覺得{}，推薦大家關注",
]
adjectives = ["有趣", "厲害", "驚人", "普通", "失望", "期待", "滿意", "好奇"]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("開始生成資料...")
batch_size = 10000
total = 1000000

for i in range(0, total, batch_size):
    rows = []
    for _ in range(batch_size):
        platform = random.choice(platforms)
        author = random.choice(authors)
        keyword = random.choice(keywords)
        template = random.choice(templates)
        adj = random.choice(adjectives)
        content = template.format(keyword, adj)
        days_ago = random.randint(0, 365)
        created_at = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows.append((platform, author, content, created_at))
    
    cursor.executemany(
        "INSERT INTO posts (platform, author, content, created_at) VALUES (?, ?, ?, ?)",
        rows
    )
    conn.commit()
    print(f"已插入 {i + batch_size:,} 筆")

conn.close()
print("完成！")