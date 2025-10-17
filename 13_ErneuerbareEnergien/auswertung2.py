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

# fester Abstand d=5cm pm 0.1

d = [10, 20, 30, 40, 15, 25, 35, 13, 8, 32, 5]
U_leer = [3.58, 2.22, 0.95, 0.32, 3.26, 1.37, 0.85, 3.40, 3.77, 0.95, 3.678]

sorted_indices = np.argsort(d)
d_sorted = np.array(d)[sorted_indices]
U_sorted = np.array(U_leer)[sorted_indices]
dd = 0.1
dU_leer = uncert(U_leer)

fig, ax = plt.subplots(1,1, figsize=(7, 4))

ax.errorbar(x=d[:-1], y=U_leer[:-1], yerr=dU_leer[:-1], fmt='+', color='blue', 
                capsize=5, label=r'Messdaten')
ax.errorbar(x=d[-1], y=U_leer[-1], yerr=dU_leer[-1], fmt='+', color='orange', 
                capsize=5, label=r'berechnete Werte')


ax.plot(d_sorted, U_sorted, 'b--')
ax.set_ylabel(r'Spannung $U_\text{leer}$ / V', fontsize=16)

ax.grid(True)
ax.set_xlabel(r'Abstand $d$ / cm', fontsize=16)
ax.legend(frameon=True, fontsize=16)

plt.tight_layout()
plt.show()