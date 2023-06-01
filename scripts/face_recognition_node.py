#!/usr/bin/env python

import rospy
from opencv_apps.msg import FaceArrayStamped
from std_msgs.msg import String


# callback function
def callback(data, pub):
    name = ""
    if len(data.faces) > 0:
        for face in data.faces:
            if len(face.eyes) > 0:
                name = face.label
                print("name: " + name)
                # pub.publish("Welcome " + name + ". Please speak your passphrase to unlock the door!")
    # else:
    #     print("No face recognized!")
    #     pub.publish("No face recognized!")


# main function
def face_listener(callback):
    rospy.init_node('face_listener', anonymous=True)
    pub = rospy.Publisher('facerecognition_result', String, queue_size=10)
    rospy.Subscriber("face_recognition/output", FaceArrayStamped, callback=lambda data: callback(data, pub))
    rospy.spin()


if __name__ == "__main__":
    face_listener(callback)


# roslaunch usb_cam usb_cam-test.launch
# roslaunch smart_door_lock face_recognition.launch image:=/usb_cam/image_raw launch_trainer:=false