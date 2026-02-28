import requests
from bs4 import BeautifulSoup
import os
import pytz
from datetime import datetime

def check_site():
    url = "https://in.bookmyshow.com/cinemas/mumbai/miraj-cinemas-imax-wadala/buytickets/MCIW/20260319"
    target_movie = "dhurandhar" # Change this to "scream" for testing
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        
        # Log the attempt for Streamlit
        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST).strftime('%d %b %Y, %I:%M %p')
        with open("last_check.txt", "w") as f:
            f.write(f"{current_time} (Status: {response.status_code})")

        # The Scraper Part
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This searches specifically for text within the page tags
        found = soup.find_all(string=lambda text: target_movie.lower() in text.lower())

        if found:
            send_telegram_alert(f"✅ SCRAPER ALERT: '{target_movie}' found on BookMyShow!\nLink: {url}")
        elif response.status_code != 200:
            send_telegram_alert(f"⚠️ BOT BLOCKED: Received Status {response.status_code}. BookMyShow is blocking the scraper.")
            
    except Exception as e:
        print(f"Scraper Error: {e}")

def send_telegram_alert(message):
    token = os.environ.get('TG_TOKEN')
    chat_id = os.environ.get('TG_CHAT_ID')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={'chat_id': chat_id, 'text': message})

if __name__ == "__main__":
    check_site()
