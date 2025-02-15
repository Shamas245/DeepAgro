# summarizer_agent.py

class SummarizerAgent:
    def __init__(self):
        self.data = {}

    def aggregate_data(self, user_data, api_data):
        """Aggregates user and API data into one dictionary."""
        self.data = {
            "user": user_data,
            "api": api_data
        }
        return self.data

    def get_summary(self):
        return self.data
