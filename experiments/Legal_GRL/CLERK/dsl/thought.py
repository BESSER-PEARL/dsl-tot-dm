class Thought():
    def __init__(self, thought: str, previous_thought = None):
        self.thought = thought
        self.previous_thought = previous_thought
        self.child_thought = None
    
    def set_child_thought(self, thought: str):
        self.child_thought = thought

    def get_thought(self) -> str:
        return self.thought
    