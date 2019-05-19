#!/usr/bin/env python

from zad4.srv import *
import rospy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import *
from std_msgs.msg import Header
from tf.transformations import quaternion_from_euler


class Interpolator:

    def __init__(self):
        self.maxit = 0
        self.t = 0
        self.a3 = 0.0
        self.a2 = 0.0
        self.a1 = 0.0
        self. a0 = 0.0

    def linear_init(self,x0,x1,maxit):
        x0 = float(x0)
        x1 = float(x1)
        self.a3 = 0
        self.a2 = 0
        self.a1 = (x1-x0)/maxit
        self.a0 = x0

    def spline_init(self,x0,x1,maxit):
        x0 = float(x0)
        x1 = float(x1)

        self.a3 = (2*(float(x0)-float(x1)))/maxit**3
        self.a2 = -(3*(x0 - x1))/maxit**2
        self.a1 = 0
        self.a0 = x0

    def interpolation(self,it):
        return self.a3 * it**3 + it**2 * self.a2 + it*self.a1 + self.a0


hz = 10.0

def res(data):
    print "hello"
    if data.time <= 0:
        print ("Czas nie moze byc mniejszy od zera ani 1/%d sekundy" % hz)
        return -1
    xz = 0
    yz = 0
    zz = 0
    rollz = 0
    pitchz = 0
    yawz = 0
    xf = float(data.x)
    yf = float(data.y)
    zf = float(data.z)
    rollf = float(data.roll)
    pitchf = float(data.pitch)
    yawf = float(data.yaw)
    interpolatorx = Interpolator()
    interpolatory = Interpolator()
    interpolatorz = Interpolator()
    interpolatorroll = Interpolator()
    interpolatorpitch = Interpolator()
    interpolatoryaw = Interpolator()
    if data.type == "lin":
        print "Liniowa interpolacja"
        interpolatorx.linear_init(xz,xf,float(data.time)*hz)
        interpolatory.linear_init(yz, yf, float(data.time) * hz)
        interpolatorz.linear_init(zz, zf, float(data.time) * hz)
        interpolatorroll.linear_init(rollz, rollf, float(data.time) * hz)
        interpolatorpitch.linear_init(pitchz, pitchf, float(data.time) * hz)
        interpolatoryaw.linear_init(yawz, yawf, float(data.time) * hz)
    else:
        print "Interpolacja wielomianem 3 stopnia"
        interpolatorx.spline_init(xz, xf, float(data.time) * hz)
        interpolatory.spline_init(yz, yf, float(data.time) * hz)
        interpolatorz.spline_init(zz, zf, float(data.time) * hz)
        interpolatorroll.spline_init(rollz, rollf, float(data.time) * hz)
        interpolatorpitch.spline_init(pitchz, pitchf, float(data.time) * hz)
        interpolatoryaw.spline_init(yawz, yawf, float(data.time) * hz)
    rate = rospy.Rate(hz)
    maxit = hz * data.time
    for k in range(0, int(maxit)):
        newPoseStamped = PoseStamped()
        newPoseStamped.header = Header()
        newPoseStamped.header.frame_id = 'floor'
        newPoseStamped.header.stamp = rospy.Time.now()
        newPoseStamped.pose = Pose()
        newPoseStamped.pose.position.x = interpolatorx.interpolation(k)
        newPoseStamped.pose.position.y = interpolatory.interpolation(k)
        newPoseStamped.pose.position.z = interpolatorz.interpolation(k)
        roll = interpolatorroll.interpolation(k)
        pitch = interpolatorpitch.interpolation(k)
        yaw = interpolatoryaw.interpolation(k)
        q = quaternion_from_euler(roll,pitch,yaw)
        newPoseStamped.pose.orientation.x = q[0]
        newPoseStamped.pose.orientation.y = q[1]
        newPoseStamped.pose.orientation.z = q[2]
        newPoseStamped.pose.orientation.w = q[3]
        global pub
        pub.publish(newPoseStamped)
        print k
        rate.sleep()


if __name__ == '__main__':
    print "Hello"
    node = rospy.init_node('oint_node')
    pub = rospy.Publisher('/pose_stamped_publisher',PoseStamped,queue_size=10)
    newPoseStamped = PoseStamped()
    newPoseStamped.header = Header()
    newPoseStamped.header.frame_id = 'floor'
    newPoseStamped.header.stamp = rospy.Time.now()
    newPoseStamped.pose = Pose()
    newPoseStamped.pose.position.x = 0
    newPoseStamped.pose.position.y = 0
    newPoseStamped.pose.position.z = 0
    newPoseStamped.pose.orientation.x = 0
    newPoseStamped.pose.orientation.y = 0
    newPoseStamped.pose.orientation.z = 0
    newPoseStamped.pose.orientation.w = 0
    pub.publish(newPoseStamped)
    service = rospy.Service('oint',ointsrv,res)
    rospy.spin()