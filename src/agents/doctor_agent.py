# doctor_agent.py

import random

class DoctorAgent:
    def diagnose_plant(self, plant_image, context_data):
        """
        Analyzes a plant image (dummy simulation) and returns a diagnosis.
        Replace with real API calls for actual diagnosis if available.
        """
        if not plant_image:
            return "No image provided. Unable to diagnose."
        
        # Simulate a diagnosis using a random health score.
        health_score = random.randint(40, 100)
        if health_score > 70:
            diagnosis = "The plant appears healthy. No significant issues detected."
        else:
            diagnosis = "The plant shows signs of stress. Consider checking soil nutrients and water availability."
        return diagnosis
