from net_calc import dp_calc
#from iapws import IAPWS97
import math
import numpy as np

def solve_lin_equation(dict_values):
    m,n=[],[]
    for u,v in dict_values:
        m.append(list(u.values()))
        n.append(v)

    return np.linalg.solve(m,n)


def convertvisc(val,in_unit,out_unit):
    con_dict={'cP':1,'ft/lb-s':0.000673}
    return val*con_dict[out_unit]/con_dict[in_unit]


test = [[{1: 1, 2: -1, 3: -1, 6: 0, 7: 0, 9: 1, 8: 0, 5: 0}, 0], [{1: 0, 2: 1, 3: 0, 6: -1, 7: -1, 9: 0, 8: 0, 5: 0}, 0], [{1: 0, 2: 0, 3: 1, 6: 0, 7: 0, 9: 0, 8: 0, 5: 1}, -0.4449], [{1: 0, 2: 0, 3: 0, 6: 1, 7: 0, 9: -1, 8: -1, 5: 0}, 0.4449], [{1: 0, 2: 0.35708521557940925, 3: 0, 6: 0.35708521557940925, 7: 0, 9: 0.35708521557940925, 8: 0, 5: 0}, 0], [{1: 0, 2: 0, 3: 0.35708521557940925, 6: 0, 7: 0, 9: 0.35708521557940925, 8: 0, 5: 0}, 0.29692935523125497], [{1: 0.35708521557940925, 2: 0.35708521557940925, 3: 0, 6: 0, 7: 0.35708521557940925, 9: 0, 8: 0, 5: 0}, 196.0], [{1: 0.35708521557940925, 2: 0, 3: 0, 6: 0, 7: 0, 9: -0.35708521557940925, 8: 0.35708521557940925, 5: 0}, 211.0]]
m,n=[],[]
for u,v in test:
    m.append(list(u.values()))
    n.append(v)

