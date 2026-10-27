# Label-specific conditional chi-square: exact low-order diagnostics

2026-10-27 04:54 UTC. No many-program rank-scaling theorem claimed.

For n full Choi programs of the mixed-flag Haar family let Omega_a denote the averaged program+data state. The correct label-independent baseline is

 M_n=(Omega_0+Omega_1+Omega_2)/3
    =E_U[J_U^tensor n] tensor I_(3r)/(3r).

This identity holds because the average of the three logical data states is exactly I_(3r)/(3r) for EVERY U. It retains all program-program correlations instead of mistaking them for label information.

Define the Petz weighted square

 C_n=Tr[(Omega_0-Omega_1) M_n^+ (Omega_0-Omega_1)].

Support is restricted to M_n; Omega_a<=3M_n makes this legitimate. Cauchy-Schwarz implies half trace distance <=sqrt(C_n)/2.

Exact n=1 calculation gives C_1=6/(9r²-1). Numerical Schur-block evaluation at n=2 and n=3 gives, to roundoff,

 C_n=6n/(9r²-1), n=2,3,

for all tested r (2,3,5,10,30,100 at n2;2,3,5,10,30 at n3). These computations use the exact finite Haar Gram matrix d^(cycles(pi^-1 sigma)) and symmetric-group irreducible blocks, not Monte Carlo.

The half-distance coefficients are1/3 for n1, exactly(10+2sqrt3)/27 for n2, and numerically0.603941882754 for n3, each divided by r in the tested range.

These data support linear n/r² growth of LABEL information after cancellation of common program correlations. They do not prove it for n growing with r. In particular the Haar Gram matrix develops representation-support constraints when the tensor order exceeds d=3r; one cannot analytically continue an inverse Gram formula through that change. A useful next proof would control the conditional likelihood operator or the relevant Schur boundary weights up to n of order r². The received collision theorem currently gives only Omega(r).

Files: mixed_flag_two_program_conditional_moment.py/.txt and mixed_flag_three_program_conditional_moment.py/.txt. The n2 characteristic-polynomial calculation is separately preserved; no symbolic general-n formula is asserted.
