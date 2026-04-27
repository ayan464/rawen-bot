import discord
from discord.ext import commands
import requests
import os

# BOT AYARLARI
intents = discord.Intents.default()
intents.message_content = True  # Mesaj içeriğini okuma izni
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='.', intents=intents)

# ---------------------------------------------------------
# OCR API ANAHTARI
# ---------------------------------------------------------
OCR_API_KEY = 'K87635629488957' 

@bot.event
async def on_ready():
    print(f'RAWEN Bot {bot.user} olarak aktif ve hazır!')
    # Botun durumunu Discord'da güncelleyelim
    await bot.change_presence(activity=discord.Game(name="Resimleri Okuyorum..."))

@bot.event
async def on_message(message):
    # Bot kendi mesajına cevap vermesin
    if message.author == bot.user:
        return

    # TEST KOMUTU: Botun aktifliğini ölçmek için
    if message.content.lower() == ".test":
        await message.channel.send(f"Bot aktif! Mevcut kanal: **{message.channel.name}**")

    # Resim kontrolü
    if message.attachments:
        print(f"Resim algılandı! Kanal: {message.channel.name}")
        
        target_channel = "ss-metin-odası"
        current_channel = message.channel.name.strip()
        
        if current_channel == target_channel:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg']):
                    processing_msg = await message.channel.send("Resim algılandı, bulut üzerinden taranıyor... ☁️")
                    
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
                                await processing_msg.edit(content="✅ Tarama Tamamlandı!")
                                # Metni parçalara bölerek gönder (Discord 2000 karakter sınırı için)
                                await message.channel.send(f"**Okunan Metin:**\n
