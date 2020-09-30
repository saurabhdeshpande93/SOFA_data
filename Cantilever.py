import Sofa
import numpy as np

class CantileverBeam(Sofa.PythonScriptController):
	def __init__(self, node, node_name, force):
		self.createGraph(node, node_name, force)

	def createGraph(self, rootNode, node_name,force):
		cube = rootNode.createChild(str(node_name))
		cube.createObject('MeshGmshLoader', name="loader", filename="./cantilever_4m.msh" )
		cube.createObject('MeshTopology', name = 'topology', src="@loader")
		self.dofs = cube.createObject('MechanicalObject', name="dofs", template='Vec3d')
		cube.createObject('UniformMass', name = 'mass', totalMass=1)
		cube.createObject('HexahedronFEMForceField',youngModulus="500",poissonRatio="0.4")
		cube.createObject('BoxROI', box="-2.1 -0.5 0 -1.99 0.5 1", position="@topology.position", name="FixedROI", drawBoxes='1')
		self.topROI = cube.createObject('BoxROI', box=" 1.0 0.49 0.01 1.99 0.51 0.99", position="@topology.position", name="topROI", drawBoxes='1')
		cube.createObject('FixedConstraint', indices="@FixedROI.indices")
		self.ff = cube.createObject('ConstantForceField', force= force, indices='1015')



		visuNode = cube.createChild('visual')
		visuNode.createObject('OglModel', name='visual')
	  	visuNode.createObject('IdentityMapping')

	def onEndAnimationStep(self, dt):
		print(self.topROI.indices)
		qtnodes = np.array(self.topROI.indices)
		qtnodes = [ int(x) for x in qtnodes]
		np.savetxt("qt_nodes.csv", qtnodes)

		#print(self.ff.ConstantForceField)

	# def onBeginAnimationStep(self, dt):
	# 	df = np.array([[1,0,0]])
	
	# 	print(self.ff.force[0])
	# 	self.ff.force = np.add(self.ff.force,df)  
	# 	print(self.ff.force[0])


def createScene(rootNode):
	rootNode.createObject('VisualStyle',displayFlags='showVisual showBehavior')
	rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
	rootNode.createObject('RequiredPlugin', name='SofaPython')
	rootNode.createObject('DefaultAnimationLoop')
	rootNode.createObject('DefaultVisualManagerLoop')
	rootNode.gravity = '0 0 0'
	rootNode.createObject('StaticSolver',name='static_beam', newton_iterations=10)

	#rootNode.createObject('EulerImplicitSolver',name='cg_odesolver',printLog='false')
	rootNode.createObject('CGLinearSolver',name='linear solver',iterations=100,tolerance=1.0e-9,threshold=1.0e-9)
	force = [2.0] #np.linspace(-10,10,3)

	for i in force:
		print('Position when force value is ' + str(i))
		controller = CantileverBeam(rootNode,i, [np.random.uniform(-4.0,4.0),np.random.uniform(-4.0,4.0),np.random.uniform(-4.0,4.0)])
		# controller.ff.force = [0,i,0]

