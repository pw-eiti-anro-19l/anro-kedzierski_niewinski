cmake_minimum_required(VERSION 2.8.3)
project(zad4)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
  std_msgs
  tf
  urdf
  message_generation
)
add_service_files(DIRECTORY srv
  FILES
  jintsrv.srv
  ointsrv.srv
)
generate_messages(
  DEPENDENCIES
  std_msgs
  sensor_msgs
)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES
#  CATKIN_DEPENDS kdl rospy sensor_msgs std_msgs tf
#  DEPENDS system_lib
CATKIN_DEPENDS message_runtime std_msgs sensor_msgs rospy
)


include_directories( include ${catkin_INCLUDE_DIRS} )

