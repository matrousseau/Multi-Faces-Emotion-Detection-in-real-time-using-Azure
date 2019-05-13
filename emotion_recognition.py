import numpy as np
import cv2


class EmotionCapture():

    def __init__(self):
        self.flow = cv2.VideoCapture(1)

    def detect_emotion(self, frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'test', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
        return frame

    def capture_frame(self):

        while(True):
            # Capture frame-by-frame
            ret, frame = self.flow.read()
            frame_changed = self.detect_emotion(frame)
            # Display the resulting frame
            cv2.imshow('frame',frame_changed)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


capture = EmotionCapture()
capture.capture_frame()
