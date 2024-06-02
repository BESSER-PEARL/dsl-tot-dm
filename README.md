<a name="readme-top"></a>
<!-- ABOUT THE PROJECT -->
## Application of ToT to LLM-enabled DM

We propose a DSL to facilitate the configuration and automate the execution of the [ToT](https://github.com/princeton-nlp/tree-of-thought-llm?tab=readme-ov-file) framework based on the task decomposition required for a modeling process.
The modeling process is divided by tasks, as shown in the following example:
```python
  task: 
      level: 1
      name: "Classes"
      description: "A class represents objects that share a common structure and behavior."
      assessments:
          "Classes are retrieved from nouns in the domain description."
          "The principal concepts of the domain are represented in classes."
  task: 
      level: 2
      name: "Association"
      description: "Associate is used when a class is related to another."
      assessments:
          "Associations and cardinalities are included in the model."
```


<!-- GETTING STARTED -->
## Setup

### Prerequisites

Request OpenAI or Azure keys to have access to the LLM API. Instructions are in the following links:

* [OpenAI](https://platform.openai.com/docs/quickstart)
* [AzureOpenAI](https://learn.microsoft.com/en-gb/azure/ai-services/openai/quickstart?tabs=command-line%2Cpython&pivots=programming-language-python)

Create the .env file with the variables indicated in this [file](.env_example):




### Run the project

1. Install Python 3.11 and create a virtual environment
2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
3. Create your model, see the [how-to](#how-to-create-a-new-model-for-the-dsl) section.
4. Run the application with your model:
   ```sh
   python run.py --model ER_3lev.dmtot #Replace by your model name
   ```
4. A log will capture all the thoughts created by the LLM for the task decomposition configured.
   


<!-- RECOMMENDATIONS -->

### How to create a new model for the DSL

The DSL is created with [TextX](https://github.com/textX/textX), and the [concrete syntax](dsl/dsl_grammar.tx) follows a grammar with a structured format where a Model is composed of a Tree, a Problem, multiple Tasks, and a Notation.

Examples of Entity Relationships diagram, UML class diagram, UML activity diagram, and BPMN workflow diagram are located [here](examples/models/).

<!-- USAGE EXAMPLES -->
## Paper Experiments

The results of the experiments include the [reference models](experiments/reference_model/) and the [output](experiments/logs/) from the experiments.
To run the experiments, use the [input](experiments/input/) data with the domain descriptions and models. Then execute the experiment:
   ```sh
   python run.py --model exercise2_asocclass_5lev.dmtot
   ```




