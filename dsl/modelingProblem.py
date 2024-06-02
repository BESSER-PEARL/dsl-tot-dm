from dsl.modelingTask import ModelingTask
from dsl.modelNotation import ModelNotation
import re
regex_path = r'(\/.*?\.[\w:]+)'

class ModelingProblem():
    def __init__(self, levels, description, purpose = 'UML Class diagram'):
        self.modelingTasks = ['']*(levels)
        self.assessment = ['']*(levels)  
        self.modelNotation = {}
        
        if (len(re.findall(regex_path, description)) > 0):
            data = open(description).readlines()
            description = ''.join(data[:])
        self.domain_description = description
        self.modeling_purpose = purpose
        
    def get_purpose(self):
        return self.modeling_purpose
    
    def get_domain_description(self):
        return self.domain_description
    
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
    