# Independent receiving review: qubit entropy comparator and correlated products

2026-10-29. Reviewer: review_finite_quantum_sampler. Verdict: PASS at the explicit finite-dimensional scope of GOVERNING.md. This accepts the local factor 2 and the separate complete/product factor 2+sqrt(2), including the stated stationary-barycenter prior transfer. No general N371 closure, complete factor 2, optimality among all EB maps, historical novelty, unknown-channel acquisition procedure, or physical implementation advantage is accepted.

## Received hypotheses
Each channel is a unital CPTP qubit map with a full-domain two-output CPTP extension having the channel as both marginals. Product factors may differ. Quantum inputs need not be product, labels/priors need not be independent, and any finite-dimensional reference may remain entangled. The axes are the leading RIGHT singular axes of each Bloch matrix; arbitrary ties can be resolved once. The resulting product dephasing is one common channel, not a state-dependent fitted comparator.

Proper input/output rotations may diagonalize a real Bloch matrix with SIGNED singular entries. They correspond to qubit unitaries. A diagonal unital CP map is a Pauli channel; complete positivity, rather than a spurious all-positive singular-value convention, ensures its four probabilities are nonnegative. The review checks signed cases explicitly.

## 1. Joint measurement requirement
Measure the two chosen orthogonal output spin axes on separate receiver systems. The adjoint of the extension maps their joint four-outcome PVM to a valid input POVM. Unitality makes each pulled-back marginal unbiased: Tr[Phi*(sigma)]=Tr[sigma Phi(I)]=0. In the singular basis the input Bloch vectors a,b are orthogonal with lengths s1,s2.

Writing a joint effect as (gamma I+g.sigma)/2 gives |g|<=gamma. The marginal and normalization equations yield a+b=g_++-g_-- and a-b=g_+--g_-+. Thus |a+b|+|a-b|<=sum gamma=2, and orthogonality gives s1^2+s2^2<=1. This implication uses no converse characterization of self-compatibility.

Primary cross-check: Busch–Heinosaari, arXiv:0706.1415v2, https://arxiv.org/pdf/0706.1415v2, equation (39) and Proposition 4, with the surrounding unbiased-observable hypotheses. The manuscript's elementary necessity proof is independently sufficient and agrees with this standard criterion.

## 2. Local factor 2 is sound, including its restricted sharpness
Let a=c(sqrt(x)), c0=c(sqrt(x+y)) for the manuscript's positive-coefficient entropy-deficit series. Then 0<=a<=c0. If the largest squared singular value is at most 1/2, c(|Tr|)<=c0/2. Otherwise the squared output radius is at most max(x,(x+y)/2), giving 2c(|Tr|)<=max(2a,c0)<=a+c0. The intermediate maximum inequality is valid precisely because a<=c0. This proves the local entropy-gain comparison for all radii, including the pure boundary by convergence/continuity of the series.

I independently supplied a physical boundary extension. Let V|0>=|00> and V|1>=(|01>+|10>)/sqrt(2), and W=(X tensor X)VX. The channel B(rho)=[VrhoV†+WrhoW†]/2 has symmetric outputs, is CPTP, and both marginals are unital with diagonal multipliers (1/sqrt(2),1/sqrt(2),1/2). Fix leading axis X and take a weak Y Bloch vector. The ratio of dephasing entropy gain to channel entropy gain tends to 2. This certifies the manuscript's sharpness for that fixed-axis choice, not for optimized arbitrary EB channels.

## 3. Complete comparison uses an actual convex decomposition
For a leading axis n, divide Pauli indices into (0,n) and (j,k). Removing min(p_a,p_b) from both members of each pair gives nonnegative residual probabilities and a paired contribution 2min(p_a,p_b) Ad(P_a) composed with Delta_n. In the canonical gauge this is an exact identity of channels, including arbitrary references, not only a Bloch-length comparison. The total paired weight is

 alpha = 1-|p0-pn|-|pj-pk| = 1-max(|lambda_j|,|lambda_k|) = 1-s2.

The middle equality follows from |u+v|+|u-v|=2max(|u|,|v|). Complete positivity is essential for removing nonnegative weights. Compatibility implies s2<=1/sqrt(2), so alpha>=1-1/sqrt(2)>0.

Each paired branch differs from dephasing only by an output unitary; each residual branch is unitary. Entropy concavity on the full joint system plus reference gives gain_Phi>=alpha gain_Delta. Input/output basis changes preserve this conclusion by conjugating the input state/reference trivially and the final comparator back to the input gauge. The proof is complete/reference-stable. It does not yield constant 2.

## 4. Tensorization is valid for correlated states
For any subset S let f(S)=S(Delta_S rho)-S(rho), with the reference included in every entropy. The increment for adding i equals the Holevo information of the two equiprobable states rho_S and Z_i rho_S Z_i. Further commuting dephasing on another site is the same CPTP map on both ensemble members, so data processing decreases that Holevo information. Thus f is monotone submodular, with f(empty)=0.

For the product decomposition, the branch output entropy is S(Delta_S rho), because all remaining operators are local unitary conjugations. No product form for rho or output-state independence is used. Entropy concavity yields gain_Phi>=E f(S). For a fixed order, the increment when i is added to S's earlier elements is at least its increment after ALL earlier elements. Summing these inequalities proves f(S)>=sum_(i in S) [f([i])-f([i-1])]. Averaging and using inclusion probabilities alpha_i gives E f(S)>=min_i(alpha_i) f(all). Correlations between inclusion events would not invalidate this final bound; the actual product expansion is sufficient to supply the marginals. Hence the complete bound is independent of the number of sites and the finite reference dimension.

The same proof applies to a correlated Pauli channel IF a suitable nonnegative partial-dephasing/unitary decomposition with stated site coverage is explicitly supplied. Acquiring such a decomposition from generic self-compatibility is not proved.

## 5. Prior transfer and quantifiers
For an ensemble, the identity average gain_Phi=delta+kappa follows directly by expanding Holevo quantities. Unitality ensures kappa>=0. Pinching obeys D(rho||Delta rho)=gain_Delta. With natural logarithms, Pinsker gives T(rho,Delta rho)<=sqrt(gain_Delta/2); Jensen and the entropy comparison yield the submitted constants.

If Phi(bar_rho)=bar_rho, gain_Phi(bar_rho)=0; the complete bound forces gain_Delta(bar_rho)=0, hence Delta(bar_rho)=bar_rho. The measurement Holevo loss then equals average gain_Delta and is at most delta/alpha*. The local factor-2 improvement applies to a one-qubit ensemble without importing it into a reference-stable theorem. Maximally mixed barycenters qualify even when the individual states are entangled across sites and their labels are correlated.

The kappa term cannot simply be removed for THIS fixed channel-selected comparator. For the boundary cloner above, a singleton prior on a pure Y-axis state has delta=0, kappa approximately 0.41649553, and disturbance by X dephasing exactly 1/2. This is NOT a counterexample to every possible prior-dependent EB map: the singleton state could be re-prepared perfectly. Accordingly, this scope warning does not settle the unrestricted N371 question.

## Independent executed evidence
* Verified all AUTHOR_FREEZE.json hashes before testing; originals unmodified.
* Replayed the author's 24,000 local/reference diagnostics and 100 three-qubit/reference diagnostics in the audit folder. Reported residuals and bounds reproduced. The early comparator script's phrase 'complete extension remains conjectural' refers to the attempted factor 2, not the later analytically proved factor 2+sqrt(2).
* Checked 1,365 exact rational Pauli-pair identities over all denominator-12 Pauli probability vectors and all three axis choices. No positivity or reconstruction failures.
* Constructed the unital boundary extension above independently; marginal/self-compatibility and singular-multiplier residuals are zero in the executed arithmetic. Weak-axis entropy ratios approach 2 (1.99999999833 at radius 10^-4, evaluated by a stable series).
* Generated 100 independent three-qubit/reference-two states of varying ranks, with signed channels and unrelated input/output unitary gauges. Checked all relevant submodularity inequalities and the complete bound. These test channels satisfy the load-bearing singular inequality; not every such test channel is asserted self-compatible.
* Checked a stationary maximally-mixed-barycenter prior generated from an entangled state's local Pauli orbit, and the singleton nonstationary obstruction above.

These are exact rational algebra tests plus floating entropy diagnostics. The analytical arguments, not empirical extrema, establish the theorem. No native circuit or laboratory result is claimed.

## What this actually changes and what remains
The manuscript provides an explicit nonlinear entropy comparator and a dimension-uniform correlated-product extension. The hard step is supplied by an exact convex channel decomposition and entropy data processing rather than by inferring nonlinear control from quadratic covariance. It therefore closes a genuine scoped proof obligation for unital self-compatible qubit products with stationary priors. It does not extend automatically to nonunital channels, arbitrary globally correlated channels, arbitrary nonstationary means without kappa, unknown-axis acquisition, or complete factor 2. Historical comparison against entropy-production, pinching, and complete log-Sobolev literature remains necessary before originality or foundational significance beyond this mathematical scope is claimed. Astra N371 source provenance is contextual and was not independently re-audited here.
