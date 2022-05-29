import torch
import torch.nn as nn
import torch.optim as optim
import time
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, models, transforms
from PIL import Image
from torchvision.datasets.folder import pil_loader

device = torch.device('cuda:0' if torch.cuda.is_available() else
                      'cpu')


class ImageClassifierDataset(Dataset):
    def __init__(self, image_list, image_classes):
        self.images = []
        self.labels = []
        self.classes = list(set(image_classes))
        self.class_to_label = {c: i for i, c in enumerate(self.classes)}
        self.image_size = 224
        self.transforms = transforms.Compose([transforms.Resize(self.image_size),
                                              transforms.CenterCrop(self.image_size),
                                              transforms.ToTensor(),
                                              transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                                              ])
        for image, image_class in zip(image_list, image_classes):
            transformed_image = self.transforms(image)
            self.images.append(transformed_image)
            label = self.class_to_label[image_class]
            self.labels.append(label)

    def __getitem__(self, index):
        return self.images[index], self.labels[index]

    def __len__(self):
        return len(self.images)


def get_image_classifier_dataset_train():
    return ImageClassifierDataset([
        pil_loader("humans/f1.jpg").convert("RGB"),
        pil_loader("humans/f2.jpg").convert("RGB"),
        pil_loader("humans/f3.jpg").convert("RGB"),
        pil_loader("humans/f4.jpg").convert("RGB"),
        pil_loader("humans/f5.jpg").convert("RGB"),
        pil_loader("humans/f6.jpg").convert("RGB"),
        pil_loader("humans/f7.jpg").convert("RGB"),
        pil_loader("humans/f8.jpg").convert("RGB"),
        pil_loader("humans/f9.jpg").convert("RGB"),
        pil_loader("humans/f10.jpg").convert("RGB"),
        pil_loader("humans/f11.jpg").convert("RGB"),
        pil_loader("humans/f12.jpg").convert("RGB"),
        pil_loader("humans/f13.jpg").convert("RGB"),
        pil_loader("humans/f14.jpg").convert("RGB"),
        pil_loader("humans/f15.jpg").convert("RGB"),
        pil_loader("humans/f16.jpg").convert("RGB"),
        pil_loader("humans/f17.jpg").convert("RGB"),
        pil_loader("humans/f18.jpg").convert("RGB"),
        pil_loader("humans/f19.jpg").convert("RGB"),
        pil_loader("humans/f20.jpg").convert("RGB"),
        pil_loader("humans/f21.jpg").convert("RGB"),
        pil_loader("humans/f22.jpg").convert("RGB"),
        pil_loader("humans/f23.jpg").convert("RGB"),
        pil_loader("humans/f24.jpg").convert("RGB"),
        pil_loader("humans/f25.jpg").convert("RGB"),
        pil_loader("humans/f26.jpg").convert("RGB"),
        pil_loader("humans/f27.jpg").convert("RGB"),
        pil_loader("humans/f28.jpg").convert("RGB"),
        pil_loader("humans/f29.jpg").convert("RGB"),
        pil_loader("humans/f30.jpg").convert("RGB"),
        pil_loader("humans/f31.jpg").convert("RGB"),
        pil_loader("humans/f32.jpg").convert("RGB"),
        pil_loader("humans/f33.jpg").convert("RGB"),
        pil_loader("humans/f34.jpg").convert("RGB"),
        pil_loader("humans/f35.jpg").convert("RGB"),
        pil_loader("humans/f36.jpg").convert("RGB"),
        pil_loader("humans/f37.jpg").convert("RGB"),
        pil_loader("humans/f38.jpg").convert("RGB"),
        pil_loader("humans/f39.jpg").convert("RGB"),
        pil_loader("humans/f40.jpg").convert("RGB"),
        pil_loader("humans/b1.jpg").convert("RGB"),
        pil_loader("humans/b2.jpg").convert("RGB"),
        pil_loader("humans/b3.jpg").convert("RGB"),
        pil_loader("humans/b4.jpg").convert("RGB"),
        pil_loader("humans/b5.jpg").convert("RGB"),
        pil_loader("humans/b6.jpg").convert("RGB"),
        pil_loader("humans/b7.jpg").convert("RGB"),
        pil_loader("humans/b8.jpg").convert("RGB"),
        pil_loader("humans/b9.jpg").convert("RGB"),
        pil_loader("humans/b10.jpg").convert("RGB"),
        pil_loader("humans/b11.jpg").convert("RGB"),
        pil_loader("humans/b12.jpg").convert("RGB"),
        pil_loader("humans/b13.jpg").convert("RGB"),
        pil_loader("humans/b14.jpg").convert("RGB"),
        pil_loader("humans/b15.jpg").convert("RGB"),
        pil_loader("humans/b16.jpg").convert("RGB"),
        pil_loader("humans/b17.jpg").convert("RGB"),
        pil_loader("humans/b18.jpg").convert("RGB"),
        pil_loader("humans/b19.jpg").convert("RGB"),
        pil_loader("humans/b20.jpg").convert("RGB"),
        pil_loader("humans/b21.jpg").convert("RGB"),
        pil_loader("humans/b22.jpg").convert("RGB"),
        pil_loader("humans/b23.jpg").convert("RGB"),
        pil_loader("humans/b24.jpg").convert("RGB"),
        pil_loader("humans/b25.jpg").convert("RGB"),
        pil_loader("humans/b26.jpg").convert("RGB"),
        pil_loader("humans/b27.jpg").convert("RGB"),
        pil_loader("humans/b28.jpg").convert("RGB"),
        pil_loader("humans/b29.jpg").convert("RGB"),
        pil_loader("humans/b30.jpg").convert("RGB"),
        pil_loader("humans/b31.jpg").convert("RGB"),
        pil_loader("humans/b32.jpg").convert("RGB"),
        pil_loader("humans/b33.jpg").convert("RGB"),
        pil_loader("humans/b34.jpg").convert("RGB"),
        pil_loader("humans/n1.jpg").convert("RGB"),
        pil_loader("humans/n2.jpg").convert("RGB"),
        pil_loader("humans/n3.jpg").convert("RGB"),
        pil_loader("humans/n4.jpg").convert("RGB"),
        pil_loader("humans/n5.jpg").convert("RGB"),
        pil_loader("humans/n6.jpg").convert("RGB"),
        pil_loader("humans/n7.jpg").convert("RGB"),
        pil_loader("humans/n8.jpg").convert("RGB"),
        pil_loader("humans/n9.jpg").convert("RGB"),
        pil_loader("humans/n10.jpg").convert("RGB"),
        pil_loader("humans/n11.jpg").convert("RGB"),
        pil_loader("humans/n12.jpg").convert("RGB"),
        pil_loader("humans/n13.jpg").convert("RGB"),
        pil_loader("humans/n14.jpg").convert("RGB"),
        pil_loader("humans/n15.jpg").convert("RGB"),
        pil_loader("humans/n16.jpg").convert("RGB"),
        pil_loader("humans/n17.jpg").convert("RGB"),
        pil_loader("humans/n18.jpg").convert("RGB"),
        pil_loader("humans/n19.jpg").convert("RGB"),
        pil_loader("humans/n20.jpg").convert("RGB"),
        pil_loader("humans/n21.jpg").convert("RGB"),
        pil_loader("humans/n22.jpg").convert("RGB"),
        pil_loader("humans/n23.jpg").convert("RGB"),
        pil_loader("humans/n24.jpg").convert("RGB"),
        pil_loader("humans/n25.jpg").convert("RGB"),
        pil_loader("humans/n26.jpg").convert("RGB"),
        pil_loader("humans/n27.jpg").convert("RGB"),
        pil_loader("humans/n28.jpg").convert("RGB"),
        pil_loader("humans/n29.jpg").convert("RGB"),
        pil_loader("humans/n30.jpg").convert("RGB"),
        pil_loader("humans/n31.jpg").convert("RGB"),
        pil_loader("humans/n32.jpg").convert("RGB"),
        pil_loader("humans/n33.jpg").convert("RGB"),
        pil_loader("humans/n34.jpg").convert("RGB"),
        pil_loader("humans/n35.jpg").convert("RGB"),
        pil_loader("humans/n36.jpg").convert("RGB"),
        pil_loader("humans/n37.jpg").convert("RGB"),
        pil_loader("humans/n38.jpg").convert("RGB"),
        pil_loader("humans/n39.jpg").convert("RGB"),
        pil_loader("humans/n40.jpg").convert("RGB"),
    ], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0
        ])


def get_image_classifier_dataset_test():
    return ImageClassifierDataset([
        pil_loader("humans/f35.jpg").convert("RGB"),
        pil_loader("humans/f36.jpg").convert("RGB"),
        pil_loader("humans/f37.jpg").convert("RGB"),
        pil_loader("humans/f38.jpg").convert("RGB"),
        pil_loader("humans/f39.jpg").convert("RGB"),
        pil_loader("humans/f40.jpg").convert("RGB"),
        pil_loader("humans/f41.jpg").convert("RGB"),
        pil_loader("humans/f42.jpg").convert("RGB"),
        pil_loader("humans/f43.jpg").convert("RGB"),
        pil_loader("humans/f44.jpg").convert("RGB"),
        pil_loader("humans/f45.jpg").convert("RGB"),
        pil_loader("humans/f46.jpg").convert("RGB"),
        pil_loader("humans/f47.jpg").convert("RGB"),
        pil_loader("humans/f48.jpg").convert("RGB"),
        pil_loader("humans/f49.jpg").convert("RGB"),
        pil_loader("humans/f50.jpg").convert("RGB"),
        pil_loader("humans/b35.jpg").convert("RGB"),
        pil_loader("humans/b36.jpg").convert("RGB"),
        pil_loader("humans/b37.jpg").convert("RGB"),
        pil_loader("humans/b38.jpg").convert("RGB"),
        pil_loader("humans/b39.jpg").convert("RGB"),
        pil_loader("humans/b40.jpg").convert("RGB"),
        pil_loader("humans/b41.jpg").convert("RGB"),
        pil_loader("humans/b42.jpg").convert("RGB"),
        pil_loader("humans/b43.jpg").convert("RGB"),
        pil_loader("humans/b44.jpg").convert("RGB"),
        pil_loader("humans/b45.jpg").convert("RGB"),
        pil_loader("humans/b46.jpg").convert("RGB"),
        pil_loader("humans/b47.jpg").convert("RGB"),
        pil_loader("humans/b48.jpg").convert("RGB"),
        pil_loader("humans/b49.jpg").convert("RGB"),
        pil_loader("humans/b50.jpg").convert("RGB"),
        pil_loader("humans/n35.jpg").convert("RGB"),
        pil_loader("humans/n36.jpg").convert("RGB"),
        pil_loader("humans/n37.jpg").convert("RGB"),
        pil_loader("humans/n38.jpg").convert("RGB"),
        pil_loader("humans/n39.jpg").convert("RGB"),
        pil_loader("humans/n40.jpg").convert("RGB"),
        pil_loader("humans/n41.jpg").convert("RGB"),
        pil_loader("humans/n42.jpg").convert("RGB"),
        pil_loader("humans/n43.jpg").convert("RGB"),
        pil_loader("humans/n44.jpg").convert("RGB"),
        pil_loader("humans/n45.jpg").convert("RGB"),
        pil_loader("humans/n46.jpg").convert("RGB"),
        pil_loader("humans/n47.jpg").convert("RGB"),
        pil_loader("humans/n48.jpg").convert("RGB"),
        pil_loader("humans/n49.jpg").convert("RGB"),
        pil_loader("humans/n50.jpg").convert("RGB"),
    ], [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
    ])


train = get_image_classifier_dataset_train()
# test = get_image_classifier_dataset_test()