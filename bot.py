import telegram
from telegram.ext import Updater, CommandHandler

TOKEN = "TON_TOKEN_TELEGRAM"

def start(update, context):
    update.message.reply_text("🤖 Bot Football PRO actif !")

def score(update, context):
    update.message.reply_text("⚽ Analyse des matchs FIFA en cours...")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("score", score))

updater.start_polling()
updater.idle()
