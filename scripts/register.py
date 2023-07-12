#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String

import enchant
import os

from config import DATA_DIR


banner = r"""
███████╗███╗   ███╗ █████╗ ██████╗ ████████╗    ██████╗  ██████╗  ██████╗ ██████╗     ██╗      ██████╗  ██████╗██╗  ██╗
██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝    ██╔══██╗██╔═══██╗██╔═══██╗██╔══██╗    ██║     ██╔═══██╗██╔════╝██║ ██╔╝
███████╗██╔████╔██║███████║██████╔╝   ██║       ██║  ██║██║   ██║██║   ██║██████╔╝    ██║     ██║   ██║██║     █████╔╝ 
╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║       ██║  ██║██║   ██║██║   ██║██╔══██╗    ██║     ██║   ██║██║     ██╔═██╗ 
███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║       ██████╔╝╚██████╔╝╚██████╔╝██║  ██║    ███████╗╚██████╔╝╚██████╗██║  ██╗
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

GROUP S7: The Smart Locksmiths
             ________
            / ______ \
            || _  _ ||
            ||| || |||
            |||_||_|||
            || _  _o|| (o)
            ||| || |||
            |||_||_|||      ^~^  ,
            ||______||     ('Y') )
           /__________\    /   \/
  _________|__________|__ (\|||/) _________
          /____________\
          |____________|

Please choose:
[1] Register Passphrase

"""

dictionary = enchant.Dict("en_US")

# check for valid passphrase
def is_valid_passphrase(passphrase):
    words = passphrase.split()
    if len(words) > 0 and len(words) <= 2:
        if all(dictionary.check(word) for word in words):
            return True
    return False


def callback_register_passphrase(msg):
    face_name = msg.data

    passphrase = raw_input("Hi {}! Please enter your passphrase in English [Maximum 2 words]: ".format(face_name))
    if is_valid_passphrase(passphrase):
        rospy.loginfo("Valid passphrase")
        # file_path = r"/home/mustar/catkin_ws/src/smart_door_lock/passphrase.txt"
        file_path = os.path.join(DATA_DIR, face_name, "passphrase.txt")
        if not os.path.exists(file_path):
            os.mkdir(os.path.join(DATA_DIR, face_name))
        with open(file_path, "w") as f:
            f.write(passphrase)
            rospy.loginfo("User [{}] with passphrase [{}] registered successfully".format(face_name, passphrase))
        rospy.signal_shutdown('reason')
    else:
        print("Invalid passphrase.")



if __name__ == "__main__":
    rospy.init_node('register_passphrase_node', anonymous=True)
    
    print(banner)
    option = raw_input(">> ")
    print(option)
    if option == '1':
        rospy.Subscriber("/facerecognition_result", String, callback_register_passphrase)
    rospy.spin()