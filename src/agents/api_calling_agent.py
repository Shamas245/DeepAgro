from typing import Dict, Any, Optional
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
import google.generativeai as genai
import json
import os
import requests

class APICallingAgent(ChatAgent):
    def __init__(self, api_key: str):
        # Set up Gemini API key
        os.environ["GOOGLE_API_KEY"] = "api_key"
        genai.configure(api_key=api_key)

        # Create system message
        system_message = BaseMessage.make_user_message(
            role_name="API Agent",
            content="""You are an Agricultural API Agent that fetches and analyzes data from multiple sources."""
        )

        # Create the model
        model = ModelFactory.create(
            model_platform=ModelPlatformType.GEMINI,
            model_type=ModelType.GEMINI_1_5_PRO,
            model_config_dict={
                "temperature": 0.7,
            }
        )

        super().__init__(
            system_message=system_message,
            model=model
        )

    def fetch_weather_data(self, location: str) -> Dict[str, Any]:
        """Fetch weather and climate data"""
        try:
            # Simulated weather data for testing
            weather_data = {
                "current_weather": {
                    "temperature": 25,
                    "humidity": 65,
                    "precipitation": 0.2
                },
                "climate_patterns": {
                    "avg_rainfall": 750,
                    "growing_season": "March to September",
                    "climate_zone": "Mediterranean"
                }
            }
            return weather_data
        except Exception as e:
            print(f"Weather data fetch error: {str(e)}")
            return {}

    def fetch_economic_trends(self, crop_types: list) -> Dict[str, Any]:
        """Fetch economic trends from World Bank"""
        try:
            # Fetch World Bank agricultural data
            response = requests.get(
                "https://api.worldbank.org/v2/topic/1/indicator/AG.PRD.CROP.XD?format=json"
            )
            worldbank_data = response.json()

            # Simulated social trends for testing
            social_trends = {
                "trending_crops": crop_types,
                "market_sentiment": "positive",
                "price_trends": "stable"
            }

            return {
                "social_trends": social_trends,
                "market_data": worldbank_data
            }
        except Exception as e:
            print(f"Economic data fetch error: {str(e)}")
            return {}

    def analyze_location_data(self, location: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze location-specific agricultural data"""
        # Problem: No validation of location string
        if not location or not isinstance(location, str):
            return {
                "error": "Invalid location provided",
                "location": location
            }
        
        weather_data = self.fetch_weather_data(location)
        
        # Extract potential crops based on location and conditions
        analysis_prompt = BaseMessage.make_user_message(
            role_name="Analyst",
            content=f"""Based on the following data:
            Location: {location}
            Weather: {json.dumps(weather_data, indent=2)}
            User Resources: {json.dumps(user_data, indent=2)}
            
            Identify potential crop types suitable for this location.
            Consider climate patterns, soil type, and available resources.
            Return as a JSON list of crop names."""
        )
        
        crop_analysis = self.step(analysis_prompt)
        potential_crops = json.loads(str(crop_analysis))
        
        # Fetch economic data for identified crops
        economic_data = self.fetch_economic_trends(potential_crops)
        
        return {
            "location": location,
            "weather_data": weather_data,
            "economic_data": economic_data,
            "potential_crops": potential_crops
        }
            