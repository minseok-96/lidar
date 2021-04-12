#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

class distance:
	def __init__(self):
		rospy.init_node("again1",anonymous=False)
		self.sub_laser=rospy.Subscriber("/scan",LaserScan, callback=self.callback)
		#self.pub_laser=rospy.Publisher("/scan_c",LaserScan,ques)

	def callback(self,_data):
		
		Max= max(_data.ranges)
		Min= min(_data.ranges)
		print(Max,Min)
if __name__=="__main__":
	er = distance()
	rospy.spin()
			
