import os
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
from matplotlib.gridspec import GridSpec
from scipy.optimize import curve_fit
from scipy.signal import find_peaks, savgol_filter

plt.style.use('science')
plt.rcParams.update({'font.size': 14})

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

with open("13_ErneuerbareEnergien/data/measure01.dat") as f:
    data = np.array([float(i.strip('\n').replace(',', '.')) for i in f.readlines()])

time = np.arange(0, len(data), 1) #s
d_data = 0.005*data + 0.03

dV = 0.5
dt = 0.1
t_fit = np.linspace(0, 7.38, 1000)

#popt, pcov = curve_fit(ffit, t, V)
#V_fit = ffit(t_fit, *popt)
#fit_param = np.sqrt(np.diag(pcov))
fig, ax = plt.subplots(1,1, figsize=(7, 4))

#ax.errorbar(x=time, y=data, yerr=d_data, fmt='o', color='blue', 
#                capsize=5, label=r'Messdaten', markersize=4)
ax.scatter(time, data, marker="+")
ax.set_ylabel(r'Spannung $U_C$ / V', fontsize=16)
ax.grid(True)
ax.set_xlabel(r'Zeit $t$ / s', fontsize=16)
ax.legend(frameon=True, fontsize=16)
plt.tight_layout()
plt.show()
