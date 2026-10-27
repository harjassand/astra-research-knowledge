# Independent parametric two-face contraction audit

PASS, 27 October 2026. Separate quantitative extension of the independently received reduction-region theorem.

For beta>1 use F_beta=beta logdet NX−logdet X−(beta−1)logdet EX. Coefficients sum to zero, so reference-congruence invariance is exact. On EM=I the derivative is beta N((NM)^−1)−M^−1−(beta−1)I. The same compact two-face KKT calculation gives G_beta=cES_plus−S_plus−epsilon ES_minus+S_minus, with no beta-dependent multiplier term. This follows from functional congruence invariance, not a feasible-path assumption.

Actual inverse Jensen yields f_beta(M), where independently expanded f_beta(m)=(m−1)[3−(beta−1)m]/[m(m+3)]. For 1<c<3/(beta−1), the upper normal is excluded by the same corner-Schwarz pairing and positive f_beta(c). With upper normal zero, each m>1 eigenvector has nonpositive gradient expectation from the lower normal, contradicting positive f_beta(m). Thus I is the unique compact minimum. The usable range implicitly has beta<4; beta=1+3/k with k>1 always satisfies it.

For original X<=k tau and tau=EX, every s>0 actual resolvent head M_s=(tau+sI)^−1/2(X+sI)(tau+sI)^−1/2 is positive, has EM_s=I, and is STRICTLY below kI since k(tau+sI)−(X+sI)>=(k−1)sI. Select individual compact bounds around each such head. Exact Bregman subtraction gives D_in−beta D_out=integral F_beta(M_s), not a comparison after whitening entropy. Linear terms vanish individually, support restriction is legitimate, and singular sources have integrable logarithmic lower endpoint and O(s^-2) tail. For X!=tau all heads are nonidentity and all integrands strictly positive.

Consequently D_out<k/(k+3) D_in for every nonidentity source with peak<=k, in any finite reference. For 1<k<3, Delta>=(3−k)/(k+3) D_in (indeed strict away from identity), yielding coefficient1/4 at k=9/5. At k=3 this gives whole reduction-region positivity. For k>3 contraction remains valid but does not imply VALUE. This is source-relative to the actual marginal tau, not an arbitrary pairwise channel contraction. The exact scalar/constants checker was independently replayed without mutating its frozen JSON and matched exactly.
