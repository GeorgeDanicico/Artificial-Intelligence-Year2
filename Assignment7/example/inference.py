# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 14:20:51 2021

@author: tudor
"""

import torch
import torch.nn.functional as F

import myModel
from createdb import save_db
from trainmodel import save_to_file


save_db()

# saves the train model
save_to_file()

# we load the model

filepath = "myNetwork.pt"
ann = myModel.Net(2, 20, 1)

ann.load_state_dict(torch.load(filepath))
ann.eval()

while True:
    x1 = float(input("x1 = "))
    x2 = float(input("x2 = "))
    tensor = torch.tensor([x1, x2])
    print(ann(tensor).item())

# visualise the parameters for the ann (aka weights and biases)
# for name, param in ann.named_parameters():
#     if param.requires_grad:
#         print (name, param.data)