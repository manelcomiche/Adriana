import discord
import aiohttp
import asyncio
import time
import re
from discord.ext import commands
from dotenv import load_dotenv
import os

from gtts import gTTS

# Load environment variables from .env file
load_dotenv()

# Retrieve tokens and API keys from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
NAGA_API_KEY = os.getenv('NAGA_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

intents = discord.Intents.all()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Transcribing Audio"))
    print(f"Logged in as {bot.user.name}")

async def transcribe_audio(file_url: str):
    # Start the timer to measure the transcription time
    start_time = time.monotonic()

    url = "https://api.naga.ac/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {NAGA_API_KEY}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status != 200:
                return None
            file_data = await response.read()

        form_data = aiohttp.FormData()
        form_data.add_field('file', file_data, filename='voice-message.ogg', content_type='audio/ogg')
        form_data.add_field('model', 'whisper-large-v3')

        async with session.post(url, headers=headers, data=form_data) as resp:
            if resp.status == 200:
                data = await resp.json()
                # Measure and print the time taken for transcription
                end_time = time.monotonic()
                print(f"Transcription took {end_time - start_time:.2f} seconds")
                return data.get("text", None)
            else:
                print(f"Transcription error: {resp.status}")
                return None

async def get_weather(city: str):
    # Start the timer to measure the weather API response time
    start_time = time.monotonic()

    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=yes&lang=en"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                weather_data = await resp.json()
                # Measure and print the time taken for the weather API call
                end_time = time.monotonic()
                print(f"Weather API call took {end_time - start_time:.2f} seconds")
                return weather_data
            else:
                print(f"Weather API error: {resp.status}")
                return None

async def format_weather_response(weather_data):
    if not weather_data:
        return "I'm sorry, I couldn't retrieve the weather information."

    condition = weather_data['current']['condition']['text']
    temp_c = weather_data['current']['temp_c']
    feelslike_c = weather_data['current']['feelslike_c']
    return f"The current weather is {condition} with a temperature of {temp_c}°C, feeling like {feelslike_c}°C."

async def get_gpt_response(prompt: str):
    # Start the timer to measure the GPT API response time
    start_time = time.monotonic()

    url = "https://api.naga.ac/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NAGA_API_KEY}"
    }
    body = {
        "model": "llama-3-8b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=headers) as resp:
            data = await resp.json()
            # Measure and print the time taken for the GPT API call
            end_time = time.monotonic()
            print(f"GPT response took {end_time - start_time:.2f} seconds")
            return data["choices"][0]["message"]["content"]

async def text_to_speech(text: str, voice_channel, language='en'):
    # Start the timer to measure the TTS process time
    start_time = time.monotonic()

    # Generate TTS using gTTS
    tts = gTTS(text=text, lang=language)
    tts.save("output.mp3")

    # Measure and print the time taken for the TTS generation
    end_time = time.monotonic()
    print(f"TTS generation took {end_time - start_time:.2f} seconds")

    # Connect to the voice channel
    if not voice_channel.guild.voice_client:
        vc = await voice_channel.connect()
    else:
        vc = voice_channel.guild.voice_client

    # Play the generated audio file
    vc.play(discord.FFmpegPCMAudio("output.mp3"))
    while vc.is_playing():
        await asyncio.sleep(1)
    
    await vc.disconnect()

    # Clean up the audio file after playing
    os.remove("output.mp3")

async def process_voice_message(message):
    attachment = message.attachments[0]
    if attachment.content_type.startswith('audio/'):
        # Transcribe the audio
        transcription = await transcribe_audio(attachment.url)
        if not transcription:
            await message.channel.send("I couldn't transcribe the audio.")
            return

        # Check if the transcription is related to weather
        match = re.search(r'what\s+is\s+the\s+weather\s+like\s+in\s+(\w+)', transcription, re.IGNORECASE)
        if match:
            city = match.group(1)
            weather_data = await get_weather(city)
            weather_response = await format_weather_response(weather_data)
            gpt_response = await get_gpt_response(f"Summarize this weather information for {city} into one sentence: {weather_response}")
            print(gpt_response)
        else:
            # Get the GPT response for non-weather-related queries
            gpt_response = await get_gpt_response('Answer with a brief text as a simple voice assistant to this message, try to be concise: ' + transcription)
        
        if not gpt_response:
            await message.channel.send("I couldn't get a response from GPT.")
            return

        # Connect to voice channel and speak
        if message.author.voice:
            await text_to_speech(gpt_response, message.author.voice.channel, language='en')
        else:
            await message.channel.send("You are not connected to a voice channel.")

@bot.event
async def on_message(message):
    if message.attachments:
        await process_voice_message(message)

bot.run(DISCORD_TOKEN)