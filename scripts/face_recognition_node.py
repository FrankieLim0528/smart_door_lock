#!/usr/bin/env python

import rospy
from opencv_apps.msg import FaceArrayStamped


# testing callback function
def test_callback(data):
    if len(data.faces) > 0:
        for face in data.faces:
            if len(face.eyes) > 0:
                rospy.loginfo(face.label)

# listener
def face_listener(callback):
    rospy.init_node('face_listener', anonymous=True)
    rospy.Subscriber("face_recognition/output", FaceArrayStamped, callback)
    rospy.spin()


if __name__ == "__main__":
    face_listener(test_callback)


# roslaunch usb_cam usb_cam-test.launch
# roslaunch smart_door_lock face_recognition.launch image:=/usb_cam/image_raw launch_trainer:=false