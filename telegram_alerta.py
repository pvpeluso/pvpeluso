import urllib.request, urllib.parse, json, time
from datetime import datetime

# ─── CONFIGURAÇÃO ───────────────────────────
TOKEN   = "8763933342:AAE3Kwa4qw6UFQNsMyMo7Bv9NPYDgJmLenY"
CHAT_ID = "SEU_CHAT_ID"   # rode telegram_setup.py para obter
INTERVALO_H = 1            # horas entre mensagens
# ────────────────────────────────────────────

def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def mensagem():
    hora = datetime.now().hour
    if 5 <= hora < 12:
        periodo = "Bom dia"
    elif 12 <= hora < 18:
        periodo = "Boa tarde"
    else:
        periodo = "Boa noite"
    return f"{periodo}! Lembrete do seu Android 🤖\n🕐 {agora()}"

def enviar(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    dados = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": texto
    }).encode()
    try:
        r = urllib.request.urlopen(url, dados, timeout=10)
        resp = json.loads(r.read().decode())
        if resp.get("ok"):
            print(f"[{agora()}] ✅ Mensagem enviada!")
        else:
            print(f"[{agora()}] ❌ Erro: {resp}")
    except Exception as e:
        print(f"[{agora()}] ❌ Falha: {e}")

if __name__ == "__main__":
    if CHAT_ID == "SEU_CHAT_ID":
        print("⚠️  Configure o CHAT_ID primeiro! Rode: python telegram_setup.py")
        exit(1)

    print(f"[{agora()}] 🚀 Bot iniciado. Mensagem a cada {INTERVALO_H}h.")
    print("  Pressione Ctrl+C para parar.\n")

    while True:
        msg = mensagem()
        print(f"[{agora()}] 📤 Enviando mensagem...")
        enviar(msg)
        print(f"[{agora()}] ⏳ Próximo envio em {INTERVALO_H}h.\n")
        time.sleep(INTERVALO_H * 3600)
