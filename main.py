from telethon import TelegramClient
import asyncio
import requests

# Ваши данные API Telegram
api_id = '4848484'  # Замените на ваш API ID
api_hash = 'ejejsjwjwjs'  # Замените на ваш API Hash
phone_number = 'YOUR_PHONE_NUMBER'  # Замените на ваш номер телефона

# Создаем клиент Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Функция для получения популярных токенов с CoinGecko
def get_popular_tokens(limit=10):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка при получении данных с CoinGecko: {e}")
        return []

# Функция для форматирования сообщения
def format_message(tokens):
    formatted_tokens = []
    for token in tokens:
        name = token['name']
        symbol = token['symbol'].upper()
        price = token['current_price']
        market_cap = token['market_cap']
        price_change_24h = token['price_change_percentage_24h']
        volume_24h = token['total_volume']

        emoji_up = "📈" if price_change_24h >= 0 else "📉"
        emoji_cap = "💰"
        emoji_vol = "💹"

        # Экранирование специальных символов Markdown
        name = name.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]')
        symbol = symbol.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]')

        # Форматирование токена
        formatted_tokens.append(
            f"✨ **Токен:** {name} ({symbol})\n"
            f"💵 **Цена:** ${price:,.2f} {emoji_up}\n"
            f"📊 **Изменение за 24ч:** {price_change_24h:+.2f}%\n"
            f"🏦 **Капитализация:** ${market_cap:,.0f} {emoji_cap}\n"
            f"📈 **Объем за 24ч:** ${volume_24h:,.0f} {emoji_vol}\n"
        )

    # Объединение всех токенов в одно сообщение
    message = "🔥 **Популярные токены сейчас:**\n\n" + "\n".join(formatted_tokens)
    message += "\n────────────────────\n🔗 [Подписывайтесь на наш канал](https://t.me/cryptocoins10sec)"
    return message

# Основная функция
async def main():
    await client.start(phone_number)
    print("Userbot started!")

    channel_username = 'cryptocoins10sec'  # Замените на username вашего канала

    # Отправляем начальное сообщение
    initial_message = "🔄 Загрузка данных о токенах..."
    sent_message = await client.send_message(channel_username, initial_message, parse_mode='markdown')
    message_id = sent_message.id
    print(f"Сообщение отправлено с ID: {message_id}")

    # Основной цикл
    while True:
        tokens = get_popular_tokens(limit=10)
        if tokens:
            try:
                # Форматируем и обновляем сообщение раз в 2 минуты
                new_message = format_message(tokens)
                await client.edit_message(channel_username, message_id, new_message, parse_mode='markdown')
                print("Сообщение успешно обновлено.")
            except Exception as e:
                print(f"Ошибка при обновлении сообщения: {e}")
        else:
            print("Не удалось получить данные о токенах.")

        await asyncio.sleep(120)  # Ожидание 2 минуты перед следующим обновлением

# Запуск юзербота
with client:
    client.loop.run_until_complete(main())
