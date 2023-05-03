import sys
from skimage.metrics import structural_similarity
import cv2
import numpy as np
from PIL import Image

def getRgb(x, y): 
          
        image = Image.open('img/'+ sys.argv[1])
        # image = Image.open('./img/vinayag-1.jpg')

        # Get the RGB value at x=100, y=200
        pixel_rgb = image.getpixel((x, y))

        # Print the RGB value
        # print(x)
        # print(y)
        print(pixel_rgb)

def colourCompare():
        filePath = './uploads/mask.png'
        # new_size = (195, 210.5)
        # new_size = (216, 232)
        # print(sys.argv[1])
        # print(sys.argv[2])
     #    before = cv2.imread("./tmp/"+sys.argv[1])
     #    after = cv2.imread("./tmp/" + sys.argv[2])

        before = cv2.imread('./img/thaila.jpeg')
        after = cv2.imread('./img/thaila1.jpeg')

        # img = cv2.imread('./img/sample_tshirt.jpg')

        # height, width, channels = img.shape

        # print('Image size: {} x {} pixels, {} channels'.format(width, height, channels))

        # img2 = cv2.imread("./uploads/align.png")
        # height1, width1, channels1 = img2.shape

        # print('Image size: {} x {} pixels, {} channels'.format(width1, height1, channels1))

        # before1 = cv2.resize(before, new_size)
        # after1 = cv2.resize(after, new_size)

        # Convert images to grayscale
        before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
        after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

        # Compute SSIM between two images
        (score, diff) = structural_similarity(before_gray, after_gray, full=True)
        print("Image similarity", score*100-1)
        diff = (diff * 255).astype("uint8")

        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        mask = np.zeros(before.shape, dtype='uint8')
        filled_after = after.copy()

        for c in contours:
            area = cv2.contourArea(c)
            if area > 40:
                x,y,w,h = cv2.boundingRect(c)
               #  getRgb((x+w - x)/2 + x, (y+h - y)/2 + y)
                cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 2)
                cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
                cv2.drawContours(mask, [c], 0, (0,255,0), -1)
                cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)

        cv2.imshow('before', before)
        cv2.imshow('after', after)
        cv2.imshow('diff',diff)
     #    cv2.imshow('mask',mask)
        cv2.imwrite(filePath, after)
        # cv2.imshow('filled after',filled_after)
        cv2.waitKey(0)
        # print("llonemore1")
        sys.stdout.flush()


colourCompare()

