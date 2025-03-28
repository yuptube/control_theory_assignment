t = 0:0.01:10; % Define time vector
G=tf([1,3], [1,4, 5])
[y, t] = step(G, t); % Compute step response
disp(t);
plot(t, y); grid on;
xlabel('Time (s)');
ylabel('Response');
title('Step Response');