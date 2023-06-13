#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from gtts import gTTS
import os

def callback(data):
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

def googletts():
    # initialize subscriber node called 'googletts'
    rospy.init_node('googletts', anonymous=True)
    # subscribe 2 topics - facerecognition_result and speechrecognition_result
    rospy.Subscriber("/facerecognition_result", String, callback, queue_size=1)
    rospy.Subscriber("/speechrecognition_result", String, callback, queue_size=1)

    rospy.spin()

if __name__ == '__main__':
    googletts()
