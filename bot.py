import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = "ft:gpt-3.5-turbo-0125:personal:my-poaster:AXRpow9E"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Hi! I am your personal schizophrenic twittos bot. Send me a message!'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
Just send any message and I'll respond with my fine-tuned personality!
    """
    await update.message.reply_text(help_text)

async def get_ai_response(message: str) -> str:
    """Get response from your fine-tuned OpenAI model"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": message}],
            max_tokens=150,
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "Sorry, I encountered an error processing your message."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and respond with AI."""
    try:
        # Show typing action while getting response
        await update.message.chat.send_action('typing')
        
        # Get AI response
        ai_response = await get_ai_response(update.message.text)
        
        # Send response back to user
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text(
            "Sorry, I encountered an error processing your message."
        )

def main():
    """Start the bot."""
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()