import torch
import pandas as pd
from torch.utils.data import Dataset
from skimage import io
import numpy as np


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
        image = image[:, :, np.newaxis]
        labels = self.label_frame.iloc[idx, 2:].values
        image = image.transpose((2, 0, 1))
        image = torch.from_numpy(image)
        labels = torch.from_numpy(labels)

        return {'image': image.type('torch.FloatTensor'), 'labels': labels.type('torch.FloatTensor')}


# manga_dataset = Manga109Dataset(csv_file='./mangalabels.csv', root_dir='manga')

# for i in range(len(manga_dataset)):
#     sample = manga_dataset[i]
#
#     print(sample['labels'])

# train_loader = DataLoader(manga_dataset, batch_size=4, shuffle=True, num_workers=4)
# for i, sample in enumerate(train_loader):
#     if i == 0:
#         continue
#     print(sample)
#     break
