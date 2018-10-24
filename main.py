import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from cnn import MangaNet
from dataset import Manga109Dataset

# Device configuration
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Etiquetas
classes = ('L1', 'L2', 'L3', 'L4', 'L5', 'L6',
           'L7', 'L8', 'L9', 'L10', 'L11', 'L12')

# Hyper parameters
num_epochs = 20
num_classes = 12
learning_rate = 0.0001

train_dataset = Manga109Dataset(csv_file='./mangalabels.csv', root_dir='manga')

# Data loader
train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)

model = MangaNet(12)
# Loss and optimizer
criterion = nn.MultiLabelSoftMarginLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
total_step = len(train_loader)
for epoch in range(num_epochs):
    for i, sample in enumerate(train_loader):
        if i == 0:
            continue

        optimizer.zero_grad()
        # Forward pass
        outputs = model(sample['image'])
        loss = criterion(outputs, sample['labels'])

        # Backward and optimize
        loss.backward()
        optimizer.step()

        if (i + 1) % 40 == 0:
            print(model.classifier[0].weight)
            # print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
            #       .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))

# Save the model checkpoint
torch.save(model.state_dict(), 'model.ckpt')
