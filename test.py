import torch
import numpy as np
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, precision_score

from cnn import MangaNet
from dataset import Manga109Dataset

model = MangaNet(8)
checkpoint = torch.load('model.ckpt')
model.load_state_dict(checkpoint)

test_dataset = Manga109Dataset(csv_file='./test.csv', root_dir='manga')
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True)

classes = ['Peleas', 'Terror', 'Humor', 'Romance', 'Comedia romántica', 'Ciencia ficción', 'Deportes', 'Suspenso']

true_labels = []
predicted_labels = []

sum_ac_pag = 0.0
sum_prec_pag = 0.0

with torch.no_grad():
    correct = 0
    total = 0

    sum_accuracy = 0.0
    sum_precision = 0.0

    for i, sample in enumerate(test_loader):
        outputs = model(sample['image'])
        predicted_t = torch.sigmoid(outputs).data > 0.25

        groun_truth_t = sample['labels'].type('torch.IntTensor')
        _groun_truth = groun_truth_t.numpy().flatten()
        _predicted = predicted_t.numpy().flatten()

        # print(_groun_truth, _predicted)
        accuracy_image = accuracy_score(_groun_truth, _predicted)
        print("Precision imagen: ", accuracy_image)
        # print(torch.max(groun_truth_t, 1))
        groun_truth = np.argwhere(_groun_truth == 1).flatten()
        predicted = np.argwhere(_predicted == 1).flatten()

        labels_well_predicted = len(np.intersect1d(groun_truth, predicted))
        labels_union = len(np.union1d(groun_truth, predicted))

        print("Etiquetas bien clasificadas: {} de {}".format(labels_well_predicted, len(groun_truth)))
        if labels_union != 0:
            # Exactitud de la prediccion para la pagina
            ac_pag = labels_well_predicted * 100.0 / labels_union
            sum_ac_pag = sum_ac_pag + ac_pag

        if len(predicted) != 0:
            # Precision de la preddiccion para la pagina
            pre_pag = labels_well_predicted * 100.0 / len(predicted)
            sum_prec_pag = sum_prec_pag + pre_pag

        true_labels.append(_groun_truth.astype(int))
        predicted_labels.append(_predicted.astype(int))

        # print(torch.max(predicted_t, 1))
        sum_accuracy = sum_accuracy + accuracy_image
        sum_precision = sum_precision + precision_score(_groun_truth, _predicted)

print("Accuracy: ", sum_accuracy / len(test_loader))
print("Precision: ", sum_precision / len(test_loader))

print("Exactitud: ", sum_ac_pag / len(test_loader))
print("Precision: ", sum_prec_pag / len(test_loader))

# print(true_labels, predicted_labels)
np.savetxt("predicted.csv", predicted_labels, delimiter=",", fmt='%d')
