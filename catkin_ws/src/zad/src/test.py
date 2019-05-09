import PyKDL

# frame
f = PyKDL.Frame(PyKDL.Rotation.RPY(0,1,0),
                PyKDL.Vector(3,2,4))

# get the origin (a Vector) of the frame
origin = f.p

# get the x component of the origin
x = origin.x()
x = origin[0]

# get the rotation of the frame
rot = f.M

# get ZYX Euler angles from the rotation
[Rz, Ry, Rx] = rot.GetEulerZYX()

# get the RPY (fixed axis) from the rotation
[R, P, Y] = rot.GetRPY()


