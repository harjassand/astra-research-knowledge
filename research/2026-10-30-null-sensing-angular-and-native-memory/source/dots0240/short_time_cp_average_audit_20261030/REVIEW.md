# Independent review: short-time CP transfer and the startup obstruction

2026-10-30. Reviewed actual source arguments in `CONNECTED_COMMUTATOR_TRANSFER.md`, `SHORT_TIME_CP_AVERAGE.md`, and `FIXED_HORIZON_SERVICE_OBSTRUCTION.md`. Exact copies and source hashes are retained alongside this receipt. No source was edited.

## Verdict

1. **PASS as a conditional mathematical lemma:** the explicit connected-commutator incidence estimate, relative-factor inequality, convergent short-time similarity, and resulting local/common-bath noise transfer are correct under their stated assumptions.
2. **REJECT the proposed generic native bridge:** locality, raw V/W monotonicity, and positive finite reset-completion probability do not supply the required volume-uniform fixed-horizon weighted service. The independent two-stage counterexample is exact; even the integrated-W version fails.
3. **No change to the separately accepted simple compiler:** its bounded-depth local multiplicative CP credit is not this common-time averaging construction. No native transactional service, all-Hilbert descent, or native memory theorem is certified here.

The rejection is of the claimed generic service implication/criterion, not an impossibility theorem for all time averages, all state-dependent smoothing, or autonomous quantum memory. Transferring the counterexample to a particular FGL code's safe basin would require an additional embedding argument.

## 1. Correct incidence recurrence

Use the Heisenberg commutator `[L,M]=L composed with M-M composed with L`. Represent all nested commutators by the actual ordered local pairs; cancellation is unnecessary. If L_X has at most r physical sites, M_Z at most u, and their physical supports are disjoint, they commute **because the clean L_X acts trivially on the retained bath**. Every nonzero commutator is HP and identity-annihilating, has support inside X union Z, and has cb norm at most 2||L_X||_cb||M_Z||_cb.

Let J=sup_i sum_(X containing i)||L_X||_cb and m=sup_i sum_(Z containing i)||M_Z||_cb. For an anchor i, terms with i in Z contribute at most

    2 sum_(Z containing i) ||M_Z|| sum_(X meeting Z)||L_X||
        <= 2uJm.

Terms with i in X contribute at most

    2 sum_(X containing i) ||L_X|| sum_(Z meeting X)||M_Z||
        <= 2rJm.

Double counting pairs with i in both sets is harmless. Thus m([L,M])<=2J(u+r)m. Starting at u_0=q and incidence eta gives

    u_n<=q+nr,
    m(ad_L^n N)<=eta (2Jr)^n (1+q/r)_n.

There is no hidden tree-counting or noise-position factor. The two anchored cases already account for the distinguished original noise support and all subsequent connected growth. Repeated terms with identical supports are allowed and counted with multiplicity in this decomposition norm.

Bath-only terms can be omitted from this incidence count because they commute with clean L and annihilate every system-only animal. For bath-only Hamiltonian evolution an interaction picture is available and preserves the joint cb norms. A bath-only dissipator need not have an invertible interaction picture; it can simply remain separate, since it also annihilates the proof observable. Clean terms acting jointly on a common bath would invalidate disjoint-physical-support cancellation and are **not** covered by this lemma.

## 2. Relative-factor bound is valid for arbitrary local HP maps

Write f_A=e^(a|A|) f_out g, where g is the product of those factors whose supports meet Z, and f_out the product of the rest. At most k|Z| factors enter g. Hence

    theta^(k|Z|) I <= g <= I.

The untouched product is supported outside the map's physical patch. Even when its factors overlap the support of g, it commutes with g by hypothesis and is in the bimodule algebra of M_Z. Thus

    M_Z(f_out g)=f_out M_Z(g),
    [f_out,M_Z(g)]=0.

This is the missing justification if one merely says the map acts only on the touched factors; no tensor factorization of the commuting check/flag algebra is required. Complete boundedness gives

    +/- M_Z(g) <= ||M_Z||_cb I
                 <= ||M_Z||_cb theta^(-k|Z|) g.

Multiplying by commuting positive f_out proves the claimed relative Loewner bound. If Z meets no factor, identity annihilation makes the output exactly zero. The amplification includes all other physical sites, fresh references if present, and the retained common bath; no dimension factor appears.

The physical support of f_A contains at most b|A| sites, so summing local maps with maximum size u and incidence m yields

    +/- M(V) <= b m theta^(-ku) W.

Repeated unary tokens cause no problem: they increase k and b by fixed amounts, and no independence is assumed.

## 3. Convergence and exact transfer

For every finite physical volume, clean L is a bounded superoperator. With an infinite-dimensional retained bath, it is still a bounded physical superoperator tensored with the identity, and a bounded joint N admits the same Banach-space exponential identity. Thus the source's phrase “finite matrix identity” may be replaced by “bounded-superoperator identity” without changing the argument:

    exp(-sL)N exp(sL)=sum_n (-s)^n ad_L^n(N)/n!.

The incidence bound and relative-factor cost give

    +/- ad_L^n(N)V
      <= b eta theta^(-kq)
         [2Jr theta^(-kr)]^n (1+q/r)_n W.

For x(s)=2Jr theta^(-kr)s<1, absolute summation and the binomial generating function prove

    +/- M(s)V
      <= b eta theta^(-kq)(1-x(s))^(-1-q/r) W.

This is uniform in physical volume. The exact exponential identity itself exists at all finite s; the stronger uniform weighted-local estimate is what has the stated short-time radius. No positivity is attributed to exp(-sL).

Because exp(sL) is unital CP and N exp(sL)=exp(sL)M(s),

    N exp(sL)V <= C_T eta exp(sL)W.

If L W<=0 globally, then exp(sL)W<=W and integration gives the source's

    N F_T <= C_T eta T W,
    F_T=integral_0^T exp(sL)V ds.

The slightly sharper immediate statement retains the time integral:

    N F_T <= C_T eta integral_0^T exp(sL)W ds.

Time-dependent perturbations are handled pointwise with the same uniform incidence budget. This is not a noisy propagator expansion and does not accumulate an approximation error with storage time.

## 4. Conditional drift and basin order

If the actual finite-window service inequality holds at a horizon T satisfying x(T)<1, then

    L F_T=exp(TL)V-V

is exact, and the stated drift consequence follows. A service theorem only at a larger horizon does **not** automatically meet this condition; existence of a positive reset-tail probability at shorter time is not sufficient, as Section 6 shows.

The original per-move completion proof does extend V descent to W descent: an increasing source animal A is charged to B=A union D, with |A|<=|B|. Multiplying by these sizes cannot weaken the paying loss. This applies to the actual deterministic moves to which the full-animal proof applies, and to Hamiltonians commuting with the occupancy algebra. It is not a consequence of an arbitrary CP channel's V descent alone.

For the raw-barrier comparison, the same factor estimate gives the global local bound

    L f_A >= -c |A| f_A,
    c=bJ theta^(-kr).

Positivity implies exp(sL)f_A>=exp(-cs|A|)f_A: differentiate exp(cs|A|)exp(sL)f_A and apply exp(sL) to Lf_A+c|A|f_A>=0. Therefore, for a_+-a_0>=cT,

    F_T[V_+] >= T V_0.

This step is valid without a no-jump or bounded-depth representation of the semigroup.

If an order is only known inside P, applying exp(sL) to it requires Schrödinger preservation of P. Furthermore that preservation alone does **not** imply [P,F_T]=0; a separate covariance/block-algebra argument is necessary for the usual killed-observable comparison. The source correctly leaves both requirements open for the native generator. The two-weight inequality does not provide either one by itself.

## 5. Fixed-horizon W service is already impossible in the generic example

At each of m sites use a rate-one chain ready -> primed -> corrected. The defect remains present in the first two states. Starting all ready gives exact survival

    s(t)=exp(-t)(1+t),
    g(t)=theta+(1-theta)s(t).

Independent sites give, for all nonempty connected intervals on a path,

    E V(t)=sum_(ell=1)^m (m-ell+1) exp(a ell) g(t)^ell,
    E W(t)=sum_(ell=1)^m ell(m-ell+1) exp(a ell) g(t)^ell.

Both observables descend pointwise under every actual correction; the priming transition leaves them fixed. Local dimensions, rates and incidence are bounded, and there is no quantum interference or bath.

Put k=m-ell and r=exp(-a)<1. The normalized initial interval weights are proportional to (k+1)r^k. Their mean k stays bounded (in fact tends to 2r/(1-r)), so

    W(0)/V(0)=m-O(1),       V(0)>=exp(am).

Since V(0)-E V(T)<=V(0), a fixed positive alpha in

    V-exp(TL)V >= alpha W-bm I

would imply 1>=alpha[m-O(1)]-bm/V(0), impossible as m grows. The finite-window criterion fails even though each individual site has positive completion probability for every T>0.

## 6. Exact two-stage obstruction to integrated W

For 0<=t<=m^(-1/2),

    1-s(t)=integral_0^t u exp(-u)du <= t^2/2,
    g(t)>=1-(1-theta)/(2m).

Let c0=(1-theta)/2<1/2. For every ell<=m, Bernoulli gives

    g(t)^ell >= (1-c0/m)^m >= 1-c0 > 1/2.

The initial V weight of intervals with ell>=m/2 tends to one, because the shorter-interval contribution is at most polynomial(m)exp(am/2), whereas V(0)>=exp(am). For all sufficiently large m it is at least half V(0). Hence throughout that time interval,

    E W(t) >= (m/2)(1/2)(V(0)/2)=mV(0)/8.

For any fixed T>0 and m>=T^(-2),

    integral_0^T E W(t)dt >= sqrt(m)V(0)/8.

Again the total V decrement is at most V(0), while bm/V(0) tends to zero. No fixed alpha>0,b<infinity can make

    V-exp(TL)V >= alpha integral_0^T exp(tL)Wdt-bm I

hold uniformly. The p-stage generalization has g(t)=1-O(t^p), giving the analogous lower growth m^(1-1/p)V(0) for p>1.

Thus even retaining integrated W in the sharp noise-transfer estimate does not repair the generic service argument. A local reset-tail or fair-service statement cannot be substituted for the weighted inequality. This is a counterexample to the abstract implication, not a claimed embedding into the native code family or a proof that every alternative use of F_T is impossible.

## 7. Independent numerical regression and final status

`check_startup_obstruction.py` evaluates the full interval sums in normalized form, avoiding exponential overflow. With a=0.3, theta=0.1 and T=1, the integrated-W/V(0) ratio grows from 4.89 at m=16 to 85.24 at m=4096, while the normalized decrement never exceeds one. The corresponding admissible alpha without the asymptotically negligible linear allowance falls to 0.0117. These checks illustrate the exact divergence proof; they do not replace it.

**Final status:** the exact short-time connected-commutator transfer theorem is accepted at its conditional scope. The generic CP-average native-compiler bridge is not accepted, because its required weighted service premise is disproved by the stated elementary example. Actual native full-Hilbert monotonicity, controller-dependent local service weights, basin compatibility and readout remain separate obligations. The full-Hilbert simple-compiler receipt in `simple_compiler_whole_audit_20261030` remains unchanged.
