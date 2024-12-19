import telebot
import requests
from prompts import PromptManager
from logger import InteractionLogger

class OllamaTelegramBot:
    def __init__(self, telegram_token, ollama_model='llama3'):
        """
        Initialize the Telegram bot with modular components.
        
        :param telegram_token: Telegram Bot API token
        :param ollama_model: Name of the Ollama model to use (default: llama3)
        """
        # Initialize bot components
        self.bot = telebot.TeleBot(telegram_token)
        self.ollama_model = ollama_model
        
        # Initialize modular components
        self.prompt_manager = PromptManager()
        self.interaction_logger = InteractionLogger()
        
        # Current persona tracking
        self.current_persona = 'default'
        
        # Register message handlers
        self._register_handlers()
        
    def _initialize_bot_info(self):
        """
        Get bot information and initialize logger with it.
        """
        try:
            bot_user = self.bot.get_me()
            bot_info = {
                'bot_id': bot_user.id,
                'bot_username': bot_user.username,
                'bot_name': bot_user.first_name,
                'is_bot': bot_user.is_bot,
                'supports_inline': bot_user.supports_inline_queries,
                'model': self.ollama_model,
                'version': '1.0.0'  # You can add version tracking
            }
            self.interaction_logger.set_bot_info(bot_info)
            print(f"Bot initialized: @{bot_user.username}")
        except Exception as e:
            print(f"Warning: Could not get bot information: {e}")
            self.interaction_logger.set_bot_info({
                'bot_id': 'unknown',
                'model': self.ollama_model,
                'error': str(e)
            })
    
    def _register_handlers(self):
        """
        Register all Telegram bot message handlers.
        """
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            welcome_text = (
                "👋 Welcome to ChusDeBoss Telegram Bot!\n\n"
                "Commands:\n"
                "/help - Show this help message\n"
                "/persona <name> - Change bot's personality\n"
                "/logfile - Get the current log file path\n"
                "/botinfo - Get information about this bot\n"
                "Available combined personas: \n  " + "\n  ".join(self.prompt_manager.list_personas())
            )
            self.bot.reply_to(message, welcome_text)
            
        @self.bot.message_handler(commands=['botinfo'])
        def send_bot_info(message):
            bot_info = self.interaction_logger.bot_info
            if bot_info:
                info_text = (
                    f"Bot Information:\n"
                    f"Username: @{bot_info.get('bot_username', 'N/A')}\n"
                    f"Name: {bot_info.get('bot_name', 'N/A')}\n"
                    f"Model: {bot_info.get('model', 'N/A')}\n"
                    f"Version: {bot_info.get('version', 'N/A')}"
                )
            else:
                info_text = "Bot information not available."
            self.bot.reply_to(message, info_text)
        
        @self.bot.message_handler(commands=['logfile'])
        def send_log_file(message):
            log_file_path = self.interaction_logger.get_current_log_file()
            response = f"Current log file: {log_file_path}"
            self.bot.reply_to(message, response)
        
        @self.bot.message_handler(commands=['persona'])
        def change_persona(message):
            try:
                # Extract persona name from the command
                persona_name = message.text.split(' ', 1)[1].strip().lower()
                
                if persona_name in self.prompt_manager.list_personas():
                    self.current_persona = persona_name
                    response = f"Persona changed to: {persona_name}"
                else:
                    response = (
                        "Persona not found. Available personas: " + 
                        ", ".join(self.prompt_manager.list_personas())
                    )
                
                self.bot.reply_to(message, response)
            
            except IndexError:
                self.bot.reply_to(message, 
                    "Please specify a combined persona. Use /persona <name>. "
                    "Available: " + ", ".join(self.prompt_manager.list_personas())
                )
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            # Get user information
            user_id = message.from_user.id
            username = message.from_user.username or "Anonymous"
            
            # Generate response
            response = self.get_ollama_response(message.text)
            
            # Log the interaction
            self.interaction_logger.log_interaction(
                user_id, 
                username, 
                message.text, 
                response, 
                self.current_persona
            )
            
            # Reply to the user
            self.bot.reply_to(message, response)
    
    def get_ollama_response(self, prompt):
        """
        Generate a response using Ollama API with combined system prompt.
        """
        try:
            system_prompt = self.prompt_manager.get_persona(self.current_persona)
            
            response = requests.post('http://localhost:11434/api/generate', json={
                'model': self.ollama_model,
                'system': system_prompt,
                'prompt': prompt,
                'stream': False
            })
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return "Sorry, I couldn't generate a response. There might be an issue with the Ollama server."
        
        except requests.exceptions.ConnectionError:
            return "Unable to connect to Ollama server. Please ensure it's running."
        
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def run(self):
        """
        Start the Telegram bot
        """
        print(f"Bot is running using {self.ollama_model} model...")
        print(f"Interactions will be logged to: {self.interaction_logger.get_current_log_file()}")
        self.bot.infinity_polling()