import os
import json
from datetime import datetime

class InteractionLogger:
    """
    Manages logging of bot interactions with advanced features.
    """
    def __init__(self, log_directory='bot_logs', max_log_files=10):
        """
        Initialize interaction logger with log file management.
        
        :param log_directory: Directory to store log files
        :param max_log_files: Maximum number of log files to keep
        """
        # Create log directory if it doesn't exist
        self.log_directory = log_directory
        os.makedirs(log_directory, exist_ok=True)
        
        # Manage log file rotation
        self.max_log_files = max_log_files
        self._rotate_logs()
        
        # Generate unique log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_directory, f"interaction_log_{timestamp}.jsonl")
    
        # Store bot information
        self.bot_info = None
        
    def set_bot_info(self, bot_info):
        """
        Store bot information and write initial session log.
        
        :param bot_info: Dictionary containing bot information
        """
        self.bot_info = bot_info
        
        # Log session start with bot information
        session_info = {
            'event_type': 'session_start',
            'timestamp': datetime.now().isoformat(),
            'bot_info': self.bot_info
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as log_file:
            log_file.write(json.dumps(session_info) + '\n')  
            
              
    def _rotate_logs(self):
        """
        Rotate log files, keeping only the most recent logs.
        """
        # Get all log files, sorted by creation time
        log_files = sorted(
            [f for f in os.listdir(self.log_directory) if f.startswith('interaction_log_')],
            reverse=True
        )
        
        # Delete excess log files
        for old_log in log_files[self.max_log_files:]:
            os.remove(os.path.join(self.log_directory, old_log))
    
    def log_interaction(self, user_id, username, message, bot_response, persona):
        """
        Log a single interaction to a JSON Lines (JSONL) file.
        
        :param user_id: Telegram user ID
        :param username: Telegram username
        :param message: User's input message
        :param bot_response: Bot's generated response
        :param persona: Current bot persona
        """
        interaction = {
            'event_type': 'interaction',
            'timestamp': datetime.now().isoformat(),
            'bot_info': self.bot_info,
            'user_id': user_id,
            'username': username,
            'message': message,
            'bot_response': bot_response,
            'persona': persona
        }
        
        # Append to log file in JSON Lines format
        with open(self.log_file, 'a', encoding='utf-8') as log_file:
            log_file.write(json.dumps(interaction) + '\n')
    
    def get_current_log_file(self):
        """
        Return the path to the current log file.
        
        :return: Path to the current log file
        """
        return self.log_file
    
    def analyze_logs(self, log_file=None):
        """
        Analyze log files and provide basic statistics.
        
        :param log_file: Specific log file to analyze (defaults to current)
        :return: Dictionary of log analysis
        """
        if log_file is None:
            log_file = self.log_file
        
        analysis = {
            'total_interactions': 0,
            'users': set(),
            'personas_used': set()
        }
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    interaction = json.loads(line)
                    analysis['total_interactions'] += 1
                    analysis['users'].add(interaction['user_id'])
                    analysis['personas_used'].add(interaction['persona'])
            
            # Convert sets to lists for JSON serialization
            analysis['users'] = list(analysis['users'])
            analysis['personas_used'] = list(analysis['personas_used'])
            
            return analysis
        except FileNotFoundError:
            return {"error": "Log file not found"}
        
        
        