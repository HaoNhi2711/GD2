import openai

openai.api_key = ""
def chat_with_chatgpt(prompt):# nhận chuỗi văn bảng từ người nhập gửi tới openai
    response = openai.ChatCompletion.create(  # gọi api từ openai với giá trị lưu ở response 
        model="gpt-3.5-turbo", #mô hình chat
        messages=[{"role": "user", "content": prompt}] # role và user vai trò người dùng và  prompt lấy nội dung của người nhập
    )
    return response.choices[0].message['content'].strip()  # content là nơi chứa nội dung do openai trả lời

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]: #lower không phân biệt chữ hoa hoặc chữ thường
            break # dừng kết thúc chương trình khi người dùng nhập các từ trong mảng

        response = chat_with_chatgpt(user_input) # gọi hàm chatgpt và lấy nội dung từ người nhập 
        print("ChatBox:", response) #in ra câu trả lời từ openai