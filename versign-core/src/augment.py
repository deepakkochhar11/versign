#########################################################################################
# This script takes two arguments, inDir and outDir, and augments the input data in     #
# inDir by generating four new images for each image in the input data. Augmentation is #
# performed by performing minor transformations (rotation, etc.) on input data.         #
#########################################################################################
#from preprocess import ImageProcessor
from PIL import Image

import cv2, random, os, numpy as np, sys
from preprocess.resize import center_inside


def otsu(image):
    blur = cv2.GaussianBlur(image, (5,5), 0)
    ret, bin = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return bin

def randomRotate(image, min=-5, max=5):
    im2 = image.convert("RGBA")
    rot = im2.rotate(random.uniform(min, max), expand=True)
    fff = Image.new("RGBA", rot.size, (255,)*4)
    out = Image.composite(rot, fff, rot)
    return out.convert(image.mode)

def augment(inDir, outDir):
    # Path of input directory
    if not inDir.endswith("/"):
        inDir += "/"

    # Path where augmented data will be saved
    if not outDir.endswith("/"):
        outDir += "/"

    # No. of copies of to create
    copies = 4

    # Max angle to rotate through
    aMax = 5

    # For each image file in the input directory
    for file in os.listdir(inDir):
        if not file.endswith(".jpg") and not file.endswith(".png"):   # Ignore non-images
            continue

        # Extract file name and extension
        fn = file[:-4]
        ext = "." + file.split(".")[-1]

        # Apply OTSU thresholding on input image and save it
        outFile = outDir + fn + "0" + ext
        #cv2.imwrite(outFile, otsu(cv2.imread(inDir +  fn + ext, 0)))
        cv2.imwrite(outFile, cv2.imread(inDir +  fn + ext, 0))

        # Crop and normalize image's size
        cropped = center_inside(cv2.imread(outFile, 0), canvas_size=(150, 220))
        cv2.imwrite(outFile, cropped)

        # Augment input data by rotating image at random angles in range (-5, 5)
        image = Image.open(outFile)
        for i in range(0, copies):
            rotated = randomRotate(image, min=-aMax, max=aMax)
            rotated = Image.fromarray(center_inside(np.array(rotated), canvas_size=(150, 220)))
            rotated.save(outDir + fn + str(i + 1) + ext)

def main():
    # Validate command-line arguments
    if len(sys.argv) < 3:
        print "\nUsage:\tpython", sys.argv[0], "<input-folder> <output-folder>\n"
        return

    inDir = sys.argv[1]
    outDir = sys.argv[2]

    augment(inDir, outDir)

if __name__ == "__main__":
    main()