import telegram
from telegram.ext import Updater, CommandHandler

TOKEN = "8254455597:AAGoKJ74A5IlnHa31nVO_MWv-fM2x_Q-WfI"

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
