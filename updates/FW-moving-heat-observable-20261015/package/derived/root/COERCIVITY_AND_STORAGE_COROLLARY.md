# A stronger coercivity constant and its storage interface

15 October 2026. Internal deduction from the new universal sharp QC theorem.
External mathematical review, historical priority, and practical solver advantage
remain UNKNOWN. Existing source proofs are preserved, not overwritten.

For delta<0 and the two PSD conditions, write

    F=lambda J_rho+(gamma-lambda)j²+nu H,
    nu=alpha-delta²/[8(2beta+delta)]>=0.

The first two terms are quasiconvex. With C A=(a-d,b+c), H(A)=|C A|⁴.
For every x,h in R² the fourth-power Bregman inequality is

    |x+h|⁴-|x|⁴-4|x|²x·h >= |h|⁴/3.

For example, subtracting the right side leaves
6(x·h+|h|²/3)²+2(|x|²|h|²-(x·h)²), which is nonnegative. After applying
this inequality at C B and integrating, the linear term vanishes for a
zero-boundary perturbation. Thus the affine Jensen gap of F is at least
(nu/3) integral |C Dphi|⁴.

For f=phi1+i phi2, 2 barpartial f=C Dphi. The complex-valued Beurling bound
||B||_{L4->L4}<=sqrt(24) gives

    ||Dphi||_4² <= (25/2)||C Dphi||_4²,
    integral |Dphi|⁴ <= (625/4) integral |C Dphi|⁴.

This is the proved nonsharp bound from Bañuelos–Janakiraman, Theorem1.1,
https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf . No conjectural
sharp transform norm is used. Zero extension and approximation cover bounded
Lipschitz W0^(1,4) data; periodic cutoff/transference gives the periodic and
zero-end strip statements used by the inherited storage theorem. Consequently

    integral [F(B+Dphi)-F(B)] >= (4nu/1875) integral |Dphi|⁴.

At nu=0 this argument supplies no positive constant. Indeed subtracting
epsilon H from J_r violates its second acoustic contact. A positive constant
by a different argument is not ruled out.

## Exact improvement for the earlier Heat18 quartic G

G=3H+(35/24)u²+j²-(5/2)uj=J_(-5/2)+(9/8)H. Therefore

    integral [G(B+Dphi)-G(B)] >= (3/1250) integral |Dphi|⁴.

The new constant3/1250 is exactly6000 times the previous1/2500000.
The same new constant holds uniformly for every supplied alpha3 family
member r∈[-21/8,-5/2], because alpha*(r)<=15/8. This is not an optimality
claim for the coercivity constant.

## Receiving interface: current N866 storage computability

PR98, inspected at8a1e001ac128468ae8d151c9a859b89ef3b9a664, preserves the
source-derived G finite-horizon and buffered spatial construction. Its horizon
proof uses the affine Jensen constant gamma to control near-minimizer gradients.
G itself, its coefficient growth bounds, endpoint conventions and its existing
Heat18 global periodic diffusion are unchanged. Hence the improved gamma can
replace the old lower bound in those numerical budget inequalities; no transfer
to a different quartic or silently changed fixed diffusion is required.

For its actual example U=(cos y,sin y), B=0, M=224 and horizon target0.001:

    old gamma=1/2500000, new gamma=3/1250,
    new R⁴=(2M+1)/gamma=561250/3<21⁴,
    new E*=2M/gamma=560000/3,
    horizon error <=6960 E* (N-1)^(-3/4).

The integer N=10^17 satisfies the same source horizon-error test, verified by
raising it to the fourth power with exact rational arithmetic. The published
loose sufficient choice was10^22 with R<184. This is an improvement in a
sufficient horizon/gradient budget, not an optimal horizon, a lower bound on
all methods, or an executed storage computation. The full spatial cutoff/grid
has not been reoptimized or enumerated here. The source's already enormous
grid does not become a practical solver merely from a stronger constant.

The finite-observation critical-tail obstruction is unchanged. Effective
endpoint coefficients/tails, numerical enclosures, and the rest of N866's
cost contract remain required. The sharp boundary J_r alone does not meet
this coercivity input by the displayed argument.
