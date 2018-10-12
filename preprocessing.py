import os

import redis

from skimage import io

r = redis.StrictRedis(host='localhost', port=6379, db=0)


def split(filename, folder, manga_id):
    """
    Separar la imagen que contiene dos páginas
    y guardarlo como escala de grises
    :param filename:
    :param folder:
    :param manga_id:
    :return:
    """
    img = io.imread('data/{}/{}'.format(folder, filename), as_gray=True)

    height, width = img.shape
    width_cutoff = width // 2
    page_left = img[:, :width_cutoff]
    page_right = img[:, width_cutoff:]

    right = (i - 2) * 2 + 1
    left = right + 1
    io.imsave("manga/{}/page{}.jpg".format(manga_id, right), page_right)
    io.imsave("manga/{}/page{}.jpg".format(manga_id, left), page_left)


mid = 3
manga = r.hgetall('M{}'.format(mid))
folder = manga[b'carpeta'].decode("utf-8")
list_dir = os.listdir('data/{}'.format(folder))

"""
Se ignoran las primeras dos páginas 000 y 001 porque no suelen aportar
solo se separa las imágenes porque salen desordenada
"""
for i in range(2, 16):
    for file_name in list_dir:
        if file_name.split(".")[0] == str(i).zfill(3):
            split(file_name, folder, mid)


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