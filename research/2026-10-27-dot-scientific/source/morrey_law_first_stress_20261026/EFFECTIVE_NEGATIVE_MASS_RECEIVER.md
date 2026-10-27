# Effective negative spectral mass evaluation for a compact tensor proposal

Status: analytic/effective interface, pending independent audit; no full numerical objective certificate has been executed.

Use the canonical received S0 and any computable smooth compact tensor correction G=K(H), with a received global operator ceiling M. Inside E change variables x=tZ(θ). The exact objective is

∫_0^1∫ tr[(π²t²A(S0+G)(tZ))_-] dμ dt.

Outside E the integrand is simply tr(G_-), over a known compact support. Every cutoff contribution is included.

## Explicit vertex domination for the canonical field

Write the scaled canonical field π²S0=B+(1-t)K0/t, where

V=J^-1Γe/A, P=I+zn^T/A,
B=sym(V n^T/A)-tr(V n^T/A)I,
K0=(zz^T+2Γ)/A + sym(DV P)-tr(DV P)I.

The source identities give ||Γ/A||op≤1, |z|≤√3, |n|/A≤2/√3, ||J^-1||op=2. Hence |V|≤2√3, ||P||op≤3, and ||B||op≤8. The Jacobian of Γe has three diagonal entries bounded by3 and six off-diagonal entries bounded by1, so its Frobenius norm is at most√33<6. Since |∇A|≤2√3, the quotient derivative gives ||DV||op≤24/A. Therefore

||K0||op ≤ (291/A)+2 <296/A.

Thus the weighted canonical matrix W0=π²t²A S0 obeys

||W0||op ≤8At²+296t(1-t)≤92,

using A≤9/4. Its negative trace is bounded by276.

Exclude four phase squares of radius ρ about the phase vertices, with ρ small enough that they are disjoint. Their Haar mass is4ρ²/π². The canonical negative-mass tail is therefore at most123ρ². In these squares A≤6ρ². The correction contribution is bounded by

3Mπ²∫_0^1t²dt ·6ρ²·4ρ²/π² =24Mρ⁴.

The inequality tr((X+Y)_-)≤tr(X_-)+||Y||nuclear pays the combined tail. Hence an explicit total tail budget is

**123ρ²+24Mρ⁴.**

No actual Brownian density corner asymptotic is used.

## Effective regular-region integration

On the remaining compact phase domain A has a computable positive lower bound. The weighted canonical matrix is regular even at t=0 because its displayed expression is polynomial in t. The correction matrix is computable with a known modulus from its explicit potential. Matrix negative trace is Lipschitz in nuclear norm. Rational interval matrix bounds and exact characteristic-polynomial root isolation therefore give convergent upper/lower cell integrals on the regular compact domain. Refine until their difference meets the requested budget, then add the explicit vertex tail above.

For the two-jet cutoff proposal, the exact radial compiler further gives piecewise polynomial weighted matrices in t (degrees2/20/9 for the chosen beta cutoff). This can eliminate radial transition aliasing. It does not itself price the nonsmooth negative-eigenvalue integral or phase integration.

Outside E, G is continuous on a known compact support. The elliptope is semialgebraic with boundary of volume zero. Rational box subdivision with exact semialgebraic inside/outside decisions and interval integration of tr(G_-) yields convergent bounds; undecided boundary-box volume is explicitly charged by3M and decreases to zero. No density or source value is renormalized.

These steps give a terminating positive-accuracy objective evaluator for any fixed computable compact tensor proposal. The present implementation has only executed exact finite-site and one-ray polynomial primitives; the global evaluator and a near-zero proposal remain to be built. The coarse .849→.750 diagnostic is not upgraded by this theorem.

Scope distinction: the completeness library uses genuinely smooth compact potentials, for which M is directly computable from coefficients and cutoff derivatives. The two-jet collar potential is globally C1/W2,∞ rather than automatically C∞ at the vertices; using it as an additional proposal requires an explicit bound for its tensor ceiling and its own regular-region modulus. Its existential boundedness proof is not a numerical M receipt.
