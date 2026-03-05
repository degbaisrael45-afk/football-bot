import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "8254455597:AAGoKJ74A5IlnHa31nVO_MWv-fM2x_Q-WfI"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "⚽ Football Bot PRO actif\n\n"
        "Commandes :\n"
        "/match equipe1 equipe2\n"
        "/analyse equipe1 equipe2"
    )

def match(update: Update, context: CallbackContext):
    try:
        team1 = context.args[0]
        team2 = context.args[1]

        message = (
            f"⚽ Match analysé\n\n"
            f"{team1} vs {team2}\n\n"
            "Pronostic IA :\n"
            "🔹 +2.5 buts probable\n"
            "🔹 Les deux équipes marquent\n"
            "🔹 Score probable : 2-1"
        )

        update.message.reply_text(message)

    except:
        update.message.reply_text("Utilise : /match equipe1 equipe2")

def analyse(update: Update, context: CallbackContext):
    try:
        team1 = context.args[0]
        team2 = context.args[1]

        message = (
            f"🤖 Analyse avancée\n\n"
            f"{team1} vs {team2}\n\n"
            "Risque FIFA truqué : 35%\n"
            "Match assez fiable\n"
            "Conseil : Over 2.5"
        )

        update.message.reply_text(message)

    except:
        update.message.reply_text("Utilise : /analyse equipe1 equipe2")

def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("match", match))
    dp.add_handler(CommandHandler("analyse", analyse))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
