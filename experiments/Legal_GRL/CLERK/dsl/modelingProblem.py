from dsl.input import Input
from dsl.modelingTask import ModelingTask
from dsl.modelNotation import ModelNotation
import re
regex_path = r'(\/.*?\.[\w:]+)'

class ModelingProblem():
    def __init__(self, levels, input, purpose = 'UML Class diagram'):
        self.modelingTasks = ['']*(levels)
        self.assessment = ['']*(levels)  
        self.modelNotation = {}
        input_values = input.get_inputs_values()
        self.domain_description = input_values[0][1]
        self.modeling_purpose = purpose
        self.input = input
        self.focus_actors = [i[1] for i in input_values[1:]]
        
    def get_purpose(self):
        #print("get_purpose()", [self.modeling_purpose] + self.focus_purpose)
        #return [self.modeling_purpose] + self.focus_purpose
        return self.modeling_purpose
        #if self.focus_purpose is None:
        #    return [self.modeling_purpose]
        #else:
        #    return self.modeling_purpose, self.focus_purpose
    """
    Generate Legal GRL models from law articles.
    The focus of the model is: Ignore the gas related regulation.
    Create the model from the perspective of focal actors: Tax Authority and Consumer.

    """
    
    def get_domain_description(self):
        return self.domain_description

    def get_input(self):
        return self.input
    
    def add_task(self, task: ModelingTask):
        level = task.get_level() - 1
        self.modelingTasks[level] = {"Name": task.get_name(), "Purpose": task.get_description()}
        self.assessment[level] = {"Name": task.get_name(), "Criteria": [], "nCriterias": 0}
        for a in task.get_assessment():
            self.assessment[level]["Criteria"].append(a)
            self.assessment[level]["nCriterias"] += 1

    def get_task(self, level):
        return self.modelingTasks[level]
    
    def get_tasks(self):
        return self.modelingTasks
    
    def get_assessment(self):
        return self.assessment
    
    def get_notation(self):
        return self.modelNotation

    def add_notation(self, notation: ModelNotation):
        self.modelNotation = {"Name": notation.get_name(), "Purpose": notation.get_description()}
    