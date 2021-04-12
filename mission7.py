#!/usr/bin/env python

import rospy
import math 
import copy
import numpy as np
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32

class Laser():
	def __init__(self):
		
		rospy.init_node("mission7",anonymous=False)
		self.laser_sub = rospy.Subscriber("/scan",LaserScan,callback=self.callback)
		self.point_pub = rospy.Publisher("/scan_",PointCloud,queue_size=5)
		

	def callback(self,_data): #deep copy

		ps=PointCloud()
		ps.header.frame_id="laser"
		radius=5

		for i in range(0,len(_data.ranges)):	
			po=Point32()
			po.z=1
			po.x=radius*math.cos(_data.angle_increment*i)
			po.y=radius*math.sin(_data.angle_increment*i)
			ps.points.append(po)
		self.point_pub.publish(ps)
			
		
	def callback2(self,_data):#light copy

		ls=LaserScan()
		ps=PointCloud()
		po=Point32()
		_data.ranges=[3 for i in range(0,len(_data.ranges))]

		ps.header.frame_id="laser"

		for i in range(0,len(_data.ranges)):
			
			po.x=_data.ranges[i]*math.cos(_data.angle_increment*i)
			po.y=_data.ranges[i]*math.sin(_data.angle_increment*i)
			po.z=1
			ps.points.append(copy.copy(po))
		print(ps)
		self.point_pub.publish(ps)

if __name__=='__main__':

	las=Laser()
	rospy.spin()