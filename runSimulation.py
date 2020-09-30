import os
import subprocess
import numpy as np
import time as time
import pandas as pd 

# sofa_dir= "/home/saurabh/Desktop/sofa_files/sofa/v19.06/build/bin/runSofa"

# tstart = time.time()

# forces = np.linspace(0,10,5000)

# for force in forces:
# 	# without UI
# 	subprocess.call([sofa_dir, "./Simulation_canti.py", "--argv", str(force),, "-g", "batch", "start"])

# 	# with UI
# 	#subprocess.call([sofa_dir, "./Simulation_canti.py", "--argv", str(force)])



# tend = time.time()
# total_t = tend - tstart

# print("Total run time is",total_t)


########################## For all the directions ##############################3


#Or we can generate forces in random directions 

df = pd.read_csv('qt_nodes.csv', names=['u'], header = None)
topnodes= df['u'].values

#Let's convert all elements of array to integers to be given as force indices 
topnodes = [ int(x) for x in topnodes]
#print(topnodes)
#print("Length of array is", len(topnodes))
#number of training example generated at a particular node 
m = 450

#Index on which forces are applied on this node numbers 
index = topnodes

#index = np.array([0,1,70,71,72,73,74,75,76,77,78,79])



sofa_dir= "/home/saurabh/Desktop/sofa_files/sofa/v19.06/build/bin/runSofa"

tstart = time.time()


for i in range(m):
	 #force[i,:]
	#print('You are at example number ', m)

	for j in index:
		# without UI
		subprocess.call([sofa_dir, "./Simulation_canti_general.py", "--argv", str(j), "-g", "batch", "start"])

		# with UI
		#subprocess.call([sofa_dir, "./Simulation_canti_general.py", "--argv", str(j)])



	

tend = time.time()
total_t = tend - tstart

print("Total run time is",total_t)



##This way we can give forces in specific directions 


# magnitude = np.linspace(-5,5,4)
# f_len = len(magnitude)

# m = 3*len(magnitude) #Number of training examples 

# force = np.zeros((m,3))

# for i in range(m):
# 	if (i < m/3):
# 		print(i)
# 		force[i,:] = [float(magnitude[i]),0.0,0.0]
# 	elif ((m/3)<=i<(2*m)/3):
# 		force[i,:] = [0.0,float(magnitude[i-f_len]),0.0]
# 	else:
# 		force[i,:] = [0.0,0.0,float(magnitude[i-2*f_len])]

# print(force)


###To truncate number to particular decimal point
# def truncate(f, n):
#     '''Truncates/pads a float f to n decimal places without rounding'''
#     s = '{}'.format(f)
#     if 'e' in s or 'E' in s:
#         return '{0:.{1}f}'.format(f, n)
#     i, p, d = s.partition('.')
#     return '.'.join([i, (d+'0'*n)[:n]])


# for i in range(m):
# 	# f_x = truncate(np.random.uniform(-5,0),3)
# 	# f_y = truncate(np.random.uniform(-5,5),3)
# 	# f_z = truncate(np.random.uniform(-5,0),3)	
	
# 	# force[i,:] = [f_x,f_y,f_z]
# 	force[i,:] = [np.random.uniform(-4,4),np.random.uniform(0,10),np.random.uniform(0,3)]
