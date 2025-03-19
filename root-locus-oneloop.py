import numpy as np
from matplotlib import pyplot as plt 
import control as ctrl

K = 600
num = [1* K, 3*K] if K != 0 else [1]
den = [1, 14, 45, 50 +K, 3*K ]

# Compute roots of the denominator (characteristic equation)
roots = np.roots(den)
print("Roots of the characteristic equation:", roots)
G = ctrl.TransferFunction(num, den)
# Plot the root locus
plt.figure(figsize=(8, 6))
ctrl.root_locus(G)
plt.title(f"Root Locus of the System K = {K}" )
plt.xlabel("Real Axis")
plt.xlim(-12,5)
plt.ylabel("Imaginary Axis")
plt.grid()
plt.show()