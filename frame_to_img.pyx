# Cython treats print as it if were from python 2.7
from __future__ import print_function
import cv2
import numpy as np
cimport numpy as np

def img_from_frames(path, output_path, int user_height, int user_width, bint verbose = True):
    """
    Creates images by averaging each frame in a video
    """
    DTYPE = np.uint8
    cap = cv2.VideoCapture(path)
    
    cdef int length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cdef int width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cdef int height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cdef float fps = cap.get(cv2.CAP_PROP_FPS)
    
    if length < user_width:
        user_width = length
        
    cdef int avg_group_size = length//user_width
    #remainder_frames = length % user_width
    
    print(f"\nTotal Frames (Aprox): {length}\tFrames grouping: {avg_group_size}\n")
    print(f"Input Frame Data:\n\tHeight: {height}\n\tWidth: {Width}\n\tfps: {fps:.2f}\n")
    print(f"Output Img:\n\tHeight: {user_height}\n\tWidth: {user_Width}\n")
    
    cdef np.ndarray img_shape = np.zeros((height,user_width,3), 
                                         dtype = DTYPE)
    cdef np.ndarray avg_group_shape = np.zeros((height, avg_group_size, 3), 
                                               dtype = DTYPE)
    
    cdef int avg_len = 0
    cdef int w_px = 0
    cdef int progress = length//100
    cdef float pct
    cdef bint valid_frame
    cdef int progress_bar
    # We will avoid this for now as we don't know if frame
    # can actually change shape (height, width, 3)
    #cdef np.ndarray[DTYPE, ndims = ...] frame
    cdef np.ndarray frame
    
    cdef int fr
    for fr in range(length): 
        
        try:
            valid_frame, frame = cap.read()
            if valid_frame == False:
                break

            if  avg_len < avg_group_size:
                avg_group_shape[:,avg_len,:] = np.uint8(np.average(frame, axis = 1))
                avg_len +=1
            else:
                img_shape[:,w_px,:] = np.uint8(np.average(avg_group_shape, axis = 1))
                avg_group_shape = np.zeros((height, avg_group_size, 3))
                w_px += 1
                avg_len = 0
                
            pct = (fr+1)/<float>length
            
            if verbose == True and (fr % progress == 0 or fr == 0 or valid_frame == False):
                
                progress_bar = <int>(fr/<float>(4*progress))
                print('>Progress: [{0}] {1:.0%}'.format("|"*progress_bar + " "*(25-progress_bar), pct), end = '\r')
                
        except IndexError: 
            break
    
    # Cut outs excesive frames
    #output_image = img_shape
    cdef np.ndarray output_image = img_shape[:,:fr+1,:]
    
    # Outputs resulting image to output_path and resizes it
    cv2.imwrite(output_path, cv2.resize(output_image, (user_width, user_height)))      
    print('\n>Done')