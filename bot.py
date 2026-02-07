import os
from dotenv import load_dotenv
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    bot_reply = completion.choices[0].message.content
    await update.message.reply_text(bot_reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("🚀 GROQ BOT STARTED")
app.run_polling()
