import os
import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from skimage import io, transform


class Manga109Dataset(Dataset):
    def __init__(self, json_file, root_dir, transform=None):
        """
        Args:
            json_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.label_frame = pd.read_json(json_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.label_frame)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir,
                                self.label_frame.iloc[idx, 0])
        image = io.imread(img_name)
        labels = self.label_frame.iloc[idx, 1:].as_matrix()
        labels = labels.astype('float').reshape(-1, 2)
        sample = {'image': image, 'labels': labels}

        if self.transform:
            sample = self.transform(sample)

        return sample
