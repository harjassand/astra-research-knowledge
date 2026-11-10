ROOT mathematical preparation, 10 November 2026
Elementary reaction realization: a finite-class construction and its infinite-class boundary

CONTRACT. Let Q be a fixed finite complex-balanced mass-action channel table on the original species, including any fixed catalytic channels already supplied by the completed compiler. Its rates k_r are positive rational and at most one. At activities lambda it has conditional-Poisson stationary law pi on an ACTUAL communicating class Gamma, and the accepted polynomial physical Poincare gap g_0. All fixed degrees, species and channel counts below depend on this fixed table, not on lambda or the variable initial state. The original compiler supplies the table, balanced fluxes, rate/bit bounds and g_0; this note does not reprove that capital.

For the finite-class quantitative result ONLY, assume a supplied numerical bound B>=1 satisfies |x|_1<=B for EVERY x in Gamma. This is a capacity hypothesis, not a truncation of an infinite physical process. No general infinite-class robust compiler follows from this note.

1. EXACT BINARY GRAPH LIFT.
Order the reactant molecules of each distinct complex c once. A complex of order zero is represented by the empty complex, a complex of order one by its original species, and one of order q>=2 by a new species C_c. Introduce private prefix species C_{c,l}, 2<=l<=q, with C_{c,q}=C_c. Its decoder column is the original prefix population c_l. Repeated molecules are retained. Use the reversible assembly channels
 X_{a1}+X_{a2} <-> C_{c,2},
 C_{c,l-1}+X_{al} <-> C_{c,l}, 3<=l<=q.
Every side has at most two molecules. Replace each original channel y->z by rep(y)->rep(z). It is zero/unimolecular on each side. Original null/parallel labels may be kept separately.

Let D be the nonnegative integer decoder that is identity on original species and sends a prefix species to its prefix population. Every assembly/release firing has decoded change zero. A central firing has decoded change z-y and is enabled only when D state>=y. Releasing all prefixes reaches the canonical encoding (x,0) with x=D state. Conversely, any enabled original reaction can be lifted by assembling its y, firing the central channel and releasing z. Therefore the actual fine communicating class is exactly
 Gamma_hat={u>=0: D u in Gamma}.
This proves actual reachability and enabled decoded edges, rather than merely equality of lattices. All decoder columns in this construction are nonzero, so |u|_1<=|Du|_1. For finite Gamma the fine class is also finite.

2. EXACT NOMINAL BALANCE AND THE STATIC DECODING ERROR.
Give every prefix species activity a_{c,l}=theta lambda^{c_l}, with 0<theta<=1. At the first assembly take forward/reverse rate constants K theta,K. At later assemblies take K,K. Each binding pair is detailed balanced. If j_r=k_r lambda^y is an original balanced complex flux, set the central rate j_r/a_rep(y), taking a_rep(y)=lambda^y for order<=1 and theta lambda^y for order>=2. Central rates are k_r or k_r/theta. Thus their fluxes are exactly j_r and the whole fine network is complex balanced at (lambda,a).

The fine stationary product law, conditioned on Gamma_hat, is explicit. For a fixed decoded x its unnormalized weight is the original weight lambda^x/x! times
 q_theta(x)=sum_{a: E a<=x} theta^{|a|} (x)_{E a}/a!,
where a lists prefix copy numbers and E lists their encoded populations. Let D_*>=1 bound every original complex order and every prefix encoded order. If s is the number of prefix species and b=B+2, then
 1<=q_theta(x)<=exp(s theta b^{D_*}).
Indeed (x)_{Ea}<=b^{D_*|a|}, and extending the nonnegative sum to every a gives the exponential. Consequently the decoded law differs from pi in TV by at most e^u-1 and in every ABSOLUTE first moment by at most B(e^u-1), where u=s theta b^{D_*}. The probability of any occupied prefix is also at most e^u-1. Taking theta<=epsilon/[64(1+s)b^{D_*+1}] pays both static errors. The lambda powers cancel EXACTLY; no rare-class probability bound has been substituted.

3. POLYNOMIAL GAP FOR A GENUINELY FINITE CLASS.
Write q for the fixed total number of fine species. There are at most n=b^q fine states. Let E_hat be the fine nominal Dirichlet form. The following path comparison gives a polynomial bound without a minimum-state-probability exponential.

Within each decoder fibre, release ONE full prefix at a time. Releasing a prefix of encoded order k completely increases its product weight by
 theta^-1 u_C / product of k rising original-species factors >=1/(theta b^{D_*}).
At an intermediate release stage the weight can fall by at most b^{D_*+1} relative to the start of that one prefix. With theta b^{D_*}<=1, completed release blocks never lower that starting weight. A full release path has length at most D_* B, every used dissociation has rate at least K, and hence every edge conductance on the path from u is at least K b^{-(D_*+1)} pi_hat(u). Summing over at most b^q starting states gives
 E_pi_hat |h(u)-h(canon Du)|^2
 <= C_R b^{q+D_*+2} K^-1 E_hat(h).
This deliberately loose congestion bound is polynomial for the fixed table. It includes multiple simultaneously occupied prefixes; no single-intermediate approximation is used.

Lift an original edge between canonical encodings by assembly, central firing and release, at most 2D_*+1 steps. Source-side prefix weights relative to the canonical state are theta times a nonzero falling factorial and hence at least theta. The central conductance is EXACTLY pi(x) k_r (x)_y divided by E_pi q_theta. On the target side,
 pi(x) k_r (x)_y / pi(x')
 =k_r lambda^{y-z}(x')_z <=W^{2D_*}b^{D_*},
where W>=2+sum_i(lambda_i+lambda_i^-1). Therefore choosing
 K >= 4 W^{2D_*} b^{D_*}/theta
makes the fast edge conductances dominate the original edge flux up to a fixed factor. Congestion is fixed-table bounded: a fine edge determines its decoder and there are only fixed many reaction/prefix positions. Thus
 E_original(h composed with canon)<=C_R E_hat(h).

Since pi_hat(canon x)=pi(x)/E_pi q_theta and the decoded fine law lies between e^-u pi and e^u pi, variance decomposition gives
 Var_pi_hat h
 <=C_R [b^{q+D_*+2}/K+g_0^-1] E_hat(h).
Every factor is polynomial in numerical B,W,epsilon^-1 and the accepted original parameters. The displayed comparison is for actual elementary channels, not a virtual central jump supplied for free.

4. INDEPENDENT FIXED RATE ERRORS, MIXING AND ALL FIRINGS ON THAT FINITE CLASS.
For relative channel errors bounded by delta, off-diagonal rate sums have the same bounds. Positive rooted-tree weights on n states have n-1 rate factors. After normalization this gives
 exp(-4 n delta)<=mu_tilde(u)/pi_hat(u)<=exp(4 n delta)
for delta<=1/2, with harmless enlargement of the constant. Null firings do not enter these trees but remain separately counted. Choose delta<=epsilon/[256 b^{q+1}]. This pays stationary TV and absolute decoded first moments. The perturbed stationary Dirichlet form and variance are uniformly comparable to the nominal ones, so its physical Poincare gap is comparable as well. This argument also covers a nonreversible complex-balanced nominal chain; L2 contraction uses its invariant-law Dirichlet form, not detailed balance of central channels.

Normalize ALL rate constants by one common rational S>=max(K,theta^-1). The nominal constants are then <=1, their minimum is at least k_min/S, and the physical mixing time is multiplied by S. All are polynomial numerical costs. A time
 T>=C gap_pert^-1 [log(1/mu_tilde(canon x0))+log(b/epsilon)]
makes transient TV and ABSOLUTE decoded first-moment errors small. The initial log reciprocal weight is polynomial: the fine partition function is at most exp(sum original/prefix activities), and the canonical factorial and lambda terms contribute at most B log b+B log W. No lower bound on the probability of the class is needed for this upper bound on a reciprocal CONDITIONAL point weight.

With normalized rates<=1 and at most b total molecules, the sum of all actual channel intensities is at most C_R b^2. Expected TOTAL firing count to T is therefore at most C_R b^2 T, including assembly, disassembly, central, failed, null and parallel channels. Molecule number and molecule-time are bounded by b and bT. Exact rational arithmetic/output use fixed-table many coefficients with bit lengths polynomial in complete input length plus log B. No state-space enumeration is required by these choices; n<=b^q is a bound, not an enumeration procedure.

This proves the finite-capacity elementary realization from the accepted original gap/rate compiler, including robust stationary and transient law/moment accuracy. It is an original composition/path calculation using established complex-balance and tree machinery, not a claim that those classical tools are new.

5. WHAT IS MISSING ON INFINITE CLASSES.
The same exact graph lift and nominal complex balance exist. For fixed lambda, its conditioned product normalizer is finite. Monotone convergence as theta decreases to zero, dominated by the finite product-Poisson partition at theta=1 (and its polynomial moments), gives qualitative decoded TV/first-moment convergence to pi. This does NOT provide a polynomial-numerical theta choice uniformly in x0,lambda. The crude whole-space partition ratio can be exponentially bad. Also the finite-tree error exponent n and the capacity-dependent gap comparison do not survive B->infinity.

Reflecting or killing at a selected B changes the physical process and its graph; neither is an elementary implementation of the full target. A true infinite-class result needs an untruncated confinement/perturbation mechanism with polynomially controlled scale, or a different design. Applying the prior universal catalytic compiler AGAIN to the fine network would reintroduce arbitrarily high molecularity and is not a solution. This is the central remaining operation, not a hidden lemma credited as proved.

6. CURRENT PRIMARY AND CONTRARY CONTRACTS.
Hoessly--Wiuf, arXiv:2110.13235v1, https://arxiv.org/pdf/2110.13235, was read at Definition3.1, Assumptions1--2, Theorem4.1, Section5.3 and AppendixB.2--B.3. Theorem4.1 requires a FINITE CLOSED state set and fast-chain return identity and gives compact-time O(eta) convergence for appropriate initial support. The watched generator is the finite Schur complement, so internal residence times have not been made physical time for free. Examples5.8--5.9 explicitly show recurrence may differ under a reduction. Theorem5.10/Corollary5.11 restore correspondence for sub-conservative networks/intermediates; they do not give a robust all-infinite-class polynomial compiler.

Plesa's higher-order-to-bimolecular paper was encountered through indexed text, but ROOT's exact PMC9839831 page returned a reCAPTCHA. No alternate/preprint/export recovery was attempted and no governing theorem from that paper is imported. The independent Hoessly--Wiuf paper is not an alternate copy of it. This source limitation is recorded outside any scientist prompt.

No simulations, physical experiment, new worker, optimizer or resource-consuming probe was used in this derivation.
