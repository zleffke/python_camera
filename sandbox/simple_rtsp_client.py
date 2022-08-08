#!/usr/bin/env python3
"""
#   Title: Simple RTSP Stream Viewer
# Project: All Sky Camera
# Version: 0.0.1
#    Date: Aug, 2022
#  Author: Zach Leffke, KJ4QLP
# Comment:
# - Sandbox for learning to work with RTSP cameras and OpenCV
"""

import cv2
import os
import numpy as np
import datetime
import string

RTSP_URL = 'rtsp://admin:sky_track_2022@192.168.1.10/live'

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print('Cannot open RTSP stream')
    exit(-1)

frame_counter = 0
while True:
    _, frame = cap.read()
    ts = datetime.datetime.utcnow()
    ts_str = datetime.datetime.strftime(ts, '%Y-%m-%dT%H:%M:%S.%fZ')
    print(frame_counter)
    frame_cnt_str = "Frame: {:d}".format(frame_counter)

    pixels = np.shape(frame) #reads number of pixels
    scale = 2
    h_pix = int(pixels[1]/scale) #extracts horizontal pixel count, div by 2
    v_pix = int(pixels[0]/scale) #extracts vertical pixel count, div by 2

    #frame_resize=cv2.resize(frame, (950,600))
    frame=cv2.resize(frame, (h_pix,v_pix), interpolation = cv2.INTER_AREA) #resizes image

    # describe the type of font
    # to be used.
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Use putText() method for
    # inserting text on video
    cv2.putText(frame,
                ts_str,
                (40, 40),
                font, .75,
                (255, 255, 255),
                1,
                cv2.LINE_4)

    cv2.putText(frame,
                frame_cnt_str,
                (40, 80),
                font, .75,
                (255, 255, 255),
                1,
                cv2.LINE_4)

    color = (64,64,255)
    # Line thickness of 2 px
    thickness = 1

    #----RECTANGLE----
    # Start coordinate, here (5, 5)
    # represents the top left corner of rectangle
    start_point = (h_pix-100, v_pix-100)
    # Ending coordinate, here (220, 220)
    # represents the bottom right corner of rectangle
    end_point = (h_pix+100, h_pix+100)
    # Using cv2.rectangle() method
    # Draw a rectangle with blue line borders of thickness of 2 px
    #frame = cv2.rectangle(frame, start_point, end_point, color, thickness)

    #----CIRCLE----
    x_offset = 9
    y_offset = 1
    center = (int(h_pix/2+x_offset), int(v_pix/2+y_offset))
    rad_offset = -16
    radius = int(v_pix/2+rad_offset)
    frame = cv2.circle(frame, center, radius, color, thickness)
    frame = cv2.circle(frame, center, int(radius*2/3), color, thickness)
    frame = cv2.circle(frame, center, int(radius*1/3), color, thickness)

    #----NSEW Indicators
    cv2.putText(frame, "N", (int(center[0]-15), int(center[1]-v_pix/2+15)),
                font, .5, color, 1, cv2.LINE_4)
    cv2.putText(frame, "0", (int(center[0]+4), int(center[1]-v_pix/2+15)),
                font, .5, color, 1, cv2.LINE_4)
    cv2.putText(frame, "S", (int(center[0]-15), int(center[1]+v_pix/2-5)),
                font, .5, color, 1, cv2.LINE_4)
    cv2.putText(frame, "180", (int(center[0]+4), int(center[1]+v_pix/2-5)),
                font, .5, color, 1, cv2.LINE_4)
    cv2.putText(frame, "E", (int(center[0]+h_pix/2-178), int(center[1]-2)),
                font, .5, color, 1, cv2.LINE_4)
    cv2.putText(frame, "90", (int(center[0]+h_pix/2-178), int(center[1]+12)),
                font, .5, color, 1, cv2.LINE_4)
    cv2.putText(frame, "W", (int(center[0]-h_pix/2+165), int(center[1]-2)),
                font, .5, color, 1, cv2.LINE_4)
    cv2.putText(frame, "270", (int(center[0]-h_pix/2+150), int(center[1]+12)),
                font, .5, color, 1, cv2.LINE_4)

    #----RETICLE-----
    line_len = v_pix/2-10
    h_start = (int(center[0] - line_len), int(center[1]))
    h_stop  = (int(center[0] + line_len), int(center[1]))
    frame = cv2.line(frame, h_start, h_stop, color, thickness)

    v_start = (int(center[0]), int(center[1] - line_len))
    v_stop  = (int(center[0]), int(center[1] + line_len))
    frame = cv2.line(frame, v_start, v_stop, color, thickness)

    cv2.imshow('All Sky Camera', frame)
    frame_counter += 1

    ts_end = datetime.datetime.utcnow()
    loop_td = (ts_end - ts).total_seconds()
    print(loop_td)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
