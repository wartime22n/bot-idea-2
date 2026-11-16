import discord
from discord.ext import commands
import requests
import pyttsx3
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

def doviz(cur, re):
    url = f'https://api.frankfurter.dev/v2/rates?quotes={re}&base={cur}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[0]['rate'], response.json()[0]['date']
    else:
        return "Bilgi alinamadi."

def reddit():
    url = "https://uselessfacts.jsph.pl/random.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['text'],response.json()['permalink']
    else:
        return "Bilgi alinamadi."
def get_weather(city):
    img_url = f"https://wttr.in/{city}.png"
    url = f"https://wttr.in/{city}?format=%C+%t"
    img_res = requests.get(img_url)
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return "Hava durumu alınamadı."
def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 130)
    engine.say(text)
    engine.runAndWait()
@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')
@bot.command()
async def dov(ctx, currency, re):
    data, date = doviz(currency, re)
    await ctx.send(f'{data} (Tarih: {date})')
@bot.command()
async def fact(ctx):
    fact, permalink = reddit()
    await ctx.send(fact)
    await ctx.send(permalink)
    speak(fact)
@bot.command()
async def hello(ctx):
    await ctx.send(f'Merhaba! Ben {bot.user}, bir Discord sohbet botuyum!')

@bot.command()
async def weather(ctx, city):
    weather = get_weather(city)
    await ctx.send(f'{city} için hava durumu: {weather}')
    speak(f'{city} weather: {weather}')
    await ctx.send(f"https://wttr.in/{city}.png")


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


bot.run("BUFghhnfnajl326B2H3JJ2JKM2JF2JUHhdhsh345")