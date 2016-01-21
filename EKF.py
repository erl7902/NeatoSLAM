import numpy as np

class EKF(X, P):

A = [[1,0,0],[0,1,0],[0,0,1]]
q = [[0,0,0],[0,0,0],[0,0,0]]
X = [0.0, 0.0, 0.0]
c = .97
 
def update_from_odom (x, y, theta):

	deltax = x - X[0]
	deltay = y - X[1]
	deltat = theta - X[2]

	X[0] = X[0] + deltax
	X[1] = X[1] + deltay 
	X[2] = X[2] + deltat

	newA = A
	newA[1][3] = (-deltay)
	newA[2][3] = deltax

	q = [[c * deltax ** 2, c * deltax * deltay, c * deltax * deltat], 
	[c * deltay * deltax, c * deltay ** 2, c * deltay * deltat], c * deltax * deltat, c * deltat * deltay, c * deltat ** 2]
	
	newA = np.dot(np.dot(newA, A), newA)
	A = newA
	#update_from_reobserved(A, q)

#input: list of landmarks reobserved
#output: new X based on kalman gain
def update_from_reobserved(old_lan):

#TODO: V and R
range_bearings = []

for i in range 0, len(old_lan):
	range_bearings.append([math.sqrt((old_lan[i][0] - X[0]) ** 2 + (old_lan[i][1] - X[1]))],[math.atan(old_lan[i][0] - X[0], old_lan[i][1] - X[1])])
	#TODO: Jacobian H 
	H = [ ]
	#TODO: Matrix math
	K = P * transpose(H) * ((H * P * transpose(H) + V * R * transpose(V)) ** -1)	
	X = X + K (z - h) 
	
return X 

def add_new_landmarks(new_lan):  