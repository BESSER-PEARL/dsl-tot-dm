<a name="readme-top"></a>
<!-- ABOUT THE PROJECT -->
## CLERK: a Companion Large Language Model Expert for Modeling Regulatory Knowledge

CLERK assists with Legal GRL modeling by implementing the ToT4DM approach with three key features:

1. **Tree-of-Thought (ToT) framework**: breaks down complex steps into manageable tasks, focusing only on essential information for constructing a Legal GRL model.

2. **Self-evaluation and branch selection** – evaluates intermediate outputs and advances along the most promising path to build the final Legal GRL model.

3. **Enhanced in-context learning** – uses context manager, role prompting, zero-shot and few-shot CoT, and structured output formatting with explicit syntax definition.

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
   python run.py --model legalgrl_4lev_art4_dsl.dmtot #Replace using your CLERK model
   ```
4. A log will capture all the thoughts created by the LLM for the CLERK DSL model configured.
   

<!-- RECOMMENDATIONS -->

### How to execute CLERK with a new Law article

An example of the DSL is availble  [here](input/legalgrl_4lev_art50_1_dsl.dmtot). To use CLERK with a new law article, follow these steps:
1. **Law article:** Go to problem > domain, insert the text of the law article that you want to model. 
2. **Modeling purpose:** Go to problem > purpose, specify the focus of the model, and define the focal actors.


<!-- USAGE EXAMPLES -->
## Paper Experiments

The results of the experiments include the [reference models](reference_model/) and the [output](output/) from the experiments.
To run the experiments, use the [input](input/) data with the domain descriptions and models. Then execute the experiment:
   ```sh
   python run.py --model legalgrl_4lev_art4_dsl.dmtot
   ```




