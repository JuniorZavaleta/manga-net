import os

import redis

from skimage import io

r = redis.StrictRedis(host='localhost', port=6379, db=0)

list_dir = os.listdir('data/AisazuNihaIrarenai')
mangaId = 3


def split(filename):
    """TODO"""


# Se ignoran las primeras dos páginas 000 y 001 porque no suelen aportar
for i in range(2, 16):
    for filename in list_dir:
        if filename.split(".")[0] == str(i).zfill(3):
            img = io.imread('data/AisazuNihaIrarenai/'+filename, as_gray=True)

            height, width = img.shape
            width_cutoff = width // 2
            page_left = img[:, :width_cutoff]
            page_right = img[:, width_cutoff:]

            right = (i - 2) * 2 + 1
            left = right + 1
            io.imsave("manga/{}/page{}.jpg".format(mangaId, right), page_right)
            io.imsave("manga/{}/page{}.jpg".format(mangaId, left), page_left)


# from skimage import io, transform
# from torchvision import transforms
#
# class CustomCrop(object):
#
#     def __init__(self, output_size):
#         assert isinstance(output_size, (int, tuple))
#         self.output_size = output_size
#
#     def __call__(self, sample):
#         image = sample['image']
#
#
# transformations = transforms.Compose([
#     CustomCrop])