import random as ran
from scipy.optimize import curve_fit

# Ransac Algorithm.
# Adapted from 'SLAM for Dummies'

N, S, D, X, C
#Prereq: D must be divisible by the step degree from the laser
def __init__(N1,S1,D1,X1,C1):
	N = N1
	S = S1
	D = D1
	X = X1
	C = C1

	
# Corners - find that minima, see if they look like two intersecting ransac lines	

def ransac_go (un_data):
	iter = 0
	extracted = []
	while( (len (un_data) > 0) and ( (len ( un_data)) > C) and (iter < N) ):
		#select random reading 
		newread = ran.randint(0, ( len ( un_data)))
		#creating a bunch of samples of size S including the new reading.
		samplesX = [newread]
		samplesY = [(un_data[newread])]
		while (len(samples) < S):
			newindex = ran.randint( (index(newread - degree )) , (index(newread + degree )))
			if (newindex not in samplesX): 
				samplesX.append( newindex )
				samplesY.append(un_data[newindex])
		
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
		if ( count > C ) # count is greater than consensus C 
			# new least squares fit line 
			C, D = 	curve_fit((lambda x, A, B : A*x + B), subsubsetX, subsubsetY)[0] 
			extracted.append ( (C, D) ) # add the line as a tuple
			
			# Remove all of the subsubset from the original data
			for i in range (0 , len ( subsubsetX ) ):
				del un_data[subsubsetX[i]]
			
		# And now we do it all again.	
		iter = iter + 1
		
	return extracted		