import numpy as np
from matplotlib import pyplot as plt 
import control

# root locus plot
# assignment one
G = control.TransferFunction((1, 3), (1, 14, 45, 50 , 0))
# G = control.TransferFunction((1,1), (1, 0,0))
control.rlocus(G , grid=False)
plt.show()