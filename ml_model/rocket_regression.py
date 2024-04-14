import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
import glob
import random
import wandb
import torch.nn.functional as F

learning_rate = 0.0005
num_epochs =  80

input_size = 20
hidden_size_1 = 128
hidden_size_2 = 64
output_size = 1
num_batch = 4

#Initialise weights and biases
wandb.init(
    # Set the project where this run will be logged
    project="trash_collision_hackathon_fnn",
    # Track hyperparameters and run metadata
    config={
        "learning_rate": learning_rate,
        "epochs": num_epochs,
        "hidden_size_1": 128,
        "hidden_size_2": 64,
        "output_size":1,
        "num_batch":2,
    },
)

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

#Create a simple fully connected network with two hidden layers
class RocketLaunchRegression(nn.Module):
    def __init__(self, input_size, hidden_size_1, hidden_size_2, output_size):
        super(RocketLaunchRegression, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size_1)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size_1, hidden_size_2)
        self.fc3 = nn.Linear(hidden_size_2,output_size)


    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x

class Dataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file, header=None)  # The header will be automatically inferred
        self.features = self.data.iloc[:, :-1].values.astype(np.float32)
        print(self.features.shape)
        self.labels = self.data.iloc[:, -1].values.astype(np.float32)
        print(self.labels.shape)

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sample = {
            'features': torch.tensor(self.features[idx]),
            'label': torch.tensor(self.labels[idx])
        }
        return sample


csv_file = "data.csv"
dataset = Dataset(csv_file)
dataloader = DataLoader(dataset, batch_size=num_batch, shuffle=True)

net = RocketLaunchRegression(input_size, hidden_size_1, hidden_size_2, output_size)
net.train()
criterion = nn.MSELoss()
optimizer = optim.Adam(net.parameters(), lr=learning_rate)

# Training loop
for epoch in range(num_epochs):
    running_loss = 0.0
    for i, batch in enumerate(dataloader):
        features, labels = batch['features'], batch['label']
        # Zero the parameter gradients
        optimizer.zero_grad()
        
        # Forward pass
        outputs = net(features)
        loss = criterion(outputs.squeeze(), labels.float()) # Squeeze to make the shape compatible
        
        # Backward pass and optimization
        loss.backward()
        optimizer.step()
        
        # Print statistics
        running_loss += loss.item()
        if (i+1) % 100 == 0:  # Print every 100 mini-batches
            print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(dataloader)}], Loss: {running_loss/100:.4f}')
            running_loss = 0.0
        wandb.log({"loss": loss.item()})

# Define the file path to save the weights
weights_path = "model_weights.pth"

# Save the current weights of the model
torch.save(net.state_dict(), weights_path)

# Load the test dataset
test_csv_file = "test_data.csv"
test_dataset = Dataset(test_csv_file)
test_loader = DataLoader(test_dataset, batch_size=num_batch, shuffle=False)

# Evaluation loop
with torch.no_grad():
    net.eval()  # Set the model to evaluation mode
    test_loss = 0.0
    for i, batch in enumerate(test_loader):
        features, labels = batch['features'], batch['label']
        outputs = net(features)
        loss = criterion(outputs.squeeze(), labels.float())
        test_loss += loss.item()
    average_test_loss = test_loss / len(test_loader)
    print(f'Test - Average Loss: {average_test_loss:.4f}')
    wandb.log({"test_loss": average_test_loss})
    net.train()  # Set the model back to training mode

# Evaluation loop for accuracy calculation
threshold = 0.5  # Define a threshold for accuracy calculation
correct_predictions = 0
total_samples = 0

with torch.no_grad():
    net.eval()  # Set the model to evaluation mode
    for i, batch in enumerate(test_loader):
        features, labels = batch['features'], batch['label']
        outputs = net(features)
        predictions = outputs.numpy()  # Convert predictions to numpy array
        labels = labels.numpy()  # Convert labels to numpy array
        
        # Calculate accuracy
        correct_predictions += np.sum(np.abs(predictions - labels) < threshold)
        total_samples += len(predictions)

accuracy = correct_predictions / total_samples
print(f'Test Accuracy: {accuracy * 100:.2f}%')
wandb.log({"test_accuracy": accuracy})
net.train()  # Set the model back to training mode
