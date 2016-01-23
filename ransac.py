import random as ran
from scipy.optimize import curve_fit


# Ransac Algorithm.
# Adapted from 'SLAM for Dummies'
step = 0.017437326 #step from data - ~1 degree per step
N = 5
S = 5 
D = 10
X = 7
C = 4 
#Prereq: degrees must be divisible by the step degree from the laser
#Overwriting this by using indexes instead. D * step = # of degrees away
#def __init__(N1,S1,D1,X1,C1):

	
# Lines.
un_dataa = [0.0, 0.0, 0.0, 1.0, .99, .98, .97, .96, .95, .94, .93, .9, .7, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .1, .4, .7, .2, .9]
un_data1 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
un_data2 = [1.5, 1.3, 1.2, 1.1, 1.6, 1.7, 0.0, 0.0, 0.0, .7, .8, 1.5, 1.5, 1.6, 1.7]

def ransac_go(un_data):
	iter = 0
	extracted = []
	while( (len (un_data) > 0) and ( (len ( un_data)) > C) and (iter < N) ):
		
		#select random reading 
		newread = ran.randint(0, ( len ( un_data)))
		
		#creating a bunch of samples of size S w/in degree D including the new reading.
		#convert from polar to cartesian coordinates. x = laserscan * cos(angle), y = laserscan * sin(angle)
		samplesX = [un_data[newread] * math.cos(newread * step)]
		samplesY = [(un_data[newread]) * math.sin(newread * step)]
		while (len(samples) < S):
			newindex = ran.randint( (index(newread - D )) , (index(newread + D )))
			if (newindex not in samplesX): 
				samplesX.append(un_data[newread] * math.cos(newread * step))
				samplesY.append((un_data[newread]) * math.sin(newread * step))
		
		#Least squares line - linear regression, can change function at will (lambda) 
		#returns slope (A) and intercept (B)
		A, B = 	curve_fit((lambda x, A, B : A*x + B), samplesX, samplesY)[0] 
		
		# need to find which ones are close to the line 
		subsubsetX = []
		subsubsetY = []
		count = 0
		for i in range (0, len(samplesX)):
			x = samplesX[i]
			y = samplesY[i]
			d = sqrt( (( x - ((y - B)/A)) ** 2) + ( ( (A * x + B) - (y) ) ** 2) ) / 2 #already divided by two
			xhyp = abs( (A * x + B) - y )
			ans = sqrt ( (xhyp ** 2) - ( d ** 2))
			
			if ( ans <= X ) : # distance is <= X centimeters from line ("fits" the line)
				subsubsetX.append ( samplesX[i] ) 
				subsubsetY.append ( samplesY[i] )
				count = count + 1
		if ( count > C ): # count is greater than consensus C  
		
			# points for use with line segments
			xlow = min(subsubsetX)
			xhigh = max(subsubsetX)
			ylow = min(subsubsetY)
			yhigh = max(subsubsetY)
			
			# new least squares fit line
			popt, pcov = curve_fit((lambda x, A, B : A*x + B), subsubsetX, subsubsetY)[0]
			# add the line as a line segment tuple. popt[0] = a, popt[1] = b
			# throw out the covariance. 
			extracted.append ( popt ) 
			
			# Remove all of the subsubset from the original data
			for i in range (0 , len ( subsubsetX ) ):
				del un_data[subsubsetX[i]]
			
		# And now we do it all again.	
		iter = iter + 1
	
	return extracted	


print ransac_go(un_dataa)
print ransac_go(un_data1)
print ransac_go(un_data2)	