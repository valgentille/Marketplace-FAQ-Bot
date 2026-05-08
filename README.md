# 🤖 Marketplace FAQ Bot

Chatbot conversationnel alimenté par l'API Anthropic (Claude) pour automatiser le support vendeur d'une Marketplace e-commerce.

## Aperçu

Ce projet démontre l'intégration d'un LLM (Large Language Model) dans un contexte métier réel : répondre automatiquement aux questions fréquentes des vendeurs partenaires d'une Marketplace, en conservant le contexte de la conversation.

```
Bot: Bonjour ! Je suis le FAQ Bot de la Marketplace.
     Posez votre question sur l'onboarding, les commissions...

Vous: Comment devenir vendeur ?

Bot: Pour devenir vendeur sur notre Marketplace, vous devez soumettre
     un dossier en ligne sur notre portail vendeur. La validation
     prend 5 jours ouvrés. L'inscription est gratuite les 3 premiers mois.
     Vous aurez besoin de votre SIRET, RIB et d'une pièce d'identité.

Vous: Et les commissions ?

Bot: Les commissions varient de 8% à 15% selon la catégorie produit.
     Elles sont prélevées automatiquement sur chaque vente réalisée.
     Le détail par catégorie est disponible dans votre espace vendeur.
```

## Architecture

```
marketplace-faq-bot/
├── src/
│   └── chatbot.py        # Classe principale MarketplaceFAQBot
├── tests/
│   └── test_chatbot.py   # Tests unitaires (avec mocks)
├── main.py               # Point d'entrée CLI
├── requirements.txt
├── .env.example
└── README.md
```

## Fonctionnalités

- **Conversation multi-turn** : mémorise le contexte entre les échanges
- **Prompt système métier** : connaissances spécifiques à la Marketplace (commissions, onboarding, litiges...)
- **Interface CLI interactive** : commandes `reset`, `history`, `quit`
- **Tests unitaires** : couverture des cas principaux avec mocks de l'API
- **Gestion des variables d'environnement** : clé API via `.env`

## Technologies

| Outil | Rôle |
|-------|------|
| Python 3.11+ | Langage principal |
| Anthropic SDK | Accès au modèle Claude |
| `unittest.mock` | Tests sans appels API réels |
| `python-dotenv` | Gestion des secrets |

## Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/valgentille/marketplace-faq-bot.git
cd marketplace-faq-bot

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou : venv\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer la clé API
cp .env.example .env
# Éditez .env et ajoutez votre clé ANTHROPIC_API_KEY
```

## Utilisation

```bash
# Lancer le chatbot en mode CLI
python main.py
```

### Commandes disponibles dans le CLI

| Commande | Action |
|----------|--------|
| *(votre question)* | Envoie un message au bot |
| `reset` | Efface l'historique de conversation |
| `history` | Affiche les messages précédents |
| `quit` / `exit` | Quitte le chatbot |

### Utilisation en tant que module

```python
from src.chatbot import MarketplaceFAQBot

bot = MarketplaceFAQBot()  

# Question simple
reponse = bot.chat("Quelles sont les commissions ?")
print(reponse)

# Question de suivi (contexte conservé)
reponse2 = bot.chat("Et pour la catégorie électroménager ?")
print(reponse2)

# Réinitialiser la conversation
bot.reset()
```

## Tests

```bash
python -m pytest tests/ -v
```

Les tests utilisent des mocks (`unittest.mock`) pour simuler l'API Anthropic, ce qui permet de tester sans consommer de tokens ni nécessiter une connexion.

```
test_chat_returns_string ..................... OK
test_conversation_history_grows ............. OK
test_reset_clears_history ................... OK
test_history_roles .......................... OK
test_api_called_with_history ................ OK
test_system_prompt_used ..................... OK
```

## Personnalisation du prompt système

Le comportement du bot est entièrement contrôlé par le `SYSTEM_PROMPT` dans `src/chatbot.py`. Pour adapter ce bot à un autre contexte métier, il suffit de modifier ce prompt :

```python
SYSTEM_PROMPT = """
Tu es un assistant FAQ pour [votre entreprise].
...
"""
```

## Licence
MIT
