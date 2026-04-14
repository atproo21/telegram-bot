import telebot
from telebot import types

import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 5470824284

bot = telebot.TeleBot(TOKEN)

user_data = {}
users = set()

# START
@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.chat.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛍 Shop bot", "📚 Kurs bot")
    markup.add("🧾 Biznes bot", "✍️ Boshqa")

    bot.send_message(message.chat.id,
    "🤖 Assalomu alaykum!\n\nQanday bot kerakligini tanlang 👇",
    reply_markup=markup)

# BOT TYPE TANLASH
@bot.message_handler(func=lambda m: m.text in ["🛍 Shop bot", "📚 Kurs bot", "🧾 Biznes bot", "✍️ Boshqa"])
def choose_type(message):
    user_data[message.chat.id] = {"type": message.text}

    bot.send_message(message.chat.id, "📋 Biznesingizni qisqacha yozing:")
    bot.register_next_step_handler(message, ask_count)

# SONI
def ask_count(message):
    user_data[message.chat.id]["info"] = message.text

    bot.send_message(message.chat.id, "📊 Nechta mahsulot yoki xizmat bor?")
    bot.register_next_step_handler(message, ask_price)

# NARX
def ask_price(message):
    user_data[message.chat.id]["count"] = message.text

    bot.send_message(message.chat.id, "💰 Narx ko‘rsatilsinmi? (ha/yo‘q)")
    bot.register_next_step_handler(message, ask_delivery)

# DELIVERY
def ask_delivery(message):
    user_data[message.chat.id]["price"] = message.text

    bot.send_message(message.chat.id, "🚚 Yetkazib berish bormi?")
    bot.register_next_step_handler(message, ask_payment)

# PAYMENT
def ask_payment(message):
    user_data[message.chat.id]["delivery"] = message.text

    bot.send_message(message.chat.id, "💳 To‘lov turi qanday?")
    bot.register_next_step_handler(message, ask_contact)

# CONTACT (BUTTON)
def ask_contact(message):
    user_data[message.chat.id]["payment"] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📞 Raqam yuborish", request_contact=True)
    markup.add(btn)

    bot.send_message(message.chat.id, "Telefon raqamingizni yuboring:", reply_markup=markup)

# TELEFONNI OLISH
@bot.message_handler(content_types=['contact'])
def finish(message):
    user_data[message.chat.id]["phone"] = message.contact.phone_number

    data = user_data[message.chat.id]

    username = message.from_user.username or "yo‘q"
    user_id = message.chat.id

    text = f"""
🆕 YANGI KLIENT!

📌 Bot turi: {data['type']}
📋 Biznes: {data['info']}
📊 Soni: {data['count']}
💰 Narx: {data['price']}
🚚 Delivery: {data['delivery']}
💳 To‘lov: {data['payment']}
📞 Tel: {data['phone']}

👤 Username: @{username}
🆔 ID: {user_id}
"""

    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ So‘rovingiz qabul qilindi! Tez orada yozamiz.")

# ADMIN REPLY
@bot.message_handler(commands=['reply'])
def reply_user(message):
    if message.chat.id != ADMIN_ID:
        return

    try:
        parts = message.text.split(" ", 2)
        user_id = int(parts[1])
        text = parts[2]

        bot.send_message(user_id, f"📩 Admin:\n{text}")
        bot.send_message(message.chat.id, "Yuborildi ✅")
    except:
        bot.send_message(message.chat.id, "Format: /reply user_id text")

# STATISTIKA
@bot.message_handler(commands=['stats'])
def stats(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"👥 Foydalanuvchilar: {len(users)} ta")

# CANCEL
@bot.message_handler(commands=['cancel'])
def cancel(message):
    user_data.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "❌ Bekor qilindi")

bot.polling()
