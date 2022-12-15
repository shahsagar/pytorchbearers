import openai
import argparse

with open('openai_key.txt') as f:
    openai.api_key = f.readline()


def extract_prompt(choices):
    prompts = []

    for choice in choices:
        if choice and choice.text:
            prompts.append(choice.text)

    return prompts[0]


'''
Function which takes in prompt and generates a recipe as output
'''


def get_recipe(prompt, temperature=0.7, max_tokens=3700, number_of_results=1):
    try:
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

    except Exception as e:
        raise Exception("Error occured in calling GPT completion api", e)

    return []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Cmdline arguments to run the gpt prompt generator')
    parser.add_argument("--prompt", type=str,
                        help="prompt for generating recipe")
    parser.add_argument("--temperature", type=float,
                        help="temperature between 0.7 and 0.9", default=0.7)
    parser.add_argument("--max_tokens", type=str,
                        help="max input tokens", default=3700)

    args = parser.parse_args()
    try:
        prompts = get_recipe(args.prompt, args.temperature,
                             args.max_tokens, number_of_results=1)
        print(prompts)
    except Exception as e:
        print("Exception occured", e)
