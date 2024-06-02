import os
from openai import AzureOpenAI
from openai import OpenAI, OpenAIError
import backoff 

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) 

api_source = os.getenv("OPENAI_API_TYPE")

gpt = None  
if api_source == "azure":
    model_name = os.getenv("AZURE_DEPLOYMENT_NAME")

    llm = AzureOpenAI(azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"))

    completion_tokens = prompt_tokens = 0

    def azure(prompt, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
        messages = [{"role": "user", "content": prompt}]
        return chatazure(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)

    def chatazure(messages, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
        global completion_tokens, prompt_tokens
        outputs = []
        while n > 0:
            cnt = min(n, 20)
            n -= cnt
            res = llm.chat.completions.create(model=model,
                            messages=messages, 
                            temperature=temperature, 
                            n=cnt, 
                            )
            outputs.extend([choice.message.content for choice in res.choices])
            # log completion tokens
            completion_tokens += res.usage.completion_tokens
            prompt_tokens += res.usage.prompt_tokens
        return outputs

    gpt = azure

elif api_source == "openai":
    model_name = os.getenv("OPENAI_MODEL_NAME")

    completion_tokens = prompt_tokens = 0

    @backoff.on_exception(backoff.expo, OpenAIError)
    def completions_with_backoff(**kwargs):
        print(kwargs)
        client = OpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"),
                )
        response = client.chat.completions.create(**kwargs)
        return response

    def gpt(prompt, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
        messages = [{"role": "user", "content": prompt}]
        return chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
        
    def chatgpt(messages, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
        global completion_tokens, prompt_tokens
        outputs = []
        while n > 0:
            cnt = min(n, 20)
            n -= cnt
            res = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, n=cnt, stop=stop)          
            outputs.extend([choice.message.content for choice in res.choices])
            completion_tokens += res.usage.completion_tokens
            prompt_tokens += res.usage.prompt_tokens
        return outputs
        
    def gpt_usage(backend="gpt-4"):
        global completion_tokens, prompt_tokens
        if backend == "gpt-4":
            cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03
        elif backend == "gpt-3.5-turbo":
            cost = completion_tokens / 1000 * 0.002 + prompt_tokens / 1000 * 0.0015
        return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}

print(f'LLM( Api source: {api_source}, model: {model_name})')