syms theta1
syms theta2
syms theta3
syms r11;
syms r12;
syms r13;
syms r14;
syms r21;
syms r22;
syms r23;
syms r24;
syms r31;
syms r32;
syms r33;
syms r34;

M1 = [[cos(theta1) -sin(theta1) 0 0];[sin(theta1) cos(theta1) 0 0];[ 0 0 1 1];[0 0 0 1]];


M2= [[cos(theta2) -sin(theta2) 0 1];[0 0 1 0];[-sin(theta2) -cos(theta2) 0 0]; [0 0 0 1]];


M3 = [[cos(theta3) -sin(theta3) 0 0.5];[sin(theta3) cos(theta3) 0 0];[ 0 0 1 0];[0 0 0 1]];


END = M1*M2*M3;

R = [[r11 r12 r13 r14];[r21 r22 r23 r24];[ r31 r32 r33 r34];[0 0 0 1]];


eqn = END == R;
equations = [eqn(1, 4), eqn(2, 4), eqn(3, 4)];
result = solve(equations,[theta1, theta2, theta3]);