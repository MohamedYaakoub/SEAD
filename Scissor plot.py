import numpy as np
from matplotlib import pyplot as plt

# Global variables
A = 8.89  # aspect ration Main wing
A_h = 7.88
taper_mw = 0.356
taper_h = 0.410
c = 3.17  # I used MAC #Ø: should be 2.934 I think.
lh = 28.55 - 0.08861 * 28.55 - 12.49 + 1.038 - 0.25 * c  # length of aircraft - approx 3/4 tail - AX0 + AX0 to lemac - quarter chord
lf = 0
lf_n = lh  ###### CHANGEEE###########

b = 26.21  # wing span probably!!
bf = 3.56  # fuselage diameter - I put width #Assumed circular
bn = 1.4
ln = 2.6    #I put length of the engine
hf = bf

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
eta_mw = 0.95
eta_h = 0.95
mach_mw = 0.730  # at cruise alt
mach_h = mach_mw

CL = 0  # wing lift coefficient at landing (all flaps deployed)
CL_h = - 0.35 * A_h ** (1 / 3)
CL0 = 0  # CL0 is the lift coefficient of the flapped wing at zero angle of attack


def fun_CL_a(mach, wing_area, eta, lambda_half_chord):  # will be used for both the main wing and the horizontal tail
    beta = np.sqrt(1 - mach ** 2)
    result = (2 * np.pi * wing_area) / (
            2 + np.sqrt(4 + (wing_area * beta / eta) ** 2 * (1 + (np.tan(lambda_half_chord)) ** 2 / beta ** 2)))
    print(result)
    return result


# CL_a_mw = fun_CL_a(mach_mw, S, eta_mw, lambda_half_chord_mw)
CL_a_h = fun_CL_a(mach_h, S_h, eta_h, lambda_half_chord_h)


def fun_CL_aAh(mach, wing_area, eta, lambda_half_chord):
    CL_aW = fun_CL_a(mach, wing_area, eta, lambda_half_chord)
    result = CL_aW * (1 + 2.15 * bf / b) * S_net / S + (np.pi / 2) * (bf ** 2 / S)
    return result


CL_aAh = fun_CL_aAh(mach_mw, S, eta_mw, lambda_half_chord_mw)


def wing_downwash():
    weird_distance = lh / 3  # check slide 42

    r = 2 * lh / b
    mtv = 2 * weird_distance / b
    k_e = (0.1124 + 0.1265 * lambda_quarter_chord_mw + 0.1766 * lambda_quarter_chord_mw ** 2) / r ** 2 + 0.1024 / r + 2
    k_e0 = 0.1124 / r ** 2 + 0.1024 / r + 2
    # CL_aW = fun_CL_a(mach_mw, 0, 0, 0)
    result = k_e / k_e0 * (r / (r ** 2 + mtv ** 2) * 0.4876 / np.sqrt(r ** 2 + 0.6319 + mtv ** 2) +
                           (1 + (r ** 2 / (r ** 2 + 0.7915 + 5.0734 * mtv ** 2)) ** 0.3113) * (
                                   1 - np.sqrt(mtv ** 2 / (1 + mtv ** 2)))) * CL_aAh / (np.pi * A)
    return result


def fun_Cm_ac():
    Cm_0 = 0
    Cm_ac_w = Cm_0 * (A * np.cos(lambda_LE_mw) ** 2 / (A + 2 * np.cos(lambda_LE_mw)))
    Cm_ac_fus = -1.8 * (1 - 2.5 * bf / lf) * (np.pi * bf * hf * lf / (4 * S * c)) * (
            CL0 / fun_CL_aAh(0))  # compute CL_aAH for low speed

    def fun_Cm_ac_flaps():
        u1 = 0  # check slide 18
        u2 = 0.8  # recheck slide 19
        u3 = 0.04  # recheck slide 19
        cprime_c = 0
        delta_Cl_max = 0  # the airfoil lift coefficient increase due to flap extension at landing condition (estimated in the wing design module)

        Cm_025 = u2 * (- u1 * delta_Cl_max * cprime_c - (CL + delta_Cl_max * (1 - Swf_S)) * 1 / 8 * cprime_c * (
                cprime_c - 1)) + \
                 0.7 * A / (1 + 2 / A) * u3 * delta_Cl_max * np.tan(lambda_quarter_chord_mw)
        return Cm_025 - CL * (0.25 - fun_x_ac() / c)

    Cm_ac_flaps = fun_Cm_ac_flaps()

    return Cm_ac_w + Cm_ac_fus + Cm_ac_flaps  # nacelle contribution is still remaining


def fun_x_ac():
    wing = 0.28  # using lambda = 17.8 and A = 8.89
    fus_1 = -1.8 / CL_aAh * (bf * hf * lf_n) / (S * c)
    fus_2 = 0.273 / (1 + taper_mw) * (bf * S / b * (b - bf)) / (c ** 2 * (b + 2.15 * bf))
    nacelles = -4 * (bn ** 2 * ln) / (S * c * CL_aAh) * 4
    return wing + fus_1 + fus_2 + nacelles


x_ac = fun_x_ac()


def plot_stability():
    de_da = wing_downwash()
    # CL_ah = fun_CL_a(0, 0, 0, 0)

    m = 1 / (CL_a_h / CL_aAh * (1 - de_da) * lh / c * VhV2)  # slope
    q = -(x_ac - 0.05) * m
    print(q)
    x_plot = np.linspace(0, 1, 100)
    y_plot = m * x_plot + q
    plt.plot(x_plot, y_plot, label='stability')


def plot_controllability():
    Cm_ac = fun_Cm_ac()
    CL_AH = 0  # CLA-h can be approximated with the wing lift coefficient (in this case at landing condition), ignoring the minor contribution of the fuselage.
    m = 1 / (CL_h / CL_AH * lh / c * VhV2)
    q = (Cm_ac / CL_AH - x_ac) / (CL_h / CL_AH * lh / c * VhV2)


if __name__ == '__main__':
    plot_stability()
    # plot_controllability()
    plt.ylabel(r'$S_h$/S')
    plt.xlabel(r'$X_{cg}$ / MAC')
    plt.axhline(y = 0, color='black')
    plt.axvline(x= 0, color='black')
    plt.legend()
    plt.show()

