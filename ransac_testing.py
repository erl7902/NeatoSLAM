import random as ran
from scipy.optimize import curve_fit
import numpy as np
import math


# Ransac Algorithm.
# Adapted from 'SLAM for Dummies'
step = 0.017437326 #step from data - ~1 degree per step
N = 5
S = 5 
D = 5
X = .3
C = 4 
#Prereq: degrees must be divisible by the step degree from the laser
#Overwriting this by using indexes instead. D * step = # of degrees away
#def __init__(N1,S1,D1,X1,C1):

	
# Lines.
un_dataa = [1.0, .99, .98, .97, .96, .95, .94, .93, .9, .7, .1, .15, .4, .8, .2, .9]
un_data1 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
un_data2 = [1.5, 1.3, 1.2, 1.1, 1.6, 1.7, 0.0, 0.0, 0.0, .7, .8, 1.5, 1.5, 1.6, 1.7]


prPoints = []
for i in range(0, len(un_dataa)):
	prPoints.append(((un_dataa[i] * math.cos(i * step)), (un_dataa[i] * math.sin(i * step))))
print prPoints

def ransac_go(un_data):
	iter = 0
	extracted = []
	done = 0
	for i in range (0, len(un_data)):
		un_data[i] = [un_data[i], 0]
		#print(un_data[i])
	
	while((done < len(un_data)) and ( (len(un_data)) > C) and (iter < N) ):
		values = []
		#select random reading 
		newread = ran.randint(0, (len(un_data)))
		while (newread < len(un_data) and un_data[newread][1] > 0):
			newread = ran.randint(0, (len(un_data)))
		#creating a bunch of samples of size S w/in degree D including the new reading.
		#convert from polar to cartesian coordinates. x = laserscan * cos(angle), y = laserscan * sin(angle)
		samplesX = []
		samplesX.append((un_data[newread][0] * math.cos(newread * step)))
		samplesY = []
		samplesY.append((un_data[newread][0]) * math.sin(newread * step))
		while (len(samplesX) < S):
			newindex = ran.randint( (newread - D ) , (newread + D ))
			while(newindex < 0 or newindex >= len(un_data) or (un_data[newindex][1] is 1)):
				newindex = ran.randint( (newread - D ) , (newread + D ))
			if (newindex not in samplesX): 
				samplesX.append(un_data[newindex][0] * math.cos(newread * step))
				samplesY.append((un_data[newindex][0]) * math.sin(newread * step))
		
		#Least squares line - linear regression, can change function at will (lambda) 
		#returns slope (A) and intercept (B)
		def line(x, a, b):
			return a * x + b
		#(lambda x, A, B : A*x + B)
		A,B = curve_fit((lambda x, A, B : A*x + B), samplesX, samplesY)[0]
		# need to find which ones are close to the line 
		subsubsetX = []
		subsubsetY = []
		count = 0
		for i in range (0, len(samplesX)):
			x = samplesX[i]
			y = samplesY[i]
			Ap = (-1/A)
			Bp = (y - A * x)
			
			ama = np.array([[(-1/A - A), 1], [-A, 1]])
			bma = np.array([Bp, B])
			
			xma = np.linalg.solve(ama, bma)
			ans = math.sqrt ( ((x - xma[0])**2) + ((y - xma[1]) ** 2))
			#print ans
			#print (ans <= X)
			
			if ( ans <= X ) : # distance is <= X centimeters from line ("fits" the line)
				values.append(int(math.atan2(samplesY[i], samplesX[i] )))
				subsubsetX.append ( samplesX[i] ) 
				subsubsetY.append ( samplesY[i] )
				count = count + 1
		if ( count > C ): # count is greater than consensus C  
			
			# new least squares fit line
			AA, BB = curve_fit((lambda x, A, B : A*x + B), subsubsetX, subsubsetY)[0]
			# add the line as a line segment tuple. popt[0] = a, popt[1] = b
			# throw out the covariance.
			extracted.append ([AA, BB]) 
			
			# Remove all of the subsubset from the original data
			for i in range (0 , len ( values ) ):
				un_data[values[i]][1] = 1
				done = done + 1
			
		# And now we do it all again.	
		iter = iter + 1
	
	return extracted	


print ransac_go(un_dataa)
#print ransac_go(un_data1)
#print ransac_go(un_data2)	