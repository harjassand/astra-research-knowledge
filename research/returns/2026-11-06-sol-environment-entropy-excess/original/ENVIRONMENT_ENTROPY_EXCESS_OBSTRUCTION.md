# The environment boundary scale cannot be made uniformly effective for free

This is an authored obstruction to a proposed way of completing the full
COMMON_QUESTION.md. It does not prove ordinary-capacity noncomputability
or construct its evaluator. It is independent of the four constructors'
developing work, which has not been read.

## 1. Exact stationary input and output identities

Fix a finite channel N and ANY stationary input process with consistent
finite physical states rho_n. Let B^n,E^n be its actual receiver and true
complementary output processes, with entropy rates h_B,h_E. Stationarity
and subadditivity give

    e_B(n)=S(B^n)-n*h_B>=0,
    e_E(n)=S(E^n)-n*h_E>=0,
    I_c(rho_n,N^n)=n*(h_B-h_E)+e_B(n)-e_E(n).       (1)

The processes need not have a known memory dimension, be Markov, mix,
or admit a physical stationary resource at Bob. The rho_n are ordinary
input states. In particular

    I_c(rho_n,N^n)>=n*(h_B-h_E)-e_E(n).            (2)

Only the ENVIRONMENT excess needs an upper bound. A receiver excess is
favourable. Replacing both sides by absolute memory bounds loses this
one-sided distinction.

## 2. Effective excess plus a uniform rate gap would give a finite test

Consider a computable family of finite rational channels N_z, with
Q(N_z)=0 on no instances and Q(N_z)>0 on yes instances, for which that
yes/no promise is undecidable. This section is a conditional structural
lemma for ANY such family. The ordinary zero-versus-positive family is
reported in the read N684/N1677/N1680 source lineage; the lemma does not
reprove or strengthen that lineage.

Suppose a proposed reduction supplies a computable g_z>0 and, on every
yes instance, a stationary ordinary input process with

    h_B-h_E>=g_z.

If it ALSO supplies a computable integer n_z for which

    e_E(n_z)<=n_z*g_z/2,                           (3)

then (2) gives

    (1/n_z) Q^(1)(N_z^n_z)>=g_z/2 on yes,
    (1/n_z) Q^(1)(N_z^n_z)=0 on no.               (4)

Finite-block coherent-information maximization over its finite compact
state space is computable, with a certified entropy-continuity net.
Approximating (4) to g_z/8 separates the two promises. Thus the proposed
pair of operations is impossible for an undecidable family.

The witness process need not itself be acquired. The contradiction uses
the existential state in the FINITE block and a computable maximization
over every physical input state of that block. It pays the entire block
description and precision cost; it does not claim efficiency.

This rules out several generic proposed supplies of (3):

* A computable bound e_E(n)<=K_z for all n: take
  n_z>=2K_z/g_z.
* A computable sublinear envelope b_z(n) for e_E(n), with an actual
  computable way to reach b_z(n)/n<=g_z/2.
* A uniform effective convergence bound on the environment conditional
  entropies S(E_i|E^{i-1}) to h_E whose cumulative error gives the previous
  envelope. An exponentially decaying bound with computable prefactor
  and exponent is more than sufficient.

An uncomputable memory-dependent bound, such as 2log D with an unknown
finite witness dimension, does NOT supply (3) effectively. That is exactly
the scale a successful uniform ordinary-rate-gap construction may retain.

## 3. What a mixer proof must actually establish

A dimension-independent Hilbert--Schmidt spectral gap of the retained
memory, or exponentially decaying bounded-observable two-point
correlations, is not an environment conditional-entropy bound of the
kind above. The actual environment has an arbitrarily long quantum
history, with transmitted mixer purifiers and erasure flags retained.
Conditioning on that history changes the relevant object.

This does not by itself prove that no mixer can earn a positive rate.
It says that simultaneously claiming a uniform computable rate gap and
an effective environment excess scale would contradict the hard family.
A proof may preserve a positive rate while leaving a genuinely
noneffective boundary scale; the ordinary capacity question allows that.
Conversely a strong history-convergence estimate may be valid while
the claimed positive bulk rate fails. The actual signed-rate inequality
cannot be replaced by either property in isolation.

The read N1680 exact Bell-chain history example already disproves an
automatic telescoping claim. The present deduction identifies the ONE
output whose effective excess would be enough for a finite certificate,
and applies to any stationary-source representation, not merely that
specific encoder or a catalyst architecture. It remains a method
constraint, not the full negative answer.

## 4. Ordinary primary comparator

The governing strong-converse source read is Beigi--Tomamichel,
arXiv:2609.11771v1, especially Theorems1--2 and section5:
https://arxiv.org/html/2609.11771v1 . Its actual low-fidelity-to-high-fidelity
conversion uses a projective-norm-controlled channel-image projector.
Its above-capacity fidelity theorem does not supply (3), a below-capacity
activation cutoff, or a terminating upper evaluator for Q. This is a
scope comparison, not a criticism of its proved strong converse.

The N1680 finite stationary-source variational characterization and
unresolved entropy-rate remainder are in the exact available original:
/Users/harjas/Documents/ChatGPT/coordination/work/astra-capital-successor-20261030/repo/research/2026-11-03-p1-ordinary-capacity-resource-interface/source/p1/COMPLETE_VISIBLE_RESPONSE.txt
The unavailable offered package remains unavailable. No extra review
or reconstruction of its held original was performed.

The full ordinary evaluator question stays open in this lead construction.
