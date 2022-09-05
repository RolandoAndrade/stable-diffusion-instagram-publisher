import unittest

from main import download_image, get_files, generate_images, publish_instagram


class MyTestCase(unittest.TestCase):
    def test_get_files(self):
        print(get_files('tests'))

    def test_download_image(self):
        url = 'https://replicate.com/api/models/stability-ai/stable-diffusion/files/bea78d60-66e8-41a5-a092-f29efb484859/out-0.png'
        download_image(url, 3, 'tests')

    def test_generate_images(self):
        generate_images([
            'heart exploding into a rainbow of colors watercolor style'
        ], 'tests')

    def test_publish_instagram(self):
        publish_instagram('Nice caption', 'tests')



if __name__ == '__main__':
    unittest.main()
