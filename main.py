"""
Point d'entrée principal du FAQ Bot.

Usage :
    python main.py
"""

from src.chatbot import MarketplaceFAQBot


def main():
    bot = MarketplaceFAQBot()
    bot.run_cli()


if __name__ == "__main__":
    main()
