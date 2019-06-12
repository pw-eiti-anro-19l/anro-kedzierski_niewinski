#!/usr/bin/env python

from zad4.srv import *
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header


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
    j1z = 0.0
    j2z = 0.0
    j3z = 0.0
    j1f = float(data.j1)
    j2f = float(data.j2)
    j3f = float(data.j3)
    interpolator1 = Interpolator()
    interpolator2 = Interpolator()
    interpolator3 = Interpolator()
    if data.interpolation == 'lin':
        interpolator1.linear_init(j1z,j1f,hz*float(data.time))
        interpolator2.linear_init(j2z, j2f, hz*float(data.time))
        interpolator3.linear_init(j3z, j3f, hz*float(data.time))
    else:
        interpolator1.spline_init(j1z, j1f, hz*float(data.time))
        interpolator2.spline_init(j2z, j2f, hz*float(data.time))
        interpolator3.spline_init(j3z, j3f, hz*float(data.time))
    rate = rospy.Rate(hz)
    maxit = hz * data.time

    for k in range(0,int(maxit)):
        newJointState = JointState()
        newJointState.header = Header()
        newJointState.header.stamp = rospy.Time.now()
        newJointState.header.frame_id = 'floor'
        newJointState.name=['joint1','joint2','joint3']
        j1 = interpolator1.interpolation(k)
        j2 = interpolator2.interpolation(k)
        j3 = interpolator3.interpolation(k)
        newJointState.position = [j1,j2,j3]
        global pub
        print newJointState.position
        pub.publish(newJointState)
        print k
        rate.sleep()
    global service

if __name__ == '__main__':
    print "Hello"
    node = rospy.init_node('jint_node')
    pub = rospy.Publisher('/joint_states',JointState,queue_size=10)
    service = rospy.Service('jint',jintsrv,res)
    newJointState = JointState()
    newJointState.header = Header()
    newJointState.header.frame_id = 'floor'
    newJointState.header.stamp = rospy.Time.now()
    newJointState.name = ['joint1', 'joint2', 'joint3']
    pub.publish(newJointState)
    rospy.spin()