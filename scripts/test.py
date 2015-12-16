#!/usr/bin/env python

# Author: Tejas Ram

import roslib; roslib.load_manifest('maki_demo')
import rospy, os, sys
import subprocess

def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass

if __name__ == '__main__':
    
    print '---------1'
    os.system("roslaunch maki_demo maki_demo.launch file:='1.wav'")
    
    print '---------2'
    os.system("roslaunch maki_demo maki_demo.launch file:='2.wav'")

    print '---------3'
    os.system("roslaunch maki_demo maki_demo.launch file:='3.wav'")

    print '---------4'
    os.system("roslaunch maki_demo maki_demo.launch file:='4.wav'")

