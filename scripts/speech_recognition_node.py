#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import speech_recognition as sr

# recognize speech in audio file
# audio_file = "path/to/audio/file.wav"
# audio = sr.AudioFile(audio_file)
# with audio as source:
#     recognized_text = recognize_speech(recognizer.record(source))


def googlesr():
    rospy.init_node('googlesr', anonymous=True)
    pub = rospy.Publisher('result', String, queue_size=10)

    while not rospy.is_shutdown():
        # obtain audio from the microphone
        r = sr.Recognizer()
        r.energy_threshold = 300  # Adjust the energy threshold as needed
        
        # get available microphones
        # print(sr.Microphone.list_microphone_names())
        # mic = sr.Microphone(device_index=3)

        with sr.Microphone() as source:
            print(">>> Say something!")
            r.adjust_for_ambient_noise(source, duration=5)
            audio = r.listen(source, phrase_time_limit=3)
            #audio = r.record(source, duration=5)
        
        # write audio to a WAV file
        with open("microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())
        
        # audio_file = sr.AudioFile("microphone-results.wav")
        # with audio_file as source:
        #     audio_file = r.record(source, duration=5, offset=0)
        #     r.recognize_google(audio_data=audio_file)

        # recognize speech
        try:
            # result = r.recognize_google(audio) # online using Google Web Speech API
            result = r.recognize_sphinx(audio) # offline using CMUSPhinx
            print("SR result: " + result)
        except sr.UnknownValueError:
            print("SR could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        pub.publish(result)

if __name__ == '__main__':
    try:
        googlesr()
    except rospy.ROSInterruptException:
        pass