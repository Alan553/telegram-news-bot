from telethon import TelegramClient, events
import requests

api_id = 39780948
api_hash = "be29273ba2666a856a477c219b800b6f"

bot_token = "7804124206:AAEU7hm2GWzNnHlLGMNmGBrAh2nSbmbHvfQ"
chat_id = "511463852"

channels = [
    "@marketfeed",
    "@financialjuice"
]

client = TelegramClient("session", api_id, api_hash)

def send_alert(text):

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    requests.post(url, data=data)

def analyze_gold(news):

    news = news.lower()

    bullish_words = {
        "rate cut": 4,
        "dovish": 3,
        "recession": 3,
        "war": 4,
        "geopolitical": 3,
        "bank crisis": 4,
        "risk off": 3,
        "weak dollar": 3
    }

    bearish_words = {
        "rate hike": 4,
        "hawkish": 3,
        "strong dollar": 3,
        "inflation rising": 3,
        "bond yields rising": 2,
        "strong economy": 2,
        "risk on": 2
    }

    bull = 0
    bear = 0

    for word, score in bullish_words.items():
        if word in news:
            bull += score

    for word, score in bearish_words.items():
        if word in news:
            bear += score

    total = bull + bear

    if total == 0:
        return None, 0

    confidence = int((max(bull, bear) / total) * 100)

    if bull > bear:
        return "BUY", confidence

    if bear > bull:
        return "SELL", confidence

    return None, confidence

def generate_trade(signal):

    if signal == "BUY":

        entry = "Market Price"
        sl = "10 - 15 pips below"
        tp = "20 - 40 pips above"

    else:

        entry = "Market Price"
        sl = "10 - 15 pips above"
        tp = "20 - 40 pips below"

    return entry, sl, tp

@client.on(events.NewMessage(chats=channels))
async def handler(event):

    news = event.message.text

    signal, confidence = analyze_gold(news)

    if signal and confidence >= 60:

        entry, sl, tp = generate_trade(signal)

        message = f"""
⚡ AI NEWS GOLD SIGNAL

Signal : {signal} XAUUSD
Confidence : {confidence}%

Entry : {entry}
SL : {sl}
TP : {tp}

News :
{news}
"""

        send_alert(message)


client.start()
print("AI GOLD NEWS BOT RUNNING...")
client.run_until_disconnected()
