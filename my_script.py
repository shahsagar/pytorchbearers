import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = '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'

st.set_page_config(layout="wide")

if "input" not in st.session_state:
    st.session_state.input = {'ingredients': []}


def list_ingredients():
    for i, ingredient in enumerate(st.session_state.input['ingredients']):
        st.write(ingredient)


cols = st.columns(9)

with cols[0]:
    # st.header("ENTER INGREDIENTS [REQUIRED]")
    ingredient = st.text_input(
        'ENTER INGREDIENTS [REQUIRED]', value="", placeholder='Enter an ingredient')
    if ingredient != "" and ingredient not in st.session_state.input['ingredients']:
        st.session_state.input['ingredients'].append(ingredient)
    list_ingredients()

with cols[1]:
    # st.header("Dietary Restriction")
    st.session_state.input['dietary_restriction'] = st.selectbox(
        'DIETARY RESTRICTIONS', ['any', 'vegan', 'vegetarian', 'non-vegetarian', 'kosher', 'halal'])

with cols[2]:
    st.session_state.input['time'] = st.selectbox(
        'TIME', ['any', 'breakfast', 'lunch', 'dinner', 'midnight snack'])

with cols[3]:
    st.session_state.input['cuisine'] = st.selectbox(
        'CUISINE', ['Any', 'Indian', 'Thai', 'Japanese', 'Chinese', 'Italian', 'French'])

with cols[4]:
    st.session_state.input['flavour_profile'] = st.selectbox(
        'FLAVOUR PROFILE', ['Any', 'sweet', 'spicy', 'salty', 'bitter', 'sour', 'umami'])

with cols[5]:
    st.session_state.input['allergies'] = st.multiselect(
        'ALLERGIES', ['gluten', 'nuts', 'fish', 'dairy', 'eggs', 'soy'])

with cols[6]:
    st.session_state.input['meal_type'] = st.selectbox(
        'MEAL TYPE', ['any', 'appetizer', 'entree', 'dessert'])

with cols[7]:
    st.session_state.input['number_of_calories'] = st.slider(
        'NUMBER OF CALORIES', 0, 4000, 500)

with cols[8]:
    st.session_state.input['preparation_time'] = st.slider(
        'Preparation Time (in minutes)', 0, 120, 30)

clicked = st.button('Generate recipe')
if 'response' in st.session_state or (clicked and st.session_state.input['ingredients']):
    gpt_prompt = f'''Create a recipe using {', '.join(st.session_state.input['ingredients'])}'''
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=gpt_prompt,
        temperature=0.5,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    ) if clicked else st.session_state['response']

    # st.write(response)
    # st.session_state['response'] = response
    if response.choices:
        full_recipe = response.choices[0].text
        st.write(full_recipe)
        start_index = full_recipe.rfind(
            'Instructions') or full_recipe.rfind('Directions')
        instructions = full_recipe[start_index + 1:]

        n = 4
        image_response = openai.Image.create(
            prompt=instructions,
            n=n,
            size="1024x1024"
        ) if clicked else st.session_state['image_response']
        # st.session_state['image_response'] = image_response

        # st.write(image_response)
        cols = st.columns(n)
        for i in range(n):
            with cols[i]:
                image_url = image_response['data'][i]['url']
                st.image(image_url)
