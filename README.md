# Ollama Telegram Bot

This is a Telegram bot that interfaces with the Ollama language model to provide conversational AI capabilities. It allows users to interact with different personas, log interactions, and manage bot settings.

## Features

-   **Ollama Integration:** Uses the Ollama API to generate responses based on user input.
-   **Multiple Personas:** Supports different conversational personas, allowing the bot to adopt various roles and styles.
-   **Interaction Logging:** Logs all interactions, including user messages, bot responses, and persona used, to a JSON Lines file.
-   **Log Rotation:** Manages log files by rotating them and keeping only the most recent ones.
-   **Telegram Bot Commands:**
    -   `/start` or `/help`: Displays a welcome message and available commands.
    -   `/persona <name>`: Changes the bot's persona to the specified name.
    -   `/logfile`: Returns the path to the current log file.
    -   `/botinfo`: Displays information about the bot, including its username, name, model, and version.
-   **Dynamic Persona Switching:** Users can switch between predefined personas using the `/persona` command.
-   **Modular Design:** The bot is built with modular components for easy maintenance and extension.

## Prerequisites

Before running the bot, ensure you have the following:

-   **Python 3.6+**
-   **Ollama:** Make sure you have Ollama installed and running. You can find installation instructions on the [Ollama website](https://ollama.com/).
-   **Telegram Bot Token:** You need to create a Telegram bot using the [BotFather](https://t.me/botfather) and obtain its API token.
-   **Environment Variables:** Set the `TELEGRAM_BOT_TOKEN` environment variable with your Telegram bot token. Optionally, you can set `OLLAMA_MODEL` to specify the Ollama model to use (defaults to `llama3`).

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
4.  **Set environment variables:**
    - Create a `.env` file in the root directory of the project.
    - Add your Telegram bot token to the `.env` file:
      ```
      TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
      # Optional:
      # OLLAMA_MODEL=llama3
      ```
    - Alternatively, you can set the environment variables directly in your shell.

## Usage

1.  **Run the bot:**

    ```bash
    python src/main.py
    ```
2.  **Interact with the bot on Telegram:**
    - Start a chat with your bot using the bot's username.
    - Use the available commands to interact with the bot.
    - Send messages to the bot, and it will respond using the current persona.

## Configuration

-   **Ollama Model:** The default Ollama model is `llama3`. You can change this by setting the `OLLAMA_MODEL` environment variable or by modifying the `ollama_model` variable in `src/main.py`.
-   **Log Directory:** The log files are stored in the `bot_logs` directory by default. You can change this by modifying the `log_directory` variable in `src/logger.py`.
-   **Max Log Files:** The maximum number of log files to keep is set to 10 by default. You can change this by modifying the `max_log_files` variable in `src/logger.py`.
-   **Personas:** You can add or modify personas in the `src/prompts.py` file.

## File Structure

```
.
├── src
│   ├── __init__.py
│   ├── bot.py        # Main bot logic
│   ├── prompts.py    # Manages system prompts for different personas
│   ├── logger.py     # Manages logging of bot interactions
│   └── main.py       # Entry point for the bot
├── requirements.txt  # List of Python dependencies
└── README.md         # This file
```

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues.

## License

This project is licensed under the MIT License.
