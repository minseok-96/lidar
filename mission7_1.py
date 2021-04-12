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
		self.point_pub = rospy.Publisher("/scan_p",PointCloud,queue_size=5)


	def callback(self,_data): #deep copy

		ls=LaserScan()
		ps=PointCloud()
		ps.header.frame_id="laser"
		_r=2

		for i in range(0,720):	
			_theta= 3.14 - (i * 0.01)
			_z=_r*math.sin(_theta)
			for j in range(0,720):
				_theta2= 3.14 - (j * 0.01)
				_x=_r*math.cos(_theta)*math.cos(_theta2)
				_y=_r*math.cos(_theta)*math.sin(_theta2)

				po=Point32()
				po.x=_x
				po.y=_y
				po.z=_z	
			#print(po.z)
			#for self.j in range(0,len(_data.ranges)):
			#po.x=po.x*math.cos(_data.angle_increment*self.j)
			#po.y=po.y*math.sin(_data.angle_increment*self.j)
			#print(po.z)
				ps.points.append(po)
		self.point_pub.publish(ps)
		#self.j+=1
		#if(self.j>=90):
		#	self.j=0
		#print(self.j)
		
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