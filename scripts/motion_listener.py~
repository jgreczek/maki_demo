#!/usr/bin/env python
#Author Xuan Liu (Juan Leo)
#action supporting imports
import roslib; roslib.load_manifest('cordial_testing'); roslib.load_manifest('cordial_sound')
import rospy, os, sys
import actionlib
import geometry_msgs.msg
from std_msgs.msg import Int8
from std_msgs.msg import String

#sound supporting imports
from cordial_sound.msg import SoundRequest
from cordial_sound.libsoundplay import SoundClient

from tablet_manager import TabletManager
from cordial_core.msg import *

import os
from csv import reader
from random import random, choice

motion_l = None

def callback(data):    
	goal = data.data
    	rospy.loginfo(rospy.get_caller_id() + "I heard %s", goal)    
	motion_l.maki_body.send_goal(BehaviorGoal(behavior=goal))

class ml:

    def __init__(self):
	self.maki_body = actionlib.SimpleActionClient("/CoRDial/Behavior", BehaviorAction)
    
    def motion_listener(self):
    	rospy.init_node('motion_listener', anonymous=True)
   	rospy.Subscriber('motion_box', String, callback)
    	rospy.spin()

    
	
if __name__ == '__main__':
    motion_l = ml()
    motion_l.motion_listener()
