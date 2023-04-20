import cv2
import numpy as np

# Load the two images
img1 = cv2.imread('./img/sample_tshirt-edit.jpg')
img2 = cv2.imread('./img/sample_tshirt.jpg')

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
cv2.imshow('Aligned', aligned)
cv2.imwrite(filePath, aligned)
cv2.waitKey(0)
cv2.destroyAllWindows()
