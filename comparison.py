from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np
import sys

# Load the images
image1 = Image.open('./img/design-2.jpeg')#orignal design
image2 = Image.open('./img/design-2edit.jpeg')#cropped design
# image1 = Image.open('./img/'+sys.argv[1])
# image2 = Image.open('./img/'+sys.argv[2])

# Resize the images to the same dimensions
image1 = image1.resize((500, 500), resample=Image.BILINEAR)
image2 = image2.resize((500, 500), resample=Image.BILINEAR)

# Convert the images to grayscale
image1 = image1.convert('L')
image2 = image2.convert('L')

# Compute the SSIM similarity score
ssim_score = ssim(np.array(image1), np.array(image2))

# Print the similarity score
print(f"SSIM: {ssim_score}")