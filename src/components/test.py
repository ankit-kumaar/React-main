import cv2
import imghdr
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
from PIL import Image
import pytesseract
import os

def detect_licence_number(image_path):
    # Check if the image file format is supported
    if imghdr.what(image_path) not in ['jpeg', 'jpg', 'png', 'bmp']:
        raise ValueError("Unsupported image file format")

    try:
        # Load the image and convert it to grayscale
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detect edges using Canny edge detection
        edged = cv2.Canny(blurred, 30, 150)

        # Find contours in the edged image
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Initialize the list of license plate contours
        license_plate_contours = []

        # Iterate through the contours
        for contour in contours:
            # Compute the bounding rectangle and aspect ratio
            (x, y, w, h) = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h

            # Check if the contour has a rectangular shape with an aspect ratio similar to a license plate
            if 3 < aspect_ratio < 6 and 1000 < cv2.contourArea(contour) < 5000:
                license_plate_contours.append((x, y, w, h))

        # Initialize the list of license plate numbers
        license_plate_numbers = []

        # Iterate through the license plate contours
        for (x, y, w, h) in license_plate_contours:
            # Crop the license plate region from the original image
            license_plate = image[y:y + h, x:x + w]

            # Convert the license plate image to grayscale and apply thresholding
            gray_license_plate = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_license_plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Use TensorFlow OCR model to recognize the characters
            # For simplicity, we will use the Tesseract-OCR engine with the TensorFlow backend
            # You can replace this with a custom-trained TensorFlow model if needed
            try:
                license_plate_number = pytesseract.image_to_string(thresh, lang='eng', config='--psm 11')
                license_plate_numbers.append(license_plate_number.strip())
            except Exception as e:
                raise Exception("Failed to recognize characters: " + str(e))

        # Return the detected license plate numbers
        if license_plate_numbers:
            print("Detected license plate number:", license_plate_numbers[0])
            return license_plate_numbers[0]
        else:
            raise Exception("No license plate numbers detected")

    except Exception as e:
        raise Exception("Error processing image: " + str(e))

# Example usage
image_path = "path_to_your_image.jpg"
detect_licence_number(image_path)