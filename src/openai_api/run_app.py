from . import dalle
from . import gpt
from . import prompt_processor
import json
import os
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))


def run(input_json):
    gpt_prompt = prompt_processor.create_gpt_prompt(input_json)
    gpt_metadata = prompt_processor.create_gpt_metadata(input_json)

    recipe = gpt.get_recipe(
        gpt_prompt, 0.7, 3700, 1)

    dalle_prompt = prompt_processor.create_dalle_prompt(recipe)

    images = dalle.generate_output(dalle_prompt)

    # with open('recipe.txt', 'w') as f:
    #     print(recipe, file=f)
    # plt.imshow(images[0])
    # plt.savefig('dish.png')

    return recipe, images


if __name__ == '__main__':
    with open(os.path.join(here, 'gpt_json.json')) as f:
        gpt_json = json.loads(f.read())
        run(gpt_json)
