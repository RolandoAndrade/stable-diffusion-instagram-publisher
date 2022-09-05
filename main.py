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


def generate_image(prompt: str, index: int = 0, images_dir: str = 'images'):
    """Generates a single image

    Args:
        prompt (str): Prompt to generate the image.
        index (int): Index of the image to generate.
        images_dir (str): The directory where the images are stored.
    """
    model = replicate.models.get("stability-ai/stable-diffusion")
    output = model.predict(prompt=prompt)
    download_image(output[0], index, images_dir)


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


def start_new(prompt_list, caption_list):
    number_of_images = int(input('Number of images: '))
    for i in range(number_of_images):
        prompt = input('Prompt to generate image: ')
        caption = input('Caption for this paragraph: ')
        prompt_list.append(prompt)
        caption_list.append(caption)
    caption_list.append('#stablediffusion #artificialintelligence #art #ai')
    generate_images(prompt_list)

def regenerate_images(prompt_list):
    while True:
        should_regenerate = input('See the "images" directory. Do you want to regenerate any image? (y/N): ' or 'N')
        if should_regenerate.upper() == 'Y':
            files = get_files()
            try:
                index = int(input('What image do you want to regenerate? (0-' + str(len(files) - 1) + '): '))
                change_prompt = True
                if len(prompt_list) > 0:
                    should_change_prompt = input(
                        'See the "images" directory. Do you want to regenerate any image? (y/N): ' or 'N')
                    if should_change_prompt.upper() == 'Y':
                        prompt_list[index] = input('New prompt:') or \
                                             prompt_list[index]
                    generate_image(prompt_list[index], index)
                else:
                    prompt = input('Prompt to generate image: ')
                    generate_image(prompt, index)

            except ValueError:
                print('Must be a number.')
        else:
            break

if __name__ == '__main__':
    should_generate = input('Do you want to generate new images? (Y/n): ' or 'Y')
    prompt_list = []
    caption_list = []
    if should_generate.upper() != 'N':
        start_new(prompt_list, caption_list)
    regenerate_images(prompt_list)
    caption = '\n\n'.join(caption_list)
    print('Files: ', get_files())
    print('Description: ', caption)
    should_publish = input('Do you want to publish? (Y/n): ' or 'Y')
    if should_publish.upper() == 'Y':
        publish_instagram(caption)
