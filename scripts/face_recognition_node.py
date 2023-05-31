#!/usr/bin/env python

import rospy
from opencv_apps.msg import FaceArrayStamped
from std_msgs.msg import String


# callback function
def callback(data, pub):
    if len(data.faces) > 0:
        for face in data.faces:
            if len(face.eyes) > 0:
                pub.publish(face.label)

# main function
def face_listener(callback):
    rospy.init_node('face_listener', anonymous=True)
    pub = rospy.Publisher('face_recognition_result', String, queue_size=10)
    rospy.Subscriber("face_recognition/output", FaceArrayStamped, callback=lambda data: callback(data, pub))
    rospy.spin()


if __name__ == "__main__":
    face_listener(callback)


# roslaunch usb_cam usb_cam-test.launch
# roslaunch smart_door_lock face_recognition.launch image:=/usb_cam/image_raw launch_trainer:=false