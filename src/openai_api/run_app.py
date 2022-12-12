import dalle, gpt, prompt_processor
import json
import os

here = os.path.dirname(os.path.abspath(__file__))

def run(input_json):
    gpt_prompt = prompt_processor.create_gpt_prompt(input_json)
    gpt_metadata = prompt_processor.create_gpt_metadata(input_json)

    recipe = gpt.get_recipe(
        gpt_prompt, 0.7, 2667, 1)

    dalle_prompt = prompt_processor.create_dalle_prompt(recipe)

    images = dalle.generate_output(dalle_prompt)

    return recipe, images




if __name__ == '__main__':
    with open(os.path.join(here,'gpt_json.json')) as f:
        gpt_json = json.loads(f.read())
        run(gpt_json)