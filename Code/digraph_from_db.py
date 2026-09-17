#!/opt/homebrew/bin/python3.12
# A dynamic directed graph using PyVIS from SQLite DB

import networkx as nx

from pyvis.network import Network

def Plot(SoTs,Full_SoTs,Nodes,Edges,Prompt_Nodes):
    G = nx.MultiDiGraph()
    net = Network(notebook=True, directed=True, height='1000px', width='1800px')
    for node in Nodes:
        if node not in Isolated_List:
            Original_Node=node.replace("-\n",'')
            if Original_Node in SoTs:
                I=SoTs.index(Original_Node)
                net.add_node(node, label=Full_SoTs[I], shape="circle", color="rgba(240, 240, 0, 0.5)")
            elif node in SoTs: 
                I=SoTs.index(node)
                net.add_node(node, label=Full_SoTs[I], shape="circle", color="rgba(240, 240, 0, 0.5)")
            elif node in Prompt_Nodes:
                net.add_node(node, label=node, shape="circle", color="rgba(255, 140, 0, 0.9)")
            else:
                net.add_node(node, label=node, shape="circle", color="rgba(0, 140, 255, 0.7)")

    for edge in Edges:
        weight=edge[2]['weight']
        label=edge[2]['val']
        color=edge[2]['color']
        G.add_edge(edge[0], edge[1], label=label, weight=weight, color=color)
        if DEBUG: print (f"{label}:{weight},{color}")

    for u, v, k, d in G.edges(keys=True, data=True):
        try:
            if not u in Isolated_List and not v in Isolated_List:
                net.add_edge(u, v, label=str(d['label']), weight=d['weight'], color=d['color']) 
        except:
            continue
    
    for e in net.edges:
        print (f"Edge {e} - width: {e['weight']}")
        e['width'] = e['weight']

    net.toggle_physics(True)
    net.show_buttons(filter_=['physics'])
    net.show('interactive_multidigraph_from_db.html')