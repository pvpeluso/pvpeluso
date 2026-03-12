from .news_fetcher import fetch_ai_news
from .summarizer import summarize_top_news
from .telegram_sender import send_telegram_message


def main():
    print("Buscando notícias de IA...")
    news = fetch_ai_news()
    print(f"{len(news)} notícias encontradas.")

    print("Gerando resumo com Claude...")
    summary = summarize_top_news(news)
    print(f"Resumo:\n{summary}\n")

    print("Enviando para o Telegram...")
    send_telegram_message(summary)
    print("Mensagem enviada com sucesso!")


if __name__ == "__main__":
    main()
