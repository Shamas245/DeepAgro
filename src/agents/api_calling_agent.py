from typing import Dict, Any
from camel.agents import ChatAgent
from camel.typing import TaskType, RoleType
from config import BaseConfig
import aiohttp

class APICallingAgent(ChatAgent):
    def __init__(self):
        system_message = """You are an Agricultural API Calling Agent responsible for fetching and processing external data.

Your core responsibilities:
1. Fetch economic data:
   - Crop market prices
   - Agricultural commodity trends
   - Economic indicators
   - World Bank agricultural data
   - Trading Economics agricultural metrics

2. Fetch environmental data:
   - Weather forecasts
   - Climate patterns
   - Soil conditions
   - Water table information
   - Environmental risks

3. Data processing:
   - Clean and structure API responses
   - Handle API errors gracefully
   - Ensure data consistency
   - Format data for other agents

You must maintain data accuracy and handle rate limits appropriately.
Always validate API responses before passing data to other agents."""

        super().__init__(
            system_message=system_message,
            task_type=TaskType.API,
            role_type=RoleType.ASSISTANT,
            model_config={
                "temperature": BaseConfig.TEMPERATURE,
                "max_tokens": BaseConfig.MAX_TOKENS
            }
        )
        self.session = None
    
    async def initialize(self):
        self.session = aiohttp.ClientSession()
    
    async def fetch_economic_data(self, location: str) -> Dict[str, Any]:
        if not self.session:
            await self.initialize()
        
        # Implement API calls to World Bank and Trading Economics
        return {}
    
    async def fetch_weather_data(self, location: str) -> Dict[str, Any]:
        if not self.session:
            await self.initialize()
        
        # Implement weather API calls
        return {}
    
    async def close(self):
        if self.session:
            await self.session.close()
            