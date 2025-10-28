import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks, savgol_filter
import scienceplots

plt.style.use('science')
plt.rcParams.update({'font.size': 14})

r_0 = 190 #cm

measure1 = [
    (5, 159.2),
    (15,158.9),
    (25,158.3),
    (35,157.4),
    (45,156.6),
    (55,155.7),
    (65,154.4),
    (75,152.1),
    (85,147.7),
    (90,141.2),
    (40,157.2)
] 
res1 = []
for s,o in measure1:
    g = r_0 - o
    b = o - s
    l = 1/b + 1/g 
    res1.append(1/l)
print(res1)

measure2 = [
    (20, 158.4, 49.9),
    (30, 157.6, 60.4),
    (40, 157.3, 71.3),
    (50, 156.1, 82.0),
    (60, 155.1, 93.0)
]
res2 = []
for s,o1,o2 in measure2:
    a = r_0 - s
    b1 = o1 - s
    b2 = o2 - s
    e = b1 - b2
    f = 0.25* (a**2 - e**2)/a
    res2.append(f)
print(res2)
measure3 = [
    (5, 93.7),
    (15,93.4),
    (25,93.0),
    (35,92.6),
    (45,92.2),
    (55,91.5),
    (65,90.2),
    (70,89.5),
    (30,92.8),
    (10,93.5),
]
res3 = []
B_prime = 80.9
print(B_prime)
for rb, rl in measure3:
    b = rl - rb
    g_prime = rl - B_prime

    l = 1/b - 1/g_prime
    res3.append(1/l)

print(res3)
