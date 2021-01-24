import networkx as nx
from net_calc import dp_calc

class pressure_path:

    def __init__(self, multi_graph):
        self.multi_graph = multi_graph

    def get_pressure_path(self):
        G = self.multi_graph
        G_graph = nx.Graph(G)
        p_nodes = []
        for node_ in G.node:
            if G.node[node_]['P'] is not '': p_nodes.append(node_)

        if len(p_nodes) > 0:
            start_node = p_nodes[0]
            for node_ in p_nodes[1:]:
                yield nx.shortest_path(G_graph, start_node, node_)
        else:
            yield p_nodes

    def get_parallel_paths(self):
        G = self.multi_graph
        for u, v, w in nx.Graph(G).edges(data=True):
            if G.number_of_edges(u, v)+G.number_of_edges(v,u) > 1: yield [u, v, u]

    def get_cycle(self):
        G = self.multi_graph
        cycles = nx.cycle_basis(nx.Graph(G))

        for cycle in cycles:
            cycle.append(cycle[0])
            yield cycle

    def rearrange_path(self,paths):
        G = self.multi_graph
        temp_paths=[]
        for path in paths:
            if path[0]==path[-1]:
                temp_n=0
            else:
                temp_n=G.node[path[0]]['P']-G.node[path[-1]]['P']
            #----

            #-----
            temp_path = []
            for i in range(len(path) - 1):
                if path[i] in G.predecessors(path[i + 1]):
                    if G.get_edge_data(path[i],path[i+1])[0]['Q']:
                        temp_n-=dp_calc.get_dp(G,path[i],path[i+1])
                    else:
                        temp_path.append([path[i], path[i + 1],1])
                else:
                    if G.get_edge_data(path[i+1], path[i ])[0]['Q']:
                        temp_n += dp_calc.get_dp(G, path[i+1], path[i])
                    else:
                        temp_path.append([path[i + 1], path[i],-1])
                    #---
                    #----

            temp_paths.append([temp_path,temp_n])

        return temp_paths