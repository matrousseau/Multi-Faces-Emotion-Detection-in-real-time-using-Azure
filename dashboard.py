import dash
import dash_core_components as dcc
import dash_html_components as html

from flask import Flask, Response
import cv2

import numpy as np
import requests

import matplotlib.pyplot as plt
from PIL import Image
import os
import datetime
import json
import sqlite3

class VideoCamera(object):
    def __init__(self):

        self.flow = cv2.VideoCapture(1)

        # SETUP API
        self.subscription_key = 'a4c51bb3b2f04086b706f15ff6142cdd'
        assert self.subscription_key
        self.face_api_url = ' https://westeurope.api.cognitive.microsoft.com/face/v1.0/detect'

        # BUILDING NEW FOLDERS
        now = datetime.datetime.now()
        self.path_folder = now.strftime("%Y-%m-%d-%Hh%Mm%Ss")
        os.mkdir(self.path_folder)
        os.mkdir(self.path_folder + '/logs')
        os.mkdir(self.path_folder + '/img')

        # LINK TO DB
        self.connexion_db = sqlite3.connect('faces.db')
        self.cursor = self. connexion_db.cursor()

    def __del__(self):
        self.flow.release()

    def get_frame(self):
            success, image = self.flow.read()
            jpeg_emotion_detected= self.detect_emotion(image)
            ret, jpeg = cv2.imencode('.jpg', jpeg_emotion_detected)
            return jpeg.tobytes()

    def detect_emotion(self, image):

        headers = {'Content-Type': 'application/octet-stream',
           'Ocp-Apim-Subscription-Key': self.subscription_key}
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
            'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
            }
        _, img = cv2.imencode('.jpg', image)
        img = img.tobytes()
        response = requests.post(self.face_api_url, params=params, headers=headers, data=img)
        response.raise_for_status()
        faces = response.json()
        squared_frame = self.add_square(image, faces)
        return squared_frame

    def add_square(self, frame, faces):

        for face in faces:
            fr = face["faceRectangle"]
            fa = face["faceAttributes"]
            fe = fa["emotion"]
            age = fa["age"]
            gender = fa["gender"]
            surprise = fe["surprise"]
            neutral = fe["neutral"]
            happiness = fe["happiness"]
            origin = (fr["left"], fr["top"])

            cv2.rectangle(frame, (fr["left"], fr["top"]+fr["height"]), (fr["left"]+fr["width"], fr["top"]),(253,253,253),2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame,"%s"%(gender.capitalize()),(fr["left"]+fr["width"], fr["top"]), font, 1,(255,255,255))
            cv2.putText(frame,"%s"%(age),(fr["left"]+fr["width"], fr["top"]+ 40), font, 1,(255,255,255))
            self.cursor.execute("INSERT INTO faces VALUES (?, ?, ?, ?, ?)", (gender, age, surprise, neutral, happiness))

        # self.connexion_db.commit()
        return frame


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

@server.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

app.layout = html.Div([
    html.H1("Multi faces emotion detection"),
    html.Img(src="/video_feed")
])

if __name__ == '__main__':
    app.run_server(debug=True)
