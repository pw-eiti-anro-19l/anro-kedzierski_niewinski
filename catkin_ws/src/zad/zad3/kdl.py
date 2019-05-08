import rospy
import yaml
import PyKDL as kdl
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker


def callback(data):
    marker=PoseStamped()
    kdlChain =kdl.Chain()   
    frame = kdl.Frame();
    main_matrix = translation_matrix((0, 0, 0))
    infile = yaml.load(open("./plik.yaml"))
    dh = infile["dh"]
    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotZ), frame.DH(0, 0, dh[0][4] , 0)))
  		
    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotX), frame.DH(dh[1][4], 0, 0, dh[1][2])))
    	
    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotY), frame.DH(dh[2][4], 0, 0, 0)))

    jointPos = kdl.JntArray(kdlChain.getNrOfJoints())
    jointPos[0] = data.position[0] 
    jointPos[1] = data.position[1]
    jointPos[2] = data.position[2]
    
    forvKin = kdl.ChainFkSolverPos_recursive(kdlChain)
    eeFrame = kdl.Frame()
    forvKin.JntToCart(jointPos, eeFrame)



    quaternion = eeFrame.M.GetQuaternion()

    marker.header.frame_id = 'floor'
    marker.header.stamp = rospy.Time.now()


    marker.pose.position.x = eeFrame.p[0]
    marker.pose.position.y = eeFrame.p[1]
    marker.pose.position.z = eeFrame.p[2]

    marker.pose.orientation.x = quaternion[0]
    marker.pose.orientation.y = quaternion[1]
    marker.pose.orientation.z = quaternion[2]
    marker.pose.orientation.w = quaternion[3]
    marker.pose.color(255,0,0)

   
    publisher.publish(marker)

def kdl_listener():
    rospy.init_node('KDL_DKIN', anonymous = False)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':

    t_list = {}

    publisher = rospy.Publisher('kdl', PoseStamped, queue_size=100)

    try:
	    kdl_listener()        
    except rospy.ROSInterruptException:
        pass
