#!/usr/bin/env python

import rospy
from opencv_apps.msg import FaceArrayStamped
from std_msgs.msg import String


# constant variables
RATE = 0.1  # the higher, the faster for next detection


# callback function
def callback(data, pub, rate):
    name = ""
    if len(data.faces) > 0:
        for face in data.faces:
            if len(face.eyes) > 0:
                name = face.label
                pub.publish("Welcome " + name + ". Please speak your passphrase to unlock the door!")
                rate.sleep()
                break
    # else:
    #     pub.publish("No face recognized!")

# main function
def face_listener(callback):
    rospy.init_node('face_listener', anonymous=True)
    rate = rospy.Rate(RATE)
    pub = rospy.Publisher('facerecognition_result', String, queue_size=10)
    rospy.Subscriber("face_recognition/output", FaceArrayStamped, callback=lambda data: callback(data, pub, rate), queue_size=1)
    rospy.spin()


if __name__ == "__main__":
    face_listener(callback)


# roslaunch usb_cam usb_cam-test.launch
# roslaunch smart_door_lock face_recognition.launch image:=/usb_cam/image_raw launch_trainer:=false
# roslaunch smart_door_lock smart_door_lock.launch