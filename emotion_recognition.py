import numpy as np
import cv2
import requests

import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import os
import datetime
import json


class EmotionCapture():

    def __init__(self):
        self.flow = cv2.VideoCapture(0)
        self.subscription_key = "bbe9aa125b48403c9c6190284d593b93"
        assert self.subscription_key
        self.face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

        now = datetime.datetime.now()
        self.path_folder = now.strftime("%Y-%m-%d-%Hh%Mm%Ss")
        os.mkdir(self.path_folder)
        os.mkdir(self.path_folder + '/logs')
        os.mkdir(self.path_folder + '/img')

    def detect_emotion(self, count):

        image_path = self.path_folder + "/img/frame%d.jpg" % count

        image_data = open(image_path, "rb")
        headers = {'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': self.subscription_key}
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,emotion'}

        response = requests.post(self.face_api_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()

        analysis = response.json()
        with open(self.path_folder + "/logs/logs%d.json" % count, 'w') as outfile:
            json.dump(analysis, outfile)


    def capture_frame(self):
        count = 0
        while(True):
            # Capture frame-by-frame
            ret, frame = self.flow.read()
            cv2.imwrite(self.path_folder + "/img/frame%d.jpg" % count, frame)
            self.detect_emotion(count)
            count += 1
            # Display the resulting frame
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break




capture = EmotionCapture()
capture.capture_frame()
