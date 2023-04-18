#This file is not in use. Will be deprecated.

class Activity:
    def __init__(self, name, input_bindings, output_bindings):
        self.name = name
        self.input_bindings = input_bindings
        self.output_bindings = output_bindings

    def input_bindings(self):
        return self.input_bindings
    
    def output_bindings(self):
        return self.output_bindings
        
class CausalNet:
    def __init__(self, activities, start_activity, end_activity, dependencies):
        self.activities = activities
        self.start_activity = start_activity
        self.end_activity = end_activity
        self.dependencies = dependencies

    def input(activity):
        return activity.input_bindings()
    
    def output(activity):
        return activity.ouput_bindings()
    
    def generate_with_heuristic(self, heuristic_model):
        return