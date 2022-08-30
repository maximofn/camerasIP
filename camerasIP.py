import cv2
import numpy as np

from config import *

AXIS_HORIZONTAL = 1
AXIS_VERTICAL = 0

# Open cameras
filename_bedroom = f'{PROTOCOL}://{CAMERA_BEDROOM_USER}:{CAMERA_BEDROOM_PASSWORD}@{CAMERA_BEDROOM_IP}:{PORT}/{HD_STREAM}'
capture_bedroom = cv2.VideoCapture(filename_bedroom)
if capture_bedroom.isOpened():
    bedroom_opened = True
    print("Bedroom camera connected in HD")
else:
    bedroom_opened = False
    print("Bedroom camera not connected in HD, trying in SD")
    filename_bedroom = f'{PROTOCOL}://{CAMERA_BEDROOM_USER}:{CAMERA_BEDROOM_PASSWORD}@{CAMERA_BEDROOM_IP}:{PORT}/{SD_STREAM}'
    capture_bedroom = cv2.VideoCapture(filename_bedroom)
    if capture_bedroom.isOpened():
        bedroom_opened = True
        print("Bedroom camera connected in SD")
    else:
        bedroom_opened = False
        print("Bedroom camera not connected in SD")
filename_room = f'{PROTOCOL}://{CAMERA_ROOM_USER}:{CAMERA_ROOM_PASSWORD}@{CAMERA_ROOM_IP}:{PORT}/{HD_STREAM}'
capture_room = cv2.VideoCapture(filename_room)
if capture_room.isOpened():
    room_opened = True
    print("Room camera connected in HD")
else:
    room_opened = False
    print("Room camera not connected in HD, trying in SD")
    filename_room = f'{PROTOCOL}://{CAMERA_ROOM_USER}:{CAMERA_ROOM_PASSWORD}@{CAMERA_ROOM_IP}:{PORT}/{SD_STREAM}'
    capture_room = cv2.VideoCapture(filename_room)
    if capture_room.isOpened():
        room_opened = True
        print("Room camera connected in SD")
    else:
        room_opened = False
        print("Room camera not connected in SD")


while (capture_bedroom.isOpened() or capture_room.isOpened()):
    # Capture frame-by-frame
    if capture_bedroom.isOpened():
        ret_bedroom, frame_bedroom = capture_bedroom.read()
        # If capturated frame is not in HD, resize it
        if frame_bedroom.shape[0] != HD_RESOLUTION[0]:
            frame_bedroom = cv2.resize(frame_bedroom, (HD_RESOLUTION[1], HD_RESOLUTION[0]))
    else:
        ret_bedroom = False
    if capture_room.isOpened():
        ret_room, frame_room = capture_room.read()
        # If capturated frame is not in HD, resize it
        if frame_room.shape[0] != HD_RESOLUTION[0]:
            frame_room = cv2.resize(frame_room, (HD_RESOLUTION[1], HD_RESOLUTION[0]))
    else:
        ret_room = False

    # If some camera is desconnected, try to reconnect
    if bedroom_opened and not ret_bedroom:
        capture_bedroom = cv2.VideoCapture(filename_bedroom)
        if capture_bedroom.isOpened():
            print("Bedroom camera reconnected:")
        else:
            print("Bedroom camera not reconnected:")
    if room_opened and not ret_room:
        capture_room = cv2.VideoCapture(filename_room)
        if capture_room.isOpened():
            print("Room camera reconnected:")
        else:
            print("Room camera not reconnected:")

    if ret_bedroom == True and ret_room == True:
        # Concatenate images
        frame = np.concatenate((frame_bedroom, frame_room), axis=AXIS_HORIZONTAL)
        # Display two cameras
        cv2.namedWindow("camerasIP", cv2.WINDOW_NORMAL)
        cv2.imshow('camerasIP', frame)
    elif ret_bedroom == False and ret_room == True:
        # Display room camera
        cv2.namedWindow("camerasIP", cv2.WINDOW_NORMAL)
        cv2.imshow('camerasIP', frame_room)
    elif ret_bedroom == True and ret_room == False:
        # Display bedroom camera
        cv2.namedWindow("camerasIP", cv2.WINDOW_NORMAL)
        cv2.imshow('camerasIP', frame_bedroom)
    else:
        print(f'ret_bedroom: {ret_bedroom} ret_room: {ret_room}')
        if ret_bedroom == False:
            capture_bedroom.release()
        if ret_room == False:
            capture_room.release()
        continue

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    # If windows is close then break
    if cv2.getWindowProperty('camerasIP',cv2.WND_PROP_VISIBLE) < 1:
        break

capture_bedroom.release()
capture_room.release()
cv2.destroyAllWindows()