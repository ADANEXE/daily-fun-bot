import os
import discord
from discord.ext import commands
from discord import app_commands
import json
import random
from keep_alive import keep_alive

TOKEN = os.getenv("TOKEN")
SUPPORT_SERVER = os.getenv("SUPPORT_SERVER")
BOT_INVITE = os.getenv("BOT_INVITE")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Load server questions
try:
    with open("data.json", "r") as f:
        data = json.load(f)
except:
    data = {}
    with open("data.json", "w") as f:
        json.dump(data, f)

daily_channel = {}

def save_data():
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# Admin sets daily channel
@bot.tree.command(name="daily_setup", description="Set daily fun channel")
@app_commands.describe(channel="Channel for daily posts")
async def daily_setup(interaction: discord.Interaction, channel: discord.TextChannel):
    daily_channel[interaction.guild.id] = channel.id
    await interaction.response.send_message(f"✅ Daily fun channel set to {channel.mention}", ephemeral=True)

# Admin adds question
@bot.tree.command(name="add_question", description="Add a daily question for your server")
@app_commands.describe(question="Question text")
async def add_question(interaction: discord.Interaction, question: str):
    gid = str(interaction.guild.id)
    if gid not in data:
        data[gid] = []
    data[gid].append(question)
    save_data()
    await interaction.response.send_message("✅ Question added!", ephemeral=True)

# Post today's question
@bot.tree.command(name="daily_now", description="Post today's fun question now")
async def daily_now(interaction: discord.Interaction):
    gid = str(interaction.guild.id)
    if interaction.guild.id not in daily_channel:
        await interaction.response.send_message("❌ Daily channel not set. Use /daily_setup", ephemeral=True)
        return

    channel = bot.get_channel(daily_channel[interaction.guild.id])
    questions = data.get(gid, [
        "🔥 Would you rather fly or be invisible?",
        "😂 What's the most embarrassing thing you've done?",
        "🤔 Is cereal a soup?"
    ])
    question = random.choice(questions)

    embed = discord.Embed(title="🎉 Daily Fun", description=question, color=discord.Color.orange())
    await channel.send(embed=embed)
    await interaction.response.send_message("✅ Posted!", ephemeral=True)

# About command
@bot.tree.command(name="about", description="About the bot")
async def about(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎉 Daily Fun Bot",
        description="Posts daily fun questions in your server!",
        color=discord.Color.green()
    )
    embed.add_field(name="👨‍💻 Developer", value="Otaku | Adan", inline=False)
    embed.add_field(name="🛠 Support Server", value=f"[Join Here]({SUPPORT_SERVER})", inline=False)
    embed.add_field(name="➕ Invite Bot", value=f"[Invite]({BOT_INVITE})", inline=False)
    embed.set_footer(text="Daily Fun Bot | Public Bot Ready")
    await interaction.response.send_message(embed=embed, ephemeral=True)

keep_alive()
bot.run(TOKEN)
