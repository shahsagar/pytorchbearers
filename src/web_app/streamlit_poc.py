from PIL import Image
from datetime import datetime as dt
import streamlit as st
import os
import sys
import matplotlib.pyplot as plt
import openai
import requests
from io import BytesIO
from PIL import Image

from datetime import datetime
from pytz import timezone
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# from openai_api import prompt_processor

st.set_page_config(layout="wide")

if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/openai_key.txt'):
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/openai_key.txt') as f:
        openai.api_key = f.readline()
else:
    openai.api_key = st.secrets["openai_key"]

if "input" not in st.session_state:
    st.session_state.input = {'ing_list': []}


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
    # logging.info(f'inputtt for gpt {gpt_prompt}')

    return gpt_prompt


def create_gpt_metadata(gpt_json):
    gpt_metadata = []
    return gpt_metadata


def create_dalle_prompt(gpt_response):
    #gpt_response = dalle_json['gpt_response']
    dalle_prompt = gpt_response.split("Visual Description:", 2)[1]
    # logging.info(f'inputtt for dalle {dalle_prompt}')

    return dalle_prompt


def list_ingredients():
    for i, ingredient in enumerate(st.session_state.input['ing_list']):
        st.write(ingredient)


st.markdown("<h2 style='text-align: center; color: #fd6d6d;'>AI ENTERS THE KITCHEN</h2>",
            unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; '>Hello hungry foodies, it\'s time to munch!</h4>",
            unsafe_allow_html=True)
# st.markdown("<h5 style='text-align: center; '>But, whether you are in a soup since you only have a few items in your refrigator OR you are in a pickle because you have a lot of ingredients but do not know what different you could prepare - Do not worry, we got you covered!</h5>",
#             unsafe_allow_html=True)
# st.markdown("<h5 style='text-align: center; '>Just list down your ingredients below. You are free to specify other options or leave it as is.</h5>",
#             unsafe_allow_html=True)

# st.markdown('<div style="text-align: center;">**Hello hungry foodies, it is time to munch!**</div>',
#             unsafe_allow_html=True)
st.write('')
st.markdown('<div style="text-align: center;">But, whether you are in a soup since you only have a few items in your refrigerator OR you are in a pickle because you don\'t know what different to prepare - Worry not, we got you covered!</div>',
            unsafe_allow_html=True)
st.write('')
st.markdown('<div style="text-align: center;">Just list down your ingredients below. You are free to specify other options or leave it as is.</div>',
            unsafe_allow_html=True)
st.write('')

# st.write('Hello Foodies, welcome!')
# st.write('')
# st.write('Just list down your ingredients below. You are free to specify other options or leave it as is.')

cols = st.columns(9)

with cols[0]:
    # st.header("ENTER INGREDIENTS [REQUIRED]")

    ingredient = st.text_input(
        'ENTER INGREDIENTS*', value="", placeholder='Enter an ingredient')
    if ingredient != "" and ingredient not in st.session_state.input['ing_list']:
        st.session_state.input['ing_list'].append(ingredient)
    list_ingredients()

with cols[1]:
    st.session_state.input['cuisine_type'] = st.selectbox(
        'CUISINE', ['Any', 'Indian', 'Thai', 'Japanese', 'Chinese', 'Italian', 'French'])

with cols[2]:
    st.session_state.input['flavor'] = st.selectbox(
        'FLAVOR PROFILE', ['Any', 'Sweet', 'Spicy', 'Salty', 'Bitter', 'Sour', 'Umami'])

with cols[3]:
    st.session_state.input['diet_restriction'] = st.selectbox('DIETARY RESTRICTIONS', [
        'Any', 'Vegan', 'Vegetarian', 'Non vegetarian', 'Kosher', 'Halal'])

with cols[4]:
    st.session_state.input['time_of_meal'] = st.selectbox(
        'TIME OF MEAL', ['Any', 'Breakfast', 'Lunch', 'Dinner', 'Midnight Snack'])

with cols[5]:
    st.session_state.input['allergies_list'] = st.multiselect(
        'ALLERGIES', ['None', 'Gluten', 'Nuts', 'Fish', 'Dairy', 'Eggs', 'Soy'], default='None')

with cols[6]:
    st.session_state.input['meal_type'] = st.selectbox(
        'MEAL TYPE', ['Any', 'Appetizer', 'Entree', 'Dessert'])

with cols[7]:
    st.session_state.input['calorie_count'] = st.slider(
        'CALORIES (Max)', 0, 4000, 500)

with cols[8]:
    st.session_state.input['prep_time'] = st.slider(
        'PREP TIME (Max)', 0, 120, 30)

cols = st.columns(5)
with cols[0]:
    pass
with cols[1]:
    pass
with cols[2]:
    clicked = st.button('Generate recipe')
with cols[3]:
    pass
with cols[4]:
    pass

if 'response' in st.session_state or (clicked and st.session_state.input['ing_list']):
    with st.spinner(text="Creating something yummy for you..."):
        try:
            gpt_json = st.session_state.input
            gpt_prompt = create_gpt_prompt(gpt_json)

            recipe = run_gpt(gpt_prompt)

            if (recipe):
                st.write(recipe)

            dalle_prompt = create_dalle_prompt(recipe)

            images = run_dalle(dalle_prompt)
            if (images):
                cols = st.columns(len(images))
                for i in range(len(images)):
                    with cols[i]:
                        st.image(images[i])

            st.download_button(
                label="Download recipe",
                data=recipe,
                file_name='recipe.txt',
            )

            st.session_state.input['ing_list'] = []

            st.write('P.S.: Remember, this recipe is generated using artificial intelligence. Kindly use your natural intelligence to decide if it is right for you :)')

        except Exception as e:
            print('Something went wrong. Please try again')
        # TODO -> Add the case for showing user helpful message in case of recipe blank and images
