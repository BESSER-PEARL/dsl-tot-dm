#from dsl.modelingProblem import ModelingProblem
from dsl.modelingProblem import ModelingProblem
from dsl.modelingTask import ModelingTask
#from dsl.modelNotation import ModelNotation
from dsl.thought import Thought
import os
from dotenv import load_dotenv, find_dotenv
from dsl.prompts import GeneratorPrompt, EvaluatorPrompt
_ = load_dotenv(find_dotenv())

        
class Level():
    def __init__(self, id: int, previous_level = None):
        self.id = id
        self.task = ''
        self.thougths = []
        self.selected_thought = None
        self.previous_level = previous_level
        self.next_level = None
        self.modeling_problem = None
        self.generator_prompt = GeneratorPrompt(self.id)
        self.evaluator_prompt = EvaluatorPrompt(self.id)
    
    def set_next_level(self, task: ModelingTask):
        self.next_level = task

    def set_task(self, task: ModelingTask):
        self.task = task

    def add_thought(self, thought):
        self.thougths.append(thought)
    
    def set_selected_thought(self, thought):
        self.selected_thought = thought
    
    def get_id(self):
        return self.id
    
    def get_task(self) -> ModelingTask: 
        return self.task
    
    def get_thoughts(self):
        return self.thougths
    
    def get_selected_thought(self):
        return self.selected_thought
    
    def setup_prompts(self, modeling_problem: ModelingProblem):
        self.modeling_problem = modeling_problem
        self.generator_prompt.prompt()
        self.evaluator_prompt.prompt(0)

    def generate_prompt(self, prompt_name, thought = ''):
        prompt = ''
        if prompt_name == 'generator':
            prompt = self.generator_prompt.prompt()
            prompt = prompt.format(
                purpose=self.modeling_problem.get_purpose(), 
                domain=self.modeling_problem.get_domain_description(),
                tasks=self.modeling_problem.get_tasks(),
                thought = thought)
        if prompt_name == 'evaluator':
            prompt = self.evaluator_prompt.prompt(self.modeling_problem.get_assessment()[self.id-1]["nCriterias"])
            prompt = prompt.format(
                purpose=self.modeling_problem.get_purpose(), 
                domain=self.modeling_problem.get_domain_description(),
                assessment=self.modeling_problem.get_assessment())
        return prompt
