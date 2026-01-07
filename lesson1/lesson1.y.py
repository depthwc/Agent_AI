import json
from google import genai
from dotenv import load_dotenv


load_dotenv(".env")
api=GENAI
HISTORY_FILE = "history.json"


def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []



def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)



client = genai.Client(api_key=api)


history = load_history()


chat = client.chats.create(
    model="gemini-2.5-flash",
    history=history
)

print("Chat loaded. Messages in history:", len(history))

while True:
    user_q = input("User: ")
    if user_q == ".exit":
        break


    response = chat.send_message(user_q)

    print("AI:", response.text)

 
    history.append({"role": "user", "content": user_q})
    history.append({"role": "model", "content": response.text})

    save_history(history)

save_history(history)
print("Conversation saved.")




#   print(f'role - {message.role}',end=": ")
#    print(message.parts[0].text)



#   print(f'role - {message.role}',end=": ")
#    print(message.parts[0].text)


#parts=[Part(text='hi')]
#role='user'
#parts=[Part(text='Hi there! How can I help you today?')] 
#role='model'
#parts=[Part(text='my name is depthwc')] 
#role='user'
#parts=[Part(text="It's nice to meet you, Depthwc! How can I help you today?")] 
#role='model'
