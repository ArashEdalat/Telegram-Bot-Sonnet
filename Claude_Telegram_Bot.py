#pip install python-telegram-bot requests

# On the Telegram search for BotFather.
# Use the /newbot command to create a bot and recieve a bot token

import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace with your API keys
TELEGRAM_TOKEN = "your_telegram_bot_token"
CLAUDE_API_KEY = "your_claude_api_key"
CLAUDE_API_URL = "https://api.anthropic.com/v1/complete"

# Function to send messages to Claude
def query_claude(prompt):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "prompt": f"Assistant: {prompt}",
        "model": "claude-v1.3",
        "max_tokens_to_sample": 300,
    }
    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["completion"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Start command handler
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm your Claude-powered bot. Ask me anything!")

# Message handler
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    update.message.reply_text("Thinking...")
    response = query_claude(user_message)
    update.message.reply_text(response)

# Main function
def main():
    # Set up the Telegram bot
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()