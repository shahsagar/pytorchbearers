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
from openai_api import prompt_processor

st.set_page_config(layout="wide")


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


if "input" not in st.session_state:
    st.session_state.input = {'ing_list': []}


def list_ingredients():
    for i, ingredient in enumerate(st.session_state.input['ing_list']):
        st.write(ingredient)


st.markdown('<div style="text-align: center;">Hello hungry foodies, it is time to munch!</div>',
            unsafe_allow_html=True)
st.write('')
st.markdown('<div style="text-align: center;">Whether you are in a soup since you only have a few items in your refrigator or you are in pickle because you have a lot of ingredients but do not know what different you could prepare - Do not worry, we got you covered!</div>',
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
        'FLAVOUR PROFILE', ['Any', 'Sweet', 'Spicy', 'Salty', 'Bitter', 'Sour', 'Umami'])

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
        'NUMBER OF CALORIES', 0, 4000, 500)

with cols[8]:
    st.session_state.input['prep_time'] = st.slider(
        'PREP TIME', 0, 120, 30)

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
            gpt_prompt = prompt_processor.create_gpt_prompt(gpt_json)

            recipe = run_gpt(gpt_prompt)

            if (recipe):
                st.write(recipe)

            dalle_prompt = prompt_processor.create_dalle_prompt(recipe)

            images = run_dalle(dalle_prompt)
            if (images):
                cols = st.columns(len(images))
                for i in range(len(images)):
                    with cols[i]:
                        st.image(images[i])

            st.write('P.S.: Remember, this recipe is generated using artificial intelligence. Kindly use your natural intelligence to decide if it is right for you :)')
        except Exception as e:
            print('Something went wrong. Please try again')

        # TODO -> Add the case for showing user helpful message in case of recipe blank and images
