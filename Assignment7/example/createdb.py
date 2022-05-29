import torch
import numpy as np
from constants import *

def createDB():
    distributions = (DOMAIN_UPPER_BOUND - DOMAIN_LOWER_BOUND) * torch.rand(DATA_SET_SIZE, INPUT_SIZE) + DOMAIN_LOWER_BOUND

    print(distributions)

    output_data = []

    for value in distributions.numpy():
        output_data.append(np.sin(value[0] + value[1]/np.pi))

    tensor = torch.tensor(output_data)

    return torch.column_stack((distributions, tensor))


def save_db():
    torch.save(createDB(), "dataset.dat")



