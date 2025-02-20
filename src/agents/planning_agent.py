# planning_agent.py

from typing import Dict, Any, List
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
import google.generativeai as genai
import json
import os

class PlanningAgent(ChatAgent):
    def __init__(self, api_key: str):
        # Set up Gemini API key
        os.environ["GOOGLE_API_KEY"] = "api_key"
        genai.configure(api_key=api_key)

        # Create system message
        system_message = BaseMessage.make_user_message(
            role_name="Farm Planner",
            content="""You are an Agricultural Planning Expert that creates detailed farming plans based on recommendations and data."""
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

    def create_farm_plan(self, recommendations: Dict[str, Any], summarized_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a detailed farming plan based on recommendations and data"""
        try:
            planning_prompt = BaseMessage.make_user_message(
                role_name="Planner",
                content=f"""Create a detailed farming plan based on:
                
                Recommendations: {json.dumps(recommendations, indent=2)}
                Farm Data: {json.dumps(summarized_data, indent=2)}
                
                Include in the plan:
                1. Timeline and schedule
                2. Resource allocation
                3. Implementation steps
                4. Risk management strategies
                5. Budget allocation
                6. Monitoring and evaluation plan
                
                Return as a structured JSON object."""
            )
            
            plan_response = self.step(planning_prompt)
            return json.loads(str(plan_response))
        except json.JSONDecodeError:
            return {
                "error": "Failed to generate plan",
                "raw_response": str(plan_response)
            }

    def get_phase_details(self, plan: Dict[str, Any], phase: str) -> Dict[str, Any]:
        """Get detailed information about a specific planning phase"""
        try:
            phase_prompt = BaseMessage.make_user_message(
                role_name="Phase Planner",
                content=f"""Provide detailed breakdown of the {phase} phase:
                
                Overall Plan: {json.dumps(plan, indent=2)}
                
                Include:
                1. Specific tasks and subtasks
                2. Required resources
                3. Timeline
                4. Success criteria
                5. Potential challenges
                
                Return as a structured JSON object."""
            )
            
            phase_response = self.step(phase_prompt)
            return json.loads(str(phase_response))
        except json.JSONDecodeError:
            return {
                "error": f"Failed to get details for phase: {phase}",
                "raw_response": str(phase_response)
            }
