import Sofa
import numpy as np

class CantileverBeam(Sofa.PythonScriptController):


	def __init__(self, node, node_name, force,store):
		self.createGraph(node, node_name, force)
		self.node_name = node_name
		self.store = store
		self.force = force  
	

	def createGraph(self, rootNode, node_name,force):
		cube = rootNode.createChild(str(node_name))
		cube.createObject('MeshGmshLoader', name="loader", filename="./cantilever.msh" )
		cube.createObject('MeshTopology', name = 'topology', src="@loader")
		self.dofs = cube.createObject('MechanicalObject', name="dofs", template='Vec3d')
		cube.createObject('UniformMass', name = 'mass', totalMass=1)
		cube.createObject('HexahedronFEMForceField',youngModulus="100000",poissonRatio="0.4")
		cube.createObject('BoxROI', box="-0.51 -0.1 0 -0.5 0.1 0.2", position="@topology.position", name="FixedROI", drawBoxes='0')
		cube.createObject('FixedConstraint', indices="@FixedROI.indices")
		self.ff = cube.createObject('ConstantForceField', force= force, indices='1')

		visuNode = cube.createChild('visual')
		visuNode.createObject('OglModel', name='visual')
	  	visuNode.createObject('IdentityMapping')

	def onEndAnimationStep(self, dt):
		#print(self.dofs.position[0][self.node_name])
		print('Example number', self.node_name)
		#print(self.dofs.position[0])
	
		self.store.append(self.dofs.position)
		self.store = np.array(self.store)

		n_total = len(self.force)
		print(n_total)
		
		if self.node_name == n_total -1:
			print('And the stored values are ')
			print(self.store)
			print( self.store.shape)
			self.store = self.store.reshape(n_total*12096,1)
			f_value = np.zeros((self.store.shape[0],self.store.shape[1]))
			
			f = np.linspace(0,10,3) #same as the input force 

			for i in range(n_total):
				f_value[12096*i] = f[i]

			# data=np.hstack((f_value,self.store))
			# np.savetxt("SOFA_data.csv", data, delimiter=",")



def createScene(rootNode):
	rootNode.createObject('VisualStyle',displayFlags='showVisual showBehavior')
	rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
	rootNode.createObject('RequiredPlugin', name='SofaPython')
	rootNode.createObject('DefaultAnimationLoop')
	rootNode.createObject('DefaultVisualManagerLoop')
	rootNode.gravity = '0 0 0'
	rootNode.createObject('StaticSolver',name='static_beam', newton_iterations=20)
	#rootNode.createObject('EulerImplicitSolver',name='cg_odesolver',printLog='false')
	rootNode.createObject('CGLinearSolver',name='linear solver',iterations=100,tolerance=1.0e-9,threshold=1.0e-9)
	force = np.linspace(0,10,3) #same above
	#force = [-5,5,5]
	store = []

	for i in range(len(force)):
		print('Position when force value is ' + str(i))
		controller = CantileverBeam(rootNode, i, [0,force[i],0],store)


		# controller.ff.force = [0,i,0]


