# Productive dilution defeats an A-only incoming profile

30 October 2026. Exact abstract local obstruction, not a counterexample to earlier fixed-rate or birth/seed theorems.

Fix q,gamma,kappa>0 and integer killing degree m>=1. There are n labels. Source C enters the working pool at rate gamma per source label. Each entry creates one working rank1 label AND chooses one of the previous Y working labels uniformly, resetting that label to rank1. (If Y=0, no reset is made.) Every working rank1 label progresses independently to target rank0 at rate q. Thus each existing working label has adverse participation gamma C/Y, batch size1. For Y>=1 this is <=2 gamma C/(1+Y), so PRODUCTIVE_POOL_FORCING applies. Kill at rate kappa(A)_m.

Take initial Y=A=a_n=floor(n^epsilon), all initially working labels target, with

    0<epsilon<min{1/4,1/(m+1)}.

Set T_n=a_n^2/n, which tends to zero. Let the comparison process suppress all working progress until T_n. Its working population is

    Y_t=a_n+Binomial(n-a_n,1-exp(-gamma t)),

independent of which labels the entry resets select. Write Z_t for the initially-target labels not yet reset. Conditional on Y_t=y, each growth step at working size r preserves a given old target with probability1-1/r. Therefore

    E[Z_t |Y_t=y]=a_n(a_n-1)/(y-1).

More generally, for a fixed j<=a_n-1,

    E[(Z_t)_j |Y_t=y]
       =(a_n)_j (a_n-1)_j/(y-1)_j.                 (D)

This follows because j distinct specified old labels all avoid one reset with probability1-j/r, and the product telescopes as r runs from a_n to y-1. It is not independent survival of the old targets.

At T_n the binomial mean is of order a_n^2. A lower-tail Chernoff bound in (D), first for j=1, gives E Z_(T_n)<=C uniformly in n. In contrast the incoming inverse profile is f_s(A_0)=(1+a_n)^(-s)->0.

The probability that ANY working progress occurs by T_n is at most

    q E integral_0^T_n Y_t dt
       <=q[a_n T_n+gamma n T_n^2/2]
       =O(a_n^3/n+a_n^4/n)->0.

Thus the comparison agrees with the actual target dynamics up to T_n with probability tending to1.

The kill also occurs before T_n with probability tending to0. Indeed pay the preceding progress event separately; otherwise its hazard is kappa(Z_t)_m. For t<=a_n/n, use (Z_t)_m<=a_n^m. For a_n/n<t<=T_n, binomial concentration and (D) give the integral bound

    E integral_0^T_n (Z_t)_m dt
       <= C a_n^(m+1)/n + o(1),           m>1,

and <=C a_n^2 log(a_n)/n+o(1) for m=1. To see the concentration step explicitly, Y_t>=c n t except with probability exp(-c' n t); on that event (D) is at most C a_n^(2m)/(nt)^m. Integrate this power from a_n/n to T_n. The exceptional contribution is bounded by a_n^m integral_(a_n/n)^T_n exp(-c'nt)dt, hence negligible. The chosen epsilon makes every displayed bound tend to0. The actual kill compensator then gives P(tau<=T_n)=o(1).

Choose a fixed K with P(Z_(T_n)<=K)>=3/4, using the uniform first moment. With probability at least1/2 for n large, no working progress and no killing occurred, and A_(T_n)<=K. Consequently, for every fixed s>0,

    E[f_s(A_(T_n));T_n<tau]>= (1/2)(1+K)^(-s)>0,

while f_s(A_0)->0. There can be no population-uniform bound

    E[f_s(A_t);t<tau]<=C_s f_s(A_0)

for this productive-pool class. This pinpoints the missing incoming-profile interface; good deterministic forcing alone does not repair it.

## A precise candidate carried variable, not a completed solution

In the no-progress comparison, a growth/reset jump Y->Y+1 satisfies

    E[Z_after * Y |Z_before,Y]=Z_before*(Y-1).

Thus Z(Y-1) is exactly a martingale for the entry/reset part. Ordinary progress increases A(Y-1). This suggests carrying a dilution-aware quantity such as A(Y-1), suitably normalized by total population, instead of A alone. No inverse-profile supermartingale, full Green or signed-cycle theorem is claimed from this observation; its jump corrections and seed/return costs still need proof.
