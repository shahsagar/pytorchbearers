from PIL import Image
from datetime import datetime as dt
import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from openai_api import run_app
import json

st.set_page_config(layout="wide")

if "input" not in st.session_state:
    st.session_state.input = {'ing_list': []}


def list_ingredients():
    for i, ingredient in enumerate(st.session_state.input['ing_list']):
        st.write(ingredient)


cols = st.columns(9)

with cols[0]:
    # st.header("ENTER INGREDIENTS [REQUIRED]")
    ingredient = st.text_input(
        'ENTER INGREDIENTS [REQUIRED]', value="", placeholder='Enter an ingredient')
    if ingredient != "" and ingredient not in st.session_state.input['ing_list']:
        st.session_state.input['ing_list'].append(ingredient)
    list_ingredients()

with cols[1]:
    # st.header("Dietary Restriction")
    st.session_state.input['food_category'] = st.selectbox('DIETARY RESTRICTIONS', [
                                                           'Any', 'Vegan', 'Vegetarian', 'Non vegetarian', 'Kosher', 'Halal'])

# XXX: integrate this in prompt processor or combine here
with cols[2]:
    st.session_state.input['time'] = st.selectbox(
        'TIME', ['Any', 'Breakfast', 'Lunch', 'Dinner', 'Midnight Snack'])

with cols[3]:
    st.session_state.input['cuisine_type'] = st.selectbox(
        'CUISINE', ['Any', 'Indian', 'Thai', 'Japanese', 'Chinese', 'Italian', 'French'])

with cols[4]:
    st.session_state.input['flavor'] = st.selectbox(
        'FLAVOUR PROFILE', ['Any', 'Sweet', 'Spicy', 'Salty', 'Bitter', 'Sour', 'Umami'])

with cols[5]:
    st.session_state.input['allergies_list'] = st.multiselect(
        'ALLERGIES', ['Gluten', 'Nuts', 'Fish', 'Dairy', 'Eggs', 'Soy'])

with cols[6]:
    st.session_state.input['meal_type'] = st.selectbox(
        'MEAL TYPE', ['Any', 'Appetizer', 'Entree', 'Dessert'])

with cols[7]:
    st.session_state.input['calorie_count'] = st.slider(
        'NUMBER OF CALORIES', 0, 4000, 500)

with cols[8]:
    st.session_state.input['prep_time'] = st.slider(
        'Preparation Time (in minutes)', 0, 120, 30)

clicked = st.button('Generate recipe')
if 'response' in st.session_state or (clicked and st.session_state.input['ing_list']):
    recipe, images = run_app.run(st.session_state.input)

    if(recipe):
        st.write(recipe)
    if(images):
        cols = st.columns(len(images))
        for i in range(len(images)):
            with cols[i]:
                st.image(images[i])

    #TODO -> Add the case for showing user helpful message in case of recipe blank and images