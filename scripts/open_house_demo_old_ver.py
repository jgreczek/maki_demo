#!/usr/bin/env python
# Author: Xuan(Juan) Liu(Leo) 

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8

#action supporting imports
import roslib; roslib.load_manifest('cordial_testing'); roslib.load_manifest('cordial_sound')
import rospy, os, sys
import actionlib
import geometry_msgs.msg
#sound supporting imports
from cordial_sound.msg import SoundRequest
from cordial_sound.libsoundplay import SoundClient


#robot_manager
from robot_manager import RobotManager

from tablet_manager import TabletManager
from cordial_core.msg import *
from std_msgs.msg import String

import os
from csv import reader
from random import random, choice

import threading
import logging

def sleep(t):
     try:
        rospy.sleep(t)
     except:
        pass 

#dialog = {}
styleDict = {}
styleSet = {}
current_msg = None
last_msg = None
buff_msg = None
key = False
task = []
length = len(task)
counter = 0

def initDialogueDict():
    #global dialog
    global styleDict
    global styleSet 
    #styleMap = ['none','astronaut','clown','wizard','dinosaur','animal','doctor','surgeon','teacher']
    styleMap = ['astronaut','clown','wizard']
    #temporary solution # 0 hat, 1 eyes, 2 glasses, 3 clothing, 4 shoes, 5 acc
    styleSet['astronaut'] = ["red hat","pink eyes","studying glasses","pink clothing","pink shoes","pink cat"]
    styleSet['clown'] = ["yellow hat","yellow eyes","yellow glasses","white clothing","yellow shoes","green cat"]
    styleSet['wizard'] = ["blue hat","blue eyes","costume glasses","blue clothing","blue shoes","blue cat"]
    #formal solution
    #styleSet['none'] = ['none','none','none','none','none']
    ###########################################################
#style dictionary
#formal solution
    for elem in styleMap:
    	for clothes in styleSet[elem]:
   	    styleDict[clothes] = elem 

#    Xray Game
#    mapX = ["MAKI's eye","MAKI's ear","MAKI's nose"]
#    for part in mapX:
#	if part not in dialog:
#	    dialog[part] = "This part is " + part

    #print dialog.keys()

def dataProcessing(text):
    #text.remove('\n')
    global styleDict
    global styleSet
    global task, length, counter
    complete = 'complete_'
    multi = 'multi_'
    rand = 'rand'
    _and = 'and'

    #styleCounter = {'none':0,'astronaut':0,'clown':0,'wizard':0,'dinosaur':0,'animal':0,'doctor':0,'surgeon':0,'teacher':0}
    styleCounter = {'astronaut':0,'clown':0,'wizard':0}
    element = text.split(',')
    element[len(element) - 1] = element[len(element) - 1].strip('\n')
    ############################
    #TODO complete the dm.say orders

    #print element
    if element[0] == "Start":
        task = ['up','self_introduce','explain','game_introduce','game_initialize']
        length = len(task)
        counter = 0
        
	request = ['start']
        return request
    elif element[0] == "Dress":
        request = element[1:7] #TODO need to change if number of items changed
	#print 'Dress'
        for style in styleSet.keys():
	    #print 'request',request
            #print 'style',styleSet[style]
	    if request == styleSet[style]:
                temp = complete + style
    	  	task.append(temp)
                length = len(task)
                counter = 0
                return request
	for elem in request:
	    styleCounter[styleDict[elem]] += 1
	
	for style in styleCounter.keys():
	    if styleCounter[style] > 2:
		temp = multi + style
                task.append(temp)
                length = len(task)
                counter = 0
		return request
	i = 2
	while i > 0:
	    i = i - 1
            import random
            num = random.randint(1,7)	
	    temp = rand + str(num)
	    task.append(temp)
	    if i:
            	task.append(_and)	
        length = len(task)
        counter = 0
	return request 
    elif element[0] == 'End':
        task = ['sleep']
        request = ['sleep']
        return request

#    elif element[0] == "xray":#don't need this part temporarily
	#print 'xray'
#       request = element[1]
#    	return dialog[request] 


def callback(data):
    global current_msg
    global key
    global last_message
    global buff_msg
    
    #determine game type according to the data head tag!!!!!!!!!

    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    #print type(data), type(data.data), len(data.data)
    raw_msg = data.data
    if not raw_msg == buff_msg:
    	current_msg = dataProcessing(raw_msg)
        if current_msg == last_msg and (not current_msg == None):    
	    key = False
            print key
    	else:
            key = True

	#TODO change to a mouth color publisher according to the current_msg
        pub = rospy.Publisher('mouth_color', Int8, queue_size=10)
        #target_color = current_msg[len(current_msg)-1] #this is formal solution
        #temp solution
        target_color = 1
        if task[0] == "complete_astronaut":
    	    target_color = 1
        elif task[0] == "complete_clown":
	    target_color = 2
        elif task[0] == "complete_wizard":
	    target_color = 3
        pub.publish(target_color)
    
    buff_msg = raw_msg


def listener(target_topic):

    rospy.Subscriber(target_topic, String, callback)
    #rospy.Subscriber()
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

if __name__ == '__main__':
    initDialogueDict()
    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(5.0)
    dm = RobotManager()
    listener("Game_MAKI")
    while not rospy.is_shutdown():
    	try:   
	    #listener("Game_MAKI")
            if key == True:

	    	print 'last_msg', last_msg
		print 'current_msg', current_msg
                print 'task', task
                #dm = RobotManager()
		###working area April 6th
		for elem in task:
		    dm.say(elem)  

		task = []
 	        last_msg = current_msg
        	key = False
		###	
		
    		#dm.say("self_introduce")#use a dictionary here, and a global variable 'task', dm.say(sentence[task]) 

    	except rospy.ROSInterruptException:
	    pass
	
	#print '++'
		
	rate.sleep()





'''
old initialization
    mapHat = ["red hat", "yellow hat", "blue hat"]
    mapGlasses = ["studying glasses", "costume glasses", "yellow glasses"]	
    mapEyes = ["pink eyes", "yellow eyes", "blue eyes"]
    mapClothes = ["white clothing", "pink clothing", "blue clothing"]
    mapShoes = ["pink shoes", "blue shoes", "yellow shoes"]
    mapAcc = ["green cat", "blue cat", "pink cat"]
    for hat in mapHat:
	for eyes in mapEyes:
	    for glasses in mapGlasses:
		for clothes in mapClothes:
		    for shoes in mapShoes:
			for acc in mapAcc:
			    combo = (hat, eyes, glasses, clothes, shoes, acc)
                            if combo not in dialog:
				dialog[combo] = "Wow, Maki is wearing a " + combo[0] + ', a ' + combo[1] + ', ' + combo[3] + ' and ' + combo[4] + ' with beautiful ' + combo[2]  + '. Maki also has a cute ' + combo[5] + '. Maki is so happy, thanks!'

'''
