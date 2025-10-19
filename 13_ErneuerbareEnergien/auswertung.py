import os
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
from scipy.optimize import curve_fit
from matplotlib.patches import Patch

plt.style.use('science')
plt.rcParams.update({'font.size': 16})

def uncert(values, mode='voltage'):
    uncert = []
    for v in values:
        if mode == 'voltage':
            if v > 2: uncert.append(0.005*v + 0.03)
            else: uncert.append(0.005*v + 0.003)
        if mode == 'current':
            if v > 19: uncert.append(0.015*v + 0.3) # hardcode for the rounding of 19.4 to be correct
            else: uncert.append(0.01*v + 0.05)
    return uncert

def ffit(t, U_0, lam):
    return U_0 * np.exp(-lam*t)

# d= 11 pm 0.1 cm
# U_M = 10.09 pm 1%

files = [f'measure0{i}.dat' for i in range(1,4)]
measures = []
for name in files:
    with open("13_ErneuerbareEnergien/data/"+ name, 'r') as file:
        data = np.array([float(i.strip('\n').replace(',', '.')) for i in file.readlines()])
        time = np.arange(0, len(data), 1) #s
        d_data = 0.005*data + 0.03
        measures.append((data, time, d_data))



colors = ['blue', 'crimson', 'forestgreen']  # data colors (blue, green, red)
fit_colors = ['#222222', '#222222', '#222222']  # all fits black

fit_ranges = [(55,88,2), (154,210,3), (203,242,3)]

for i, measure in enumerate(measures):
    fig, axs = plt.subplots(1,2, figsize=(10, 4))

    y,t, dy = measure
    tmin, tmax, step = fit_ranges[i]
    
    popt, pcov = curve_fit(ffit, t[tmin:tmax] - tmin, y[tmin:tmax])
    t_fit = np.linspace(tmin*0.98, tmax*1.02, 1000)
    y_fit = ffit(t_fit - tmin, *popt)
    fit_param = np.sqrt(np.diag(pcov))

    axs[0].scatter(t,y, marker='+', color=colors[i], label=f'Messung {i}')
    axs[0].set_ylabel(r'Spannung $U_C$ / V', fontsize=18.5)
    axs[0].axvspan(
    tmin, tmax,
        color='grey',       # or a custom muted tone
        alpha=0.3,          # transparency (adjust 0.1–0.3 for taste)
    )
    axs[0].grid(True)

    axs[1].errorbar(x=t[tmin:tmax:step], y=y[tmin:tmax:step], yerr=dy[tmin:tmax:step], capsize=5,
                    color=colors[i], fmt="d", markersize=4, label=f'Messreihe {i+1}')
    axs[1].plot(t_fit, y_fit, color=fit_colors[i], label='Ausgleichskurve')
    axs[1].grid(True)

    axs[0].set_xlabel(r'Zeit $t$ / s', fontsize=18.5)
    axs[1].set_xlabel(r'Zeit $t$ / s', fontsize=18.5)
    plt.tight_layout()
    tau = 1/popt[1]
    dtau = fit_param[1]/(popt[1]**2)
    print(tau, dtau)
    plt.show()

tau = R = 60.74748886693542
dR = 60.74748886693542* (0.4410166246142596 / 60.74748886693542 + 0.01/1)

CB = 59.3777750254805 / R
dCB = CB * (0.4014629336478521 / 59.3777750254805 + dR / R)

CA =  21.656671105789 / R
dCA = CA * ( 0.13572845444462314 / 21.656671105789 + dR/R)

print(CA*1000, dCA*1000)
print(CB*1000, dCB*1000)
