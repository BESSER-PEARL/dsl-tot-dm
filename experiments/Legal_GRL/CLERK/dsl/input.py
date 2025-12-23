import re
regex_path = r'(\/.*?\.[\w:]+)'

class Input():
    def __init__(self):
        self.inputs_values = [] 

    def get_inputs_values(self):
        return self.inputs_values

    def add_input(self, name, description):#, is_optional):
        if len(re.findall(regex_path, description)) > 0:
            with open(description) as f:
                description = f.read()

        self.inputs_values.append((name, description))
    
    def process_input(self, args):
        args_dict = vars(args)
        for name, value in args_dict.items():
            if value is None or value == '':
                print(f"{name} not provided")
            else:
                self.add_input(name, value)