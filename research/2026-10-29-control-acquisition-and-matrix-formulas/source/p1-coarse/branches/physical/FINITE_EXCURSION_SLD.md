# Finite excursions, soft energy constraints, and effective SLD comparison

Research continuation, 28 October 2026. This is an ordinary derivation, with
floating-point diagnostics separated from the proof. No historical priority or
efficient practical algorithm is claimed.

## Result and opportunity judgment

A mean-energy limit on an untouched quantum reference does **not** make exact
complete SLD channel order decidable. Any finite violating experiment can be
diluted into a sufficiently rare high-energy sector. Its absolute signal becomes
small but its sign survives. This is a direct consequence of Astra's accepted
N675 result, not a re-audit or a strengthening of its reduction.

There is a useful constructive counterpart. If an experiment supplies a finite
physical excursion, represented by two actual endpoint states, then an
**absolute** channel-comparison margin admits a computable reference cutoff.
For a reference with number Hamiltonian, mean endpoint energy at most E,
excursion a>0, and desired score error epsilon, retaining reference levels below

    Lambda >= max(1, 144 E/(a^4 epsilon^2))

suffices. This establishes computability of a bounded finite-excursion score
with an explicit cutoff. It does not make the optimization efficient, acquire
the channels, or establish a physical advantage. The underlying SLD variational
formula, measured triangular discrimination, gentle truncation, and finite
semialgebraic optimization are established ingredients. The actual addition
here is their resource-qualified composition and the accompanying exact-order
versus fixed-margin distinction.

This is useful foundational hygiene and possibly a module for operational
channel comparison. It is not presently a sufficient central opening for the
civilisational mission. A stronger route would need either an efficient
dimension-independent optimizer on a scientifically important channel family,
or an experimentally acquired contract that enables this cutoff without full
channel characterization.

## 1. Definitions

Let P,Q be finite-dimensional quantum channels with common input A. A reference
R is untouched. For positive rho and Hermitian H supported on supp(rho), define

    J_rho(X) = (rho X + X rho)/2,
    g_rho(H) = Tr[H J_rho^{-1}(H)].

The inverse is on the relevant support. Equivalently, take a Hermitian SLD L
satisfying J_rho(L)=H and put g=Tr(HL). Its value is independent of a choice on
the common nullspace.

Fix a physical excursion a>0. An admissible experiment has two density operators

    alpha = rho+aH, beta = rho-aH.

Thus rho=(alpha+beta)/2, H=(alpha-beta)/(2a), and

    -rho/a <= H <= rho/a.

For a channel Phi, write

    S_Phi(alpha,beta;a) = g_{Phi_R(rho)}(Phi_R(H)).

It lies in [0,a^-2]. Multiplying by a^2 gives measured quantum triangular
discrimination, with the convention TD(p,q)=1/2 sum (p-q)^2/(p+q).

The two-channel score is

    Delta(alpha,beta;a) = S_Q(alpha,beta;a)-S_P(alpha,beta;a).

We study an absolute additive margin. Dividing this score by an arbitrarily
small baseline changes the problem and voids the fixed-margin conclusion.

For a concrete effective reference let R=ell^2(N_0), with energy operator

    K_R = sum_{j>=0} j |j><j|.

Both endpoint states obey Tr(alpha K_R),Tr(beta K_R)<=E. Finite-support
experiments suffice for the exact-order reduction; infinite-dimensional
extensions of the cutoff use trace-norm limits and the bounded variational
formula below. Other known discrete Hamiltonians work if their finite energy
counting function is computable; the dimension is the number of retained energy
levels, not the numerical cutoff energy itself.

## 2. Bounded variational representation

**Lemma 1.** If -rho/a<=H<=rho/a, there is an SLD L with ||L||op<=1/a, and

    g_rho(H) = max_{X=X*, ||X||op<=1/a}
                [2 Tr(HX)-Tr(rho X^2)].

**Proof.** First suppose rho>0. The Lyapunov inverse has the positive integral

    J_rho^{-1}(H) = 2 integral_0^infty exp(-t rho) H exp(-t rho) dt.

Applying this positive map to -rho/a<=H<=rho/a and using
J_rho^{-1}(rho)=I gives -I/a<=L<=I/a. Completing the square gives, for Hermitian
X,

    2 Tr(HX)-Tr(rho X^2)
       = g_rho(H)-Tr[rho (X-L)^2] <= g_rho(H).

The maximizer L is in the stated ball. For singular rho restrict to its support
and take L=0 on the kernel. The relative bound forces H to vanish on the kernel,
including its cross blocks. This proves the statement. The bound g<=a^-2
follows from g=Tr(rho L^2). QED.

**Corollary 1 (state/tangent continuity).** For two relative-bounded pairs
(rho,H),(sigma,K) with the same a,

    |g_rho(H)-g_sigma(K)|
      <= 2 ||H-K||_1/a + ||rho-sigma||_1/a^2.

This follows by evaluating each variational functional at the other maximizer.
No smallest eigenvalue appears. The relative tangent bound replaces that
conditioning cost.

**Corollary 2 (endpoint continuity, sharper for the present use).** For density
operators alpha,beta,alpha',beta',

    |S_id(alpha,beta;a)-S_id(alpha',beta';a)|
       <= (||alpha-alpha'||_1+||beta-beta'||_1)/a^2.

**Proof.** Set Y=aX. The variational formula is

    a^2 S_id = max_{-I<=Y<=I}
       Tr[alpha (Y-Y^2/2)] + Tr[beta (-Y-Y^2/2)].

Each coefficient has spectrum in [-3/2,1/2]. Since the difference of two
density operators has trace zero, add I/2 to either coefficient; the resulting
operator norm is at most one. Taking the difference of the two suprema proves
the bound. The same result after an arbitrary channel follows from trace-norm
contractivity. QED.

The endpoint representation makes the relation with established measured
triangular discrimination explicit. It should not be marketed as a new
information divergence.

## 3. Effective energy cutoff

Let P_Lambda be the reference projection onto energies <Lambda, Q_Lambda=I-P.
Take Lambda>=1. Define a CPTP compression, acting only on R, by

    Gamma_Lambda(tau) = P tau P
       + Tr_R[Q tau Q] tensor |0><0|.

The second term means that high-energy reference weight is reset to the actual
ground level while its A marginal is retained. The output reference has
dimension ceil(Lambda). No freely supplied new physical flag is needed. Energy
cannot increase. This channel is a mathematical witness reduction; actually
performing it on a device is a separate preparation operation.

For either endpoint tau with mean reference energy at most E, Markov's
inequality gives tail weight p_tau=Tr(Q tau)<=E/Lambda. The gentle projection
bound and the trace p_tau of the replacement term give

    ||tau-Gamma_Lambda(tau)||_1 <= 2 sqrt(p_tau)+p_tau.

Let p=min(1,E/Lambda) and delta=2 sqrt(p)+p. Since reference compression commutes
with each local channel,

    |Delta(alpha,beta;a)
       -Delta(Gamma_Lambda alpha,Gamma_Lambda beta;a)|
       <= 4 delta/a^2 <= 12 sqrt(p)/a^2.             (1)

Thus Lambda>=max(1,144 E/(a^4 epsilon^2)) makes the right side at most epsilon.
For E=0 the reference is already in the ground level.

If V_E(a) is the supremum of the positive part of Delta over all admissible
endpoints and V_{E,Lambda}(a) is the same supremum on the retained reference,
then

    0 <= V_E(a)-V_{E,Lambda}(a) <= 4 delta/a^2.

The lower inequality follows by embedding low-energy experiments in the full
reference. The upper one follows by compressing every admissible experiment;
the compressed endpoints remain normalized and retain the energy constraint.

**Computability consequence.** Suppose channel matrices and retained energies
are rational, and E,a,epsilon are positive rationals. The finite-dimensional
optimization can be expressed over real and imaginary density-matrix entries
and SLD matrices. Density positivity is semialgebraic, channel action is linear,
J_rho(L)=H is bilinear, and Tr(HL) is polynomial. Include -I/a<=L<=I/a. Real
quantifier elimination therefore computes the finite supremum to any rational
accuracy. Equation (1) supplies the computable omitted-tail modulus. This is a
termination argument, not an efficient implementation. Its PSD variable count
already grows quadratically with input dimension times the cutoff dimension;
general quantifier elimination is an extremely strong, often unusable baseline.

If channels are unknown, the argument has not acquired them. If known estimates
satisfy ||P-P_hat||diamond<=eta and ||Q-Q_hat||diamond<=eta, Corollary 2 gives
uniform score error at most 4 eta/a^2. Standard process tomography is an equally
informed route for obtaining such estimates when its preparation/readout access
is actually available. No query, precision, or physical-time saving is asserted.

## 4. Exact comparison stays undecidable at every positive energy budget

**Proposition.** For any fixed E>0 and fixed a>0, universal exact nonpositivity
of Delta over the energy-bounded endpoint class is equivalent to unrestricted
complete SLD dominance. Consequently the generic rational POVM decision problem
retains the undecidability supplied by accepted N675.

**Proof.** One direction is immediate because bounded-energy endpoint tests are
a subclass of complete tests. For the other direction, suppose a finite
reference r, a faithful rho, and a traceless Hermitian H give a strict violation.
Rescale H by a positive t small enough that rho+-a t H are density operators.
The score difference scales by t^2 and remains strictly positive.

Embed the r-dimensional reference in levels 1,...,r. Let mu_A be any faithful
state, use ground level 0 as a separate block, and define

    alpha_tilde = (1-p) mu_A tensor |0><0| + p alpha_bad,
    beta_tilde  = (1-p) mu_A tensor |0><0| + p beta_bad,

with 0<p<min(1,E/r). Both endpoint energies are <=pr<E. Channel action respects
the reference blocks. The low block has zero tangent. Homogeneity of the SLD
metric gives Delta_tilde=p Delta_bad>0. Therefore every unrestricted failure
has an energy-bounded failure. The construction can also force arbitrarily
small distance from the fixed ground product state. QED.

There is no contradiction with the computable fixed-margin result: dilution
shrinks the absolute margin, and exact comparison would require deciding
whether the computable nonnegative optimum equals zero. Equality of a
computable real with zero is not generally decidable. A fixed physical
excursion does not by itself supply a positive signal margin.

## 5. Diagnostics and unresolved next attack

`finite_excursion_sld.py` executes 240 seeded floating-point cases with two
random local quantum channels, noncommuting reference states, ranks varying
from one to full, varying reference dimension and finite excursion. It checks
the SLD operator bound, data processing under reference compression, endpoint
continuity and the two-channel tail inequality. Four rare-sector fixtures keep
mean energy fixed while the absolute signal decreases with the energy level.
`diagnostics.json` records every case. These checks do not establish the proof
or historical priority.

The uniform sqrt(p) tail bound is conservative. The executed random fixtures
showed single-channel losses no larger than 2.722 p, but this does **not** prove
a linear tail theorem. In a spectral truncation that commutes with rho, a
linear bound is plausible from the explicit Sylvester coefficients. The actual
energy projection need not commute with rho. A dimension-free linear bound
requires new work; it must not be inferred from these fixtures. Intermediate
tests with strongly nonuniform spectra and noncommuting projectors expose the
role of triangular Schur multipliers, whose operator norms can grow with
dimension. No sharp exponent is claimed.

More consequential is the analogous question for the **unrestricted Umegaki
entropy defect** from N675. Its denominator can approach a singular state
without a paid finite excursion. The bounded-SLD argument does not transfer:
logarithmic sensitivity can depend on arbitrarily small eigenvalues. The exact
energy-dilution argument transfers to any block-additive defect, but a uniform
fixed-margin entropy truncation theorem has not been proved here.

## Sources and comparator ledger

1. Astra N675, pinned current packet:
   https://raw.githubusercontent.com/harjassand/astra-research-knowledge/44b7e51f36b6dd4759a0227f23cc6b11671b1583/knowledge/current/packets/N675.json
   Exact retrieved class: variable-dimensional rational-complex strictly
   positive POVM pairs; every finite untouched reference; faithful rho and
   traceless H; unrestricted Umegaki state pairs. User-provided acceptance of
   the theorem and accepted internal dependencies governs this continuation;
   stale packet review labels do not request re-audit.
2. Later public Astra manuscript: *Complete information orders of quantum
   channels: equivalence and undecidability*, dated 11 October 2026,
   https://harjassand.github.io/publications/complete-information-orders/
   and DOI https://doi.org/10.5281/zenodo.23349086 . The present result uses only
   the accepted exact-order conclusion above, not new uninspected claims from
   the later manuscript.
3. Yupan Liu, *Quantum state testing beyond the polarizing regime and quantum
   triangular discrimination*, https://arxiv.org/abs/2303.01952 ; published
   https://doi.org/10.1007/s00037-025-00273-8 . Measured quantum triangular
   discrimination is prior work. The present bounded score is in that family,
   not a new divergence.
4. A. T. Rezakhani, M. Hassani, S. Alipour, *Continuity of the quantum Fisher
   information*, https://arxiv.org/abs/1507.01736 ;
   https://doi.org/10.1103/PhysRevA.100.032317 . General QFI/SLD continuity is prior
   work; no claim is made that all existing continuity results require the same
   spectral assumptions or that this proof is historically first.
5. M. E. Shirokov, *On the Energy-Constrained Diamond Norm and Its Application
   in Quantum Information Theory*, https://doi.org/10.1134/S0032946018010027 .
   Energy-constrained approximation and continuity are established frameworks.
6. E. Shmaya, *Comparison of information structures and completely positive
   maps*, https://doi.org/10.1088/0305-4470/38/44/008 ; F. Buscemi,
   *Comparison of quantum statistical models: equivalent conditions for
   sufficiency*, https://arxiv.org/abs/1004.3794 . Universal decision simulability
   is a distinct, strongly developed operational route. It must be compared
   explicitly before presenting entropy order as universal decision power.

Current-source retrieval issue: Astra Research returned published_refresh_failed
on 28 October 2026. Read-only public GitHub retrieval succeeded at the pinned
commit above. Firecrawl had insufficient credits. These are retrieval facts,
not scientific obstructions.
