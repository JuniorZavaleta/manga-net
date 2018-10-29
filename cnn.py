import torch.nn as nn


class MangaNet(nn.Module):

    def __init__(self, num_classes=8):
        super(MangaNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, stride=2, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv2d(16, 16, kernel_size=3, stride=2, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),

            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 256, kernel_size=2, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Linear(4 * 6 * 256, 1024, bias=False),
            nn.Dropout(),
            nn.ReLU(),
            nn.Linear(1024, 1024, bias=False),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(1024, 256, bias=False),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(256, num_classes, bias=False),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(-1, 4 * 6 * 256)
        x = self.classifier(x)
        return x
