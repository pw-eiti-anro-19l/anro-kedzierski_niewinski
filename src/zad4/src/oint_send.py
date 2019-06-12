#!/usr/bin/env python

import sys
import rospy
from zad4.srv import *

def client(x,y,z,roll,pitch,yaw,time,type):
    print("Start client from jint_send")
    rospy.wait_for_service('oint')
    try:
        print "1"
        inter = rospy.ServiceProxy('oint',ointsrv)
        print "2"
        resp = inter(x,y,z,roll,pitch,yaw,time,type)
    except rospy.ServiceException,e :
        print("Fail in oint_send in creating try")


if __name__ == '__main__':
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    z = float(sys.argv[3])
    roll = float(sys.argv[4])
    pitch = float(sys.argv[5])
    yaw = float(sys.argv[6])
    time = float(sys.argv[7])
    type = str(sys.argv[8])
    client(x,y,z,roll,pitch,yaw,time,type)