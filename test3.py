import cv2

# Load the two images
img1 = cv2.imread('./img/sample.jpg')
img2 = cv2.imread('./img/sample.jpg')

# Resize the images to the same dimensions
img1 = cv2.resize(img1, (300, 300))
img2 = cv2.resize(img2, (300, 300))

# Calculate the MSE between the two images
mse = ((img1 - img2) ** 2).mean()

print(f"MSE: {mse}")
