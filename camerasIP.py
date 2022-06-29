import cv2
import numpy as np

from config import *

AXIS_HORIZONTAL = 1
AXIS_VERTICAL = 0

filename_bedroom = f'rtsp://{CAMERA_BEDROOM_USER}:{CAMERA_BEDROOM_PASSWORD}@{CAMERA_BEDROOM_IP}:{PORT}/{STREAM}'
capture_bedroom = cv2.VideoCapture(filename_bedroom)

filename_room = f'rtsp://{CAMERA_ROOM_USER}:{CAMERA_ROOM_PASSWORD}@{CAMERA_ROOM_IP}:{PORT}/{STREAM}'
capture_room = cv2.VideoCapture(filename_room)

while (capture_bedroom.isOpened()):
    ret_bedromm, frame_bedromm = capture_bedroom.read()
    ret_romm, frame_romm = capture_room.read()

    if ret_bedromm == True and ret_romm == True:

        # Concatenate images
        frame = np.concatenate((frame_bedromm, frame_romm), axis=AXIS_HORIZONTAL)

        # Display two cameras
        cv2.namedWindow("camerasIP", cv2.WINDOW_NORMAL)
        cv2.imshow('camerasIP', frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        # If windows is close then break
        if cv2.getWindowProperty('camerasIP',cv2.WND_PROP_VISIBLE) < 1:
            break
        
    else:
        print(f'ret_bedromm: {ret_bedromm} ret_romm: {ret_romm}')
        if ret_bedromm == False:
            capture_bedroom.release()
            capture_bedroom = cv2.VideoCapture(filename_bedroom)
        if ret_romm == False:
            capture_room.release()
            capture_room = cv2.VideoCapture(filename_room)
        continue

capture_bedroom.release()
capture_room.release()
cv2.destroyAllWindows()