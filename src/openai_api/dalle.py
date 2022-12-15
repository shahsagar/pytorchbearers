import os
import openai
import requests
from io import BytesIO
from PIL import Image
import argparse
import matplotlib.pyplot as plt
import streamlit as st

if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/openai_key.txt'):
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/openai_key.txt') as f:
        openai.api_key = f.readline()
else:
    openai.api_key = st.secrets["openai_key"]

'''
Function which takes in prompt and generates a list of PIL images as output
'''


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Cmdline arguments to run the dalle generator')
    parser.add_argument("--prompt", type=str,
                        help="prompt less than 400 chars",)
    parser.add_argument("--n", type=int, help="number of results", default=4)
    parser.add_argument("--size", type=str,
                        help="image size", default="1024x1024")

    args = parser.parse_args()

    try:
        images = generate_output(args.prompt, args.n, args.size)
        for idx, img in enumerate(images):
            plt.imshow(img)
            plt.savefig(f'result_image_{idx}.png')
            plt.show()
    except Exception as e:
        print(e)

'''
sample prompt
"Heat a large pan over medium heat. Add the onion and cook until softened, about 5 minutes. 
Add the ginger and garlic and cook for an additional minute.\n3. Add the spices and stir to coat the onion and garlic. 
Add the broth, coconut milk, Sriracha sauce, and honey.  Add the chickpeas and tofu and stir. Simmer for 10 minutes.  
Add the frozen peas and cilantro and cook. Serve over rice or with naan",'''
