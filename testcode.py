import sqlite3
import pandas as pd
import requests

# Cấu hình API AI (thay thế bằng API key của bạn)
API_KEY = "your_openai_api_key"
GEMINI_API_URL = "https://gemini.googleapis.com/v1/your_endpoint"

# Hàm đọc dữ liệu từ CSV vào database
def load_csv_to_db(csv_file):
    conn = sqlite3.connect("y_hoc.db")
    cursor = conn.cursor()

    # Tạo bảng nếu chưa có
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT
        )
    """)

    # Đọc file CSV
    df = pd.read_csv(csv_file)

    # Thêm dữ liệu vào database
    for _, row in df.iterrows():
        cursor.execute("INSERT OR IGNORE INTO medical_data (question, answer) VALUES (?, ?)", (row["Bệnh"], row["Mô tả"]))

    conn.commit()
    conn.close()
    print("✅ Dữ liệu từ CSV đã được tải vào database!")

# Hàm truy vấn database
def query_database(question):
    conn = sqlite3.connect("y_hoc.db")
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM medical_data WHERE question = ?", (question,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Hàm gọi AI để lấy câu trả lời nếu database không có
def send_message_to_ai(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": f"Câu hỏi: {prompt}\nTrả lời:",
        "max_tokens": 150,
        "temperature": 0.7,
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("response", "Xin lỗi, tôi không có câu trả lời cho câu hỏi này.")
    else:
        return "Có lỗi xảy ra khi kết nối với AI."

# Hàm lưu câu trả lời mới vào database
def save_to_database(question, answer):
    conn = sqlite3.connect("y_hoc.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO medical_data (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

# Hàm chính
def main():
    # Load dữ liệu từ file CSV vào database
    load_csv_to_db("y_hoc_data.csv")

    print("🤖 Chatbot Y học sẵn sàng! Gõ 'exit' để thoát.")
    while True:
        question = input("Bạn: ").strip()
        if question.lower() == "exit":
            break
        
        # Kiểm tra trong database trước
        answer = query_database(question)
        if not answer:
            answer = send_message_to_ai(question)  # Gọi AI nếu không có dữ liệu
            save_to_database(question, answer)  # Lưu câu trả lời mới vào database
        
        print(f"Bot: {answer}")

# Chạy chương trình
if __name__ == "__main__":
    main()
