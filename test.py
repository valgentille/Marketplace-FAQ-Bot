from anthropic import Anthropic

client = Anthropic()

models = client.models.list()

for m in models:
    print(m.id)