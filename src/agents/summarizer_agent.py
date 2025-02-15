# summarizer_agent.py

class SummarizerAgent:
    def __init__(self):
        self.data = {}

    def aggregate_data(self, user_data, api_data):
        """
        Aggregates data from user inputs and API calls into a single dictionary.
        """
        self.data = {
            "user": user_data,
            "api": api_data
        }
        return self.data

    def get_summary(self):
        return self.data
