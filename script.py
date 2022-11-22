import sys

import cv2
import extcolors
from colormap import rgb2hex
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def justprint():
     print('hello');
     x = Image.open(r"./uploads/images.jpeg")
     img = extcolors.extract_from_image(x)
     print(img)
     sys.stdout.flush()

justprint()