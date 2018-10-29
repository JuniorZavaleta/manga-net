import os

import redis

from skimage import io, exposure
from skimage.transform import resize

r = redis.StrictRedis(host='localhost', port=6379, db=0)

TELEGRAM_IN_FOLDER = 'static/telegram_images/{}.jpg'
TELEGRAM_OUT_FOLDER = 'telegram_processed/{}.jpg'


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


def preprocesamiento_telegram(file_id):
    filepath = TELEGRAM_IN_FOLDER.format(file_id)
    img = io.imread(filepath)

    height, width, _ = img.shape

    # Considerar como dos páginas cuando el ancho es mayor al alto
    if width > height:
        width_cutoff = width // 2
        page_left = img[:, :width_cutoff]
        page_right = img[:, width_cutoff:]

        # Reducir dimensiones
        page_left = resize(page_left, (415, 295), anti_aliasing=True)
        page_right = resize(page_right, (415, 295), anti_aliasing=True)

        # Recortar márgenes
        page_left = page_left[10:400, 10:285]
        page_right = page_right[10:400, 10:285]

        # Reajustar limites
        page_left = exposure.rescale_intensity(page_left, in_range=(-1, 1))
        page_right = exposure.rescale_intensity(page_right, in_range=(-1, 1))

        filename_right = TELEGRAM_OUT_FOLDER.format(file_id + '_right')
        filename_left = TELEGRAM_OUT_FOLDER.format(file_id + '_left')
        io.imsave(filename_right, page_right)
        io.imsave(filename_left, page_left)

        return [filename_right, filename_left]
    else:
        # Reducir dimensiones
        page = resize(img, (415, 295), anti_aliasing=True)

        # Recortar márgenes
        page = page[10:400, 10:285]

        # Reajustar límites
        page = exposure.rescale_intensity(page, in_range=(-1, 1))
        filename = TELEGRAM_OUT_FOLDER.format(file_id)
        io.imsave(filename, page)

        return [filename]


"""
Se ignoran las primeras dos páginas 000 y 001 porque no suelen aportar
solo se separa las imágenes porque salen desordenada
"""
for m_id in range(1, 8):
    for i in range(2, 17):
        manga = r.hgetall('M{}'.format(m_id))
        folder = manga[b'carpeta'].decode("utf-8")
        list_dir = os.listdir('data/{}'.format(folder))

        for file_name in list_dir:
            if file_name.split(".")[0] == str(m_id).zfill(3):
                preprocesamiento(file_name, folder, m_id)
