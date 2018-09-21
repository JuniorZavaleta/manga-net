from skimage import io, transform
from torchvision import transforms

class CustomCrop(object):

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        self.output_size = output_size

    def __call__(self, sample):
        image = sample['image']


transformations = transforms.Compose([
    CustomCrop)