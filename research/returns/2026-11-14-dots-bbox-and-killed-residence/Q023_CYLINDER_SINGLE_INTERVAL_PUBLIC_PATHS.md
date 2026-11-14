# Exact single-interval cylinder partition bound

Cylinder height L=1600, width w>=400, exterior minus. Restrict to configurations with ONE NONEMPTY interval of plus spins in each row, with neighboring row intervals overlapping or immediately adjacent (no intervening missing column). This extra condition is essential: disjoint, separated intervals have smaller symmetric-difference boundary than the endpoint variation formula. Write left and right missing lengths l_y,r_y>=0, l_y+r_y<=w-1. Periodic y. Full strip energy is E_full=(16-.04w)L. Exact excess:
 E-E_full=.04 sum_y(l_y+r_y)+8 sum_y(|l_{y+1}-l_y|+|r_{y+1}-r_y|).
Discard the per-row compatibility constraint to factor the relative partition function into two identical nonnegative height-loop sums.

Set q=exp(-.04), t=exp(-8), K_ij=t^|i-j| on nonnegative integers, D_ii=q^i, T=D^(1/2) K D^(1/2). The loop sum is Tr(T^L). K is positive semidefinite (the standard geometric correlation kernel; e.g. its Fourier symbol on Z is (1-t²)/(1-2t cos(theta)+t²)>0). Its operator norm is <=(1+t)/(1-t) by absolute row sums. T is positive trace class, Tr(T)=1/(1-q), and ||T||<=||K||. Hence
 Tr(T^L) <= [(1+t)/(1-t)]^(L-1)/(1-q).
The ADJACENT-OVERLAPPING SINGLE-INTERVAL relative cylinder partition function is therefore at most the square of this quantity, independent of w. At L1600 the logarithm is below8.63 (diagnostic value in companion JSON).

This is a genuine bounded subclass calculation, NOT the full cylinder bound. Missing classes include separated neighboring intervals, empty rows, multiple occupied intervals in a row, and holes. They cannot be discarded from an upper bound. Those need a contour/defect injection with paid entropy. Empty-row phase coexistence at w400 is particularly important; treating it as a dilute local missing-cell gas is invalid.
