import torch.nn as nn
import matplotlib.pyplot as plt


class MangaNet(nn.Module):

    def __init__(self, num_classes=1000):
        super(MangaNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=5, stride=2, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv2d(16, 16, kernel_size=3, stride=2, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),

            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 128, kernel_size=2, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(13 * 9 * 128, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(1024, 1024),
            nn.ReLU(inplace=True),
            nn.Linear(1024, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), 13 * 9 * 128)
        x = self.classifier(x)
        return x
