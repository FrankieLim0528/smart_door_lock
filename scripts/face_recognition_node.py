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

            # pub.publish("Welcome home " + name + ". Please speak your passphrase to unlock the door!")
            pub.publish(name)
            # sub.unregister()
            rospy.signal_shutdown("Face Recognition for one time")

    # else:
    #     pub.publish("No face recognized!")

# main function
def face_listener(callback):
    rospy.init_node('face_listener', anonymous=True)

    rate = rospy.Rate(RATE)
    pub = rospy.Publisher('facerecognition_result', String, queue_size=1)
    sub = rospy.Subscriber("face_recognition/output", FaceArrayStamped, callback=lambda data: callback(data, pub, rate), queue_size=1)
    # rospy.wait_for_message("face_recognition/output", FaceArrayStamped)
    # sub.unregister()
    # if len(data.faces) > 0:
    #     face = data.faces[0]
    #     if len(face.eyes) > 0:
    #         name = face.label

    #         # pub.publish("Welcome " + name + ". Please speak your passphrase to unlock the door!")
    #         pub.publish(name)
            
    
    rospy.spin()


if __name__ == "__main__":
    time.sleep(1)
    face_listener(callback)


# roslaunch usb_cam usb_cam-test.launch
# roslaunch smart_door_lock face_recognition.launch image:=/usb_cam/image_raw launch_trainer:=false
# roslaunch smart_door_lock smart_door_lock.launch