#!/usr/bin/env python
import rospy
from std_msgs.msg import String,Int8

import datetime
import thread


rospy.init_node('listener', anonymous=True)
f = open('log_file' + str(datetime.datetime.now()) + '.txt','w')
last_time = rospy.get_time()
last_data = None
occupy = True
game_buffer = []
mouth_buffer = []
motion_buffer = []


# Define a function for the thread
def print_time(threadName, delay):
    global f
    global last_time
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
	try:
    	    if rospy.get_time() - last_time >= 60.0:
		last_time = rospy.get_time()
         	f.close()
        	f = open('log_file' + str(datetime.datetime.now()) + '.txt','w')
	except rospy.ROSInterruptException:
	    pass
	rate.sleep()

def callback(data):
    global f
    global game_buffer
    global occupy
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
    temp = str(datetime.datetime.now()) + ', ' + str(rospy.get_time()) + ', ' + "Game_MAKI" + ', ' + data.data + '\n'
    game_buffer.append(temp)
    if occupy:
        occupy = False
        for element in game_buffer:
    	    f.write(element)
        game_buffer = []
        occupy = True

def callback2(data):
    global f
    global mouth_buffer
    global occupy
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    temp = str(datetime.datetime.now()) + ', ' + str(rospy.get_time()) + ', ' + "mouth_color" + ', ' + str(data.data) + '\n'
    mouth_buffer.append(temp)
    if occupy:
        occupy = False
        for element in mouth_buffer:
    	    f.write(element)
        mouth_buffer = []
        occupy = True

def callback3(data):
    global f
    global motion_buffer
    global occupy
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    temp = str(datetime.datetime.now()) + ', ' + str(rospy.get_time()) + ', ' + "motion_box" + ', ' + str(data.data) + '\n'
    motion_buffer.append(temp)
    if occupy:
        occupy = False
        for element in motion_buffer:
    	    f.write(element)
        motion_buffer = []
        occupy = True

    
def listener():
    global f
    global last_time

    rospy.Subscriber("Game_MAKI", String, callback)	

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def listener2(threadName, delay):#threadName, delay
    global f

    rospy.Subscriber("mouth_color", Int8, callback2)	

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def listener3(threadName, delay):#threadName, delay
    global f

    rospy.Subscriber("motion_box", String, callback3)	

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    

if __name__ == '__main__':
    thread.start_new_thread( print_time, ("Thread-1", 2, ) )
    thread.start_new_thread( listener2, ("Thread-2", 2, ) )
    thread.start_new_thread( listener3, ("Thread-3", 2, ) )
    #thread.start_new_thread( listener4, ("Thread-4", 2, ) )

    listener()
    #listener2()
