from . import dalle
from . import gpt
from . import prompt_processor
import json
import os
import matplotlib.pyplot as plt

from datetime import datetime
from pytz import timezone

here = os.path.dirname(os.path.abspath(__file__))


def run_gpt(input_json):
    fmt = "%Y%m%d-%H:%M:%S"
    now_time = datetime.now(timezone('US/Eastern'))
    timestr = now_time.strftime(fmt)
    gpt_prompt = prompt_processor.create_gpt_prompt(input_json)

    try:
        recipe = gpt.get_recipe(
            gpt_prompt, 0.7, 3700, 1)

        # with open(f'logs/recipe-{timestr}.txt', 'w') as f:
        #     print(recipe, file=f)

        dalle_prompt = prompt_processor.create_dalle_prompt(recipe)

        return recipe, dalle_prompt

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
        images = dalle.generate_output(dalle_prompt, 3)

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
