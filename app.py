import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication,QDialog, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer, pyqtSignal 
from models.faceRecognition import faceRecognition
from dotenv import load_dotenv
from models.notifications import Notification
import os
from models.faceDetection import faceDetection

class CameraFeed(QDialog):
    frame_saved = pyqtSignal(str)  # Signal to indicate a frame has been saved

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera Feed")

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)

        self.setLayout(layout)

        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 milliseconds
        self.frame_count = 0

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap)

            # Save frame every 30 seconds
            self.frame_count += 1
            if self.frame_count == 300:  # 30 seconds at 30 fps
                cv2.imwrite("test.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                self.frame_count = 0
                self.frame_saved.emit("test.jpg")  # Emit the signal with the filename

    def closeEvent(self, event):
        self.camera.release()
        event.accept()

class LoginWindow(QDialog):
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

        if username == name and password == passkey:
            self.accept()

        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password. Please try again.")
            

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()

        self.open_camera_window_button = QPushButton("Open Live")
        self.open_camera_window_button.clicked.connect(self.open_camera_window)
        layout.addWidget(self.open_camera_window_button)

        self.setLayout(layout)

        # Connect the frame_saved signal to a slot
        self.camera_window = CameraFeed()
        self.camera_window.frame_saved.connect(self.detect_from_frame)

    def open_camera_window(self):
        self.camera_window.exec_()
        
    def detect_from_frame(self, filename):
        detect(filename)
        
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
    sys.exit(app.exec_())
