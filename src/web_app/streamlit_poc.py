from PIL import Image
from datetime import datetime as dt
import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from openai_api import dalle


if "myingredients" not in st.session_state:
    st.session_state.myingredients = []

if "rerun" not in st.session_state:
    st.session_state.rerun = False


def list_ingredients():
    st.session_state.tskclk = []
    for i, ingredient in enumerate(st.session_state.myingredients):
        st.write(ingredient)


if st.session_state.rerun:
    st.session_state.rerun = False
    st.experimental_rerun()
else:
    ingredient = st.text_input(
        'Enter your ingredients', value="", placeholder='Enter an ingredient')
    if st.button('Add Task') and ingredient != "" and ingredient not in st.session_state.myingredients:
        st.session_state.myingredients.append(ingredient)

list_ingredients()

if st.button('Generate recipe'):
    prompt = '''Soak Dried Chickpeas or Use Canned
Rinse and soak dry chickpeas in about 4 cups water, overnight, or at least 8-10 hours. Drain and rinse them before cooking. Skip this step if using unsoaked chickpeas. If using canned chickpeas, rinse and drain them.
Saute and Pressure Cook
Turn on Saute adjust it to high. Heat oil (or ghee) and add cumin seeds. When cumin begins to splutter, add onions and saute them for 3-4 minutes. Add ginger and garlic paste, along with green chilies, and saute for another minute. Now add the tomato, and all the spices along with a few tablespoons of water. Use that to deglaze the pot and scrape off any brown bits stuck at the bottom. Cancel Saute.
Add chickpeas, and water and give it a stir. Close the lid, vent set to 'sealing', and pressure cook for 45 minutes at Bean/Chili or Manual mode.
If using unsoaked dry chickpeas, adjust the pressure cook time to 60 minutes. If using canned chickpeas, reduce the cooking time to 5 minutes.
Once cooking time is up, wait for the pressure to release naturally for 10-15 minutes, followed by manual pressure release. Open the lid after the pin drops. 
Finish and Serve
Using a potato masher or a wooden spoon, mash a few beans. This makes the curry creamy and thick naturally. To thicken it more, simmer for a few minutes on saute mode.
Garnish with cilantro and squeeze a few drops of lime or lemon juice. Serve with Puri, Naan, or Cumin rice!'''
    st.write(prompt)
    # image = Image.open('Chana-Masala-Featured.jpg')
    images = dalle.generate_output(prompt)
    st.image(images[0])
    # st.image(image)
