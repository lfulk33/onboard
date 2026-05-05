import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_serper_results(query):
    serper_api_key =  os.getenv("SERPER_API_KEY")
    serper_url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }    

    payload = {
        "q": query,
    }

    response = requests.post(serper_url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["organic"]

if __name__ == "__main__":
    print(get_serper_results("\"Jack Widow Giant Spider\" Monster Halloween Prop"))