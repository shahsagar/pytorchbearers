import streamlit as st
from PIL import Image
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

if "input" not in st.session_state:
    st.session_state.input = {'ingredients':[]}

if "rerun" not in st.session_state:
    st.session_state.rerun = False

def list_ingredients():
    for i, ingredient in enumerate(st.session_state.input['ingredients']):
        st.write(ingredient)

cols = st.columns(9)

with cols[0]:
    # st.header("ENTER INGREDIENTS [REQUIRED]")
    ingredient = st.text_input('ENTER INGREDIENTS [REQUIRED]', value="", placeholder = 'Enter an ingredient')
    if ingredient != "" and ingredient not in st.session_state.input['ingredients']:
        st.session_state.input['ingredients'].append(ingredient)
    list_ingredients()

with cols[1]:
    # st.header("Dietary Restriction")
    st.session_state.input['dietary_restriction'] = st.selectbox('DIETARY RESTRICTIONS', ['any', 'vegan', 'vegetarian', 'non-vegetarian', 'kosher', 'halal'])

with cols[2]:
    st.session_state.input['time'] = st.selectbox('TIME', ['any', 'breakfast', 'lunch', 'dinner', 'midnight snack'])

with cols[3]:
    st.session_state.input['cuisine'] = st.selectbox('CUISINE', ['Indian', 'Thai', 'Japanese', 'Chinese', 'Italian', 'French'])

with cols[4]:
    st.session_state.input['flavour_profile'] = st.selectbox('FLAVOUR PROFILE', ['sweet', 'spicy', 'salty', 'bitter', 'sour', 'umami'])

with cols[5]:
    st.session_state.input['allergies'] = st.multiselect('ALLERGIES', ['gluten', 'nuts', 'fish', 'dairy', 'eggs', 'soy'])

with cols[6]:
    st.session_state.input['meal_type'] = st.selectbox('MEAL TYPE', ['any', 'appetizer', 'entree', 'dessert'])

with cols[7]:
    st.session_state.input['number_of_calories'] = st.slider('NUMBER OF CALORIES', 0, 4000, 500)

with cols[8]:
    st.session_state.input['preparation_time'] = st.slider('Preparation Time (in minutes)', 0, 120, 30)

if st.button('Generate recipe'):
    st.write(st.session_state.input)
    image = Image.open('Chana-Masala-Featured.jpg')
    st.image(image)