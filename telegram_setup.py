import urllib.request, json

TOKEN = "8763933342:AAE3Kwa4qw6UFQNsMyMo7Bv9NPYDgJmLenY"

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
r = urllib.request.urlopen(url)
data = json.loads(r.read().decode())

if not data["result"]:
    print("Nenhuma mensagem encontrada. Mande uma mensagem para @Cleonorbot no Telegram e rode novamente.")
else:
    for msg in data["result"]:
        chat = msg["message"]["chat"]
        print(f"✅ chat_id encontrado: {chat['id']}")
        print(f"   Nome: {chat.get('first_name', '')} {chat.get('last_name', '')}")
