# program-QOSP-
This is the program for the admission of QOSP 


The program using the relation:
RX(theta) = Cos(theta/2)*Id -iSin(theta/2)*X
RY(theta) = Cos(theta/2)*Id -iSin(theta/2)*Y
RZ(theta) = Cos(theta/2)*Id -iSin(theta/2)*Z
And HZH = X

So to decompose some specific gate like Cx, the depth of the circuit increase dramatically.

To reduce the depth of the circuit, for each rotation gate in the same axes, we can apply the relation Ru(theta1)*Ru(theta2) = Ru(theta1+theta2) (not yet program)

