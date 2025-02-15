# user_conversation_agent.py

class UserConversationAgent:
    def __init__(self):
        self.user_data = {}

    def collect_user_input(self, form_data):
        """
        Collects user input data from a dictionary (e.g., from a form)
        and stores it.
        """
        self.user_data = form_data
        return self.user_data
