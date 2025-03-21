import numpy as np
from matplotlib import pyplot as plt
import control as ctrl

K = 1
num = [1 * K, 3 * K] if K != 0 else [1]
den = [1, 14, 45, 50 + K, 3 * K]

# Compute roots of the denominator (characteristic equation)
poles = np.roots(den)
zeros = np.roots(num)
num_poles = np.size(poles)
num_zeros = np.size(zeros)

# Calculate the centroid (alpha)
alpha = (sum(poles) - sum(zeros)) / (num_poles - num_zeros)

print(f"Number of Poles: {num_poles}, Number of Zeros: {num_zeros}")
print(f"Centroid (Alpha): {alpha}")

G = ctrl.TransferFunction(num, den)

# Plot the root locus
plt.figure(figsize=(8, 6))
ctrl.root_locus(G, grid=True)

# Plot asymptotes
angles = [60, 180, 300]  # degrees
angles_rad = np.radians(angles)

# Define a range to extend the asymptotes
asymptote_length = 15

for angle in angles_rad:
    x_asymp = [alpha.real, alpha.real + asymptote_length * np.cos(angle)]
    y_asymp = [0, asymptote_length * np.sin(angle)]
    plt.plot(x_asymp, y_asymp, 'r--', linewidth=1.5, label=f"Asymptote {np.degrees(angle)}°")

plt.title(f"Root Locus of the System (K = {K})")
plt.xlabel("Real Axis")
plt.ylabel("Imaginary Axis")
plt.xlim(-20, 5)
plt.grid()
plt.show()