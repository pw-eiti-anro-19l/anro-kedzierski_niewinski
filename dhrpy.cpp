#include <iostream>
#include <kdl/kdl.hpp>
#include <kdl/tree.hpp>
#include <kdl/chain.hpp>
#include <math.h>
#include <stdlib.h>


using namespace std;

int main(int argc,char *argv[])
{
	KDL::Chain chain;
	double const PI = M_PI;
	int arguments = argc - 1;
	if ( arguments % 3 != 0 )
	{
		std::cout<<"Podaj parametry a alpha d rowna ilosc razy \n";
		return -1;
	}
	int nodes = arguments/3;
	for (int i = 0; i< nodes; i++)
	{
		double zlacze[3], koncowka[3];
		chain.addSegment(KDL::Segment(KDL::Joint(KDL::Joint(KDL::Joint::RotZ)),KDL::Frame::DH(atof(argv[i+1]), atof(argv[i+2]), atof(argv[i+3]), 0.0)));
	}
	
	for (int i = 0; i< nodes; i++)
	{
		double roll, pitch, yaw, x, y, z;
		chain.getSegment(i).getFrameToTip().M.GetRPY(roll, pitch, yaw);
		x = chain.getSegment(i).getFrameToTip().p.x();
		y = chain.getSegment(i).getFrameToTip().p.y();
		z = chain.getSegment(i).getFrameToTip().p.z();
		cout << "Zlacze " << i << " rpy : " << roll << ", " << pitch << ", " << yaw << endl;
		cout << "Zlacze " << i << " xyz : " << x << ", " << y << ", " << z << endl;
	}
		

	return 0;
}
