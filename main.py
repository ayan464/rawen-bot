import discord
from discord.ext import commands
import requests
import os

# BOT AYARLARI
# Intent'leri tam yetkiyle açıyoruz ki mesajları okuyabilsin
intents = discord.Intents.default()
intents.message_content = True
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
        target_channel = "ss-metin-odası"
        current_channel = message.channel.name.strip()
        
        if current_channel == target_channel:
            for attachment in message.attachments:
                # Sadece resim dosyalarını (png, jpg, jpeg) işle
                if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg']):
                    processing_msg = await message.channel.send("Resim algılandı, taranıyor... ☁️")
                    
                    try:
                        # OCR Space API kullanımı (Sunucuya tesseract kurmaya gerek bırakmaz)
                        payload = {
                            'apikey': OCR_API_KEY,
                            'url': attachment.url,
                            'language': 'eng', 
                            'isOverlayRequired': False,
                            'detectOrientation': True
                        }
                        
                        r = requests.post('https://api.ocr.space/parse/image', data=payload)
                        result = r.json()
                        
                        if result.get('ParsedResults'):
                            detected_text = result['ParsedResults'][0]['ParsedText']
                            if detected_text.strip():
                                await processing_msg.edit(content="✅ Tarama Tamamlandı!")
                                # Metni Discord'un 2000 karakter sınırına takılmaması için keserek gönderiyoruz
                                await message.channel.send(f"**Okunan Metin:**\n
