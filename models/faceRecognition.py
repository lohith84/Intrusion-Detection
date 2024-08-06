from ultralytics import YOLO
from ultralytics.engine.results import Results  
from deepface import DeepFace
from PIL import Image
import gradio as gr
import shutil
import cv2
import os

import pandas as pd
import numpy as np
import os
from deepface import DeepFace

def faceRecognition(input_image):

    # Path to the directory containing cropped objects
    cropped_objects_dir = "./faces/"

    # Initialize a list to store the extracted characters
    extracted_chars = []

    #file_to_delete = "./database/ds_facenet512_opencv_v2.pkl"
    #if os.path.exists(file_to_delete):
     #   os.remove(file_to_delete)    

    # Iterate through the image files in the directory
    for filename in os.listdir(cropped_objects_dir):
        if filename.endswith(".jpg"):
            img_path = os.path.join(cropped_objects_dir, filename)
            model = DeepFace.find(img_path=img_path, db_path="database", enforce_detection=False, model_name="Facenet512")
            print("Processing:", filename)
            print("Model:", model)
            # Check if a face was recognized in the image
            if model and len(model) > 0 and 'identity' in model[0] and len(model[0]['identity']) > 0:
                # Extract the first character of the filename and append it to the list
                import pandas as pd

                # Example Series object
                k=model[0]['identity']
                stt=str(k)
                model = pd.Series([stt])
                
                # Accessing the string value within the Series
                path = model[0]
                
                # Extracting the filename from the path using .str accessor
                filename = path.split("\\")[-1]
                
                # Getting the first character of the filename
                name = filename[0]
                

            else:
                # If no face is recognized, set name to 'unknown'
                name = 'u'  # 'u' for 'unknown'

            extracted_chars.append(name)

    return extracted_chars

