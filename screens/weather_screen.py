# screens/weather_screen.py
import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
import threading

from config import weather_api_key


# Function to fetch weather data
def fetch_weather_data(location):
    api_key = weather_api_key
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"

    response = requests.get(base_url)
    if response.status_code == 404:
        return {"status": "error"}
    else:
        data = response.json()
        temp = {
            "celcius": round(data["main"]["temp"] - 273.15, 2),
            "fahrenheit": round((data["main"]["temp"] - 273.15) * 9 / 5 + 32, 2),
            "status": "success",
        }
        return temp

class WeatherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Input field
        self.input_field = TextInput(hint_text='Enter location', size_hint_y=None, height=50)
        layout.add_widget(self.input_field)

        # Submit button
        submit_button = Button(text='Submit', size_hint_y=None, height=50)
        submit_button.bind(on_press=self.show_weather_data)
        layout.add_widget(submit_button)

        # Image to display weather condition
        self.weather_image = AsyncImage(source='', size_hint_y=None, height=400)
        layout.add_widget(self.weather_image)

        # Label to display weather data
        self.weather_label = Label(text='', size_hint_y=0.7)
        layout.add_widget(self.weather_label)

        self.add_widget(layout)

    def show_weather_data(self, instance):
        location = self.input_field.text

        # Show loading popup
        loading_popup = Popup(title='Loading...', content=Label(text='Fetching weather data'), size_hint=(None, None),
                              size=(400, 200))
        loading_popup.open()

        # Fetch weather data in a separate thread
        threading.Thread(target=self.fetch_weather_data_thread, args=(location, loading_popup)).start()

    def fetch_weather_data_thread(self, location, loading_popup):
        # Fetch weather data
        weather_data = fetch_weather_data(location)

        # Close loading popup
        loading_popup.dismiss()

        if weather_data["status"] == "success":
            # Display weather data
            self.weather_label.text = f'Temperature at {location} is {weather_data["celcius"]}°C'

            # Set weather image based on temperature
            if weather_data["celcius"] > 30:
                self.weather_image.source = "assets/images/hot.jpg"
            elif weather_data["celcius"] < 10 and weather_data["celcius"] > 0:
                self.weather_image.source = "assets/images/cool.jpg"
            elif weather_data["celcius"] < 30 and weather_data["celcius"] > 10:
                self.weather_image.source = "assets/images/normal.jpg"
            elif weather_data["celcius"] < 0:
                self.weather_image.source = "assets/images/cold.jpg"
            else:
                self.weather_image.source = "assets/images/confused.png"
        else:
            self.weather_label.text = "Error fetching data"
            self.weather_image.source = ''  # Clear image source if error occurs
