# summarizer_agent.py

from typing import Dict, Any, List, Optional
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
import google.generativeai as genai
import json
import os

class SummarizerAgent(ChatAgent):
    def __init__(self, api_key: str):
        # Set up Gemini API key
        os.environ["GOOGLE_API_KEY"] = "api_key"
        genai.configure(api_key=api_key)

        # Create system message
        system_message = BaseMessage.make_user_message(
            role_name="Summarizer",
            content="""You are an Agricultural Data Summarizer that analyzes and combines information from multiple sources."""
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
        
        self.summarized_data: Dict[str, Any] = {}

    def aggregate_data(self, user_data: Dict[str, Any], weather_data: Dict[str, Any], economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregates and analyzes data from multiple sources.
        
        Args:
            user_data: Data collected from user conversations
            weather_data: Weather forecasts and climate data
            economic_data: Economic trends and market data
        """
        # Problem: No validation of input data
        # Fix: Add validation
        if not user_data or not weather_data or not economic_data:
            return {
                "error": "Missing required data",
                "missing": [
                    k for k, v in {
                        "user_data": user_data,
                        "weather_data": weather_data,
                        "economic_data": economic_data
                    }.items() if not v
                ]
            }

        # Combine all data
        combined_data = {
            "user_information": user_data,
            "environmental_data": weather_data,
            "economic_trends": economic_data
        }
        
        # Create analysis prompt
        analysis_prompt = BaseMessage.make_user_message(
            role_name="Analyst",
            content=f"""Analyze and summarize the following agricultural data:
            
            User Information:
            {json.dumps(user_data, indent=2)}
            
            Weather Data:
            {json.dumps(weather_data, indent=2)}
            
            Economic Trends:
            {json.dumps(economic_data, indent=2)}
            
            Provide a comprehensive summary including:
            1. Key farm characteristics
            2. Environmental conditions and challenges
            3. Economic opportunities and risks
            4. Potential synergies between different factors
            
            Return the analysis as a structured JSON object."""
        )
        
        # Get analysis from model
        analysis_response = self.step(analysis_prompt)
        analyzed_data = json.loads(str(analysis_response))
        
        # Store the summarized data
        self.summarized_data = {
            "raw_data": combined_data,
            "analysis": analyzed_data
        }
        
        return self.summarized_data

    def get_summary(self, aspect: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve summarized data, optionally filtered by aspect.
        
        Args:
            aspect: Optional filter ('environmental', 'economic', or 'farm_characteristics')
        """
        if not self.summarized_data:
            return {"error": "No data has been analyzed yet"}
            
        if not aspect:
            return self.summarized_data
            
        if aspect in self.summarized_data.get("analysis", {}):
            return {aspect: self.summarized_data["analysis"][aspect]}
            
        return {"error": f"Aspect '{aspect}' not found in analysis"}

    def get_recommendations(self) -> Dict[str, Any]:
        """Generate recommendations based on summarized data"""
        if not self.summarized_data:
            return {"error": "No data available for recommendations"}
            
        recommendation_prompt = BaseMessage.make_user_message(
            role_name="Advisor",
            content=f"""Based on the following analyzed data:
            {json.dumps(self.summarized_data, indent=2)}
            
            Provide specific recommendations for:
            1. Crop selection and farming practices
            2. Resource management
            3. Risk mitigation strategies
            4. Economic optimization
            
            Return recommendations as a structured JSON object."""
        )
        
        recommendations = self.step(recommendation_prompt)
        return json.loads(str(recommendations))

    def export_data(self, format: str = "json") -> str:
        """Export summarized data in specified format"""
        if format.lower() == "json":
            return json.dumps(self.summarized_data, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
