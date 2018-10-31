import unittest

from preprocessing import preprocesamiento
from skimage import io


class TestPreprocessingImage(unittest.TestCase):

    WIDTH_EXPECTED = 275
    HEIGHT_EXPECTED = 390

    def test_preprocessing(self):
        # Preprocesar pagina 66
        preprocesamiento('066.jpg', 'BakuretsuKungFuGirl', 1, 66)

        # (66 - 2) * 2 + 1 -> 64 * 2 + 1 -> 128 + 1 -> 129 pagina derecha
        # 130 pagina izquierda
        right = io.imread('manga/1/page129.jpg')
        height, width, _ = right.shape
        self.assertEqual(self.WIDTH_EXPECTED, width)
        self.assertEqual(self.HEIGHT_EXPECTED, height)

        left = io.imread('manga/1/page130.jpg')
        height, width, _ = left.shape
        self.assertEqual(self.WIDTH_EXPECTED, width)
        self.assertEqual(self.HEIGHT_EXPECTED, height)


if __name__ == '__main__':
    unittest.main()
