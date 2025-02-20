import asyncio
import json
from getpass import getpass
from agents.user_conversation_agent import UserConversationAgent


def test_conversation_agent():
    """Test the conversation agent functionality"""
    try:
        # Initialize agent with API key
        api_key = "api_key"
        agent = UserConversationAgent(api_key)
        
        print("\nTesting initial question generation...")
        response = agent.collect_user_data()
        print(f"Initial question: {response['content']}")
        
        # Test with sample responses
        test_inputs = [
            "My budget is $50,000",
            "I'm located in California's Central Valley",
            "The soil is clay loam and we have good water access",
            "I have a tractor and basic farming equipment"
        ]
        
        for user_input in test_inputs:
            print(f"\nTesting user input: {user_input}")
            response = agent.collect_user_data(user_input)
            print(f"Agent response: {response['content']}")
            
        return "All tests completed successfully!"
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        raise

def main():
    """Main function to run the tests"""
    print("Starting Agricultural Conversation Agent tests...")
    try:
        response = test_conversation_agent()
        print(f"\n✓ {response}")
    except Exception as e:
        print(f"\n× Test failed with error: {str(e)}")
    finally:
        print("\nTest run completed.")

if __name__ == "__main__":
    main()
    
    