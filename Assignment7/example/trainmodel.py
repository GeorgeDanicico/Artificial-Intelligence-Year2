import torch

from example.myModel import Net
from constants import *

def train_model():
    data_set = torch.load("dataset.dat")

    input_data = data_set.narrow(1, 0, 2)
    output_data = data_set.narrow(1, 2, 1)

    input_data_chunks = torch.split(input_data, 20)  # 20 is the batch size
    output_data_chunks = torch.split(output_data, 20)

    # we set up the lossFunction as the mean square error
    lossFunction = torch.nn.MSELoss()

    # we create the ANN
    ann = Net(n_feature=2, n_hidden=20, n_output=1).double()

    # print(ann)
    # we use an optimizer that implements stochastic gradient descent
    optimizer_batch = torch.optim.SGD(ann.parameters(), lr=0.02)

    # we memorize the losses forsome graphics
    loss_list = []
    avg_loss_list = []

    # we set up the environment for training in batches
    batch_size = 20
    n_batches = DATA_SET_SIZE // batch_size
    print(n_batches)

    for epoch in range(4000):

        for batch in range(n_batches):
            # we prepare the current batch  -- please observe the slicing for tensors
            # we compute the output for this batch
            prediction = ann(input_data_chunks[batch].double())

            # we compute the loss for this batch
            loss = lossFunction(prediction, output_data_chunks[batch])

            # we save it for graphics
            loss_list.append(loss)

            # we set up the gradients for the weights to zero (important in pytorch)
            optimizer_batch.zero_grad()

            # we compute automatically the variation for each weight (and bias) of the network
            loss.backward()

            # we compute the new values for the weights
            optimizer_batch.step()

        # we print the loss for all the dataset for each 10th epoch
        if epoch % 100 == 99:
            y_pred = ann(input_data.double())
            loss = lossFunction(y_pred, output_data)
            print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))

    return ann


def save_to_file():

    ann = train_model()
    torch.save(ann.state_dict(), "myNetwork.pt")
