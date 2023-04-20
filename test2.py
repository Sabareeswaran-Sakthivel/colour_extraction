import sys
from skimage.metrics import structural_similarity
import cv2
import numpy as np
from PIL import Image

def getRgb(x, y): 
          
        image = Image.open('img/'+ sys.argv[1])
        # image = Image.open('./img/sample_tshirt.jpg')

        # Get the RGB value at x=100, y=200
        pixel_rgb = image.getpixel((x, y))

        # Print the RGB value
        # print(x)
        # print(y)
        print(pixel_rgb)

def align(edit, original):
        # Load the two images
        img1 = cv2.imread('./img/' + edit)
        img2 = cv2.imread('./img/' + original)
        # img1 = cv2.imread('./img/sample_tshirt-edit.jpg')
        # img2 = cv2.imread('./img/sample_tshirt.jpg')

        # Convert the images to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Detect and extract features from the images using the ORB feature detector
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(gray1, None)
        kp2, des2 = orb.detectAndCompute(gray2, None)

        # Match the features in the two images using a brute-force matcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        # Sort the matches by their distance
        matches = sorted(matches, key=lambda x: x.distance)

        # Select the top N matches (you can adjust this value to improve registration accuracy)
        N = 50
        matches = matches[:N]

        # Extract the corresponding keypoints from the two images
        pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        # Compute the homography matrix that maps the points in img1 to the points in img2
        H, _ = cv2.findHomography(pts1, pts2, cv2.RANSAC)

        # Warp img1 to align with img2 using the homography matrix
        aligned = cv2.warpPerspective(img1, H, (img2.shape[1], img2.shape[0]))

        # Display the aligned image
        filePath = './align/align.png'
        # cv2.imshow('Aligned', aligned)
        cv2.imwrite(filePath, aligned)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def colourCompare():
        filePath = './uploads/mask.png'
        # new_size = (195, 210.5)
        # new_size = (216, 232)
        # print(sys.argv[1])
        # print(sys.argv[2])
        align(sys.argv[2], sys.argv[1])
        before = cv2.imread("./img/"+sys.argv[1])
        after = cv2.imread("./align/align.png")

        # before = cv2.imread("./img/sample_tshirt.jpg")
        # after = cv2.imread("./uploads/align.png")

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
        # print("Image similarity", score*100)
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
                getRgb((x+w - x)/2 + x, (y+h - y)/2 + y)
                cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 2)
                cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
                cv2.drawContours(mask, [c], 0, (0,255,0), -1)
                cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)

        # cv2.imshow('before', before)
        # cv2.imshow('after', after)
        # cv2.imshow('diff',diff)
        cv2.imshow('mask',mask)
        cv2.imwrite(filePath, after)
        # cv2.imshow('filled after',filled_after)
        cv2.waitKey(0)
        # print("ll")
        sys.stdout.flush()


colourCompare()

