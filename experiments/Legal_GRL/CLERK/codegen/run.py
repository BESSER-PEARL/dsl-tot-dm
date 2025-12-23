from os import mkdir
from os.path import exists, dirname, join
from textx import metamodel_from_file
import jinja2
import argparse
import json

import subprocess

current_folder = dirname(__file__)
mmodel_folder = join(current_folder, 'dsl/')
model_folder = join(current_folder, 'models/')
template_folder = join(current_folder, 'dsl/')
input_folder = join(current_folder, 'input')
output_folder = join(current_folder, '')

def run(args):   
    mm = metamodel_from_file(mmodel_folder + 'dsl_grammar.tx')
    model = mm.model_from_file(model_folder + args.model)

    input_data = {}
    for input in model.inputs:
        input_name = format_arg_names(input.name)
        print(f"Input arg name:\n{input_name}, Optional: {input.isOptional}")
        input_data[input_name] =  input.isOptional

    print("Tree:",len(model.tasks))
    for level, task in enumerate(model.tasks):
        print(f"Level: {level} Task: {task.name}")
        print("#Assessments:", len(task.assessments))
    if model.notation is None:
        print("Model Notation not specified. Step not executed." )
    else:
        print("Model Notation:", model.notation.name)

    if not exists(output_folder):
        mkdir(output_folder)

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    template = jinja_env.get_template('py_template.template')

    with open(join(output_folder, "%s.py" % "clerk"), 'w') as f:
        log_name=args.model.replace(".dmtot", ".log")
        f.write(template.render(model=model, input_data = input_data, log_name = log_name))

def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--model', type=str, required=True, default='domain_model.dmtot')
    args = args.parse_args()
    return args

def format_arg_names(name):
    return name.replace(" ","_")

if __name__ == '__main__':
    args = parse_args()
    print(args)
    run(args)