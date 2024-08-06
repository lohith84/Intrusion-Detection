# Intrusion Detection System using YOLO V8

## Overview
This project implements an intrusion detection system utilizing deep learning techniques. It integrates real-time video streaming from an IP camera, object detection using the YOLOv8 model, and face recognition using FaceNet512. The system detects intruders, and triggers alerts via email when a potential threat is identified.

## Features
- **Real-Time Video Stream Access**: Uses Real Time Streaming Protocol (RTSP) to connect to and stream video from an IP camera.
- **Object Detection**: Implements YOLOv8 for detecting potential intruders in real-time.
- **Face Recognition**: Uses FaceNet512 to identify individuals by comparing facial embeddings against a database.
- **Email Alerts**: Automatically sends email notifications upon detecting an intruder.
- **User Authentication**: Ensures secure access to the system using PyQt.

## Technologies
The project utilizes the following technologies:
- **Python**: Programming language used for implementing the system.
- **OpenCV**: Library for real-time computer vision tasks, used for frame extraction and processing.
- **YOLOv8**: Object detection model for identifying potential intruders in real-time.
- **FaceNet512**: Face recognition model for identifying individuals by comparing facial embeddings.
- **SMTP**: Protocol for sending email alerts.
- **PyQt**: Framework for building the graphical user interface and managing user authentication.
- **PyQtChart**: Library for graphical representation of data.
- **Google Colab**: Platform for training the YOLOv8 model with the prepared dataset.
- **RTSP**: Protocol used for streaming video from the IP camera.


## Installation

### Prerequisites
- Python 3.6 or later
- IP Camera with RTSP support
- Google Colab (for model training)

### Setup Instructions

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/lohith84/Intrusion-Detection.git
    cd Intrusion-Detection
    ```

2. **Virtual Environment Setup:**
   Create and activate a virtual environment to manage dependencies.

    ```bash
    python -m venv intrusion
    source intrusion/bin/activate  # On Windows use intrusion\Scripts\activate.bat
    ```

3. **Install Dependencies:**
   Install the required Python libraries.

    ```bash
    pip install -r requirements.txt
    ```
    
4. **ENV file Configuration**
   ```bash
   INTRUSALERTS_PASSWORD=Password for Email Alerts
   INTRUSALERTS_FROM_EMAIL=From Email Address
   INTRUSALERTS_TO_EMAIL=To Email Address
   IP_CAM_ADDRESS=rtsp_url
   ADMIN_NAME=User Admin Name
   ADMIN_PASSWORD=User Admin Password
   ```

## Usage

### Accessing the Camera Stream
Update the RTSP URL with your camera's configuration details.

```python
rtsp_url = 'rtsp://username:password@ip_address:port/channel_path'
```

### Running the System

1. **Using Normal Camera**
   The system uses normal camera

    ```bash
    python app.py
    ```

2. **Using IP Camera**
   The system uses HIK Vision IP camera

    ```bash
    python test.py
    ```
    
## Training the Model

1. **Dataset Preparation:**
   Annotate and augment your dataset for training.

2. **Model Training:**
   Use Google Colab to train the YOLOv8 model with the prepared dataset.

## Project Structure

- **app.py:** Handles the whole system.

- **Models:** Handles the extraction and processing of video frames.
    1. **faceDetection.py:** Detect the faces in the frame using YOLOv8.
    2. **faceExtraction.py:** Extacts the faces in the frame.
    3. **faceRecognition.py:** Implements intruder detection using YOLOv8 and FaceNet512.
    4. **notifications.py:** Manages email alerts using SMTP.
   
- **database:**
Name folders in Sequetial Order as person1,person2...

- **requirements.txt:** List of required Python libraries.

## Manual
For detailed instructions on setting up and using the system, please refer to the project manual:
- [Intrusion Detection System - User Manual](https://drive.google.com/file/d/1LflM0TR32F9Qckumg76iX-pMx-5EZyvh/view?usp=sharing)

## Team
This project was developed by:
- **H Lohith**
- **M Jerusha** 
- **Pamu Rahul** 
- **Pulimi Rahul** 

## Contributions
Contributions are welcome! Please fork the repository and submit a pull request.

### Notes:
- Replace placeholders with your actual details.
- Customize sections like features and technologies used according to your project specifics.
- Add additional sections as needed

Feel free to tailor this template further based on your project's unique aspects and requirements!
