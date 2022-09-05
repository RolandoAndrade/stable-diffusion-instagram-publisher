# Stable Diffusion Instagram Publisher

Small script used to generate images from a prompt, define the caption and
publish the generated images on Instagram.

## Requirements 

You need an  [API Key from Replicate](https://replicate.com/) and install the
dependencies from `requirements.txt`. You will also have to create an empty directory
named `images` where generated images will be stored.

Before you start, you need to set up an [Instagram account and a Meta Developer Account ](https://developers.facebook.com/docs/instagram-api/getting-started)

## How to use

Export the `REPLICATE_API_TOKEN`, `INSTAGRAM_USER` and `INSTAGRAM_PASSWORD` envs.
Then run the script.

It will ask for the number of images. This is the number of images that will be generated and published in 
the same post.

For each image, it asks for a prompt and caption. The prompt is the text used by stable diffusion to generate the images
while the caption represents a paragraph in the image description.

After finishing, it will generate the images and publish them automatically on Instagram.

If you want to have more control in what is published, you can generate the images with the 
`test_generate_images` unit test and after review them, publish them using the `test_publish_instagram`
unit test.