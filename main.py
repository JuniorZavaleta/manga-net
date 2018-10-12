import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from cnn import MangaNet
from dataset import Manga109Dataset

# Device configuration
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Hyper parameters
num_epochs = 10
num_classes = 12
learning_rate = 0.001

train_dataset = Manga109Dataset(csv_file='./mangalabels.csv', root_dir='manga')
test_dataset = Manga109Dataset(csv_file='./mangalabels.csv', root_dir='manga')

# Data loader
train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
test_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)

model = MangaNet(12)
# Loss and optimizer
criterion = nn.MultiLabelMarginLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
total_step = len(train_loader)
for epoch in range(num_epochs):
    for i, sample in enumerate(train_loader):
        if i == 0:
            continue

        # Forward pass
        outputs = model(sample['image'])
        loss = criterion(outputs, sample['labels'].squeeze(1))

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (i + 1) % 100 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                  .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))

# Test the model
model.eval()  # eval mode (batchnorm uses moving mean/variance instead of mini-batch mean/variance)
with torch.no_grad():
    correct = 0
    total = 0
    for i, sample in enumerate(test_loader):
        outputs = model(sample['image'])
        print(outputs.data)
        _, predicted = torch.max(outputs.data, 1)
        total += sample['labels'].size(0)
        print(predicted)
        print(sample['labels'])

    print('Test Accuracy of the model on the test images: {} %'.format(100 * correct / total))

# Save the model checkpoint
torch.save(model.state_dict(), 'model.ckpt')
