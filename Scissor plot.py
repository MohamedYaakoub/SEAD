import numpy as np
from matplotlib import pyplot as plt

# Global variables
A = 8.89   # aspect ration Main wing
A_h = 7.88
taper_mw = 0.356
taper_h = 0.410
c = 3  # I used MAC #Ø: should be 2.934 I think.
lh = 28.55 - 0.08861 * 28.55 - 12.49 + 1.038 - 0.25 * c  # length of aircraft - approx 3/4 tail - AX0 + AX0 to lemac - quarter chord
lf = 26.5

b = 26.21  # wing span probably!!
bf = 3.56  # fuselage diameter - I put width #Assumed circular
bn = 1.4
ln = 2.6    #I put length of the engine
hf = bf

lf_n = 28.55 - lh - ln

VhV2 = 1  # T-tail
lambda_quarter_chord_mw = np.radians(15)  # main wing
lambda_quarter_chord_h = np.radians(20)
S = 77.3  # Main wing area
S_net = S - bf * c  # net surface area of the wing (without the area inside in the fuselage)
S_h = 15.61
Swf_S = 0.78 * 0.25  # ratio between flapped wing area and reference wing area (as defined in the wing design module). Consider only the TE flaps here!


# 'depth' of flaps are about 25% of the wing. Flap width/wing width = 0.78

def lambda_n(n, m, phi_m, Aspect_ratio, taper):
    return np.arctan(np.tan(phi_m) - 4 / Aspect_ratio * ((n - m) / 100 * (1 - taper) / (1 + taper)))


lambda_half_chord_mw = lambda_n(50, 25, lambda_quarter_chord_mw, A, taper_mw)
lambda_half_chord_h = lambda_n(50, 25, lambda_quarter_chord_h, A_h, taper_h)
lambda_LE_mw = lambda_n(0, 25, lambda_quarter_chord_mw, A, taper_mw)
lambda_LE_h = lambda_n(0, 25, lambda_quarter_chord_h, A_h, taper_h)

# print(np.degrees(lambda_half_chord_mw))
# print(np.degrees(lambda_half_chord_h))
# print(np.degrees(lambda_LE_mw))
# print(np.degrees(lambda_LE_h))

eta_mw = 0.95
eta_h = 0.95
mach_cruise = 0.730  # at cruise alt
mach_landing = 0.189

CL = 3.43  # wing lift coefficient at landing (all flaps deployed) I used at L/D
CL_h = - 0.35 * A_h ** (1 / 3)
CL0 = 0.15  # CL0 is the lift coefficient of the flapped wing at zero angle of attack ##CHANGE!!!


def fun_CL_a(mach, wing_area, eta, lambda_half_chord):  # will be used for both the main wing and the horizontal tail
    beta = np.sqrt(1 - mach ** 2)
    result = (2 * np.pi * wing_area) / (
            2 + np.sqrt(4 + (wing_area * beta / eta) ** 2 * (1 + (np.tan(lambda_half_chord)) ** 2 / beta ** 2)))
    return result



def fun_CL_aAh(mach, wing_area, eta, lambda_half_chord):
    CL_aW = fun_CL_a(mach, wing_area, eta, lambda_half_chord)
    print(CL_aW, mach)
    result = CL_aW * (1 + 2.15 * bf / b) * S_net / S + (np.pi / 2) * (bf ** 2 / S)
    # print(CL_aW * (1 + 2.15 * bf / b) * S_net / S, (np.pi / 2) * (bf ** 2 / S), mach)
    return result


def wing_downwash():
    CL_aAh = fun_CL_aAh(mach_cruise, S, eta_mw, lambda_half_chord_mw)
    weird_distance = 4.2  # check slide 42  ##CHANGE!!!

    r = 2 * lh / b
    mtv = 2 * weird_distance / b
    k_e = (0.1124 + 0.1265 * lambda_quarter_chord_mw + 0.1766 * lambda_quarter_chord_mw ** 2) / r ** 2 + 0.1024 / r + 2
    k_e0 = 0.1124 / r ** 2 + 0.1024 / r + 2
    # CL_aW = fun_CL_a(mach_cruise, 0, 0, 0)
    result = k_e / k_e0 * (r / (r ** 2 + mtv ** 2) * 0.4876 / np.sqrt(r ** 2 + 0.6319 + mtv ** 2) +
                           (1 + (r ** 2 / (r ** 2 + 0.7915 + 5.0734 * mtv ** 2)) ** 0.3113) * (
                                   1 - np.sqrt(mtv ** 2 / (1 + mtv ** 2)))) * CL_aAh / (np.pi * A)
    return result


def fun_Cm_ac():
    CL_aAh = fun_CL_aAh(mach_landing, S, eta_mw, lambda_half_chord_mw)
    Cm_0 = -0.06
    Cm_ac_w = Cm_0 * (A * np.cos(lambda_LE_mw) ** 2 / (A + 2 * np.cos(lambda_LE_mw)))
    Cm_ac_fus = -1.8 * (1 - 2.5 * bf / lf) * (np.pi * bf * hf * lf / (4 * S * c)) * (
            CL0 / CL_aAh)  # compute CL_aAH for low speed

    def fun_Cm_ac_flaps():
        u1 = 0.20125  # check slide 18
        u2 = 0.8  # recheck slide 19
        u3 = 0.04  # recheck slide 19
        cprime_c = 1.233    ##CHANGE!!!
        delta_Cl_max = 1.6  # the airfoil lift coefficient increase due to flap extension at landing condition (estimated in the wing design module)  ##CHANGE!!!

        Cm_025 = u2 * (- u1 * delta_Cl_max * cprime_c - (CL + delta_Cl_max * (1 - Swf_S)) * 1 / 8 * cprime_c * (
                cprime_c - 1)) + \
                 0.7 * A / (1 + 2 / A) * u3 * delta_Cl_max * np.tan(lambda_quarter_chord_mw)
        return Cm_025 - CL * (0.25 - fun_x_ac(mach_landing) / c)

    Cm_ac_flaps = fun_Cm_ac_flaps()
    return Cm_ac_w + Cm_ac_fus + Cm_ac_flaps  # nacelle contribution is still remaining


def fun_x_ac(mach):
    CL_aAh = fun_CL_aAh(mach, S, eta_mw, lambda_half_chord_mw)
    if mach == 0.73:
        wing = 0.28  # using lambda = 17.8 and A = 8.89
    else:
        wing = 0.27
    fus_1 = -1.8 / CL_aAh * (bf * hf * lf_n) / (S * c)
    fus_2 = 0.273 / (1 + taper_mw) * (bf * S / b * (b - bf)) / (c ** 2 * (b + 2.15 * bf)) * np.tan(lambda_quarter_chord_mw)
    nacelles = -4 * (bn ** 2 * ln) / (S * c * CL_aAh) * 4
    return wing + fus_1 + fus_2 + nacelles




def plot_stability():
    CL_a_h = fun_CL_a(mach_cruise, S_h, eta_h, lambda_half_chord_h)
    x_ac = fun_x_ac(mach_cruise)
    CL_aAh = fun_CL_aAh(mach_cruise, S, eta_mw, lambda_half_chord_mw)

    de_da = wing_downwash()
    print(de_da)
    # CL_ah = fun_CL_a(0, 0, 0, 0)

    m = 1 / (CL_a_h / CL_aAh * (1 - de_da) * lh / c * VhV2)  # slope
    q = -(x_ac - 0.05) * m
    q_2 = -x_ac * m
    x_plot = np.linspace(0, 1, 100)
    y_plot = m * x_plot + q
    y_plot_2 = m * x_plot + q_2
    plt.plot(x_plot, y_plot, label='Stability')
    plt.plot(x_plot, y_plot_2, label='Neutral Stability', linestyle= "dashed")


def plot_controllability():
    x_ac = fun_x_ac(mach_landing)
    Cm_ac = fun_Cm_ac()
    print(Cm_ac, "asdasd")
    CL_AH = CL  # CLA-h can be approximated with the wing lift coefficient (in this case at landing condition), ignoring the minor contribution of the fuselage.
    m = 1 / (CL_h / CL_AH * lh / c * VhV2)
    q = (Cm_ac / CL_AH - x_ac) / (CL_h / CL_AH * lh / c * VhV2)
    x_plot = np.linspace(0, 1, 100)
    y_plot = m * x_plot + q
    plt.plot(x_plot, y_plot, label='Controllability')


if __name__ == '__main__':
    plot_stability()
    plot_controllability()
    # plot_controllability()
    plt.ylabel(r'$S_h$/S')
    plt.xlabel(r'$X_{cg}$ / MAC')
    plt.axhline(y = 0, color='black')
    plt.axvline(x= 0, color='black')
    plt.axhline(y=S_h/S,label='Current horizontal wing size ratio', color = 'black', linestyle = 'dotted')
    plt.legend()
    plt.ylim(0)
    plt.xlim(0,1)
    plt.grid()
    plt.show()

