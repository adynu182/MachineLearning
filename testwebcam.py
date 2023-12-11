import cv2
webcam = cv2.VideoCapture(0,cv2.CAP_DSHOW)


stop=False
while stop==False:
    ret,frame=webcam.read()
    
    if ret==True:
        cv2.imshow("Camera1",frame)
        key=cv2.waitKey(1)
        if key==ord("q"):
            break
            
webcam.release()
cv2.destroyAllWindows()

