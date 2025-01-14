import matplotlib.pyplot as plt
import numpy as np

# Load curve
data_inf = np.loadtxt("results/loadcurve_inf.data")
data_K10 = np.loadtxt("results/loadcurve_K10.data")
data_K7 = np.loadtxt("results/loadcurve_K7.data")
data_K5 = np.loadtxt("results/loadcurve_K5.data")

x_inf, y_inf, yerr_inf = data_inf[:, 0], data_inf[:, 11], data_inf[:, 12]
x_K10, y_K10, yerr_K10 = data_K10[:, 0], data_K10[:, 11], data_K10[:, 12]
x_K7, y_K7, yerr_K7 = data_K7[:, 0], data_K7[:, 11], data_K7[:, 12]
x_K5, y_K5, yerr_K5 = data_K5[:, 0], data_K5[:, 11], data_K5[:, 12]

# Plot
plt.figure(figsize=(10, 6))
plt.ylim(bottom=0, top=1.2)
plt.errorbar(x_inf, y_inf, yerr=yerr_inf, fmt='o', label=r'$T_{Resp} Qlen=\infty$', color='C1', markersize=6)
plt.errorbar(x_K10, y_K10, yerr=yerr_K10, fmt='o', label=r'$T_{Resp} Qlen=10$', color='C2', markersize=6)
plt.errorbar(x_K7, y_K7, yerr=yerr_K7, fmt='o', label=r'$T_{Resp} Qlen=7$', color='C3', markersize=6)
plt.errorbar(x_K5, y_K5, yerr=yerr_K5, fmt='o', label=r'$T_{Resp} Qlen=5$', color='C4', markersize=6)
plt.plot(x_inf, y_inf, label='_nolegend_', color='C1')
plt.plot(x_K10, y_K10, label='_nolegend_', color='C2')
plt.plot(x_K7, y_K7, label='_nolegend_', color='C3')
plt.plot(x_K5, y_K5, label='_nolegend_', color='C4')

plt.xlabel(r'${\rho}$', fontsize=12)
plt.ylabel('Time [s]', fontsize=12)
plt.legend(loc='upper left')
plt.savefig("TrespMM1.png", dpi=300, bbox_inches='tight')

# Response time breakdown
data_inf = np.loadtxt("results/loadcurve_inf.data")

x_inf, y_resp, yerr_resp = data_inf[:, 0], data_inf[:, 11], data_inf[:, 12]
y_srv, yerr_srv = data_inf[:, 7], data_inf[:, 8]
y_wait, yerr_wait = data_inf[:, 9], data_inf[:, 10]

plt.figure(figsize=(10, 6))
plt.errorbar(x_inf, y_resp, yerr=yerr_resp, fmt='o', label=r'$T_{Resp} Qlen=\infty$', color='C1', markersize=6)
plt.errorbar(x_inf, y_srv, yerr=yerr_srv, fmt='o', label=r'$T_{Srv} Qlen=\infty$', color='C2', markersize=6)
plt.errorbar(x_inf, y_wait, yerr=yerr_wait, fmt='o', label=r'$T_{Wait} Qlen=\infty$', color='C3', markersize=6)

plt.plot(x_inf, y_resp, label='_nolegend_', color='C1')
plt.plot(x_inf, y_srv, label='_nolegend_', color='C2')
plt.plot(x_inf, y_wait, label='_nolegend_', color='C3')

plt.xlim(0, 0.95)
plt.ylim(0, 1.2)
plt.xlabel(r'${\rho}$', fontsize=12)
plt.ylabel('Time [s]', fontsize=12)
plt.legend(loc='upper left')

plt.savefig("TrespMM1BD.png", dpi=300, bbox_inches='tight')

# Validation
data_inf = np.loadtxt("results/loadcurve_inf.data")

x_inf = data_inf[:, 0]
y_resp = data_inf[:, 11]
yerr_resp = data_inf[:, 12]

theoretical_curve = lambda x: 0.1 / (1 - x)

plt.figure(figsize=(10, 6))
plt.fill_between(x_inf, y_resp - yerr_resp, y_resp + yerr_resp, color='C1', alpha=0.4, label=r'$T_{Resp}\pm\sigma$')
plt.plot(x_inf, y_resp, 'o-', label=r'$T_{Resp}$', color='C1', markersize=6)
x = np.linspace(0.1, 0.9, 400)
plt.plot(x, theoretical_curve(x), label='Theoretical curve', color='C2', linewidth=2)

plt.xlim(0.1, 0.9)
plt.ylim(0, 1.2)
plt.xlabel(r'${\rho}$', fontsize=12)
plt.ylabel('Time [s]', fontsize=12)
plt.legend(loc='upper left')

plt.savefig("TrespMM1Validation.png", dpi=300, bbox_inches='tight')

# Drop rate
x_inf, y_inf, yerr_inf = data_inf[:, 0], 100 * data_inf[:, 3] / data_inf[:, 1], 100 * data_inf[:, 4] / data_inf[:, 1]
x_K10, y_K10, yerr_K10 = data_K10[:, 0], 100 * data_K10[:, 3] / data_K10[:, 1], 100 * data_K10[:, 4] / data_K10[:, 1]
x_K7, y_K7, yerr_K7 = data_K7[:, 0], 100 * data_K7[:, 3] / data_K7[:, 1], 100 * data_K7[:, 4] / data_K7[:, 1]
x_K5, y_K5, yerr_K5 = data_K5[:, 0], 100 * data_K5[:, 3] / data_K5[:, 1], 100 * data_K5[:, 4] / data_K5[:, 1]
plt.figure(figsize=(10, 6))
plt.errorbar(x_inf, y_inf, yerr=yerr_inf, fmt='o', label=r'$Qlen=\infty$', color='C1', markersize=6)
plt.errorbar(x_K10, y_K10, yerr=yerr_K10, fmt='o', label=r'$Qlen=10$', color='C2', markersize=6)
plt.errorbar(x_K7, y_K7, yerr=yerr_K7, fmt='o', label=r'$Qlen=7$', color='C3', markersize=6)
plt.errorbar(x_K5, y_K5, yerr=yerr_K5, fmt='o', label=r'$Qlen=5$', color='C4', markersize=6)

plt.plot(x_inf, y_inf, label='_nolegend_', color='C1')
plt.plot(x_K10, y_K10, label='_nolegend_', color='C2')
plt.plot(x_K7, y_K7, label='_nolegend_', color='C3')
plt.plot(x_K5, y_K5, label='_nolegend_', color='C4')

plt.ylabel('Drop rate [%]', fontsize=12)
plt.legend(loc='upper left')
plt.savefig("DropMM1.png", dpi=300, bbox_inches='tight')

# Utilization
x_inf, y_inf, yerr_inf = data_inf[:, 0], 100 * data_inf[:, 5], 100 * data_inf[:, 6]
x_K10, y_K10, yerr_K10 = data_K10[:, 0], 100 * data_K10[:, 5], 100 * data_K10[:, 6]
x_K7, y_K7, yerr_K7 = data_K7[:, 0], 100 * data_K7[:, 5], 100 * data_K7[:, 6]
x_K5, y_K5, yerr_K5 = data_K5[:, 0], 100 * data_K5[:, 5], 100 * data_K5[:, 6]

plt.figure(figsize=(10, 6))
plt.errorbar(x_inf, y_inf, yerr=yerr_inf, fmt='o', label=r'$Qlen=\infty$', color='C1', markersize=6)
plt.errorbar(x_K10, y_K10, yerr=yerr_K10, fmt='o', label=r'$Qlen=10$', color='C2', markersize=6)
plt.errorbar(x_K7, y_K7, yerr=yerr_K7, fmt='o', label=r'$Qlen=7$', color='C3', markersize=6)
plt.errorbar(x_K5, y_K5, yerr=yerr_K5, fmt='o', label=r'$Qlen=5$', color='C4', markersize=6)

plt.plot(x_inf, y_inf, label='_nolegend_', color='C1')
plt.plot(x_K10, y_K10, label='_nolegend_', color='C2')
plt.plot(x_K7, y_K7, label='_nolegend_', color='C3')
plt.plot(x_K5, y_K5, label='_nolegend_', color='C4')

plt.ylabel('Utilization [%]', fontsize=12)
plt.legend(loc='upper left')
plt.savefig("UtilMM1.png", dpi=300, bbox_inches='tight')

