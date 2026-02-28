import requests
import os
import pytz
from datetime import datetime

def check_site():
    target_date = "20260319"
    target_url = f"https://in.bookmyshow.com/cinemas/mumbai/miraj-cinemas-imax-wadala/buytickets/MCIW/{target_date}"
    movie_name = "dhurandhar"
    
    # YOUR SCRAPER API KEY (Get this for free from ScraperAnt or Scrape.do)
    # Put this in your GitHub Secrets as 'SCRAPER_API_KEY'
    api_key = os.environ.get('SCRAPER_API_KEY')
    
    # The API acts as a middleman to bypass the 403 error
    proxy_url = f"https://api.scraperant.com/v2/general?url={target_url}&x-api-key={api_key}"

    try:
        response = requests.get(proxy_url, timeout=60)
        
        # Log status for Streamlit
        IST = pytz.timezone('Asia/Kolkata')
        now = datetime.now(IST).strftime('%d %b %Y, %I:%M %p')
        with open("last_check.txt", "w") as f:
            f.write(f"{now} (Status: {response.status_code})")

        if response.status_code == 200:
            content = response.text.lower()
            if movie_name.lower() in content:
                send_telegram_alert(f"🚨 TICKETS FOUND! '{movie_name}' is live on {target_date}!\nLink: {target_url}")
            else:
                print(f"Checked at {now}: Not found yet.")
        else:
            print(f"API Error: {response.status_code}")

    except Exception as e:
        print(f"Request failed: {e}")

def send_telegram_alert(message):
    token = os.environ.get('TG_TOKEN')
    chat_id = os.environ.get('TG_CHAT_ID')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={'chat_id': chat_id, 'text': message})

if __name__ == "__main__":
    check_site()
