import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

class PlotRootLocus:
    def __init__(self, D,G,I, K, Kt=None):
        """
        Initialize the system with a given Transfer Function (G).
        """
        if not isinstance(G, ctrl.TransferFunction):
            raise ValueError("Input must be a control.TransferFunction object.")
        self.Kt = Kt
        self.D = D        
        self.G = G
        self.I = I
        self.K = K
        self.Tf=self.get_transfer_function()
        self.Ls=self.get_root_locus()
    def get_transfer_function(self):
        # Open-loop transfer function (Forward Path)
        open_loop = self.D * self.G *self.I

        # Total feedback path (sum of I(s) and Kt)
        if self.Kt is not None:
            feedback_path = self.Kt / self.I +1
            Tf = ctrl.feedback(open_loop,feedback_path)  
            return Tf
        

        Tf = ctrl.feedback(open_loop)
        return Tf
    
    def get_root_locus(self):
        # Open-loop transfer function (Forward Path)
        if self.Kt is not None:
            open_loop = self.D * self.G 
            Locus = ctrl.feedback(open_loop, self.I )
            return Locus

        open_loop = self.D * self.G *self.I
        print(f"Open-loop transfer function: {open_loop} ")
        Locus_num = open_loop.num[0][0] / self.K
        Locus_den = open_loop.den[0][0]
        Locus = ctrl.TransferFunction(Locus_num, Locus_den)

        print(f"Closed-loop transfer function: {Locus} , K = {self.K}")
        return Locus


    def get_ayampototes_angle_and_alpha(self):
        """
        Compute the centroid (alpha) for asymptotes.
        """
        poles, zeros = ctrl.poles(self.Ls), ctrl.zeros(self.Ls)
        diff_num = len(poles) - len(zeros)
        assert diff_num > 0
        alpha = (sum(poles) - sum(zeros)) / diff_num
        
        angle_list = []
        
        for n in range(diff_num):
            angle = (180 + 360 * (n)) / diff_num
            angle_list.append(angle % 360)  # Ensure angles are within [0, 360)
        return alpha.real , angle_list
       

    def plot_root_locus(self):
        """
        Plot the root locus and asymptotes.
        """
        ctrl.root_locus(self.Ls, grid=False)

        # Plot asymptotes
        alpha , angle_list = self.get_ayampototes_angle_and_alpha()
        if alpha is not None:
            angles = angle_list  # Degrees
            angles_rad = np.radians(angles)
            asymptote_length = 100

            for angle in angles_rad:
                x_asymp = [alpha, alpha + asymptote_length * np.cos(angle)]
                y_asymp = [0, asymptote_length * np.sin(angle)]
                plt.plot(x_asymp, y_asymp, 'r--', linewidth=1.5, label=f"Asymptote {int(np.degrees(angle))}°")
        
    
    def plot_transfer_function_after_feedback(self):
        """
        Plot the root locus and asymptotes.
        """
        plt.figure(figsize=(8, 6))
        ctrl.root_locus(self.Tf, grid=False)

        if self.Kt is not None:
            plt.title(f"Root Locus Plot at K = {self.K} , Kt = {self.Kt}")
        else:
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

        time, response = ctrl.step_response(self.Tf)
        
        plt.figure(figsize=(8, 4))
        plt.plot(time, response, label=f"Step Response (K = {self.K})")
        # plt.xlim(-20, 5)
        plt.xlabel("Time (s)")
        plt.ylabel("Response")
        plt.title("Step Response")
        plt.grid()
        plt.show()

    def vis_max_zeta_plot_bode(self ):
        """
        Plot the Bode magnitude and phase plots, marking max zeta frequency.
        """
        poles = ctrl.poles(self.Tf)
        max_zeta ,freq_at_max_zeta  = self.compute_damping_factor(poles)
        
        mag, phase, omega = ctrl.frequency_response(self.Tf)
        # Create figure with two subplots
        fig, ax = plt.subplots(2, 1, figsize=(8, 6))

        # Plot magnitude response
        ax[0].semilogx(omega, 20 * np.log10(mag), label="Magnitude Response", linewidth=2)
        ax[0].set_ylabel("Magnitude [dB]")
        ax[0].grid(True)
        ax[0].set_title("Bode Diagram")

        if max_zeta is not None:
            # Mark the frequency where max zeta occurs
            ax[0].axvline(freq_at_max_zeta, color='r', linestyle='--', label=f"Zeta Max @ {freq_at_max_zeta:.2f} rad/s")
            
            # Annotate max zeta on magnitude plot
            ax[0].annotate(f"Zeta Max = {max_zeta:.5f}",
                           xy=(freq_at_max_zeta, -10), xycoords="data",
                           xytext=(-50, 30), textcoords="offset points",
                           arrowprops=dict(arrowstyle="->", color="red"), fontsize=10, color="red")

        # Plot phase response
        ax[1].semilogx(omega, phase, label="Phase Response", linewidth=2)
        ax[1].set_ylabel("Phase [deg]")
        ax[1].set_xlabel("Frequency [rad/s]")
        ax[1].grid(True)
        plt.show()

    def compute_max_damping_factor(self, K_range=np.logspace(-3, 3, 100)):
        """
        Compute the maximum damping factor zeta from root locus with varying K_T.
        """
        max_zeta = 0.0
        best_KT = 0.0
        open_loop_tf = self.D * self.G * self.I
        omega_n = 0
        
        for K_T in K_range:
            
            # Apply K_T in the feedback path
            feedback_path = K_T / self.I + 1
            Tf = ctrl.feedback(open_loop_tf, feedback_path)
            poles = ctrl.poles(Tf)
            # Filter complex poles (nonzero imaginary part)
            complex_poles = poles[np.imag(poles) != 0]
            # Compute damping factor for complex poles
            for pole in complex_poles:
                    zeta , omega_n = self.compute_damping_factor(pole)  # Fix here, don't return K_T
                    if zeta > max_zeta:
                        max_zeta = zeta
                        best_KT = K_T # Store corresponding K_T
                        omega_n = omega_n


        return max_zeta, best_KT  ,omega_n
     
    def compute_damping_factor(self , poles):
        """
        Compute the maximum damping factor zeta from root locus with varying K_T.
        """
        complex_pole=poles[np.imag(poles) != 0]
        sigma = np.abs(np.real(complex_pole))
        d_freq = np.abs(np.imag(complex_pole))
        omega_n = np.sqrt(sigma**2 + d_freq**2)
        zeta =  sigma / omega_n
         
        assert np.max(zeta) < 1  
        # print(f"Complex Poles: {complex_pole}, Sigma: {sigma}, Natural Frequency: ")
        # print(f"Maximum Zeta: {zeta}")
        # print(f"Maximum d_freq: {d_freq}")


        return np.max(zeta) , np.max(omega_n)
    
    def step_response_approx(zeta, wn):

        if zeta >= 1:
            raise ValueError("This function is valid only for underdamped systems (zeta < 1).")
    
        # Compute derived parameters
        wd = wn * np.sqrt(1 - zeta**2)  # Damped natural frequency

        # Rise time (approximate for 10%–90% response)
        tr = (np.pi - np.arccos(zeta)) / wd

        # Peak time
        tp = np.pi / wd

        # Settling time (time to reach ±1% of final value)
        ts = 4 / (zeta * wn)

        # Maximum overshoot
        Mp = np.exp(-np.pi * zeta / np.sqrt(1 - zeta**2))

        # Create transfer function: G(s) = wn^2 / (s^2 + 2*zeta*wn*s + wn^2)
        num = [wn**2]
        den = [1, 2*zeta*wn, wn**2]
        G = ctrl.TransferFunction(num, den)
         # Compute step response
        t, y = ctrl.step_response(G)

        # Plot step response
        plt.figure(figsize=(8, 5))
        plt.plot(t, y, label="Step Response", linewidth=2)
        plt.axhline(1, color='gray', linestyle="--", label="Final Value")

        # Mark time-domain specifications
        plt.scatter(tr, 0.9, color='r', marker='o', label=f"Rise Time: {tr:.2f}s")
        plt.scatter(tp, 1 + Mp, color='g', marker='o', label=f"Peak Time: {tp:.2f}s")
        plt.axhline(1 + Mp, color='g', linestyle="--", label=f"Overshoot: {Mp*100:.1f}%")
        plt.axvline(ts, color='m', linestyle="--", label=f"Settling Time: {ts:.2f}s")

        plt.xlabel("Time (s)")
        plt.ylabel("Response")
        plt.title("Step Response ")
        plt.grid(True)
        plt.show()

        return {
            "Rise Time (tr)": tr,
            "Peak Time (tp)": tp,
            "Settling Time (ts)": ts,
            "Overshoot (Mp)": Mp
        }

    
  
# Example usage
if __name__ == "__main__":
    # Define Transfer Function G
# Define K  and find closed-loop poles
    K = 600 # K<143
    kt = 0.0717
    kt_max = 0.305386 
    G=ctrl.TransferFunction([1,3], [1,4, 5])
    D=ctrl.TransferFunction([K], [1, 10])
    I=ctrl.TransferFunction([1], [1, 0])
    # Create and use the PlotRootLocus class
    system = PlotRootLocus(D,G,I,K)
    _ , _ , omega_n = system.compute_max_damping_factor()
    print(f"omega_n is {omega_n:.6f} "   )
    system.plot_root_locus()
    # print(system.get_ayampototes_angle_and_alpha())
    print(system.get_root_locus())
    system.vis_max_zeta_plot_bode()
    system.plot_step_response()
    system.plot_transfer_function_after_feedback()

    # system.vis_max_zeta_plot_bode()
    # print(system.vis_max_zeta_plot_bode())
    # zeta , freq_at_max_zeta = system.compute_max_damping_factor()
    # print(f"max zeta is {zeta:.6f} , freq_at_max_zeta is {freq_at_max_zeta:.6f}"   )
    # max_zeta , bestKT = system.compute_max_damping_factor()
    # print(f"max zeta is {max_zeta:.6f} , bestKT is {bestKT:.6f}"   )