# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
import models,sys,os
from django.shortcuts import render_to_response
import time,thread
from apptest import models
import os
import hkslib
import tools.facerecognition
import tools.facerecognition
import cv2
from django.views.decorators.cache import cache_control


detector = hkslib.get_frontal_face_detector()
faces=os.listdir("face/")
faceencodings=[]
names=[]
for face in faces:
    names.append(face.split(".")[0])
    face_image = tools.facerecognition.load_image_file("face/" + face)
    face_location = tools.facerecognition.face_locations(face_image)
    faceencodings.append(tools.facerecognition.encodings(face_image=face_image, known_face_locations=face_location)[0])

class features:
    def detectFace(self,img):

        frame = cv2.imread(img)

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Only process every other frame of video to save time
        # Find all the faces and face encodings in the current frame of video
        face_locations = tools.facerecognition.face_locations(small_frame)
        face_encodings = tools.facerecognition.encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = tools.facerecognition.compare(faceencodings, face_encoding, tolerance=0.4)
            name = "Unknown"
            for i in range(len(match)):
                if match[i]:
                    name = names[i]
            face_names.append(name)

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255))
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imwrite("./static/face_img/face.jpg", frame)
        faceCount = len(face_names)
        if faceCount == 0:
            return False
        elif faceCount == 1:
            return face_names[0]
        elif faceCount > 1:
            facename = []
            for i in range(faceCount):
                facename.append(face_names[i])
            return facename



@cache_control(no_cache=True)
def face_recognition(request):
    if request.method == "GET":
        return render(request, 'face_recognition.html')
    elif request.method == "POST":
        obj = request.FILES.get('img')
        file_path = os.path.join('static/face_img','face_wait.jpg')
        f = open(file_path,mode="wb")
        for i in obj.chunks():
            f.write(i)
        f.close()

        face_path = os.path.abspath('./' + 'static/face_img')
        img = face_path + '/face_wait.jpg'
        obj_features = features()
        result = obj_features.detectFace(img)
        if result== False:
            content=u'并没有发现脸蛋.您可以换一张清晰的图片试试'
            return render(request, 'face_recognition_post.html',{'content':content})
        elif type(result) == unicode:
            if result == 'Unknown' :
                content=u'发现1个美丽又帅气的脸蛋.'
            else:
                content = u'我认识这家伙.他叫'+ result
            return render(request, 'face_recognition_post.html',{'content':content})
        else:
            face_number = str(len(result))
            content = u'发现' + face_number + u'个美丽又帅气的脸蛋.我猜他们的名字是' + str(result)[1:-1]
            return render(request, 'face_recognition_post.html', {'content': content})

def object_recognition(request):
    if request.method == "GET":
        return render(request, 'object_recognition.html')
    elif request.method == "POST":
        obj = request.FILES.get('img')
        file_path = os.path.join('static/face_img','object_wait.jpg')
        f = open(file_path,mode="wb")
        for i in obj.chunks():
            f.write(i)
        f.close()
        os.system('./darknet detect cfg/yolov3.cfg yolov3.weights static/face_img/object_wait.jpg')
        os.system('mv /home/l/django_demo/predictions.jpg /home/l/django_demo/static/face_img/')
        return render(request, 'object_recognition_post.html')

def register(request):
    error = ""
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        u = request.POST.get('username')
        p1 = request.POST.get('password_1')
        p2 = request.POST.get('password_2')
        b = request.POST.get('button')
        if b == None :
            error = "您没有同意注册协议"
            return render(request, 'register.html', {'error': error})
        elif p1 != p2:
            error = "您输入的两次密码不一样"
            return render(request, 'register.html', {'error': error})
        else:
            models.UserInfo.objects.create(username=u, password=p1)
            content = '恭喜您注册成功！'
            return render(request, 'login.html',{'content': content})



def index(request):
    return render(request, 'index.html')

def error_notfound(request):
    return render(request,'404.html')

def error_service(request):
    return render(request,'500.html')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        # 数据库中执行 select * from user where usernam='x' and password='x'
        u = request.POST.get('username')
        p = request.POST.get('password')
        # obj = models.UserInfo.objects.filter(username=u,password=p).first()
        # print(obj)# obj None,
        # count = models.UserInfo.objects.filter(username=u, password=p).count()
        obj = models.UserInfo.objects.filter(username=u, password=p).first()

        if obj:
            return render(request, 'index.html', {'username': u})
            # return redirect('../index/')
        else:
            return render(request, 'login.html')
    else:
        # PUT,DELETE,HEAD,OPTION...
        return redirect('../index/')

