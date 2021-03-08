import cv2
import datetime as dt
import os, errno
import pathlib
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('--camid', help='Set the Camera Index')
parser.add_argument('--motionframes', help='How many motion frames before start recording')
parser.add_argument('--nomotionframes', help='how many motion wait before recording stops')
parser.add_argument('--conturarea', help='how many conturs to use if motion is detected (usually 900)')
parser.add_argument('--fps', help='which frameraete to record (normal value 24)')
parser.add_argument('--format', help='which format for recording (DIVX, XVID, MJPG, X264, WMV1, WMV2)')
parser.add_argument('--width', help='Resolution Webcam width')
parser.add_argument('--height', help='Resolution Webcam height')
parser.add_argument('--showvideo', help='Want to see what the camera see ? (true or false)')
parser.add_argument('--saveseq', help='Do you want to save as video or as sequence of jpg')

args = parser.parse_args()
cap = cv2.VideoCapture(int(args.camid))

resolution = (int(args.width),int(args.height))
motion_detected = False
motion_counter = 0
non_motion_counter = 0
videoWriter = None
showvideo = args.showvideo.lower() == "true"

def writeFrame(frame):
    resized = cv2.resize(frame,resolution)
    videoWriter.write(resized)

def createFilePath():
    curDir = '{0}/video/'.format(pathlib.Path().absolute())
    if not os.path.exists(curDir):
        try:
            os.makedirs(curDir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    return '{0}{1}.avi'.format(curDir,dt.datetime.now().strftime("%d_%m_%Y-%H.%M.%S"))
    
def createVideoWriter():
    path = createFilePath()
    writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*args.format), int(args.fps), resolution, True)
    return writer

while cap.isOpened():
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    motion_detected = False   
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 40, 255, cv2.ADAPTIVE_THRESH_MEAN_C)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)       
    clearFrame = None
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        non_motion_counter = int(args.nomotionframes)
        if cv2.contourArea(contour) < int(args.conturarea):
            continue
        motion_detected = True
        print('Contur: Motion detected {0} , motion counter {1} '.format(motion_detected, motion_counter))     
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
    if motion_detected:       
        motion_counter += 1       
        if motion_counter > int(args.motionframes):
            if videoWriter is None:
                videoWriter = createVideoWriter()
            writeFrame(frame2)

    if motion_detected is not True:
        non_motion_counter -= 1
        if non_motion_counter == 0 and videoWriter is not None:
            videoWriter.release()
            videoWriter = None
        
    if showvideo:    
        cv2.imshow("Current Feed", frame1)
        cv2.imshow("Threshold", thresh)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cap.release()
videoWriter.release()
cv2.destroyAllWindows()