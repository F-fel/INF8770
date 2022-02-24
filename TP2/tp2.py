from PIL import Image
import PIL
import cmath
import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
images =[]
for filename in os.listdir("pics"):
    images.append(filename)
def compress():
    for x in images:
        picture = Image.open('pics/'  + x)
        x = x[:-4]
        file_name ='jpeg/' +x+'.jpg'
        picture.save(file_name,optimize=True,quality=5)
        picture.close()
def PSNR(im1, im2):
    # credits to geeksforgeeks
    mse = np.mean((im1 - im2) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * cmath.log10(max_pixel / cmath.sqrt(mse))
    return psnr
def compare():
    for filename in images:
        original = cv2.imread('pics/'+filename)
        filename = filename[:-4]
        compressed = cv2.imread('jpeg/'+filename+'.jpg')
        height = original.shape[0]
        width = original.shape[1]
        axis = original.shape[2]
        (score, diff) = compare_ssim(original, compressed,gaussian_weights=True, full=True, channel_axis=axis-1)
        diff = (diff * 255).astype("uint8")
        print("SSIM: {}".format(score))
        print(PSNR(original,compressed))
compress()
compare()
