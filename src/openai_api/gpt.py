import openai
import requests
from io import BytesIO
from PIL import Image
import argparse
import matplotlib.pyplot as plt

# XXX: replace it with env var; current hack to overcome vscode-jupyter bash issue
openai.api_key = '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'

"""
Sample prompt - i have potatoes, rice, and tofu.Create a 500 calories recipe using these ingredients and show the calorie breakwdown
"""


def preprocessed_prompt(prompt):
    '''
    Englishify the prompt from the user input of variables
    return the preprocessed prompt - intuitive prompt =- TODO  gpt + dalle combo here
    '''
    return prompt


def get_english_prompt(user_input):
    '''
    Englishify the prompt from the user input of variables
    '''
    pass


def extract_prompt(choices):
    prompts = []

    for choice in choices:
        if choice and choice.text:
            prompts.append(choice.text)

    return prompts[0]


'''
Function which takes in prompt and generates a list of PIL images as output
'''


def get_recipe(prompt, temperature=0.7, max_tokens=1670, number_of_results=1):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,  # "i have potatoes, rice, and tofu. Create a 500 calories recipe using these ingredients and show the calorie breakwdown",
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    if (response):
        return extract_prompt(response['choices'])
    return []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Cmdline arguments to run the gpt prompt generator')
    parser.add_argument("--prompt", type=str,
                        help="prompt for generating recipe")
    parser.add_argument("--temperature", type=float,
                        help="temperature between 0.7 and 0.9")
    parser.add_argument("--max_tokens", type=str,
                        help="max input tokens", default=1670)

    args = parser.parse_args()
    prompts = get_recipe(args.prompt, args.temperature,
                          args.max_tokens, number_of_results=1)

    print(prompts)
