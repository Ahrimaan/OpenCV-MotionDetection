# OpenCV-MotionDetection

## Basic Motion Detection written in Python

To start this program first install all needed Packages 
`pip install -r requirements.txt`

after install you can run the script with 

`python main.py --camid 2 --motionframes 5 --nomotionframes 20 --conturarea 700 --fps 24 --format MJPG --width 1024 --height 768`

## Args overview

### --camid
The Index of your cam attached to the pc (default is 0)

### --motionframes
How many motion frames before start recording

### --conturarea
how many conturs to use if motion is detected (usually 900) see [OpenCV Docs](https://docs.opencv.org/master/d3/dc0/group__imgproc__shape.html#ga2c759ed9f497d4a618048a2f56dc97f1)

### --nomotionframes
how many motion wait before recording stops

### --conturarea
how many conturs to use if motion is detected (usually 900)

### --fps
which frameraete to record , you have to experiment around depedning on your cam (i have 10 as a default)

### --format 
which format for recording (DIVX, XVID, MJPG, X264, WMV1, WMV2)

### --width
Resolution Webcam width

### --height
Resolution Webcam height

### --showvideo
Want to see what the camera see ? (true or false)