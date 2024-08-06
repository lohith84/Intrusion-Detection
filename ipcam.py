import cv2
import os

# Define the RTSP stream URL
rtsp_url = 'rtsp://admin:isdr@430@192.168.49.104:558/PSIA/streaming/channels/101'

# Create a VideoCapture object
vs1 = cv2.VideoCapture(rtsp_url)

# Check if the VideoCapture object is opened successfully
if not vs1.isOpened():
    print("Error: Unable to open RTSP stream.")
    exit()

# Create a directory to store frames
output_folder = './'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Read a frame from the video capture
ret, frame = vs1.read()

if ret:
    # Save the frame as an image file
    frame_filename = os.path.join(output_folder, 'test.jpg')
    cv2.imwrite(frame_filename, frame)
    print("Frame saved as test.jpg")
else:
    print("Error reading frame")

# Release the VideoCapture object
vs1.release()
