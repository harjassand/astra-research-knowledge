# Independent physical-frame and process challenge

Date: 2026-10-27. Authoring branch: independent_opening_6, same existing model.
No descendants, experiments, paid compute, or public writes. The parent owns
the strict-noise net/compiler proof; this document does not certify that moving
implementation or rediscover its entanglement-annihilation input.

## 1. The precise interface being challenged

The scoped parent model has product-state initialization, supplied one- or
two-site operation instruments, and a mandatory **unobserved, fresh** local
noise channel after every retained quantum output. Operation outcomes occur
before that mandatory noise. There is no environment error flag, noiseless
refresh, entangled external input/reference, or uncharged interposed control.
Final destructive local measurement is permitted.

For local dimension d, the noise is

\[
\Phi_c(X)=\frac{c\,\mathrm{tr}(X)I-X^T}{dc-1},\qquad
c>c_0=(1+\sqrt3)/2.
\]

Lami–Huber2016 Theorem7 is an existing source for the relevant two-site
entanglement-annihilation condition. Harrow–Nielsen2003 SectionIII.3 already
extends separability-based approximate classical sampling to fixed bounded
qudit dimension and separability-preserving gates. No new tractability class
follows merely from composing positive kernels.

Independently read source:
[Lami–Huber, arXiv1603.02158v1, Thm7](https://arxiv.org/html/1603.02158v1);
[Harrow–Nielsen, arXivquant-ph/0301108v1, III.2–III.3](https://arxiv.org/html/quant-ph/0301108v1).
The current arXiv records list only v1 for each; an attempted Lami–Huberv2
HTML fetch returned404 and is not a read version.

The parent factorization is algebraically consistent:

\[
\Phi_c=D_t\circ\Phi_{c_0},\quad
D_t(X)=tX+(1-t)\mathrm{tr}(X)I/d,\quad
t=\frac{dc_0-1}{dc-1}.
\]

A pure-projector fidelity-epsilon net has support at least
lambda_max(H)-epsilon[lambda_max(H)-lambda_min(H)] in any Hermitian direction
H. The support of D_t(state space) is
t lambda_max(H)+(1-t)tr(H)/d. Since
lambda_max(H)-tr(H)/d >= [lambda_max(H)-lambda_min(H)]/d,
epsilon <= (1-t)/d suffices. This independently checks the geometric
mechanism, not the parent's particular net generation or LP implementation.
Using a strict inequality leaves a computational slack margin.

Exact rational gate superoperators, rational c, and rational projector
vertices give rational LP data even though c0 is irrational: c0 is used to
prove containment, not as a required coefficient of the compiled target map.

## 2. A universal physical frame has an unavoidable size cost

Here and below this cardinality theorem is **qubit only**. A physical product
frame means a fixed list of M normalized two-qubit products
tau_m tensor sigma_m, with each local factor positive semidefinite.
Mixed local factors and non-Cartesian product lists are allowed.
The universal target is the entire range of (Phi_c tensor Phi_c) on pure
two-qubit inputs. The same target follows from one pure product initialization,
arbitrary dense rational-unitary control, exact state reconstruction, and a
fixed closed frame polytope.

This reachability condition is essential. The singleton {I/2 tensor I/2} is
an invariant physical product frame at every c if no nontrivial initialization
or universal output range is required. Thus an unqualified assertion that no
finite invariant frame exists at c0 would be false.

Write s=1/(2c-1). On qubits,

\[
\Phi_c=\mathrm{Ad}_Y\circ D_s.
\]

The deterministic local Y conjugations do not affect a universal-orbit
containment question. The noisy maximally entangled orbit contains

\[
\rho_R=(1-s^2)I/4+s^2|\Omega_R\rangle\langle\Omega_R|.
\]

Its partial transpose has minimum eigenvalue

\[
\lambda=\frac{1-3s^2}{4}
=\frac{c(c-1)-1/2}{(2c-1)^2}.
\]

For finite c>c0, 0<lambda<1/4. A corresponding eigenvector w_R ranges over
the maximally entangled orbit under local rotations. For any physical product
vertex with Bloch vectors r_m,u_m, partial transposition and a choice of rotation
coordinates give

\[
g_m(R)=\langle w_R|\tau_m\otimes\sigma_m^T|w_R\rangle
=\frac{1-r_m\cdot R u_m}{4}.
\]

The orthogonal reflection from transposition can be absorbed into the
parametrization; R has normalized Haar distribution on SO(3).
Let L=|r_m||u_m|<=1 and a=1-4lambda>0. Under Haar rotation,
r_m dot R u_m is uniform on [-L,L] when L>0. Therefore

\[
\Pr_R[g_m(R)\le\lambda]
=
\begin{cases}
0,&L<a,\\
(1-a/L)/2,&L\ge a
\end{cases}
\le 2\lambda.
\]

For L=0 the probability is0 because g_m=1/4>lambda.
If rho_R lies in the frame hull, its partial-transpose eigenvector obeys

\[
\lambda=\sum_m p_m(R)g_m(R).
\]

At least one g_m(R)<=lambda. Hence these M events cover the whole rotation
group, and a union bound gives the necessary condition

\[
\boxed{M\ge\left\lceil\frac{1}{2\lambda}\right\rceil
=\left\lceil\frac{2}{1-3/(2c-1)^2}\right\rceil.}
\]

For an equal local Cartesian frame F tensor F with |F|=N, M=N^2, so
N>=ceil(sqrt(ceil[1/(2lambda)])).
This is a lower bound, not an optimal construction or an asserted matching
scaling for the parent's net.

At c=c0, lambda=0. Each product vertex has g_m=0 on a Haar-null set:
mixed factors cannot do better, and pure aligned factors still give a
measure-zero rotation set. A finite union cannot cover the group.
This independently obtains the endpoint obstruction at the exact universal
physical-frame scope. It says nothing against nonphysical Hermitian vertices,
arbitrary HMMs, continuous/adaptive frames, or entangled blocks.

### Binary input-size implication

Define the rational dyadic

\[
c_B=\frac{2^{B-1}+\lceil\sqrt3\,2^{B-1}\rceil}{2^B}.
\]

It has an O(B)-bit rational description and
0<c_B-c0<2^{-B}. Since
lambda'(c)=3/(2c-1)^3 <=1/sqrt3 for c>=c0,

\[
M\ge\frac{1}{2\lambda(c_B)}
>\sqrt3\,2^{B-1}.
\]

Thus an **explicit universal physical product-vertex list** has exponential
output size when the strict noise gap is part of the binary input.
This does not prevent polynomial cost in circuit width/depth for fixed d,c,
and does not lower-bound an implicit, adaptive, continuous, or nonphysical
sampler. An N-state index uses only log2(N) bits; cardinality is not itself
the trajectory's memory cost.

The Fraction/isqrt implementation constructs c_B without floating point.
For B=32 it certifies M>=15,456,821,314 and N>=124,326.
For B=64 it certifies M>=37,426,317,030,626,048,823 and N>=6,117,705,210.
No such enormous frame was generated or stored.

### Approximation regularizes the exact boundary

Suppose for every R a state in the same frame hull is within trace distance
epsilon of rho_R. The witness
W_R=(|w_R><w_R|)^Gamma has operator norm1/2, so its expectation can differ by
at most epsilon. Some frame vertex must obey
g_m(R)<=lambda+epsilon. If lambda+epsilon<1/4, the same Haar argument gives

\[
\boxed{M\ge\left\lceil\frac{1}{2(\lambda+\epsilon)}\right\rceil.}
\]

At c0 this is finite for every fixed positive epsilon. This explains why a
no-finite-exact-frame endpoint is compatible with ordinary stated-error
separability simulation. It does not prove a matching approximation bound.

### A constructive stated-error repair using the parent net as an interface

Let L>=1 bound the number of local mandatory noise uses in a circuit, and let
0<epsilon<1 be the desired error in the unconditioned joint classical output
distribution. For rational c>c0, form the entirely rational plan

\[
h=\frac{4\epsilon}{3L},\quad
\Delta=\min(s/2,h),\quad
s'=s-\Delta,\quad c'=(1+1/s')/2.
\]

Replace the target noise by Phi_(c') in the **reference simulation**. This
does not physically alter the device or give exact samples from its original
distribution.

For qubit Pauli channels the diamond distance equals the l1 distance of the
Pauli probabilities: the triangle inequality gives the upper bound, and
applying the difference to half a maximally entangled state gives matching
orthogonal Bell outputs. Hence

\[
\tfrac12\|\Phi_c-\Phi_{c'}\|_\diamond=3\Delta/4.
\]

A hybrid over at most L local uses bounds the joint-output TV error by
3LDelta/4<=epsilon, including ordinary adaptive operation outcomes.
This is an unconditioned guarantee; selecting an exponentially rare
transcript can amplify the error and is not a free conditional sampler.

The new rational margin lambda'=(1-3s'^2)/4 obeys

\[
\lambda'\ge\min(3/16,\epsilon/(2L)).
\]

To see this, if Delta=s/2 then s'<=1/(2sqrt3), giving lambda'>=3/16.
Otherwise Delta=h<=s/2<=1/(2sqrt3), so
s'<=1/sqrt3-h and
lambda'>=(6h/sqrt3-3h^2)/4
>=3sqrt3*h/8=sqrt3*epsilon/(2L)>=epsilon/(2L).

Moreover t'=sqrt3*s', so
lambda'=(1-t')(1+t')/4. The rational fidelity-net tolerance lambda'/2
therefore lies strictly below (1-t')/2, the parent's qubit containment
condition. Thus the exact parent compiler applied to this slightly noisier
reference has a stated accuracy/resource margin controlled by epsilon/L,
rather than an exponentially tiny binary input gap.

The included accuracy_plan.py constructs and exactly checks these rational
plans for gaps at16,32,64,128 dyadic bits; it does not generate the parent's
frame or solve its kernels. For fixed dimension, ordinary bounded-chart
projector nets are polynomial in inverse fidelity tolerance, so this repair
avoids an exponential dependence on the *noise gap* in explicit frame output
size. It is not a new approximate-simulation tractability result: HN already
has the stated-error class. It can still be too expensive in L/epsilon, and
no full-cycle runtime advantage over an adaptive separable-state sampler
has been measured.

## 3. The same averaged channel can expose entangled flagged branches

For qubits the channel is the Pauli mixture

\[
\Phi_c=\sum_{P\in\{I,X,Y,Z\}}p_P\mathrm{Ad}_P,\quad
p_Y=(1+3s)/4,\quad p_I=p_X=p_Z=(1-s)/4.
\]

For rational c these superoperator weights are rational. Choose an independent
flag availability eta in (0,1], and the five-outcome local instrument

\[
\mathcal J_?=(1-\eta)\Phi_c,\qquad
\mathcal J_P=\eta p_P\mathrm{Ad}_P.
\]

Erasing the flags gives exactly Phi_c. This is an instrument at the **noise
output**, which the parent's scoped theorem explicitly does not grant.

Take |00> and the entirely rational two-qubit unitary

\[
V=
\begin{pmatrix}
3/5&0&0&-4/5\\
0&1&0&0\\
0&0&1&0\\
4/5&0&0&3/5
\end{pmatrix}.
\]

It prepares |psi>=(3|00>+4|11>)/5. In the event that both local noise flags
are available, their local Pauli inverses restore the subnormalized state
eta^2 |psi><psi|. The event has probability eta^2, independent of the input
Pauli labels. Its partial transpose has the negative expectation

\[
\langle\psi^-|[\eta^2|\psi\rangle\langle\psi|]^\Gamma
|\psi^-\rangle=-12\eta^2/25.
\]

No positive mixture of physical product vertices can represent this
subnormalized outcome. This rules out **every** physical product frame for
the full flagged instrument, not merely the parent's chosen finite net.
Entangled-block, nonphysical, or other hidden-state simulators are not
excluded.

The obstruction itself needs **no recovery gate**. Every separately labelled
(P,Q) branch is a known local-unitary conjugate of the entangled state.
For example the (I,I) branch already has negative partial-transpose witness
-12*eta^2*p_I^2/25. Local inverses above serve to combine the branches into
one common witness and to display the unknown-input correction interface.

For eta=1/100, the both-flag probability is1/10000 and the witness is
-3/62500. The expected heralding repetitions are10000. It would be incorrect
to count a conditional entangled trajectory as a deterministic free resource.
Each local classical record has five possible symbols. A straightforward
packet costs one availability bit and two additional Pauli bits when
available; asymptotic compression instead costs the record's Shannon entropy.

For eta=1, inverse Pauli feedback corrects **every unknown input** exactly.
If ideal corrections are not granted, a known Pauli frame can be folded into
the next supplied ideal gate and final measurement settings, but that needs
appropriate classical feedforward and control acquisition. The theorem does
not supply this environment access or its latency/noise/metrology cost.

This correction principle is old: Gregoratti–Werner2002/2003,
Proposition2 and the following discussion, characterize perfect
environment-assisted quantum correction for Kraus operators proportional to
isometries. Their depolarizing example already makes the basic point. The
present calculation specializes it to the compiler's rational channel and
charges a partial flag's heralding cost; it is not a new error-correction
device.

[Gregoratti–Werner, arXivquant-ph/0209025v1, II.1–II.3 and III.1](https://arxiv.org/html/quant-ph/0209025v1).
The arXiv record and university publication record list different related DOI
strings; this document pins the arXivv1 actually read and does not resolve that
bibliographic discrepancy by guessing.

### Averaged corrected threshold with partial flags

Undo the fixed Y and write the equivalent D_s as a Pauli mixture with its
large identity weight. Correct observed Pauli errors and discard flags.
The effective averaged map is exactly

\[
\eta\,\mathrm{id}+(1-\eta)D_s=D_q,\qquad
q=\eta+(1-\eta)s.
\]

The ordinary qubit symmetric depolarizing EA threshold is q<=1/sqrt3,
an existing special case of Lami–Huber. Consequently

\[
\eta_{\rm av}=\frac{1/\sqrt3-s}{1-s}
\]

is the averaged corrected boundary. For small eta the averaged map may
still be EA even while its retained both-flagged branch is entangled.
This is why an averaged noise number does not specify a monitored
instrument. At c=3/2, eta_av approximately0.1547; eta=.01 is comfortably
below it. Near c0 the allowable averaged flag correction margin tends to0.
No statement here gives an uncharged physical correction operation.

## 4. Freshness is independent information: an unobserved two-call echo

Choose P with the above distribution once per pair of noise calls. Apply
that same Pauli at both calls, then discard/reset the classical label.
There is no exposed flag. Each isolated one-use channel, with a fresh input
independent of the label, is exactly Phi_c. For every unknown input X,
including one entangled with an external reference,

\[
\sum_Pp_P\,P(PXP^\dagger)P^\dagger=X,
\]

because P^2 is a phase times identity.

For two active qubits, store independent labels P,Q and use the pair twice.
For an arbitrary ideal two-qubit U, the known schedule

1. apply U, then Ad_(P tensor Q);
2. apply the identity, then the same Ad_(P tensor Q)

has net channel Ad_U on every unknown input. Repeating such fresh *pairs*
implements an arbitrary ideal circuit with two operation calls per ideal
gate. The first output can have the EA averaged state while the second
restores entanglement.

Resources of this abstract process are a four-valued label per active qubit,
a two-phase clock, label retention for one interval, and an independent draw
between pairs. Its existence is not physical acquisition of such a memory
environment. The construction is the familiar ability of correlated random
unitaries to revive information, specialized as an exact rational process
witness. It is not a new device or a proof of classical hardness.

A direct physical prior is Xuetal2013's optical realization of revivals under
a classical random-unitary environment, whose interpretation explicitly
uses its retained classical operation label:
[NatureCommunications4,2851, theoretical model and interpretation](https://pmc.ncbi.nlm.nih.gov/articles/PMC3868330/).
The publisher URL initially failed with an authentication redirect; the PMC
article supplied the primary full text. This is a different physical model,
not an experimental implementation of this branch's repeated-Pauli process.

The second call is **not** Phi_c acting independently on the current
system state: the input and retained environment are correlated. Thus this
example does not refute the scoped composition of fresh CPTP noise maps.
It decisively shows that isolated one-use tomography does not imply the
multi-time premise needed for that composition.

The executable checks every matrix unit, rather than only a prepared state.
For the rational |psi> above, local XX readout gives

\[
\mathbb E_{\rm echo}[XX]=24/25,\qquad
\mathbb E_{\rm fresh}[XX]=(24/25)s^4.
\]

For c>c0, their gap is greater than64/75. At c=3/2 the fresh value is3/50,
while the echo value is24/25. Even a one-qubit |0> input followed by two
noise calls suffices: the Z expectations are1 (echo) and s^2 (fresh).
This uses no entangling preparation and has gap greater than2/3.

A bounded diagnostic can falsify this specific correlation mechanism with
ordinary local readout. If the two simple hypotheses have known means with
gap Delta, thresholding the sample mean of +/-1 measurements at their
midpoint has error at most exp[-m Delta^2/8] under either hypothesis.
For Delta>2/3, m>=18 log(1/alpha) is sufficient for error<=alpha under either
hypothesis. This is a model discrimination cost, not a general Markov
certificate; detector/gate errors must also be charged. No shots were taken.

Unknown longer memory may pass this diagnostic. Exact arbitrary-depth
freshness is not established by one two-call test, and no finite-data
physical exactness claim is made.

## 5. Kernel sparsity and fair-bit cost, separated from frame size

Conditional on an existing finite rational physical frame and exact rational
gate data, a two-qudit trace-preserving update solves a rational feasibility
LP in the d^4-dimensional real Hermitian matrix space. A basic feasible
column needs at most d^4 nonzero output vertices. This is ordinary
Caratheodory/LP sparsity. An m-outcome instrument can use at most m*d^4
joint (outcome, vertex) entries by decomposing branches separately.

This sparse support does **not** remove the need to acquire the vertex list
and find feasible columns. A local Cartesian frame with N vertices has N^2
input-pair columns per distinct two-site gate. A full dense table would have
N^4 entries; a sparse per-column representation has at most d^4*N^2
probabilities and output pairs for a trace-preserving gate. Lazy on-demand
column solving can trade work for cache size.

For fixed d,c and a fixed rational frame, choosing a full-rank rational basis
of at most d^4 columns and using exact linear elimination gives rational
weights. Cramer's rule bounds their bit length polynomially in matrix
dimension and input bit length. With that dimension/frame fixed, the weight
bit length is O(L) in the supplied gate's rational description length L.
This is an algebraic resource bound, not a speed measurement of a general LP
solver. If d or the noise gap varies, neither the constants nor the explicit
frame acquisition are free.

The included rational_sampler.py implements ordinary exact inverse-CDF
sampling. Draw unbiased bits of U in[0,1], and stop when the current dyadic
interval falls wholly inside one categorical CDF cell. For a column with r
positive entries,

\[
\Pr[B>k]\le\min(1,(r-1)2^{-k}),\qquad
\mathbb E B\le\lceil\log_2(r-1)\rceil+2 \quad(r>1).
\]

Only the at most r-1 dyadic cells containing CDF boundaries remain
undecided. Summing the geometric tail proves the expectation bound.
Exact rational interval comparisons have finite arithmetic cost per bit;
the geometric tail also bounds the expected polynomial bit-arithmetic cost.
No assumption that an arbitrary rational probability is a unit-cost
randomness primitive is needed.

For r=16 the stated bound is6 bits, independent of N and circuit depth.
The Bernoulli1/3 example has expected cost2 bits but unbounded worst case.
No algorithm with a fixed finite worst-case number of unbiased bits can
sample a non-dyadic rational exactly, since all its leaf probabilities have
a common power-of-two denominator.

For G updates of support at most r, a union bound gives
Pr[some update uses more than k bits] <=G(r-1)2^-k.
A finite bit cap that aborts changes the output law; charging its probability
gives an approximate algorithm. The uncapped sampler terminates almost
surely with the exact distribution, not a deterministic bounded runtime.
The code checks exact assigned/unresolved probability mass through depth64
without Monte Carlo and without enumerating2^64 prefixes.

The frame index requires log2(N) bits per local site. Thus exact online
sampling may be inexpensive **after** an expensive explicit frame/table
acquisition. Neither frame count nor expected random bits alone is a
full-cycle cost comparison.

## 6. Strong prior and the surviving scientific claim

Cihan Okay's 2026 paper gives the general preservation-to-kernel interface
already: Definition13 is branchwise convex containment, Theorem16 constructs
the positive update, Lemma17 composes adaptive instruments, and Corollary19
gives exact Born-distribution sampling. Its operators can be nonphysical
Hermitian states; this is broader representation freedom than the parent
physical product frame.

Personally read these sections from the publisher's 2June2026 open article:
[Polyhedral classical simulators for quantum computation](https://link.springer.com/article/10.1007/s40687-026-00626-x),
DOI10.1007/s40687-026-00626-x. A targeted search found no noise-specific
section but does not prove absence of a noise theorem elsewhere.

The defensible remaining parent result is a specified fixed local rational
**physical product** frame under a strict fresh/unobserved noise margin, its
exact universal gate interface, and its exact endpoint/cost quantifiers.
The generic stochastic-composition idea, separability-based approximate
sampling, and environment-assisted Pauli correction are established priors.

The challenge adds an independent quantitative explicit-frame lower bound,
a trace-tolerance regularization, and exact rational countermodels to
averaged-channel-to-instrument/process transfer. None is claimed here to be
a new tractability class, a physical noise-control capability, or a novelty
certificate.

## 7. What a physical transfer certificate would have to bound

If an actual process admits a per-update bound delta_j in half diamond norm
against the specified fresh reference **on the full retained system and
memory**, uniformly over possible inputs/interventions, then a telescoping
hybrid and contractivity give total-variation error at most
min(1,sum_j delta_j) for every adaptive classical transcript. One can
therefore compose an exact reference frame sampler with that acquired
process-error budget to obtain a stated-error operational guarantee.

This premise is much stronger than isolated one-use channel estimates. The
echo construction passes the latter exactly and violates the former.
No process norm, environment-access exclusion, gate calibration, or
multi-time physical experiment has been acquired in this branch.

Executable checks and measured times are in RESULTS.json and
SAMPLER_RESULTS.json. This document's proof is self-contained at its stated
abstract scope; it awaits independent review and does not mark itself
audited.
