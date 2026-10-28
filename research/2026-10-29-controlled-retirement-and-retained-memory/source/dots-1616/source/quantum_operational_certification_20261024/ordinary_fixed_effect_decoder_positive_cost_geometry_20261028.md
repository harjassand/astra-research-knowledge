# Fixed-effect full-decoder geometry: a positive-cost odd branch

28 October 2026, after the 14:13 frozen package. New author derivation, not independently received. This is a concrete fixed-effect decoder optimization mechanism, not a full decoder oracle, source acquisition theorem, or improvement over an equally informed conventional learner. The globally moving effect remains open.

## 1. An exact slice of the full CPTP body

Order a qubit-output decoder Choi matrix by output index. Every full CPTP decoder has

    C=[[A,B],[B*,I-A]], 0<=A<=I,
    B=sqrt(A) K sqrt(I-A), ||K||<=1.                    (1)

The factorization follows from block positivity, with contractions extended arbitrarily on zero supports. Conversely every displayed contraction gives a PSD matrix with partial trace I. This does not impose a rank-one recovery or an entanglement-breaking decoder. Here A is a KNOWN fixed effect; optimizing it jointly is not supplied by this note.

Use the received positive-cost dual representation

    u(C)=m0+Tr(W C), m0>0, W>=0.                        (2)

It applies to the affine denominator of the interior decoder design after its affine substitution. Let W_ij denote output blocks, and set

    M=sqrt(I-A) W_10 sqrt(A)=L S R*, S>=0 diagonal,
    K=-R V L*, ||V||<=1.

A full square singular-value decomposition is allowed, including zero singular values. Cyclicity of trace gives the EXACT identity

    u(C_A(V))=m+2Tr[S(I-Re V)],
    m=m0+Tr(W_00 A)+Tr(W_11(I-A))-2Tr S >=m0.           (3)

Indeed V=I is a feasible cost-minimizing slice decoder. Thus the polar reduction respects the actual CPTP partial trace and does not repair an infeasible matrix by mixing with a fixed replacement decoder. Equation(3) is an optimization identity, not an unknown-source whitening or physical measurement oracle.

Any PSD affine-quadratic leverage numerator on C becomes

    N(V)=||c+L0(V)||²,                                  (4)

for a known real-linear map on complex matrices. Its output can be realified without changing the argument.

## 2. Two branches, with no discarded noncommuting term

For an arbitrary contraction V, put X=Re V, H=Im V and E=I-X. Then 0<=E<=2I and

    X²+H²=(V*V+VV*)/2<=I,
    H²<=I-X²=2E-E²<=2E.                                (5)

This uses no commutativity between X and H. In particular

    q(H):=Tr(S H²)<=2Tr(S E)=u(V)-m.

Writing z0=c+L0(I),

    N(V)<=2||z0-L0(E)||²+2||L0(iH)||².                  (6)

The first term is an affine PSD quadratic over a single effect F=E/2 in[0,I], with exact cost m+4Tr(SF). Returning V_even=I-2F is an actual contraction with exactly that cost and numerator ||z0-2L0(F)||². It therefore reduces to the positive-cost one-sided effect problem, not a diagonal cube. The earlier working spectral-block argument for that problem is not promoted here.

The second term has a useful finite rounding mechanism proved next. This is an actual positive result for the odd branch; no conclusion for the whole fixed-A problem follows until the even branch is controlled.

## 3. Odd-branch covariance relaxation

For a real Hermitian coordinate covariance Z>=0 let G be the corresponding centered Hermitian Gaussian matrix. Define

    rho(Z)=E G², s=E||L0(iG)||², q=Tr(S rho).

Use the fractional SDP

    Z>=0, rho(Z)<=I, maximize F_Z=s/(m+q).               (7)

Every deterministic Hermitian H with ||H||<=1 gives a feasible rank-one covariance and, by(5), a benchmark denominator no larger than the original u(V). The fractional perspective is a finite SDP. Tr Z=Tr rho<=k bounds its domain; a small scalar coordinate covariance is strictly feasible. The following argument rounds a supplied rational feasible Z; it does not assume an exact unknown optimum.

Let R=2 ceil(sqrt(ceil(log_2(192 max(2,k))))). Then R²=O(log(2k)) and R>=sqrt(2 log(96k)). The established Hermitian Gaussian-series bound, with variance rho<=I, gives

    Pr(||G||>R)<=2k exp(-R²/2)<=1/48.

Gaussian quadratic moments and Markov give

    Pr(||L0(iG)||²>=s/2)>=1/12,
    Pr(Tr(SG²)>48q)<=1/48,

with zero-cost case q=0 interpreted exactly. Hence probability at least1/24 supports all three useful bounds simultaneously. No independence is asserted between numerator, cost and norm events. Gaussian-series concentration is an established ingredient; see Tropp, User-Friendly Tail Bounds, Theorem4.1, https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf .

For any Hermitian H with ||H||<=1/2 define the POLYNOMIAL contractions

    V_±=I-2H² +/- iH.                                   (8)

They are exactly feasible because

    V_±*V_±=I-3H²+4H^4<=I.

Their positive costs agree exactly:

    u(V_±)=m+4Tr(SH²).                                  (9)

Their even parts agree and odd parts have opposite sign. Thus

    max_± N(V_±)>=||L0(iH)||².                           (10)

This completion avoids a matrix square root, assumed unitary rounding, and the constant replacement-cost floor. Setting H=G/(2R) on the joint event gives

    max_± N(V_±)/u(V_±)
       >= s/[8R²m+384q]
       >= F_Z/max(8R²,384).                             (11)

Both returned matrices correspond to feasible full CPTP decoders in the fixed-A slice through(1). The ratio guarantee is logarithmic in k, not proportional to the k² parameter count.

## 4. Finite canonical arithmetic, not a reciprocal-small-cost stopping rule

For the canonical supplied rational instance m,S,L0,Z, use the already received finite Gaussian coupling construction in `ordinary_binary_povm_coherent_cost_rounding_20261028.md`, Section4. Choose a rational delta<=1/8 small enough that

    delta sqrt(||L0*L0||)<=sqrt(s)/4,
    delta sqrt(||S||)<=sqrt(m)/4.

The same explicit rational sufficient bounds in that source apply with its Hbar and Kbar. Generate rational Hermitian Gtilde coupled to G with Frobenius discrepancy<=delta except probability1/96. This costs precision bits polynomial in the input length, log(1/m), log(1/s), dimensions and confidence, not a mesh with reciprocal delta many cells. On the joint event,

    ||L0(iGtilde)||²>=s/8,
    Tr(S Gtilde²)<=96q+m/8,
    ||Gtilde||<=R+delta.

Set H=Gtilde/(4R). Certify I-4H²>=0 by exact rational PSD arithmetic; if it fails, use V=I. The joint event has strict slack and passes. Equations(8)–(10) now give the safe bound

    max_± N(V_±)/u(V_±)
       >=s/[256R²m+3072q]
       >=F_Z/max(256R²,3072).                           (12)

The favorable event has probability at least1/32. A predetermined ceil[32 log(1/beta)] independent trials, evaluating both actual ratios and including V=I, succeeds except beta. Every trial returns an exactly feasible rational contraction. Tiny m affects bits, not the repeat count. If s=0 the branch can be skipped.

The canonical statement is finite. Translating arbitrary rational A,W into a certified polar canonical instance and then producing an exactly rational Choi matrix requires a separate precision ledger near singular A. The mathematical fixed-slice transfer is exact, and known-control physical implementations can approximate it, but this note does NOT silently call that missing rational-interface ledger a completed global polynomial decoder oracle. In the interior design A and I-A have a supplied positive floor, which is a possible way to pay this ledger; its cost must be proved before an acquisition claim.

## 5. Boundary and next obligation

This resolves the imaginary Hermitian-contraction branch of the known fixed-effect channel slice with positive cost and full CPTP feasibility. It does not solve the remaining affine one-sided effect branch, optimize the effect A, or compare costs across changing polar frames. An arbitrary alternating choice of a single A remains subject to the earlier moving-weight/policy-localization obstructions.

The previous received k⁴ strict-ordinary learner and generic coded-reference k² dichotomy remain unchanged. The latter uses an actual stronger input/reference interface. The present optimization work concerns whether full-decoder geometry can remove the remaining strict-ordinary dimension bill, not whether generic fast acquisition exists at all.
