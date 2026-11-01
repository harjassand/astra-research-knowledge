# An actual-time receiver with a profile pinned at every inventory-changing interface

Author-derived construction, not independently audited and not a claimed solution of arbitrary weak reversibility. This is a concrete attempt to remove the neighboring-Green-profile obstruction in a compatible boundary model. It is kept as an operation toward the larger question, not promoted as completion of the civilisation-scale mission.

## 1. Raw model and conclusion

There are free counts A=a and B=b, and exactly one finite controller/enzyme in phases s in E. Each phase has a fixed nonnegative integer inventory j_s. Put

    n=b+j_s,     M=a+n.

The only count-changing reservoir is 0<->A, with immigration lambda>0 and death mu a, mu>0. Internal phase transitions s->r change B by j_s-j_r and preserve a and n. Their rates are acquired from a finite mass-action list, are independent of a, and depend polynomially on b with nonnegative falling-factorial forms and positive coefficients. Let Q_n be their actual finite phase generator at inventory n. Choose n0 so that, for n>=n0, every phase is available and the enabled directed phase graph is fixed. Every phase must reach a nonempty marked set G in that graph.

Only marked phases support A/B exchange, and every such exchange leaves its phase unchanged. At a marked phase the finite list consists of positive-rate reversible pairs

    A+kB+E_s <-> (k+1)B+E_s,     k>=0.                    (1)

Every marked phase has at least one pair. These have actual rates f_(s,k) a (b)_k and r_(s,k) (b)_(k+1). Parallel pairs are allowed. The phase graph may contain cycles and need not obey detailed balance. No stationary phase law is supplied.

All internal moves preserve M, so M(t)<=M(0)+Poisson(lambda t). This gives nonexplosion directly. The complete construction below proves a Foster inequality outside a finite set and, for each prescribed theta>0, finite invariant E exp(theta M) on every closed irreducible class. If the original raw network is weakly reversible, every actual communication class is closed by its translated complex return paths.

This statement is broader than the unit-rate bottleneck and does not need a spectral gap, but it still has real architectural restrictions: bounded controller phase, one free nonport inventory, A-neutral hidden motion, and pinned inventory-changing outputs. No theorem for arbitrary coupled boundary geometry follows.

## 2. Acquire the finite profile rather than assume mixing

For n>=n0 kill the ACTUAL phase chain when it first enters G. On T=E\G, solve exactly

    (-Q_n[T,T]) v_T(n)=1,      v_s(n)=0 for s in G.        (2)

Reachability to G makes the matrix a nonsingular M-matrix. Its inverse is nonnegative, so v_T>0 and (2) is the ordinary finite expected hitting-time vector. Every coefficient is a polynomial in n; hence v and Q_n v are rational functions acquired by finite symbolic elimination or positive tree formulas. At a marked phase,

    (Q_n v)_s>=0.

Let

    J(n)=1+sum_(s in G)(Q_n v)_s,
    c_t=rmin(1-1/t)/16,
    epsilon(n)=c_t n/J(n),
    h_s(n)=1+epsilon(n) v_s(n),                           (3)

where t>1 is chosen later and rmin is the least reverse coefficient in (1). Then, EXACTLY,

    h_s=1 on every marked phase,
    Q_n h=-epsilon(n) on T,
    0<=(Q_n h)_s<=c_t n on G.                            (4)

The elementary finite-path bound also pays the size of these objects. If there are q phases and the largest phase source degree is d, a path to G has at most q-1 edges. For n>=n0 every edge on a selected path has rate at least c>0, while total phase activity is at most C(1+n)^d. Each block of q jumps reaches G with probability at least c'(1+n)^(-d(q-1)); holding times have finite means uniformly bounded above while outside G. Thus

    0<v_s(n)<=C'(1+n)^(d(q-1)),
    1<=J(n)<=C''(1+n)^(dq),
    epsilon(n)>=c'(1+n)^(-P),
    1<=h_s(n)<=C'''(1+n)^(P')                           (5)

for finite acquired constants/exponents. Sharper exact rational bounds are optional. The holding-time argument is physical time, not a jump-count identification. No uniform gap is asserted, and the bottleneck can have gap zero.

For the finitely many inventories n<n0 set h_s(n)=1 on all valid phases. All marked values remain exactly one at EVERY n, including a head or an actual exchange landing. Invalid phase/inventory combinations do not represent states.

## 3. The pinned interface removes neighboring-profile transport

Take

    W(a,b,s)=t^n h_s(n).                                 (6)

Reservoir jumps change only a, so they leave W unchanged. A hidden phase jump preserves n, so its contribution is exactly t^n Q_n h. An exchange changes n by one, but its source AND target are the SAME marked phase, where h_s is identically one for every inventory. Its landing value is therefore exactly t^(n+1) or t^(n-1). No ratio h(n+1)/h(n), Green-entry transport estimate, frozen composition, or guessed resampling law appears.

At an unmarked phase and n>=n0,

    L W=-epsilon(n)t^n.                                 (7)

At a marked phase, writing b=n-j_s,

    t^(-n) L W
      =(Q_n h)_s+sum_k (b)_k[
            f_(s,k) a(t-1)-r_(s,k)(b-k)(1-1/t)].          (8)

Put Cfr=max_(s,k) f_(s,k)/r_(s,k), and choose

    eta=1/(16 Cfr t)>0.

Increase n0 so b-k>=n/2 and (b)_k>=1 for every exchange source. For a<=eta n, the bracket in (8) is at most

    -(7/16) r_(s,k) n(1-1/t).

Equation (4) costs at most rmin n(1-1/t)/16. Since at least one pair is available at every marked phase, it follows that

    L W<=-c n t^n,      a<=eta n, s in G, n>=n0,          (9)

with c>0. The inequality is pointwise. It does not require the process to stay in this cone during a trajectory.

Every possibly positive W contribution, including the finitely extended head, is bounded by

    (L W)^+ <= C(1+a)(1+n)^D t^n.                        (10)

In the tail the only positive terms are the marked exchange/bounded marked Q_n h terms, whose rates have the displayed finite polynomial bounds. In the head, the valid hidden phase space is finite and h=1, and the marked exchanges still have known exact landing values. There is no uncharged transition from an unmarked phase to a different inventory.

## 4. A second exponential joins the high-A region

Choose

    t^(1/(1+eta)) < u < t,
    Z=u^M,     V=W+Z.                                   (11)

Every internal move preserves M. Hence, for every actual phase and composition,

    L Z=[lambda(u-1)-mu a(1-1/u)]Z.                      (12)

For a>=a0, (12) is at most -c a Z. There are three exhaustive tail regimes.

* If n is large and a<a0, (7) or (9) supplies a negative term at least c t^n/(1+n)^P. The possible positive Z term is at most C u^n. Since u<t, the former dominates.
* If n is large and a0<=a<=eta n, W is nonpositive by (7) or (9), and Z has negative drift by (12).
* If a>eta n and a>=a0, Z has negative drift. By (10), its ratio to the possible positive W term has the exponential factor

      u^(a+n)/t^n >= [u^(1+eta)/t]^n.

  The base exceeds one. This absorbs every fixed polynomial in n; for bounded n and a tending to infinity, the factor u^a absorbs the head's linear-a terms. Thus this whole regime also dissipates outside a finite set.

Small a and small n form a finite set. V is nonnegative, finite at every state and normlike because Z alone grows with M. Therefore LV<=-1 outside an actual finite set; no recurrent law or averaging is assumed to obtain the inequality.

## 5. Every prescribed stationary exponential reward

For any theta>0, first choose t>exp(2theta), then choose u in the interval (11) with u>exp(theta). The interval is nonempty, even though it can be very narrow. In each of the three regimes the same reserved negative terms eventually dominate exp(theta M): (7)--(9) have an exponential t^n divided only by a polynomial, while (12) has u^M. Absorptions can reserve a fixed fraction of these terms. Thus this choice gives

    L V_theta <= -exp(theta M)

outside a finite set. Standard stopped Dynkin/regenerative receiving gives finite expected exponential reward per return cycle and hence a finite stationary exponential moment on every closed irreducible class. It need not assume pi(V_theta)<infinity: start from a finite return set, use stopped Dynkin to bound each outside excursion's reward by its finite one-jump starting V value, then use the finite trace chain on that return set. This is an actual reward argument, not integration of a generator against an unproved invariant integrability assumption.

## 6. What remains for the general question

The useful new interface is exact pinning: the acquired hitting profile equals one at EVERY state through which the slow inventory changes. This removes the neighbor-profile operation rather than claiming it for arbitrary Green entries. Internal phases still evolve, all actual phase clocks are included, and zero-gap examples are admitted.

A generic conservative weakly reversible core can change several inventories, can let A participate in hidden motion, and can land at unpinned internal states. It does not automatically satisfy this interface. For that larger model, neighboring profile transport and mutually evolving face geometry remain unearned. The accepted N1394/N1485 results already contain finite transient-chain and evolving-hidden-fiber techniques in their own guarded architectures; the present derivation does not supersede their whole-transfer proofs or inherit their audit status. Historical priority of the pinned interface theorem is UNKNOWN.
