import networkx as nx
from net_calc.graph_properties import pressure_path as pp
from math import pow
from net_calc import dp_calc


class graphs:

    def __init__(self, multi_di_graph):
        self.multi_di_graph = multi_di_graph

    def unknownQ(self, node_):
        '''
        :param node_: node in graph, unit less, integer
        :return: number of unknown Q in pipes from node_, unit less, integer
        '''
        G = self.multi_di_graph
        temp_Q = 0
        for u, v, w in list(G.in_edges(node_, data=True)) + list(G.out_edges(node_, data=True)):
            if not w['Q']: temp_Q += 1
        return temp_Q

    def get_base_equation(self):
        """
        :return: dict as key= ID of unknown pipe, value=0
        """
        G = self.multi_di_graph
        mbase = {}
        for u, v, w in G.edges(data=True):
            if not w['Q']: mbase[w['ID']] = 0
        return mbase

    def get_q_equation(self,node_):
        '''

        :param node_: node in a graph, unit less, integer
        :return: coefficient of q equation around node, m as dict in LHS, n as number at RHS
        '''

        m_temp=self.get_base_equation()
        G = self.multi_di_graph
        n = 0
        m = {}
        for u, v, w in G.in_edges(node_, data=True):
            if not w['Q']:
                m[w['ID']] = 1
            else:
                n -= w['Q']
        for u, v, w in G.out_edges(node_, data=True):
            if not w['Q']:
                m[w['ID']] = -1
            else:
                n += w['Q']
        return [{**m_temp,**m}, n]

    def get_q_system_equation(self):
        temp_q=[]
        G=self.multi_di_graph
        for node in G.node:
            if G.node[node]['type']=='feed' or G.node[node]['type']== 'prod': continue
            temp_q.append(self.get_q_equation(node))
        return temp_q

    def get_p_equation(self,pair, Q_olds, Q_news,i=0):
        '''

        :param node_1: node 1, unit less, integer
        :param node_2: node 2, unit less, integer
        :param Q_olds: flow rate 1 in dict, ft3/s, float
        :param Q_news: flow rate 2 in dict, ft3/s, float
        :return: kQ^(n-1), unit less, float
        '''
        G = self.multi_di_graph
        node_1=pair[0]
        node_2=pair[1]
        p_sign=pair[2]

        edge_data = G.get_edge_data(node_1, node_2)[i]

        ID=edge_data['ID']
        Q_old=Q_olds[ID]
        Q_new=Q_news[ID]
        mu = edge_data['mu']
        rho = edge_data['rho']
        segments = edge_data['segments']
        temp_nK = 0
        for segment in segments.values():
            if segment['var'] == 'pipe':
                L = segment['L']
                D = segment['D']
                roughness = segment['roughness'] / D
                Re = dp_calc.get_reynolds_number(D, Q_new, rho, mu)
                nK = dp_calc.get_nK(Q_old, Q_new, rho, mu, D, L, roughness)
                temp_nK += nK[1] * pow(abs(Q_new), nK[0] - 1)
        return {ID:p_sign*temp_nK}

    #---------- get p equations here----------------

    def get_p_path_equation(self,paths,m_base,Q_olds,Q_news):

        for path in paths:
            temp_p=m_base
            for pair in path[0]:
                temp_p={**temp_p, **self.get_p_equation(pair,Q_olds,Q_news)}
            yield [temp_p,path[1]]





    def get_p_parallel_equation(self,paths,m_base,Q_olds,Q_news):
        G = self.multi_di_graph
        for path_ in paths:
            path=path_[0]
            temp_p=m_base

            temp_p=dict(temp_p,**self.get_p_equation(path[0] , Q_olds, Q_news))
            if path[0][0]==path[1][0] and path[0][1]==path[1][1]:
                temp_p = {**temp_p, **self.get_p_equation(path[1], Q_olds, Q_news,1)}
            else:
                temp_p = {**temp_p, **self.get_p_equation(path[1], Q_olds, Q_news)}



            yield [temp_p,path_[1]]

