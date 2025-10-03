import os
import telebot
import cv2
import numpy as np

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Folder untuk menyimpan foto wajah
if not os.path.exists("faces"):
    os.makedirs("faces")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Halo! Kirimkan fotomu, nanti aku simpan dan bisa mengenali wajahmu 😊")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    img_path = f"faces/{message.from_user.id}.jpg"
    with open(img_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, f"Foto wajahmu sudah disimpan dengan nama {message.from_user.id}.jpg ✅")

@bot.message_handler(commands=['check'])
def check_face(message):
    user_id = message.from_user.id
    img_path = f"faces/{user_id}.jpg"
    if os.path.exists(img_path):
        bot.reply_to(message, "Aku sudah mengenali wajahmu 😎")
    else:
        bot.reply_to(message, "Kamu belum upload foto, kirim fotomu dulu!")

bot.infinity_polling()
