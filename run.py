from os import mkdir
from os.path import exists, dirname, join
from textx import metamodel_from_file
import jinja2
import argparse

import subprocess

current_folder = dirname(__file__)
mmodel_folder = join(current_folder, 'dsl/')
model_folder = join(current_folder, 'models/')
template_folder = join(current_folder, 'dsl/')
output_folder = join(current_folder, '')

def run(args):
      
    mm = metamodel_from_file(mmodel_folder + 'dsl_grammar.tx')

    model = mm.model_from_file(model_folder + args.model)

    print("Tree:",model.tree.levels)
    print("Modeling purpose:", model.problem.purpose)
    ordered_tasks = sorted(model.tasks, key=lambda x: x.level)
    for t in ordered_tasks:
        print(f"Level: {t.level} Task: {t.name}")
        print("#Assessments:", len(t.assessments))
    print("Model Notation:", model.notation.name)

    if not exists(output_folder):
        mkdir(output_folder)

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    template = jinja_env.get_template('py_template.template')

    with open(join(output_folder, "%s.py" % "main"), 'w') as f:
        f.write(template.render(problem=model.problem, tasks=model.tasks, tree=model.tree, notation=model.notation, model=args.model))

    subprocess.run(["python", "main.py"]) 


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--model', type=str, required=True, default='domain_model.dmtot')
    args = args.parse_args()
    return args
    

if __name__ == '__main__':
    args = parse_args()
    print(args)
    run(args)