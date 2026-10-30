# Collective Green with genuine replenishment and competing seed deletions

30 October 2026. New local candidate; not yet reviewed or integrated into a full chemical section.

## Contract

Use the collective rank process with q,b,k,L fixed. Add one-label immigration at constant rate lambda>0, with the new label of any rank<=L. Immigration does not alter existing ranks. Kill at rate h(A)=kappa(A)_m. Add seed marks of intensity v<=c h(A), each deleting at most d existing labels and otherwise leaving surviving ranks unchanged. Constants are fixed. All progress/safe/adverse bounds remain uniform as the population changes and after every seed. No other population losses occur. The exact process is nonexplosive, and the kill/seed marks have their stated predictable intensities. Total population is bounded above by initial n plus its immigration count.

For every delta<min{1/(2L-1),m/(Lm+1)}, this contract gives, for n large and t_n=n^-delta,

    E tau^j <= C_j t_n^j,
    E integral_0^tau f_s(A_t)dt <= C_s t_n f_s(A_0),
    E[f_s(A_out); kill] <= C_s f_s(A_0),
    E[f_(s+p)(A_out); kill]
       <= C_(s,p) n^[-delta p/(2p+m)] f_s(A_0).

Here f_s=(1+A)^(-s), and the kill output removes at most m targets. No claim is made about a raw network satisfying the contract, physical-clock conversion, or signed-cycle negativity.

## 1. Independently earn a uniform replenishment/head bound

From any state with fewer than m labels, no kill or seed is enabled. Within one unit of time, m immigrants arrive with probability at least p_birth=P(Pois(lambda)>=m)>0. Thus by time1 either a mark has already occurred or there are at least m labels; when initially fewer than m, stop at the first time their number reaches m. When initially at least m, start immediately.

Choose m labels. Before the first kill/seed mark there are no deletions. In the next unit interval, give each selected label at least L progress rings and suppress all adverse events touching that cohort. Its aggregate adverse-event intensity is at most bm, so it has an independent dominating potential clock of rate bm. Together with the independent progress potential clocks this event has probability p_progress>0, uniform in all other state variables. Safe moves help. If a kill/seed mark occurs earlier, the first-mark stage has already ended. If not, this event leaves all m labels at the target.

During a further unit interval suppress cohort adverse touches again (probability>=exp(-bm)). On this potential event, until the first mark the total mark hazard is >=h(m)>0. Hence the probability that SOME mark occurs within the combined bounded window is bounded below by a constant p_mark>0, uniformly in the starting state. The argument uses unconditioned potential events: an early mark counts as success, not a reason to condition the cohort law on survival.

At its actual occurrence, the first mark is a kill with conditional probability >=r=1/(1+c), since v<=c h. The event that its time lies in the bounded window is determined before its mark type is chosen. Therefore a kill occurs in a fixed time window with probability >=p_birth p_mark r>0 from EVERY state. Repeat after each window while alive. This gives uniform exponential tail and all moments for the remaining killing time, independently of the large-n estimates below. This is the missing genuine head/replenishment mechanism in SEED_EXTENSION_OBSTRUCTION.md.

## 2. Actual large-n survival with deletions

Keep virtual identities for the initial n labels after deletion. A deleted label continues a virtual rank process with progress q and no adverse moves; surviving labels follow their exact ranks. Potential progress clocks were attached before deletion. The resulting n-label virtual process satisfies the collective contract, even though the physical state influences surviving labels' rates. At all times,

    actual target count >= virtual target count - d N_seed,

where N_seed counts actual seeds. New immigrants only help this inequality.

The competing-mark ratio implies P(N_seed before kill>=j)<=rho^j, rho=c/(1+c)<1 (if c=0 there are no seeds). This does NOT by itself imply finite killing time; step1 earned that separately.

At t_n/2, virtual collective forcing supplies M=floor(c0 n t_n^L) target identities except with probability exp[-c n t_n^(2L-1)]. During the second half-block the bounded-touch argument from COLLECTIVE_KILLED_GREEN, now with threshold M/4, keeps at least3M/4 of that cohort virtual targets except with probability exp(-cM). If fewer than M/(4d) seeds occur before killing (omit this condition if d=0), at least M/2 remain physical targets throughout that half-block. The probability of the excluded seed-count event before killing is <=exp(-cM).

On the survival event tau>t_n all these comparisons concern the actual process before killing. Outside the three exceptional events, integrated killing hazard is >=c t_n M^m. The independent hazard-clock realization therefore gives

    P(tau>t_n) <= C exp(-c n^epsilon)

for some epsilon>0. No law is conditioned on survival in the forcing estimate. The lower bound on the hazard is only used on the actual survival event; marks after killing are irrelevant.

Using step1 conditionally at time t_n, the residual lifetime has uniformly bounded moments and exponential tail. Thus E tau^j<=C_j t_n^j. More precisely,

    P(tau>t_n+u)<=C exp(-c n^epsilon) exp(-c' u),

and integral_0^infinity P(tau>t)^(1/2)dt<=C t_n.

## 3. Incoming profiles survive seeds through a killed barrier

The prior un-killed bound Lf_s<=C_s f_s is no longer true for seed deletion: its intensity can be superlinear in A. Use killing absorption rather than ignore that term.

For A>=2d, a seed loses at most d targets and

    L_seed f_s <= c h(A) C_(s,d) f_s(A)/A.

The bounded adverse component contributes <=C_s f_s; progress, safe moves and immigration contribute<=0. Take V=2f_s and kill reward g=f_s. For a sufficiently large fixed threshold R_s,

    L_nonkill V - h V + h g <=0,   A>R_s,

because the seed term is O(h/A) V, the adverse term is O(V), and h(A) grows as A^m. Choose R_s also larger than m,2d,2k. All constants depend only on fixed grades and model constants.

Stop at killing or first entrance into A<=R_s. Localized Dynkin with the displayed reward yields

    E[g(A_(tau-)); kill before low] <=2f_s(A_0),
    P(low before kill) <=C_s f_s(A_0).

The second inequality follows because V at a low entrance is bounded below by2(1+R_s)^(-s). For initial A<=R_s the corresponding bounds are trivial after increasing constants. After a low entrance, a terminal inverse profile is <=1. Hence

    E f_s(A_(tau-))<=C_s f_s(A_0).

A kill removes at most m targets, so its actual output obeys the same estimate. No seed output is being called a terminal kill output.

The same killed barrier, stopped before low, bounds E[f_s(A_t);t<tau,no low yet] by C_s f_s(A_0); the low-entry probability bounds the remaining contribution. Therefore, uniformly in deterministic t,

    E[f_s(A_t);t<tau]<=C_s f_s(A_0).

Apply this with grade2s and Cauchy-Schwarz, then use the square-root survival integral from step2. This proves the stated graded occupation estimate. This is not an optional-stopping claim for an un-killed seed process.

## 4. Stronger output grade

The actual kill compensator gives P(A_(tau-)<=K)<=C K^m E tau<=C K^m t_n. Combine this with terminal grade2s preservation and split at K>=2m exactly as in COLLECTIVE_INCOMING_GRADE_COMPLETION.md. Choosing K proportional to n^[delta/(2p+m)] gives the displayed stronger-output reset.

## Unclosed interfaces

The theorem's positive-rate replenishment, surviving-label bounds and pure-deletion seed action are real assumptions. Immigration into an unbounded-rank or inert class, seed-driven changes that violate the collective contract, an unpriced clock change, or terminal activation outputs are not covered. This is an actual local Green mechanism with immigration and deletions, not an automatic extension of the reviewed raw compiler or of global recurrence.
