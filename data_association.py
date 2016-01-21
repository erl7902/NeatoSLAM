# Data assocation
# Nearest Neighbor

# lines [0] = a, [1] = b
# landmarks are saved the same way
def data_assoc (lines, landmarks): 
	# Currently just compares a and b values
	# Eventually will take into account euclidean distance
	oldlands = []
	newlands = []
	
	for l in range (0, len(lines)):
		result = findland(l, landmarks)
		if (result):
			oldlands.append(l)
		else:
			newlands.append(l)
			
	new_set = [oldlands, newlands]	 
	return new_set
	
def findland(line, landmarks):
	for j in range (0, landmarks): 
			if( abs( j[0] - l[0] ) < .3):
				if( abs(j[1] - l[1] ) < 2): # should be in cm
					return true
	return false