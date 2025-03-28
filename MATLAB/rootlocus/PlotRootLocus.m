classdef PlotRootLocus
    properties
        D
        G
        I
        K
        Kt
        Tf
        Ls
    end
    
    methods
        function obj = PlotRootLocus(D, G, I, K, Kt)
            obj.Kt = Kt ;
            obj.D = D;
            obj.G = G;
            obj.I = I;
             
            obj.K = K;
            obj.Tf = obj.get_transfer_function();
            obj.Ls = obj.get_root_locus();
        end
        
        function Tf = get_transfer_function(obj)
            open_loop = obj.D * obj.G * obj.I;
            
            if ~isnan(obj.Kt)
                feedback_path = obj.Kt / obj.I + 1;
                Tf = feedback(open_loop, feedback_path);
            else
                Tf = tf(open_loop);
            end
        end
        
        function Locus = get_root_locus(obj)
            if ~isnan(obj.Kt)
                open_loop = obj.D * obj.G;
                Locus = feedback(open_loop, obj.I);
            else
                open_loop = obj.D * obj.G * obj.I;
                Locus_num = open_loop.Numerator{1} / obj.K;
                Locus_den = open_loop.Denominator{1};
                Locus = tf(Locus_num, Locus_den);
            end
        end
        
        function [alpha, angle_list] = get_asymptotes(obj)
            poles = pole(obj.Ls);
            zeros = zero(obj.Ls);
            diff_num = length(poles) - length(zeros);
            if diff_num <= 0
                error('Invalid pole-zero configuration.');
            end
            alpha = (sum(poles) - sum(zeros)) / diff_num;
            
            angle_list = mod((180 + 360 * (0:diff_num-1)) / diff_num, 360);
        end
        
        function plot_root_locus(obj)
            rlocus(obj.Ls);
            hold on;
            grid off;
            title('Root Locus Plot with Asymptotes');
            xlabel('Real Axis');
            ylabel('Imaginary Axis');
            % Plot Asymptotes
            [alpha, angles] = obj.get_asymptotes();
            asymptote_length = 100; % Length of asymptotes
            for i = 1:length(angles)
                angle_rad = deg2rad(angles(i));
                x_asymp = [real(alpha), real(alpha) + asymptote_length * cos(angle_rad)];
                y_asymp = [0, asymptote_length * sin(angle_rad)];
                plot(x_asymp, y_asymp, 'r--', 'LineWidth', 1.5);
            end
            hold off;
            figure;
        end
        function plot_bode(obj)
            bode(obj.Tf)
            figure
        end
        
        function plot_transfer_function_after_feedback(obj)
            
            rlocus(obj.Tf);
            grid off;
            title('Transfer function after feedback in s-plane');
            xlabel('Real Axis');
            ylabel('Imaginary Axis');
            figure;
        end

        function [complex_part , real_part] = get_zeta(obj )
            poles = pole(obj.Tf);
            complex_poles= poles(imag(poles) ~= 0);
            real_part = real(complex_poles(1));
            complex_part = imag(complex_poles(1));
        end

        %function get_max_zeta(obj)
         %   k_t = 0;
          %  max_zeta = 0;
           % omega_n = 0;
            

            %for i = 1:logspace(-2,3,100)

        function rltool_vis(obj)
            rltool(obj.Tf);
        end

        function plot_step_response(obj)
            [y,t]=step(obj.Tf);
            plot(t,y)
            grid on;
            title(sprintf('Step Response (K = %f)', obj.K));
            xlabel('Time (s)');
            ylabel('Response');

        end
    end
end
