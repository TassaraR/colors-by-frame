# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

directory = r''
file = ''
output_file = 'output.png'
path = os.path.join(directory, file)
verbose = True

cap = cv2.VideoCapture(path)

user_width = 1920
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)

if length < user_width:
    user_width = length
    
avg_group_size = length//user_width
remainder_frames = length % user_width

print(f"length: {length}\tframes_avg_group: {avg_group_size}\tremainder: {remainder_frames}\n")
print(f"width: {user_width}\nheight: {height}\nfps: {fps:.2f}\n")

img_shape = np.zeros((height,user_width,3))
print(f"img_size: {img_shape.shape}\n")

avg_group_shape = np.zeros((height, avg_group_size, 3))

n,i = 0,0

for fr in range(length): 
    
    try:
        gotFrame, frame = cap.read()
        if gotFrame == False:
            break
        
        if  n < avg_group_size:
            avg_group_shape[:,n,:] = np.uint8(np.average(frame, axis = 1))
            n +=1
        else:
            img_shape[:,i,:] = np.uint8(np.average(avg_group_shape, axis = 1))
            avg_group_shape = np.zeros((height, avg_group_size, 3))
            i += 1
            n = 0
        if verbose == True:
            print(f'Total frames processed: {fr+1}/{length} | {((fr+1)/length):.1%}', end = '\r', flush = True)
    except IndexError: 
        break
        
print('\nDone')
cv2.imwrite(output_file,img_shape) 