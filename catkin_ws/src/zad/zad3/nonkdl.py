#!/usr/bin/env python
import rospy
import yaml
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker

def callback(data):
    marker=Marker()
    main_matrix = translation_matrix((0, 0, 0))
    infile = yaml.load(open("./wynik.yaml"))
    j0 = infile["j0"]
    j1 = infile["j1"]
    j2 = infile["j2"]
    j=[j0,j1,j2]
    #print(data.position[0])
    #print(data.position[1])
    #print(data.position[2])

    i=0
    while i<3:
        th=j[i]['len']
	x=j[i]['z']
	b=th*j[i]['z']
	if i==2:
		b=-1
	else:
		b=1
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
    print(main_matrix)

    x, y, z = translation_from_matrix(main_matrix)
    string=str(x)+" "+str(y)+" "+str(z)
    #print(string)

    
    xq, yq, zq, wq = quaternion_from_matrix(main_matrix)
    string=str(xq)+" "+str(yq)+" "+str(zq)+" "+str(wq)
    #print(string)
        
    marker.type = marker.CUBE
    marker.action=marker.ADD
    marker.header.frame_id = 'floor'
    marker.header.stamp = rospy.Time.now()


    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = z

    marker.pose.orientation.x = xq
    marker.pose.orientation.y = yq
    marker.pose.orientation.z = zq
    marker.pose.orientation.w = wq

    marker.scale.x = 0.1;
    marker.scale.y = 0.1;
    marker.scale.z = 0.1;
    marker.color.r = 0.0;
    marker.color.g = 1.0;
    marker.color.b = 1.0;
    marker.color.a = 1.0;

   
    publisher.publish(marker)

def nonkdl_listener():
    rospy.init_node('NONKDL_DKIN', anonymous = False)
    # publisher = rospy.Publisher('n_k_axes', PoseStamped, queue_size=10)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':
    t_list = {}
    publisher = rospy.Publisher('nonkdl', Marker, queue_size=100)


    # laczenie z modelem
    try:

	    nonkdl_listener()
    except rospy.ROSInterruptException:

            pass
