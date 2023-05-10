import cv2
import time
from BACKEND.Modality1_EyeBlink import f_detector
import imutils
import numpy as np
import os
import joblib
import tempfile

def read_blinks(file_data, max_frames=533):
    detector = f_detector.eye_blink_detector()
    COUNTER = 0
    TOTAL = 0

    cam = cv2.VideoCapture(file_data)

    
    # create a VideoCapture object to read frames
    currentframe=1
    baseline=0
    start_time = time.time()
    tblinks=[]
    ablinks=[]
    while True:
        ret,im = cam.read()
        if currentframe >= max_frames or not ret: break
        #if not ret: break
        #im = cv2.flip(im, 1)
        im = imutils.resize(im, width=720)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        rectangles = detector.detector_faces(gray, 0)
        boxes_face = f_detector.convert_rectangles2array(rectangles,im)
        if len(boxes_face)!=0:
            areas = f_detector.get_areas(boxes_face)
            index = np.argmax(areas)
            rectangles = rectangles[index]
            boxes_face = np.expand_dims(boxes_face[index],axis=0)
            COUNTER,TOTAL = detector.eye_blink(gray,rectangles,COUNTER,TOTAL)
            img_post = f_detector.bounding_box(im,boxes_face,['blinks: {}'.format(TOTAL)])
        else:
            img_post = im 
        end_time = (time.time() - start_time)/60
        baseline = round(TOTAL/end_time)
        tblinks.append(TOTAL)
        ablinks.append(baseline)

        currentframe+=1

    while True:
        if currentframe >= max_frames: break
        currentframe+=1
        tblinks.append(None)
        ablinks.append(None)
    
    # print(len(tblinks))
    # print(len(ablinks))
    average=np.array(ablinks)
    total=np.array(tblinks)
      
    # Clean up the temporary file
    #os.unlink(filename)
  
    cam.release()
    cv2.destroyAllWindows()
    del cam
    return total,average


def BP(file_data, child_conn):
    model = joblib.load('BACKEND\Modality1_EyeBlink\my_blink_model.pkl')
    _, avg = read_blinks(file_data)    
    pred = model.predict([avg])[0]
    prob = model.predict_proba([avg])[0]
    print(f"BP {prob}")
    if pred == 0:
       bp_result = "Lie"
    else:
       bp_result = "True"

    # send the BP result to the parent process through child_conn
    child_conn.send((bp_result, prob))
    print("BP sent result")
    child_conn.close()