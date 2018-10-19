import torch
from torch.utils.data import DataLoader

from cnn import MangaNet
from dataset import Manga109Dataset

model = MangaNet(12)
checkpoint = torch.load('model.ckpt')
model.load_state_dict(checkpoint)

test_dataset = Manga109Dataset(csv_file='./test.csv', root_dir='manga')
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True)

with torch.no_grad():
    correct = 0
    total = 0

    for i, sample in enumerate(test_loader):
        print(sample['labels'])
        outputs = model(sample['image'])

        _, predicted = torch.max(outputs, 1)
        print(predicted)
