import json


def create_gpt_prompt(gpt_json):
    '''
    new prompt format

    prompt = 
    Create a recipe with the following conditions

    Conditions:
    1. use chicken, rice, cauliflower
    2. it should be a spicy vegetarian recipe
    3. avoid gluten and soy 
    4. calorie count should be less than 500 calories 
    5. there should be an appetizer and an entree
    6. generate a visual description of the final dish

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
    meal_type = gpt_json['meal_type']
    food_category = gpt_json['food_category']
    flavor = gpt_json['flavor']
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
    meal = ''
    if meal_type:
        meal = meal_type

    viz = 'There should be a visual description of the final dish'

    # entree appetizer
    food_breakdown = ''
    if food_category:
        food_breakdown = 'There should be '
        viz += ' including '
        for category in food_category:
            food_breakdown = food_breakdown + category + ', '
            viz = viz + category + ' and '
        food_breakdown = food_breakdown[:-2] + '.'
        viz = viz[:-4]


    desired_format = "Desired Format:\nIngredients: -||-\nInstructions: -||-\nCalorie Breakdown: -||-\nNutrition Information Per Serving: -||-\nVisual Description: -||-"
    new_prompt = f'Create a recipe with the following conditions\n\nConditions:\nuse {ingredients}\nit should be {flavor} {meal} {cuisine} recipe\n{allergies}\ncalorie count should be less than{calories}\n{food_breakdown}\n{viz}\n\n{desired_format}'

    #gpt_prompt = f'Create a {calories} {meal} {cuisine} recipe using {ingredients} {cal_breakdown} {allergies} {food_breakdown} {viz}'
    gpt_prompt = new_prompt.rstrip()
    print(gpt_prompt)

    return gpt_prompt


def create_gpt_metadata(gpt_json):
    gpt_metadata = []
    return gpt_metadata


def create_dalle_prompt(gpt_response):
    #gpt_response = dalle_json['gpt_response']
    dalle_prompt = gpt_response.split("Visual Description:\n", 2)[1]
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
