import time
from openai import OpenAI
import tiktoken
import numpy as np
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

PRICE_PER_1K_INPUT = 0.00015
PRICE_PER_1K_OUTPUT = 0.0006

def count_tokens(text, model_name):
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def call_llm(prompt: str, model_name: str):
    start = time.time()

    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
    )

    end = time.time()

    output_text = response.choices[0].message.content

    tokens_input = count_tokens(prompt, model_name)
    tokens_output = count_tokens(output_text, model_name)

    cost = (
        (tokens_input / 1000) * PRICE_PER_1K_INPUT +
        (tokens_output / 1000) * PRICE_PER_1K_OUTPUT
    )

    latency = end - start

    return output_text, tokens_input, tokens_output, cost, latency
