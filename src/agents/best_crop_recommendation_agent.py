# best_crop_recommendation_agent.py

from typing import Dict, Any, List
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
import google.generativeai as genai
import json
import os

class BestCropRecommendationAgent(ChatAgent):
    def __init__(self, api_key: str):
        # Set up Gemini API key
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)

        # Create system message
        system_message = BaseMessage.make_user_message(
            role_name="Crop Advisor",
            content="""You are an Agricultural Crop Recommendation Expert that analyzes farm conditions and suggests optimal crops."""
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

    def recommend_crops(self, summarized_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate crop recommendations based on summarized data"""
        
        recommendation_prompt = BaseMessage.make_user_message(
            role_name="Advisor",
            content=f"""Analyze the following agricultural data and recommend optimal crops:
            
            {json.dumps(summarized_data, indent=2)}
            
            Consider:
            1. Environmental conditions (weather, soil, water)
            2. Economic trends and market demand
            3. Available resources and equipment
            4. Location-specific factors
            
            Provide recommendations including:
            1. Top recommended crops
            2. Expected yield potential
            3. Resource requirements
            4. Risk factors
            5. Economic potential
            
            Return as a structured JSON object."""
        )
        
        try:
            recommendations = self.step(recommendation_prompt)
            return json.loads(str(recommendations))
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse recommendations",
                "raw_response": str(recommendations)
            }

    def get_crop_details(self, crop_name: str, farm_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed information about a specific crop's suitability"""
        
        analysis_prompt = BaseMessage.make_user_message(
            role_name="Crop Specialist",
            content=f"""Analyze the suitability of {crop_name} for the following conditions:
            
            {json.dumps(farm_conditions, indent=2)}
            
            Provide detailed analysis including:
            1. Growing requirements
            2. Expected challenges
            3. Management recommendations
            4. Economic considerations
            
            Return as a structured JSON object."""
        )
        
        crop_analysis = self.step(analysis_prompt)
        return json.loads(str(crop_analysis))
