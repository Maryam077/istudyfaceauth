import base64
import re
from io import BytesIO
from django.core.files.base import ContentFile
import face_recognition
import cv2 
import os
import time

def decode_base64(data, altchars=b'+/'):
    image_data = re.sub('^data:image/.+;base64,', '', data)
    return base64.b64decode(image_data)

def prepare_image(image):
    return BytesIO(decode_base64(image))

def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))

def face_detect(location):
    capture_duration = 10
    WindowName ='Preview'
    view_window = cv2.namedWindow(WindowName,cv2.WINDOW_NORMAL)


    cap = cv2.VideoCapture(0)
    #out = cv2.VideoWriter('outpy.jpeg', cv2.VideoWriter_fourcc(*'XVID'),20.0, (640,480))

    
    start_time = time.time()
    path = 'FaceAuth\profile_images\img'+str(int(time.time()))+'.jpeg'
    while True:
        s, img = cap.read()
        if s:
            cv2.imshow("Preview", img)
            if (int(time.time() - start_time) >= capture_duration/2) and not os.path.isfile(path):
                cv2.imwrite(path,img)
            cv2.waitKey(1)
            if (int(time.time() - start_time) >= capture_duration):
                cap.release()
                cv2.destroyWindow("Preview")
                break
    return path

