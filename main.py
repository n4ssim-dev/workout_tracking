from dotenv import load_dotenv
import os
import requests
from datetime import datetime

load_dotenv()

#env
APP_ID = os.getenv("N_APP_ID")
API_KEY = os.getenv("N_API_KEY")
SHEETY_ENDPOINT = os.getenv('SHEETY_ENDPOINT')
SHEETY_TOKEN = os.getenv('SHEETY_TOKEN')

#Urls
HOST_DOMAIN = 'https://trackapi.nutritionix.com'
API_ENDPOINT = '/v2/natural/exercise'

#GlobalScope
GENDER = "male"
WEIGHT = 79
HEIGHT = 174
AGE = 45

exercise_input = input("Quelles exercices as-tu fais ? :\n")

headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY
}

parameters = {
    "query": exercise_input,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "gender": GENDER,
    "age": AGE
}

response = requests.post(url=f'{HOST_DOMAIN}{API_ENDPOINT}', headers=headers, json=parameters)
data = response.json()

# ////// Ajouter une ligne au google sheet ///// #

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in data["exercises"]:
    bearer_headers = {
        "Authorization": f"Bearer {SHEETY_TOKEN}"
    }
    sheet_params = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(SHEETY_ENDPOINT, json=sheet_params,headers=bearer_headers)
    print(sheet_response.text)