import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Define K  and find closed-loop poles
K = 600
Kt = 1 # Kt >0.06724
# Define the open-loop transfer function G(s)H(s)
num = [1* K, 3*K]  # (s + 3)
den = [1, 14, K* Kt + 45, 50+ K+K * 3*Kt ,1800]  # (s+10)(s)(s^2+4s+5)

# Create the transfer function
G = ctrl.TransferFunction(num, den)

# Plot the root locus
plt.figure(figsize=(8, 6))
ctrl.root_locus(G)
plt.title(f"Root Locus of the System K = {K}" )
plt.xlabel("Real Axis")
plt.ylabel("Imaginary Axis")
plt.grid()
plt.show()


cl_sys = ctrl.feedback(G, 1)  # Closed-loop system
poles = ctrl.poles(cl_sys)

print("Closed-loop poles:", poles)