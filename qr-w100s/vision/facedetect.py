#!/usr/bin/env python

from common import anorm2, draw_str
import numpy as np

import cv2
import multiprocessing
import Queue #needed separately for the Empty exception
import time, datetime

import sys,os

import cv2

from common import SleepableCVProcess

class FaceDetectProcess(SleepableCVProcess):
   def __init__(self, inputqueue, outputqueue):
      SleepableCVProcess.__init__(self, inputqueue, outputqueue)

   def setup(self):      
      # this takes a long time, so clear the queue afterwards
      filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "haarcascades","haarcascade_frontalface_alt2.xml"))
      self.face_cascade = cv2.CascadeClassifier(filepath)
      filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "haarcascades","haarcascade_mcs_eyepair_big.xml"))
      self.eye_cascade  = cv2.CascadeClassifier(filepath)
      while(True):
         try:
            tstamp, cv_img = self.inputqueue.get(False)
         except Queue.Empty:
            break
   
   def doWork(self, cv_img):
      try:
         gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
         vis = gray.copy()
         vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2RGB)
   
         faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
         
         for (x,y,w,h) in faces: 
            cv2.rectangle(vis,(x,y),(x+w,y+h),(255,0,0),2)
            
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = vis[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
               cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
         
         return vis
      
      except Exception, e:
         print "exception in fd:", e
         return cv_img


