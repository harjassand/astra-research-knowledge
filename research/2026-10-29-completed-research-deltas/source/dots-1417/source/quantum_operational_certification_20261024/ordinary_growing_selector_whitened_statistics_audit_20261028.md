# Growing real selector: finite quadratic-design statistics

28 October 2026. New analytic mechanism review; zero source calls, Bernoulli draws, RNG draws or acquisition simulations. This note receives the statistical module, not a full envelope invariant or an as-yet unwritten global growing-selector theorem. Earlier received sources/pilots are untouched. The deterministic check uses exact finite moment sums and prescribed rational matrices only.

## 1. Scope and the required rational preconditioner

A FROZEN actual receiver and its ordinary global input/readout test give one Bernoulli outcome y with mean p(x)=x^T A x for each real unit selector x in dimension m>=1, with 0<=A<=I. This access contract is substantive. The experiment has fresh independently reset calls; no scalar-value oracle is supplied.

Conditional on the past, a known learner envelope B satisfies A<=B, tau I<=B<=4I, with 0<tau<=1. For exact finite arithmetic use rational B and a rational positive symmetric C satisfying

    B<=C^(-2)<=2B,  ||C||^2<=1/tau.                     (1)

Then F=CAC<=CBC<=I. Merely stating C<=B^(-1/2) does NOT imply CBC<=I without commutation. One must certify (1) directly or construct a commuting polynomial in B. The lower bound on B is learner-chosen regularization, NOT an eigenvalue floor on the unknown source gauge or A.

An OPTIONAL independent commuting rational construction is (the full candidate instead fixes its binomial polynomial; this Newton alternative is not substituted into that protocol)

    C_0=I/2,
    C_(k+1)=C_k(3I-B C_k^2)/2,
    k=ceil log2(4/tau).                                 (2)

Every iterate is a positive polynomial in B, commutes with B and is bounded above by B^(-1/2). For R_k=I-BC_k^2,

    0<=R_(k+1)=R_k^2(3I+R_k)/4<=R_k^2,
    R_k<=(1-tau/4)^(2^k) I<=I/2.

The last step is purely rational: (1-a)^N<=1/(1+Na) for 0<a<1, and N=2^k ensures Na>=1 with a=tau/4. Hence BC_k^2 lies between I/2 and I, proving (1). This is a predeclared iteration cap, not an unknown-spectrum stopping rule. Rational bit growth from degree 3^k is polynomial in 1/tau; the caller must still bound B's input bitlength, for example through its stated mesh rounding. This is a finite classical cost, not a claim of optimal preprocessing.

Condition A<=B may hold only on previous statistical good events. The analysis below is conditional on those histories. On arbitrary bad histories the caller must keep the known floor/norm controls or invoke its prescribed safe fallback, so the same source/control cap remains valid. No empirical membership test for A<=B is available.

## 2. An explicitly samplable real projective two-design

Choose z as follows: with probability 2/(m+2), choose a uniform coordinate vector e_i; otherwise choose independent uniform signs and put z=s/sqrt(m). Then

    E[z_i z_j]=delta_ij/m,
    E[z_i z_j z_k z_l]
      =(delta_ij delta_kl+delta_ik delta_jl+delta_il delta_jk)
          /[m(m+2)].                                   (3)

Indeed diagonal fourth moments are 3/[m(m+2)], the i!=j squared-product moments are 1/[m(m+2)], and all remaining fourth moments vanish by the sign symmetry or basis sparsity. This is a projective second design (fourth vector moments); it need not have Haar first moments. The m=1 case is included. It is sampled in O(m) random bits plus uniform-index generation, never by enumerating 2^m sign vectors in the learner.

For each actual source call set

    P=zz^T,
    s_z=||Cz||^2=Tr(C^2 P),
    x=Cz/sqrt(s_z),
    T(z)=m(m+2)P/2-mI/2,
    Y=y s_z T(z).                                      (4)

All estimator arithmetic uses rational P,s_z,T,Y when C is rational: P has entries 0,1 or +/-1/m. The normalized physical input x has a known algebraic normalization but is not assumed to be an exact finite gate primitive; its finite preparation belongs to the whole-process implementation budget. Since C^(-2)<=2B<=8I, ||Cz||>=1/sqrt(8), so this normalization is stable. C is a known learner matrix, not an unknown-source inverse.

Conditional on z, p(x)=z^T F z/s_z. The fourth-moment identity gives

    E[Y]=E[(z^T F z)T(z)]=F.                            (5)

Thus using rational C changes the target to EXACT F=CAC and introduces no transformed-moment bias or exact-square-root assumption. The earlier B^(-1/2) formula is a mathematical special case, not needed for this implementation.

## 3. Exact variance and robust mean constants

Define

    L_m=m^3(m+3)/4.

A direct multiplication gives

    T(z)^2=m^3(m+2)P/4+m^2 I/4,
    E[T(z)^2]=m^2(m+3)I/4,
    Tr T(z)^2=L_m.                                     (6)

Because y^2=y, s_z<=1/tau and 0<=F<=I,

    E||Y-F||_F^2
      =E Tr(Y^2)-Tr(F^2)
      <=E[s_z(z^T F z)Tr T(z)^2]
      <=L_m/tau.                                       (7)

The Bernoulli identity is essential to the inverse-tau rather than inverse-tau-squared rate. No Gaussian observations, fractional exact expectation values or independent measurements of different matrix entries are used.

For a batch average M_N of N fresh samples,

    E||M_N-F||_F^2<=L_m/(N tau).

Choose the canonical c=gamma/16, 0<gamma<=1, and r=c/12. Then

    N=ceil[2304 L_m/(tau c^2)]                          (8)

makes P(||M_N-F||_F>r)<=1/16 by Markov's inequality on the squared norm. There is no matrix concentration theorem or exponential net hidden in this step.

Use an odd number b of independent batches with the SAME fixed B,C. Set k_b=(b+1)/2 and choose the FIRST batch matrix having at least k_b neighbors INCLUDING ITSELF at squared Frobenius distance <=4r^2. If none exists, return a prescribed fallback value and let the caller's safe physical policy continue or terminate. Ties are resolved by the fixed first-index rule. Exact rational squared-distance comparisons are finite and inclusive, so no unstated numerical decision margin is required. The search costs O(b^2 m^2) rational operations; it is a majority-neighborhood selector, not an exponential optimization.

If at least k_b batches are good, any good batch has k_b good neighbors. Every selected k_b-neighborhood intersects the good set because 2k_b>b. Therefore

    ||Fhat-F||_op<=||Fhat-F||_F<=3r=c/4.                 (9)

Conditional on the fixed pre-batch history, bad indicators are independent with probabilities <=1/16. A union over bad subsets of size k_b yields

    P(majority bad)<=choose(b,k_b)(1/16)^k_b
                     <=2^(-b-2).                       (10)

For J predeclared levels and 0<beta<=1, choose the smallest positive odd b>=ceil log2(2J/beta). Each level then fails with probability at most beta/(8J), so conditional union across adaptive levels is <=beta/8, safely <=beta. The level's envelope may depend on PAST data, but not on another batch's current outcomes; all its batches freeze B,C before sampling. Conditioning on eventual global success is not part of the argument.

A numerical implementation that does not retain exact rational batch matrices can alternatively target statistical radius r/2 and certify deterministic matrix-rounding error <=r/2. This needs N=ceil[64L_m/(tau r^2)], four times the exact-arithmetic batch size. It then uses the same exact rational medoid comparisons on the rounded matrices. This is an OPTIONAL larger-cost variant, not the canonical cap (8). Unpadded approximate distance tests are not interchangeable with the inclusive exact rule.

## 4. Transfer to the rational envelope update

The received estimator output can be reconstructed without a square root:

    Ahat=C^(-1) Fhat C^(-1).

On (9),

    -(c/4)C^(-2)<=Ahat-A<=(c/4)C^(-2),
    hence -(c/2)B<=Ahat-A<=(c/2)B.                       (11)

If the caller rounds its WHOLE proposed B update with certified operator error <=c tau/4, that contributes at most cB/4. Thus the combined statistical and numerical error is bounded in Loewner order by +/-3cB/4. Adding cB supplies a positive domination margin. The complete envelope recurrence, upper bound B<=4I, spectral floors, final encoder selection and finite arithmetic of that recurrence are the main reviewer's separate responsibility; they are not proven merely by (11).

All matrices in (4), batch averages, neighborhood tests and Ahat are rational. For each fixed C there is a common sample-matrix denominator depending on C and m, so summing N samples increases the bitlength by O(log N), rather than requiring unrelated denominator products. Exact inversion and the mesh policy have known finite bit costs. The matrix-to-selector input synthesis is separately approximated under one linked operational budget.

## 5. Exact source cap and paid random sampling

For the canonical dyadic schedule tau_(j-1)=2^(-(j-1)), j=1,...,J, with

    J=ceil log2(8/epsilon),  0<epsilon<=1,

one has sum_j 1/tau_(j-1)=2^J-1<16/epsilon. All bN_j actual real-selector queries therefore obey

    N_design <= b[J+36864 L_m/(c^2 epsilon)]
              =O(m^4/(gamma^2 epsilon) log(J/beta)),      (12)

using L_m<=m^4. Ceilings account for the additive bJ. This is the acquisition module's source-block cap; any final payload or other source phases belong to the complete caller ledger. The rate is conditional on this dyadic schedule and cannot be asserted if a different invariant forces tau_last of order gamma*epsilon without substituting that change.

To sample the design exactly, first draw a uniform integer in {0,...,m+1}; its first two values select the basis branch. That branch uses a uniform index in {0,...,m-1}; the other branch uses m independent signs. Thus there are at most two uniform-integer draws and m sign bits per query. Uniform integers can use binary rejection sampling with a PREDECLARED cap. If T_max bounds all source queries, limit each integer draw to

    R=ceil log2(2T_max/nu_rng)

attempts, where 0<nu_rng is allocated inside the one whole-process discrepancy budget. Each acceptance probability is at least1/2, so the probability of ANY exhaustion is <=nu_rng. Exhaustion invokes a fixed safe fallback, never a repeated source query or retrospective postselection. Conditional on successful capped draws, each accepted integer is exactly uniform; equivalently one couples to the ideal uncapped sampler and pays the exhaustion event. At most

    2T_max R ceil log2(m+2)+mT_max

random bits suffice. Rejections consume classical randomness but no source calls. All already executed source calls remain charged on an exhaustion history.

Actual normalized-selector preparation, any fixed-receiver global test controls, adaptive classical arithmetic, memory and routing are paid. Approximation of query states or RNG is handled by the whole-process discrepancy, not by pretending that the ideal unbiased identity holds exactly for an uncharged physical approximation. The finite design's support may be exponentially large but its sampling and the estimator do not enumerate it. The same mechanism is available to every equally informed conventional learner.

## Evidence and disposition

The separate `growing_selector_whitened_design_statistics_check_20261028.py/.json` verifies exact second/fourth moments, estimator mean and T^2 identities on six prescribed finite designs, four canonical BINOMIAL-polynomial preconditioner cases, twelve exact odd-b majority tails, and a boundary witness showing why the distance comparison must be inclusive. The canonical cases explicitly test CBC, backward error, commutation, mean CAC and the2304 batch constant; they do not substitute the optional Newton alternative. These are analytic/algebraic checks, not sampled acquisition evidence.

PASS for the rational-preconditioned design, variance, canonical batch/majority constants, finite sampling and conditional source cap, subject to the stated quadratic Bernoulli access and envelope/preconditioner contracts. A full growing-selector theorem still needs the separately checked envelope invariant, final selection and complete physical accounting. No new source samples or prior-source changes occurred.
