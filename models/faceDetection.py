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

from models import faceExtraction 

def faceDetection(input_image):
    model = YOLO('./best.pt')
    results: Results = model.predict(input_image)[0]

    return faceExtraction.faceExtraction(input_image, model, results)
