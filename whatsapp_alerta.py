import requests
import time
from datetime import datetime
from urllib.parse import quote

# ─── CONFIGURAÇÃO ───────────────────────────────────────────
SEU_NUMERO  = "+55SEU_NUMERO"   # ex: +5511999999999
SUA_APIKEY  = "SUA_APIKEY"      # chave recebida do CallMeBot
INTERVALO_H = 1                 # horas entre cada mensagem
# ────────────────────────────────────────────────────────────

def enviar_whatsapp(mensagem):
    url = (
        f"https://api.callmebot.com/whatsapp.php"
        f"?phone={SEU_NUMERO}"
        f"&text={quote(mensagem)}"
        f"&apikey={SUA_APIKEY}"
    )
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            print(f"[{agora()}] ✅ Mensagem enviada!")
        else:
            print(f"[{agora()}] ❌ Erro: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"[{agora()}] ❌ Falha na conexão: {e}")

def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def mensagem_do_momento():
    hora = datetime.now().hour
    if 5 <= hora < 12:
        periodo = "Bom dia"
    elif 12 <= hora < 18:
        periodo = "Boa tarde"
    else:
        periodo = "Boa noite"
    return f"{periodo}! Lembrete automático do seu Android - {agora()}"

if __name__ == "__main__":
    print(f"[{agora()}] 🚀 Script iniciado. Mensagem a cada {INTERVALO_H}h.")
    print("  Pressione Ctrl+C para parar.\n")

    while True:
        msg = mensagem_do_momento()
        print(f"[{agora()}] 📤 Enviando: {msg}")
        enviar_whatsapp(msg)
        print(f"[{agora()}] ⏳ Próximo envio em {INTERVALO_H}h...\n")
        time.sleep(INTERVALO_H * 3600)
