from keras.models import model_from_json
from keras import Model
import cv2
import numpy as np
import tempfile
import os

def load_model(filename):
    # load json and create model
    json_file = open(f'BACKEND\Modality2_FacialExpressions\{filename}.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(f'BACKEND\Modality2_FacialExpressions\{filename}.h5')
    return loaded_model

def fer(data):
  loaded_model = load_model('fer')
    # load the layers from the pre-trained, loaded model
  layer_names = [layer.name for layer in loaded_model.layers]
  layer_outputs = [layer.output for layer in loaded_model.layers]
  # print(f"layer_names total: {len(layer_names)}")

  # pre-process input X
  # data -= np.mean(data, axis=0)
  # data /= np.std(data, axis=0)

  # for each entry, we will convert each of the 300 images (48, 48, 1) to encoding vectors
  encoding_model = Model(inputs = loaded_model.inputs, outputs = layer_outputs[23])

  X_cnn = np.zeros((data.shape[0], data.shape[1], 2048))

  # print(f"xi.shape={xi.shape}, yi.shape={yi.shape}, yi={yi}")
  predictedX = encoding_model.predict(data)
  # the encoding vector for each facial image is a 336 dimensional vector, 
  # and there are 300 frames.
  # print(f"predictedX has shape {predictedX.shape}")
  X_cnn = predictedX

  return X_cnn

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def get_face_from_image(img):
  # resized_image = image_resize(img, width=1000)
  gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
  face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
  faces = face.detectMultiScale(gray, 1.2, 5)
  return (True, faces[0]) if len(faces)>0 else (False, None)

def preprocess_image(img):
  gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) # we turn the image to grayscale
  cropped_img = np.expand_dims(np.expand_dims(cv2.resize(gray_img, (48, 48)), -1), 0)
  cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)
  return cropped_img

# Given a filename, reads the video and captures frames from it
# For each frame, extracts a facial image if available
# Saves the cropped facial image
def read_video(file_data, max_frames=600):
  
  cam = cv2.VideoCapture(file_data)
  # else:
  #   # Save the video data to a temporary file
  #   with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
  #       f.write(file_data.read())
  #       filename = f.name
  #   #print(filename)
  #   # Open the video file with OpenCV
  #   cam = cv2.VideoCapture(filename, apiPreference=cv2.CAP_FFMPEG)

  currentframe = 0

  xdata = np.zeros((max_frames, 48*48))
  while(True):
    ret, frame_image = cam.read()
    #print(frame_image)
    if currentframe >= max_frames: break # limit the max number of frames we examine

    if ret: # a frame is found.
      # name='./data/frame' + str(currentframe) + '.jpg' # name of the image to store
      # print('Showing...'+name)

      # detect a primary face from the given frame image (if any)
      (detected, rect) = get_face_from_image(frame_image)
      # print(f"frame.shape={frame.shape}")

      # yhat = np.zeros((1, 7))

      x = np.zeros(48*48)
      # if a face is detected for the frame, crop the image
      if detected:
        (x, y, w, h) = rect
        cropped_face = frame_image[y:y+h, x:x+w]
        cropped_img = preprocess_image(cropped_face) # the low-res result ready for prediction
        # print(f'cropped_img shape={cropped_img.shape}')
        x = cropped_img.flatten()
        # print(f"x.shape: {x.shape}, min and max: {np.min(x), np.max(x)}")

        # make a prediction
        # yhat = loaded_model.predict(cropped_img)
      # print(f"yhat={yhat}")
      
      xdata[currentframe, :] = x
      # xdata[currentframe, :, :] = yhat

      currentframe+=1

    else: # we've reached the end of the video.
      break

  # Clean up the temporary file
  # os.unlink(filename)
  
  # Release all space and windows once done
  cam.release()
  cv2.destroyAllWindows()

  return xdata

def FE(file_data, child_conn):
    gru = load_model('gru_model4_76.19')
    data = read_video(file_data=file_data)
    # print(data.shape)
    data = data.reshape(600, 48, 48, 1)
    roi = fer(data)
    # print(roi.shape)
    roi = roi.reshape(1, 600, 2048)
    pred = gru.predict(roi)[0][0]
    print(f"FE {pred}")
    if pred < 0.5:
       fe_result = "False"
    else:
       fe_result = "True"
    # send the FE result to the parent process through child_conn
    child_conn.send((fe_result, pred))
    print("FE sent result")
    child_conn.close()
