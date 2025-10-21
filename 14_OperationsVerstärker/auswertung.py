import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks, savgol_filter
import scienceplots

plt.style.use('science')
plt.rcParams.update({'font.size': 14})

def get_all_csv() -> list[str]:
    files = sorted([i for i in os.listdir(os.getcwd() + '/data') if i[-4:] == '.csv'])
    if not files:
        print(f"Keine .csv Dateien gefunden.")
        return []

    return list(files)

def extract_csv(filepath:str, skipheader:int=12)->tuple:
    with open(f'data/{filepath}', 'r', errors='ignore') as f:
        lines = f.readlines()

    channels = lines[10].split(',')[1:]
    units = lines[11].split(',')
    if len(channels) not in [1, 2]:
        return False

    try:
        data = np.genfromtxt(f'data/{filepath}', delimiter=',', skip_header=skipheader)
    except Exception as e:
        print(f"[ERROR] Datei {os.path.basename(filepath)}: Fehler beim Einlesen: {e}")
        return False
    
    time = data[: , 0]
    ch = []
    for j in range(len(channels)):
        ch.append(data[:, j+1])
    return time, ch, units

files = get_all_csv()
AXES = {
    2 : (0, 0),
    3 : (0, 1),
    4 : (1, 0)
}
fig, axs = plt.subplots(2,2, figsize=(11, 7))

tilte = ['Kriechfall', 'Grenzfall', 'Schwingfall']
color = ['blue', 'green', 'red']
lines = []
for i,j in enumerate([2, 3, 4]):
    x,y = AXES[j]
    time, channels, units = extract_csv(files[j])
    l, = axs[x][y].plot(time, channels[0], color=color[i])
    l.set_label(f'Messung {i+1}: {tilte[i]}')
    axs[x][y].grid(True)
    lines.append(l)

axs[0][0].set_ylabel(r'Spannung $U$ / V', fontsize=18)
axs[1][0].set_ylabel(r'Spannung $U$ / V', fontsize=18)

axs[0][1].set_xlabel(r'Zeit $t$ / s', fontsize=18)
axs[1][0].set_xlabel(r'Zeit $t$ / s', fontsize=18)
#axs[0][0].set_xlabel(r'Zeit $t$ / s', fontsize=18)

axs[1][1].axis('off')
axs[1][1].legend(handles=lines, fontsize=20, loc='center left')
plt.tight_layout()

plt.show()


