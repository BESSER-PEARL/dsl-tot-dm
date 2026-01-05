class Input():
    def __init__(self):
        self.inputs_values = [] 
        self.name = ""
        self.domain = ""

    def get_inputs_values(self):
        return self.inputs_values
    
    def get_name(self):
        return self.name
    
    def get_domain(self):
        return self.domain

    def add_input(self, name, type, description):
        if type == "FILE":
            with open(description) as f:
                description = f.read()
                self.domain = description

        self.inputs_values.append((name, description))
    
    def process_input(self, args, args_metamodel):
        file_name = ""
        for name, value in args_metamodel.items():
            if value["type"] == "FILE":
                file_name = name
        
        args_dict = vars(args)
        for arg, arg_mm in zip(args_dict.items(),args_metamodel.values()):
            name = arg[0]
            value = arg[1]
            type = arg_mm["type"]
            if name == file_name:
                self.name = value
            if value is None or value == '':
                print(f"{name} not provided")
            else:
                self.add_input(name, type, value)
        