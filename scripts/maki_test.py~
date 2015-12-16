#!/usr/bin/env python

#Author: Tejas Ram
""" This code is used to feed commands to maki to carry out actions or speak out a sentence.
The sound files of each sentence are located in the cordial_sound package under 'sounds' folder.
The motions given should be declared in maki_cordial_server under the motions variable as well as in the maki.ppr file
"""

#action supporting imports
import roslib; roslib.load_manifest('cordial_testing'); roslib.load_manifest('cordial_sound')
import rospy, os, sys
import actionlib
import geometry_msgs.msg
#sound supporting imports
from cordial_sound.msg import SoundRequest
from cordial_sound.libsoundplay import SoundClient

from tablet_manager import TabletManager
from cordial_core.msg import *

import os
from csv import reader
from random import random, choice

def sleep(t):
     try:
        rospy.sleep(t)
     except:
        pass 

maki_sound_file = "1.wav"	# the sound file which the maki should play	
maki_body_act = "eyeroll"	# the action which maki should perform which should be listed in maki_cordial_server and maki.ppr
loop_count = 2		# number of times the action must be repeated
loop_time = 2		# the time interval between each action
flag = 0

# class to define actions and send it to the maki_cordial_server
class Test_Maki():
    def __init__(self):
	maki_body = actionlib.SimpleActionClient("/CoRDial/Behavior", BehaviorAction)	# the action server of maki_cordial_server
        rospy.sleep(2.0)
	global loop_count
	global loop_time 
        global flag 

	self.new_behavior_time = rospy.Time.now()			
	self.eye_gaze_time = rospy.Time.now()
	self.blink_time = rospy.Time.now() + rospy.Duration(10)

        while not loop_count == 0 or flag == 1:	# while number of times the actions are repeated
            print loop_count
	    loop_count -= 1
	    if rospy.Time.now() >= self.new_behavior_time:
		behav = maki_body_act
		self.new_behavior_time = rospy.Time.now() + rospy.Duration(loop_time)	
		maki_body.send_goal(BehaviorGoal(name=behav))	# sending the behavior to maki
		print "sent behavior: ", behav
		sleep(loop_time)		


if __name__=="__main__":
    
    # when actions are defined, the maki Test class is called
    if not maki_body_act == "" and maki_sound_file == "":
    	rospy.init_node("face_relay")
    	Test_Maki()

    # when a sound file is defined it calls the soundplay_node
    if not maki_sound_file == "" and maki_body_act == "":
	rospy.init_node('soundplay_test', anonymous = True)
        soundhandle = SoundClient()
        rospy.sleep(1)
        soundhandle.stopAll()
        print maki_sound_file
        soundhandle.playWave(maki_sound_file)
        sleep(7)
    
    # when both sound file and action are defined it calls both the test class and soundplay_node
    if not maki_sound_file == "" and not maki_body_act == "":
	rospy.init_node('face_relay')
	os.system("rospy.init_node('soundplay_test', anonymous = True)")
        soundhandle = SoundClient()
        rospy.sleep(1)
        soundhandle.stopAll()
        print maki_sound_file
	soundhandle.playWave(maki_sound_file)
	Test_Maki()
        sleep(7)





