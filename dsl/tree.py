
import argparse
from tree_of_thought.search import solve
from tree_of_thought.task import DMToTTask
from dsl.modelingProblem import ModelingProblem
from dsl.level import Level
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) 

api_source = os.getenv("OPENAI_API_TYPE")

class Tree():
    def __init__(self, number_levels, generator_samples, evaluator_votes):
        self.generator_samples = generator_samples
        self.evaluator_votes = evaluator_votes
        self.number_levels = number_levels
        self.levels = []
        self.current_level = 1
        self.modeling_problem = None

    def setup_tree(self):
        previous_level = None
        for i in range(self.number_levels):
            current_level = Level(i + 1,previous_level)
            current_level.set_task(self.modeling_problem.get_task(i))
            current_level.setup_prompts(self.modeling_problem)
            self.levels.append(current_level)
            previous_level = current_level
        for i in range(self.number_levels - 1):
            self.levels[i].set_next_level(self.levels[i+1])
        
    def get_current_level(self):
        return self.levels[self.current_level - 1]
       
    def set_initial_level(self):
        self.current_level = 1
    
    def increment_level(self):
        self.current_level += 1

    def set_input(self, problem: ModelingProblem):
        self.modeling_problem = problem
    
    def execute(self, logName=''):
        self.set_initial_level()
        api_source = os.getenv("OPENAI_API_TYPE")
        model_name = ""
        if api_source == "azure":
            model_name = os.getenv("AZURE_DEPLOYMENT_NAME")
        elif api_source == "openai":
            model_name = os.getenv("OPENAI_MODEL_NAME")
        args = argparse.Namespace(backend= model_name, temperature=0.7, task='DM', naive_run=False, 
                                  prompt_sample='standard', method_generate='sample', method_evaluate='vote', method_select='greedy', 
                                  n_generate_sample=self.generator_samples, n_evaluate_sample=self.evaluator_votes, n_select_sample=1)
        task = DMToTTask(self.number_levels, self, self.modeling_problem)
        ys, infos = solve(args, task, True, logName)
        return ys[0]

