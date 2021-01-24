import networkx as nx
from net_calc.get_equations import graphs
from net_calc.graph_properties import pressure_path as pp

from net_calc import solver
from net_calc import dp_calc
import numpy as np

test_1 = [{"data":{"id":"n0","node_type":"feed","pressure":"100"},"position":{"x":100,"y":300},"group":"nodes","removed":False,"selected":False,"selectable":True,\
"locked":False,"grabbable":True,"classes":""},{"data":{"id":"n1","node_type":"cont","pressure":""},"position":{"x":300,"y":300},"group":"nodes","removed":False,\
"selected":False,"selectable":True,"locked":False,"grabbable":True,"classes":""},{"data":{"id":"n2","node_type":"feed","pressure":"50"},"position":{"x":500,"y":200},\
"group":"nodes","removed":False,"selected":False,"selectable":True,"locked":False,"grabbable":True,"classes":""},{"data":{"id":"n3","node_type":"feed","pressure":"50"},\
"position":{"x":500,"y":400},"group":"nodes","removed":False,"selected":False,"selectable":True,"locked":False,"grabbable":True,"classes":""},\
{"data":{"id":"e0","source":"n0","target":"n1","density":"32.2","length":"100","viscosity":"1","diameter":"4","roughness":"0.00015"},"position":{},"group":"edges",\
"removed":False,"selected":False,"selectable":True,"locked":False,"grabbable":True,"classes":""},{"data":{"id":"e1","source":"n1","target":"n2","density":"32.2",\
"length":"100","viscosity":"0.1","diameter":"4","roughness":"0.00015"},"position":{},"group":"edges","removed":False,"selected":False,"selectable":True,\
"locked":False,"grabbable":True,"classes":""},{"data":{"id":"e2","source":"n1","target":"n3","density":"32.2","length":"50","viscosity":"1","diameter":"4",\
"roughness":"0.00015"},"position":{},"group":"edges","removed":False,"selected":False,"selectable":True,"locked":False,"grabbable":True,"classes":""}]

def get_result (input_data):
    G=nx.MultiDiGraph()
    for element in input_data:

        if element['group'] == 'nodes':
            if element['data']['pressure'] == '':
                G.add_node(element['data']['id'] ,type= element['data']['node_type'], T=100,P=(element['data']['pressure']))
            else:
                G.add_node(element['data']['id'] ,type= element['data']['node_type'], T=100,P=float(element['data']['pressure']))

        else:
            G.add_edge(element['data']['source'], element['data']['target'], Q='',ID=element['data']['id'],rho=62.4,mu=0.000671968994813,\
                segments={1:{'var':'pipe','L':float(element['data']['length']),'D':float(element['data']['diameter']),'roughness':float(element['data']['roughness'])}})

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

    # for key in result.keys():
    #     result[key]=result[key]*62.4*3.6



    return result



