# Physical permutation twirling and a moving singlet subcode

2026-10-29. Author derivation pending independent review. This document is a
new load-bearing construction; it is not covered merely by acceptance of the
matching-survival witness. Historical novelty is not claimed.

## 1. General multiplicity-one intertwiner theorem
Let U be an irreducible unitary representation of a finite group G on L,
dim(L)=d. Let W be a representation on physical output H, with U occurring
exactly once, through an isometry V:L->H satisfying W_g V=V U_g. Let M and M'
be arbitrary finite-dimensional input/output source memories. Let T be any
CPTP map L tensor M -> H tensor M', with Kraus operators K_a. Actually apply
U_g before the call, W_g* after it, with fresh uniform private g, and average
out/retire g. The resulting map is

  Tbar = E_g (Ad_Wg* tensor id) T (Ad_Ug tensor id).

For each a define the memory operator

  B_a = (1/d) Tr_L[(V* tensor I) K_a],
  R_a = K_a - V tensor B_a,
  R_a,g = (W_g* tensor I) R_a (U_g tensor I).

The partial trace here contracts the L output/input indices after V*, leaving
an operator M->M'. The group average of K_a is V tensor B_a: averaging each
memory matrix element projects Hom(L,H) onto its one-dimensional intertwiner
space. Therefore E_g R_a,g=0. Expanding the Kraus sum, the cross terms cancel
for EVERY joint input, including inputs correlated with memory or a reference:

  Tbar = Ad_V tensor B_good + T_bad,
  B_good(sigma)=sum_a B_a sigma B_a*,
  T_bad(rho)=E_g sum_a R_a,g rho R_a,g* .                 (1)

Both terms are CP. This is a mathematical CP instrument, not an observed
syndrome, an acquired noise model, or a mixture of Pauli/unitary errors.
Trace preservation and covariance give

  T_bad*(I_HM') = I_L tensor H_bad,
  H_bad=I_M - sum_a B_a*B_a >=0.                         (2)

Thus its bad-event probability depends only on the memory marginal, even
when the carrier is entangled with that memory.

## 2. Stronger memory-marginal closure
Let F=Tr_H composed with T_bad. Covariance makes F invariant under every
Ad_Ug on the carrier input. Averaging that input and using irreducibility,

  F(rho_LM) = F(I_L/d tensor Tr_L rho_LM)
            = B_bad(Tr_L rho_LM),                       (3)
  B_bad(sigma)=Tr_H T_bad(I_L/d tensor sigma).

B_bad is CP, with trace effect H_bad. Moreover B_good+B_bad is a TP memory
channel. Equation (3) holds as a channel identity, including arbitrary external
reference systems. It is stronger than input-independent branch probability.
The bad branch can leave quantum correlations between output carrier and
memory. It cannot, after the group key is retired, transmit fresh information
from the carrier into the memory MARGINAL. Refined Kraus labels or a retained
key are different interfaces and need not satisfy this statement.

## 3. Single-call norm and matching witness
For any fixed memory state sigma, trace the output memory. Equation (1) is

  Tbar_sigma = (1-p_bad) Ad_V + p_bad R_sigma,

where R_sigma is a channel when p_bad>0 and p_bad=Tr(H_bad sigma). The
normalized Choi state of R_sigma is orthogonal to |V>>/sqrt(d), because every
R_a,g has zero partial intertwiner coefficient. Equivalently

  p_bad=1-F_raw,P(T_sigma),
  F_raw,P(T_sigma)=sum_j |Tr(V* A_j)/d|^2,

for reduced source Kraus operators A_j:L->H. Consequently

  (1/2)||Tbar_sigma-Ad_V||diamond = p_bad.               (4)

The upper bound follows by the channel-mixture expression. A maximally
entangled input attains the lower bound since the good and bad Choi supports
are orthogonal. This is a statement about the actually averaged channel with
a fixed initially independent sigma; the full-memory statement is (1)-(3).

For n=2m>=4 qubits take L to be the full singlet sector P, H=(C^2)^tensor n,
and W_g physical permutations. Schur-Weyl decomposition has S_n shapes
(m+j,m-j), each with spin multiplicity 2j+1. The input shape (m,m) appears
once, at j=0. Thus all hypotheses above hold even if T leaks outside P.
No physical projection onto P, singlet measurement, or reset is required
merely to obtain (1)-(4).

The random-matching singlet survival theorem gives, for every sigma,

  p_bad(sigma) <= C_n q_matching(sigma),
  C_n=(n+2)/(n-1).                                      (5)

That theorem already bounds raw projected entanglement infidelity, so leakage
is included. Since (5) holds for every memory density operator, it is the
operator inequality H_bad <= C_n E_fail, where E_fail is the test failure
effect on memory. It does not presume that the current service carrier is
independent of memory; (2) supplies the needed correlated-input transfer.

## 4. Fixed proper subcode, physically moved before the call
Choose ANY isometry E:C^K->L, including K a power of two. The service is:
encode with V E, apply physical permutation W_g, use the source, apply W_g*,
then use any fixed TP decoder D:H->C^K that exactly inverts V E on its code.
For example D(X)=E*V* X V E + Tr[(I-VEE*V*)X] tau_K with any density tau_K.
The physical permutations intentionally move the code through its orbit;
E's image is NOT required to be invariant under them.

Restricting (1) and applying this decoder yields exactly

  Sbar = id_K tensor B_good + S_bad,
  S_bad=(D tensor id) T_bad (Ad_E tensor id),
  S_bad*(I)=I_K tensor H_bad,
  Tr_K S_bad(rho_KM)=B_bad(Tr_K rho_KM).                 (6)

Thus the matching bound uses C_n, not (d/K)C_n, for these moving-subcode
services. This removes the localization penalty by changing the actual
service operation, not by strengthening the old fixed-subcode theorem.
A logical Pauli twirl is not required for (6). For independent fixed sigma,

  (1/2)||Sbar_sigma-id_K||diamond <=p_bad<=C_n q.

Equality with 1-F_e(Sbar_sigma) is not asserted: reset decoding can turn some
raw bad/leakage weight into identity overlap. The physical bound remains sound.

## 5. Guard and arbitrary-error outer-code bridge: precise obligations
Apply one fresh independent group key per service call and use the same
physical-source boundary as the matching tests. A private role chooses test
with probability a and service with probability s. Existing sequential guard
proofs may be used only after checking their actual stopping/selection rules.
Equations (2),(5) give the per-history hazard inequality with R=C_n s/a for
all actual conditional quantum states, including memory-carrier correlation.
No joint latent Pauli model is assumed.

On a virtual branch with at most t bad service slots, its entire data-memory
Kraus operators are identities on all other slots. They therefore belong to
the linear span of arbitrary operators supported on at most t slots, tensored
with memory operators. An outer code correcting ALL t-slot quantum errors
corrects this span (including coherent errors and memory correlations) by the
Knill-Laflamme condition. A merely classical decoder success claim on sampled
Pauli histories does not alone establish this quantum correction obligation.

Equation (3), with TP local decoding/recovery, also closes the reduced memory
process on each virtual good/bad and observed test history. Subject to source
controllers using only that memory and the allowed classical history, the
accepted memory instrument B_acc is exactly independent of payload input after
keys are retired. This can be proved by induction on calls, tracing processed
carrier outputs and using (3) at every service. The operator-valued accepted
bad-event tail is bounded by epsilon whenever the guard's all-input hazard
proof establishes that bound. If the accepted map after outer recovery splits
A_acc=id_payload tensor B_le_t + A_gt_t, then

  Tr_payload A_gt_t = B_gt_t composed with Tr_payload,
  ||A_gt_t||diamond=||B_gt_t||diamond<=epsilon,
  B_acc=B_le_t+B_gt_t,
  (1/2)||A_acc-id_payload tensor B_acc||diamond<=epsilon. (7)

The last line follows by subtracting the two CP maps A_gt_t and
id tensor B_gt_t and using their norm bounds. It uses the aggregate bad-event
effect, not a sum of separate branch norm estimates. Retaining a dummy-payload
memory simulator gives a safe weaker fallback if an implementation violates
the exact memory-closure hypotheses but still proves the all-input tail.
No normalized conditional guarantee, nonzero yield, safe recovery on abort,
or unrestricted positive quantum capacity follows from (7).

## 6. Physical implementation and explicit boundaries
Uniform S_n permutations can be sampled by Fisher-Yates using n-1 uniform
bounded-integer draws. Rejection sampling from fair bits is exact, with
expected O(n log n) bits. Capping each draw's number of attempts at R costs
at most O(n log n R) bits and has failure probability <=(n-1)2^-R; abort on
sampling failure. All sampling, flags, routing settings and keys are private.

Any permutation is a product of at most n-1 unrestricted transpositions;
actual pre/post permutations cost at most 2(n-1) physical SWAP gates on a
fully connected architecture (a SWAP is 3 CNOTs if no native SWAP). On a line,
each permutation costs at most n(n-1)/2 adjacent swaps, with O(n) parallel
depth via a sorting network. Its inverse must also be implemented. Local
learned frames conjugate these permutations, adding the corresponding known
single-qubit rotations. Initial encoding, final decoding, storage, key
handling and source/control boundary errors remain paid. Group averaging does
not make incorrect gates or information leaks harmless.

Finite keys must remain hidden from the source during all relevant subsequent
calls and retired from the output covered by (1)-(7). Keeping g as an explicit
output generally preserves the scalar/residual cross terms in each key block;
those guarantees then need a new proof. A source acting during the routing
rather than only at the declared port also lies outside the ideal theorem
unless its complete control-plus-source channel is explicitly accounted for.

A random logical Pauli pad uses about 2 log2(K) secret bits, whereas naive
physical permutation selection uses log2(n!)=Theta(n log n) bits. The proposed
substitution can reduce logical compilation work but increases key demand and
may increase routing. No practical total-cost advantage has been established.

## Primary comparison
Jenčová and Plávala, arXiv:1603.01437v3, Section 4.1, Proposition 1, establishes
maximally entangled optimal inputs for discriminating covariant channels when
the input representation is irreducible. Read 2026-10-29 at
https://arxiv.org/html/1603.01437 . The scalar-memory version of (4) belongs to
this established covariance framework; no new general diamond-norm principle
is claimed. Equations (1)-(3) are directly proved above, including memory and
multiplicity-one physical leakage. The important program transfer is physical
permutation control plus the matching witness and a moving qubit subcode.
