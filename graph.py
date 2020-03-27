from graphviz import Digraph, nohtml

g = Digraph('g', filename='btree.gv',
            node_attr={'shape': 'record', 'height': '.1'})
test = '<f0> |<f1> G|<f2>'
for i in range(3,512):
    test += "|<f%d>" % i
g.node('node0', nohtml(test))
g.node('node1', nohtml(test))
g.node('node2', nohtml(test))
g.node('node3', nohtml(test))
g.node('node4', nohtml(test))
g.node('node5', nohtml(test))
g.node('node6', nohtml(test))
g.node('node7', nohtml(test))
g.node('node8', nohtml(test))

g.edge('node0:f2', 'node4:f1')
g.edge('node0:f0', 'node1:f1')
g.edge('node1:f0', 'node2:f1')
g.edge('node1:f2', 'node3:f1')
g.edge('node2:f2', 'node8:f1')
g.edge('node2:f0', 'node7:f1')
g.edge('node4:f2', 'node6:f1')
g.edge('node4:f0', 'node5:f1')

g.view()