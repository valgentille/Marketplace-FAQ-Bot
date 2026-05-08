"""
Marketplace FAQ Chatbot
-----------------------
Chatbot alimenté par l'API Anthropic (Claude) pour répondre aux questions
fréquentes des vendeurs d'une Marketplace e-commerce.

Auteur : Valerie Kouane Guineo
Modèle : claude-opus-4-7
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")


# --------------------------------------------------------------------------
# Prompt système : définit le rôle et la base de connaissance du bot
# --------------------------------------------------------------------------
SYSTEM_PROMPT = """
Tu es un assistant FAQ pour la Marketplace d'Auchan, une grande enseigne de distribution française.
Tu réponds uniquement aux questions liées à la Marketplace.

## Domaines couverts
- Onboarding vendeur (inscription, validation, documents requis)
- Commissions et frais
- Gestion des commandes et expéditions
- Litiges et remboursements
- Délais et modalités de paiement
- Intégration du catalogue produits
- Support technique

## Informations clés
- Commission : 8% à 15% selon la catégorie produit
- Délai de paiement : 30 jours après livraison confirmée
- Onboarding : dossier en ligne, validation sous 5 jours ouvrés
- Frais d'inscription : gratuits les 3 premiers mois
- Support vendeur : marketplace-support@auchan.fr
- Litiges : traitement sous 48h, médiation possible
- Catalogue : intégration via flux CSV, XML ou API REST

## Instructions
- Réponds de façon concise (3-5 phrases maximum)
- Sois professionnel et bienveillant
- Si la question est hors sujet, redirige poliment vers le bon service
- Si tu n'as pas l'information, dis-le clairement plutôt qu'inventer
"""


class MarketplaceFAQBot:
    """
    Utilise l'API Anthropic pour générer des réponses contextuelles
    basées sur un historique de messages.
    """

    def __init__(self, api_key: str | None = None):
       
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Missing ANTHROPIC_API_KEY in .env")
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-opus-4-7"
        self.conversation_history: list[dict] = []

    def chat(self, user_message: str) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = self.client.messages.create(
            model=self.model,
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=self.conversation_history
        )

        bot_reply = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        return bot_reply
    
    def reset(self):
        self.conversation_history = []
        print("🔄 Conversation réinitialisée.\n")

    def run_cli(self):
        """
        Commandes spéciales :
        - 'quit' ou 'exit' : quitter
        - 'reset' : effacer l'historique
        - 'history' : afficher les messages précédents
        """
        print("=" * 60)
        print("  FAQ Bot — Marketplace Auchan")
        print("  Modèle : claude-sonnet-4-20250514")
        print("  Tapez 'quit' pour quitter, 'reset' pour recommencer")
        print("=" * 60)
        print()
        print("Bot: Bonjour ! Je suis le FAQ Bot de la Marketplace.")
        print("     Posez votre question sur l'onboarding, les commissions,")
        print("     les litiges ou toute autre thématique vendeur.")
        print()

        while True:
            try:
                user_input = input("Vous: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nAu revoir !")
                break

            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit"):
                print("Bot: Au revoir ! N'hésitez pas à revenir.")
                break

            if user_input.lower() == "reset":
                self.reset()
                continue

            if user_input.lower() == "history":
                print(f"\n--- Historique ({len(self.conversation_history)} messages) ---")
                for msg in self.conversation_history:
                    prefix = "Vous" if msg["role"] == "user" else "Bot"
                    print(f"{prefix}: {msg['content'][:80]}...")
                print()
                continue

            print("Bot: ", end="", flush=True)
            response = self.chat(user_input)
            print(response)
            print()
