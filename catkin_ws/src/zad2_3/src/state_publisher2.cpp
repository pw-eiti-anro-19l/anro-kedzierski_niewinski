
#include <string>
#include <ros/ros.h>
#include <sensor_msgs/JointState.h>
#include <tf/transform_broadcaster.h>

int main(int argc, char** argv) {
    ros::init(argc, argv, "state_publisher");
    ros::NodeHandle n;
    ros::Publisher joint_pub = n.advertise<sensor_msgs::JointState>("joint_states", 1);
    tf::TransformBroadcaster broadcaster;
    ros::Rate loop_rate(360);

   	const double degree = M_PI/180;
	double angle=0, theta1=0,theta2=0,theta3=0, a2=0.5;
    // message declarations
   

    while (ros::ok()) {
       //update joint_state
	tf::Quaternion myq;
	ros::param::get("theta1",theta1);
	ros::param::get("theta2",theta2);
	ros::param::get("theta3",theta3);
	ros::param::get("a2",a2);
	//floor->link1
	geometry_msgs::TransformStamped odom1;
    	sensor_msgs::JointState joint1;
    	odom1.header.frame_id = "floor";
    	odom1.child_frame_id = "link1";
        joint1.header.stamp = ros::Time::now();
	//sterowanie
	myq.setRPY(0 ,0,theta1); //theta 1
	geometry_msgs::Quaternion msg;
	tf::quaternionTFToMsg(myq,msg);
	odom1.transform.translation.x = 0;
        odom1.transform.translation.y = 0;
        odom1.transform.translation.z = 0;
	odom1.transform.rotation=msg;
        odom1.header.stamp = ros::Time::now();
        //send the joint state and transform
        joint_pub.publish(joint1);
        broadcaster.sendTransform(odom1);
	
	//link1->link2
	geometry_msgs::TransformStamped odom2;
    	sensor_msgs::JointState joint2;
    	odom2.header.frame_id = "link1";
    	odom2.child_frame_id = "link2";
        joint2.header.stamp = ros::Time::now();
	//sterowanie
	myq.setRPY(-1.57+theta2, 0 ,0); //theta 2
	tf::quaternionTFToMsg(myq,msg);
	odom2.transform.rotation=msg;
	odom2.transform.translation.x = 0;
        odom2.transform.translation.y = 0.5;
        odom2.transform.translation.z = 0.5;
        odom2.header.stamp = ros::Time::now();
        //send the joint state and transform
        joint_pub.publish(joint2);
        broadcaster.sendTransform(odom2);
	
	//link2->link3
	geometry_msgs::TransformStamped odom3;
    	sensor_msgs::JointState joint3;
    	odom3.header.frame_id = "link2";
    	odom3.child_frame_id = "link3";
	myq.setRPY(theta3,0, 0); //theta 3
	tf::quaternionTFToMsg(myq,msg);
	odom3.transform.rotation=msg;
	odom3.transform.translation.x = 0;
        odom3.transform.translation.y = 0;
        odom3.transform.translation.z = a2; //zamienic na a2
        joint3.header.stamp = ros::Time::now();
	//sterowanie
	//odom3.transform.rotation=msg;
        odom3.header.stamp = ros::Time::now();
        //send the joint state and transform
        joint_pub.publish(joint3);
        broadcaster.sendTransform(odom3);



        // This will adjust as needed per iteration
      loop_rate.sleep();
    }


    return 0;
}

