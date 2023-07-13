# smart_door_lock

## Setup

1. Create Catkin workspace if not exists.
   ```
   $ mkdir catkin_ws
   $ cd catkin_ws/
   $ mkdir src
   $ catkin_make     # build/ and devel/ folders are created
   ```
2. Setting Terminal
   ```
   $ echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
   $ echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
   $ bash
   ```
3. Clone the repository into your workspace
   ```
   $ cd ~/catkin_ws/src
   $ git clone https://github.com/FrankieLim0528/smart_door_lock.git
   ``` 
4. Install dependencies in the workspace
   ```
   $ rosdep install --from-paths src --ignore-src -r -y
   ```
5. Create, edit and execute Python script
   ```
   $ cd scripts/
   $ touch <script>.py
   $ chmod +x <script.py>
   
   $ python <script>.py
   ```

## Project Structure
```
smart_door_lock
├── CMakeLists.txt
├── include
│   └── smart_door_lock
├── launch
│   └── smart_door_lock.launch
├── package.xml
├── README.md
├── scripts
│   ├── face_recognition_node.py
│   ├── speech_generation_node.py
│   └── speech_recognition_node.py
├── src
├── msg
└── srv
```

## Commands

```
# Start ROS Master
$ roscore

# Nodes
$ rosnode list
$ rosnode info /<node>
$ rosnode ping /<node>

# Topic
$ rostopic echo /<topic>   # print Publisher message
$ rostopic info /<topic>
$ rostopic pub -1 /<topic> std_msgs/String "data: 'Hello World'"
$ rostopic pub -r 5 /<topic> std_msgs/String "data: 'Hello World'"

# Visualize ROS Graph
$ rosrun rqt_graph rqt_graph

# Run Node
$ rosrun <package> <script>

# Build ROS package
$ catkin_make

# Open cam
$ roslaunch usb_cam usb_cam-test.launch

# Train face recognition (Set launch_trainer:=false after finish training)
$ roslaunch smart_door_lock face_recognition.launch image:=/usb_cam/image_raw launch_trainer:=true

# Register passphrase
$ roslaunch smart_door_lock register_passphrase.launch

# Launch main program
$ roslaunch smart_door_lock smart_door_lock.launch

```

## Sample Script Paths

- Online Speech Recognition
```
~/catkin_ws/src/rc-home-edu-learn-ros/rchomeedu_speech/scripts/google_sr.py

$ pip install SpeechRecognition

```

- Text To Speech
```
# Online
~/catkin_ws/src/rc-home-edu-learn-ros/rchomeedu_speech/scripts/google_tts.py

$ pip install gTTS
$ sudo apt install mpg321

```

## Debug
- Speech Recognition Issue
```
Traceback (most recent call last):
  File "speech_recognition_node.py", line 5, in <module>
    import speech_recognition as sr
  File "/home/ubuntu/.local/lib/python2.7/site-packages/speech_recognition/__init__.py", line 1513
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transciption_id}"
                                                                           ^
SyntaxError: invalid syntax
```
Solution: Replace line 1513 in `__init__.py` from 
```
endpoint = f"https://api.assemblyai.com/v2/transcript/{transciption_id}"

to 

endpoint = "https://api.assemblyai.com/v2/transcript/" + transciption_id
```
 
```
AttributeError: Could not find PyAudio; check installation
```
Solution:
```
$ sudo apt-get install portaudio19-dev python-pyaudio
$ pip install PyAudio
```

Missing PocketSphinx Module

Solution: https://pypi.org/project/pocketsphinx/0.1.0/
```
$ sudo apt-get install -qq python python-dev python-pip build-essential swig libpulse-dev libasound2-dev
$ pip install setuptools_scm scikit-build
$ pip install pocketsphinx # only support python 3.8+
```

## Launch File
- Each <node> tag specifies a node to launch.
- The `name` attribute specifies a unique name for the node.
- The `pkg` attribute specifies the ROS package that contains the node.
- The `type` attribute specifies the Python script to run.
- The `output` attribute determines where the output from the node will be displayed (screen in this case).

## Git Cheatsheet
```
# Configurations
git config --global user.email "email@example.com"
git config --global user.name "name"

# Commit
git add <file>
git commint -m "commit message"
git push origin <branch>

# Update
git pull

```
Note: Alternatively, you can use GitHub Desktop.


## References
- https://w3.cs.jmu.edu/spragunr/CS354_S19/labs/packaging/package_lab.shtml
