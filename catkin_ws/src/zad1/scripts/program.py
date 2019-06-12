#!/usr/bin/env python
import rospy
import click
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

def talker():
	pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size = 10)
	rospy.init_node('gadacz')
	rate = rospy.Rate(10)
	message = Twist()
	while not rospy.is_shutdown():
		character = click.getchar()
		if character == frw_char:
			message.linear.x  = 1.0
			message.angular.z = 0.0
		elif character ==bwd_char:
			message.linear.x  = -1.0
			message.angular.z = 0.0
		elif character ==lft_char:
			message.linear.x  = 0.0
			message.angular.z = 1.0
		elif character ==rth_char:
			message.linear.x  = 0.0
			message.angular.z = -1.0

	 	elif character =='q':
			break 

		pub.publish(message)
		rate.sleep()

if __name__ == '__main__':
	try:
		frw_char = rospy.get_param('fwd')
		bwd_char = rospy.get_param('bwd')
		lft_char = rospy.get_param('lft')
		rth_char = rospy.get_param('rth')	
		talker()
	except rospy.ROSInterruptException:
		pass
