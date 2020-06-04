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

def face_auth(location, username):
    
    video_capture = cv2.VideoCapture(0)
    capture_duration =30
    
    process_this_frame = True
    known_face_names  = []
    known_face_encodings = []
    for prof in UserProfile.objects.all():
        if len(prof.photo):
            known_face_names.append(prof.user.username)
            user_image = face_recognition.load_image_file(prof.photo)
            user_face_encoding = face_recognition.face_encodings(user_image)[0]
            known_face_encodings.append(user_face_encoding)
    print(known_face_names)
    #print(face_encodings)
    start_time = time.time()

    while True:
        ret, frame = video_capture.read()

        #for faster results
        small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:,:,::-1]

        if process_this_frame:
            try:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                name = 'Unknown'
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    print(matches)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)
            except Exception as e:
                print(e)
        
        if (int(time.time() - start_time) >= capture_duration):
            process_this_frame = False
            break

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        cv2.waitKey(1)
       
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    if username in face_names:
        return True
    else:
        return False

