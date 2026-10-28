# Matrix-Bernstein growing-selector refinement: statistics and full-budget review

28 October 2026. **PASS.** Reviewed source: `ordinary_growing_selector_matrix_bernstein_refinement_20261028.md`, SHA256 `370dcda53990355eb4659f8f57aa70b5958f633f98f882da16c385de0b93ef3c`.

This is a separate theorem review. The received base's m^4/gamma^2 proof and receipts remain unchanged. Zero source calls, Bernoulli samples or RNG draws were used. Exact prescribed-matrix checks are not acquisition simulations.

## 1. Primary import and actual observation law

The separately bound `growing_selector_matrix_bernstein_primary_statistics_import_20261028.md` records my independent reading of [Tropp, arXiv:1004.4389v6](https://arxiv.org/pdf/1004.4389v6), Theorem6.1(ii), printed pages21--22, and the complete application to this source's actual Y. That import is independent of the main/full-refinement receipts, avoiding a dependency cycle. The PDF text and formula were retrieved directly; unsupported web screenshots are documented rather than claimed successful.

The source uses the SAME canonical rational binomial C and actual normalized-Cz Bernoulli input as the frozen base. It does not import an expectation oracle. Conditional on a good previous envelope, F=CAC lies in[0,I], and each current batch fixes B,C before all fresh reset queries. The variance inequality

    E Y^2=E[s(z^T Fz)T(z)^2]<=(S_m/tau)I

is an operator inequality because T(z)^2 is positive and the multiplying scalar lies in[0,1/tau]. It requires no commutation of F and sampled T. Centering subtracts F^2, and the norm bound R_m/tau follows from tau<=1 and m>=1. Applying the primary bound to both signs therefore yields exactly the stated2m sample-mean tail. It is not a matrix-martingale claim across random envelopes.

With P_m=2S_m+R_m, delta<=1, L=ceil log2(4mH/beta) and N=ceil[P_mL/(tau delta^2)], the exponent is at least L. Since e>2, each estimate fails with probability at most beta/(2H). Conditional first-failure union across at most H adaptive estimates costs at most beta/2. The guard and fallback continue to impose a fixed physical/resource cap on bad histories, even when the next good-envelope variance hypothesis would no longer hold.

No Frobenius-to-operator loss or medoid remains in this refinement. The dimension-three scaling comes from the bounded operator variance S_m, not from changing observations. The arithmetic sample mean is exactly rational in the reference model; finite gate/RNG discrepancies remain inside one whole-process budget.

## 2. Relative regime epsilon<gamma

J=ceil log2(gamma/epsilon) is at least1, H=J+1, and tau_J lies in(epsilon/(2gamma),epsilon/gamma]. Every coarse update uses fixed c0=1/16 and matrix precision delta0=1/64. These are exactly the base update's c0/4 accuracy and rounding requirements, so its invariant becomes

    A+tau_j I<=B_j<=(8/7)A+2tau_j I.

The terminal estimate uses new independent data after B_J freezes, at delta=gamma/64. Exact reconstruction gives +/-2delta B_J Loewner error for the possibly indefinite rational M. For every unit direction, including the data-dependent selected one,

    |x^T(M-A)x|<=u p(x)+v,
    u=gamma/28,  v=gamma tau_J/16<=epsilon/16.

This is a UNIFORM consequence of the matrix event, not a one-direction bound conditioned on selecting x. Comparing the certified epsilon/16 Rayleigh minimizer of M with a true minimizing direction of A gives

    p(x)<=[(1+u)/(1-u)]p_*+[2v+epsilon/16]/(1-u).

The displayed constants are correct: the multiplier is at most1+2gamma/27, and the additive term is at most7epsilon/36<epsilon/4. M need not be PSD, and no estimated spectral gap is required. The separately received finite-control/eigensolver interface handles its bounded rational input on every history.

The source-count sum is also correct. The coarse reciprocal-floor sum and terminal reciprocal floor are each less than2gamma/epsilon. Multiplying by delta0^(-2)=4096 and delta_terminal^(-2)=4096/gamma^2 gives

    T_coarse<=J+8192P_mL gamma/epsilon,
    T_terminal<=1+8192P_mL/(gamma epsilon).

Since gamma<=1, their sum is at most H+16384P_mL/(gamma epsilon). Every ceiling contributes its stated additive1; no random stopping time is used to improve this bound.

## 3. Additive regime epsilon>=gamma

This branch has no envelopes or terminal gamma-precision batch. With C=I, H=1, delta=epsilon/16 and Rayleigh slack epsilon/16, the ordinary matrix estimate gives

    p(x)<=p_*+3epsilon/16<=(1+gamma)p_*+epsilon/4.

Its count is at most1+256P_mL/epsilon^2, which is at most1+256P_mL/(gamma epsilon) exactly because epsilon>=gamma. The equality boundary belongs here; undefined zero-height coarse formulas are not instantiated. Omitting this branch and retaining a gamma-precision terminal estimate would not justify the claimed rate when epsilon is larger than gamma.

For both branches, H and the sample counts are determined from supplied rational tolerances before outcomes. P_m=m^3/2+5m^2/2+m is degree three, and L is a finite integer obtained by power-of-two comparisons. The scaling is O_tilde(m^3/(gamma epsilon)); no optimality or lower bound is proved.

## 4. All-history controls, confidence and complete transfer

The refinement retains the canonical finite binomial preconditioner, largest-dyadic whole-update rounding and exact PSD accept/abort policy. It does not alter the received physical receiver. An all-history bound follows, for example, from ||Fhat||<=m(m+1)/(2tau) and ||C^(-1)||^2<=8, giving ||M||<=4m(m+1)/tau in the relative branch. The additive branch has the smaller direct sample-mean bound. Hence finite rational eigensolving and final selector compilation do not assume a good fitted covariance or an empirical gap.

The exact new training cap replaces the base T_max when assigning sampler, state-preparation and gate-precision budgets. A final payload is still additional to training. In full common-algebra recovery, every decoder phase, every uniform m-anchor draw, logical sign and global Clifford test is included in the combined schedule; primitive-only random-bit accounting is not reused as a bound on all acquisition. Already executed calls on aborted histories remain charged. No counts are discarded, reused or postselected.

Section6 correctly changes ONLY the selector primitive of the frozen base's Section7. Its new m-anchor rho, supplied operator visibility, factor-m decoder-regret transfer and structural floor all remain unchanged. The selector's own branch comparison MUST use the passed primitive tolerance epsilon_p=[2^q/(2^q+1)]epsilon_global/8, not the unscaled global epsilon. The same applies to J,H,L and all sample caps.

For that passed tolerance, both branches give scalar additive<=epsilon_p/4, hence Bell additive<=epsilon_global/32. Retaining the base's looser epsilon_global/8 allowance is therefore safe. On successful decoder acquisition, its uniform excess remains

    F_dec+(225/8192)epsilon_global,
    F_dec=1980m q A_geom tau^2/kappa.

With decoder failure<=epsilon_global/16, selector failure<=epsilon_global/16 and one operational discrepancy<=epsilon_global/8, a conservative bound using the stronger primitive reserve is

    E ell <=(1+gamma)ell_star+(1+gamma)F_dec
                         +(9/32+225/4096)epsilon_global.

This is below the frozen base's stated +epsilon_global conclusion. The factor1+gamma on F_dec is retained. Additional sample accuracy does not remove that structural floor, and a former four-anchor weighted-tail promise cannot be substituted for the new m-anchor one.

Selector state control still has O(m) known amplitude-synthesis cost before routing/precision overhead, despite only ceil log2 m selector qubits. Source/test/receiver controls, memory, all input/output qubit traffic and finite-time width4^w substitutions remain paid. An equally informed conventional active-effect learner can implement the same refinement. No generic circuit-encoder, non-reset, hardware, family-validation or dimension-free untwirled-diamond conclusion follows.

## 5. Evidence and disposition

The source-disabled check `growing_selector_matrix_bernstein_statistics_check_20261028.py/.json` verifies four exact canonical binomial-C operator cases (including noncommuting A,B), both signs of the centered norm bound, the operator variance and160 exact branch/count/terminal-inequality cases. It does not sample source outcomes and does not substitute finite checks for the primary theorem or general proof.

No remaining statistical or full-budget objection was found. The companion receipt binds this final source, the separately received primary import, exact evidence, the frozen base and independently received main refinement review. No prior receipt is overwritten or retroactively strengthened.
