# from . import dalle
# from . import gpt
# from . import prompt_processor
import json
import os
import matplotlib.pyplot as plt
import openai
import requests
from io import BytesIO
from PIL import Image

from datetime import datetime
from pytz import timezone
# import lovely_logger as logging

here = os.path.dirname(os.path.abspath(__file__))


def generate_output(prompt, number_of_results=1, size="1024x1024"):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=number_of_results,
            size=size
        )

        image_urls = response['data']
        result_images = []
        for url in image_urls:
            response = requests.get(url['url'])
            img = Image.open(BytesIO(response.content))
            result_images.append(img)
    except Exception as e:
        raise Exception("Error occured in calling Dalle image create api", e)
        return e

    return result_images


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


def run_gpt(gpt_prompt):
    fmt = "%Y%m%d-%H:%M:%S"
    now_time = datetime.now(timezone('US/Eastern'))
    timestr = now_time.strftime(fmt)

    try:
        recipe = get_recipe(
            gpt_prompt, 0.7, 3700, 1)
        print(recipe)
        # with open(f'logs/recipe-{timestr}.txt', 'w') as f:
        #     print(recipe, file=f)

        return recipe

    except Exception as e:
        print(e)
        return e


def run_dalle(dalle_prompt):
    fmt = "%Y%m%d-%H:%M:%S"
    now_time = datetime.now(timezone('US/Eastern'))
    timestr = now_time.strftime(fmt)

    try:
        # to check excpetion handling
        # dalle_prompt = "A plate of spicy Bittergourd Curry with slices of Bittergourd cooked in a creamy sauce of spices and milk. The dish is topped with chopped fresh coriander leaves and served hot."

        # change number of images here
        images = generate_output(dalle_prompt, 3)

        # plt.imshow(images[0])
        # plt.savefig(f'logs/dish-{timestr}.png')

        return images

    except Exception as e:
        print(e)
        return e


if __name__ == '__main__':
    with open(os.path.join(here, 'gpt_json.json')) as f:
        gpt_json = json.loads(f.read())
        recipe, dalle_prompt = run_gpt(gpt_json)
        run_dalle(dalle_prompt)
