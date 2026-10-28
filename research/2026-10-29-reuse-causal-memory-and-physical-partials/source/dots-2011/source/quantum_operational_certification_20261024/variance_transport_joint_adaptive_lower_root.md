# Variance-sensitive complete transport for rare quantum recovery

27 October 2026. Root proof candidate for independent receiving. Separate
from the already received conservative complete-transport rank theorem.
No complete relative-entropy SDPI for the datum channel is assumed.

## 1. A receiver-variance transport lemma

Let the heat flow on a compact parameter manifold act entrywise on every
finite matrix algebra. Suppose its conditional matrix entropy obeys

    E_t <= exp(-a t) E_0,       I_t = -E'_t.

Here E_t=D(rho_t || E rho_t), and E averages the parameter but leaves the
quantum-memory algebra fixed. For a Hermitian matrix-valued test f,
suppose the following OPERATOR bound holds at every parameter:

    Gamma(f,f) <= L^2 K,

where K>=0 is constant on the parameter manifold. Put
q=Tr(rho_bar K). Then

    | integral Tr[(rho_theta-rho_bar) f(theta)] d pi |
           <= 2 L sqrt(q E_0/a).                           (1)

### Proof, including the noncommuting memory

For a faithful matrix density, the logarithmic-mean chain rule gives
partial_j rho = [rho](partial_j log rho), where
[rho](X)=integral_0^1 rho^s X rho^(1-s) ds. Integration by parts and
Cauchy--Schwarz in this positive quadratic form imply

    |d/dt integral Tr(rho_t f)|
      <= sqrt(I_t) sqrt(integral sum_j Tr[(partial_j f)
                                      [rho_t](partial_j f)]).

The logarithmic mean is bounded by the arithmetic mean. Since f and all
its derivatives are Hermitian, the second squared factor is at most
integral Tr[rho_t Gamma(f,f)] <= L^2 Tr(rho_bar K)=L^2 q.
The memory mean is invariant under heat flow; no pointwise domination
rho_t(theta)<=C rho_bar is invoked.

For 0<b<a, integration by parts and entropy decay give

    integral_0^infinity exp(bt) I_t dt <= a E_0/(a-b).

Weighted Cauchy--Schwarz, with b=a/2, yields
(integral sqrt(I_t)dt)^2 <= 4 E_0/a. Integrating the pairing derivative
proves (1). Faithful regularization on the support of rho_bar and the
finite-dimensional limit handle singular program ensembles. With the
normalized matrix trace one uses the density m rho_theta; both entropy
and pairing reduce to the ordinary physical traces displayed here.

For SU(N) in the Hilbert--Schmidt metric, a=N is available from positive
Ricci=N/2 and complete MLSI. The exact convention and primary source are
recorded in `complete_transport_adaptive_query_principle_root.md`:
[Brannan--Gao--Junge, Theorems 4.3/4.5 and Definition 2.3](https://arxiv.org/html/2007.06138).
The direct heat-flow calculation above is special to this matrix-valued
diffusion setting and does not silently change a general noncommutative
gradient representation.

## 2. Canonical hidden rank/signal family

Let integers 1<=r<=D, p=r/D, and let P_r be a fixed rank-r projection on
the D-dimensional flag space. The unknown channel is

    E_U(X)=U [ X tensor P_r/D
          + (Tr X) I_3/3 tensor (I_D-P_r)/D ] U*,
    U in SU(3D).

The success code has mixed flag rank r and signal p. Its replacement
noise is orthogonal to that code, so known-source full-p recovery exists.
The actual datum mean E_U(I_3/3)=I_(3D)/(3D) is independent of U.

We allow arbitrary finite-dimensional coherent adaptive calibration,
with at most n physical channel calls before the datum arrives. The
learned accepted-plus-erased channel is required, for every U, to be
within unhalved error p/4 of (p id, (1-p) erasure).

## 3. Exact operator variance bound for a decoder test

Write P_a(U)=U(|a><a| tensor P_r)U*, and
P_code=sum_a P_a. For a Hermitian test with label blocks H_a on
program P tensor physical B, put Hbar=(H_0+H_1+H_2)/3. The labeled datum
has three uniform classical labels. Its associated matrix-valued test
has U-dependent part

    f_H(U) = (1/(3D)) sum_a Tr_B[P_a(U)(H_a-Hbar)]
                 + a U-independent term.

Consequently, with X=sum_a[P_a,H_a-Hbar], operator-valued Parseval gives

    Gamma(f_H,f_H)=Tr_B(X*X)/(9D^2).                       (2)

For a B-only projection P and Hermitian H,

    Tr_B [P,H]*[P,H] <= 4 Tr_B H^2.                       (3)

Indeed (A-B)*(A-B)<=2A*A+2B*B with A=PH,B=HP gives terms
2HPH+2PH^2P. The first is bounded by 2H^2 before the partial trace.
For the second, partial-trace cyclicity in the B-only projection gives
Tr_B PH^2P<=Tr_B H^2. This is NOT the false rank-sensitive inequality
Tr_B HPH<=rank(P) I in the presence of quantum memory.

Using X*X<=3 sum_a [P_a,H_a-Hbar]*[P_a,H_a-Hbar] and

    sum_a(H_a-Hbar)^2 = sum_a H_a^2 - 3 Hbar^2 <= sum_a H_a^2,

we obtain the POINTWISE operator bound

    Gamma(f_H,f_H) <= (12/D) K_H,
    K_H=(1/(9D)) sum_a Tr_B H_a^2.                        (4)

K_H is independent of U and positive on program memory. There is no
program-dimension factor and no rank(P_code) substitution. Applying (1)
with a=3D gives the variance-sensitive correlation inequality

    |Tr[(sigma_PAB-rho_bar_P tensor tau_AB)H]|
                   <= 4 sqrt(q_H I(U:P))/D,                (5)
    q_H=Tr(rho_bar_P K_H),  tau_AB=I_A/3 tensor I_B/(3D).

## 4. Adaptive information paid by physical source calls

For a conditional input rho_QM^U, the output relative entropy to
I_B/(3D) tensor rho_M^U is exactly

    p D(rho_QM^U || I_3/3 tensor rho_M^U) <= 2p log 3.

This follows by decomposing the fixed active/inactive flag blocks
before U; the reference state is U-invariant. Subtracting the
corresponding relative entropy of the average output gives
I(U:BM)-I(U:M), which is no larger than the displayed average conditional
relative entropy. Since I(U:M)<=I(U:QM), each physical query increases
learner information by at most 2p log 3. Therefore

    I(U:P)<=2np log 3.                                    (6)

This holds for coherent adaptive inputs, not only known fresh probes.
All processing and erasure/abort branches are retained; initial memory
is independent of U.

## 5. Rare acceptance supplies the necessary variance factor

Let T_a be the final decoder's effect for accepting and correctly
reporting logical basis label a. These are positive effects on P,B with
sum_a T_a<=I. Set H=sum_a |a><a| tensor T_a. Because T_a^2<=T_a,

    q_H <= q_accept/3.

The actual marginal on P,B equals rho_bar_P tensor I_B/(3D), since the
uniform input datum has this same physical mean for every U. Thus the
acceptance probability here is exactly the same in the actual experiment
and in the product baseline.

Complete unhalved error <=p/4 implies

    s_correct >=7p/8,     q_accept <=9p/8.

Hence the correlation witness obeys

    Tr[(sigma-rho_bar tensor tau)H]
          =s_correct-q_accept/3 >=p/2,
    q_H<=3p/8.

Combine (5),(6) to obtain

    p/2 <= 2p sqrt(3n log 3)/D,
    n >= D^2/(48 log 3) >= D^2/128.                       (7)

The last conservative constant follows from log 3<2. The exact
48 log 3 expression is the primary constant. This closes the candidate
joint r^2/p^2 exponent for arbitrary adaptive PRE-DATUM calibration on
the canonical grid, without a relative-entropy SDPI or estimation oracle.

## 6. Separate all-real-p reduction

For arbitrary integer r>=1 and 0<p<=1, take D=floor(r/p), p'=r/D and
c=p/p'. Then 1/2<=c<=1 and D>=r/(2p). Locally dilute each base-channel
output by a known erasure map with survival c. One base physical call
simulates one target call exactly, including inputs entangled with an
unknown adaptive memory. The resulting channel is still rank-r success
plus a fixed orthogonal replacement state, now with signal p.

Apply the canonical transport calculation to the decoder effects pulled
back through the known datum erasure map. They remain positive with sum
at most I, and their baseline acceptance is the target acceptance.
Thus q_H<=3p/8 and the correlation witness is at least p/2. For the
simulated adaptive program we may conservatively use the BASE budget
I(U:P)<=2n p' log 3. This yields

    n >= c D^2/(48 log 3)
       >= r^2/(384 p^2 log 3)
       >= r^2/(1024 p^2).                                 (8)

No heralded training success is treated as free. The known output map
is a deterministic CPTP erasure channel, not postselection. The exact
complete-instrument comparison uses the actual target signal p,
not p', throughout.

## Scope and unresolved questions

The proposed result is a worst-case source-family query lower bound at
fixed relative error. The all-p family uses output dimension O(r/p);
it does not assert this scaling for every fixed ambient dimension or
every replacement state. The comparison is with the existing consumed-
program recovery upper bound's rank/signal query exponents, not its gate,
memory, energy, constant or logarithmic costs.

Post-datum/interleaved source calls, indefinite causal order, environment
or purified-source access, reusable programs, expected-query guarantees,
and complete datum-relative-entropy SDPI remain outside the claim.
The source family's known structure is available equally to both sides.
All original physical preparations, all branches and the fixed query cap
are explicit. Independent full receiving and historical novelty assessment
are separate obligations; this file is currently a candidate.
