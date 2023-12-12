import threading
import winsound
import cv2
import imutils
from datetime import datetime

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
x, cam_frame = cap.read()
cam_frame = imutils.resize(cam_frame, width=500)
cam_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2GRAY)
cam_frame = cv2.GaussianBlur(cam_frame, (21, 21), 0)
alarm = False
set_alarm = False
counter = 0
def alarm_trigger():
    global alarm
    now = datetime.now()
    current_time = now.strftime("%d-%m-%Y, %H:%M:%S")
    ftime = now.strftime("%Y-%m-%d %H.%M.%S.%f")
    
    #capture image of moving objects
    return_value, image = cap.read()     
    
    #save captured images on the drive with timestamps
    cv2.imwrite(f'Alarm-{ftime}.png', image)  
    for x in range(6):
        if not set_alarm:
            break
            
        #The loudness of the sound is between 2500 to 8000, and duration 500      
        winsound.Beep(3000, 500)
    print("Alarm =", current_time)
    alarm = False
while True:
    x, frame = cap.read()
    frame = imutils.resize(frame, width=500)
    if set_alarm:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        difference = cv2.absdiff(gray, cam_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        cam_frame = gray
        
        #sensitivity of the size of moving objects, between 1000 to 1000000
        if threshold.sum() > 1000:  
            counter += 1
        else:
            if counter > 0:
                counter -= 1
        cv2.imshow("Cam", threshold)
        cv2.imshow("real", frame)
    else:
        cv2.imshow("Cam", frame)
    
    #movement duration sensitivity, between 10 to 100    
    if counter > 10:  
        if not alarm:
            alarm = True    
            threading.Thread(target=alarm_trigger).start()         
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        set_alarm = not set_alarm
        counter = 0
    if key_pressed == ord("q"):
        set_alarm = False
        break
cap.release()
cv2.destroyAllWindows()
