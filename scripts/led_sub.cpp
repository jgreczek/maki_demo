#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <iostream>
#include "ros/ros.h"
#include "std_msgs/MultiArrayLayout.h"
#include "std_msgs/MultiArrayDimension.h"
#include "std_msgs/Int32MultiArray.h"
int Arr[50];
void arrayCallback(const std_msgs::Int32MultiArray::ConstPtr& array);
int main(int argc, char **argv)
{
ros::init(argc, argv, "led_sub");
ros::NodeHandle n;
ros::Subscriber sub3 = n.subscribe("led_array", 50, arrayCallback);
while (ros::ok())
	{
ros::spinOnce();
for(int j = 0; j < 50; j++)
{
printf("%d, ", Arr[j]);
}
printf("\n");
sleep(2);
}
}

void arrayCallback(const std_msgs::Int32MultiArray::ConstPtr& array)
{
int i = 0;
// print all the remaining numbers
for(std::vector<int>::const_iterator it = array->data.begin(); it != array->data.end(); ++it)
{
Arr[i] = *it;
i++;
}
return;
}
