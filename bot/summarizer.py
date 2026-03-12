import anthropic
from .news_fetcher import NewsItem


def summarize_top_news(news_items: list[NewsItem]) -> str:
    client = anthropic.Anthropic()

    news_text = "\n\n".join([
        f"Título: {item.title}\nDescrição: {item.description}\nLink: {item.link}"
        for item in news_items
    ])

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Abaixo estão as principais notícias sobre IA do dia.
Identifique a notícia mais importante e relevante, e escreva um resumo em português brasileiro em bullet points.

Formato obrigatório da resposta:
📰 *[TÍTULO DA NOTÍCIA]*

• bullet point 1
• bullet point 2
• bullet point 3
• bullet point 4
• bullet point 5

🔗 [link da notícia]

Notícias do dia:
{news_text}"""
        }]
    )

    return response.content[0].text
