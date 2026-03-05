import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = os.getenv("BOT_TOKEN")


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🤖 FOOTBALL BOT PRO ACTIF\n\n"
        "Commandes disponibles :\n"
        "/match equipe1 equipe2\n"
        "/analyse equipe1 equipe2\n"
        "/score equipe1 equipe2"
    )


def match(update: Update, context: CallbackContext):
    try:
        team1 = context.args[0]
        team2 = context.args[1]

        message = (
            f"⚽ Analyse du match\n\n"
            f"{team1} vs {team2}\n\n"
            "📊 Pronostic IA :\n"
            "• +2.5 buts probable\n"
            "• Les deux équipes marquent\n"
            "• Match offensif\n"
            "• Fiabilité : 78%"
        )

        update.message.reply_text(message)

    except:
        update.message.reply_text("Utilisation : /match equipe1 equipe2")


def analyse(update: Update, context: CallbackContext):
    try:
        team1 = context.args[0]
        team2 = context.args[1]

        message = (
            f"🤖 Analyse avancée\n\n"
            f"{team1} vs {team2}\n\n"
            "📊 Statistiques IA\n"
            "• Possession équilibrée\n"
            "• Attaque active\n"
            "• Défense moyenne\n\n"
            "⚠️ Risque FIFA truqué : 32%\n"
            "✅ Match assez fiable"
        )

        update.message.reply_text(message)

    except:
        update.message.reply_text("Utilisation : /analyse equipe1 equipe2")


def score(update: Update, context: CallbackContext):
    try:
        team1 = context.args[0]
        team2 = context.args[1]

        message = (
            f"⚽ Score probable\n\n"
            f"{team1} vs {team2}\n\n"
            "🔮 Prédiction IA\n"
            "Score probable : 2-1\n"
            "Alternative : 1-1\n"
            "Over 2.5 : Oui"
        )

        update.message.reply_text(message)

    except:
        update.message.reply_text("Utilisation : /score equipe1 equipe2")


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("match", match))
    dp.add_handler(CommandHandler("analyse", analyse))
    dp.add_handler(CommandHandler("score", score))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
