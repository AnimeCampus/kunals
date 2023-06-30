import random
import json
from pyrogram import Client, filters

# Initialize the Pyrogram client
api_id = 16743442
api_hash = '12bbd720f4097ba7713c5e40a11dfd2a'
bot_token = '5992274138:AAHLa2D-jnuMqIz9mixrTlkMjKWoPxaWxck'

app = Client('my_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Counter for tracking message count
message_count = 0
catch_attempts = {}

# Function to retrieve a random Pokemon and its image
def get_random_pokemon():
    with open('pokemon.json', 'r') as file:
        pokemon_data = json.load(file)
    
    if pokemon_data:
        pokemon_entry = random.choice(pokemon_data)
        pokemon_name = pokemon_entry["name"]
        pokemon_image = pokemon_entry["image"]
        return pokemon_name, pokemon_image
    
    return None, None

# Function to handle incoming messages
@app.on_message(filters.group)
def handle_messages(client, message):
    global message_count
    global catch_attempts
    
    # Increment message count
    message_count += 1
    
    # Check if it's time to send a new Pokemon
    if message_count % 10 == 0:
        # Get a random Pokemon
        pokemon_name, pokemon_image = get_random_pokemon()
        if pokemon_name and pokemon_image:
            # Add the Pokemon to catch_attempts dictionary
            catch_attempts[message.chat.id] = pokemon_name
            
            reply_text = "A wild Pokemon appeared!"
            message.reply_photo(pokemon_image, caption=reply_text)

    # Check if the message is a catch attempt
    if message.text and message.text.lower() == 'catch':
        chat_id = message.chat.id
        if chat_id in catch_attempts:
            pokemon_name = catch_attempts[chat_id]
            if random.random() < 0.5:
                reply_text = f"Congratulations! You caught the {pokemon_name}!"
            else:
                reply_text = f"Oops! The {pokemon_name} escaped!"
            
            # Remove the Pokemon from catch_attempts
            del catch_attempts[chat_id]
            
            message.reply_text(reply_text)

# Start the bot
app.run()
