from openai import OpenAI
import requests
from io import BytesIO
from PIL import Image

from rembg import remove

import io

import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
remove_bg_api_key = os.getenv('REMOVE_BG_API_KEY')

# Initialize OpenAI API
client = OpenAI(api_key=openai_api_key)


# Function to generate images
def generate_image_variation(image, size):
    response = client.images.create_variation(
        image=image,
        size=size,
        n=1,
    )
    image_url = response.data[0].url
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img


def generate_image(prompt, size):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        n=1,
    )
    image_url = response.data[0].url
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img


def remove_background(image_type, image_path):
    with open(image_path, 'rb') as input_file:
        input_data = input_file.read()
        result = remove(input_data)
        img = Image.open(io.BytesIO(result)).convert("RGBA")

        # Get the bounding box of the non-transparent pixels
        bbox = img.getbbox()

        # Crop the image to the bounding box
        img_cropped = img.crop(bbox)

        # Save the processed image

        if image_type == 'bird':
            img_resized = img_cropped.resize((45, 45))  # 34x24

        elif image_type == 'pipe':
            img_resized = img_cropped.resize((52, 320))

        return img_resized


def generate(theme):
    print('generating bird...')
    bird_img = generate_image(
        prompt=f'flappy bird like character in style of {theme} with simple design and transparent background.',
        size='1024x1024')

    bird_img.save('../assets/sprites/redbird-upflap.png')

    print('generating background...')
    bg_img = generate_image(prompt=f'very simple background related to {theme} with sky and buildings.',
                            size='1024x1024')

    bg_img.save('../assets/sprites/background-day.png')

    print('generating pipe...')
    pipe_img = generate_image(
        prompt=f'vertical Mario pipe in style of {theme} with simple design and transparent background.',
        size='1024x1024')

    pipe_img.save('../assets/sprites/pipe-green.png')

    print('generating base...')
    bg_img = generate_image(prompt=f'continuous 2D floor pattern in style of {theme}.',
                            size='1024x1024')

    bg_img.save('../assets/sprites/base.png')

    print('removing bird background...')
    bird_img = remove_background(image_type='bird', image_path='../assets/sprites/redbird-upflap.png')
    bird_img.save('../assets/sprites/redbird-upflap.png')
    bird_img.save('../assets/sprites/redbird-midflap.png')
    bird_img.save('../assets/sprites/redbird-downflap.png')

    print('removing pipe background...')
    pipe_img = remove_background(image_type='pipe', image_path='../assets/sprites/pipe-green.png')
    pipe_img.save('../assets/sprites/pipe-green.png')


if __name__ == '__main__':
    generate(theme='russia')
