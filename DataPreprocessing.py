import os
import torchaudio
import torch
from torch.utils.data import Dataset, DataLoader
from torchaudio.transforms import MFCC

class VoiceCommandDataset(Dataset):
    def __init__(self, directory):
        """
        Args:
            directory (string): Directory with all the voice samples.
        """
        self.directory = directory
        self.files = [os.path.join(root, file)
                      for root, _, files in os.walk(directory)
                      for file in files if file.endswith('.wav')]

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        waveform, sample_rate = torchaudio.load(self.files[idx])
        mfcc_transform = MFCC(sample_rate=sample_rate, n_mfcc=13,
                              melkwargs={'n_fft': 400, 'hop_length': 160, 'n_mels': 23, 'center': False})
        mfcc = mfcc_transform(waveform)
        mfcc = mfcc.mean(dim=0)  # Average across channels
        label = int(self.files[idx].split('/')[-2][-1])  # Assuming label is part of the directory name
        return mfcc, label

# Usage
