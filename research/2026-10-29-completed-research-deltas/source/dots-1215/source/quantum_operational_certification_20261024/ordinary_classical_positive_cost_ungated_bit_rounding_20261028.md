# Ungated dyadic-block rounding: a bit-polynomial positive-cost cube oracle

28 October 2026. Author proof/check, with the central ungated-block construction proposed by the parent agent and the finite feasible-SDP/cap details checked here. Independent receiving pending. This is separate from the frozen received gated source SHA `d30bebfe86d4abc4154482d9b3a435de247c09e9dbc2ecf164dcabafbfa99e01` and its parallel-gate logarithmic companion.

## 1. Scope and input

Use exactly the binary cube, positive affine cost and BASIC PSD moment relaxation of the received source:

    N(z)=(1,z)^T A(1,z), A>=0, z in{0,1}^n,
    u(z)=m+sum_i w_i z_i, m>0,w_i>=0,
    M>=0, M00=1, M0i=Mii=p_i,
    d=m+sum_i w_i p_i, F=Tr(A M)/d.

All input data are known rational numbers. Choose rational a>=max(1,||A||op), for example max(1,Tr A). The algorithm below rounds ANY supplied feasible M. A finite perspective SDP can supply such a matrix near the relaxation optimum, with its solver/certification bill counted. This note does not supply a full-CPTP feasible matrix rounding.

Apply the received tail cutoff delta=min(1/2,m/(64an)). Retain p_i>=delta and group into nonempty dyadic groups I with p_i in(p_I/2,p_I]. There are L<=min(n,1+ceil(log2(1/delta))) groups. These groups are found from rational bit positions; no grid with length1/delta is enumerated.

For F<1 return the baseline z=0 and accept additive-one relaxation loss. For F>=1, if R0=N(0)/m>=F/4 return the baseline. Otherwise the received tail proof gives

    S_keep/d>=F/16,  S_keep<=L sum_I S_I,
    S_I=Tr(A_II M_I),                                    (1)

and L>=1.

## 2. A separate unweighted correlation SDP on each group

For each group let

    T_I=max{Tr(A_II Y):Y>=0,diag Y=1},
    c_I=m+(1/2)sum_(i in I) w_i.                         (2)

The padded matrix M_I/p_I+diag(1-p_i/p_I) is feasible, so p_I T_I>=S_I. The dyadic scales are distinct and sum to at most2. Because p_I/2<=p_i,

    sum_I p_I c_I<=2m+sum_keep w_i p_i<=2d.

It follows that

    max_I T_I/c_I>=S_keep/(2Ld)>=F/(32L).                 (3)

This replaces rare-gate sampling by an ordinary, UNGATED correlation rounding on one selected group. Paying the baseline m once per trial is harmless because it is charged with weight p_I in the group-selection proof, not physically repeated1/p_I times.

Implement each nonzero-trace block SDP to a certified feasible rational matrix Ytilde_I with achieved objective

    Ttilde_I=Tr(A_II Ytilde_I) in[T_I/2,T_I].             (4)

Zero-trace PSD blocks are zero and can be skipped. Such a constant-factor finite objective gap has polynomial bit complexity: T_I>=Tr A_II>0, T_I<=|I|Tr A_II, and the correlation body has the strict center I. For example, a weak SDP output with exact diagonal one, smallest eigenvalue>=-eta, and objective>=T_I-Tr A_II/8, for eta<=1/8, becomes exactly feasible after replacing Y by(Y+eta I)/(1+eta), with objective still greater than T_I/2. Rational affine/eigenvalue feasibility certificates and the imported finite SDP solver are paid; no exact optimum is presumed.

Choose the group maximizing the ACTUALLY achieved rational ratio Ttilde_I/c_I. Equations(3)-(4) give

    Ttilde_I/c_I>=F/(64L).                               (5)

## 3. Constant-probability useful output without a rare gate

Write Ttilde=Ttilde_I, c=c_I and g=|I|. Draw s=sign(N(0,Ytilde_I)) and set z_I=(1+s)/2, z=0 outside I. Every output is a feasible binary vector and

    E u(z)=c,
    E||sum a_i z_i||^2>=Ttilde/(2pi).                    (6)

If R0>=Ttilde/(64c), return the baseline. Otherwise N(0)<Ttilde/64. The pointwise offset inequality N(z)+N(0)>=||sum a_i z_i||^2/2 gives

    E N(z)>=3Ttilde/64,
    E[N(z)-t u(z)]>=5Ttilde/128,
    t=Ttilde/(128c).                                    (7)

Here pi<4 was used conservatively. On every binary vector in the group,

    ||sum a_i z_i||^2<=g Tr A_II<=2g Ttilde,
    N(z)<=2N(0)+2||sum a_i z_i||^2
          <=(4g+1/32)Ttilde.                            (8)

Thus the ideal probability of N(z)>t u(z) is at least

    5/(512g+4)>=1/(128g)>=1/(128n).                      (9)

This lower bound does NOT depend on a/m, the rare p_i, or their numerical magnitudes. Couple each finite sign sampler to its ideal one with error at most1/(512n). Then its actual success probability remains at least1/(256n). Independent trials with deterministic cap

    ceil[256n log(1/beta)]                               (10)

find a useful vector except probability beta. Return the largest actually evaluated ratio among all trials and the baseline. On success, the returned ratio is at least F/(8192L); the earlier baseline branches are better. All returned vectors remain feasible on failed histories.

Finite Gaussian factor and sign sampling require only polynomial input-bit arithmetic and polynomially many random bits. Every ideal marginal is standard normal, irrespective of a correlation eigenvalue approaching zero. A polynomially precise factor, Gaussian tail truncation/quantization and marginal anti-concentration yield the stipulated1/(512n) coupling. The algorithm uses no source query, and it does not implement a quantum receiver.

## 4. What the complexity claim now means

Unlike the numerical-magnitude cap of the common-gate sampler, this algorithm has polynomial classical time in n, the rational input bit length and log(1/beta), under the explicitly paid certified SDP primitive. The tail cutoff and any tiny nonzero Tr A_II affect bit precision only. The Gaussian trial count is O(n log(1/beta)); it is not proportional to1/p_I or1/m.

The O(L) approximation order is consistent with the geometric BASIC-moment integrality gap in `ordinary_classical_positive_cost_gated_rounding_log_improvement_20261028.md`. That example violates RLT pairwise moment bounds, so no gap is asserted for stronger relaxations or for the optimization task itself.

No arbitrary full-CPTP coordinate grouping is supplied. Choi positivity and the input partial-trace equality are coupled, unlike the product cube. Therefore the received generic k^6 source rate is not changed by this classical reduced theorem alone. The equally informed conventional learner receives the same oracle.
