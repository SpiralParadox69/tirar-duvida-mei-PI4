import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv() 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

resposta = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Diga olá em uma frase."}],
)

print(resposta.choices[0].message.content)
