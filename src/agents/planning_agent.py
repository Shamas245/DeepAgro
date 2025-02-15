# planning_agent.py

class PlanningAgent:
    def provide_plan(self, summarized_data, selected_crop, additional_input=None):
        """
        Provides a sustainable growing plan for the selected crop.
        Additional input can be used to customize the plan further.
        """
        plan = f"Sustainable Growing Plan for {selected_crop}:\n"
        plan += "1. Optimize water usage based on local rainfall patterns.\n"
        plan += "2. Use organic fertilizers and integrated pest management.\n"
        plan += "3. Rotate crops to maintain soil fertility.\n"
        if additional_input:
            plan += f"\nAdditional considerations: {additional_input}\n"
        return plan
