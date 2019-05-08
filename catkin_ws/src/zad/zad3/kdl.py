import rospy
import yaml
import PyKDL as kdl
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker


def callback(data):
    marker=Marker()
    kdlChain =kdl.Chain()   
    frame = kdl.Frame();
    main_matrix = translation_matrix((0, 0, 0))
    infile = yaml.load(open("./plik.yaml"))
    dh = infile["dh"]
    print(dh)
    print("\n")
    d=0
    th=0
    counter = 0
    for i in dh:
        #print(data)

        last_d = d
        last_th = th
        a = i[0]
        d = i[1]
        al = i[2]
        th = i[3]

        if counter!= 0:
        	kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), frame.DH(a - 0.5, al, d - 0.5, th)))

        counter += 1
    		
    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), frame.DH(0, 0, d, th)))
    	

    jointPos = kdl.JntArray(kdlChain.getNrOfJoints())
    jointPos[0] = data.position[0] 
    jointPos[1] = data.position[1]
    jointPos[2] = data.position[2]
    
    forvKin = kdl.ChainFkSolverPos_recursive(kdlChain)
    eeFrame = kdl.Frame() # <--polaczyc eeFrame z reszta robota
    forvKin.JntToCart(jointPos, eeFrame)
    print(eeFrame)



    quaternion = eeFrame.M.GetQuaternion()

    
    marker.header.frame_id = "/map"

    marker.type = marker.POINTS
    marker.action = marker.ADD
    marker.pose.orientation.w = 1


    ti = rospy.Duration()
    marker.lifetime = ti
    marker.scale.x = 0.4
    marker.scale.y = 0.4
    marker.scale.z = 0.4
    marker.color.a = 1.0
    marker.color.r = 1.0

   
    publisher.publish(marker)

def kdl_listener():
    rospy.init_node('KDL_DKIN', anonymous = False)
    # publisher = rospy.Publisher('n_k_axes', PoseStamped, queue_size=10)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':

    t_list = {}

    publisher = rospy.Publisher('xD', Marker, queue_size=100)
    
 
    
    # laczenie z modelem
    try:
	    kdl_listener()        
    except rospy.ROSInterruptException:
        pass
