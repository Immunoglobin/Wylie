#!/usr/bin/env python3


import cv2
import numpy as np
import argparse
import time
import subprocess
from gpiozero import AngularServo

# Global Flags
scale = 3
blur = False
grayscale = False
laplace = False
alpha = 1.0
threshold = False
recording = False

parser = argparse.ArgumentParser()
parser.add_argument("--device", type=int, default=0, help="Video Device number e.g. 0, use v4l2-ctl --list-devices")
parser.add_argument("--singleframe", type=bool, default=False, help="Use single frame camera instead of dual output thermal")
args = parser.parse_args()


# Initialize servo on GPIO 17
servo = AngularServo(17, min_pulse_width=0.0006, max_pulse_width=0.0025)
servo.angle = -90
	
if args.device:
	dev = args.device
else:
	dev = 0
if args.singleframe:
	singleframe = args.singleframe
else:
	singleframe = False
	

#init video
cap = cv2.VideoCapture('/dev/video'+str(dev), cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0.0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))*scale
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/2)*scale
scaledWidth = int(width * scale)
scaledHeight = int(height * scale)
# Create our window
cv2.namedWindow('Critter-Cam',cv2.WINDOW_GUI_NORMAL)
cv2.resizeWindow('Critter-Cam', scaledWidth, scaledHeight)
font=cv2.FONT_HERSHEY_SIMPLEX


# Set up blob detector
blob_params = cv2.SimpleBlobDetector_Params()

#blob_params.minThreshold = 127
#blob_params.maxThreshold = 255
blob_params.blobColor=255
blob_params.filterByArea = False
blob_params.minArea = 10
blob_params.filterByCircularity = False
blob_params.filterByConvexity = False
blob_params.filterByInertia = False
detector = cv2.SimpleBlobDetector_create(blob_params)


# Define functions before main loop

def play_sound(file):
	subprocess.run(["aplay","-D","default:CARD=Device",file])

def articulate_jaw():
	servo.angle = -90
	time.sleep(1)
	servo.angle = 90
	time.sleep(1)

def rec():
	play_sound("/home/njeffers/heydeer2.wav")
	articulate_jaw()
	now = time.strftime("%Y%m%d--%H%M%S")
	#do NOT use mp4 here, it is flakey!
	videoOut = cv2.VideoWriter('videos/'+now+'output.avi', cv2.VideoWriter_fourcc(*'XVID'),25, (scaledWidth,scaledHeight))
	return(videoOut)






while(cap.isOpened()):

	# Capture frame-by-frame
	ret, frame = cap.read()

	# If we successfully read the camera's frame
	if ret == True:
		if singleframe:
			imdata = frame
		else:
			# Split the Image data from the Thermal data
			imdata,thdata = np.array_split(frame, 2)


		# Convert the real image to RGB
		bgr = cv2.cvtColor(imdata,  cv2.COLOR_YUV2BGR_YUYV)

		#Contrast
		bgr = cv2.convertScaleAbs(bgr, alpha=alpha)

		#bicubic interpolate, upscale and blur
		bgr = cv2.resize(bgr,(scaledWidth,scaledHeight),interpolation=cv2.INTER_CUBIC)#Scale up!


		# Apply our colormap to the real image
		if grayscale:
			heatmap = cv2.applyColorMap(bgr, cv2.COLORMAP_JET)
		else:
			heatmap = bgr
		if blur:
			heatmap = cv2.GaussianBlur(heatmap, (7,7), 0)


		if threshold:
			ret,heatmap = cv2.threshold(heatmap, 200, 255, cv2.THRESH_BINARY)
		if laplace:
			heatmap = cv2.Laplacian(src=heatmap, ddepth=cv2.CV_8U, ksize=3)

		# Do image processing for blob detection
		grey_img = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
		grey_img = cv2.GaussianBlur(grey_img, (7,7), 0)
		ret,grey_img = cv2.threshold(grey_img, 200, 255, cv2.THRESH_BINARY)
		keypoints = detector.detect(grey_img)
		heatmap = cv2.drawKeypoints(heatmap, keypoints, np.array([]), (255,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


		# Render the image to the screen
		cv2.imshow('Critter-Cam',heatmap)

		# If there is a keypoint on screen start recording
		if len(keypoints) > 0 and not recording:
			recording = True
			start = time.time()
			videoOut = rec()
			print("Recording started: ",start)

		if len(keypoints) == 0 and recording:
			recording = False
			print("Stopped recording")

		if recording:
			elapsed = (time.time() - start)
			elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed)) 
			#print(elapsed)
			videoOut.write(heatmap)

		# Wait for the q key to be pressed to quit the application
		keyPress = cv2.waitKey(60)
		if keyPress == ord('q'):
			break
			capture.release()
			cv2.destroyAllWindows()
		if keyPress == ord('b'):
			blur = not blur
		if keyPress == ord('g'):
			grayscale = not grayscale
		if keyPress == ord('l'):
			laplace = not laplace
		if keyPress == ord('t'):
			threshold = not threshold
		if keyPress == ord('f'): #contrast+
			alpha += 0.1
			alpha = round(alpha,1)#fix round error
			if alpha >= 3.0:
				alpha=3.0
		if keyPress == ord('v'): #contrast-
			alpha -= 0.1
			alpha = round(alpha,1)#fix round error
			if alpha<=0:
				alpha = 0.0

