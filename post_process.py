import Sofa
import numpy as np
import sys 
import time 
import csv
import pandas as pd 

t1= time.time()

class CantileverBeam(Sofa.PythonScriptController):


	def __init__(self, node, name, node_name, commandLineArguments):
		#self.force= [0,float(commandLineArguments[1]),0]
		self.force = [0.016035990091154, 0.043855726653413, 0.0]
		self.node = node
		self.name = name
		self.node_name = node_name
		self.createGraph(self.node, self.node_name, self.force)

	

	def bwdInitGraph(self,node):
		print("bwdinit")
		init_position = np.array(self.dofs.rest_position)
		print(init_position)
		init_position = init_position.reshape(12096,)


		#Input the external deformation matrix 

		df = pd.read_csv('Data/single_pred_topface.csv', names=['f', 'u','a'], header = None) #'a' stands for actual sofa data in the csv file
		deforms = df['u'].values

		print(deforms)

		new_position = init_position + deforms

		new_position = new_position.reshape(4032,3)

		print(new_position)


		#From SOFA 
		new_position_SOFA = np.array(self.dofs.position)
		new_position_SOFA = new_position_SOFA.reshape(12096,)


		#Crosscheck if difference is zero

		self.nn_node = self.cube.createChild('nn_node')
		self.nn_topology = self.nn_node.createObject('MeshTopology', name = 'topology_nn', position = new_position.tolist(), quads ='@../topology.quads' )
		# self.nn_node.createObject('MechanicalObject', template = "Vec3d", name = "dofs", position = "@topology_nn.position")

		visuNode = self.nn_node.createChild('visu')
		visuNode.createObject('OglModel', name='visual', position = "@topology_nn.position", quads = "@topology_nn.quads")
		visuNode.createObject('VisualStyle',displayFlags='showWireframe')
		#visuNode.createObject('IdentityMapping')

		####Visualise SOFA solution which is stored in the csv file #####################3

		position_sofa = df['a'].values
		position_sofa = position_sofa + init_position
		position_sofa = position_sofa.reshape(4032,3)

		self.sofa_node = self.cube.createChild('sofa_node')
		self.sofa_topology = self.sofa_node.createObject('MeshTopology', name = 'topology_sofa', position = position_sofa.tolist(), quads ='@../topology.quads' )
		# self.nn_node.createObject('MechanicalObject', template = "Vec3d", name = "dofs", position = "@topology_nn.position")

		visuNode = self.sofa_node.createChild('visu_sofa')
		visuNode.createObject('OglModel', name='visual', position = "@topology_sofa.position", quads = "@topology_sofa.quads")
		visuNode.createObject('VisualStyle',displayFlags='showWireframe')

		# df_step = pd.read_csv('Data/first_step.csv', names=['f', 'u'], header = None) 
		# step_one = df['u'].values

		# self.step_node = self.cube.createChild('step_node')
		# self.step_topology = self.nn_node.createObject('MeshTopology', name = 'topology_nn', position = step_one.tolist(), quads ='@../topology.quads' )
		# # self.nn_node.createObject('MechanicalObject', template = "Vec3d", name = "dofs", position = "@topology_nn.position")

		# visuNode = self.nn_node.createChild('visu')
		# visuNode.createObject('OglModel', name='visual', position = "@topology_nn.position", quads = "@topology_nn.quads")
		# #visuNode.createObject('IdentityMapping')



	def createGraph(self, rootNode, node_name,force):
		self.cube = rootNode.createChild(node_name)
		self.cube.createObject('MeshGmshLoader', name="loader", filename="./cantilever_4m.msh" )
		self.cube.createObject('MeshTopology', name = 'topology', src="@loader")
		self.dofs = self.cube.createObject('MechanicalObject', name="dofs", template='Vec3d')
		self.cube.createObject('UniformMass', name = 'mass', totalMass=1)
		self.cube.createObject('HexahedronFEMForceField',youngModulus="1000",poissonRatio="0.3")
		self.cube.createObject('BoxROI', box="-0.51 -0.1 0 -0.5 0.1 0.2", position="@topology.position", name="FixedROI", drawBoxes='0')
		self.cube.createObject('FixedConstraint', indices="@FixedROI.indices")
		self.ff = self.cube.createObject('ConstantForceField', force= self.force, indices='74')

		#self.nn_position = cube.createObject('MeshTopology', name = 'topology', src="@loader")
		
	def onEndAnimationStep(self, dt):
		
		displacement = np.array(self.dofs.position)-np.array(self.dofs.rest_position)
		print(displacement)
		#print('Force = ', self.ff.force)
		#print(commandLineArguments)
		pass

		# first_step = np.array(self.dofs.position)
		# np.savetxt("Data/first_step.csv",first_step,delimiter=",")


	
		# init_position = np.array(self.dofs.rest_position)

		# if self.node_name == self.n_total -1:
		#print('And the stored values are ')
	
		#print(self.store)
		#print(self.store)
		# store = store - init_position #works only when intitial entry is zero
		# #print(self.store)
		# #print(init_position)

		# store = store.reshape(12096,1)
		# f_value = np.zeros((store.shape[0],store.shape[1]))
		
		# f_value[4] = self.force[1] #same as the input force 

		# # for i in range(self.n_total):
		# # 	f_value[12096*i] = f[i]

		# data=np.hstack((f_value,store))

		# df = pd.DataFrame(data, index = None, columns = None) 

		#print(df)

		#for saving underformed
		#np.savetxt("Data/undeformed.csv", init_position, delimiter=",")

		# with open('Data/test_topology.csv', 'a') as f:
  #   			df.to_csv(f, sep = ',', header = False ,index=False)
		
		# with open('Data/SOFA_data_test10.csv','a') as fd:
  #   			fd.write(data)

		#np.savetxt("Data/SOFA_data_test"+ str(int(self.force[1]))+ ".csv", data, delimiter=",")

		#sys.exit(0)
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
	rootNode.createObject('BackgroundSetting',color='1 1 1')
	rootNode.createObject('StaticSolver',name='static_beam',newton_iterations = 30) #correction_tolerance_threshold= 1.0e-9 # newton_iterations=10
	#rootNode.createObject('EulerImplicitSolver',name='cg_odesolver',printLog='false')
	rootNode.createObject('CGLinearSolver',name='linear solver',iterations=100,tolerance=1.0e-9,threshold=1.0e-9)


	t1= time.time()
	controller = CantileverBeam(rootNode, "controller", "Beam", commandLineArguments)

	t2 = time.time()
	
	print("Run time is", t2-t1)
	print(commandLineArguments)
