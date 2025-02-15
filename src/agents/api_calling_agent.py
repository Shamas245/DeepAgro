# api_calling_agent.py

import requests
import random

class APICallingAgent:
    def __init__(self):
        # Replace these with your actual API keys
        self.world_bank_api_key = "YOUR_WORLD_BANK_API_KEY"
        self.trading_economics_api_key = "YOUR_TRADING_ECONOMICS_API_KEY"
        self.weather_api_key = "YOUR_WEATHER_API_KEY"
        self.climate_api_key = "YOUR_CLIMATE_API_KEY"
    
    def fetch_economic_data(self, location):
        # Simulated API call to fetch economic insights
        economic_data = {
            "average_income": random.uniform(2000, 5000),
            "crop_prices": {
                "Wheat": random.uniform(2.0, 5.0),
                "Corn": random.uniform(1.5, 4.0),
                "Soybean": random.uniform(3.0, 6.0),
                "Rice": random.uniform(2.5, 5.5),
                "Barley": random.uniform(2.0, 4.5)
            }
        }
        return economic_data

    def fetch_environmental_data(self, location):
        # Simulated API call to fetch environmental insights
        environmental_data = {
            "temperature": random.uniform(15, 35),
            "rainfall": random.uniform(0, 200),
            "humidity": random.uniform(30, 90)
        }
        return environmental_data

    def get_all_api_data(self, location):
        economic_data = self.fetch_economic_data(location)
        environmental_data = self.fetch_environmental_data(location)
        return {"economic": economic_data, "environmental": environmental_data}
