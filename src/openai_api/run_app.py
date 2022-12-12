from openai_api import dalle, gpt, prompt_processor


def run(input_json):
    gpt_prompt = prompt_processor.create_gpt_prompt(input_json)
    gpt_metadata = prompt_processor.create_gpt_metadata(input_json)

    recipe = gpt.get_recipe(
        gpt_prompt, gpt_metadata['temperature'], gpt_metadata['max_tokens'], gpt_metadata['number_of_results'])

    dalle_prompt = prompt_processor.create_dalle_prompt(recipe)

    images = dalle.generate_output(dalle_prompt)

    return recipe, images
