# Positive residual events require a stronger coherent interface

28 October 2026. Review of the root's precision attack; no equipment operation.

## Finding

The proposed linear-combination-of-unitaries (LCU) residual event is sound
under an explicitly stronger interface. Native passive evolution and native
nonselective Lueders channels do not supply that interface. The positive-event
sampling improvement may be developed as a conditional extension, but cannot
be transferred to the scalar-echo operation count.

With coherent access, LCU and amplitude estimation are the strong existing
comparators. The addition is the choice of a measurable residual event for
the compiler's certificate. A new generic LCU or amplitude-estimation principle
is not present.

## 1. Exact access contract and normalization

Let the actual Hilbert vector b have known norm beta>0. Assume available:

1. Coherent preparation of the normalized amplitude state |b>/beta.
2. Coherently controlled (1,a,0) block encodings of every native contraction
   A_i, including the needed word products on fresh ancilla registers.
3. Preparation/unpreparation of the coefficient register and a projection
   testing that all encoding and coefficient ancillas are in their success
   state.

For amplitude estimation, also require inverse preparation/encoding circuits,
success and initialization reflections, and the controls needed by the chosen
amplitude-estimation implementation. They are not needed merely to repeat
independent success trials.

For a dictionary V=[A_(w_1)b,...,A_(w_r)b], coefficient map T_i and vector x,
define the actual residual E_i=A_i V-VT_i. The operator

    K_(i,x) = sum_j x_j A_i A_(w_j)
              - sum_j (T_i x)_j A_(w_j)

satisfies K_(i,x)b=E_i x. If

    C_(i,x)=||x||_1+||T_i x||_1,

standard signed LCU produces a top block K_(i,x)/C_(i,x). Consequently its
ancilla success probability on |b>/beta is exactly

    p_(i,x)=||E_i x||^2 / (beta^2 C_(i,x)^2).

The root formula without beta applies when b is normalized. Known quantum
identity centering changes its norm to sqrt(1-1/d) for a pure-state reset;
the normalized centered operator also needs an actual coherent preparation
algorithm. Merely subtracting 1/d from scalar response records does not prepare
that amplitude state.

If actual block encodings have normalizations alpha_i>1, product
normalizations multiply along words. C must then include the appropriate
word-normalization weights. The fact ||A_i||<=1 does not acquire a
normalization-one encoding.

## 2. Positive-event sample cost and its exact scope

For n independent Bernoulli trials, zero successes give the one-sided
confidence statement

    p <= 1-delta^(1/n) <= log(1/delta)/n

with false-certification probability at most delta. Thus a residual upper
bound epsilon can be certified in the zero-success case using

    n >= beta^2 C^2 log(1/delta)/epsilon^2.

This is a positive probability measurement. It avoids estimating a difference
of order-one moments to additive accuracy epsilon^2, which can require
epsilon^-4 repetitions under ordinary bounded-variance scalar sampling.
The comparison concerns that estimator and access model, not every possible
native scalar procedure.

Zero successes are a sufficient event, not a complete test for all acceptable
residuals. For a genuinely nonzero p near the target threshold, the event can
be rare. A useful verifier should count successes and use an appropriate
one-sided binomial bound, or state a promise gap. Testing p<=p_0 against
p>=4p_0 requires order log(1/delta)/p_0 trials with ordinary multiplicative
probability bounds; no zero-count promise is necessary. Exact-zero residuals
are the particularly clean case.

If dictionary words have length at most L, a straightforward multiplexed
SELECT uses at most 2r(L+1) controlled native block-encoding calls per trial.
This is a conservative compilation bound, not a free single query. Count
coefficient loading, source-state preparation, ancillary registers, reset,
measurement and the controlled-gate synthesis as well. Word products of block
encodings normally require distinct success ancillas; silently reusing them
can admit failed branches into the purported top block.

## 3. A single positive event can bound an entire residual matrix

Let R_i=E_i*E_i and let W>0 be the known computational metric. Write a known
positive factorization

    W^-1 = sum_k d_k z_k z_k*,   d_k>0.

A rational LDL* factorization permits rational d_k,z_k when W is rational,
avoiding an assumed exact irrational Cholesky factor. For each z_k set
C_k=||z_k||_1+||T_i z_k||_1, and define

    S_i = beta^2 sum_k d_k C_k^2.

Classically select k with probability beta^2 d_k C_k^2/S_i, then run its
coherent residual trial. The mixture has success probability

    p_mix = Tr(W^-1 R_i)/S_i.

Since W^-1/2 R_i W^-1/2 is positive,

    R_i <= Tr(W^-1 R_i) W.

Therefore p_mix<=epsilon^2/S_i certifies R_i<=epsilon^2 W. Zero successes
require order S_i log(1/delta)/epsilon^2 trials. The trace criterion can be
dimensionally looser than a sharp operator-norm certificate; S_i also carries
coefficient conditioning and the chosen factorization cost. Neither is hidden
by calling the trial a single residual measurement.

Separate forward and adjoint residuals are needed for nonsymmetric blocks.
Allocate the joint confidence budget across all residual families, together
with any noisy model-selection/acquisition statements. No extra union bound
over future words is required once these finite uniform matrix bounds hold.

## 4. Encoding errors establish a precision floor

Suppose the actual prepared success amplitude differs from
E_i x/(beta C) by a vector of norm at most zeta. A measured success-probability
upper bound p_upper then implies

    ||E_i x|| <= beta C (sqrt(p_upper)+zeta).

The deterministic zeta budget includes coefficient synthesis, primitive
block-encoding errors, word composition and initial-state preparation. It
must be known and small enough relative to epsilon/(beta C). Repetitions do
not remove it. Classical outcome/readout errors also require a calibrated
probability allowance; false-negative bias must not be treated as a rare
true residual.

## 5. Why native Lueders and passive operations do not provide this access

A native Lueders channel physically acts on density operators by

    Phi(rho)=sum_y sqrt(E_y) rho sqrt(E_y).

The compiler's physical Hilbert space is the Hilbert-Schmidt space of
operators. A block encoding of Phi acts coherently on vectorized operators
and has matrix sum_y sqrt(E_y) tensor conjugate(sqrt(E_y)). Applying Phi to a
laboratory density matrix, then discarding its measurement record, does not
implement that linear map on amplitude vectors. Nor does it supply controlled
SELECT over different word histories, signed interference between those
histories, or coherent access to the discarded environment.

Even a Stinespring unitary for a channel is a different interface from
uncontrolled channel use. Constructing a suitable superoperator block
encoding from a known dilation is an additional algorithm with its own
normalization and preparation cost. A projective instrument implemented with
accessible coherent records may offer such extra structure, but that must be
specified and constructed. It is not a consequence of the Lueders CP map.

The same distinction is more immediate for a classical dissipative RC or heat
network. One-port preparation, switching and a scalar response do not offer
coherent quantum superposition of program histories or a quantum norm-success
test. Other linear-combination experiments may be possible on particular
apparatus, but those are additional source operations to construct and cost.

This is an access-contract rejection, not a blanket impossibility theorem for
all physical realizations. For example, unknown-unitary control has a
well-known black-box obstruction, while physical path extensions can supply
the missing structure. The role of that result here is to prevent treating
coherent control as automatically supplied by an ordinary operation oracle.

## 6. Strong equally informed quantum comparator

With full coherent access, amplitude estimation is stronger than independent
positive-event sampling. The standard bound, at constant success probability,
is

    |p_hat-p| <= 2*pi*sqrt(p(1-p))/M + pi^2/M^2.

It implies the one-sided amplitude estimate

    sqrt(p) <= pi/M + sqrt(p_hat+2*pi^2/M^2).

Near zero this supplies residual-norm accuracy epsilon using order
beta C/epsilon coherent calls, before confidence amplification and all circuit
costs. Taking medians of independent runs raises confidence with a logarithmic
factor. The cost includes the preparation circuit and its inverse, reflections
and controls; it cannot be compared with native scalar receiver samples as
though access were the same. Its longer coherent depth may be decisive in an
implementation.

Thus the new construction is a conditional residual-event acquisition for the
compiler. LCU, the near-zero statistical gain and the further coherent
amplitude-estimation gain should be attributed at their established scope.

## 7. Exact positive-flag obstruction even for ordinary quantum channel testers

The parent construction already has a classical finite-transcript support
obstruction. Here is a stronger access-specific version allowing adaptive
quantum testers with ancillary systems and entangled measurements, while
retaining ordinary uncontrolled channel calls.

On a qubit let Depol(X)=Tr(X)I/2 and

    Phi_t = t Id + (1-t) Depol,      1/3 <= t <= 1.

Every member is a Lueders channel. The equal mixture of the three projective
Pauli dephasings has t=1/3, the trivial one-outcome measurement has t=1, and
convex mixtures of Lueders instruments are Lueders instruments by scaling
each POVM effect by its mixture weight.

Choose an interior t_0, a nonzero traceless reset component b_0, dictionary
V=[b_0], and the fixed scalar coefficient map T=t_0. The exact residual is
(t-t_0)b_0, zero at t_0 and nonzero otherwise.

**Claim.** No finite ordinary-channel-call experiment can have a positive
event whose probability is zero at t_0 and positive at another t in this
family. Thus it cannot directly realize the normalized squared residual.

**Proof.** For every t, convexity of this line segment gives
Phi_(t_0)=q Phi_t+(1-q)Xi with q>0 and Xi another channel in the family
(take the opposite endpoint). An n-query adaptive experiment has outcome
probabilities multilinear in the n channel uses. Expanding this mixture gives
a sum of nonnegative branch probabilities; the term choosing Phi_t in every
slot has weight q^n. Hence

    p(t_0) >= q^n p(t).

If p(t_0)=0, then p(t)=0. Ancillas, known quantum processing and intermediate
measurement/feedforward do not change positivity or multilinearity. For an
almost-surely terminating protocol, apply the argument to each event that the
flag has occurred by the nth call, then take their countable union. QED.

This is the usual full-support/unambiguous-discrimination obstruction applied
to an explicit Lueders residual family, not a new general impossibility
principle. It does not rule out confidence certificates, signed estimators,
approximate events with a nonzero floor, or access to a particular coherent
physical dilation. Controlled block encoding supplies additional information
outside this ordinary-channel-query model.

## Primary sources inspected

- Gilyen, Su, Low and Wiebe, *Quantum singular value transformation and beyond:
  exponential improvements for quantum matrix arithmetics*,
  [primary manuscript](https://ir.cwi.nl/pub/28513/28513.pdf), Section 4.3,
  Definition 51 and Lemma 52; Section 4.4 on products. Lemma 52 supplies the
  signed LCU block encoding and its synthesis-error accounting. The product
  discussion explicitly treats the ancillary registers.
- Brassard, Hoyer, Mosca and Tapp, *Quantum Amplitude Amplification and
  Estimation*, [primary manuscript](https://arxiv.org/pdf/quant-ph/0005055),
  Section 4, Theorem 12. The displayed probability-dependent error bound and
  inverse/preparation access are the comparator used above.
- Araujo, Feix, Costa and Brukner, *Quantum circuits cannot control unknown
  operations*, New Journal of Physics 16 (2014), 093026,
  [primary manuscript](https://arxiv.org/pdf/1309.7976),
  [DOI](https://doi.org/10.1088/1367-2630/16/9/093026). Ordinary black-box
  unitary use does not universally yield controlled use; physical subspace
  structure can change that access model. This source is not asserted to
  prove a special impossibility theorem for the restricted Lueders family.
