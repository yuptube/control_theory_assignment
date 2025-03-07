import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Define the open-loop transfer function G(s)H(s)
num = [1]  # (s + 3)
den = [0.001,1]  # s/100 +1

# Create the transfer function
G = ctrl.TransferFunction(num, den)

# Plot the Bode diagram
plt.figure(figsize=(8, 6))
ctrl.bode(G)
plt.title("Bode Diagram of the System")
plt.xlabel("Frequency (rad/s)")
plt.ylabel("Magnitude (dB)")
plt.grid()
plt.show()