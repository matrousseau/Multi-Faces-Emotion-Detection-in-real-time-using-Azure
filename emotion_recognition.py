import numpy as np
import cv2
import requests

import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

class EmotionCapture():

    def __init__(self):
        self.flow = cv2.VideoCapture(0)



    def detect_emotion(self, count):

        subscription_key = "bbe9aa125b48403c9c6190284d593b93"
        assert subscription_key

        face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'


        # Set image_path to the local path of an image that you want to analyze.
        image_path = "D:\\IA\\Projets\\Multi-Faces-Emotion-Detection-in-real-time-using-Azure\\13-05-19\\frame%d.jpg" % count

        # Read the image into a byte array
        image_data = open(image_path, "rb")
        headers = {'Content-Type': 'application/octet-stream',
                    'Ocp-Apim-Subscription-Key': subscription_key}

        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,emotion',
        }
        response = requests.post(face_api_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()

        # The 'analysis' object contains various fields that describe the image. The most
        # relevant caption for the image is obtained from the 'description' property.
        analysis = response.json()
        print(analysis)


    def capture_frame(self):
        count = 0
        while(True):
            # Capture frame-by-frame
            ret, frame = self.flow.read()
            cv2.imwrite("D:\\IA\\Projets\\Multi-Faces-Emotion-Detection-in-real-time-using-Azure\\13-05-19\\frame%d.jpg" % count, frame)
            self.detect_emotion(count)
            # Display the resulting frame
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



capture = EmotionCapture()
capture.capture_frame()
