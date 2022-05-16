from graphviz import Digraph

name = 'arbre-viz-profondeur'

g = Digraph('G', filename = name + '.gv', format='png') # par defaut format='pdf'

g.edge('chien', 'petit', color="blue")
g.edge('chien', 'et')
g.edge('petit', 'le')
g.edge('et', 'jaune')
g.edge('et', 'noir')

g.node('et', fillcolor='red', style='filled')

# génere et affiche le graphe name.gv.png
g.view()