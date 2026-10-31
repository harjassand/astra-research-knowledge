# Acquired infinite-fiber corrector for catalytic star lifts

## Result first

A raw finite reaction list can acquire, rather than assume, a Lyapunov corrector for the following arbitrary-dimensional class. Take any finite weakly reversible one-species core on a distinguished count A; attach any number of unbounded counts B_j through positive-rate pairs

    2A -> A+B_j,     A+B_j -> 2A.

Permit any further reactions that preserve both A and the total count N=A+sum B_j. If the complete reaction graph is weakly reversible, every closed communicating class is nonexplosive and positive recurrent, and its invariant law has every exponential moment of N. There is no restriction on the molecularity of the one-species core or the neutral reactions.

The pivot, core, star, and neutral remainder are found by a finite raw-list scan. For rational rates and any rational t>1, a terminating exact rational calculation constructs V_t and explicit epsilon,C with LV_t <= -epsilon V_t+C on the nonconservative part. It does not supply a stationary distribution, assume a fast-fiber mixing estimate, or truncate the unbounded satellite counts.

**Status:** derived here with an executable exact certificate and finite challenges; independent whole-proof audit pending. No historical novelty, external review, general weak-reversibility theorem, or physical capability is claimed. All objects are abstract count-process mathematics.

## 1. Precise input and generator

There are d=k+1 counts (a,b_1,...,b_k). Non-null core reactions are uA -> vA, u != v, with positive rate kappa_uv and stochastic mass-action propensity kappa_uv (a)_u. The directed graph on the integer complexes u,v is weakly reversible. Star rates are alpha_j for 2A -> A+B_j and beta_j for its reverse. Put alpha=sum alpha_j and beta_min=min beta_j. Every satellite has both rates positive. Arbitrary additional finite reactions must have delta a=0 and delta N=0. Their intensities may have arbitrary molecularity and rational positive rates; their contribution to every function of (a,N) is exactly zero.

All reaction graphs and neutrality checks use the actual input list, after deleting null channels and aggregating parallel star channels. The program also verifies weak reversibility of the full reaction graph. This last condition supplies classwise closedness; it is not used to manufacture a drift inequality.

If the core has no non-null reactions, every jump preserves N and all reachable classes are finite. Otherwise let M be its greatest source complex. Weak reversibility implies every complex is a source, so all targets are <=M. A non-null reaction with source M has target <M.

## 2. The acquired correction

Fix rational t>1. If M>=2 take c=1. If M=1 the non-null core consists of 0<->A; write mu for its aggregate death rate and take

    0<c<=mu(1-1/t)/(2 alpha)

when alpha>0; any rational positive c works when no satellites are present. The implementation also caps c by 1.

Set g(1)=1 and, for integer a>=1,

    g(a+1)/g(a)=a/(a+c),
    g(a)=product_{r=1}^{a-1} r/(r+c).

For every inflow 0->vA choose

    g(0)>t^v g(v).

The program uses 1+max_v t^v g(v); when there is no inflow it uses g(0)=1. Set

    V_t(a,b)=t^N g(a).

These are exact rational numbers at every integer state. No Gamma-function oracle is needed. The optional identity g(a)=Gamma(a)Gamma(1+c)/Gamma(a+c) is merely notation.

For a>=1,

    exp(-c) a^(-c) <= g(a) <=1,

since log(1+c/r)<=c/r and H_(a-1)<=1+log a. Consequently V_t has finite sublevel sets. For each 1<t'<t, a constant K(t,t',c)>0 satisfies V_t>=K(t')^N, because a<=N and exponential growth dominates N^c. Thus integrability of V_t for arbitrary t implies every exponential total-count moment.

## 3. Exact generator identity, including the extinction face

Define the core quotient, with only enabled terms included,

    P(a)=sum_{u->v} kappa_uv (a)_u [t^(v-u)g(a+v-u)/g(a)-1].

For a>=2 the full generator quotient is exactly

    LV_t/V_t = P(a)+c alpha a
                - [c a/(a+c)] sum_j beta_j b_j.                 (1)

Indeed the forward star jump keeps N fixed and changes a to a-1. Its g-ratio minus one is c/(a-1), which cancels the factor a-1 in a(a-1). A reverse star jump changes a to a+1; its ratio minus one is -c/(a+c). Neutral reactions contribute zero.

For a=1 the same expression holds with the positive term c alpha a deleted, because the forward star source 2A is disabled. The negative term remains exactly as written. In particular the first nonzero pivot layer retains a restoring contribution linear in every satellite count.

For a=0 all star reactions are disabled, and

    LV_t/V_t = sum_{0->v} kappa_0v [t^v g(v)/g(0)-1].           (2)

If an inflow exists this is a strictly negative constant, uniformly over ALL satellite counts. The finite correction g(0) is indispensable: the formula from a>=1 cannot be extrapolated to zero.

If no inflow exists, weak reversibility of the core implies that 0 is absent from all non-null core reactions. Then a=0 cannot communicate with a>=1; on a=0 every permitted remaining reaction preserves N. Each such reachable class is finite. It need not be an absorbing singleton if neutral reactions are present.

## 4. Tail control in the pivot coordinate

For a>M, every core ratio is a finite rational function:

    g(a+j)/g(a) = product_{r=0}^{j-1}(a+r)/(a+c+r),       j>=0,
    g(a-j)/g(a) = product_{r=1}^{j}(a+c-r)/(a-r),         j>=0.

All denominators are positive in this region. Every ratio tends to 1 as a tends to infinity. Thus when M>=2,

    P(a) = a^M sum_{M->v} kappa_Mv [t^(v-M)-1] + O(a^(M-1)).

The leading coefficient is strictly negative. Hence H(a)=P(a)+c alpha a tends to -infinity. This works even for a cubic core attached to quadratic conversion channels; it is not a binary-only theorem.

When M=1, write lambda for the aggregate immigration rate. For a>=2,

    H(a) = lambda[t a/(a+c)-1]
           +mu a[t^(-1)(a+c-1)/(a-1)-1]+c alpha a.

The coefficient of a is -mu(1-1/t)+c alpha <=-mu(1-1/t)/2<0 when satellites exist. Without satellites it is strictly negative without the c alpha term. Thus H(a) again tends to -infinity.

## 5. A terminating finite exact threshold construction

Write H(a)+1=Q(a)/D(a), with rational polynomials and D positive for a>M. Start R>=max(2,M+1), double R, and substitute a=R+z until every coefficient of Q(R+z) is nonpositive and every coefficient of D(R+z) is nonnegative with positive constant term. The denominator sign is normalized first.

This search terminates: Q has negative leading coefficient, so all its derivatives are eventually negative (zero derivatives beyond its degree cause no issue); D has positive leading coefficient, so all of its derivatives are eventually positive. The Taylor coefficients at R therefore have the required signs. It follows for every real a>=R, not merely on a grid, that H(a)<=-1.

There remain finitely many pivot layers 1<=a<R. Compute their exact H_a=P(a)+c alpha a for a>=2, and H_1=P(1). Their satellite coefficient is at least

    d_a=[c a/(a+c)] beta_min >0.

For epsilon=min(1,-(2)) when inflow exists, and epsilon=1 otherwise, choose a rational/integer B_a with H_a-d_a b<=-epsilon whenever b>B_a. Then the exceptional set

    K={1<=a<R, sum b_j<=B_a}

is finite. On a=0 with inflow, (2) already supplies drift -epsilon; without inflow the separate finite-shell classes are handled directly.

An explicit safe global constant is

    C=max_a t^(a+B_a)g(a) max(0,H_a+epsilon),

omitting negative B_a. Since g depends only on a and the negative satellite term can only lower the quotient, this proves

    LV_t <= -epsilon V_t+C.                                 (3)

The program records the actual shifted polynomial coefficient witnesses, every finite-layer threshold, and exact rational epsilon,C. No efficient bit-complexity claim is made. Recognition tries at most d pivot candidates; polynomial arithmetic, coefficient growth, and threshold-doubling work are real charged costs. The generic finite terminal-gap criterion in the separate subdirectory has a different cost contract.

## 6. Probabilistic conclusion

On the nonconservative part V_t is positive, normlike, and has finite generator sums at every state. The usual stopped-Dynkin argument applied to (3) bounds the probability of leaving increasingly large finite sublevels before any fixed time, proving nonexplosion. A finite state set has bounded rates, so explosion cannot remain hidden inside a sublevel despite arbitrarily high-degree neutral channels.

Outside a sufficiently large finite sublevel, (3) gives LV_t<=-1. The stopped optional-sampling estimate therefore gives finite expected hitting time of that finite set from every state. Weak reversibility lifts every complex return path to an enabled population return path, so each reachable set is a closed irreducible class. Standard finite-set regeneration gives positive recurrence. The stationary moment conclusion does not assume that either pi(V_t) or pi(Lambda) is already finite. Stopped exponential Dynkin and Fatou first give, for every T>0,

    P_T V_t <= r V_t+b,    r=exp(-epsilon T)<1,
    b=C(1-r)/epsilon.

Let phi_n(v)=min(v,n). Invariance and concavity give

    integral phi_n(V_t) d pi <= integral phi_n(r V_t+b) d pi.

The difference phi_n(V_t)-phi_n(rV_t+b) is bounded below by -b and tends pointwise to (1-r)V_t-b. Fatou therefore yields (1-r)pi(V_t)<=b, proving pi(V_t)<=C/epsilon. As t>1 is arbitrary, the lower bound in Section2 yields pi(exp(theta N))<infinity for every finite theta>0.

No uniformity over rate constants, number of species, requested exponential exponent, or communicating classes is asserted. The constants change with these inputs. No general conclusion about all weakly reversible networks or arbitrary fast generators is obtained.

## 7. Executed witness and exact non-complex-balance obstruction

`pivot_lift.py` acquires pivot A from a three-species reaction list containing

    0 <-> A             rates1,1
    2A <-> 3A           rates2,1
    2A <-> A+B          rates2/3,5/7
    2A <-> A+C          rates3/2,7/5
    2B+C <-> B+2C       rates3,4/3.

The first component forces a=1 at any complex-balanced concentration. At complex3A, which is a leaf of its component, complex balance forces2a^2=a^3, hence a=2. These requirements contradict one another. The proof therefore cannot be reduced to a complex-balanced Poisson stationary law for this example.

The last reversible pair preserves A and N, so its entire generator contribution to V is zero. Its high molecularity and nonlinear rates do not require an additional averaging premise.

The executed checks include the exact all-population coefficient certificate, 6,760 exact rational grid states as a separate challenge, the deficiency-zero baseline, a core without the zero complex, removal of neutral channels, species/reaction permutations, and rejection of an unauthorized satellite immigration channel. These finite checks do not prove the theorem; the identities and coefficient certificate do.

## 8. Prior-art positioning and unresolved scope

This is a sufficient structural closure/construction, not an asserted first theorem. Classical Foster-Lyapunov theory, one-dimensional maximal-source dissipation, and rational/gamma-function recurrences are standard machinery. The baseline 0<->A,2A<->A+B_j is deficiency zero and complex balanced, so its recurrence and moments are already classical. The value of that baseline here is that it defeats finite same-linkage target-following drift while admitting an explicit acquired infinite-fiber correction.

The actual three-species witness is not complex balanced. This alone does not establish novelty relative to general non-product-form recurrence criteria. Relevant primary comparators are Hoessly and Mazza, *Stationary Distributions and Condensation in Autocatalytic Reaction Networks* (2019), https://doi.org/10.1137/18M1220340, and Hoessly, *Stationary distributions via decomposition of stochastic reaction networks* (2021), https://doi.org/10.1007/s00285-021-01620-3. Their product-form and compatible-decomposition machinery should not be replaced by an unsubstantiated novelty claim. This construction does not assume compatible invariant factors.

The current broader fronts are separate: the ConStRAINeD project announces two-species weak-reversibility recurrence, but its item16 is in preparation and was not inspected as a proof; the independent August2026 marked-target manuscript claims the single-linkage bimolecular theorem; Agazzi–Laurence arXiv:2610.31550 supplies bulk criteria with boundary obligations. None is used as a premise in this pivot proof.
