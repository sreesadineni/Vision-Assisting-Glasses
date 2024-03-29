# REQUIREMENTS FOR CODE:-
# PRE-INSTALLED OPENCV,DLIB,ESPEAK LIBRARIES IN RASPBERRY PI.

# 6.2 SOURCE CODE:
# Our project consists of two codes. They are

# 1) CODE FOR ULTRASONIC SENSOR (Distance calculation)
import RPi.GPIO as GPIO
import time
import subprocess
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
def distance():
# set Trigger to HIGH
GPIO.output(GPIO_TRIGGER, True)
# set Trigger after 0.01ms to LOW
time.sleep(0.00001)
GPIO.output(GPIO_TRIGGER, False)
StartTime = time.time()
StopTime = time.time()
# save StartTime
while GPIO.input(GPIO_ECHO) == 0:
StartTime = time.time()
# save time of arrival
while GPIO.input(GPIO_ECHO) == 1:
StopTime = time.time()
# time difference between start and arrival
TimeElapsed = StopTime – StartTime
 distance = (TimeElapsed * 34300) / 2
 return distance
def execute_unix(inputcommand):
p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
return output
a = 'obstacle nearby'
c = 'espeak -ven+f3 -k5 -s150 --punct="<characters>" "%s" 2>>/dev/null' % a
if __name__ == '__main__':
try:
while True:
dist = distance()
print ("Measured Distance = %.1f cm" % dist)
if dist < 20:
execute_unix(c)
time.sleep(1)
# Reset by pressing CTRL + C
except KeyboardInterrupt:
print('Measurement stopped ')


# 2) CODE FOR FACE RECOGNITION:-
import face_recognition
import cv2
import numpy as np
from espeak import espeak
video_capture = cv2.VideoCapture(0)
#list of known family members for 
# Family member 1
sree_image = face_recognition.load_image_file("sree.jpg")
sree_face_encoding = face_recognition.face_encodings(sree_image)[0]
#Family member 2
meghana_image = face_recognition.load_image_file("meg2.jpg")
meghana_face_encoding = face_recognition.face_encodings(meghana_image)[0]
#Family member 3
bhavesh_image = face_recognition.load_image_file("bha2.jpg")
bhavesh_face_encoding = face_recognition.face_encodings(bhavesh_image)[0]
# Create arrays of known face encodings and their names
known_face_encodings = [
 sree_face_encoding,
 meghana_face_encoding,
 bhavesh_face_encoding
]
known_face_names = [
 " Sree ",
 " Meghana ",
]
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
def execute_unix(inputcommand):
p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
 
(output, err) = p.communicate()
return output
while True:
 # Grab a single frame of video
 ret, frame = video_capture.read()
 # Resize frame of video to 1/4 size for faster face recognition processing
 small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
 # Convert the image from BGR color (which OpenCV uses) to RGB color (which 
face_recognition uses)
 rgb_small_frame = small_frame[:, :, ::-1]
 # Only process every other frame of video to save time
 if process_this_frame:
 # Find all the faces and face encodings in the current frame of video
 face_locations = face_recognition.face_locations(rgb_small_frame)
 face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
 face_names = []
 for face_encoding in face_encodings:
 # See if the face is a match for the known face(s)
 matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
 name = "Unknown"
 
 # Or instead, use the known face with the smallest distance to the new face
 face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
 best_match_index = np.argmin(face_distances)
 if matches[best_match_index]:
 name = known_face_names[best_match_index]
 c = 'espeak -ven+f3 -k5 -s150 --punct="<characters>" "%s" 2>>/dev/null' % name
 execute_unix(c)
 
 face_names.append(name)
 
 process_this_frame = not process_this_frame
 # Display the results
 for (top, right, bottom, left), name in zip(face_locations, face_names):
 # Scale back up face locations since the frame we detected in was scaled to 1/4 size
 top *= 4
 right *= 4
 bottom *= 4
 left *= 4
 # Draw a box around the face
 cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
 # Draw a label with a name below the face
 cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
 font = cv2.FONT_HERSHEY_DUPLEX
 cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
 # Display the resulting image
 cv2.imshow('Video', frame)
 # Hit 'q' on the keyboard to quit!
 if cv2.waitKey(1) & 0xFF == ord('q'):
 break
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()