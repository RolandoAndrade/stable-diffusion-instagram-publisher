import os
from typing import List
from instagrapi import Client
from os import listdir
from os.path import isfile, join
import replicate
from PIL import Image
import requests
from io import BytesIO


def get_files(directory: str = 'images'):
    """Gets the files in the images directory.

     Args:
         directory (str): The directory where the files are stored.
    """
    return sorted([join(directory, f) for f in listdir(directory) if isfile(join(directory, f))])


def download_image(image_url: str, number: int, images_dir: str = 'images'):
    """Downloads an image and saves it to a jpg file.

    Args:
        image_url: Url of the image to download.
        number: The current number of the image to download.
        images_dir: The directory where the images are stored.
    """
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save(images_dir + '/img' + str(number) + '.jpg')
    print('Saved ' + images_dir + '/img' + str(number) + '.jpg')


def generate_images(prompts: List[str], images_dir: str = 'images'):
    """Generates images from the given prompt

    Args:
        prompts (List[str]): List of prompt to generate images.
        images_dir (str): The directory where the images are stored.
    """
    model = replicate.models.get("stability-ai/stable-diffusion")
    for i, prompt in enumerate(prompts):
        output = model.predict(prompt=prompt)
        download_image(output[0], i, images_dir)


def publish_instagram(caption: str, images_dir: str = 'images'):
    """Publishes the images on the defined directory

    Args:
        caption (str): Caption of the images to publish.
        images_dir (str): Directory where the images are stored.
    """
    print('Publishing images')
    cl = Client()
    cl.login(os.environ['INSTAGRAM_USER'], os.environ['INSTAGRAM_PASSWORD'])
    cl.album_upload(paths=get_files(images_dir),
                    caption=caption)
    print('Done!')


if __name__ == '__main__':
    number_of_images = int(input('Number of images: '))
    prompt_list = []
    caption_list = []
    for i in range(number_of_images):
        prompt = input('Prompt to generate image: ')
        caption = input('Caption for this paragraph: ')
        prompt_list.append(prompt)
        caption_list.append(caption)
    caption_list.append('#stablediffusion #artificialintelligence #art #ai')
    generate_images(prompt_list)
    caption = '\n\n'.join(caption_list)
    publish_instagram(caption)

