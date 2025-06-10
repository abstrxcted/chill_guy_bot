from groq import Groq
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import time

#Loading keys/tokens from .env
load_dotenv()

#Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)


#Set Groq API Key
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

#On bot log in
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore the bot's own messages
    await bot.process_commands(message)

#Main query function
@bot.command()
# * means everything after the command string is one text
# message: str = "" provides a fallback if the message has no extra text
async def yochillguy(ctx, *, message: str = "hi"):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"""message from {ctx.author}: {message} {os.getenv("CONTEXT")}""",
        }
    ],
    model="llama-3.3-70b-versatile",
)

    print(f"{ctx.author} said \"{message}\", and Chillguybot replied with: \"{chat_completion.choices[0].message.content}\"")

    time.sleep(1.5)
    await ctx.send(chat_completion.choices[0].message.content)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))

