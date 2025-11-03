import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def call_llm(prompt, model="gpt-4o-mini", temperature=0.2, max_tokens=800):
    """
    Call OpenAI LLM with given prompt and parameters.
    
    Args:
        prompt (str): The prompt to send to the LLM
        model (str): Model name to use (default: gpt-4o-mini)
        temperature (float): Temperature for response generation (default: 0.2)
        max_tokens (int): Maximum tokens in response (default: 800)
    
    Returns:
        str: The LLM response content
    """
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return resp['choices'][0]['message']['content']
