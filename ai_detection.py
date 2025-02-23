import os
from google.cloud import vision
import streamlit as st

# Set up authentication using the service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "functions/wildlife-tracker-451720-4b5b0a585351.json"

# Initialize the client
client = vision.ImageAnnotatorClient()

def detect_objects(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    # Use the Image class directly
    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    # Process the response to find labels (e.g., animal breed or type)
    # TYPE AND BREED

    if response.error.message:
        raise Exception(f"API Error: {response.error.message}")

    type = response.label_annotations[0].description
    breed = response.label_annotations[1].description

    return type, breed
