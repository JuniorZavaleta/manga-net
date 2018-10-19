import torch
import numpy as np
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix, accuracy_score
from torch import  nn
from cnn import MangaNet
from dataset import Manga109Dataset
import pandas as pd

model = MangaNet(12)
checkpoint = torch.load('model.ckpt')
model.load_state_dict(checkpoint)

test_dataset = Manga109Dataset(csv_file='./test.csv', root_dir='manga')
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True)

classes = ['Animal', 'Peleas', 'Fantasia', '4 paneles', 'Drama Histórico', 'Terror', 'Humor', 'Romance',
           'Comedia romántica', 'Ciencia ficción', 'Deportes', 'Suspenso']

with torch.no_grad():
    correct = 0
    total = 0

    sum_accuracy = 0.0
    for i, sample in enumerate(test_loader):
        outputs = model(sample['image'])
        predicted_t = torch.sigmoid(outputs).data > 0.2

        groun_truth_t = sample['labels'].type('torch.IntTensor')
        _groun_truth = groun_truth_t.numpy().flatten()
        _predicted = predicted_t.numpy().flatten()

        print(_groun_truth, _predicted)
        print("Precision imagen: ", accuracy_score(_groun_truth, _predicted))
        # print(torch.max(groun_truth_t, 1))
        groun_truth = np.argwhere(_groun_truth == 1).flatten()
        predicted = np.argwhere(_predicted == 1).flatten()

        labels_well_predicted = len(np.intersect1d(groun_truth, predicted))
        print("Etiquetas bien clasificadas: {} de {}".format(labels_well_predicted, len(groun_truth)))

        # print(torch.max(predicted_t, 1))
        sum_accuracy = sum_accuracy + accuracy_score(_groun_truth, _predicted)
        print(confusion_matrix(_groun_truth, _predicted))

    print("Precisión: ", sum_accuracy / len(test_loader))
