# -*- coding: utf-8 -*-
"""
Created on Sat Jul 02 12:58:23 2016

@author: matsumoto
"""

import cv2
import numpy as np
import scipy as sci
import pylearn2
import pickle

def training_step(config_file):
    assert(os.path.exists(config_file))
    _yaml = open(config_file).read()
    _train = yaml_parse.load(_yaml)
    _train.main_loop()
    return _train

def createHistBGR(frame):
    channel=3

    chart = np.zeros([upper,256],dtype=np.uint8)
    chart = cv2.cvtColor(chart, cv2.COLOR_GRAY2BGR)

    for i in range(0, channel):
        color=[0,0,0]
        color[i]=255

        hist = cv2.calcHist([frame], [i], None, [256], [0,256])
        cv2.normalize(hist, hist, lower, upper, cv2.NORM_MINMAX)

        for j in range(1, 255):
            v1=hist[j-1]
            v2=hist[j]
            cv2.line(chart, (j,upper-v1), (j, upper-v2), color)
    
    return chart

def createHistGray(frame):
    color=[200,200,200]

    chart = np.zeros([upper,256],dtype=np.uint8)

    hist = cv2.calcHist([frame], [0], None, [256], [0,256])
    cv2.normalize(hist, hist, lower, upper, cv2.NORM_MINMAX)
    
    for i in range(1, 255):
        v1=hist[i-1]
        v2=hist[i]
        cv2.line(chart, (i,upper-v1), (i, upper-v2), color)
    
    return chart

if __name__=='__main__':
    lower = 0
    upper = 100
    
    # main
    cap = cv2.VideoCapture(0)
    
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    while True:
        ret, frame = cap.read()
    
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_canny = cv2.Canny(frame, 100, 200)
    
        chart_color = createHistBGR(frame)
        chart_gray = createHistGray(frame_gray)
            
        key=cv2.waitKey(10)
        
        # ESC
        if key==27:
            break
        
        cv2.imshow('cam color', frame)
        cv2.imshow('cam gray', frame_gray)
        cv2.imshow('cam canny', frame_canny)
    
        cv2.imshow('hist color', chart_color)
        cv2.imshow('hist gray', chart_gray)
    
    cap.release()
    cv2.destroyAllWindows()
