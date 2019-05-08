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
    print(dh)
    print("\n")
    counter = 0
    for i in dh:
        print(data)
	
        a = i[0]
        d = i[1]
        al = i[2]
        th = i[3]

        matrix_a = translation_matrix((a, 0, 0))
        matrix_al = rotation_matrix(al, (1, 0, 0))
        matrix_d= translation_matrix((0, 0, d*(1+data.position[counter])))
        matrix_th = rotation_matrix(th, (0, 0, 1))

        trans = concatenate_matrices(matrix_a, matrix_al, matrix_d, matrix_th)
        t_list[counter] = trans

        counter += 1

    main_matrix = concatenate_matrices(t_list[0], t_list[1], t_list[2])

    x, y, z = translation_from_matrix(main_matrix)


    
    xq, yq, zq, wq = quaternion_from_matrix(main_matrix)

        
    marker.type = marker.SPHERE
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
    marker.color.b = 0.0;
    marker.color.a = 1.0;

   
    publisher.publish(marker)

def nonkdl_listener():
    rospy.init_node('NONKDL_DKIN', anonymous = False)
    # publisher = rospy.Publisher('n_k_axes', PoseStamped, queue_size=10)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':
    t_list = {}
    publisher = rospy.Publisher('n_k_axes', Marker, queue_size=100)

    print("Hello ")
    # laczenie z modelem
    try:
            print("try") 
	    nonkdl_listener()
    except rospy.ROSInterruptException:

            pass
