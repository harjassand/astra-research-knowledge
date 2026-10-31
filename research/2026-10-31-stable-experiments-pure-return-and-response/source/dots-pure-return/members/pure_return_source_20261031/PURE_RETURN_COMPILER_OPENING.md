# Pure-return certificates as acquired rapid-source machinery
31 October 2026. Initial construction, unreviewed as a whole. Completed older compilers remain separate capital.

## 1. Input is an operation and certificate, not a state-space table
Let Φ be a finite-dimensional source channel with an actually acquired Stinespring isometry W, a prepared pure fixed state ψ, and prepared environment vector c such that

    W|ψ>=|c>|ψ>.

Let P=|ψ><ψ| and Q=I-P. Reflection about P, W and their controlled inverses have their actual circuit costs paid. Require an earned integer m>=1 satisfying the OPERATOR survival certificate

    (Φ†)^m(Q) <= Q/16.                                  (1)

Classical mixing in an unrelated norm is not this certificate. A fitted channel or a norm bound alone does not provide the required circuits. Large Hilbert-space dimension is allowed only insofar as these operations are succinctly acquired.

Define the source contraction

    A=(<c| tensor I)W.

It has norm at most1 and Aψ=ψ. Contractivity then implies A†ψ=ψ, so P reduces A and AP=PA=P. The m-step dilation projected onto c^tensor m has source block A^m. For any v in Q, its Q-output norm after that projection cannot exceed the total Q-output probability in the dilation. Consequently

    ||A^m Q||^2 <= ||(Φ†)^m Q|| <=1/16.                  (2)

Thus the SAME acquired return certificate supplies a power-contraction certificate without diagonalization or source-dimension enumeration.

## 2. Exact dark realization and the classical-source interface
Write Kraus operators K_j from W and components c_j of c. Set

    L_j=K_j-c_j I,
    H_env=i(A-A†)/2.

Every L_j annihilates ψ. Direct expansion gives

    sum_j D[L_j] = Φ-I + (1/2)[A†-A, .],
    -i[H_env,.]+sum_j D[L_j]=Φ-I,
    C=sum_j L_j†L_j=2I-A-A† <=4Q,
    -iH_env-C/2=A-I.                                   (3)

The actual stacked dark jump is W-|c>tensor I, acquired by a two-term coherent sum with normalization2. It is not implemented by enumerating exponentially many Kraus matrices. A is an overlap of the same supplied isometries, and H_env is obtained from A and A† if needed.

The physical retained-source model is

    generator = -i[H_sys+sqrt(lambda)K,.]
                +lambda(Φ-I),

where K is an acquired bounded Hermitian system-source coupling, ||K||<=b, source starts ψ, and PKP=0. The dark realization (3) is exactly the same generator, not a change to the physical process. The centering condition prevents hiding a large sqrt(lambda) mean system Hamiltonian; if it is absent, that mean evolution must be acquired and paid separately.

For a source Φ preserving a diagonal classical observable algebra, and source-diagonal K, the joint Heisenberg algebra of system-valued diagonal functions is invariant. Starting ψ with the specified diagonal probabilities therefore reproduces the complete classical-source-driven system process, including prescribed system instruments and retained references. The source and its quantum jump records remain private. A physical source measurement is not received for free.

## 3. A multi-step return potential controls activity
Let

    V=sum_(j=0)^(m-1) (Φ†)^j Q.

Pure invariance implies 0<=(Φ†)^jQ<=Q. Hence

    Q<=V<=mQ, (Φ†-I)V <=-15Q/16 <=-Q/2.                (4)

This is a proof potential; it need not be prepared as a quantum oracle merely to use its scalar bounds. It is obtained from an actual certificate, not an unknown inverse-Lindbladian promise.

For the tilted physical dark-jump count let κ=e^θ-1, 0<κ<=1/(32m), and use weight Z=I+32κV. The fast drift gives at most -16κlambda Q. The tilted recycling adds at most

    κlambda sum L_j† Z L_j
      <=4κlambda(1+32κm)Q<=8κlambda Q.

The Q-Q part of i sqrt(lambda)[K,Z] has norm at most64κsqrt(lambda)b m on Q; if sqrt(lambda)>=16 b m it is bounded by4κlambda Q. The remaining cross P-Q term has norm coefficient at most32κsqrt(lambda)b m. Young's inequality spends the remaining4κlambda Q and leaves at most256κ b^2 m^2 P. H_sys commutes with the source-only weight. Therefore

    G_θ†(Z)<=256κ b^2m^2 Z,
    E exp(θ N_T)<=exp[256 b^2 m^2 T (e^θ-1)].            (5)

The initial source has Z expectation1. Nonselective system-only instruments, including their recorded outcomes, preserve that initial-weight comparison. Neither normalized rare postselection nor an activity bound for an approximate algorithm is asserted.

At θ=log(1+1/(32m)), (5) yields an exact-process count cap

    O(b^2m^2 T + m log(1/error)).                       (6)

The mean is at most256 b^2m^2 T. The microscopic rate lambda is absent from this activity scale. Below a chosen polynomial threshold in b^2m^2, ordinary simulation of the original rate-lambda Poisson channel Φ, interleaved with H_sys+sqrt(lambda)K, has polynomial rate action; no rapid-source trick is necessary. Actual acquisition and circuit costs remain paid in either regime.

## 4. Fast nonnormal kernel access from the same certificate
The separate candidate GROUPED_POISSON_KERNEL_CONSTRUCTION.md constructs

    F(s)=(1/2)e^(a' s) e^(s(A-I))Q,
    q=2^(-1/m), a'= (1-q)/2,

as an acquired contraction block, uniformly in s>=0, with polynomial m and logarithmic target-error cost. It uses (2), not a Hermitian spectral assumption. In outline, acquire B=2 A^m Q by slack singular-value amplification, group n=km+r in the Poisson series, and use weights

    e^(-(1-q-a')s) Poisson(qs;n) 2^(r/m-1).

Their sum is at most1; the selected operator is B^k A^r Q. Approximate B and source arithmetic are separately budgeted. For sufficiently large s, ||F(s)|| decays enough to select zero; below that cutoff the explicit Poisson count is only polynomial in m and log(1/error). Actual gate costs of W, ψ-reflection and all arithmetic are paid. This paragraph does not substitute for a whole independent review of that candidate.

Existing contour/QSVT functional calculus may provide the same operation. The kernel construction is a direct earned implementation, not a claim of a new general fast-forwarding theorem.

## 5. Factor-two bookkeeping in the physical Dyson source
This is the main next receiving join. The scaled kernel means the Q-sector free propagation is

    e^(lambda t(A-I))Q = 2 e^(-a'lambda t) F(lambda t).

A factor2 occurs for EVERY Q dwell. It must not be silently omitted or charged as an uncontrolled2^word loss. Let c0=b sqrt(lambda), r0=a'lambda, and use P/Q source labels. Every retained interaction insertion contributes its exact Hamiltonian -i. With PKP=0, absorb the factor2 into each target-Q interval. The positive two-state majorant is

    M=[[0,c0],[2c0,-r0+2c0]],
    E(t)=exp(Mt) diag(1,2).

Equivalently, with S=diag(1,sqrt2),

    E(t)=S exp(Msym t) S,
    Msym=[[0,sqrt2 c0],[sqrt2 c0,-r0+2c0]].              (7)

The diagonal2c0 accounts for QKQ insertions; the endpoint factors are at most2. This follows by expanding the positive Dyson series: the initial sector contributes its dwell factor, and every interaction contributes the factor of its destination dwell. It is not an assumption that the quantum Q sector has dimension one.

For a conservative high-rate regime sqrt(lambda)>=64 b m, a'>=1/(8m) gives r0>=8c0. The effective fast diagonal decay delta=r0-2c0 is positive, and the slow Perron rate is at most4b^2/a'=O(b^2m). The familiar acquired two-state bridge can potentially be received with these altered coefficients. Actual QKQ insertions have Poisson intensity2c0 on fast residence; their conditional source/cap proof must be carried through, not replaced by an unconditioned event-count assertion.

P/Q source-label preparation can retain the actual vector in each unequal-dimensional sector, as in the checked graded compiler. The new F block is applied on every fast dwell; finite per-word errors must be accumulated against the positive weights. No source eigenbasis or Q-sector table is supplied.

## 6. Complete first-event target and unresolved work
The dark jump annihilates P, but its output can lie in P OR Q. The actual stacked map W-|c>tensor I, with norm<=2, must retain its Kraus output. It cannot be replaced by a reset to ψ. An event arm applies that acquired map to the pre-jump Q row of the no-jump kernel.

Equation (7) suggests an integrable jump envelope of the form

    const * sqrt(lambda exp(-delta t)+b^2/a'^2)

on windows of length O(a'/b^2), with integrated squared mass polynomial in m and independent of lambda. The endpoint factors, row/column preparations, actual jump overlap, normalization, conditional bridge sources, full finite-bit clock hybrid and complete-isometry amplification still need a separate joined proof. It would be wrong to amplify the no-jump operator alone or infer an implementation merely from (5).

The intended consequence is a source compiler whose dependence is on an ACQUIRED return/mixing certificate and operation costs rather than an explicit Hilbert dimension or inverse stationary probability. This remains a conditional opening until those joins and a meaningful concrete source are checked. No practical speedup, novelty or civilisation-level result is claimed.
