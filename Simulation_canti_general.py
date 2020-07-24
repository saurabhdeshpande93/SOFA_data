import Sofa
import numpy as np
import sys 
import time 
import random
import pandas as pd 

t1= time.time()

class CantileverBeam(Sofa.PythonScriptController):


	def __init__(self, node, name, node_name, commandLineArguments):
		#self.force= [float(commandLineArguments[1]),float(commandLineArguments[2]),float(commandLineArguments[3])]
		self.force = [np.random.uniform(-5,5),np.random.uniform(-5,10),np.random.uniform(-5,5)]
		self.node = node
		self.name = name
		self.node_name = node_name
		self.createGraph(self.node, self.node_name, self.force)
		#self.number = np
	

	def createGraph(self, rootNode, node_name,force):
		cube = rootNode.createChild(node_name)
		cube.createObject('MeshGmshLoader', name="loader", filename="./cantilever.msh" )
		cube.createObject('MeshTopology', name = 'topology', src="@loader")
		self.dofs = cube.createObject('MechanicalObject', name="dofs", template='Vec3d')
		cube.createObject('UniformMass', name = 'mass', totalMass=1)
		cube.createObject('HexahedronFEMForceField',youngModulus="100000",poissonRatio="0.4")
		self.roi = cube.createObject('BoxROI', box="-0.51 -0.1 0 -0.5 0.1 0.2", position="@topology.position", name="FixedROI", drawBoxes='0')
		cube.createObject('FixedConstraint', indices="@FixedROI.indices")
		self.ff = cube.createObject('ConstantForceField', force= self.force, indices= random.choice([0,1,4,5,70,71,72,73,74,75,76,79,80,81,82,83,84,85,86,87,88]))

	def onEndAnimationStep(self, dt):
		#print(self.dofs.position[0][self.node_name])
		# print('Force = ', self.ff.force)
		# print('index is ', self.ff.indices[0][0])
		#print(self.roi.indices)
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
		
		force_node = self.ff.indices[0][0]
		f_value[3*force_node] = self.force[0] #Force applied on first index 
		f_value[3*force_node+1] = self.force[1]
		f_value[3*force_node+2] = self.force[2]

		data=np.hstack((f_value,store))

		df = pd.DataFrame(data, index = None, columns = None) 

		#print(df)

		#for saving underformed
		#np.savetxt("Data/undeformed.csv", init_position, delimiter=",")

		with open('Data/data_10000_generic.csv', 'a') as f:
    			df.to_csv(f, sep = ',', header = False ,index=False)
		

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
	rootNode.createObject('StaticSolver',name='static_beam',newton_iterations = 30) #correction_tolerance_threshold= 1.0e-9 # newton_iterations=10
	#rootNode.createObject('EulerImplicitSolver',name='cg_odesolver',printLog='false')
	rootNode.createObject('CGLinearSolver',name='linear solver',iterations=100,tolerance=1.0e-9,threshold=1.0e-9)


	controller = CantileverBeam(rootNode, "controller", "Beam", commandLineArguments)
	
	# print("Run time is", t2-t1)
	# print(commandLineArguments)
