# Independent audit: growing and polylogarithmic composition caps

Reviewed 2026-10-30. Scope: `GROWING_CAP_REPLACES_SUMMABLE_ABSORPTION.md` and `POLYLOG_CAP_FINITE_FIBER_EXTENSION.md` only. No frozen v1 bundle was edited.

**Verdict: both hard-network replacements pass.** Their stopped-cost and actual incoming-feedback arguments suffice to replace the sharp N^-9/4 absorption dependency. Generic formulations need the explicit renewal, jump-size, and quantitative interface hypotheses recorded below; none is automatic for an arbitrary reaction network.

## 1. Crude absorption really is earned

For the hard conservative shell N>=3, if A<3, at most 3-A successive A-increasing fast conversions reach A=3; each is enabled because enough C remains. If A>=3, clearing is already enabled. Thus at most four prescribed jumps reach killing. With normalized total rates <=C N^3 and each required rate >=c, the success probability is >=c' N^-12. Before killing some path edge is enabled, so total rate >=c and the expected duration of a four-jump block is bounded. Restarting after unsuccessful blocks proves mean killing time <=C N^12. The exact common (B)_4 factor restores the displayed bound. This uses no mixing or drift profile.

More generally, a finite killed graph with M<=C(1+N)^d states and every state reaching killing has a simple path of length at most M. Polynomial total-rate upper bounds and a positive enabled-edge lower bound give success probability at least exp[-C M log(2+N)] in M-jump blocks, whose mean duration is <=M/c. Their geometric sum gives the claimed exp[C'(1+N)^d log(2+N)] bound. Reachability and the rate bounds are essential, but no spectral or equilibrium assertion is hidden in the proof.

## 2. Growing-cap tail and value estimates

For N<=s^(1/8), the actual shell hazard calculation gives birth risk <=C s^-3 N^13 and stopped time <=C s^-4 N^12. Summing over the descending N ladder yields the stated s^-5/4 risk and s^-19/8 time bounds. Neutral births restart only while still inside the cap; leaving the cap is actual stopping, not omitted dynamics. The uniform restart probability is o(1), so the geometric estimate is legitimate. The certified 45-state head has up probability O(s^-1) and neutral-tail probability O(s^-3), so the complete killed excursion has up-and-survival probability O(s^-1) and polynomial mean time.

For the polylog cap, (1+L)^d log(2+L)=o(log s) when pd<1. Polynomial factors in N and the number of descending stages are also s^o(1). This gives tail birth risk s^{-(q-a)+o(1)} and time s^{-q+o(1)} even using the worst-case finite-graph bound. In the hard application q=4, a=1, and the already earned head estimate closes renewal. One may choose any u strictly between the existing bulk-admissible alpha and 1.

At each fixed residual, the hard-network cap contains finitely many actual states, so its stopped neutral excursion cannot conceal an explosion. Across residual excursions, the factorial contraction remains true after multiplying the cost by the fixed polynomial needed for the excursion-time bound. Summing conditional contractions proves finite expected cost and finitely many excursions before either threshold or cap exit. Thus the value is finite and the stopped process is nonexplosive before its defining exit time. First-jump decomposition gives LW=-phi inside the domain, with zero terminal values at actual exits. This requires neither an invariant cap nor full-chain recurrence.

## 3. Exact cap entry, including cap shifts

Both cap functions are increasing and have L(s+1)-L(s)<=1 for sufficiently large integer s. Immigration increases N by one and does not increase s, so it cannot enter from above the cap. Activation increases N by two and s by at most one, and likewise cannot enter. Fast conversion leaves both N and s fixed. Only clearing, which decreases N by three and preserves s, can enter from a large-s exterior state. The incoming collar is therefore precisely contained in L(s)<N<=L(s)+3. A down residual jump may shrink the cap and cause an extra exit; that exit has zero terminal value and cannot hurt contraction.

The only possible threshold entry has s=s0 and target s0+1. Capped target N is bounded, original N differs by at most two, and B=s+g_N is then bounded. Thus threshold leakage really has finite support.

At the exterior collar W=0, so its full positive generator contribution is the actual clearing rate times the target value. Both are polynomial(s) times phi(s), uniformly in composition. This is an absolute incoming-forcing bound, not merely a small probability or a discarded boundary term. On this collar B~s, N~L(s) tends to infinity, and r=N-h_B tends to minus infinity. Therefore W_r and all nearby target values vanish; the existing F has a quantitative negative drift by its extreme-composition or balanced bulk estimates.

## 4. The interface ratios beat all polynomial costs

Here g_N=B-s>=N, and B!/s!>=s^{g_N}. Dropping the helpful factors A!C! yields

    log(phi/F) <= tilt_log(s)-alpha N log s.

For the power cap, N~s^p and tilt_log=s^delta with delta<p; this is <=-c s^p log s. For the polylog cap, N~(log s)^p and tilt_log=(log s)^(1+p/2); the difference is <=-c(log s)^(1+p). Both decay faster than every inverse power of s. They therefore absorb the entire polynomial(s) incoming forcing against F's earned negative margin, even when that margin is only an inverse-polynomial multiple of F.

For bounded N and large B, the opposite comparison is required and holds: B-s=g_N is fixed, so phi/F is the chosen tilt times an inverse polynomial in B. Both tilts dominate every fixed power of B. Negative LW therefore closes the bounded-N cylinder. Everywhere else W adds nonpositive drift except at the already absorbed collar or a finite threshold set. Consequently adding W to the previously earned F+W_r preserves the complete global Foster conclusion for this particular network, including the factorial-size forcing needed for exponential stationary moments.

## 5. Generic hypotheses that cannot be omitted

Three clarifications were sent to the author during review:

1. A head up-exit bound and polynomial head time alone do not close renewal. One needs, for example, head-to-neutral-tail probability <=rho<1 uniformly, or an explicit nonvanishing renewal denominator with its exponent included in the final estimates. The hard network has the stronger O(s^-3) bound. The polylog note was amended to state rho<1 explicitly.
2. The displayed alpha<u contraction presumes residual exits exactly +/-1. If positive jumps can be as large as J, the sufficient condition becomes alpha J<u, together with a genuinely decreasing nonzero negative exit and bounded jumps. The hard network has exactly +/-1.
3. Resource z>=s and a negative outer-collar drift do not by themselves imply the factorial separation. Generic use requires a quantitative bound such as log[F/Gamma(s+1)^alpha]>=cN log s, an inverse-polynomial-F negative margin, polynomial interface rates/values, and the stated collar geometry. In the hard network these are proved from B-s=g_N~4N/3 and the existing F estimates. They must not be silently inferred from q>a alone.

With these qualifications, the reusable conclusion is legitimate: finite-fiber accessibility can replace quantitative fast-fiber absorption in this cap mechanism. It does not manufacture the needed residual, resource-order gap, finite-head downward bias, or global interface certificate for arbitrary networks.

### Repair verification

Re-read both current source files after the author amendments. The head-to-tail renewal requirement, +/-1 versus bounded-J exponent condition, and quantitative factorial-separation/interface assumptions are now explicitly stated where relevant. These repairs resolve the generic-scope issues raised above. The hard-network application required no mathematical change. Final verdict on the amended sources: pass at this child-audit level; no remaining failure identified.

### Reviewed source hashes
f4e5556616fa1071b0dd53c1798ce423c7914e23fac383efaae61d4f6a731b64  chemical_joint_shell_20261030/GROWING_CAP_REPLACES_SUMMABLE_ABSORPTION.md
4903147e0722bbd575a4768fe0481f363830bc699d4f94efca142d08e42390df  chemical_joint_shell_20261030/POLYLOG_CAP_FINITE_FIBER_EXTENSION.md
