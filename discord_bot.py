import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenvgit

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_URL = "http://127.0.0.1:8000/validate"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Omoikane has entered the server as {bot.user}')

@bot.command(name="analyze")
async def analyze(ctx, *, user_draft):
    await ctx.send("🔍 *Omoikane is analyzing the multiverse threads...*")
   
    payload = {"draft_text": user_draft} 
            
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            analysis_text = data.get('analysis', 'No analysis returned.')
            await ctx.send(f"**ARCHIVIST REPORT:**\n{analysis_text}")
        else:
            await ctx.send(f"❌ Core Error: Received status {response.status_code}")
            
    except Exception as e:
        await ctx.send(f"❌ Connection failed: {e}")

bot.run(TOKEN)