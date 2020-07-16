from django.test import TestCase
import pandas as pd
from django.contrib.auth.models import User
from .models import UserProfile
from .utils import match_face
import os

class VerifyFaceTestCase(TestCase):
    def setUp(self):
        maryam = User(username='emma',password='Az3ora1997')
        maryam.save()
        maryamprofile = UserProfile(user=maryam, photo='FaceAuth\profile_images\emma.jpg')
        maryamprofile.save()
        

    def test_verifing_face(self):
        user = User.objects.get(username='emma')
        df = pd.DataFrame([],columns=['image', 'name', 'label'])
        rootdir = 'D:/Study_tests/face_recognition/dataset/'
        for path in os.scandir(rootdir):
            print (path.name)
            for file in os.scandir(path):
                df = df.append({'image':file.path,'name': path.name,'label': match_face(user, False, file.path)}, ignore_index=True)
        
        print(df.head())
        df.to_csv('results.csv', index=None)


        #print(user.userprofile.photo)
        #match_face(user,True,'D:/istudyfaceauth/FaceAuth/profile_images/emma2.jpg')


