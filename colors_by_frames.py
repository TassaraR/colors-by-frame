# -*- coding: utf-8 -*-
import os
import numpy as np
from tkinter import Tk, filedialog
from functools import reduce 
import argparse
import pyximport; pyximport.install(setup_args={'include_dirs': np.get_include()})
from frame_to_img import img_from_frames

#directory = r'C:\Users\rtass\Downloads\The_Mandalorian_S01E01'
#file = 'mandalorian.mkv'

#path = os.path.join(directory, file)

user_width = 1920
user_height = 1080

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type = str, help="Input file path")
parser.add_argument("-s","--shape", type = str, help="Output shape in format (height px, width px)")

args = parser.parse_args()

if __name__ == '__main__':
    
    if args.input:
        if os.path.exists(args.input):
            path = args.input 
        else:
            print("File does not exist/Incorrect path to file")
            quit()
    else:
        window = Tk()
        # Don't display the Tk window
        window.withdraw()
        # I couldn't find all the supported files for opencv's VideoCapture
        path = filedialog.askopenfilename(initialdir = "~", 
                                          title = "Choose a supported File")
    
    if args.shape:
        try:
            if isinstance(eval(args.shape), tuple):
                output_dims = eval(args.shape)
                val_dim_types = reduce(lambda a,b: a & b, tuple(True if (isinstance(i, int) and i > 0) else False for i in output_dims))
                if (len(output_dims) == 2 and val_dim_types):
                    user_height, user_width = output_dims
                else:
                    raise ValueError("Incorrect shape dimensions")
            
        except NameError:
            print("Invalid output shape")
            quit()
    
    in_filename = os.path.basename(path)
    out_filepath = rf'./output_images/{os.path.splitext(in_filename)[0]}.png'
    
    img_from_frames(path, out_filepath, user_height, user_width, verbose = True)