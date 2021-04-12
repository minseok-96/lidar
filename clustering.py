#! /usr/bin/python

import rospy
import math
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point32
from sensor_msgs.msg import PointCloud
import numpy as np

class cloud:

	def __init__(self):

		self.sub_laser = rospy.Subscriber(
			"/scan",
			LaserScan,
			callback=self.judge
		)
		self.pub_marker = rospy.Publisher(
			"/mk_array",
			MarkerArray,
			queue_size=5
		)
		self.point_pub = rospy.Publisher("/scan_",PointCloud,queue_size=5)		

	def judge(self,_ls):

		currentRadian=_ls.angle_min
		_angle=_ls.angle_increment

		_mkArray=MarkerArray()
		pc=PointCloud()
		_dgroup=0.11 # m
		_dp=6.16/1000
		_points=[]
		_groupPoints=[]
		_groupPoints_new=[]
		group_num=0

	#pointCallback(sample)
		# x = np.append(np.arange(-1, 1, 0.1), np.arange(-1, 1, 0.1))
		# y = [1] *20 + [-1] *20

		# print(len(x),len(y))
		# print(x)

		# for x_, y_ in zip(x, y):
		# 	_points.append([x_, y_])
	
	# pointCallback(scan)
		for i in range(0,len(_ls.ranges)):
			x= _ls.ranges[i] *math.cos(currentRadian)
			y= _ls.ranges[i] *math.sin(currentRadian)

			if math.isinf(x) or math.isinf(y):
				# print(x,y)
				currentRadian += _angle
				continue
			_points.append([x,y])
			currentRadian += _angle
			
	# groupPoints
		for i in range(0,len(_points)-1):
			pc.header.frame_id= "laser"
			_distance=self.distance_list(_points[i][0],_points[i][1],_points[i+1][0],_points[i+1][1])
			_ri=self.distance_list(_points[i+1][0],_points[i+1][1],0,0)

			if _distance < self._hypothesis(_dgroup,_dp,_ri):
											
				# insert point to group
				_groupPoints.append(_points[i])

				# last groupPoints to groupPoints_new			
				if i == len(_points)-2:
					if len(_groupPoints) > 5:
						_groupPoints_new.append(_groupPoints)

			# No group == new group
			else:
				# group big enough
				if len(_groupPoints)> 5:
					_groupPoints_new.append(_groupPoints)
					# extract inserted groupPoints
					group_num+=1
				# initialize
				_groupPoints=[]

		#publish marker and PointCloud
		for _gr in _groupPoints_new:
			for i in _gr:
				self.pointCloud(i,pc)

		for _gr in _groupPoints_new:

			mp= self.middlePoint(_gr)
			_mkArray.markers.append(self.setMarker(mp,group_num,2))
			group_num+=1

		self.point_pub.publish(self.pointCloud(i,pc))
		self.pub_marker.publish(_mkArray)

	def pointCloud(self, _points,_pc):
		po=Point32()
		po.x= _points[0]
		po.y= _points[1]
		po.z=0.1
		_pc.points.append(po)
		return _pc

	def middlePoint(self,_gpn):

		_length=len(_gpn)
		_half1=_length/2
		_half2=(_length-1)/2
		_mp=0

		if _length%2==0:
			_mp=_gpn[_half1]
		else:
			_mp=_gpn[_half2]
		
		return _mp
	
	def distance_list(self,x1, y1, x2, y2):
		result = math.sqrt( math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
		return result

	def _hypothesis(self,dgroup,dp,ri):
		_result = dgroup + ri*dp
		#print("_result:{}".format(_result))
		return _result

	def setMarker(self, _p, _id, _op):
		marker = Marker()

		marker.header.frame_id = "laser"
		marker.ns = "position"
		marker.id= _id
		marker.lifetime = rospy.Duration.from_sec(0.1)

		marker.type = Marker.SPHERE
		marker.action = Marker.ADD
		
		marker.pose.position.x = _p[0]
		marker.pose.position.y = _p[1]
		marker.pose.position.z = 0.1
			
		marker.pose.orientation.x = 0.0
		marker.pose.orientation.y = 0.0
		marker.pose.orientation.z = 0.0
		marker.pose.orientation.w = 1.0

		marker.scale.x = 0.07
		marker.scale.y = 0.07
		marker.scale.z = 0.07

		marker.color.r = 0.0
		marker.color.g = 0.0
		marker.color.b = 0.0
		marker.color.a = 1.0

		if _op is 0:
			marker.color.r = 1.0
		elif _op is 1:
			marker.color.g = 1.0
		else:
			marker.color.b = 1.0
			marker.color.g = 0.5
			marker.color.r = 0.5
		return marker


# main

if __name__ == "__main__":
	rospy.init_node("cluster", anonymous=False)
	cl=cloud()
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		cl
		rate.sleep()
