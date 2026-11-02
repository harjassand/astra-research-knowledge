# An incompatible-gate candidate closed by an ordinary exact Foster function

Same-principal calculation. This is a complete ordinary calibration, not the unrestricted programme's endpoint or a historical-priority claim. It changes the diagnostic: an A-free evolving bath by itself does not force a new unresolved debt mechanism.

## Raw graph and all rates

There is one port 0->A at rate lambda and A->0 at rate mu A. Let H be finitely many hidden species. On an undirected graph G on H, each edge {i,j} has the four positive-rate conservative channels

    2Xi --alpha--> Xi+Xj --beta--> 2Xi,
    2Xj --gamma--> Xi+Xj --delta--> 2Xj.

Choose a set S of hidden vertices meeting EVERY component of G, and for each i in S add a positive-rate pair

    2A --p_i--> A+Xi --b_i--> 2A.

Isolated hidden vertices are allowed only if in S. There are no other genuine channels. All inventories evolve and all constants are arbitrary fixed positive. The hidden bath is A-free; hence the common catalytic-gate theorem does not apply. From an A-free hidden singleton the internal support cannot create A, so the ungated support theorem does not apply either.

Nevertheless one bounded angular correction gives a global receiver. Every actual class is positive recurrent; for every r>0 its stationary law has finite E[(1+q)e^(rN)]. The proof below uses genuine physical generator rates and pays every path. It does not rely on a bath equilibrium or a mixing gap.

## One elementary bath inequality

Put h_i=1/(Xi+1). For one oriented edge i<-j write R=Xj/(Xi+1). Direct falling-factorial differences give

    L_edge h_i
      <= alpha + delta R - gamma Xj(Xj-1)/[(Xi+1)(Xi+2)]
      <= alpha + (delta+gamma/2)R - (gamma/2)R^2
      <= C_(i<-j) - c_(i<-j)R^2,

    C_(i<-j)=alpha+(delta+gamma/2)^2/gamma,
    c_(i<-j)=gamma/4.

At Xi=0 the written positive mixed-source term is an overestimate, which preserves the inequality. Swapping i,j gives C_(j<-i)=gamma+(beta+alpha/2)^2/alpha and c_(j<-i)=alpha/4. Thus for h=sum_i h_i,

    L_bath h <= C_H - sum_(i<-j) c_(i<-j)[Xj/(Xi+1)]^2.       (B1)

These constants are acquired from raw rates; C_H is their finite sum. No unbounded positive bath term has been omitted.

## A bounded correction that pays the real seed

Fix ANY rational t>1, Delta=1-1/t, and choose an integer p>=1 with 2^p>=2t. Let h_count=|H|, B=sum_(i in S)b_i and P=sum_(i in S)p_i. Define

    c=4(t-1+1/lambda),
    0<e<=min[1/h_count, 1/(1+C_H), mu Delta/(4B)],
    g=1+c/(A+1)^p+e h,
    W=t^N g.                                                (B2)

In particular 1<=g<=G_max=1+c+e h_count. When A=0, the root pairs are inactive, but the actual port birth changes the correction. Its physical contribution is

    lambda[(t-1)(1+e h)+c(t/2^p-1)] <= -2.

By (B1), the bath can add at most e C_H<=1. Hence LW/t^N<=-1 on the ENTIRE A=0 face, including all simultaneously large hidden inventories. This is a real port jump, rather than a conditioned seed landing.

For A>=1, put d_p(A)=(A+1)^(-p)-(A+2)^(-p)>0. A forward root jump can add at most c p p_i to the A correction. A reverse root jump contributes exactly -c b_i A d_p(A)Xi there and at most e b_i A to the hidden correction. The full port contribution is bounded above by

    lambda(t-1)(1+e h_count)+lambda c t+mu c/t-mu Delta A.

Therefore, with

    C_0=lambda(t-1)(1+e h_count)+lambda c t+mu c/t+c p P+e C_H,

the ACTUAL full generator satisfies

    LW/t^N <= C_0-(3mu Delta/4)A
       -c sum_(i in S)b_i A d_p(A)Xi
       -e sum_(i<-j)c_(i<-j)[Xj/(Xi+1)]^2.                  (B3)

All competition between the root reactions, bath and port is present in this pointwise inequality.

## Finite propagation acquires the global head

Choose K_A>=4(C_0+1)/(mu Delta). For A>=K_A, (B3) is <=-1. If 1<=A<K_A, use

    A d_p(A)>=p/(K_A+2)^(p+1),
    b_S=c min_(i in S)b_i p/(K_A+2)^(p+1)>0.

If (B3) were greater than -1, every root vertex would satisfy Xi<(C_0+1)/b_S and every oriented bath edge would satisfy

    Xj/(Xi+1)<sqrt[(C_0+1)/(e c_(i<-j))].                   (B4)

Take an integer R>=1 bounding these finitely many square roots, M_0>=(C_0+1)/b_S, and M_(l+1)=R(M_l+1). Since every hidden component meets S, paths of at most h_count-1 edges propagate (B4) from a root to every hidden vertex. Thus all exceptions lie in the acquired finite head

    N<=K_A+h_count M_(h_count).                             (B5)

No enumeration of infinite faces or unevaluated expected landing law chooses this head. Equations (B1)-(B5) give LW<=-t^N outside it.

For a desired reward F=(1+q)u^N, 1<u<t, the raw quadratic rate list gives 1+q<=C_q N^2 for N>=1 with C_q=4(1+lambda+mu+sum kappa). Set zeta=1-u/t. Enlarge the head to include

    N>=(4/zeta)^2, N>=4C_q/zeta.

Then F<=t^N/2 and LW<=-F-W/(2G_max). Nonexplosion follows independently from N(s)<=N(0)+Pois(lambda s), since all core reactions conserve N. Dynkin's formula stopped at that head, followed by the true finite-head trace on each closed actual class, proves the full finite physical return/reward statement. Weak reversibility closes the actual classes. The bounded multiplier also permits an exponential physical-return conclusion for THIS graph family; this does not transfer to the banked ordered cycles, where that conclusion is false.

## Diagnostic decision

The three-species instance 2A<->A+B, 2B<->B+C<->2C, with all rates one except 2B->B+C at rate two, is not complex balanced: its hidden complex tree forces c_C/c_B=2 and c_B/c_C=1. The all-unit locus is already ordinary product-Poisson. The calculation above covers the generic instance exactly before treating it as evidence of an unsolved capability.

This rule allows arbitrary hidden graph feedback, several unpinned inventories and incompatible A-gated/A-free layers. It is a useful solved operation, but neither covers arbitrary conservative cores nor resolves the nonconservative coupled-cycle diagnostic. Its elementary bounded correction is the reason to move the hard test onward, not a reason to call the full programme complete.
