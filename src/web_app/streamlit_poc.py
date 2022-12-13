from PIL import Image
from datetime import datetime as dt
import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from openai_api import run_app
import json

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
    # sagar will fetch input json
    # XXX: replace this with Sagar's input
    with open('/home/ubuntu/pytorchbearers/src/openai_api/gpt_json.json') as f:
        input_json = json.loads(f.read())

    recipe, images = run_app.run(input_json)

    st.write(recipe)
    # XXX: display multiple images
    st.image(images[0])
