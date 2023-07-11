#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from gtts import gTTS
import os, time

def callback(data, pub):
    global current_face

    text = data.data
    # check the text before converting into speech
    rospy.loginfo("Input: %s", text)
    # convert text to speech using Google Text-To-Speech API
    # if (text != 'Wrong passphrase, please try again!'):
    #     text = "Welcome home " + text + ". Please speak your passphrase to unlock the door!"
    text = "Welcome home " + text + ". Please speak your passphrase to unlock the door!"
    tts = gTTS(text)
    # save the converted speech into mp3 file
    tts.save("speech.mp3")
    # play the mp3 file
    os.system("mpg321 speech.mp3")
    # remove the mp3 file after playing
    os.remove("speech.mp3")

    time.sleep(1)
    current_face = data.data
    pub.publish(current_face)


def speech_callback(data, pub):
    text = data.data
    # check the text before converting into speech
    rospy.loginfo("Input: %s", text)
    # convert text to speech using Google Text-To-Speech API
    tts = gTTS(text)
    # save the converted speech into mp3 file
    tts.save("speech.mp3")
    # play the mp3 file
    os.system("mpg321 speech.mp3")
    # remove the mp3 file after playing
    os.remove("speech.mp3")

    time.sleep(1)
    pub.publish(current_face)


def googletts():
    # initialize subscriber node called 'googletts'
    rospy.init_node('googletts', anonymous=True)

    # Testing
    pub = rospy.Publisher('/speechgeneration_result', String, queue_size=1)

    # subscribe 2 topics - facerecognition_result and speechrecognition_result
    rospy.Subscriber("/facerecognition_result", String, lambda msg: callback(msg, pub), queue_size=1)
    rospy.Subscriber("/speechrecognition_result", String, lambda msg: speech_callback(msg, pub), queue_size=1)

    rospy.spin()

if __name__ == '__main__':
    current_face = ""
    googletts()
