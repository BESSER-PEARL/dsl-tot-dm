import itertools
import numpy as np
from functools import partial
from tree_of_thought.llm import gpt
import logging
from os import mkdir
from os.path import exists, dirname, join
 
logger = logging.getLogger(__name__)
base_folder = dirname(dirname(__file__))
log_folder = join(base_folder, 'logs/')

def get_value(task, x, y, n_evaluate_sample, cache_value=True):
    value_prompt = task.value_prompt_wrap(x, y)
    if cache_value and value_prompt in task.value_cache:
        return task.value_cache[value_prompt]
    value_outputs = gpt(value_prompt, n=n_evaluate_sample, stop=None)
    value = task.value_outputs_unwrap(x, y, value_outputs)
    if cache_value:
        task.value_cache[value_prompt] = value
    return value

def get_values(task, x, ys, n_evaluate_sample, cache_value=True):
    values = []
    local_value_cache = {}
    for y in ys:  # each partial output
        if y in local_value_cache:  # avoid duplicate candidates
            value = 0
        else:    
            value = get_value(task, x, y, n_evaluate_sample, cache_value=cache_value)
            local_value_cache[y] = value
        values.append(value)
    return values

def get_votes(task, x, ys, n_evaluate_sample):
    vote_prompt = task.vote_prompt_wrap(x, ys)
    logger.info(f'Evaluator prompt: \n{vote_prompt}')
    vote_outputs = gpt(vote_prompt, n=n_evaluate_sample, stop=None)
    for i in range(len(vote_outputs)):
        logger.info(f'Evaluator {i+1}:\n {vote_outputs[i]}')
    values = task.vote_outputs_unwrap(vote_outputs, len(ys))
    for i in range(len(ys)):
        logger.info(f'Thought {i + 1}: {values[i]} votes')
    return values

def get_proposals(task, x, y): 
    propose_prompt = task.propose_prompt_wrap(x, y)
    proposals = gpt(propose_prompt, n=1, stop=None)[0].split('\n')
    return [y + _ + '\n' for _ in proposals]

def get_samples(task, x, y, n_generate_sample, prompt_sample):
    if prompt_sample == 'standard':
        prompt = task.standard_prompt_wrap(x, y)
    elif prompt_sample == 'cot':
        prompt = task.cot_prompt_wrap(x, y)
    else:
        raise ValueError(f'prompt_sample {prompt_sample} not recognized')
    logger.info(f'Generator prompt: \n{prompt}')
    samples = gpt(prompt, n=n_generate_sample)
    return samples

def solve(args, task, to_print=True, log_name = "test.log"):
    if not exists(log_folder):
        mkdir(log_folder)
    log_file = join(log_folder, log_name)
    logging.basicConfig(filename = log_file, filemode="a", level=logging.INFO)

    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    x = task.get_input()  # input
    ys = ['']  # current output candidates
    infos = []
    logger.info(f'Input:\n{x}')
    for step in range(task.steps):
        logger.info(f'Tree Level # {step + 1}')
        # generation
        if args.method_generate == 'sample':
            new_ys = [get_samples(task, x, y, args.n_generate_sample, prompt_sample=args.prompt_sample) for y in ys]
        elif args.method_generate == 'propose':
            new_ys = [get_proposals(task, x, y) for y in ys]
        new_ys = list(itertools.chain(*new_ys))
        ids = list(range(len(new_ys)))

        # evaluation
        if args.method_evaluate == 'vote':
            values = get_votes(task, x, new_ys, args.n_evaluate_sample)
        elif args.method_evaluate == 'value':
            values = get_values(task, x, new_ys, args.n_evaluate_sample)

        # selection
        if args.method_select == 'sample':
            ps = np.array(values) / sum(values)
            select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
        elif args.method_select == 'greedy':
            select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
        select_new_ys = [new_ys[select_id] for select_id in select_ids]
        logger.info(f'Selected thought:\n{select_new_ys[0]}')

        # log
        if to_print: 
            sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
            print(f'-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n')
        
        infos.append({'step': step, 'x': x, 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
        ys = select_new_ys
    
    if to_print: 
        print(ys)
    return ys, {'steps': infos}
