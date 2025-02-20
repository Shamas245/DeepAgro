from typing import Dict, Any, List, Optional, Tuple
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelPlatformType, ModelType, RoleType, TaskType
from camel.models import ModelFactory
from dataclasses import dataclass
import google.generativeai as genai
import json
import nest_asyncio
import os
import asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

@dataclass
class UserInput:
    budget: float
    location: str
    resources: Dict[str, Any]
    soil_type: str
    water_availability: str
    equipment: List[str]

class UserConversationAgent(ChatAgent):
    def __init__(self, api_key: str):
        # Set up Gemini API key
        os.environ["GOOGLE_API_KEY"] = "api_key"
        genai.configure(api_key=api_key)

        # Create system message
        system_message = BaseMessage.make_user_message(
            role_name="Agricultural Assistant",
            content="""You are an Agricultural User Conversation Agent specialized in gathering farming-related information."""
        )

        # Create the model
        model = ModelFactory.create(
            model_platform=ModelPlatformType.GEMINI,
            model_type=ModelType.GEMINI_1_5_PRO,
            model_config_dict={
                "temperature": 0.7,
            }
        )

        # Initialize ChatAgent with model
        super().__init__(
            system_message=system_message,
            model=model
        )
        
        self.conversation_history = []
        self.collected_data = {}
        self.required_fields = [
            "budget", "location", "soil_type", 
            "water_availability", "equipment"
        ]

    def start_conversation(self) -> str:
        """Start the conversation with a friendly greeting"""
        greeting = self.step(BaseMessage.make_user_message(
            role_name="Assistant",
            content="Introduce yourself as an agricultural advisor and ask about their farming goals."
        ))
        return str(greeting)

    def collect_user_data(self, user_input: str) -> Dict[str, Any]:
        """Process user input and ask relevant follow-up questions"""
        self.conversation_history.append(("user", user_input))
        
        # Analyze response and decide next question
        analysis_prompt = BaseMessage.make_user_message(
            role_name="Assistant",
            content=f"""Based on this conversation:
            {self._format_conversation_history()}
            
            1. Extract any relevant information about:
               - Location
               - Current farming situation
               - Goals and interests
               - Resources
               - Concerns
            2. Determine what important information is still missing
            3. Form a natural follow-up question
            
            Return as JSON with keys: 'extracted_info', 'missing_info', 'next_question'"""
        )
        
        response = self.step(analysis_prompt)
        analysis = json.loads(str(response))
        
        # Update collected data
        if analysis.get("extracted_info"):
            self.collected_data.update(analysis["extracted_info"])
        
        # Add response to history
        self.conversation_history.append(("assistant", analysis["next_question"]))
        
        return {
            "collected_data": self.collected_data,
            "next_question": analysis["next_question"],
            "missing_info": analysis.get("missing_info", [])
        }

    def _format_conversation_history(self) -> str:
        """Format conversation history for prompts"""
        return "\n".join(f"{role.upper()}: {content}" for role, content in self.conversation_history)

    def validate_response(self, field: str, value: str) -> Tuple[bool, Any]:
        """Validate user responses"""
        validation_prompt = BaseMessage.make_user_message(
            role_name="User",
            content=f"""Validate the following response for the field '{field}':
            Response: {value}
            
            Check if the response is:
            1. Appropriate for the field type
            2. Contains necessary information
            3. Is in a usable format"""
        )
        
        validation_result = self.step(validation_prompt)
        return json.loads(str(validation_result))

    def process_user_response(self, response: str) -> Dict[str, Any]:
        """Process user response"""
        processing_prompt = BaseMessage.make_user_message(
            role_name="User",
            content=f"""Process the following user response in the context of our conversation:
            Conversation history:
            {self._format_conversation_history()}
            
            Current response: {response}"""
        )
        
        processed_response = self.step(processing_prompt)
        return json.loads(str(processed_response))

