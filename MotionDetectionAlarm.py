import threading
import winsound

import cv2
import imutils
from datetime import datetime

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

x, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0

def beep_alarm():
    global alarm
    now = datetime.now()
    current_time = now.strftime("%d-%m-%Y, %H:%M:%S")
    ftime = now.strftime("%Y-%m-%d %H.%M.%S.%f")
    return_value, image = cap.read()      #capture gerakan
    cv2.imwrite(f'Alarm-{ftime}.png', image)  #simpan capture gerakan di drive
    for x in range(3):

        if not alarm_mode:
            break
        winsound.Beep(2500, 500)
    print("Alarm =", current_time)
    alarm = False
    
while True:
    x, frame = cap.read()
    frame = imutils.resize(frame, width=500)
    
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
        
        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw
        
        if threshold.sum() > 1000:  #sensitifitas ukuran objeck bergerak
            # print(threshold.sum())
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1
        
        cv2.imshow("Cam", threshold)
        cv2.imshow("real", frame)
    else:
        cv2.imshow("Cam", frame)
        
    if alarm_counter > 30:  #sensitifitas durasi gerakan
        if not alarm:
            alarm = True    
            threading.Thread(target=beep_alarm).start()
            
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break
      
cap.release()
cv2.destroyAllWindows()
                



