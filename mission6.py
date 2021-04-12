#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan

class Laser:
	def __init__(self):
		rospy.init_node("mission6",anonymous=False)
		self.sub_laser= rospy.Subscriber("/scan",LaserScan,callback=self.callback)
		self.pub_laser= rospy.Publisher("/scan_c",LaserScan,queue_size=5)

	def callback(self,_data):

		_ls=LaserScan()
		_ls.header.frame_id="laser"
		_ls.angle_min=-3.14
		_ls.angle_max=+3.14
		_ls.angle_increment=6.28/360.0
		_ls.time_increment=0.1
		_ls.range_min=_data.range_min
		_ls.range_max=_data.range_max

		for i in range(0,len(_data.ranges)):
			_ls.ranges.append(2)
		for i in range(0, len(_data.intensities)):
			_ls.intensities.append(3)
		
		self.pub_laser.publish(_ls)

	def callback2(self,_data):

		_data.ranges= [2 for i in range(0,len(_data.ranges))]
		_data.intensities =[3 for i in range(0,len(_data.intensities))]
		self.pub_laser.publish(_data)

if __name__=="__main__":
	la=Laser()
	rospy.spin()
