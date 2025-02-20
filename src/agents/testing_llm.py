import os
import google.generativeai as genai
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import (
    ModelPlatformType,
    ModelType,
    RoleType,
    TaskType
)
from camel.models import ModelFactory
import asyncio
import json

def create_test_agent():
    """Create and configure a test chat agent"""
    try:
        # Set up Gemini API key
        api_key = ""
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)

        # Define the model
        model = ModelFactory.create(
            model_platform=ModelPlatformType.GEMINI,
            model_type=ModelType.GEMINI_1_5_PRO,
            model_config_dict={
                "temperature": 0.7,
            }
        )

        # Create a proper system message
        system_msg = BaseMessage.make_user_message(
            role_name="Assistant",
            content="You are a helpful AI assistant."
        )

        # Initialize the agent
        agent = ChatAgent(
            system_message=system_msg,
            model=model
        )
        
        return agent
    except Exception as e:
        print(f"Error creating agent: {str(e)}")
        raise

async def test_agent_response():
    """Test the agent with a simple query"""
    try:
        agent = create_test_agent()
        
        # Test with a simple query
        query = "What is the capital of France?"
        print(f"\nSending query: {query}")
        
        # Create a proper message object
        message = BaseMessage.make_user_message(
            role_name="User",
            content=query
        )
        
        response = agent.step(message)
        print(f"Agent response: {response}")
        
        return response
    except Exception as e:
        print(f"\n× Test failed with error: {str(e)}")
        raise

def main():
    """Main function to run the test"""
    print("Starting AI Agent test...")
    try:
        # Run the async test
        response = asyncio.run(test_agent_response())
        
        if response:
            print("\n✓ Test completed successfully!")
            print(f"Final response: {response}")
        else:
            print("\n× Test failed - no response received")
            
    except Exception as e:
        print(f"\n× Test failed with error: {str(e)}")
        raise
    finally:
        print("\nTest run completed.")

if __name__ == "__main__":
    main()
    main()