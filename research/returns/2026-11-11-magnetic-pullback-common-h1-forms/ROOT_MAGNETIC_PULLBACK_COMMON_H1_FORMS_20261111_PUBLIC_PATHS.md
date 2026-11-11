Magnetic pullback diffusion: a common H1/H2 form with polynomial constants
11 November 2026 Brisbane / 10 November UTC

Scope. This supplies an explicit sufficient common-form contract for the
MAGNETIC conjugated Laplacian used in the temporal-freezing interface.
It is a direct chain-rule and energy calculation, not a full time-varying
MHD compiler, an assertion of novelty of Garding estimates, or a new
execution/audit of an existing producer proof. The previously accepted
constant-parameter work already invokes finite spatial Garding bounds.
Here the fixed H1/H2 spaces, coefficient-difference norm and polynomial
dependence are exposed for the particular vector pushforward operator.

1. Actual operator and fixed spaces.

Work on the ORIGINAL unit three-torus. Let Phi_t be measurable in time
and a smooth volume-preserving diffeomorphism in space, with periodic
lift Phi_t(y+m)=Phi_t(y)+m and det D Phi_t=1. Write
 M(t,y)=D Phi_t(y), N(t,y)=M(t,y)^-1.
Suppose K>=1 bounds EVERY entry of M,N and their spatial derivatives
through order3, uniformly in(t,y). This is a stated geometric envelope,
not an oracle for computing the flow or its derivatives.

Define the actual vector pushforward P_t by
 (P_t b)(Phi_t(y))=M(t,y)b(y),
and the positive conjugated diffusion operator
 L_t=P_t^-1(-Delta)P_t.
It maps smooth divergence-free periodic fields to divergence-free fields:
the volume-preserving change of variables preserves divergence, and the
ordinary Laplacian preserves it. Neither zero mean nor a constant
magnetic input is required for the estimates below.

Use the FIXED spaces
 H=H1(T3;R3) intersect {div b=0},
 V=H2(T3;R3) intersect {div b=0},
with norms
 ||b||H^2=integral(|b|^2+|D b|^2),
 ||b||V^2=||b||H^2+integral|D^2 b|^2,
where D^2 includes all ordered derivatives. Constants belong to both
spaces. The H1 pairing determines the form; no time-dependent weighted
Hilbert norm or assumed H-maximal regularity is used.

2. The principal symbol is scalar despite the vector stretching.

Let C=N N^T. In source coordinates, volume preservation gives
 (Delta_x f)(Phi_t(y))=partial_a(C_ab partial_b(f composed Phi_t)).
For instance this follows directly from the weak Dirichlet form after
the unit-Jacobian change of variables. Applying it componentwise gives
 L_t b=-N partial_a[C_ab partial_b(Mb)].              (1)
Because N M=I, expansion takes the form
 L_t b=-C_ab partial_ab b-B_b partial_b b-Z b,        (2)
where
 B_b=(partial_a C_ab)I+2N C_ab(partial_a M),
 Z=N partial_a(C_ab partial_b M).
Repeated spatial indices are summed. Symmetry of C is used in combining
the two first-order stretching terms.

Since ||M||op<=3K, the scalar principal matrix satisfies
 C>=I/(9K^2).
Elementary finite Leibniz expansions give bounds
 ||C||C2<=c K^2,
 ||B||C1+||Z||C1<=c K^4,                            (3)
with one fixed computable dimensional constant c. Derivatives through
order3 of M,N suffice. The scalar principal symbol is the important
cancellation: vector stretching does not turn its leading matrix into
an indefinite fiber metric.

3. An actual bounded form on H2 and its H1 Garding estimate.

For smooth u,v put
 a_t(u,v)=integral (L_t u) dot v
             +sum_i integral partial_i(L_t u) dot partial_i v.
In the second term integrate the leading third derivative once, and
use (2). All resulting products have at most two derivatives on either
u or v. Thus a_t extends to V times V, with
 |a_t(u,v)|<=C_* K^4 ||u||V ||v||V.                  (4)
Here and below C_* can be chosen as ONE sufficiently large computable
universal constant in dimension3, enlarged between the displayed
bounds once and fixed thereafter. It consists of finite product-rule,
index-counting and Young-inequality constants, not a numerical field
evaluation or a parameter-dependent exponent.

For the real part of a_t(u,u), the leading terms are
 integral C_ab partial_b u dot partial_a u
 +sum_i integral C_ab partial_bi u dot partial_ai u.
Every remaining term is bounded by
 c K^4[||D^2u||2 ||u||H+||u||H^2].
Absorb the first product with Young's inequality using the principal
ellipticity1/(9K^2). This squares the K^4 coefficient and costs a further
K^2, explaining the exponent10 rather than assuming a uniform lower
bound independent of geometry. Including the missing V mass term in
the lower-order allowance yields
 Re a_t(u,u)>=||u||V^2/(100K^2)-C_* K^10||u||H^2.  (5)
The derivation is valid on all V by smooth divergence-free Fourier
approximation. No derivatives of M,N or scalar coefficients IN TIME
appear in(3)--(5).

The constants are genuinely finite and effectively majorizable: there
are only three space and three vector indices, finitely many terms in
the product rule through order3, and products of at most four bounded
matrix/derivative entries before the single Young step. Expanding these
finite formulas once gives a rational universal C_*. The statement
does not require solving a PDE, evaluating a propagator norm or using
an uncharged smooth-coefficient regularity oracle.

4. A comparison of scalar coefficients and geometric references.

Let rho(t),rhotilde(t) belong to[rho_-,rho_+] with0<rho_-<=rho_+<=1.
For the SAME actual P_t, the forms rho(t)a_t,rhotilde(t)a_t have
 alpha=rho_-/(100K^2), omega=C_* rho_+ K^10,
and, if |rho-rhotilde|<=delta,
 |(rho a_t-rhotilde a_t)(u,v)|
 <=C_* K^4 delta ||u||V ||v||V.                     (6)
These are common domains and actual uniform constants, even for merely
measurable time dependence. Lipschitz regularity is needed only to
deduce a small delta from temporal freezing.

More generally suppose another actual volume-preserving reference
Phitilde_t has Mtilde,Ntilde obeying the same K envelope and
 ||M-Mtilde||C3+||N-Ntilde||C3<=zeta.
The finite products in(2)--(3) then give
 |(rho a_t-rhotilde atilde_t)(u,v)|
 <=C_*[K^4 delta+rho_+ K^3 zeta]||u||V||v||V.       (7)
This asserts a comparison WHEN the geometric difference is actually
paid; it does not infer zeta from a coefficient difference or replace
one flow by an unconstructed frozen reference.

Apply the previously derived whole-macro variational energy/adjoint
comparison in ROOT_TIME_VARYING_DIFFUSIVITY_FREEZING_AND_FORM_COMPARISON_
20261111.txt, Section2, on an interval of duration T with omega T<=1.
Equations(5)--(7) give the full-space H1 operator bound
 ||S(T,0)-Stilde(T,0)||H->H
 <=C_*[K^6 delta+rho_+ K^5 zeta]/rho_-.             (8)
One can absorb the fixed factor1200 into the universal C_* once. There
is NO number-of-cells factor. If the SAME geometric reference is used
and rho is Lipschitz with constant Lambda, freezing on cells of maximum
length ell gives delta<=Lambda ell, so(8) has a polynomial ell factor.
The alpha/omega/error constants are proof bounds independent of samples
of the unknown scalar profile; the controller need not observe it.

The abstract variational comparison used here is the energy/adjoint
estimate already derived in the named note from the V' framework. It
does not assert maximal regularity in H. Equations(1)--(7) supply its
previously conditional spatial hypothesis for THIS vector pushforward
diffusion, not for every transformed MHD operator.

5. Costs and limits that still matter.

To use(8) with polynomial physical resources, the actual compiled words
must have a paid polynomial K, geometric comparison zeta, macro duration
cap omega T<=1 and all other error envelopes. Smoothness alone supplies
none of these numerical contracts. Variable-length products of spatial
maps may have exponential derivative growth; it is not silently replaced
by a polynomial K. An explicit fixed word with finite derivatives may
bound K by finite differentiation/composition; a general unknown flow
is not provided as a unit-cost input.

For a time-dependent change of variables the transport/stretching terms
must cancel by the actual induction equation. If an uncancelled
P_t^-1 partial_t P_t term remains, its separate form bounds must be paid;
this note does not erase that term by calling the operator diffusion.
The velocity Leray projection, Lorentz coupling, different actual and
frozen carriers, joint nonlinear reset, transported mean, target writer,
global Duhamel schedule and complete binary/physical compiler costs are
not established here. Constants are included in(8), but no heat gap on
the full space or vanishing constant-column bias follows.

This note changes no scientific question or dispatch body. It provides
one explicit spatial operation for the existing non-autonomous question
while leaving its full all-data/all-disturbance/all-energy-weak unknown
coefficient/unknown-flux endpoint open. No numerical simulation, source
recovery, additional worker, experiment, native retrieval probe or
routine reproof was run.
