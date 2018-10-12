import os

import redis

from skimage import io, exposure
from skimage.transform import resize

r = redis.StrictRedis(host='localhost', port=6379, db=0)


def preprocesamiento(filename, folder, manga_id):
    """
    Separar la imagen que contiene dos páginas
    y guardarlo como escala de grises
    :param filename:
    :param folder:
    :param manga_id:
    :return:
    """
    img = io.imread('data/{}/{}'.format(folder, filename))

    height, width, _ = img.shape
    width_cutoff = width // 2
    page_left = img[:, :width_cutoff]
    page_right = img[:, width_cutoff:]

    right = (i - 2) * 2 + 1
    left = right + 1

    # Reducir dimensiones
    page_left = resize(page_left, (415, 295), anti_aliasing=True)
    page_right = resize(page_right, (415, 295), anti_aliasing=True)

    # Recortar márgenes
    page_left = page_left[10:400, 10:285]
    page_right = page_right[10:400, 10:285]

    # Reajustar limites
    page_left = exposure.rescale_intensity(page_left, in_range=(-1, 1))
    page_right = exposure.rescale_intensity(page_right, in_range=(-1, 1))

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
            preprocesamiento(file_name, folder, mid)
