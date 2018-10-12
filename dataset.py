import pandas as pd
from torch.utils.data import Dataset
from skimage import io


class Manga109Dataset(Dataset):
    def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.label_frame = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.label_frame)

    def __getitem__(self, idx):
        manga = str(self.label_frame.iloc[idx, 0])
        pagina = str(self.label_frame.iloc[idx, 1])

        img_name = '{}/{}/page{}.jpg'.format(self.root_dir, manga, pagina)
        image = io.imread(img_name, as_gray=True)
        labels = self.label_frame.iloc[idx, 2:].values

        return {'image': image, 'labels': labels}


manga_dataset = Manga109Dataset(csv_file='./mangalabels.csv', root_dir='manga')

for i in range(len(manga_dataset)):
    sample = manga_dataset[i]

    print(sample['labels'])
