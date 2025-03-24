
from tree_of_thought.llm import gpt
from functools import partial
import logging
import os
from os import mkdir
from os.path import exists, dirname, join
 
logger = logging.getLogger(__name__)
base_folder = dirname(dirname(__file__))
log_folder = join(base_folder, 'logs/')

api_source = os.getenv("OPENAI_API_TYPE")
model_name = ""
if api_source == "azure":
    model_name = os.getenv("AZURE_DEPLOYMENT_NAME")
elif api_source == "openai":
    model_name = os.getenv("OPENAI_MODEL_NAME")

class GeneratorPrompt():
    def __init__(self, current_level: int):
        self.current_level = current_level
        
    def prompt(self):
        prompt = 'You are a domain modeling expert that creates a domain model with a given purpose:\n{purpose}\n\n'
        prompt += 'The model is created using the following domain:\n{domain}\n\n'
        tasks = f"Your task is to {{tasks[{self.current_level - 1}][Name]}}: \n{{tasks[{self.current_level - 1}][Purpose]}}\n"
        prompt += tasks
        prompt += "\nTo generate a new proposal, you apply some changes to the proposal below and then return the modified elements:\n"
        prompt += "{thought}\n"
        prompt += "\nYour output is a new proposal that meets the following format:\n"
        tasks = [f"\n{{tasks[{i}][Name]}}: \nThe {{tasks[{i}][Name]}} here." for i in range(self.current_level)]
        prompt += "\n".join(tasks)  
        return prompt

class EvaluatorPrompt():
    def __init__(self, current_level: int):
        self.current_level = current_level

    def prompt(self, nCriterias):
        prompt = 'You are a domain modeling expert that decides which choice is the best model.\n'
        prompt +='The domain model has the following purpose:\n{purpose}\n'
        prompt +='You Analyze each choice in detail, then conclude in the last line "The best choice is {{s}}", where s the integer id of the choice.\n'
        prompt +='You always pay extra attention at the following criterias:\n'
        tasks = [f"\n{i+1}. {{assessment[{self.current_level-1}][Criteria][{i}]}}" for i in range(nCriterias)]
        prompt += "".join(tasks)        
        prompt += "\n\nThe domain description is:\n{domain}\n"
        return prompt


class NotationPrompt():
    def __init__(self, purpose, domain, thought, notation):
        self.purpose = purpose
        self.domain = domain
        self.thought = thought
        self.notation = notation
        
    def prompt(self):
        prompt = 'Domain Modeling is the exercise of building conceptual models from a textual domain description to explicitly represent the knowledge of domain provided by the description.\n'
        prompt += f'You are a domain modeling expert for {self.purpose} that creates a domain model from a given description:\n{self.domain}\n'
        prompt += "\nYou use the thoughts below to return the specified domain model:\n"
        prompt += f"{self.thought}\n"
        tasks = f"You create the {self.notation['Name']}: \n{self.notation['Purpose']}\n"
        prompt += tasks
        return prompt
    
    def execute(self, log_name):
        log_file = join(log_folder, log_name)
        logging.basicConfig(filename = log_file, filemode="a", level=logging.INFO)
        global gpt
        gpt = partial(gpt, model=model_name)
        prompt = self.prompt()
        logger.info(f'Notation prompt: \n{prompt}')
        model_notation = gpt(prompt, n=1)
        logger.info(f'Model notation:\n{model_notation[0]}')
        return model_notation