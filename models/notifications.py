import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

class Notification:
    def __init__(self, from_email, to_email, password):
        self.from_email = from_email
        self.to_email = to_email
        self.password = password
        self.server = None
        self.authenticate()

    def authenticate(self):
        self.server = smtplib.SMTP('smtp.gmail.com: 587')
        self.server.starttls()
        self.server.login(self.from_email, self.password)

    def send_email(self, object_detected=1):
        message = MIMEMultipart()
        message['From'] = self.from_email
        message['To'] = self.to_email
        message['Subject'] = "Intrusion Security Alert"
        message_body = f'''
        <p>ALERT - {object_detected} intruder(s) has been detected !!</p>
        '''
        message.attach(MIMEText(message_body, 'html'))
        
        # Attach all images to the message
        for file in os.listdir("./faces"):
            img = open(os.path.join("./faces/",file), 'rb').read()
            image = MIMEImage(img, name=file)     
            message.attach(image)
        
        # Send the mail
        self.server.sendmail(self.from_email, self.to_email, message.as_string())

    def quit(self):
        self.server.quit()

