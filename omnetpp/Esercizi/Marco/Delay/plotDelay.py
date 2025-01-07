#!/usr/bin/python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
import matplotlib as mpl
import matplotlib.colors as mc
from plots import plot_line, set_fonts

mu=10
lam=10
ts=0.1
delta=0.1

def theoretical(fl):
    return fl/(mu - lam * fl) + (1-fl)*(delta + 1/mu)
    

if __name__ == "__main__":
    #set_fonts()
    # plot respone time
    fig, ax = plt.subplots()
    ax.set(xlabel='$x$', ylabel='Time [s]')
    plot_line(ax, 'o--', 'results/esame_delay.data', 'Response Time', '#frac', 'avgResponseTime', 'sigma(avgResponseTime)')
    pts=[x for x in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]]
    plot_line(ax, '-', None, 'Theoretical Curve', pts, [theoretical(x) for x in pts])
    plt.legend()
    plt.savefig('sample.png')
    plt.show()

