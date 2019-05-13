import numpy as np
import cv2
import requests

import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

class EmotionCapture():

    def __init__(self):
        self.flow = cv2.VideoCapture(1)
        self.subscription_key = "88c9982696ac4d848b775ff3e43ffe7e"
        self.vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
        self.analyze_url = self.vision_base_url + "analyze"
        assert self.subscription_key


    def detect_emotion(self, count):

        subscription_key = "88c9982696ac4d848b775ff3e43ffe7e"
        assert subscription_key

        vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

        analyze_url = vision_base_url + "analyze"

        # Set image_path to the local path of an image that you want to analyze.
        image_path = "D:\\IA\\Projets\\Multi-Faces-Emotion-Detection-in-real-time-using-Azure\\13-05-19\\frame%d.jpg" % count

        # Read the image into a byte array
        image_data = open(image_path, "rb").read()
        headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                      'Content-Type': 'application/octet-stream'}
        params     = {'visualFeatures': 'Categories,Description,Color'}
        response = requests.post(
            analyze_url, headers=headers, params=params, data=image_data)
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
            count +=1
            # Display the resulting frame
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



capture = EmotionCapture()
capture.capture_frame()
