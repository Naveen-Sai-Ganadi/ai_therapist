import os
import logging
from telegram import Update, BotCommand, MenuButtonDefault
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
from groq_response import get_groq_response

# Load environment variables
load_dotenv()
TELEGRAM_BOT_API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "🤖 The first AI life coach available 24/7 used by thousands of ppl\n\n"
        "📜 Disclaimer\n"
        "By continuing, you agree to understand I am an AI life coach. I am not a licensed psychologist, "
        "therapist, or healthcare professional and do not replace the care of those. I cannot take any "
        "responsibility for the results of your actions, and any harm you suffer as a result of the use, or "
        "non-use of the information available. Use judgment and due diligence before taking any action or plan "
        "suggested. Do not use if you feel in danger to yourself or others, instead find a professional at findahelpline.com\n\n"
        "✅ Reframe your negative thoughts\n"
        "✅ Take action and get unstuck\n"
        "✅ Get you fit which helps your mind\n"
        "✅ Talk you through your day\n"
        "✅ Feel better by checking up on you\n\n"
        "You can\n"
        "📣 Send me a voice message and I'll respond by voice\n"
        "📸 Send me a photo of your day and we can discuss it\n"
        "🔍 Send me a URL web address and we can discuss it\n\n"
        "Write /reset at any moment to delete your entire convo history from our servers\n\n"
        "💡 Feedback\n"
        "Have feedback, ideas and bugs for me? Visit https://ideasbugs.canny.io/therapist-ai"
    )
    await update.message.reply_text(welcome_message)

# Command handler for /reset
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Your conversation history has been reset.")

# Message handler for general messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logger.info(f"Received message from user {update.message.from_user.id}: {user_message}")
    try:
        response = await get_groq_response(user_message)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        await update.message.reply_text("Sorry, I couldn't process your request.")

def main():
    application = Application.builder().token(TELEGRAM_BOT_API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Set the custom menu button
    bot = application.bot
    bot.set_my_commands([
        BotCommand("start", "Start a new conversation"),
        BotCommand("reset", "Delete your conversation history")
    ])

    logger.info("Starting bot polling")
    application.run_polling()

if __name__ == "__main__":
    main()
