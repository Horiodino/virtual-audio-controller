import cv2
import time
import numpy 
import pyaudio as audiomodule
import HandTrackingModule 
import subprocess

def set_system_volume(volume):
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{int(volume * 65536)}"])

detect = HandTrackingModule.handDetector(detectionCon=0.9)

capture = cv2.VideoCapture(0)
capture.set(1280,720)
time_now = 0

# consts 
thumb_xaxis = 0
index_finger_xaxis = 0
thumb_yaxis = 0
index_finger_yaxis = 0

total_distance = 0
volume_change = 0

while True:
    ret, frame = capture.read()
    response = detect.findHands(frame)
    list = detect.findPosition(frame)

    # the detect is the object that is created from the class handDetector in the HandTrackingModule.py
    # we we are parsing the frame to the function findHands in the class handDetector
    # it will detect the hands and draw the landmarks on the hands
    # the response is the list of the landmarks of the hands
    if len(list) != 0:
        print(list[4],list[8])

        # now to identify the thumb and the index finger we will use the list of the landmarks
        # it can be found on mediapipe hands documentation

        # for the thumb we will use the landmark 4 and and index finger landmark 8

        thumb_xaxis = list[4][1]
        index_finger_xaxis = list[8][1]
        thumb_yaxis = list[4][2]
        index_finger_yaxis = list[8][2]

        # now we will draw a circle on the thumb and the index finger to identify them
        cv2.circle(frame, (thumb_xaxis, thumb_yaxis), 15, (0, 0, 0), cv2.FILLED)
        cv2.circle(frame, (index_finger_xaxis, index_finger_yaxis), 15, (0, 0, 0), cv2.FILLED)

        cv2.line(frame, (thumb_xaxis, thumb_yaxis), (index_finger_xaxis, index_finger_yaxis), (0, 0, 0), 3)

        # now we have to define a alorithm to calculate the distance between the thumb and the index finger
        # which will be used to control the volume of the system
        # we will use the distance formula to calculate the distance between the thumb and the index finger
        # the formula is sqrt((x2-x1)^2 + (y2-y1)^2)

        total_distance = numpy.sqrt((thumb_xaxis - index_finger_xaxis)**2 + (thumb_yaxis - index_finger_yaxis)**2)
        print(total_distance)

        #  the volume will be between 20 to 220
        # vol_zero = 20 
        # vol_max = 220

        # now we have to map the distance to the volume

        # the distance will be between 50 to 300
        # now the distance between these point will be as percentage of the total distance
        # 50 will be 0% and 300 will be 100%

        if total_distance < 10:
            cv2.circle(frame, (thumb_xaxis, thumb_yaxis), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, (index_finger_xaxis, index_finger_yaxis), 15, (0, 255, 0), cv2.FILLED)
        
        if total_distance > 180:
            cv2.circle(frame, (thumb_xaxis, thumb_yaxis), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, (index_finger_xaxis, index_finger_yaxis), 15, (0, 255, 0), cv2.FILLED)

        volume_change = numpy.interp(total_distance, [10, 180], [0, 100])
        print(volume_change)

        # use audio module to change the volume of the system
        print(volume_change/100)
        set_system_volume(volume_change/100)



    curent_time = time.time()
    fps = 1/(curent_time - time_now)
    time_now = curent_time

    # the puttext is for the text that will be on the screen (terminal)
    #  here we are putting the fps on the screen 
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow('frame', frame)
    cv2.setUseOptimized(True)
    cv2.waitKey(1)


    # optimize the code
    # if no movement of hands on screen then no need to detect the hands

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     # sleep for 1 second
    #     time.sleep(1)
    



