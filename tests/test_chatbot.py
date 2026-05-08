"""
Tests unitaires pour le MarketplaceFAQBot.

Utilise des mocks pour éviter les appels API réels durant les tests.
"""

import unittest
from unittest.mock import MagicMock, patch


class TestMarketplaceFAQBot(unittest.TestCase):
    """Tests du comportement du chatbot sans appels API réels."""

    def setUp(self):
        with patch("src.chatbot.Anthropic") as mock_anthropic_class:
            self.mock_client = MagicMock()
            mock_anthropic_class.return_value = self.mock_client

            from src.chatbot import MarketplaceFAQBot
            self.bot = MarketplaceFAQBot(api_key="test-key")

    def _mock_response(self, text: str):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=text)]
        self.mock_client.messages.create.return_value = mock_response

    def test_chat_returns_string(self):
        self._mock_response("La commission est de 10%.")
        result = self.bot.chat("Quelles sont les commissions ?")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_conversation_history_grows(self):
        self._mock_response("Réponse de test.")
        self.assertEqual(len(self.bot.conversation_history), 0)

        self.bot.chat("Première question")
        self.assertEqual(len(self.bot.conversation_history), 2)

        self.bot.chat("Deuxième question")
        self.assertEqual(len(self.bot.conversation_history), 4)

    def test_reset_clears_history(self):
        self._mock_response("Réponse.")
        self.bot.chat("Question test")
        self.assertGreater(len(self.bot.conversation_history), 0)

        self.bot.reset()
        self.assertEqual(len(self.bot.conversation_history), 0)

    def test_history_roles(self):
        self._mock_response("Réponse bot.")
        self.bot.chat("Message utilisateur")

        self.assertEqual(self.bot.conversation_history[0]["role"], "user")
        self.assertEqual(self.bot.conversation_history[1]["role"], "assistant")

    def test_api_called_with_history(self):
        self._mock_response("Première réponse.")
        self.bot.chat("Question 1")

        self._mock_response("Deuxième réponse.")
        self.bot.chat("Question 2")

        last_call_messages = self.mock_client.messages.create.call_args.kwargs["messages"]
        self.assertEqual(len(last_call_messages), 4)  # Q1 + R1 + Q2 + R2
        self.assertEqual(last_call_messages[2]["content"], "Question 2")
        self.assertEqual(last_call_messages[2]["role"], "user")

    def test_system_prompt_used(self):
        self._mock_response("Réponse.")
        self.bot.chat("Test")

        call_kwargs = self.mock_client.messages.create.call_args.kwargs
        self.assertIn("system", call_kwargs)
        self.assertIn("Marketplace", call_kwargs["system"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
