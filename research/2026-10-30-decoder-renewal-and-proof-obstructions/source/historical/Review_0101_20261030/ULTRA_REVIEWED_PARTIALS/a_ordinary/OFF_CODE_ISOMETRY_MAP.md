# The actual covariant isometry inverse on the native mixed payload

30 October 2026. This resolves a previously underdetermined interface for
ONE specified ordinary construction. It uses the full operator formula of
2401.10137v3, not only its promise on the isometry range. No new source,
quantum, sampler or optimization run is used.

## 1. Which actual primary circuit is being consumed

The primary constructs a sequential isometry-adjointation instrument by
composing a unitary-inversion comb C' with its Schur/Clebsch--Gordan converter
{T_I,T_O}. The converter is explicit in Section 3.2.1, equations (71),(75)--
(84), and Figure 4; its composition with C' is (85)--(90). The controller C'
is chosen with its stated U(k) x U(k) symmetry (87). This is the covariant
version available without increasing the number of unitary queries.

The exact four-forward-query qubit-unitary inverse cited by the primary
has F_UI=1. Section 3.3/Corollary 6 and the following paragraph use this
conversion for exact deterministic qubit-isometry inversion. The public
result does not mean that four N calls directly supply four adaptive calls
to a purification of N. The separate RDS/PBT service in
`FORWARD_SAR_PORT_AND_LIMIT.md` pays those FORWARD isometry calls, with error.

Let V:C^k -> C^L be the isometry seen by that supplied circuit, and Pi=VV^*.
For our native Stinespring dilation L=rD. Let f=F_UI and define

    v=(k^2 f-1)/(k^2-1).                                    (S1)

I use v for the depolarizing coefficient to avoid equating a channel fidelity
with a depolarizing mixing parameter. The load-bearing primary formulas are
Appendix A.4, equations (208)--(225), in particular (217),(219),(225).

## 2. Full off-code source formula, not an inferred completion

For an arbitrary input operator X on C^L, the actual covariant construction
has two logical-output branches

    D_I(X)=v V^*XV + [(1-v)Tr(Pi X)
                         + alpha Tr((I-Pi)X)] I_k/k,
    D_O(X)=(1-alpha)Tr((I-Pi)X) I_k/k,                      (S2)

where alpha is the converter's detection error, given by its explicit known
comb/Sigma contraction (primary (218)). Its precise value is irrelevant for
the unflagged map. These are equality statements on ALL operators X, hence
also on arbitrary entangled references. They do not presume X diagonal in
the code/complement decomposition.

The primary proves (S2) as follows, and the structure can be reconstructed
without any numerical controller coefficients. Equation (190) makes T_I
commute with simultaneous physical U(L) rotations. The stabilizer subgroup
I_ran(V) direct-sum U(ran(V)^perp) therefore kills all code/complement cross
blocks and makes the complementary block scalar on the input space. This
gives its exact decomposition (194). The code block is the Haar average
of a common k-dimensional U V^* input and the matching n queries U, as in
(200). Composing the covariant inverse C' gives its depolarized inverse
with coefficient v, equations (209)--(211). The remaining output commutes
with every U(k), so it is a multiple of I_k/k, equations (212)--(218).
Trace preservation fixes the O-branch mass, and the two frame symmetries
force its logical output to be maximally mixed, equations (220)--(225).

Consequently, discarding the measurement outcome gives exactly

    D_V(X)=v V^*XV + [Tr X-v Tr(Pi X)] I_k/k.                (S3)

For the four-query exact unitary controller f=1 and v=1, this becomes

    D_V(X)=V^*XV + Tr((I-Pi)X) I_k/k.                       (S4)

Thus the mathematical bad completion from the earlier interface analysis
is in fact the completed channel of this SPECIFIED covariant source
construction. This is stronger than its abstract range-only promise.

It is not a uniqueness assertion for all conceivable isometry-inversion
circuits. Noncovariant constructions, different converters, and modified
controllers retaining additional workspace are not ruled out by (S4).

## 3. Exact native mixed-payload contraction for every r

Write U_j psi=U(psi tensor |j>), K_j=U_j/sqrt(r), and

    V psi=sum_j |j>_E tensor K_j psi,
    N(rho)=sum_j K_j rho K_j^*,  K_i^*K_j=delta_ij I_k/r.

The native payload is B only. Attach an independent maximally mixed register
of the public environment dimension, defining X_rho=I_E/r tensor N(rho).
Then

    V^* X_rho V
       =r^-1 sum_j K_j^* N(rho) K_j=r^-2 rho,
    Tr(Pi X_rho)=r^-2.                                    (S5)

Both identities hold for arbitrary references. They also hold in EVERY
random environment frame of the RDS output: I_E/r is invariant, while the
discarded frame rotates only E. There is no conditioning on, or intervention
on, a hidden native junk draw.

Substitution in (S3) yields the actual complete native logical map

    Lambda_f,r(rho)=(v/r^2)rho+(1-v/r^2)I_k/k.              (S6)

Its entanglement fidelity and complete half-diamond error are

    Fe=1/k^2+(f-1/k^2)/r^2,
    error=1-Fe,                                           (S7)

in the regime v>=0 used here. The latter follows from the ordinary
depolarizing/Pauli channel, not a generic fidelity conversion. For the
four-query exact inverse f=1,

    Fe_4(r)=1/k^2+(1-1/k^2)/r^2.                           (S8)

At qubit r=2 this is 7/16=.4375. The general inequality f<=1 caps this
entire specified unitary-controller/converter family by (S8), no matter how
many unitary-controller queries are added. This is a representation-family
cap after replacing the lost environment by an INDEPENDENT I/r, not a bound
on native adaptive recovery in general.

In particular increasing the precision of the forward SAR service makes
the implemented map converge to (S6); it cannot make its lost factor1/r^2
disappear. With m=4 isometry slots, the paid service uses
O(1/sqrt(epsilon_SAR)) original forward N queries to obtain a logical
channel within epsilon_SAR of (S8), plus its known-controller errors. Four
isometry calls have NOT become four original N calls. The small rank-two
number here must not be compared to the two-query parallel bound as though
the acquisition costs were equal.

## 4. The actual heralded branches and the reset debt

For f=1, (S2) on the native input becomes

    Lambda_I(rho)=r^-2 rho + alpha(1-r^-2) I_k/k,
    Lambda_O(rho)=(1-alpha)(1-r^-2) I_k/k.                  (S9)

Their probabilities are independent of rho:

    p_I=r^-2+alpha(1-r^-2),
    p_O=(1-alpha)(1-r^-2).                                (S10)

The I branch is a noisy depolarizing output except when alpha=0. Hypothetically
letting alpha tend to0 would give an almost exact branch of throughput only
1/r^2. The O branch is an entanglement-breaking replacement at the published
logical-output interface. In particular it is NOT a restoring draw carrying
the original quantum payload on that output. One cannot retry the same
unknown logical state after replacing it by I_k/k.

This is not a statement that every possible physical dilation of the circuit
erases the information from its entire environment. The source converter
discards physical irrep registers and, on certain paths, uses trace-and-
replace steps (primary (79),(82),Figure4). Retaining all such workspace and
coherently modifying the controller would be a DIFFERENT native operation.
Its existence and a known reset/return map would have to be constructed and
charged. Neither a free inverse of the four-query circuit nor a projection
onto its unknown final workspace follows from its CPTP code-inversion claim.

## 5. Literal source admission and cost limits

The controlling proof was read in the saved exact primary2401.10137v3 bytes:
Section3.2.1, equations71--93 and AppendixA.4, equations189--225. The latter
contains the actual full off-code map, which is why no reconstruction of the
particular four-query unitary circuit's internal amplitudes is necessary.
Every covariant exact unitary controller in that conversion gives the same
unflagged (S4). Alpha may depend on its exact controller but cancels in (S3).
No numerical alpha, hidden gap, output-state oracle or new model was supplied.

The primary gives a known-CG implementation with gate complexity
O(poly(n,L,log(1/error))) in the PHYSICAL isometry output dimension L; here
L=rD. I do not turn this displayed bound into poly(log D), or count a generic
large-dimensional Schur/CG gate as free. The four isometry slots themselves
are acquired by the separate public PBT/RDS service with its quantum store,
controller preparation and approximation budgets. These costs are distinct
from merely citing the four-query headline. They are not an improvement over
the existing O(k^2 r^2/epsilon) native full-throughput recovery upper bound.

Conclusion: the primary specified covariant macro does have a completely
determined mixed-payload map and does NOT close the scalable recovery gate.
The missing operation remains a different coherent native history or a
genuinely paid restoring interface, not a more accurate invocation of this
range-only inversion macro. No claim excludes such an operation.
