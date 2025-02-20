import pytest
from agents.main import AgriculturalAdvisor

def test_agricultural_advisor():
    api_key = "API_KEY"  # Replace with your actual API key
    advisor = AgriculturalAdvisor(api_key)
    
    test_responses = [
        "My budget is $50,000",
        "I'm located in California's Central Valley",
        "The soil is clay loam and we have good water access",
        "I have a tractor and basic farming equipment"
    ]
    
    results = advisor.process_user_input(test_responses)
    
    assert "user_data" in results
    assert "analysis" in results
    assert "recommendations" in results
    assert "farm_plan" in results
    assert "error" not in results

    # Test data structure
    assert "location" in results["user_data"]
    assert "budget" in results["user_data"]
    assert "soil_type" in results["user_data"] 