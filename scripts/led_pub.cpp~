#include <stdio.h>
#include <stdlib.h>
#include "ros/ros.h"
#include "std_msgs/Int8.h"


int main(int argc, char **argv)
{
	ros::init(argc, argv, "led_pub");
	ros::NodeHandle n;
	ros::Publisher pub = n.advertise<std_msgs::Int8>("led_array", 50);
	while (ros::ok())
	{
		std_msgs::Int8 val;
		val.data = 21;
		pub.publish(val);
		ROS_INFO("I published 12");
		ros::spinOnce();
		sleep(3);
	}
}
