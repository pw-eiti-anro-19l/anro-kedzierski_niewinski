#!/usr/bin/env python

import sys
import rospy
from zad4.srv import *

def client(j1,j2,j3,time,type):
    print("Start client from jint_send")
    rospy.wait_for_service('jint')
    try:
        print "1"
        inter = rospy.ServiceProxy('jint',jintsrv)
        print "2"
        resp = inter(j1,j2,j3,time,type)
    except rospy.ServiceException,e :
        print("Fail in jint_send in creating try")


if __name__ == '__main__':
    j1 = float(sys.argv[1])
    j2 = float(sys.argv[2])
    j3 = float(sys.argv[3])
    time = float(sys.argv[4])
    type = str(sys.argv[5])
    client(j1,j2,j3,time,type)