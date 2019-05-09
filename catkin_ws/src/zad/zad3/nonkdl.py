#!/usr/bin/env python
import rospy
import yaml
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker

def callback(data):
    marker=PoseStamped()
    main_matrix = translation_matrix((0, 0, 0))
    infile = yaml.load(open("./wynik.yaml"))
    j0 = infile["j0"]
    j1 = infile["j1"]
    j2 = infile["j2"]
    j=[j0,j1,j2]


    i=0
    while i<3:
        th=j[i]['len']
	x=j[i]['z']
	if i==2:
		b=-1
	else:
		b=1
	if i==1:
		p=0.1
	else:
		p=0
	if i==0:
		a=1
	else:
		a=0

	matrix_a = translation_matrix((0, 0, a))
	matrix_al = rotation_matrix(j[i]['r'], (0, 1, 0))
	matrix_d= translation_matrix((0, x*th, 0))
	matrix_th = rotation_matrix(data.position[i], (0, 0, b))
	trans = concatenate_matrices(matrix_a,matrix_al, matrix_th,matrix_d)
	t_list[i] = trans
	#print(i)
	#print(trans)
        i += 1

    main_matrix = concatenate_matrices(t_list[0], t_list[1], t_list[2])


    x, y, z = translation_from_matrix(main_matrix)


    
    xq, yq, zq, wq = quaternion_from_matrix(main_matrix)
    print(quaternion_from_matrix(main_matrix))
    marker.header.frame_id = 'floor'
    marker.header.stamp = rospy.Time.now()


    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = z

    marker.pose.orientation.x = xq
    marker.pose.orientation.y = -zq
    marker.pose.orientation.z = yq
    marker.pose.orientation.w = wq

   
    publisher.publish(marker)

def nonkdl_listener():
    rospy.init_node('NONKDL_DKIN', anonymous = False)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':
    t_list = {}
    publisher = rospy.Publisher('nonkdl', PoseStamped, queue_size=10)

    try:

	    nonkdl_listener()
    except rospy.ROSInterruptException:

            pass
