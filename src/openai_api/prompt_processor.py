import streamlit as st
# import lovely_logger as logging


def create_gpt_prompt(gpt_json):
    '''
    new prompt format

    prompt = 
    Create a recipe with the following conditions

    Conditions:
    1. Use chicken, rice, cauliflower done
    2. Flavor should be spicy done
    3. It should be a vegetarian recipe done
    4. The cuisine should be Indian done
    3. Avoid gluten and soy done
    5. The preparation time should be less than 30 minutes
    6. It should be a breakfast recipe done
    4. Calorie count should be less than 500 calories done
    5. There should be an appetizer and an entree done
    6. Generate a visual description of the final dish

    Desired Format:
    Ingredients: -||-
    Instructions: -||-
    Calorie Breakdown: -||- 
    Nutrition Information Per Serving: -||-
    Visual Description: -||-
    '''

    # with open('gpt_json.json') as f:
    #     gpt_json = json.loads(f.read())

    ing_list = gpt_json['ing_list']
    calorie_count = gpt_json['calorie_count']
    cuisine_type = gpt_json['cuisine_type']
    allergies_list = gpt_json['allergies_list']
    meal_type = gpt_json['meal_type']  # entree
    food_category = gpt_json['diet_restriction']  # veg non veg
    flavor = gpt_json['flavor']
    prep_time = gpt_json['prep_time']
    time_of_meal = gpt_json['time_of_meal']

    count = 1
    gpt_prompt = 'Create a recipe with the following conditions\n\nConditions:\n'

    ingredients = ''
    for ing in ing_list:
        ingredients = ingredients + ing + ', '
    ingredients = ingredients[:-2] + '.'
    gpt_prompt = gpt_prompt + f'{count} Use {ingredients}\n'

    if cuisine_type != 'Any':
        count += 1
        gpt_prompt = gpt_prompt + \
            f'{count} The cuisine should be {cuisine_type}\n'

    if allergies_list and 'None' not in allergies_list:
        count += 1
        allergies = ''
        for allergy in allergies_list:
            allergies = allergies + allergy + ', '
        allergies = allergies[:-2] + '.'
        gpt_prompt = gpt_prompt + f'{count} Avoid {allergies}\n'

    if calorie_count:
        count += 1
        gpt_prompt = gpt_prompt + \
            f'{count} The calorie count of the recipe should be less than {calorie_count}\n'

    if prep_time:
        count += 1
        gpt_prompt = gpt_prompt + \
            f'{count} The preparation time should be less than {prep_time} minutes\n'

    # veg non veg
    meal = ''
    if food_category != 'Any':
        count += 1
        gpt_prompt = gpt_prompt + \
            f'{count} It should be a {food_category} recipe\n'

    viz = 'Generate a visual description of the final dish\n'

    # entree appetizer
    meal_breakdown = 'The recipe should contain '
    if meal_type != 'Any':
        count += 1
        meal_breakdown = meal_breakdown + f'only {meal_type}'
        gpt_prompt = gpt_prompt + f'{count} {meal_breakdown}\n'

    if time_of_meal != 'Any':
        count += 1
        gpt_prompt = gpt_prompt + f'{count} Make it a {time_of_meal} recipe\n'

    if flavor != 'Any':
        count += 1
        gpt_prompt = gpt_prompt + f'{count} The flavor should be {flavor}\n'

    gpt_prompt = gpt_prompt + f'{count} {viz}'

    desired_format = '''
    Desired Format:
    Ingredients: -||-
    Instructions: -||-
    Nutrition Information Per Serving: -||-
    Preparation Time: -||- 
    Visual Description: -||-'''

    gpt_prompt += desired_format
    gpt_prompt = gpt_prompt.rstrip()
    logging.info(f'inputtt for gpt {gpt_prompt}')

    return gpt_prompt


def create_gpt_metadata(gpt_json):
    gpt_metadata = []
    return gpt_metadata


def create_dalle_prompt(gpt_response):
    #gpt_response = dalle_json['gpt_response']
    dalle_prompt = gpt_response.split("Visual Description:", 2)[1]
    logging.info(f'inputtt for dalle {dalle_prompt}')

    return dalle_prompt


def create_dalle_metadata(dalle_json):
    dalle_metadata = []
    return dalle_metadata
