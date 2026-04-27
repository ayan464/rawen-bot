import discord
from discord.ext import commands
import easyocr
import io
import os

# Bot Ayarları
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

# Resim Okuyucu (OCR) Hazırlığı - Render için CPU modu
reader = easyocr.Reader(['en'], gpu=False)

# Puan Tablosu (Senin istediğin sistem)
puan_sistemi = {1: 15, 2: 12, 3: 10, 4: 8, 5: 6, 6: 5, 7: 4, 8: 3, 9: 2, 10: 1, 11: 1, 12: 1}

@bot.event
async def on_ready():
    print(f'RAWEN Bot {bot.user} olarak aktif!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Sadece "ss-metin-odası" kanalındaki resimleri oku
    if message.channel.name == "ss-metin-odası" and message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg']):
                await message.channel.send("Resim işleniyor, lütfen bekleyin... ⏳")
                
                try:
                    image_bytes = await attachment.read()
                    results = reader.readtext(image_bytes)
                    
                    # Şimdilik okuduğu metinleri gösterir, yarın burayı puanla birleştiririz
                    detected_text = " ".join([res[1] for res in results])
                    await message.channel.send(f"Okunan Metin: {detected_text[:500]}...")
                    await message.channel.send("Sonuçlar doğru mu? Onaylıyorsanız ✅ emojisi bırakın.")
                except Exception as e:
                    await message.channel.send(f"Hata oluştu: {e}")

    await bot.process_commands(message)

# Tokeni Render üzerinden güvenli alacağız
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
