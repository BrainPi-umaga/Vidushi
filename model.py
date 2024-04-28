import torch.nn as nn

class VoiceCommandModel(nn.Module):
    def __init__(self):
        super(VoiceCommandModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=(3, 3), padding=(1, 1))  # Conv layer to process MFCCs
        self.lstm = nn.LSTM(32, 128, batch_first=True)  # LSTM layer for sequence processing
        self.fc = nn.Linear(128, 10)  # Output layer, assuming 10 classes

    def forward(self, x):
        x = x.unsqueeze(1)  # Add channel dimension
        x = torch.relu(self.conv1(x))
        x = x.squeeze(1).transpose(1, 2)  # Prepare for LSTM
        _, (hn, _) = self.lstm(x)
        x = hn.squeeze(0)  # Take the last hidden state
        x = self.fc(x)
        return torch.log_softmax(x, dim=1)

model = VoiceCommandModel()
