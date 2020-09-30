import Sofa
import numpy as np
import sys 
import time 
import csv
import pandas as pd 

t1= time.time()

class CantileverBeam(Sofa.PythonScriptController):


	def __init__(self, node, name, node_name, commandLineArguments):
		self.force= [0,float(commandLineArguments[1]),0]
		#self.force = [0.0,5.0,0.0]
		self.node = node
		self.name = name
		self.node_name = node_name
		self.createGraph(self.node, self.node_name, self.force)
	

	def createGraph(self, rootNode, node_name,force):
		cube = rootNode.createChild(node_name)
		cube.createObject('MeshGmshLoader', name="loader", filename="./cantilever.msh" )
		cube.createObject('MeshTopology', name = 'topology', src="@loader")
		self.dofs = cube.createObject('MechanicalObject', name="dofs", template='Vec3d')
		cube.createObject('UniformMass', name = 'mass', totalMass=1)
		cube.createObject('HexahedronFEMForceField',youngModulus="100000",poissonRatio="0.4")
		cube.createObject('BoxROI', box="-0.51 -0.1 0 -0.5 0.1 0.2", position="@topology.position", name="FixedROI", drawBoxes='0')
		cube.createObject('FixedConstraint', indices="@FixedROI.indices")
		self.ff = cube.createObject('ConstantForceField', force= self.force, indices='1')


	def onEndAnimationStep(self, dt):
		#print(self.dofs.position[0][self.node_name])
		#print('Force = ', self.ff.force)
		#print(commandLineArguments)
	
		# self.store.append(self.dofs.position)
		store = np.array(self.dofs.position)
		init_position = np.array(self.dofs.rest_position)

		# if self.node_name == self.n_total -1:
		#print('And the stored values are ')
	
		#print(self.store)
		#print(self.store)
		store = store - init_position #works only when intitial entry is zero
		#print(self.store)
		#print(init_position)

		store = store.reshape(12096,1)
		f_value = np.zeros((store.shape[0],store.shape[1]))
		
		f_value[4] = self.force[1] #same as the input force 

		# for i in range(self.n_total):
		# 	f_value[12096*i] = f[i]

		data=np.hstack((f_value,store))

		df = pd.DataFrame(data, index = None, columns = None) 

		#print(df)

		#for saving underformed
		#np.savetxt("Data/undeformed.csv", init_position, delimiter=",")

		with open('Data/test_topology.csv', 'a') as f:
    			df.to_csv(f, sep = ',', header = False ,index=False)
		
		# with open('Data/SOFA_data_test10.csv','a') as fd:
  #   			fd.write(data)

		#np.savetxt("Data/SOFA_data_test"+ str(int(self.force[1]))+ ".csv", data, delimiter=",")

		sys.exit(0)
	#sys.exit(0)
		# self.node.animate = False



def createScene(rootNode):
	try : 
	    sys.argv[0]
	except :
	    commandLineArguments = []
	else :
	    commandLineArguments = sys.argv
	rootNode.createObject('VisualStyle',displayFlags='showVisual showBehavior')
	rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
	rootNode.createObject('RequiredPlugin', name='SofaPython')
	rootNode.createObject('DefaultAnimationLoop')
	rootNode.createObject('DefaultVisualManagerLoop')
	rootNode.gravity = '0 0 0'
	rootNode.createObject('StaticSolver',name='static_beam',newton_iterations = 50) #correction_tolerance_threshold= 1.0e-9 # newton_iterations=10
	#rootNode.createObject('EulerImplicitSolver',name='cg_odesolver',printLog='false')
	rootNode.createObject('CGLinearSolver',name='linear solver',iterations=100,tolerance=1.0e-9,threshold=1.0e-9)


	t1= time.time()
	controller = CantileverBeam(rootNode, "controller", "Beam", commandLineArguments)

	t2 = time.time()
	
	print("Run time is", t2-t1)
	print(commandLineArguments)
