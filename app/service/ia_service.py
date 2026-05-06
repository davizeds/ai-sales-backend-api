from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)



def generate_response(pergunta, contexto):
    response=client.chat.completions.create(model='gpt-4o-mini',messages=[{'role': "system", 'content': contexto}, {'role': "user",'content': pergunta}])
    resposta=response.choices[0].message.content
    return resposta
