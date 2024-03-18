import os
from dotenv import dotenv_values

"""
weather_api_key = os.getenv("WEATHER_API_KEY")

"""
env = dotenv_values(".env")
weather_api_key = env["WEATHER_API_KEY"]
