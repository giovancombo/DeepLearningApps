# Deep Learning Applications 2023 course, held by Professor Andrew David Bagdanov - University of Florence, Italy
# Created by Giovanni Colombo - Mat. 7092745
# Dedicated Repository on GitHub at https://github.com/giovancombo/DLA_Labs/tree/main/lab2

import torch
import torch.nn as nn


class MLP(nn.Module):
        def __init__(self, hidden_size, classes):
            super(MLP, self).__init__()
            self.fc1 = nn.Linear(768, hidden_size)
            self.fc2 = nn.Linear(hidden_size, classes)
        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = self.fc2(x)
            return x

# Training Loop
def training_mlp(model, optimizer, criterion, epochs, batch_size, train_features, train_labels, test_features, test_labels, device):
    for epoch in range(epochs):
        model.train()
        for i in range(0, len(train_features), batch_size):
            optimizer.zero_grad(set_to_none = True)
            X = torch.tensor(train_features[i : i + batch_size], dtype = torch.float).to(device)
            Y = torch.tensor(train_labels[i : i + batch_size], dtype = torch.long).to(device)
            outputs = model(X)
            loss = criterion(outputs, Y)
            loss.backward()
            optimizer.step()

        # Evaluation
        total, correct = 0, 0
        model.eval()
        for i in range(0, len(test_features), batch_size):
            Xval = torch.tensor(test_features[i : i + batch_size], dtype = torch.float).to(device)
            Yval = torch.tensor(test_labels[i : i + batch_size], dtype = torch.long).to(device)
            outputs = model(Xval)   
            _, pred = torch.max(outputs.data, 1)
            total += Yval.size(0)
            correct += (pred == Yval).sum().item()
        test_accuracy = 100 * correct / total
        print(f"Epoch {epoch+1}/{epochs}:\tTraining Loss = {loss.item():.4f}   Test Accuracy = {test_accuracy:.2f}%")

    print("\nTraining completed!")
