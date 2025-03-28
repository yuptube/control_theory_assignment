K = 600 ; % K<143
kt = 0.0717;
kt_max = 0.305386 ;
G=tf([1,3], [1,4, 5]);
D=tf(K, [1, 10]);
I=tf(1, [1, 0]);
system = PlotRootLocus(D,G,I,K,1);
system.plot_bode();
system.plot_root_locus();
system.plot_step_response();
%system.rltool_vis();
