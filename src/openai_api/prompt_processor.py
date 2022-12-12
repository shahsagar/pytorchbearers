import json


def create_gpt_prompt(gpt_json):
    '''
    Create a 500 calories spicy indian non veg recipes using chicken, rice, green peas, and broccoli. 
    Show the calorie breakdown. No gluten, nuts, and soy.  
    Contain a lunch appetizer and an entree. 
    There should be a visual description of the final dish including appetizer and entree"
    '''

    # with open('gpt_json.json') as f:
    #     gpt_json = json.loads(f.read())

    ing_list = gpt_json['ing_list']
    calorie_count = gpt_json['calorie_count']
    cuisine_type = gpt_json['cuisine_type']
    allergies_list = gpt_json['allergies_list']
    meal_type = gpt_json['meal_type']
    food_category = gpt_json['food_category']
    # XXX: include this in final prompt
    # XXX: include flavor profile
    # XXX: include time of meal
    prep_time = gpt_json['prep_time']

    ingredients = ''
    for ing in ing_list:
        ingredients = ingredients + ing + ', '
    ingredients = ingredients[:-2] + '.'

    cuisine = ''
    if cuisine_type:
        cuisine = cuisine_type

    calories = ''
    cal_breakdown = ''
    if calorie_count:
        calories = f'{calorie_count} calories'
        cal_breakdown = 'Show the calorie breakdown.'

    if allergies_list:
        allergies = 'No '
        for allergy in allergies_list:
            allergies = allergies + allergy + ', '
        print(allergies)
        allergies = allergies[:-2] + '.'
    else:
        allergies = ''

    # veg non veg
    meal_type = ''
    if meal_type:
        meal_type = meal_type

    viz = 'There should be a visual description of the final dish'

    # entree appetizer
    food_breakdown = ''
    if food_category:
        food_breakdown = 'Contains '
        viz += ' including '
        for category in food_category:
            food_breakdown = food_breakdown + category + ', '
            viz = viz + category + ' and '
        food_breakdown = food_breakdown[:-2] + '.'
        viz = viz[:-4]

    gpt_prompt = f'Create a {calories} {meal_type} {cuisine} recipe using {ingredients} {cal_breakdown} {allergies} {food_breakdown} {viz}'
    gpt_prompt = gpt_prompt.rstrip()
    print(gpt_prompt)

    return gpt_prompt


def create_gpt_metadata(gpt_json):
    gpt_metadata = []
    return gpt_metadata


def create_dalle_prompt(dalle_json):
    gpt_response = dalle_json['gpt_response']
    dalle_prompt = gpt_response.split("Visual Description:\n", 1)[1]
    print(dalle_prompt)
    return dalle_prompt


def create_dalle_metadata(dalle_json):
    dalle_metadata = []
    return dalle_metadata


'''
ingredients - tofu, peas, chicken
calories - 500
allergies - gluten, 





prompt = f'I have {ingredients}. Create a recipe for me using these ingredients'
if calories:
    prompt += It needs to be a {calories} recipe and show the calorie breakdown.

if cuisine:
    prompt +=  
'''
