from . import dalle
from . import gpt
from . import prompt_processor
import json
import os
import matplotlib.pyplot as plt

from datetime import datetime
from pytz import timezone

here = os.path.dirname(os.path.abspath(__file__))


def run(input_json):
    fmt = "%Y%m%d-%H:%M:%S"
    now_time = datetime.now(timezone('US/Eastern'))
    timestr = now_time.strftime(fmt)
    gpt_prompt = prompt_processor.create_gpt_prompt(input_json)
    gpt_metadata = prompt_processor.create_gpt_metadata(input_json)

    recipe = gpt.get_recipe(
        gpt_prompt, 0.7, 3700, 1)

    with open(f'recipe-{timestr}.txt', 'w') as f:
        print(recipe, file=f)

    dalle_prompt = prompt_processor.create_dalle_prompt(recipe)

    # change number of images here
    images = dalle.generate_output(dalle_prompt, 3)

    plt.imshow(images[0])
    plt.savefig(f'dish-{timestr}.png')

    return recipe, images


if __name__ == '__main__':
    with open(os.path.join(here, 'gpt_json.json')) as f:
        gpt_json = json.loads(f.read())
        run(gpt_json)
