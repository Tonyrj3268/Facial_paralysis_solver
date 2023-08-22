import numpy as np
import cv2
import ganimation_IR_use 
from face_landmark import facemesh
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("按鍵Q-結束視訊錄製")
while(camera.isOpened()):
    ret, frame = camera.read()    
    if ret==True:
        x, y, w, h = int(frame.shape[1]/2-128),int(frame.shape[0]/2-128),256,256
        frame = cv2.flip(frame,180)
        draw_1=cv2.rectangle(frame, (x-2,y-2), (x+w+2,y+h+2), (0,255,0), 2)
        cv2.imshow('frame',draw_1)
        if cv2.waitKey(1) == ord('c'):
            input_img = cv2.resize(frame[y:y+h, x:x+w], (128,128))
            cv2.imwrite("./capture_image/" + 'frame' + '.jpg', frame)
            cv2.imwrite("./capture_image/" + 'input_img' + '.jpg', input_img)
            print('生成模型')
            ga = ganimation_IR_use.ganimation(input_img)
            result = ga.produce_pics()
            print('標記landmark中')
            face = facemesh.facemesh(result[0])
            landmarks = face.produce()
            print(landmarks)
            
        #elif cv2.waitKey(1) == ord('q'):
            break
    else:
        break





camera.release()
cv2.destroyAllWindows()

