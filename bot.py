import random
import requests
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import configparser

# Read configuration from the file
config = configparser.ConfigParser()
config.read("config.ini")

# Get API ID, hash, and bot token from the configuration
api_id = config.getint("Telegram", "api_id")
api_hash = config.get("Telegram", "api_hash")
bot_token = config.get("Telegram", "bot_token")

# Create a Pyrogram client
bot = Client("pokemon_team_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# Function to retrieve Pokémon information from PokeAPI
def get_pokemon_info(pokemon_name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
    if response.status_code == 200:
        data = response.json()
        pokemon = {
            "name": data["name"],
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
            "moves": [m["move"]["name"] for m in data["moves"]],
        }
        return pokemon
    return None


# Start command handler
@bot.on_message(filters.command("start"))
def start_command(client, message):
    # Display a welcome message and available playstyle options
    keyboard = [
        [InlineKeyboardButton("Offensive", callback_data="offensive")],
        [InlineKeyboardButton("Defensive", callback_data="defensive")],
        [InlineKeyboardButton("Balanced", callback_data="balanced")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text("Welcome to the Pokémon Team Builder! Please select a playstyle:", reply_markup=reply_markup)


# Callback query handler for playstyle selection
@bot.on_callback_query()
def playstyle_selected(client, query):
    playstyle = query.data
    if playstyle == "offensive":
        pokemons = ["charizard", "gengar", "dragonite", "machamp", "tyranitar"]
    elif playstyle == "defensive":
        pokemons = ["blissey", "skarmory", "slowbro", "ferrothorn", "gliscor"]
    elif playstyle == "balanced":
        pokemons = ["metagross", "landorus", "tapu-fini", "clefable", "excadrill"]
    else:
        query.message.reply_text("Invalid playstyle selected.")
        return

    # Generate a random team based on the selected playstyle
    team = random.sample(pokemons, 6)
    reply_text = f"Here's your {playstyle.capitalize()} Pokémon team:\n\n"
    for pokemon_name in team:
        pokemon = get_pokemon_info(pokemon_name)
        if pokemon:
            reply_text += f"- {pokemon['name'].capitalize()}\n"
            reply_text += f"  Type(s): {', '.join(pokemon['types'])}\n"
            reply_text += f"  Abilities: {', '.join(pokemon['abilities'])}\n"
            reply_text += f"  Moves: {', '.join(pokemon['moves'])}\n\n"

    query.message.reply_text(reply_text)


# Error handler
@bot.on_error()
def error_handler(client, message):
    pass


# Start the bot
bot.run()
idle() 
