# All-p and complete-recovery consequences of the hidden-flag lower bound

2026-10-27. New corollaries to `exact_erasure_hidden_flag_adaptive_channel_lower_bound_root.md`; independent receipt requested. These preserve exact orthogonal erasure and bounded total adaptive channel-query access.

## 1. Every small p, not only reciprocal integers

Fix 0<p<=1/2, D=floor(1/p)>=2, and r=pD<=1. Let E_(1/D,U,psi) be the canonical hidden-flag source. Add one orthogonal receiver erasure basis vector e and define

 E_(p,U,psi)(rho)=r E_(1/D,U,psi)(rho)+(1-r)Tr(rho)|e><e|.

Its success probability is exactly p. Its replacement state is

 tau_p=[p I3/3 tensor(I_D-Ppsi)+(1-pD)|e><e|]/(1-p).

The numerator has trace p(D-1)+(1-pD)=1-p and is orthogonal to the code U C3 tensor psi. Thus the original deficit remains exactly zero. Receiver dimension is3D+1.

Each query to E_p can be simulated by an independent source-independent coin: use one E_(1/D) query with probability r, otherwise discard the input and prepare e. This is a CPTP simulation even for entangled input, and never uses more than one original query per simulated query. Consequently an inverse learner with a worst-case cap of n E_p calls gives a learner with at most n E_(1/D) calls on the same code datum.

The canonical theorem therefore implies, at complete unhalved diamond inverse error zeta<=1/4,

 n >= floor(1/p)^2/40 >= 1/(160 p^2).

More generally retain the canonical bracket with D=floor(1/p). This is a maximum-query-budget statement. No assertion about expected cost follows merely from the coin construction; no adaptively unbounded stopping-time allowance is introduced.

## 2. From a full noisy-recovery guarantee to a code-inverse guarantee

Let E=p V(.)V*+q Tr(.)tau be any isometry-plus-replacer source. Consider a source-independent decoder D with a known logical qutrit success output and a known orthogonal erasure flag. It may use bounded adaptive queries to the same fixed source, and arbitrary source-independent processing, ancillas, and training. At a fixed source it is a CPTP map on the independent DATA input. Write

 C=D composed with V(.)V*,
 sigma=D(tau),
 A=D composed with E=p C+q R_sigma,

where R_sigma(rho)=Tr(rho)sigma. Suppose for some known 0<alpha<=1 its COMPLETE channel obeys

 ||A - [alpha p id + (1-alpha p)R_e]||_diamond <=delta.   (1)

The norm is unhalved, and both accepted and erased runs are included. A fixed dephasing of the output success/erasure flag cannot worsen (1), so assume that flag is classical. This is not a measurement of the unknown source's flag.

Let b be the accepted weight of sigma. In the normalized qutrit Choi state of A, measure the projector Q onto the accepted output/reference space orthogonal to the maximally entangled target Phi3. Its probability is zero under the ideal channel in (1). For the replacement contribution,

 Tr Q J(R_sigma) = b - Tr[Phi3(sigma_acc tensor I3/3)]
                = b-b/9 =8b/9.

The contribution from C is nonnegative. Trace-distance testing in (1) gives

 (8/9)q b <=delta/2,
 q ||R_sigma-R_e||_diamond =2q b <=9delta/8.             (2)

Subtract the replacement branch from (1), using

 p[alpha id+(1-alpha)R_e]+q R_e
 =alpha p id+(1-alpha p)R_e.

The triangle inequality yields the exact implication

 ||C-[alpha id+(1-alpha)R_e]||_diamond
 <=17delta/(8p).                                      (3)

No bound on code/replacement distinguishability has been assumed. The pure accepted Choi target is what forces any accepted replacement weight to be small. This argument remains valid after averaging over a decoder's private training randomness. It requires the data to be independent of that training conditional on the fixed source, as in the canonical task; the decoder does not receive the external input reference.

## 3. Quadratic queries for meaningful full-throughput-fraction recovery

Apply (3) to the canonical hidden-flag pair with p=1/D. Supply the same physical logical datum |0> tensor psi. The ideal outputs under the two Weyl hypotheses have orthogonal accepted states of weight alpha and the same erased component. Their HALF trace distance is alpha. The actual outputs therefore have half-distance at least

 s=alpha-17delta/(8p).

When s>0, the SAME Haar chi-square proof gives

 n >= (D^2/8)[1-1/sqrt(1+s^2)].                        (4)

For example, alpha=1 and delta<=2p/17 imply s>=3/4, hence n>=D^2/40. For any fixed alpha>0 and relative error delta<=4alpha p/17, one has s>=alpha/2, giving a strictly positive constant times p^-2.

For arbitrary0<p<=1/2, use the first corollary and D=floor(1/p) in (4); the source now has the extra known receiver erasure dimension. This establishes a worst-case quadratic lower bound for the ACTUAL complete noisy-recovery operation at any fixed nonzero fraction of the ideal success rate and sufficiently small error relative to p. It is not confined to an abstract deterministic inverse guarantee.

A fixed absolute error delta as p tends to zero is a different task: the always-erasing decoder already has error2alpha p, requiring no queries. Accepted-only conditional fidelity, an unspecified shrinking throughput, and uncharged postselection are likewise not governed by (4). The result neither fixes the inverse-accuracy exponent nor excludes improved recovery for a known code, a supplied source flag, or fixed receiver dimension.
