import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

def analyse_match(home, away, home_odds, draw_odds, away_odds, btts_odds, over25_odds):

    home_odds = float(home_odds)
    draw_odds = float(draw_odds)
    away_odds = float(away_odds)
    btts_odds = float(btts_odds)
    over25_odds = float(over25_odds)

    suspicion = 0

    if over25_odds < 1.70:
        suspicion += 40

    if btts_odds < 1.70:
        suspicion += 40

    if abs(home_odds - away_odds) < 0.50:
        suspicion += 20

    if suspicion >= 70:
        statut = "⚠️ MATCH POSSIBLEMENT SIMULÉ (TYPE FIFA)"
    else:
        statut = "Match probablement normal"

    # Probabilité victoire basée sur les cotes
    prob_home = round((1/home_odds)*100, 1)
    prob_away = round((1/away_odds)*100, 1)

    # Scores probables
    scores = ["1-1","2-1","2-2","3-2","3-1","3-3","4-2"]
    score_exact = random.choice(scores)

    # Analyse BTTS
    if btts_odds < 1.80:
        btts_result = "BTTS : OUI probable"
    else:
        btts_result = "BTTS : NON possible"

    # Analyse Over
    if over25_odds < 1.80:
        over_result = "Plus de 2.5 buts probable"
    else:
        over_result = "Moins de 2.5 buts possible"

    resultat = f"""
⚽ ANALYSE IA DU MATCH

Match : {home} vs {away}

{statut}

📊 Probabilité victoire
{home} : {prob_home}%
{away} : {prob_away}%

{btts_result}
{over_result}

🎯 Score probable : {score_exact}
"""

    return resultat


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🤖 BOT PRONOSTIC FOOTBALL IA\n\n"
        "Envoie les informations du match comme ceci :\n\n"
        "Equipe1 Equipe2\n"
        "Cote victoire equipe1\n"
        "Cote match nul\n"
        "Cote victoire equipe2\n"
        "Cote BTTS\n"
        "Cote Over2.5\n\n"
        "Exemple :\n"
        "Arsenal Chelsea\n"
        "1.90\n"
        "3.40\n"
        "3.80\n"
        "1.65\n"
        "1.70"
    )

    await update.message.reply_text(message)


async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        data = update.message.text.split("\n")

        equipes = data[0].split()

        home = equipes[0]
        away = equipes[1]

        home_odds = data[1]
        draw_odds = data[2]
        away_odds = data[3]
        btts_odds = data[4]
        over25_odds = data[5]

        resultat = analyse_match(home, away, home_odds, draw_odds, away_odds, btts_odds, over25_odds)

        await update.message.reply_text(resultat)

    except:
        await update.message.reply_text("❌ Format incorrect. Tape /start pour voir le format.")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyse))

    print("Bot démarré...")

    app.run_polling()


if __name__ == "__main__":
    main()
