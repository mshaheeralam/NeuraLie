from imutils.video import VideoStream
import cv2
import time
from BACKEND.Modality1_EyeBlink import f_detector
import imutils
import numpy as np

def eye_blink():
    detector = f_detector.eye_blink_detector()
    COUNTER = 0
    TOTAL = 0
    vs = VideoStream(src=0).start()
    blinks = 0
    start_time = time.time()
    while True:
        im = vs.read()
        im = cv2.flip(im, 1)
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
            img_post = f_detector.bounding_box(im,boxes_face,['total blinks: {}'.format(TOTAL)])
        else:
            img_post = im 

        end_time = (time.time() - start_time)/60
        blinks = round(TOTAL/end_time)
        cv2.putText(img_post,f"average blinks: {blinks}",(10,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        cv2.imshow('blink_detection',img_post)
        if cv2.waitKey(1) &0xFF == ord('q'):
            break

    vs.stream.release()
    cv2.destroyAllWindows()

    return blinks

eye_blink()