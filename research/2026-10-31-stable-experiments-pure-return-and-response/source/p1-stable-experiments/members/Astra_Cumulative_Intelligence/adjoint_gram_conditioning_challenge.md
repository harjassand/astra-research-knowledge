# Adjoints, conditioning, and the missing robust acquisition theorem

Constructive challenge note, 31 October 2026.
Scope: unknown contractions T_a on a real Hilbert space, norm-at-most-one seeds
f_i, noisy scalar moments <T_u f_i,T_v f_j>. Words may use genuine adjoints.
Every scalar read and its full primitive word length is charged.

## Decision

I did NOT prove either a general polynomial robust-acquisition theorem or a
counterexample to polynomial acquisition for additive-epsilon predictions of
all words of length at most H. In particular, exponentially bad pivot
conditioning is NOT a valid lower bound for that prediction task. Contractions
can make precisely those ill-observed directions operationally irrelevant.

I obtained a sharp obstruction to the stronger goal of acquiring the entire
normalized reachable operator representation, a clean task-level escape from
that obstruction, and an explicit sufficient/certifiable frame condition with
polynomial full costs. These distinguish a genuine unresolved theorem from
a merely missing proof of a false normalization claim.

## 1. Exponential cost of normalized complete representation, even with adjoints

Let d>=2, 0<q<=1/2, with orthonormal e_0,...,e_(d-1). Set f=e_0.
Give the source alphabet A,A*,B_theta, where

A e_j=q e_(j+1) for j<d-1; A e_(d-1)=0;
B_theta e_j=e_j for j<d-1; B_theta e_(d-1)=theta e_(d-1),
theta in {-1,+1}.

All are contractions; B_theta=B_theta* is unitary. The reachable linear space
has exact dimension d for every q>0. A natural reachable-word frame is
f,Af,...,A^(d-1)f with diagonal Gram eigenvalues
1,q²,...,q^(2d-2).

Every word sends f either to zero or to one basis vector times q to the number
of shift letters, with possible sign from B_theta. A Gram query differs between
theta=+1 and -1 only if a branch visits level d-1 and contains an odd relevant
B occurrence. If the two endpoints differ, the Gram query is zero in both
models. If endpoints agree at j, the total number of shift letters in the
two queried words is at least2(d-1): one branch must go from0 to d-1 and
then end atj, costing at least2(d-1)-j shifts, while the other costs at leastj.
Hence every differing scalar moment has absolute value at most q^(2d-2).
This remains true for arbitrarily long words and all adaptive choices.

Choose the legitimate scalar measurement service returning a +/-1 bit with
mean equal to the requested real moment. If the moment changes, its mean is
+/-z with |z|<=q^(2d-2)<=1/4. The Bernoulli relative entropy is at most
C z², e.g. C=4 suffices for |z|<=1/2. Adaptivity and arbitrary word choices do
not change the conditional per-read bound. Transcript KL after N reads is
at most C N q^(4d-4).

By the ordinary testing bound (or Pinsker for fixed constant confidence),
distinguishing the two models with error<=1/4 requires
N=Omega(q^(-4d+4)).
A log(1/delta) factor follows from binary KL for error delta.
All word execution costs are additional. The bound allows actual adjoints.

What is obstructed:
a normalized all-state operator representation that resolves B on e_(d-1),
or claims uniform operator-norm error<1. On that normalized direction the
two operators differ by2. Full reachable rank d does not supply its physical
normalization or a polynomially observable frame.

What is NOT obstructed:
the original additive-epsilon scalar prediction task. Every affected
seed-to-seed word response is at most q^(2d-2), so if epsilon exceeds that,
both sources have the same valid coarse predictor. If epsilon is smaller,
the lower bound is merely of order epsilon^-2, compatible with polynomial
accuracy cost. Thus this construction must not be advertised as refuting the
root's desired theorem.

## 2. Why the obvious password lower bound fails

A d-step partial-shift password automaton with wrong letters annihilating the
state does not hide a password from the present oracle. The norm moment
||T_w f||² tells whether each tested prefix survives. Trying each next action
finds the path in O(d|alphabet|) bounded-precision queries if surviving norm
is constant. If the surviving norm instead decays exponentially, the terminal
additive prediction is correspondingly small unless a stronger normalization
service is supplied.

The familiar noncontractive deterministic automaton merge cannot repair this:
mapping two orthogonal norm-one states to the same norm-one state has operator
norm at least sqrt2. Scaling to obtain contractions pays signal attenuation.

## 3. A certified approximate closure theorem, with acquisition debt visible

Let V=[v_1,...,v_k] consist of actually acquired word vectors,
G=V*V positive definite, P=V G^-1 V*.
Let K_a=V*T_a V and L_a=(T_a V)*(T_a V), all measured using Gram words.

The exact residual matrix is
R_a=L_a-K_a*G^-1 K_a >=0.
The normalized closure defect is
tau_a²=lambda_max(G^-1/2 R_a G^-1/2).

This is exactly ||(I-P)T_a P||², not a residual only on individually small
unnormalized landmarks. Let tau=max_a tau_a.
For a seed f_i, let b_i=V*f_i and
delta_i²=||f_i||²-b_i*G^-1 b_i.
The compressed operators A_a=G^-1/2 K_a G^-1/2 are contractions.

For a word w of length h and seeds i,j,
|<f_j,T_w f_i>-<P f_j,(P T_w P under stepwise projection)P f_i>|
<=delta_i+delta_j+h tau.
Proof: the seed replacements cost delta_i+delta_j by contraction;
the stepwise comparison telescopes, with each closure defect at most tau.
This is uniform in adaptively chosen later words on the same source.

Thus approximate closure can replace exact global rank exhaustion, and a
small unobserved direction need not be normalized and learned. All entries
needed for G,K_a,L_a are scalar real-adjoint words of length at most2L+2
if landmark words have length≤L.

This exact theorem by itself does not provide a cheap frame. Computing
G^-1 requires interval control that may be costly, and estimating the small
difference R_a from noisy entries incurs its own cancellation cost.
A weak Gram eigenvalue is not automatically a significant missing capability.

## 4. Full polynomial cost under an ACQUIRED frame certificate

Suppose a search actually produces k<=r landmark words of length≤L and
certifies G>=gamma I, gamma>0, together with the desired closure and seed
residual bounds. Gamma is a measured certificate; it is not inferred from rank.
The search, unsuccessful candidate sets and their samples must be charged.

There are O(|alphabet| k²+s k+s) distinct Gram/shift entries for exact closure
or same order with L_a added. Estimate them all within eta with joint failure
delta. Bounded +/-1 shots cost
O(eta^-2 log((|alphabet|k²+sk+s)/delta)) per entry.
Each shot costs up to2L+2 primitive applications plus preparation/readout.

For the full-rank invariant case (or after charging approximate closure
separately), a whitening perturbation bound has error
O(k eta/gamma) per compressed operator and O(k eta/gamma) per normalized seed,
provided k eta<=gamma/4. One way to see this avoids a gratuitous gamma^-2:
work in the true whitened gauge, where
E=G^-1/2 Ghat G^-1/2 has ||E-I||<=k eta/gamma and
||G^-1/2(Khat-K)G^-1/2||<=k eta/gamma.
Conjugating by E^-1/2 perturbs a true contraction by the same order.
The implementable Ghat whitening differs only by an orthogonal alignment.
Clip singular values above1 to restore contraction; clipping increases
distance to a true contraction by at most a factor2.

Taking eta=c epsilon gamma/[k(H+1)] gives uniform length-H scalar prediction
error epsilon after seed errors, and total scalar-shot count conservatively
O(|alphabet| k^4 H²/(epsilon² gamma²)
  log((|alphabet|k²+sk+s)/delta)),
plus seed terms and word-length factor O(L+1).
Finite precision sufficient for Gram margin/whitening and output arithmetic
is paid; this is not an exact-real model.

This makes the missing experimentally meaningful condition explicit:
one must acquire *a controllable frame at the requested task resolution*, or
a source operation that prepares/estimates the requisite normalized
combinations with polynomial variance/cost. Exact linear dimension alone
does not warrant it. However this condition might be sufficient rather than
necessary: a different algorithm could achieve the original task with no
well-conditioned global frame, as the obstruction example shows.

## 5. Candidate routes explored, and why they did not close

A. Greedy Gram-Schmidt:
residual pivots of size>=tau do not give a polynomial minimum Gram eigenvalue;
the change-of-basis coefficient norms can multiply through k stages.
Treating normalized synthetic vectors as native probes hides that cost.

B. Local maximum-volume replacement:
bounding coefficients of each T_a landmark by1 or a constant does not directly
bound all H-step coefficients. Linear combinations can have large transient
coordinate growth despite physical contraction. A sound theorem would have
to bound the whole relevant reachable set or construct a suitable physical
norm without assuming it.

C. Uniform random-word covariance:
the probability of a specific useful word can be exponentially small.
Random-word sampling alone does not supply worst-case controlled reachability.
Partial-shift passwords show why adaptive exploration can be much stronger,
so this is a failure of that proposed algorithm, not a lower bound.

D. Ridge covariance / positive frame compression:
with a current covariance minimum eigenvalue lambda, successor landmark
energy in a newly discovered normalized direction may only be lambda*tau².
Naive repetition multiplies these losses. Positive sparsification can cap
the number of retained terms but does not automatically stop the eigenvalue
or shot-cost degradation.

E. Primary exact-QFA learning:
Qiu, Learning Quantum Finite Automata with Queries, arXiv:2111.14041v2,
uses an amplitude-distribution oracle returning the whole hidden state vector.
That is a stronger source service than noisy scalar Gram readings, and the
paper's polynomial theorem cannot be imported as the missing robust bridge.

Primary source inspected:
https://arxiv.org/pdf/2111.14041, introduction pp1–3, especially the explicit
AD-oracle statement at web-extracted lines39–54 and125–130.
Source ref available to parent: turn24view1 (parent should open before citing).

Balle and Mohri's Learning Weighted Automata, https://cs.nyu.edu/~mohri/pub/cai.pdf,
Theorem6 explicitly includes inverse smallest Hankel singular value and a
supplied complete basis in the statistical sample polynomial. Search located
this exact statement; the complete proof was not reconstructed here.
Source ref turn25search9 (parent should open before citing).

## 6. Recommended scientific claim boundary

It is currently justified to say:
- adjoint-complete scalar access can certify an acquired approximate closure;
- normalized complete representation can require exponentially many shots
  even at fixed contraction norm and known finite rank;
- the same obstruction need not affect the actual finite-horizon scalar task;
- a demonstrated polynomial frame/normalization construction would therefore
  be a substantive missing step, rather than a routine GNS rewrite.

It is NOT justified to say:
- low-rank contractions cannot support polynomial finite-horizon prediction;
- a tiny Gram eigenvalue proves an operationally important hidden mode;
- a greedy local closure search has polynomial total source cost;
- primary exact-state oracle learning proves the noisy scalar acquisition claim.

