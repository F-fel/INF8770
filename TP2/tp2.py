import csv
from PIL import Image
import PIL
import cmath
import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
images =[]
JPEG_DIR = "jpeg/"
JP2_DIR = "JPEG2000/"
SRC_DIR = "pics/"
for filename in os.listdir("pics"):
    images.append(filename)
def compress():
    for x in images:
        im_jpg = Image.open(SRC_DIR  + x)
        im_j2p = Image.open(SRC_DIR + x)
        x = x[:-4]
        im_jpg.save('jpeg/{}.jpg'.format(x),optimize=True,quality=50)
        im_j2p.save('jpeg2000/{}.jp2'.format(x), format='JPEG2000', quality_mode="rates", quality_layers=[20,20])
        im_j2p.close()
        im_jpg.close()
def PSNR(im1, im2):
    # credits to geeksforgeeks
    mse = np.mean((im1 - im2) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * cmath.log10(max_pixel / cmath.sqrt(mse))
    return psnr
def compare(stats = {}):
    for filename in images:
        original = cv2.imread(SRC_DIR+filename)
        filename = filename[:-4]
        jpeg = cv2.imread('{}{}.jpg'.format(JPEG_DIR,filename))
        jp2 = cv2.imread('{}{}.jp2'.format(JP2_DIR,filename))
        axis = original.shape[2]
        (jpeg_ssim, jpeg_diff) = compare_ssim(original, jpeg,gaussian_weights=True, full=True, channel_axis=axis-1)
        (jp2_ssim, jp2_diff)   = compare_ssim(original, jpeg,gaussian_weights=True, full=True, channel_axis=axis-1)
        jpeg_psnr ,jp2_psnr    = PSNR(original, jpeg) , PSNR(original,jp2)
        stats[filename] = stats[filename] + [jpeg_ssim, jpeg_psnr, jp2_ssim, jp2_psnr]


def getStats():
    stats = {}
    for filename in images:
        og_size = os.path.getsize(SRC_DIR +filename)
        filename = filename[:-4]
        jpeg_size = os.path.getsize('{}{}.jpg'.format(JPEG_DIR,filename))
        jp2_size = os.path.getsize('{}{}.jp2'.format(JP2_DIR,filename))
        jp2_ratio = og_size/jp2_size
        jpeg_ratio = og_size/jpeg_size
        stats[filename] = [og_size,jpeg_size,jpeg_ratio,jp2_size,jp2_ratio]
    return stats
def make_clean():
    # delete all files in the utput directories
    for filename in images:
        os.remove(JPEG_DIR+filename)
        os.remove(JP2_DIR+filename)
if __name__ == "__main__":
    compress()
    stats = getStats()
    compare(stats)
    with open('stats.csv', 'w',newline='') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(["file name","og size", "jpeg size", "jpeg ratio", "jp2 size", "jp2_ratio", "jpeg SSIM", "jpeg psnr","jp2 SSIM", "jp2 psnr"])
        for key, value in stats.items():
            row = [key]
            for x in value:
                row.append(x)
            writer.writerow(row)

