import Sofa
def createScene(rootNode):
    node = rootNode
    node.gravity="0 0 0"

    node.createObject('EulerImplicitSolver')
    node.createObject('CGLinearSolver')


    node.createObject('MechanicalObject',position="0 0 0  1 0 0  1 1 0" , showObject=True, showObjectScale=10)
    node.createObject('FixedConstraint',indices="0")
    node.createObject('UniformMass',totalMass=100 )
    node.createObject('StiffSpringForceField',spring="0 1 100 5 1.5   0 2 100 5 1.5   1 2 100 5 1.5")


    cnode = node.createChild("constraint")
    cnode.createObject('MechanicalObject')
    cnode.createObject('DifferenceMapping',pairs="0 1")
    cnode.createObject('UniformCompliance',compliance="1e-5")