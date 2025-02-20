from typing import Dict, Any
from enum import Enum

class AgentRole(Enum):
    USER_CONVERSATION = "user_conversation"
    API_CALLER = "api_caller"
    SUMMARIZER = "summarizer"
    CROP_RECOMMENDER = "crop_recommender"
    PLANNER = "planner"
    DOCTOR = "doctor"

class BaseConfig:
    TEMPERATURE = 0.7
    MAX_TOKENS = 1500
    MODEL = "gpt-4"  # or your preferred model

class DataSchema:
    USER_INPUT_FIELDS = [
        "budget",
        "resources",
        "location",
        "soil_type",
        "water_availability",
        "equipment"
    ]

CONFIG: Dict[str, Any] = {
    "required_fields": ["location", "budget", "soil_type", "equipment"],
    "default_crops": ["cotton", "tomatoes", "almonds"],
    "min_budget": 10000,
    "supported_regions": ["California Central Valley", "Midwest", "Southeast"]
}