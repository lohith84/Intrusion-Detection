import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
import cv2
import threading
import os
import time
from models.faceRecognition import faceRecognition
from dotenv import load_dotenv
from models.notifications import Notification
from models.faceDetection import faceDetection

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)  # Add some margins for spacing

        self.username_label = QLabel("Username:")
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:")
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide the password input
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        
    def login(self):
        # Replace 'your_ip_camera_url' with the actual URL of your IP camera stream
        username = self.username_input.text()
        password = self.password_input.text()
        load_dotenv()
        name = os.environ.get("ADMIN_NAME")
        passkey = os.environ.get("ADMIN_PASSWORD")
        ip_address = os.environ.get("IP_CAM_ADDRESS")

        if username == name and password == passkey:
            QMessageBox.information(self, "Login Successful", "Welcome, Admin!")
            camera_url = ip_address
            cap = cv2.VideoCapture(camera_url)

            if not cap.isOpened():
                QMessageBox.warning(self, "Error", "Unable to open IP camera stream.")
                return

            self.hide()
            self.streaming_window = StreamingWindow(cap)
            self.streaming_window.show()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password. Please try again.")
            
        


class StreamingWindow(QWidget):
    def __init__(self, cap):
        super().__init__()
        self.setWindowTitle("Streaming")
        self.setGeometry(100, 100, 640, 480)

        layout = QVBoxLayout()

        self.label = QLabel()
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.cap = cap
        self.streaming = True
        self.frame_save_interval = 10  # Save frame every 10 seconds
        self.start_time = 0
        self.save_frame_flag = False  # Initialize save_frame_flag
        self.frame_to_save = None

        self.stream_thread = threading.Thread(target=self.stream_video)
        self.stream_thread.start()

        # Thread for saving frames
        self.save_frame_thread = threading.Thread(target=self.save_frame_thread_func)
        self.save_frame_thread.start()

    def closeEvent(self, event):
        self.streaming = False
        self.cap.release()

    def save_frame_thread_func(self):
        while self.streaming:
            if self.save_frame_flag:
                self.save_frame(self.frame_to_save)
                self.save_frame_flag = False
            time.sleep(0.1)  # Adjust this value as needed

    def save_frame(self, frame):
        output_dir = './'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filename = os.path.join(output_dir, "test.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved frame as {filename}")
        
        # After saving the frame, detect faces in the image
        self.detect_frame(filename)

    def detect_frame(self, filephoto):
        detect(filephoto)

    def stream_video(self):
        while self.streaming:
            ret, frame = self.cap.read()
            if not ret:
                QMessageBox.warning(self, "Error", "Unable to retrieve frame.")
                break

            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize the frame to fit the label size
            frame_resized = cv2.resize(frame_rgb, (640, 480))

            # Convert the frame to QImage
            h, w, ch = frame_resized.shape
            bytes_per_line = ch * w
            q_img = QImage(frame_resized.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Display the frame on the label
            self.label.setPixmap(QPixmap.fromImage(q_img))

            # Check if it's time to save a frame
            current_time = time.time()
            if current_time - self.start_time >= self.frame_save_interval:
                self.frame_to_save = frame.copy()
                self.save_frame_flag = True
                self.start_time = current_time

        self.cap.release()

        
class EmailNotification:
    def send_email(self, subject, body, image_path=None):
        # Your code to send email
        print("Sending email...")
        print("Subject:", subject)
        print("Body:", body)
        if image_path:
            print("Attaching image:", image_path)
            # Your code to attach the image to the email

class detect():
    def __init__(self, image):
        self.image = image
        self.faceDetection()
        self.faceRecognition()
        
    def faceDetection(self):
        faceDetection(self.image)
        
    def faceRecognition(self):
        names = faceRecognition(self.image)
        print(names)
        if 'u' in names:
            length=1
            load_dotenv()
            password = os.environ.get("INTRUSALERTS_PASSWORD")
            from_email = os.environ.get("INTRUSALERTS_FROM_EMAIL")
            to_email = os.environ.get("INTRUSALERTS_TO_EMAIL")
    
    # Instanciate Notification and PersonDetection classes

            email_notification = Notification(from_email, to_email, password)
            email_notification.send_email(length)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
