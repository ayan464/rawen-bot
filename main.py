import discord
from discord.ext import commands
import requests
import os

# BOT AYARLARI
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

# ---------------------------------------------------------
# OCR API ANAHTARI (Tırnak işaretleri içine alındı)
# ---------------------------------------------------------
OCR_API_KEY = 'K87635629488957' 

@bot.event
async def on_ready():
    print(f'RAWEN Bot {bot.user} olarak aktif ve hazır!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Sadece "ss-metin-odası" kanalındaki resimleri oku
    if message.channel.name == "ss-metin-odası" and message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg']):
                await message.channel.send("Resim bulut üzerinden taranıyor... ☁️")
                
                try:
                    # OCR Space API kullanımı
                    payload = {
                        'apikey': OCR_API_KEY,
                        'url': attachment.url,
                        'language': 'eng', 
                    }
                    r = requests.post('https://api.ocr.space/parse/image', data=payload)
                    result = r.json()
                    
                    if result.get('ParsedResults'):
                        detected_text = result['ParsedResults'][0]['ParsedText']
                        if detected_text.strip():
                            # Metni temizleyip Discord'a gönderir
                            await message.channel.send(f"**Okunan Metin:**\n
