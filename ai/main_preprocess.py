import numpy as np
import cv2
import os
from sklearn.preprocessing import RobustScaler

def filter(image, mask):
    binary_mask = np.zeros_like(mask)
    binary_mask[mask == 1] = 1

    positive_rate = np.mean(tile_mask)
    if positive_rate >= 0.1:
        return True
    else:
        return False


# Preprocessing
def preprocess_image(image):
    # Apply denoising and image enhancement techniques
    # (Non-Local Means Denoising, CLAHE, Contrast Stretching)
    denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2Lab)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)

    min_val = np.percentile(l_clahe, 2)
    max_val = np.percentile(l_clahe, 98)

    stretched = cv2.normalize(l_clahe , None, min_val, max_val, cv2.NORM_MINMAX)
    lab_clahe = cv2.merge((stretched, a, b))
    enhanced = cv2.cvtColor(lab_clahe, cv2.COLOR_Lab2BGR)

    
    return enhanced

def preprocess_mask(mask):
    # Apply morphological mask smoothing (erosion followed by dilation)

    eroded = cv2.erode(mask.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1)
    dilated = cv2.dilate(eroded, np.ones((3, 3), np.uint8), iterations=1)

    return dilated


folder_path = 'C:\\Users\\USER\\Desktop\\diplom\\konturs\\tiles5'
save_path = 'C:\\Users\\USER\\Desktop\\diplom\\konturs\\preprocess5\\'
file_list = os.listdir(folder_path)


for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    image = cv2.imread(file_path)

    if image is None: 
        continue

    image = preprocess_image(image)

    cv2.imwrite(save_path + file_name, image)

#cv2.imshow('Original Image', image)
#cv2.imshow('Original mask', mask)

#cv2.waitKey(0)
# Preprocessing
#preprocessed_images, preprocessed_masks = preprocess(image, mask)

#cv2.imshow('Original Image', image)
#cv2.imshow('preprocessed Image', preprocessed_images)
#cv2.waitKey(0)
#exit(0)