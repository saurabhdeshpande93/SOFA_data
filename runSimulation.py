import os
import subprocess
import numpy as np
import time as time

sofa_dir= "/home/saurabh/Desktop/sofa_files/sofa/v19.06/build/bin/runSofa"

tstart = time.time()

forces = np.linspace(0,10,5)

for force in forces:
	# without UI
	subprocess.call([sofa_dir, "./Simulation_canti.py", "--argv", str(force), "-g", "batch", "start"])

	# with UI
	#subprocess.call([sofa_dir, "./Simulation_canti.py", "--argv", str(force)])



tend = time.time()
total_t = tend - tstart

print("Total run time is",total_t)