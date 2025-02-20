from typing import Dict, Any, List
from agents.user_conversation_agent import UserConversationAgent
from agents.api_calling_agent import APICallingAgent
from agents.summarizer_agent import SummarizerAgent
from agents.best_crop_recommendation_agent import BestCropRecommendationAgent
from agents.planning_agent import PlanningAgent
import json
import os

class AgriculturalAdvisor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.conversation_agent = UserConversationAgent(api_key)
        self.api_agent = APICallingAgent(api_key)
        self.summarizer = SummarizerAgent(api_key)
        self.recommendation_agent = BestCropRecommendationAgent(api_key)
        self.planning_agent = PlanningAgent(api_key)
        
    def start_consultation(self) -> str:
        """Start the agricultural consultation"""
        return self.conversation_agent.start_conversation()

    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """Process each user response and provide next steps"""
        try:
            # Get next question and extracted data
            conversation_result = self.conversation_agent.collect_user_data(user_input)
            
            # If we have location, get external data
            if "location" in conversation_result["collected_data"]:
                location = conversation_result["collected_data"]["location"]
                weather_data = self.api_agent.fetch_weather_data(location)
                economic_data = self.api_agent.fetch_economic_trends(["rice", "wheat", "corn", "soybeans"])
                
                # Summarize available data
                summarized_data = self.summarizer.aggregate_data(
                    user_data=conversation_result["collected_data"],
                    weather_data=weather_data,
                    economic_data=economic_data
                )
                
                # If we have enough information, provide recommendations
                if not conversation_result["missing_info"]:
                    recommendations = self.recommendation_agent.recommend_crops(summarized_data)
                    farm_plan = self.planning_agent.create_farm_plan(recommendations, summarized_data)
                    
                    return {
                        "type": "final_recommendation",
                        "recommendations": recommendations,
                        "farm_plan": farm_plan,
                        "next_question": None
                    }
            
            # Continue conversation if we need more information
            return {
                "type": "question",
                "next_question": conversation_result["next_question"],
                "missing_info": conversation_result["missing_info"]
            }

        except Exception as e:
            return {"error": str(e)}

def main():
    api_key = os.getenv("GOOGLE_API_KEY", "API_KEY")
    advisor = AgriculturalAdvisor(api_key)
    
    # Start conversation
    print("\nAdvisor:", advisor.start_consultation())
    
    # Interactive loop
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
            
        result = advisor.process_user_input(user_input)
        
        if result.get("error"):
            print("\nError:", result["error"])
            break
            
        if result["type"] == "question":
            print("\nAdvisor:", result["next_question"])
        else:
            print("\nRecommendations:", json.dumps(result["recommendations"], indent=2))
            print("\nFarm Plan:", json.dumps(result["farm_plan"], indent=2))
            break

if __name__ == "__main__":
    main()
