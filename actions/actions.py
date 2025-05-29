import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("location")

        if not city:
            dispatcher.utter_message(text="Please tell me the city name.")
            return []

        api_key = "777e2e2d91494291f58cd2738dc57e2e"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            dispatcher.utter_message(
                text=f"The weather in {city} is {description} with a temperature of {temp}°C."
            )
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't get the weather for {city}.")

        return []
