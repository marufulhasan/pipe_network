import networkx as nx
from net_calc.get_equations import graphs
from net_calc.graph_properties import pressure_path as pp

from net_calc import solver
from net_calc import dp_calc
import numpy as np



def get_result (input_data):
    G=nx.MultiDiGraph()
    for element in input_data:

        if element['group'] == 'nodes':
            if element['data']['pressure'] == '':
                G.add_node(element['data']['id'] ,type= element['data']['node_type'], T=100,P=(element['data']['pressure']))
            else:
                G.add_node(element['data']['id'] ,type= element['data']['node_type'], T=100,P=2.31 * (14.696 + float(element['data']['pressure'])))

        else:
            G.add_edge(element['data']['source'], element['data']['target'], Q='',ID=element['data']['id'],rho=62.4,mu=0.000671968994813,\
                segments={1:{'var':'pipe','L':float(element['data']['length']),'D':float(element['data']['diameter'])/12,'roughness':float(element['data']['roughness'])}})

    # G.add_node('n0',type='feed', T=100,P=231.0)
    # G.add_edge('n0','n1',Q='',ID=1,rho=62.4,mu=0.000671968994813,segments={1:{'var':'pipe','L':100.0,'D':0.5,'roughness':0.0001509}})






    test=pp(G)
    eq=graphs(G)




    mbase=eq.get_base_equation()
    IDs=mbase.keys()

    Q1,Q2={},{}
    for key in mbase.keys():
        Q1[key]=1
        Q2[key]=.2


    q=eq.get_q_system_equation()


    par=test.get_parallel_paths()
    par_path=test.rearrange_path(par)


    cyc=test.get_cycle()
    cyc_path=test.rearrange_path(cyc)

    kp=test.get_pressure_path()
    kp_path=test.rearrange_path(kp)
    result = {}
    for i in range(100):
        try:
            par_eq=list(eq.get_p_parallel_equation(par_path,mbase,Q1,Q2))
            cyc_eq=list(eq.get_p_path_equation(cyc_path,mbase,Q1,Q2))
            kp_eq=list(eq.get_p_path_equation(kp_path,mbase,Q1,Q2))


            temp= solver.solve_lin_equation(q+par_eq+cyc_eq+kp_eq)
            result=dict(zip(IDs,np.around(temp,4)))



            Q1=Q2
            Q2=dict(zip(IDs,temp))
            for key in Q2.keys():
                Q2[key]=(Q1[key]+Q2[key])/2
        except:
            break

    for key in result.keys():
        result[key]= round (result[key]*62.4*3600, 2)



    return result



