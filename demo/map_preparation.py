# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # Load the image in grayscale
# image_path = "demo/map.png"
# image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# # Apply binary thresholding
# _, binary_mask = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

# # Define a kernel for morphological operations
# kernel = np.ones((5, 5), np.uint8)

# # Perform morphological closing to remove small gaps and thin lines
# closed_image = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)


# # Display the cleaned image
# plt.imshow(closed_image, cmap='gray')
# plt.axis('off')  # Optional: Hide axis for better visualization
# plt.show()




import cv2
import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue
import math
import random


# Load the map image
image_path = "demo/map.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Threshold the image to create a binary map (black=0, white=255)
_, binary_map = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)  # invert so black is 255

# Define a kernel for morphological operations
kernel = np.ones((10, 10), np.uint8)

# Perform morphological closing to remove small gaps and thin lines
safe_map = cv2.morphologyEx(binary_map, cv2.MORPH_CLOSE, kernel)

# Invert the map so that the path is in white and obstacles are in black
safe_map_inverted = cv2.bitwise_not(safe_map)

# Define start and end points
start_point = (301, 752)  # (y, x) format
end_point = (1325, 1285)

plt.imshow(safe_map_inverted, cmap='gray')
plt.axis('off')  # Optional: Hide axis for better visualization
plt.plot([start_point[1], end_point[1]], [start_point[0], end_point[0]], "ro")  # Start and end points
plt.show()
# Save inverted map to file
# Convert the image to RGBA format with custom colors
rgba_image = np.zeros((safe_map_inverted.shape[0], safe_map_inverted.shape[1], 4), dtype=np.uint8)

# Set white pixels (path) to (255, 255, 255, 255)
rgba_image[safe_map_inverted == 255] = [255, 255, 255, 255]

# Set black pixels (obstacles) to (0, 0, 0, 255)
rgba_image[safe_map_inverted == 0] = [0, 0, 0, 255]

# Save the RGBA image to file
# Ensure the RGBA image has the same size as the original image
rgba_image_resized = cv2.resize(rgba_image, (image.shape[1], image.shape[0]))
# Save the resized RGBA image to file
cv2.imwrite("demo/map_inverted.png", rgba_image_resized)

# Erode image by 10 pixels to create a buffer zone around obstacles
kernel = np.ones((10, 10), np.uint8)
eroded_map = cv2.erode(rgba_image, kernel, iterations=1)

# Save the eroded map to file
# Ensure the eroded map has the same size as the original image
eroded_map_resized = cv2.resize(eroded_map, (image.shape[1], image.shape[0]))
# Save the resized eroded map to file
cv2.imwrite("demo/map_eroded.png", eroded_map_resized)

