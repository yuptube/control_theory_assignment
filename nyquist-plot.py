import numpy as np
from matplotlib import pyplot as plt 
import control

G = control.TransferFunction((1,2,1), (1,0,0,0))
control.nyquist_plot(G)
plt.xlim(-0.3, 0.3)
plt.ylim(-0.3, 0.3)
plt.show()
