from PIL import Image
from datetime import datetime as dt
import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from openai_api import run_app

st.set_page_config(layout="wide")

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
            recipe, dalle_prompt = run_app.run_gpt(gpt_json)
            # st.session_state['response'] = recipe
            if (recipe):
                st.write(recipe)

            images = run_app.run_dalle(dalle_prompt)
            # st.session_state['image_response'] = images
            if (images):
                cols = st.columns(len(images))
                for i in range(len(images)):
                    with cols[i]:
                        st.image(images[i])

            st.write('P.S.: Remember, this recipe is generated using artificial intelligence. Kindly use your natural intelligence to decide if it is right for you :)')
        except Exception as e:
            print('Something went wrong. Please try again')

        # TODO -> Add the case for showing user helpful message in case of recipe blank and images
