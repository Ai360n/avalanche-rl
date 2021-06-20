import torch.nn as nn
import torch
import torch.nn.functional as F


class ConvDeepQN(nn.Module):
    # network architecture from Mnih et al 2015 - "Human-level Control Through Deep Reinforcement Learning"
    def __init__(self, input_channels, image_shape, n_actions, batch_norm=False):
        super(ConvDeepQN, self).__init__()
        # 4x84x84 input in original paper
        self.conv1 = nn.Conv2d(input_channels, 32, 8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, 4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, 3, stride=1)

        self.fc = nn.Sequential(
            nn.Linear(
                self._compute_flattened_shape(
                    (input_channels, image_shape[0],
                     image_shape[1])),
                512),
            nn.ReLU(),
            nn.Linear(512, n_actions))

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        # feed to linear layer
        x = x.flatten(1)
        return self.fc(x)

    def _compute_flattened_shape(self, input_shape):
        x = torch.zeros(input_shape)
        x = x.unsqueeze(0)
        with torch.no_grad():
            x = self.conv1(x)
            x = self.conv2(x)
            x = self.conv3(x)
        print("Size of flattened input to fully connected layer:", x.flatten().shape)
        return x.squeeze(0).flatten().shape[0]
