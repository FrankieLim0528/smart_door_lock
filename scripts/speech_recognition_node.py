#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import speech_recognition as sr

import time
import os
import threading

from config import DATA_DIR, MAX_ATTEMPTS, LOCKDOWN_PERIOD


door_locked = """
  ==========+ 
 |  __  __  ||
 | |  ||  | ||
 | |  ||  | ||
 | |__||__| ||
 |  __  __()|| ... Door Locked!
 | |  ||  | +|
 | |  ||  | ||
 | |  ||  | ||
 | |__||__| ||
 |__________|- 
"""


door_unlocked = """
     /|
    / |
   /__|______
  |  __  __  |
  | |  ||  | | 
  | |__||__| |
  |  __  __()| ... Door Unlocked!
  | |  ||  | |
  | |  ||  | |
  | |__||__| |
  |__________| 

"""

RATE = 0.1 

def callback_recognize_passphrase(msg):
    face_name = msg.data

    # load the user's passphrase
    file_path = os.path.join(DATA_DIR, face_name, "passphrase.txt")
    print("File Path: " + file_path)
    passphrase = ""
    try:
        with open(file_path, "r") as f:
            passphrase = f.readline()
    except IOError:
        return

    # keep record of user attempts
    if face_name not in attempts_left:
        attempts_left[face_name] = MAX_ATTEMPTS
    print("Before while loop")

    # block user by disabling speech recognition after exceeding maximum attempts
    if attempts_left[face_name] == 0:
        pass

    r = sr.Recognizer()       
    r.energy_threshold = 300  # Adjust the energy threshold as needed
    print("Before MIcrohpone")
    with sr.Microphone() as source: # obtain audio from the microphone
        print(">>> Say something! " + str(attempts_left[face_name]) + " attempts left")
        audio = r.listen(source)
        # recognize speech
        msg = String()
        result = ""
        try:
            result = r.recognize_google(audio) # online using Google Web Speech API
            rospy.loginfo("SR result: " + result)

            if result == passphrase:
                msg.data = "Door unlocked!"
                print(door_unlocked)
                rospy.signal_shutdown("correct passphrase, door unlocked")
            else:
                msg.data = "Wrong passphrase, please try again!"
                print(door_locked)
                attempts_left[face_name] -= 1
                pub.publish(msg)
            # freeze system after exceeding maximum attempts
            if attempts_left[face_name] == 0:
                msg.data = "You have exceeded the maximum number of attempts, please try again " + str(LOCKDOWN_PERIOD) + " seconds later."
                rospy.loginfo(msg)
                pub.publish(msg)
                rate.sleep()
                rospy.loginfo("Lock user {} for {}".format(face_name, LOCKDOWN_PERIOD))
                rospy.sleep(LOCKDOWN_PERIOD)
                attempts_left[face_name] = MAX_ATTEMPTS  # reset attempts after account lockout period
                rospy.loginfo("Lockdown period for {} is over!".format(face_name))
                
                
        except sr.UnknownValueError:
            rospy.loginfo("SR could not understand audio")
        except sr.RequestError as e:
            rospy.loginfo("Could not request results from Google Speech Recognition service; {0}".format(e))
            

if __name__ == '__main__':
    attempts_left = {}          # store passphrase attempts left for each user

    rospy.init_node('speech_recognition', anonymous=True)
    rate = rospy.Rate(RATE)
    pub = rospy.Publisher('/speechrecognition_result', String, queue_size=1)
    rospy.Subscriber("/speechgeneration_result", String, callback_recognize_passphrase, queue_size=1)

    rospy.spin()
    
