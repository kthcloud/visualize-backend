import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def start(update_state):
    while True:
        response = requests.get(f'{os.getenv("API_URL")}/landing/v2/status?n=100')
        update_state(response.json())
        time.sleep(10)