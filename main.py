from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI
from pystyle import Colorate, Colors, Write

import os
import random
import platform
import subprocess



client = OpenAI(
    api_key="not-required",
    base_url="https://text.pollinations.ai/openai/"
)

console = Console()


messages = [{"role": "system", "content": "You are helpful AI Assitant named Copilot"}]

def get_response(prompt, model, messages):
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        seed=random.randint(1, 1337),
    )
    
    assistant_reply = response.choices[0].message.content
    
    messages.append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply

model = "openai-large"
sym = "[:]"

menu = """
            __ 
  ___  ___ / /  
 / _ \(_-</ _ |
/_//_/___/_//_/

📡 Connected succesfully
📶 Provider: Pollinations.AI
🤖 Model: OpenAI Large (GPT-4o)


"""
print(Colorate.Horizontal(Colors.cyan_to_blue, menu, 1))
while True:
    prompt = input(Colorate.Horizontal(Colors.cyan_to_blue, "[>] ", 1))
    if prompt.startswith("search:"):
        model = "searchgpt"
        prompt = prompt[7:]
    with console.status("", spinner="bouncingBall"):
        response = get_response(prompt, model, messages)
    print(Colorate.Horizontal(Colors.cyan_to_blue, "\n[<] ", 1), end="")
    console.print(Markdown(response))
    