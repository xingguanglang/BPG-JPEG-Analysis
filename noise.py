import numpy as np
from PIL import Image

def generate_noise_image(width, height, color=True):

    if color:
        noise_array = np.random.randint(0, 128, (height, width, 3), dtype=np.uint8)
    else:
        noise_array = np.random.randint(100, 128, (height, width), dtype=np.uint8)

    noise_image = Image.fromarray(noise_array)
    return noise_image
def generate_gaussian_noise_image(width, height, mean=128, std=100, color=True):
    if color:
        noise_array = np.random.normal(mean, std, (height, width, 3)).astype(np.uint8)
    else:
        noise_array = np.random.normal(mean, std, (height, width)).astype(np.uint8)

    noise_image = Image.fromarray(noise_array, 'RGB' if color else 'L')
    return noise_image

noise_img = generate_gaussian_noise_image(800, 600, color=True)
noise_img.save('noise_image8.png')

