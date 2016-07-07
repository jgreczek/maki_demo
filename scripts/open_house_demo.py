#!/usr/bin/env python
# Author: Xuan(Juan) Liu(Leo) 
# Maki Demo for Robotics Open House 4/14/2016

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


class maki_gaming:

    def __init__(self,target_topic):
    #styleMap = ['none','astronaut','clown','wizard','dinosaur','animal','doctor','surgeon','teacher']
        self.current_msg = None
	self.last_msg = None
	self.buff_msg = None
	self.key = False
	self.task = []
        self.dm = RobotManager()
	self.lastColor = 1
	self.currentColor = 1
	self.positive_flag = False

        self.styleDict = {}
	self.styleSet = {}
    	self.styleMap = ['none','astronaut','clown','wizard','dinosaur']
        self.colorTask = 1
    #temporary solution # 0 hat, 1 eyes, 2 glasses, 3 clothing, 4 shoes, 5 acc
	self.styleSet['none'] = ['no hat', 'no face accessory','no costume','regular shoes','no accessory']
    	self.styleSet['astronaut'] = ["astrounaut helmet","astronaut face accessory","astronaut costume","astronaut shoes","a flag"]
    	self.styleSet['clown'] = ["clown hat","clown face","clown costume","clown shoes","a horn"]
    	self.styleSet['wizard'] = ["wizard hat","wizard eye","wizard costume","wizard shoes","a wand"]
	self.styleSet['dinosaur'] = ['dinosaur hat', 'no face accessory','dinosaur costume','dinosaur shoes','a mini dinosaur']
	self.game_listener = rospy.Subscriber(target_topic, String, callback = self.callback)
	#self.speech_state_listener = rospy.Subscriber("speech_state", String, callback = self.callback2)
	self.mouth_pub = rospy.Publisher('mouth_color', Int8, queue_size=10)


	self.breath_count = 0
    #formal solution
    #styleSet['none'] = ['none','none','none','none','none']
    ###########################################################
#style dictionary
#formal solution
    	for elem in self.styleMap:
    	    for clothes in self.styleSet[elem]:		
   	         self.styleDict[clothes] = elem 

        self.styleDict['no face accessory'] = ['none','dinosaur'] 
		

#    Xray Game
#    mapX = ["MAKI's eye","MAKI's ear","MAKI's nose"]
#    for part in mapX:
#	if part not in dialog:
#	    dialog[part] = "This part is " + part

    #print dialog.keys()

    def dataProcessing(self, text):
    	global styleDict
    	global styleSet
    	
    	complete = 'complete_'
    	multi = 'multi_'
    	rand = 'rand'
    	_and = 'and'

    #styleCounter = {'none':0,'astronaut':0,'clown':0,'wizard':0,'dinosaur':0,'animal':0,'doctor':0,'surgeon':0,'teacher':0}
    	styleCounter = {'none':0,'astronaut':0,'clown':0,'wizard':0,'dinosaur':0}
        color = {'red mouth':1,'blue mouth':2,'green mouth':3}
	colorName = {'red mouth':'red','blue mouth':'blue','green mouth':'green'}
    	element = text.split(',')
    	element[len(element) - 1] = element[len(element) - 1].strip('\n')
    ############################
    #TODO complete the dm.say orders

        print element
    	if element[0] == "Starting the dress up game!":
            self.task = ['self_introduce','explain','game_introduce','game_initialize']
            length = len(self.task)
            counter = 0
        
	    request = ['start']
            return request
    	elif element[0] == "Dress":
            self.colorTask = color[element[3]]
	    self.currentColor = self.colorTask
            temp1 = element[1:3]
            temp2 = element[4:7]
	    request = temp1[:]
            request.extend(temp2[:])
            for style in self.styleSet.keys():
	    #print 'request',request
            #print 'style',styleSet[style]
	        if request == self.styleSet[style]:
                    temp = complete + style
    	  	    self.task.append(temp)
			
                    #temporary task
		    if not self.lastColor == self.currentColor:
                        self.task.append(_and)
                        self.task.append(colorName[element[3]])
		    ######			

                    length = len(self.task)
                    counter = 0
                    return element
	    for elem in request:
		if elem == 'no face accessory':
		    styleCounter[self.styleDict[elem][0]] += 1
		    styleCounter[self.styleDict[elem][1]] += 1
                else:
	            styleCounter[self.styleDict[elem]] += 1
	
	    for style in styleCounter.keys():
	        if styleCounter[style] > 2:
		    temp = multi + style
                    self.task.append(temp)
                    if not self.lastColor == self.currentColor:
                        self.task.append(_and)
            	        self.task.append(colorName[element[3]])
                    length = len(self.task)
                    counter = 0
		    return element
            import random
            #sequence = [1,2,3,4,5,6,7]
            num = random.randint(1,8)
	    if num == 7:
		num = 1	
	    temp = rand + str(num)
	    self.task.append(temp)
            #self.task.append(_and)
            #temp = rand + str(num[1])
	    #self.task.append(temp)
            if not self.lastColor == self.currentColor:
                self.task.append(_and)
                self.task.append(colorName[element[3]])
            length = len(self.task)
            counter = 0
	    return element
        elif element[0] == "On main menu":
	    print element[0]
            self.task = ['sleep']
            request = ['sleep']
            return request
	elif element[0] == "Start questionnaire": #new added July 1st, by Xuan for coping games processing 
	    self.task = []
	elif element[0] == "Questionnaire answers":
	    self.task = []
	elif element[0] == "Start CS1-Breathing":
	    self.task = ['breathing_introduction','breathing_tutor']
	elif element[0] == "Breath taken":#needed to be change to breath in/out
	    self.task = []
	elif element[0] == "Breath finished":
	    self.task = []
	elif element[0] == "Start EMS":
	    self.task = ['breathing_feedback']
	elif element[0] == "EMS-bad":
	    self.task = ['negative']
	elif element[0] == "EMS-average":
	    self.task = ['neutral']
	elif element[0] == "EMS-good":
	    self.task = ['positive']
	    self.positive_flag = True
	elif element[0] == "Start EMS 2":
	    self.task = ['rap_feedback']
	elif element[0] == "EMS-bad2":
	    self.task = ['negative2']
	elif element[0] == "EMS-average2":
	    self.task = ['neutral']
	elif element[0] == "EMS-good2":
	    self.task = ['positive2']
	    self.positive_flag = True
	elif element[0] == "Start EMS 3":
	    self.task = ['value_feedback']
	elif element[0] == "EMS-bad3":
	    self.task = ['negative3']
	    if self.positive_flag:
		self.task.append('negative3_choice')
	elif element[0] == "EMS-average3":
	    self.task = ['neutral3']
	    if self.positive_flag:
		self.task.append('neutral3_choice')
	elif element[0] == "EMS-good3":
	    self.task = ['positive3']
	elif element[0] == "Start CS2-ES1-Vein":
	    self.task = ['choose_introduction','choose_tutor']
	elif element[0] == "vein chosen":
	    self.task = ['choose_feedback']
	elif element[0] == "Start CS2-ES2-Spray":#Start CS2-ES2-Spray
	    self.task = ['spray_introduction','spray_tutor']
	elif element[0] == "spray finished":
	    self.task = ['spray_feedback']
	elif element[0] == "Start CS2-ES3-Insertion":#Start CS2-ES3-Insertion
	    self.task = ['insertion_tutor']
	elif element[0] == "Insertion finished":
	    self.task = ['insertion_feedback']
	elif element[0] == "Start CS2-ES4-Gauze":
	    self.task = ['rap_introduction','rap_tutor']
	elif element[0] == "Gauze finished":
	    self.task = []
	elif element[0] == "Start value reminder":
	    self.task = ['value_introduction','value_tutor']
	elif element[0] == "P1 taken":
	    self.task = ['value_you']
	elif element[0] == "P2 taken":
	    self.task = ['value_family']
	elif element[0] == "P3 taken":
	    self.task = ['value_reason']
	elif element[0] == "P4 taken":
	    self.task = ['value_doctor']
	elif element[0] == "P5 taken":
	    self.task = ['value_ivy']
	elif element[0] == "Value finished":
	    self.task = self.task #do nothing here
	elif element[0] == "Start pain anxiety":
	    self.task = ['coping_introduction','coping_remind']
	elif element[0] == "1-great" or element[0] == "2-okay" or element[0] == "3-average":
	    self.task = ['coping_thanks1','coping_game_index','coping_next']
	elif element[0] == "4-little-anxious" or element[0] == "5-anxious" or element[0] == "6-very-anxious":
	    self.task = ['coping_thanks2','coping_game_index','coping_next']
	elif element[0] == "Start pain anxiety 2":
	    self.task = ['end_thank','end_feel']
	elif element[0] == "1-great2" or element[0] == "2-okay2" or element[0] == "3-average2":
	    self.task = ['coping_thanks1','end_encourage']
	elif element[0] == "4-little-anxious2" or element[0] == "5-anxious2" or element[0] == "6-very-anxious2":
	    self.task = ['coping_thanks2','end_encourage']
	elif element[0] == "end":# needed to be added in the end.html page
	    self.task = ['end']
	

	
	
	

#    elif element[0] == "xray":#don't need this part temporarily
	#print 'xray'
#       request = element[1]
#    	return dialog[request] 


    def callback(self,data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    #print type(data), type(data.data), len(data.data)
    	self.raw_msg = data.data
    	if not self.raw_msg == self.buff_msg:
    	    self.current_msg = self.dataProcessing(self.raw_msg)
	    print self.raw_msg
            if self.current_msg == self.last_msg and (not self.current_msg == None):    
	        self.key = False
            	print self.key
		print self.current_msg
		print self.last_msg
    	    else:
            	self.key = True

	#TODO change to a mouth color publisher according to the current_msg
            
        #target_color = current_msg[len(current_msg)-1] #this is formal solution
        #temp solution
            
            self.mouth_pub.publish(self.colorTask)
    
        self.buff_msg = self.raw_msg

    def run(self):
	rate = rospy.Rate(5.0)
	while not rospy.is_shutdown():
    	    try:   
	    #listener("Game_MAKI")
            	if self.key == True:

	            print 'last_msg', self.last_msg
		    print 'current_msg', self.current_msg
                    print 'task', self.task, self.colorTask
                #dm = RobotManager()
		###working area April 6th
		    for elem in self.task:
		    	self.dm.say(elem, wait = True)  

		    self.task = []
 	            self.last_msg = self.current_msg
		    self.lastColor = self.currentColor
        	    self.key = False
		###	

    	    except rospy.ROSInterruptException:
	        pass
	    rate.sleep()




if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(5.0)
    
    mg = maki_gaming("Game_MAKI")
    mg.run()
    

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
