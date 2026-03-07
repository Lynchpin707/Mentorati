import chainlit as cl
import sys
import os

# Ensure the root is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generator import query_buddy

@cl.on_chat_start
async def start():
    # Store a welcome message so it doesn't repeat every time
    await cl.Message(content="¡Hola! I am your Spanish Grammar Mentora. Let me know what's on your mind!", author="Mentorati").send()



@cl.author_rename
def rename(orig_author: str):
    rename_dict = {"Assistant": "Mentorati", "Chatbot": "Mentorati"}
    return rename_dict.get(orig_author, orig_author)

@cl.on_message
async def main(message: cl.Message):

    answer, sources = await cl.make_async(query_buddy)(message.content)

    source_text = f"\n\n*Sources: {', '.join(set(sources))}*"
    

    await cl.Message(
        content=f"{answer}{source_text}", 
        author="Mentorati" 
    ).send()