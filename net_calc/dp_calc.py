from math import log, pow, pi

'''calculate different pressure drop properties'''


def get_friction_factor(roughness_factor, reynolds_number):
    """

    :param roughness_factor:  roughness/ diameter, unitless, float
    :param reynolds_number: flow property,unitless integer
    :return: moddy's friction factor,unitless, float

    reference: moody's chart
    action item: add more method like swame jain

    """

    # laminer flow.
    if reynolds_number == 0:
        return 0.1

    if reynolds_number < 2100:
        return max(0.03, 64 / reynolds_number)

    # Turbulent
    x1 = roughness_factor * reynolds_number * 0.12396818633
    x2 = log(reynolds_number) - 0.7793974884

    f = x2 - 0.2
    g = (log(x1 + f) + f - x2) / (1 + x1 + f)
    f = f - (1 + x1 + f + 0.5 * g) * g * (x1 + f) / (1 + x1 + f + g * (1 + g / 3))

    g = (log(x1 + f) + f - x2) / (1 + x1 + f)
    f = f - (1 + x1 + f + 0.5 * g) * g * (x1 + f) / (1 + x1 + f + g * (1 + g / 3))

    f = 1.151292546497022842 / f

    return f * f

def get_reynolds_number(diameter, Q, rho, mu):
    '''

    :param diameter: diameter, feet, float
    :param Q: flowrate, ft3/second, float
    :param rho: density, lb/ ft3, float
    :param mu: viscosity, lb/ft.sec, float

    :return: reynolds number, unitless, integer
    '''
    return int(4 * abs(Q) * rho / (pi * diameter * mu))

def get_nK(Q1, Q2, rho, mu, d, L, K):
    '''

    :param Q1: flow rate 1, ft3/s, float
    :param Q2: flow rate 2, ft3/s, float
    :param rho: density, lb/ft3, float
    :param mu: viscosity, lb/ft.sect, float
    :param d: diameter, ft, float
    :param L: length, ft, float
    :param K: roughness factor, unitless, float
    :return: nK in h=KQ^n as array, unitless, float
    '''
    R1 = get_reynolds_number(d, Q1, rho, mu)
    R2 = get_reynolds_number(d, Q2, rho, mu)

    F1 = get_friction_factor(K, R1)
    F2 = get_friction_factor(K, R2)

    b = (log(abs(F1)) - log(abs(F2))) / (log(abs(Q2)) - log(abs(Q1)))
    a = F1 * pow(abs(Q1), b)

    area = pi * d * d / 4
    return 2 - b, a * L / (2 * 32.2 * d * area * area)

def hazennK(L,d,Cw):
    '''

    :param L: pipe length, ft, float
    :param d: pipe diameter, ft, float
    :param Cw: hazen williams factor, unitless, integer
    :return: nK in h=K*Q^n as array, unitless, float
    '''
    return 1.852,4.73*L/(pow(Cw,1.852)*pow(d,4.87))

def get_dp(G,node1,node2,i=0):
    temp_dp=0
    edge_data=G.get_edge_data(node1,node2)[i]
    Q=edge_data['Q']
    Q_sign=Q/abs(Q)
    Q=abs(Q)

    for segment in edge_data['segments'].values():
        L,D= segment['L'],segment['D']
        epsilon = segment['roughness']/D
        rho,mu=62.36,0.000671968994813 # TBD, add inside segment
        re=get_reynolds_number(D,Q,rho,mu)
        f=get_friction_factor(epsilon,re)
        velocity=4*Q/(pi*D*D)
        temp_dp+=f*(L/D)*(velocity*velocity/(2*32.17405))
    return temp_dp*Q_sign























