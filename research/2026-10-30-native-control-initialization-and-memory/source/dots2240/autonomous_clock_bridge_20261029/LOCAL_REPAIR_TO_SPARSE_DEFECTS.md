# A local repair certificate can replace a global mixing assumption

2026-10-29. Root construction under review. Intended use: the repaired two-site lease model may lack the exact scalar defect drift of the many-body guarded model. This theorem gives a different sufficient interface, but its hypotheses must be established for an actual mechanism before claiming that implementation.

## Hypotheses stated as checkable local operations

On a bounded-degree finite interaction graph, let L be a bounded finite-range clean Lindblad generator and B_x a commuting family of local bad-site projectors. Require:

1. No creation: L*(B_x)<=0 on the FULL physical Hilbert space, not only legal clock states.
2. Uniform local healing at a fixed time delta>0: exp(delta L*)B_x <=(1-c)B_x, with explicit c>0 independent of volume and x.
3. Bounded local generator strength and range, so iterated local derivatives obey ||L*^k B_x||<=C0^k k! and have radius at most k times a fixed interaction diameter. Choose delta C0<1.

No creation makes the adjoint B_x corner invariant. Indeed 0<=A<=B_x implies 0<=exp(tL*)A<=exp(tL*)B_x<=B_x. Linear extension shows every B_x-supported Hermitian operator stays in that corner; hence every derivative L*^k B_x is B_x-supported. This is what permits a RELATIVE Taylor error, not merely a global absolute error.

By bounded local loss, L*B_x>=-nu B_x for explicit nu (use its norm inside the invariant corner). Positivity therefore gives exp(tL*)B_x>=exp(-nu t)B_x. Set a=(1-exp(-nu delta))/nu, with a=delta if nu=0.

## Finite-support Lyapunov operator

The exact integral G_x=int_0^delta exp(tL*)B_x dt satisfies

    a B_x<=G_x<=delta B_x,
    L*G_x=exp(delta L*)B_x-B_x<=-c B_x.

Define the finite local polynomial

    F_x=sum_{k=0}^m delta^(k+1)/(k+1)! L*^k B_x.

With q=C0 delta<1,

    ||F_x-G_x||<=delta q^(m+1)/(1-q),
    ||L*F_x-L*G_x||<=q^(m+2)/(1-q).

Because BOTH differences are B_x-supported, these norms imply order bounds by the same constants times B_x. Choose m so the first is <=a/2 and the second <=c/2. Then

    (a/2)B_x<=F_x<=(3delta/2)B_x,
    L*F_x<=-(c/2)B_x<=-r F_x,
    r=c/(3delta).

F_x has explicitly bounded finite support. Put Z_x=F_x/b with b=3delta/2; then 0<=Z_x<=B_x<=I and B_x<=K Z_x, K=3delta/a. Its support radius R and K,r depend on local parameters, not volume/runtime.

## Products, perturbations, and arbitrary retained baths

Pack any marked set S into a subset S' of size at least |S|/P with buffers large enough that every clean/noise local term touches at most one Z_x. P is a bounded ball-volume constant. For a packed set U, locality gives

    L*(product_U Z_x)<=-r |U| product_U Z_x.

Let Hermiticity-preserving perturbations N_e annihilate I in the adjoint, with a legitimate total evolution and local norm sum at most eta_R over terms touching one Z support. The bath may be arbitrary and retained, provided system–bath interaction terms satisfy the declared bounded physical-support norm budget. Bath-only terms commute with every Z.

If e touches x in U, then N_e*(product_U Z)=N_e*(Z_x) product_(U\x)Z <=nu_e product_(U\x)Z. Consequently the moments obey

    m'_U<=-r |U| m_U + eta_R sum_{x in U}m_(U\x).

Starting clean, induction gives m_U(t)<=(eta_R/r)^|U| for all times. Since the B_x commute, the probability that every original marked box is bad is bounded by

    Tr[B_S rho(t)] <=Tr[B_S' rho(t)]
       <=K^|S'| m_S'(t)
       <=p^|S|,
    p=(K eta_R/r)^(1/P), provided K eta_R/r<1.

This is a uniform joint equal-time bound. It is stronger than local expectation stability, and requires no global spectral gap or full-state mixing assumption. Constants can be very poor because packing grows with the local polynomial radius.

## Status of the intended application

The guarded model already has stronger direct product drift and does not need this detour. For two-site leases, the proposed missing-owner/missing-partner repairs are designed to vanish on clean histories. However no creation of the complete bad-site flags, a full-space healing certificate, and their exact support definitions still require proof. This document does NOT certify leases simply by stating these hypotheses.

Nor does sparse controller damage imply a quantum-data threshold. Data faults generated before a controller heals must be propagated through an actual fault-tolerant architecture. The separate physical-time insertion norm and clock-stall theorems remain relevant but are not interchangeable with that obligation.

## Extension: a finite healing time need not fit one Taylor disk

Root derivation, 20:32 UTC, pending review. Replace hypothesis2 by exp(T L*)B_x<=(1-c)B_x at any explicit fixed finite T. The local polynomial can still be constructed without applying an extensive generator norm to a small error.

Suppose local terms have support size <=r0 and per-site sum of adjoint norms <=J. Put a_int=max(1,r0−1), C=J a_int. For an observable O on s sites, expansion into connected interaction sequences gives

    ||L*^k O|| <= C^k (s)_k ||O||,

where (s)_k=s(s+1)...(s+k−1). Each sequence can add at most a_int sites per step, and summing terms intersecting its support costs at most J times that support size. Thus for delta C<=1/4,

    ||exp(delta L*)O-Q_K(L*)O|| <=2^(s-K-1)||O||,

with Q_K(z)=sum_(k=0)^K (delta z)^k/k!. The bound follows from binom(s+k−1,k)<=2^(s+k−1). The integral polynomial R_K(z)=(Q_K(z)-1)/z has corresponding error <=delta 2^(s-K)||O||. Here R_K is a polynomial, including its value delta at z=0.

Choose M=ceil(max(1,4CT)), delta=T/M, and

    epsilon=min(c/8, a/[8(1+T)],1/8),
    a=(1-exp(-nu T))/nu.

Initialize O_0=B_x,F_0=0. At stage j choose K_j from the actual bounded support size of O_(j−1), large enough that the exponential error is <=epsilon/M and the integral error <=delta epsilon/M. Define

    O_j=Q_(K_j)(L*) O_(j−1),
    F_j=F_(j−1)+R_(K_j)(L*) O_(j−1).

CPTP adjoint contractivity and telescoping show ||O_j-exp(j delta L*)B_x||<=j epsilon/M, so ||O_j||<=2. This supplies a priori norms for choosing the next K_j. Finite range gives a recursively computable support bound independent of total volume. It may grow extremely quickly with the fixed local parameters; no practical efficiency is claimed.

The crucial identity is EXACT:

    L*F_j=O_j-B_x.

It follows from z R_K(z)=Q_K(z)-1, even with different truncation orders at different stages. Thus ||L*F_M-(exp(TL*)B_x-B_x)||<=epsilon, without using ||L|| proportional to volume. The accumulated integral error is <=(1+T)epsilon<=a/8. Every difference remains B_x-supported by the invariant corner. Therefore, conservatively,

    (a/2)B_x<=F_M<=(3T/2)B_x,
    L*F_M<=-(c/2)B_x<=-[c/(3T)]F_M.

The packing/noise proof above now applies with delta replaced by T and the computed finite support of F_M. This closes the finite-time-to-local-certificate interface at mathematical existence level, provided the connected-sequence local norm bound and the actual healing certificate are verified. It does not turn a generic rapid-mixing assumption into an acquired repair operation.
