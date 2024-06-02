import os
import re
from tot.tasks.base import Task

class DMToTTask(Task):
    def __init__(self, levels, tree, problem):
        super().__init__()
        self.tree = tree
        self.data = problem.get_domain_description()
        self.steps = levels
        
    
    def __len__(self) -> int:
        return len(self.data)
    
    def get_input(self) -> str:
        return self.data
    
    def standard_prompt_wrap(self, x: str, y:str='') -> str:
        generator_prompt = self.tree.get_current_level().generate_prompt("generator", thought=y)
        return generator_prompt 
        
    def vote_prompt_wrap(self, x: str, ys: list) -> str:
        evaluator_prompt = self.tree.get_current_level().generate_prompt("evaluator")
        for i, y in enumerate(ys, 1):
            evaluator_prompt += f'\nChoice {i}:\n{y}\n'
        self.tree.increment_level()
        return evaluator_prompt

    @staticmethod
    def vote_outputs_unwrap(vote_outputs: list, n_candidates: int) -> list:
        vote_results = [0] * n_candidates
        for vote_output in vote_outputs:
            pattern = r".*best choice is .*(\d+).*"
            match = re.match(pattern, vote_output, re.DOTALL)
            if match:
                vote = int(match.groups()[0]) - 1
                if vote in range(n_candidates):
                    vote_results[vote] += 1
            else:
                print(f'vote no match: {[vote_output]}')
        return vote_results
