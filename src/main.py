import os
from dotenv import load_dotenv
from bot import OllamaTelegramBot

load_dotenv()  # Load the .env file

def main():
    # Get Telegram bot token from environment variable
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not telegram_token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
        return
    
    # Optional: specify a different Ollama model
    # ollama_model = os.getenv('OLLAMA_MODEL', 'llama3')
    ollama_model='llama3.2:1b'
    # Create and run the bot
    bot = OllamaTelegramBot(telegram_token, ollama_model)
    bot.run()

if __name__ == '__main__':
    main()