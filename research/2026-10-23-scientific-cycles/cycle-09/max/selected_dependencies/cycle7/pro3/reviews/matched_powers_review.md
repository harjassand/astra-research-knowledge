# Focused source-bound review: matched screening powers

Reviewer: `/root/proposal_ratio_counterexample`.
Scientific date: 22 October 2026, Australia/Brisbane.

## Bound source and verdict

Reviewed in full:

`MATCHED_POWERS_THEOREM.md`, 12,836 bytes, SHA256
`4387140a21173620f5bcd2d228275b6db938eee495c30b55d2bd95bb0340c775`.

**ACCEPT WITHOUT REPAIR within the declared scope.** The principal's
general-power calculation, opposite fan-out geometry, fixed-balanced
upper/lower and bounded moving-mismatch quantifier are correct. The actual
native proposal probabilities, rejection diagonals, block holding moves,
full returns and one KL budget are retained. I found no unsupported
endpoint substitution, counting-column premise or optional-time argument.

I supplied the earlier q-only-screen fan-in prototype and its first-core
sandwich. My comparison of that original material here is a transcription
check, not an independent second audit of my own construction. The principal
has separately read and accepted that original source. This review's distinct
challenge concerns the added power exponents, fan-out lifting, fixed-balanced
rate and moving-policy statement. I have not independently re-proved the
entire reciprocal-proposal energy theorem; its displayed finite lemmas are
the expressly identified dependency of the balanced upper.

## 1. The balanced upper uses a legitimate fixed-parameter bound

For fixed 0<eta<1, theta=min(eta/2,1/4) obeys 0<theta<=eta and theta<=1/2.
Thus the finite certificate of RECIPROCAL_PROPOSAL_THEOREM.md applies with
w=1, p=(1-theta)^-1 and a finite fixed scalar H_1. There is no use of a
fixed-screen theorem restricted to symmetric Q.

Writing ell=log n and v=log ell, the selected h=v^-4 gives
q(B)>=exp[-(K+H_2(h))/(1-h)]>=e^-K/2 eventually uniformly over the class.
For N=ceil[8/(alpha e^-K) log ell], the unhit bound is at most ell^-2.
With R=n/ell^4 and d_test=ell^-2, the uncapped bad-set mass is bounded by
O(n^-1 ell^4 v^5), uniformly in Q, support and atom size. The cap is therefore
inactive eventually.

Since theta is fixed, Gamma need not approach one. It suffices that Gamma
is bounded by a fixed finite constant. Then Gamma^(N/p) is at most a fixed
power of ell, and the capture term is n^-theta times a fixed power of ell
and v. That is o(ell^-1). The source expressly pays this accumulated factor.
The smoothing/test terms are O(ell^-2), leaving only the high-weight
information-tail bound K/(ell-4 log ell-1). Its scaled limsup is K.

The unchanged Q=I lower is also correct: rare pi mass p=k/log n and
q mass e=p/[n(log n)^2] have KL tending to k<K; the mixture's exact
nontrivial eigenvalue is 1-alpha/[2n(log n)^2]. Its proposal-start TV is
asymptotic to k/log n. Letting fixed k increase to K proves the matching
lower. These are direct new-class consequences of a new finite bound and
an identified old ordinary construction, not a fresh symmetric campaign.

## 2. Both native lifts give the claimed screen factors

On a mismatch horizon put d=|eta-kappa|>0,
m=ceil(n^(4eta/d)), e=b/n^4, p=1/n and t=1/n^3.

For eta>kappa, each of m roots has q=b/m and pi=t/m; a single leaf has
q=e and pi=p. The proposal probabilities are root->leaf=1 and
leaf->each-root=1/m. Consequently the INDIVIDUAL-STATE ratios are

    q_y/q_x = m n^-4,
    Q_yx/Q_xy = 1/m,
    r_q = n^-4,
    r_pi = p/t = n²,
    S = n^-4eta m^(eta-kappa).

For kappa>eta, one root has q=b and pi=t; each of m leaves has q=e/m
and pi=p/m. The proposal probabilities are root->each-leaf=1/m and
leaf->root=1. The native ratios are instead

    q_y/q_x = n^-4/m,
    Q_yx/Q_xy = m,
    r_q = n^-4,
    r_pi = p/t = n²,
    S = n^-4eta m^(kappa-eta).

Both calculations are exact. In particular the second one does not lose
the factor m in the reverse proposal or replace a per-vertex target
probability by a block mass. Q is row-stochastic with reciprocal support
and is determined by n and the prescribed exponents before target values.
It is fixed within the run and satisfies the declared target independence.

## 3. The ceiling estimate survives varying exponents

For any eta>0, d>0 and n>1, put x=n^(4eta/d)>=1. Then
x<=ceil(x)<=x+1<=2x, so

    1 <= S=n^-4eta m^d <=2^d.

No lower or upper bound on the exponent 4eta/d was used. Hence for
|eta_n-kappa_n|<=C, the same estimate gives 1<=S<=2^C on EVERY mismatch
horizon, even if the mismatch tends to zero, eta_n tends to zero or eta_n
grows. Eventually 2^C<=n², and the actual total acceptance is exactly
one forward and n^-2 backward. It does not merely approximate ordinary
local MH.

For each fixed exponent pair, d itself supplies the finite constant C.
For the moving-policy result, the fixed finite bound on d is a stated
hypothesis. No unbounded-mismatch result is asserted. Equality horizons
are not included in this construction, and the theorem does not infer
sufficiency from eventual matching when eta_n may shrink too fast.

An infinite mismatch set supplies an unbounded subsequence of integer
horizons. The permitted class supremum may choose its finite graph at
each horizon; arbitrarily large m is explicitly admitted and charged in
the information/resource discussion. Thus the adverse subsequence
legitimately prevents uniform convergence. This is not a within-run
adaptive change of eta, kappa or Q.

## 4. Multiplicity, the KL budget and total variation

Every probability in both native lifts is positive eventually. The root,
leaf and core weights are t/b, p/e and pi_z/q_z, respectively, independently
of m. Their ordering is t/b<pi_z/q_z<p/e eventually. Summing the actual
per-vertex KL terms cancels multiplicity exactly:

    D(pi||q)=t log(t/b)+p log(p/e)+pi_z log(pi_z/q_z).

This tends to -log(1-b)<K, independently of m, eta and kappa. The admission
therefore has strict eventual slack and remains valid along all mismatched
policies in the theorem. There is no extra entropy term hidden by lumping
and no second use of K.

The root block in the fan-in lift and leaf block in the fan-out lift are
permutation invariant. All their native rows have equal outgoing masses
to each block. This proves strong lumpability. Since q, pi and every
evolved law are uniform within the nonsingleton block, native total
variation equals quotient total variation. The G quotient in equation (13)
correctly includes global moves between different roots or leaves as block
holds; it does not identify those moves with single-state rejections.

## 5. Retention and full returns

The source explicitly retains the ENTIRE leaf block in the lower event.
Its one-step escape probability is

    d_l=alpha(1-p)/(2 W_l)+beta/(2 n²).

The first term is all global escape to the nonleaf blocks. Within-leaf
global moves are permitted during retention, which is essential in the
fan-out case. The second term is the total local reverse escape. Thus
n d_l tends to zero. The root first-exit denominator v=a0+c0 charges both
local and direct global leaf moves and the global core exit.

The lower sandwich is an actual retained-path event. The upper separately
decomposes at the first core hit and applies TV contraction to the ORIGINAL
remaining chain from that state. Every subsequent exit and return is kept.
Neither side renormalizes killed rows or treats an absorbing proof counter
as an operational sampler.

Once S lies in [1,n²], the exact quotient, initial block masses, waiting
terms and escape bounds are independent of all exponents and multiplicity.
Their limit is A_b=b beta/[alpha(1-b)+beta]. Taking b up to b_K only after
the fixed-b limit yields the displayed class-floor lower bound. The source
correctly refrains from calling it an exact minimax floor.

The same-input balanced screen has forward factor n^-4eta and reverse
acceptance n^-2 n^-4eta. Its fixed-eta full-return upper tends to zero.
The pure-IMH sandwich is unchanged by either lift and gives TV~n^-1 for
deterministic horizons proportional to n. These controls are distributional,
not runtime claims, and the source preserves direct block sampling when
the explicit analytic target is naturally available.

## Scope and resources

I executed no numerical jobs and did not materialize any graph in this
review. The argument is analytic. A rational finite fixture was suggested
to the principal as a diagnostic only. Discovery/inference/token and total
monetary costs remain unknown. The adjacent receipt binds the reviewed
sources and observed completion time.

This verdict is an internal source-bound mathematical assessment, not
external acceptance, formal machine verification, historical-priority
certification, sampler speedup or evidence for a research-prompt tactic.
