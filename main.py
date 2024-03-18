# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.weather_screen import WeatherScreen


class WeatherApp(App):
    def build(self):
        # Screen manager
        sm = ScreenManager()

        # Add WeatherScreen
        sm.add_widget(WeatherScreen(name='weather'))

        return sm


if __name__ == '__main__':
    WeatherApp().run()
