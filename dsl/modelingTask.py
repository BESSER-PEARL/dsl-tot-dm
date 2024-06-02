class ModelingTask():
    def __init__(self, level: int, name: str):
        self.level = level
        self.name = name
        self.description = ""
        self.assessment = []
    
    def set_description(self, description):
        self.description = description
    
    def add_assessment(self, criteria):
        self.assessment.append(criteria)

    def get_level(self) -> int: 
        return self.level
    
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_assessment(self):
        return self.assessment