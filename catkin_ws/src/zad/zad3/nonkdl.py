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
    infile = yaml.load(open("./plik.yaml"))
    dh = infile["dh"]
    #print(dh)
    #print("\n")
    counter = 0
    for i in dh:
        #print(data)
	
        a = i[1]
        d = i[2]
        al = i[3]
        th = i[4]

        matrix_a = translation_matrix((a, 0, 0))
        matrix_al = rotation_matrix(al, (0, 0, 1))
        matrix_d= translation_matrix((0, 0, -1.57))
        matrix_th = rotation_matrix(th, (0, 0, 1))

        trans = concatenate_matrices(matrix_a, matrix_al, matrix_d, matrix_th)
        t_list[counter] = trans

        counter += 1

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
