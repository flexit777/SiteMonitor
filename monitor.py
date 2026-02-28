import requests
from bs4 import BeautifulSoup
import os
import pytz
from datetime import datetime

def check_site():
    # 1. SETUP
    url = "https://in.bookmyshow.com/cinemas/mumbai/miraj-cinemas-imax-wadala/buytickets/MCIW/20260319"
    target_movie = "dhurandhar" 
    
    # 2. "HUMANIZER" HEADERS (Bypassing the 403 Forbidden error)
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
        'Referer': 'https://in.bookmyshow.com/',
        'Connection': 'keep-alive'
    }
    
    try:
        # 3. THE REQUEST
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30)
        
        # 4. TIME LOGGING (For your Streamlit UI)
        IST = pytz.timezone('Asia/Kolkata')
        now = datetime.now(IST)
        current_time_str = now.strftime('%d %b %Y, %I:%M %p')
        
        # Write to last_check.txt for Streamlit
        with open("last_check.txt", "w") as f:
            f.write(f"{current_time_str} (Status: {response.status_code})")

        # 5. THE HEARTBEAT (Sends a daily "I'm alive" message at 10:00 AM IST)
        if now.hour == 10 and now.minute < 6: # Trigger once during the 10:00 AM window
            send_telegram_alert(f"☀️ Daily Heartbeat: Bot is running. (Last Status: {response.status_code})")

        # 6. SCRAPING LOGIC
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for the target movie in the page text
            found = soup.find_all(string=lambda text: target_movie.lower() in text.lower())

            if found:
                send_telegram_alert(f"🚨 TICKETS FOUND! '{target_movie}' detected at: {url}")
        
        # 7. BLOCK ALERT (Telegram will buzz if the website blocks the bot)
        elif response.status_code == 403:
            # send_telegram_alert(f"⚠️ Bot Blocked (403) at {current_time_str}. BookMyShow is fighting back!")
            print(f"Status 403: Access Denied by BookMyShow")

    except Exception as e:
        print(f"Error: {e}")

def send_telegram_alert(message):
    # Retrieve secrets from GitHub Settings
    token = os.environ.get('TG_TOKEN')
    chat_id = os.environ.get('TG_CHAT_ID')
    
    if token and chat_id:
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
        try:
            requests.post(tg_url, data=payload)
        except Exception as e:
            print(f"Telegram failed: {e}")

if __name__ == "__main__":
    check_site()
