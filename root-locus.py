import numpy as np
from matplotlib import pyplot as plt 
import control

# root locus plot

G = control.TransferFunction((1, 1), (1, 9, 28, 40,0))

control.rlocus(G , grid=False)

plt.show()