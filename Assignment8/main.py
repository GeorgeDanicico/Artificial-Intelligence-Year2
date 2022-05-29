# load and show an image with Pillow
from PIL import Image
# load and display an image with Matplotlib
from matplotlib import image
from matplotlib import pyplot

print("TASK 1")

print("Task A --------------------------------")
# load the image
im = Image.open('f1.jpg')
# summarize some details about the image
print(im.format)
print(im.mode)
print(im.size)
# show the image
im.show()

print("Task B --------------------------------")
# load image as pixel array
data = image.imread('f1.jpg')
# summarize shape of the pixel array
print(data.dtype)
print(data.shape)
pyplot.imshow(data)
pyplot.show()

print("Task C --------------------------------")
im = Image.open('f1.jpg')
# report the size of the image
print(im.size)
# create a thumbnail and preserve aspect ratio
im.thumbnail((100,100))
# report the size of the thumbnail
print(im.size)