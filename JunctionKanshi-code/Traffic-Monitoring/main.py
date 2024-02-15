# Importing Libraries
import cv2
import dlib
import time
import math
import numpy as np

# Video capture
video = cv2.VideoCapture("https://streaming1.highwaytraffic.go.th/Phase3/PER_3_009_IN.stream/chunklist_w1042704716.m3u8") # This is public link you can put this link in VLC to watch this steam.

# Constant Declaration
WIDTH = 1280
HEIGHT = 720

logo = cv2.imread("static/JunctionKanshiLogo.png", cv2.IMREAD_UNCHANGED)  #Logo must is PNG with transparency
logo = cv2.resize(logo, (50, 75))  # Resize as needed
position = 'bottom-right' #Location as needed

def overlay_logo(frame, logo, position, margin=10):
    frame_h, frame_w, _ = frame.shape
    logo_h, logo_w, _ = logo.shape

    if position == 'top-right':
        x, y = frame_w - logo_w - margin, margin
    elif position == 'top-left':
        x, y = margin, margin
    elif position == 'bottom-right':
        x, y = frame_w - logo_w - margin, frame_h - logo_h - margin
    elif position == 'bottom-left':
        x, y = margin, frame_h - logo_h - margin

    # If the logo has transparency (4 channels), we need to blend it accordingly.
    if logo.shape[2] == 4:
        overlay = logo[..., :3]  # RGB channels
        mask = logo[..., 3:]  # Alpha channel
        background = frame[y:y+logo_h, x:x+logo_w]
        foreground = cv2.bitwise_and(overlay, overlay, mask=mask)
        background = cv2.bitwise_and(background, background, mask=cv2.bitwise_not(mask))
        frame[y:y+logo_h, x:x+logo_w] = cv2.add(background, foreground)
    else:
        frame[y:y+logo_h, x:x+logo_w] = logo

    return frame