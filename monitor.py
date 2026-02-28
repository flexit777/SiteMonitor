import requests
import os
import pytz
from datetime import datetime

def check_site():
    url = "https://in.bookmyshow.com/cinemas/mumbai/miraj-cinemas-imax-wadala/buytickets/MCIW/20260319"
    keyword = "scream"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        # Get India Time for the log
        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST).strftime('%d %b %Y, %I:%M %p')
        
        # Write the time to our status file
        with open("last_check.txt", "w") as f:
            f.write(current_time)

        # Look for your trigger word
        if keyword.lower() in response.text.lower():
            send_telegram_alert(f"🚨 TICKETS FOUND! '{keyword}' is on the page: {url}")
            
    except Exception as e:
        print(f"Error checking site: {e}")

def send_telegram_alert(message):
    token = os.environ.get('TG_TOKEN')
    chat_id = os.environ.get('TG_CHAT_ID')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(url)

if __name__ == "__main__":
    check_site()
