import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

class PlotRootLocus:
    def __init__(self, G):
        """
        Initialize the system with a given Transfer Function (G).
        """
        if not isinstance(G, ctrl.TransferFunction):
            raise ValueError("Input must be a control.TransferFunction object.")
        
        self.G = G
        self.num, self.den = G.num[0][0], G.den[0][0]  # Extract coefficients

    def compute_centroid(self):
        """
        Compute the centroid (alpha) for asymptotes.
        """
        poles = np.roots(self.den)
        zeros = np.roots(self.num)
        num_poles = len(poles)
        num_zeros = len(zeros)

        if num_poles == num_zeros:
            return None  # No asymptotes if poles == zeros

        alpha = (sum(poles) - sum(zeros)) / (num_poles - num_zeros)
        return alpha.real

    def plot_root_locus(self):
        """
        Plot the root locus and asymptotes.
        """
        plt.figure(figsize=(8, 6))
        ctrl.root_locus(self.G, grid=True)

        # Plot asymptotes
        alpha = self.compute_centroid()
        if alpha is not None:
            angles = [60, 180, 300]  # Degrees
            angles_rad = np.radians(angles)
            asymptote_length = 100

            for angle in angles_rad:
                x_asymp = [alpha, alpha + asymptote_length * np.cos(angle)]
                y_asymp = [0, asymptote_length * np.sin(angle)]
                plt.plot(x_asymp, y_asymp, 'r--', linewidth=1.5, label=f"Asymptote {int(np.degrees(angle))}°")

        plt.title("Root Locus Plot")
        plt.xlabel("Real Axis")
        plt.ylabel("Imaginary Axis")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_step_response(self, K=1):
        """
        Plot the step response for a given gain K.
        """
        G_K = ctrl.TransferFunction([K * coeff for coeff in self.num], self.den)
        system = ctrl.feedback(G_K)

        time, response = ctrl.step_response(system)
        
        plt.figure(figsize=(8, 4))
        plt.plot(time, response, label=f"Step Response (K = {K})")
        plt.xlim(-20, 5)
        plt.xlabel("Time (s)")
        plt.ylabel("Response")
        plt.title("Step Response")
        plt.legend()
        plt.grid()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Define Transfer Function G
    num = [1, 3]
    den = [1, 14, 45, 50, 3]
    G = ctrl.TransferFunction(num, den)

    # Create and use the PlotRootLocus class
    system = PlotRootLocus(G)
    system.plot_root_locus()
    system.plot_step_response(K=2)