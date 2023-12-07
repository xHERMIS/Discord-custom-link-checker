import requests
import random
import string
import time

def generate_random_invite_code(length):
    # Generate a random invite code with the specified length
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def check_invite_validity(invite_code, webhook_url):
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = 'YOUR_BOT_TOKEN'
    
    # Discord API endpoint for invite info
    api_url = f'https://discord.com/api/v10/invites/{invite_code}?with_counts=true&token={bot_token}'
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('guild'):
            result = f"🔴 Unavailable link: {invite_code}"
        else:
            result = f"🟢 Available link: {invite_code}"
    else:
        result = f"🟢 Available link: {invite_code}"
    
    # Send the result through Discord webhook
    send_result_to_discord(result, webhook_url)

def send_result_to_discord(result, webhook_url):
    embed_data = {
        "title": "Discord Invite Checker Results",
        "description": result,
        "color": 16711680 if "🔴" in result else 65280,  # Red or Green color based on result
    }

    webhook_name = "xHERMIS"
    avatar_url = "https://cdn.discordapp.com/attachments/1179119779282423892/1182382349615370240/39e97f13b98cdf4a08f69861fc83fe9f_1.jpg"

    payload = {
        "username": webhook_name,
        "avatar_url": avatar_url,
        "embeds": [embed_data],
    }

    requests.post(webhook_url, json=payload)

# Prompt the user for the number of links to check
num_links = int(input("How many links do you want to check? "))

# Prompt the user for the number of characters each link should contain
link_length = int(input("How many characters should each link contain? "))

# Prompt the user for the Discord webhook URL
webhook_url = input("Enter your Discord webhook URL: ")

# Check the validity of the specified number of random invite codes with a delay
for _ in range(num_links):
    random_invite_code = generate_random_invite_code(link_length)
    check_invite_validity(random_invite_code, webhook_url)
    time.sleep(1)  # Add a delay of 1 second between requests
