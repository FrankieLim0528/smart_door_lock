#!/usr/bin/env python

import rospy
from opencv_apps.msg import FaceArrayStamped
from std_msgs.msg import String
import time

# constant variables
RATE = 0.1  # the higher, the faster for next detection


# callback function
def callback(data, pub, rate):
    name = ""
    if len(data.faces) > 0:
        face = data.faces[0]
        if len(face.eyes) > 0:
            name = face.label

            pub.publish(name)
            rospy.signal_shutdown("Face Recognition for one time")


# main function
def face_listener(callback):
    rospy.init_node('face_listener', anonymous=True)

    rate = rospy.Rate(RATE)
    pub = rospy.Publisher('facerecognition_result', String, queue_size=1)
    sub = rospy.Subscriber("face_recognition/output", FaceArrayStamped, callback=lambda data: callback(data, pub, rate), queue_size=1)        
    rospy.spin()


if __name__ == "__main__":
    time.sleep(1)
    face_listener(callback)

# roslaunch usb_cam usb_cam-test.launch
# roslaunch smart_door_lock face_recognition.launch image:=/usb_cam/image_raw launch_trainer:=false
# roslaunch smart_door_lock smart_door_lock.launch