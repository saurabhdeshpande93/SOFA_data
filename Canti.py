import Sofa
import numpy as np

class CantileverBeam(Sofa.PythonScriptController):


	def __init__(self, node, node_name, force,store):
		self.createGraph(node, node_name, force)
		self.node_name = node_name
		self.store = store 
	

	def createGraph(self, rootNode, node_name,force):
		cube = rootNode.createChild(str(node_name))
		cube.createObject('MeshGmshLoader', name="loader", filename="./cantilever.msh" )
		cube.createObject('MeshTopology', name = 'topology', src="@loader")
		self.dofs = cube.createObject('MechanicalObject', name="dofs", template='Vec3d')
		cube.createObject('UniformMass', name = 'mass', totalMass=1)
		cube.createObject('HexahedronFEMForceField',youngModulus="100000",poissonRatio="0.3")
		cube.createObject('BoxROI', box="-0.51 -0.1 0 -0.5 0.1 0.2", position="@topology.position", name="FixedROI", drawBoxes='0')
		cube.createObject('FixedConstraint', indices="@FixedROI.indices")
		self.ff = cube.createObject('ConstantForceField', force= force, indices='1')

		visuNode = cube.createChild('visual')
		visuNode.createObject('OglModel', name='visual')
	  	visuNode.createObject('IdentityMapping')

	def onEndAnimationStep(self, dt):
		#print(self.dofs.position[0][self.node_name])
		print('Example number', self.node_name)
		print(self.dofs.position[0])
		print('And stored values are')
		self.store.append(self.dofs.position[0])
		print(self.store)

		

		

	
		# print(self.ff.force)
		# self.ff.force = self.ff.force + df
		# print(self.ff.force)

		#self.ff.force = self.force.ff + [[0.0, 1.0, 0.0]]
		#print(type(self.ff.force))

	# def onBeginAnimationStep(self, dt):
	# 	pass 
		# df = [[0.0, 1.0, 0.0]]
	
		# print(self.ff.force)
		# self.ff.force = self.ff.force + df
		# print(self.ff.force)


def createScene(rootNode):
	rootNode.createObject('VisualStyle',displayFlags='showVisual showBehavior')
	rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
	rootNode.createObject('RequiredPlugin', name='SofaPython')
	rootNode.createObject('DefaultAnimationLoop')
	rootNode.createObject('DefaultVisualManagerLoop')
	rootNode.gravity = '0 0 0'
	#rootNode.createObject('StaticSolver',name='static_beam', newton_iterations=10)
	rootNode.createObject('EulerImplicitSolver',name='cg_odesolver',printLog='false')
	rootNode.createObject('CGLinearSolver',name='linear solver',iterations=100,tolerance=1.0e-9,threshold=1.0e-9)
	#force = np.linspace(-5,5,3)
	force = [-2,0,2]
	store = []

	for i in range(len(force)):
		print('Position when force value is ' + str(i))
		controller = CantileverBeam(rootNode, i, [0,force[i],0],store)
		# controller.ff.force = [0,i,0]