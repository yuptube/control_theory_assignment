import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

class PlotRootLocus:
    def __init__(self, G, K , K_t=None):
        """
        Initialize the system with a given Transfer Function (G).
        """
        if not isinstance(G, ctrl.TransferFunction):
            raise ValueError("Input must be a control.TransferFunction object.")
        
        self.K_t = K_t        
        self.G = G
        self.num, self.den = G.num[0][0], G.den[0][0]  # Extract coefficients
        self.K = K
        

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

        plt.title(f"Root Locus Plot at K = {self.K}")
        plt.xlabel("Real Axis")
        plt.xlim(-20, 5)
        plt.ylabel("Imaginary Axis")
        plt.grid()
        plt.show()

    def plot_step_response(self):
        """
        Plot the step response for a given gain K.
        """
        system = ctrl.feedback(self.G)

        time, response = ctrl.step_response(system)
        
        plt.figure(figsize=(8, 4))
        plt.plot(time, response, label=f"Step Response (K = {self.K})")
        # plt.xlim(-20, 5)
        plt.xlabel("Time (s)")
        plt.ylabel("Response")
        plt.title("Step Response")
        plt.grid()
        plt.show()

    def plot_bode(self):
        """
        Plot the bode
        """
        max_zeta = self.compute_damping_factor()
        plt.figure(figsize=(8, 6))
        ctrl.bode(self.G , display_margins='overlay', dB=True)

        poles=ctrl.poles(self.G)

        freq_at_max_zeta = np.abs(poles[np.argmax(-np.real(poles) / np.abs(poles))])  # Natural frequency
        # Mark the frequency where max damping factor occurs
        plt.axvline(freq_at_max_zeta, color='r', linestyle='--', label=f"Zeta Max @ {freq_at_max_zeta:.2f} rad/s")
        plt.annotate(f"Zeta Max = {max_zeta}", 
                 xy=(freq_at_max_zeta, -3), xycoords="data",
                 xytext=(-50, 30), textcoords="offset points",
                 arrowprops=dict(arrowstyle="->", color="red"), fontsize=10, color="red")
        
        plt.title(f"Bode Diagram of the System with zeta as {max_zeta}")
        plt.xlabel("Frequency (rad/s)")
        plt.ylabel("Magnitude (dB)")
        plt.show()
    
        
    def compute_damping_factor(self):
        """
        Compute the maximum damping factor zeta from root locus with varying K_T.
        """
        poles = ctrl.poles(self.G)
        # print(f"Poles: {poles}")

        # Filter complex poles (nonzero imaginary part)
        complex_poles = poles[np.imag(poles) != 0]
    
        if len(complex_poles) == 0:
            print("No complex poles found.")
            return None  # Return None if no complex poles exist

        sigma = np.abs(np.real(complex_poles))
        n_freq = np.abs(np.imag(complex_poles))
    
        zeta = sigma / n_freq
        max_zeta = np.max(zeta) 

        # print(f"Complex Poles: {complex_poles}, Sigma: {sigma}, Natural Frequency: {n_freq}")
        # print(f"Maximum Zeta: {max_zeta}")

        return max_zeta
     
  
# Example usage
if __name__ == "__main__":
    # Define Transfer Function G
    num = [1, 3]
    den = [1, 14, 45, 50, 3]
    G = ctrl.TransferFunction(num, den)
    K = 1
    # Create and use the PlotRootLocus class
    system = PlotRootLocus(G,K)
    system.compute_damping_factor()