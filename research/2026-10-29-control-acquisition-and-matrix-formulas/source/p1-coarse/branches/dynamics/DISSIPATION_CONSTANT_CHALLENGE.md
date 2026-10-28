# Sharpness of the dissipation-weighted constant 2

28 October 2026. Actual paired defects and their own coefficient trajectories
attain the factor 2 asymptotically. It is not solely an arbitrary-input
kernel constant.

Take physical H=R, A=a in (0,1), b=1; q=N, W=I, and actual word columns
V=(a^(N-1),...,1). Let T=S be the backward shift T e_0=0,
T e_j=e_(j-1), and let c=k(1,...,1), k=(1-a)/(1-a^N). Then Vc=b.
Exactly,

\[
R=I-T^TT=e_0e_0^T,\quad D=AV-VT=J=A^TV-VS=a^N e_0^T,
\quad\theta_f^2=\theta_b^2=\frac{a^{2N}}{1-a^2}.
\]

Both weighted inequalities are equalities and both range conditions hold.
For N repeats of A, every trajectory-applied forward or backward defect is
a^N k. Both coefficient energy losses equal ||c||^2=Nk^2, because
T^Nc=S^Nc=0. This also saturates the sharper finite-loss budgets.

The actual signed-corrected remainder is

\[
\mathcal E_N=a^{2N}k^2\sum_{j=0}^{N-2}(N-1-j)a^j,
\qquad
\frac{\mathcal E_N}{\theta_f\theta_b\|c\|^2}
=(1+a)\left[1-\frac{1-a^N}{N(1-a)}\right].
\]

This equals the true output a^N minus the signed-corrected prediction.
With a=1-1/n and N=n^2, the ratio is at least
(2-1/n)(1-1/n), tending to 2. All quantities are rational.
No universal constant below 2 can hold under the stated hypotheses.

The scalar Gram is singular, as permitted by the no-Gram-floor assumptions.
The initial c is a valid source representation, although not the canonical
empty-word coordinate. A full-rank extension is recorded below.

The independent checker is check_dissipation_sharpness.py; its output is
DISSIPATION_SHARPNESS_RESULTS.json. Precision needed to acquire a small theta
remains a cost. These examples establish a mathematical constant, not an
operational advantage.

## Nonsingular dictionaries also approach 2

Take physical H=R^N, A=diag(a_l) with N distinct a_l in (0,1), and b
with nonzero coordinates. For k>0 define

\[
z=\left[k\sum_{r=0}^{N-1}A^r\right]^{-1}b,\qquad
V_j=A^{N-1-j}z,\quad c=k(1,\ldots,1)^T.
\]

Then Vc=b and V is nonsingular by the Vandermonde determinant.
Keep W=I and the same T=S. The paired defects are
D=J=d e_0^T, d=A^N z, and the exact common constant is
theta^2=d^T(I-A^2)^-1d.

The normalized actual remainder is a positive weighted average of
R_N(a_l)=(1+a_l)[1-(1-a_l^N)/(N(1-a_l))], with weights proportional to
d_l^2/(1-a_l^2). For N=n^2 and all eigenvalues between 1-2/n and 1-1/n,
the ratio is at least (2-2/n)(1-1/n), tending to 2. Normalize the physical
source with b_l=1/n.

For actual preparation words, choose k=[sum_r(1-2/n)^r]^-1.
Then K=[k sum_r A^r]^-1 is a positive contraction, z=Kb, and each column
is the word image A^(N-1-j)K b. K is a calibration preparation here;
the certified future language contains only A. No dissipation certificate
for future uses of K is claimed.

The Vandermonde Gram can remain poorly conditioned. A fixed Gram floor,
W equal to the physical Gram, canonical initial coordinates, or Galerkin
reduced maps would add assumptions absent from the theorem being checked.
