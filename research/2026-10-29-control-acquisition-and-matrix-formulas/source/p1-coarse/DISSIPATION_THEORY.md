# Acquired dissipation-weighted defects for arbitrary operation programs

28 October 2026. This is the constructive continuation after the failed
primitive-relative criterion. It uses an established dissipation argument,
extends the signed residual remainder with a Julia-operator energy estimate,
and constructs finite scalar-echo acquisition of the required source forms.

## 1. The correct stronger premise

Let A_i be contractions on H, not necessarily self-adjoint. Let V map a finite
coefficient space into H, b=Vc, and W>0 be a computational metric. Choose
forward maps T_i and dual maps S_i such that

    R_i=W-T_i*WT_i >=0,  Rdual_i=W-S_i*WS_i >=0.

Set D_i=A_iV-VT_i and J_i=A_i*V-VS_i. Require actual bounded factorizations

    D_i=(I-A_i A_i*)^(1/2) K_i,  K_i*K_i<=theta_f^2 R_i,
    J_i=(I-A_i* A_i)^(1/2) L_i,  L_i*L_i<=theta_b^2 Rdual_i.

These are source-dissipation conditions. They are much stronger than replacing
a residual norm by its ratio to the finite model's increment. In finite
dimension they are equivalent to the corresponding inverse-dissipation
quadratic-form inequalities plus the appropriate range inclusions. A bare
pseudoinverse that erases a component in the kernel is invalid. In infinite
dimension the displayed bounded factorization is the clean premise.

No uniform contraction margin below one is needed in this theorem, on either
the true operators or the computational maps. Finite acquisition below does
use an additional source margin to bound its unmeasured tail.

## 2. First-order uniform bound: established energy mechanism

For a word i_1,...,i_h, use alpha_0=c, alpha_t=T_(i_t) alpha_(t-1).
The scalar difference between the source response and c*G alpha_h is a sum
of inner products between true backward states and D_(i_t) alpha_(t-1).
The factorization and Cauchy-Schwarz bound this sum by

    theta_f ||b|| ||c||_W.

The two sums telescope: backward source dissipation is at most ||b||^2,
and sum alpha_(t-1)*R_(i_t)alpha_(t-1) is at most ||c||_W^2. This is the
switched/intertwining version of the ordinary dissipation perturbation
argument. Veselic's 2004 Theorem 2 already proves the corresponding
uniform discrete-semigroup bound; it must not be claimed as new here.

## 3. Second-order signed correction

Use beta_h=c, beta_(t-1)=S_(i_t)beta_t and the same actual signed correction
as in `BLOCK_THEORY.md`. The exact residual identity is

    f-tilde_f = sum_(s<t) <J_(i_t) beta_t,
                           A_(i_(t-1))...A_(i_(s+1)) D_(i_s) alpha_(s-1)>.

**Theorem.** Under the bounded factorizations above,

    |f-tilde_f| <= 2 theta_f theta_b ||c||_W^2

for every finite word, with no horizon or contraction-gap factor.

**Proof.** Put u_t=K_(i_t)alpha_(t-1), v_t=L_(i_t)beta_t. Computational
energy telescoping gives sum||u_t||^2<=theta_f^2||c||_W^2 and the analogous
bound for v. Let e_0=0 and

    e_t=A_(i_t)e_(t-1)+(I-A_(i_t)A_(i_t)*)^(1/2)u_t.

For each contraction A, the classical Julia/Halmos block operator

    [ A                    (I-AA*)^(1/2) ]
    [ (I-A*A)^(1/2)       -A*            ]

is unitary. Define y_t=(I-A_(i_t)*A_(i_t))^(1/2)e_(t-1)-A_(i_t)*u_t.
Its energy identity gives sum||y_t||^2<=sum||u_t||^2. Therefore the raw
dissipation outputs z_t=y_t+A_(i_t)*u_t have l2 norm at most 2||u||_l2.
The exact remainder is sum <v_t,z_t>. Cauchy-Schwarz proves the claim.
QED.

The factor 2 is a bound for the causal propagation kernel. The subsequent
scoped construction in branches/dynamics/DISSIPATION_CONSTANT_CHALLENGE.md
shows that it is sharp at this theorem's stated generality, with realizable
paired defects and coefficient trajectories. It includes a nonsingular
dictionary extension. This does not establish sharpness after adding such
extra restrictions as a fixed Gram floor or true Galerkin maps.
The theorem controls the true correction; finite observation intervals must
still enclose that correction. It does not make those interval widths zero.

## 4. Finite source-form acquisition with reciprocal echoes

Specialize to self-adjoint primitives, S_i=T_i, and a warranted bound
||A_i||<=a_i<1. Then the required matrix is

    Q_i=D_i*(I-A_i^2)^(-1)D_i=sum_(k>=0) D_i*A_i^(2k)D_i.

After K terms its tail has the rigorous Loewner upper bound

    Q_i <= sum_(k=0)^(K-1) D_i*A_i^(2k)D_i
           + D_i*A_i^(2K)D_i/(1-a_i^2).

This follows by the spectral theorem and the geometric-series bound;
self-adjointness allows A_i^K to commute through the tail. For a proposed
map T_i each term is a linear expression in scalar echo records:

    V*A_i^(2k+2)V - V*A_i^(2k+1)V T_i
      -T_i*V*A_i^(2k+1)V +T_i*V*A_i^(2k)V T_i.

Repeated words are combined before interval evaluation. A midpoint matrix
plus the diagonal row sums of its entry radii is a valid Loewner upper
bound. We accept theta_i^2 only after an exact rational PSD check of

    Qupper_i <= theta_i^2 (W-T_i*WT_i).

For q primitives, r dictionary words of maximum depth L, the direct schedule
has at most q(2K+3)r(r+1)/2 entries before reuse and maximum primitive-word
length 2L+2K+2. Reset, execution, calibration, precision, computation and
the source norm premise remain separate resources. The implemented numerical
proposal requires positive definite computational dissipation; the abstract
theorem also permits semidefinite budgets with exact range handling.

With theta=max theta_i, the signed dynamical remainder is <=2theta^2||c||_W^2.
For the executed noisy fixtures, the original exact computational rho<1
is used only to give a uniform upper bound on the scalar correction's
measurement interval. The energy theorem itself has no rho denominator.

## 5. Executed construction

The synthetic sources have b=e_1 and two unknown positive contractions

    A_0=[[1-g,g],[g,1/4]],  A_1=[[1-2g,-g],[-g,1/3]].

The learner receives the reset dictionary, calibrated scalar intervals,
and the explicit prior norm warranty a=1-g/2. It does not receive these
matrices or a dimension/rank promise. The checker verifies that warranty
against the hidden matrices. In an implementation the warranty would need
independent physical justification; the readings do not establish it.

`core/run_dissipation_experiment.py` uses K=8, 37 source records, two affine
standards, 37 resets, 342 primitive applications and maximum word length 18.
For g=0.001 and raw ADC error 1e-14, the certified absolute all-word bound is
0.001069085762. The original unweighted all-word bound for the same proposed
maps and same records is 1.000002004017664. The reduction is about 935-fold.
This is a bound improvement, not a physical speedup or comparison against
every established model-reduction method.

Five source scales, a fixed-source noise sweep and a depth sweep are
preserved in `results/DISSIPATION_EXPERIMENT.json`. All fixtures check
the source inequalities and finite acquired inverse-dissipation forms in
exact arithmetic. The primary five also check 64 six-step switched programs
and six long constant-mode programs, up to 5,000 steps. Those checkers use
hidden matrices only to verify the synthetic receipts. The uniform theorem,
not sampling of long programs, establishes the all-word statement.

## 6. What improved and what remains paid

The old norm certificate pessimistically lets every residual live forever
on the slow scale of the retained state. The extra echoes measure how
that residual relaxes in the actual source. In this family it lies mainly
in a fast direction, so weighting by the actual inverse dissipation is
small. This information is absent from a single residual norm.

The acquisition tail still uses 1/(1-a^2), and moment differencing still
needs absolute precision. In the main scale sweep eta=g^3/100000 explicitly
becomes more demanding as g decreases. The fixed-source noise sweep shows
the certificate becoming wide when that precision is withdrawn. Binary
sampling would have to pay for it; no quantum shot advantage is asserted.

This is an extension of the finite experimental compiler, built from known
energy and dilation machinery. A method already using these same echoes,
source warranty and source-form residuals can adopt the certificate at the
same acquisition cost. Known-rank identification or direct knowledge of the
hidden matrices can be stronger with their added information.

The unresolved broad opening is to acquire these source-form bounds, or
an equally useful joint relation, without paying a prohibitive tail or
precision cost on relevant physical sources. The all-design lower bound
in `ADAPTIVE_EXPERIMENT_COST.md` shows that no uniform cheap solution exists
for every allowed scalar receiver and slow source.

Primary antecedents: K. Veselic, *Bounds for contractive semigroups and
second order systems*, https://arxiv.org/abs/math/0404120, Theorem 2;
P. L. Robinson, *Julia operators and Halmos dilations*,
https://arxiv.org/abs/1803.09329. The source-form echo acquisition and signed
program application above are stated separately from those existing results.

## 7. Subsequent removal of the explicit coefficient-gap noise factor

core/dissipation_noise.py preserves a stronger same-record uncertainty
calculation, independently reviewed in branches/scalar/DISSIPATION_NOISE_REVIEW.md.
For an entry-radius matrix r_jk of the weak-defect error, set a diagonal
dominator D with entries the maximum of the corresponding row and column
sums. Weighted Cauchy-Schwarz gives

    |x* error y| <= sqrt(x*D x) sqrt(y*D y).

An exact inequality D<=zeta_i R_i and the two computational energy sums then
bound the entire correction uncertainty by max_i zeta_i ||c||_W^2, without an
explicit uniform computational contraction gap. A Gram uncertainty bound
gamma_G W adds gamma_G ||c||_W^2. Small dissipation can still demand precise
observations; normalization does not manufacture those observations.

Twelve saved fixtures were re-evaluated with zero new source queries. The
main g=.001 bound becomes .001069081794. The original code, results and
their reviewed hashes remain unchanged; the refinement has separate files.

## 8. Subsequent finite acquisition without a strict source norm cap

ABSORBING_BOUNDARY_THEORY.md constructs the local source forms through finite
censored first-return data when the observer distinguishes irreversible loss
from a live hidden excursion. The source may have norm exactly one. Local
boundary Schur inverses replace the global factor 1/(1-a^2), including in the
transfer to estimated maps. The implementation executes this acquisition on
a countably infinite reachable source and preserves a full cost comparison.

This removes the strict source-gap premise from weighted-form acquisition.
The earlier unweighted compiler already needed no strict hidden source gap;
its limitation is the weaker certificate in slow-scale families, not universal
inability to certify any gap-free source. ABSORBING_BOUNDARY_EXTENSIONS.md
exhibits the separating family and charges the remaining calibration and
sensor-precision requirements.
