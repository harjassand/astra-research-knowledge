# A uniform raw-model certificate, rather than a favorable tail sample

This author verification accompanies `pinned_uniform_certificate.py` and its exact 5,802-byte JSON output. It is not an independent audit. The six-phase model has twenty directed raw reactions and source SHA-256 `fabcaded0fe13a8e0d552ab8fc050e2854a6fc05e7d953baac88e63630563050` for `results/pinned_phase_raw.json`.

The first diagnostic fixture had different equilibrium ratios in its two exchange channels. That version and its actual positive-head results are preserved under `results/pinned_v1/`. The current fixture aligns BOTH exchange ratios at 6/5, so its product-form obstruction is already in the hidden binding/switch cycle, not created by inconsistent exchange ratios. Current diagnostics retain 44 positive smaller-state drifts. No all-state sign is inferred by extrapolating the 54 negative sampled states.

## 1. Concrete raw data and the ordinary baseline

Controller levels are (0,1,2,0,1,2). Binding pairs between phases (0,1),(1,2),(3,4),(4,5) have forward/reverse rates (2,3),(4,5),(5,7),(6,11). Within-level phase pairs (0,3),(1,4),(2,5) have rates (11,13),(17,19),(23,29). Only phase 0 exchanges A/B. Its two pairs are

    A+E0 <-> B+E0                  with rates 3/2,5/4,
    A+2B+E0 <-> 3B+E0              with rates 7/5,7/6.

The sole reservoir is 0<->A with rates 1,1. The binding/switch square's forward/reverse rate ratio is

    (2/3)(17/19)(7/5)(13/11)=3094/3135 !=1.

For a candidate product-Poisson law in A,B with positive phase weights, the coefficient of the binding source's B dependence forces each upper/lower binding phase-weight ratio. After those terms cancel, the constant term forces the within-level isomerization ratio. The displayed square makes these requirements inconsistent. Both exchanges would instead agree on c_B/c_A=6/5. Thus the strongest simple ordinary product-Poisson construction is genuinely unavailable for this raw model. This is not a proof that no other established method can solve it; historical priority remains UNKNOWN.

All raw pairs are reversible. A phase can unbind down its ladder, switch to phase 0, convert B to A and remove A. Reversing this word builds every valid state. Hence the enzyme-total-one class is irreducible. The positive conservative core weight is (1,1,1,2,3,1,2,3), and M=a+b+j_s differs from weighted total by the constant one. The Poisson immigration bound proves nonexplosion without a truncation.

## 2. Exact acquired phase profile

Let n=b+j_s. For n>=10 kill the actual six-state Q_n at phase 0. In the notation of the general receiver, v_0=0 and the common denominator of the other hitting-time entries is

    D(n)=13050 n^2+242077 n+1034111.

The full rational vector is recorded in `results/pinned_phase_checks.json` and checked by (-Q_TT)v=1. It gives

    J(n)=2 P(n)/D(n),
    P(n)=6240 n^4+100484 n^3+494630 n^2+454043 n+954564.

Set t=11/10, u=137/125, c_t=7/1056 and

    epsilon(n)=7n D(n)/(2112 P(n)),
    h_s(n)=1+epsilon(n)v_s(n).

On n<10, set h=1. At every marked state h_0=1 for every n. Exact polynomial coefficient certificates after the shift n=x+10 verify

    epsilon(n)>=1/(200n),       1<=h_s(n)<=2, n>=10.

The generator identities Qh=-epsilon off the mark and 0<=Qh<=c_t n at the mark are exact. Each coefficient list in the JSON is a finite certificate on the entire half-line x>=0, not a finite set of values of n.

## 3. Uniform sign outside a finite rectangle

Take V=t^n h_s(n)+u^(a+n). Use Nstar=10000 and Astar=100000. At an unmarked phase with n>=10,

    LV/t^n=-epsilon(n)+(u/t)^n u^a[(u-1)-a(1-1/u)].

For a>=2 the bracket is negative. For a=0,1 its largest positive value after multiplication by u^a is u-1. The certificate checks

    (u-1)(u/t)^Nstar<=1/(400 Nstar).

Since ((n+1)/n)(u/t)<=1 for n>=Nstar, it follows for EVERY n>=Nstar that LV<=-t^n/(400n), for all a and every unmarked phase.

At the mark, let

    F(n)=3/2+(7/5)n(n-1),
    R(n)=(5/4)n+(7/6)n(n-1)(n-2).

The exact first summand has generator t^n[Qh+a(t-1)F-(1-1/t)R]. On a<=n/2 its upper bound is

    t^n[c_t n+(n/2)(t-1)F-(1-1/t)R] <= -(n/100)t^n.

The last inequality has a direct shifted-polynomial coefficient certificate for all n>=10. For a>=2 the second summand also has negative drift; for a=0,1 its positive normalized drift is at most u-1=0.096<n/100. This covers the whole marked a<=n/2 cone.

For a>n/2, n>=10, the possible positive first-summand drift is at most a n^2 t^n/5. The second summand is at most -c_z a u^(a+n), c_z=6/137. Put

    rho=u^3/t^2=10285412/9453125>1.

Then (u/t)^n u^a>=rho^floor(n/2). Exact integer-power comparisons at n=Nstar and Nstar+1 give

    c_z rho^floor(n/2)>=2n^2/5.

The inequality propagates separately along both parities because rho>=((n+2)/n)^2 for every n>=Nstar. Thus the high-A cone is received for ALL n>=Nstar, with half of its negative second-summand drift reserved.

Finally consider n<Nstar and a>=Astar. All positive first-summand terms are bounded by a(Nstar^2/5)t^Nstar; the n<10 cases obey this same very loose bound directly from their finite raw exchange list. The certificate checks

    c_z u^Astar >=2(Nstar^2/5)t^Nstar.

Consequently the whole remaining bounded-n/unbounded-a cylinder also has negative drift with a half reserve. Every state outside

    H={0<=a<100000, 0<=n<10000, all valid phases}

is covered. This rectangle is deliberately loose and has not been enumerated.

## 4. A specific complete exponential-reward inequality

Let r=1001/1000. The certificate additionally checks the exact reserves

    t^Nstar/(400Nstar)>=r^(Nstar+1),
    (c_z/2)(u/r)^Nstar>=1,
    [Nstar/100-(u-1)]t^Nstar>=r^(Nstar+1).

Their elementary monotonic ratios, recorded in the JSON, propagate to all larger counts. For a>=2, the reservoir part has margin at least (1-1/u)a/4=(3/137)a, so the same reserves apply in the other negative regions. Together the inequalities above give

    L V <= -r^M, outside H.                              (A)

Let S be the sum of all twenty actual rate constants, Mmax=110001 and Qmax=S Mmax^3. The free-species source order is at most three; enzyme source multiplicities are zero or one. On the head, all actual jump-target values obey

    V_target <= 2t^10001+u^110001.

Thus the finite positive rational expression

    C=Qmax[2t^10001+u^110001]+r^110001                    (B)

satisfies the COMPLETE inequality

    L V <= -r^M+C 1_H.                                  (C)

The JSON emits (B) as a factored expression. It is not materialized or advertised as a useful numerical tail constant. Its huge size and loose head are part of the actual construction, not an uncharged practical guarantee.

## 5. Stochastic receiving and cost

V is finite, positive and normlike. Nonexplosion is already controlled by immigration. The positive polynomial bound for h and the Poisson bound on M over finite times justify localized Dynkin and passage to the full finite-time reward inequality by dominated convergence; all polynomial rate factors are integrable against that bound. Equation (A) gives positive recurrence and uniqueness in the explicitly acquired irreducible class.

From (C), occupation-time averaging and Fatou on bounded truncations of r^M give

    pi(r^M)<=C.

No assumption pi(V)<infinity is needed. The general pinned-phase theorem separately proves every prescribed exponential moment by changing t,u and the finite head; this particular rational certificate emits the r=1001/1000 bound only.

The acquisition uses a five-by-five symbolic inverse, explicit polynomial identities, nonnegative coefficient lists and finitely many exact rational powers. Those operations were actually executed. The scientific claim is this scoped uniform mathematical construction. It is not a hardware demonstration, independently audited theorem, practical stabilization prescription, or complete arbitrary-network recurrence mechanism.
