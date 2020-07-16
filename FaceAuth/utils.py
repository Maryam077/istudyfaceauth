import base64
import re
from io import BytesIO
from django.core.files.base import ContentFile
import face_recognition
import cv2 
import os
import time
from .models import UserProfile
import numpy as np
import threading

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

def face_detect():

    capture_duration = 5
    WindowName ='Preview'
    view_window = cv2.namedWindow(WindowName,cv2.WINDOW_NORMAL)


    cap = cv2.VideoCapture(0)
    #out = cv2.VideoWriter('outpy.jpeg', cv2.VideoWriter_fourcc(*'XVID'),20.0, (640,480))

    
    start_time = time.time()
    if not os.path.isdir('FaceAuth\\profile_images\\'):
        os.mkdir('FaceAuth\\profile_images\\')
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

def match_face(user,show_window=False,testimage=None):
    image_paths = [userprofile.photo for userprofile in user.userprofile_set.all()]
    print(image_paths)
    user_images = [face_recognition.load_image_file(img) for img in image_paths]
    user_face_encodings = [face_recognition.face_encodings(user_image)[0] for user_image in user_images]
    names = [name for name in [user.username] for i in range(len(user_face_encodings))]
    print(names)
    print(user_face_encodings)
    
    
    if testimage==None:
        camera = cv2.VideoCapture(0)
    else :
        frame = cv2.imread(testimage,cv2.IMREAD_COLOR)

    duration = 10
    start_time = time.time()

    while True:
        if testimage==None:
            ret, frame = camera.read()

        #for faster results
        
        rgb_small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)


        try:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            name = 'Unknown'
            matchesCount = 0
            for  user_face_encoding in user_face_encodings:
                matches= face_recognition.compare_faces(user_face_encoding, face_encoding)
                #face_distances = face_recognition.face_distance(user_face_encoding, face_encoding)
                if True in matches:
                    matchesCount += 1

            if matchesCount >= len(image_paths)*0.8:
                name = user.username
                #print(name+' Face detected')
                face_names.append(name)
                if not show_window:
                    camera.release()
                    cv2.destroyAllWindows()
                    return True

                
        except Exception as e:
            pass
        
        if (int(time.time() - start_time) >= duration):
            break
        if show_window:
        # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left,bottom-30), (right, bottom), (255, 255, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 2.0, (0, 0, 0), 1)

            # Display the resulting image
            cv2.imshow('Video', rgb_small_frame)
            cv2.waitKey(1)
        
    # Release handle to the webcam
    #camera.release()
    cv2.destroyAllWindows()
    if user.username in face_names:
        return True
    else:
        print(name+' Face not detected')
        return False