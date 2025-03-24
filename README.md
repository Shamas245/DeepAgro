# DeepAgro - Intelligent Agricultural Advisory System

## Overview
DeepAgro is a sophisticated multi-agent system that leverages CAMEL AI and Google's Generative AI to provide intelligent agricultural recommendations. The system analyzes farm conditions, environmental data, and economic trends to suggest optimal crops and create detailed farming plans.

## Features
- 🤖 Multi-agent architecture for specialized tasks
- 🌱 Personalized crop recommendations
- 📊 Environmental and economic data analysis
- 📋 Detailed farming plan generation
- 💬 Interactive user data collection

## System Architecture

### Core Agents
1. **User Conversation Agent**
   - Handles user interaction
   - Collects farm-specific information
   - Validates user inputs

2. **API Calling Agent**
   - Fetches weather data
   - Retrieves economic trends
   - Analyzes market conditions

3. **Summarizer Agent**
   - Combines data from multiple sources
   - Analyzes farm conditions
   - Generates comprehensive summaries

4. **Best Crop Recommendation Agent**
   - Suggests optimal crops
   - Analyzes crop suitability
   - Considers multiple factors

5. **Planning Agent**
   - Creates detailed farming plans
   - Provides resource allocation
   - Develops implementation strategies

## Installation

### Prerequisites
- Python 3.10+

### Setup
1. Clone the repository
2. Install dependencies:

3. Set up API key:
   - Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Replace "API_KEY" with your key in the code

## Usage

```python
from agents.main import AgriculturalAdvisor

# Initialize
advisor = AgriculturalAdvisor(api_key="YOUR_API_KEY")

# Test inputs
responses = [
    "My budget is $50,000",
    "I'm located in California's Central Valley",
    "The soil is clay loam and we have good water access",
    "I have a tractor and basic farming equipment"
]

# Get recommendations
results = advisor.process_user_input(responses)
print(results)
```

## Project Structure
```
src/agents/
├── main.py                      # Main orchestration
├── user_conversation_agent.py    # User interaction
├── api_calling_agent.py          # External data fetching
├── summarizer_agent.py           # Data analysis
├── best_crop_recommendation_agent.py # Crop suggestions
├── planning_agent.py             # Plan generation
└── tests/
    └── test_agricultural_advisor.py # Test suite
```

## Testing
Run the test suite:
```bash
pytest src/agents/tests/
```

Run type checking:
```bash
mypy --ignore-missing-imports src/agents/
```

## LICENCE
This project is licensed under the MIT License.

## Notes
This README provides:
- A clear project overview
- Installation instructions
- Usage examples
- Project structure details
- Testing instructions

Feel free to contribute and improve the project!

