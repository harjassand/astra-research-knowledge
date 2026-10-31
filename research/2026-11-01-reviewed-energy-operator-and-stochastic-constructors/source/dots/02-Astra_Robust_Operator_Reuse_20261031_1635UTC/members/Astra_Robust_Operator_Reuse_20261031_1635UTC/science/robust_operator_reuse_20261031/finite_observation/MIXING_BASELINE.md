# Stronger retained baseline: certified forgetting, not a reduced recurrence

This separate falsification fixture does not modify the frozen reviewed
construction. A long-word-only timing comparison can favor a small recurrence
while overlooking an ordinary method that does almost no recurrence at all.

Let C_a be the same acquired stochastic center matrices and mu the task's
initial probability distribution. Choose the uniform distribution h as a
cheap proposal, and CHECK

    d=min_(a,i,j) C_a[i,j]/h_j,
    xi=max_a ||h^T C_a-h^T||_1.

No exact invariant law or common stationary distribution is asserted. For
d<1 write C_a=d*1*h^T+(1-d)R_a, with R_a stochastic. For any probability nu,

    ||nu^T C_a-h^T||_1
       <= (1-d)||nu-h||_1 + xi.

Indeed (nu-h)^T*1*h^T=0, stochastic R contracts row l1 norm, and h^T C-h^T is
the paid drift. At d=1 the kernel is the reset to h and xi=0. Thus the exact
recurrence D_0=||mu-h||_1, D_(t+1)=min(2,(1-d)D_t+xi) gives a uniform bound
for every sequence, even when the centers have no common equilibrium.

For the same entry boxes and eta_inf as in PROOF.md, a constant answer h^T b
has error at length l at most

    ||b||_infinity * (l*eta_inf + D_l),

plus its paid final scalar rounding. (Centering b can improve the constant;
this test deliberately uses the displayed conservative bound.) Whenever
this meets the tolerance, return the same constant for EVERY word of that
length, after reading/validating its symbols. For other lengths use ordinary
retained full-center integer replay with its existing infinity-norm budget.
The hybrid therefore admits every word of length <=L, not only the easy long
test words. It retains the observed center matrices for fallback; their
storage and any later compilation/application are not discarded from cost.

On the existing 12-state finite-observation fixture, this ordinary comparator
can answer every tested horizon-30 word with zero matrix-vector products.
The precise threshold, bounds and fallback work are in the executable report.
This erases the reduced-rank methods' online advantage for that long-word
batch, even before charging their acquisition. It does not disprove the
two-sided certificate or claim every family mixes rapidly. It identifies an
important strongest-baseline failure of this particular proposed advantage.

Minorization and stochastic contraction are ordinary Markov-chain machinery,
not a historical novelty claim. Every retained Krylov/range/spectral method
may use this hybrid too. The core result remains a sound robust admission
principle; a genuinely new computational advantage is still unestablished.
