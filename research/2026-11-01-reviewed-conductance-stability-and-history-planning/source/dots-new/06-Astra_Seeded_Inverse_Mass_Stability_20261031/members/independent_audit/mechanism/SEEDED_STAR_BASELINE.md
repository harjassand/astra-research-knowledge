# Seeded direct-return stars: ordinary bounded service correction

This is a separate pending mathematical note. Earlier accepted packages are unchanged. No novelty or general-network claim is made.

## 1. Family and exact correction

Let the only nonconservative channels be `0->A` at lambda and `A->0` at mu. For each of m>=1 satellites B_j include

    2A+B_j -> A+2B_j     at alpha_j,
    A+2B_j -> 2A+B_j     at beta_j,

with positive rates. Any additional finite internal channels preserving both A and total count N are invisible to the function below. Full weak reversibility is retained for the classwise recurrence conclusion.

Fix t>1 and set

    D=mu(1-1/t),  alpha=max_j alpha_j,  beta=min_j beta_j,
    L=alpha+beta/2,
    0<c<=min(1,D beta/(2m L^2)),
    h(0)=2t(1+c),       h(a)=1+c/a for a>=1,
    W(x)=t^N h(A).

All choices can be rational for rational input rates and t. This is a supplied explicit ordinary comparator for the stated family, not a claim that a general parser or unknown grouping has been acquired.

For a>=2, the internal drift of h is exactly

    L_internal h=c sum_j alpha_j B_j
                    -c sum_j beta_j(B_j)_2/(a+1).

Indeed a forward propensity is alpha_j a(a-1)B_j and its h increment is c/[a(a-1)]. A reverse propensity is beta_j a(B_j)_2 and its increment is -c/[a(a+1)]. At a=1 the forward terms are absent, while the reverse formula still holds. Thus the same displayed expression is an upper bound at that layer. All A,N-preserving remainder channels contribute zero, regardless of their order.

## 2. Internal quadratic estimate

Write b=sum_j B_j. Since `(B_j)_2>=0` at integer counts and a+1>=2,

    L_internal h/h <= (c/h)[L b-beta b^2/(m(a+1))].

Split the negative square in half. Using h<=1+c for the retained negative part, completing the square for the other half, and h>=1 yields

    L_internal h/h
       <= -k b^2/(a+1)+[c m L^2/(2 beta)](a+1),
    k=c beta/[2m(1+c)].

This remains valid on the first active layer a=1. The choice of c makes the positive coefficient at most D/4.

## 3. Core and extinction face

For a>=1, h decreases under immigration, so immigration contributes at most lambda(t-1). At a>=2, the death quotient is

    -D a + mu c/[t(a-1)h(a)] <=-D a+mu.

At a=1, death has quotient exactly mu because h(0)/h(1)=2t. A uniform bound on all positive-A states is consequently

    death quotient <=-D a+(mu+D).

At a=0, all seeded star channels are disabled and every A,N-preserving remainder is invisible. The immigration quotient is exactly

    lambda[t h(1)/h(0)-1]=-lambda/2.

This infinite face has uniformly negative constant quotient; it does **not** have negative-linear-in-N quotient. It must be treated separately rather than silently included in a claim `LW/W<=C-kappa N` everywhere.

For a>=1 we obtain

    LW/W <= C0-(3D/4)a-k b^2/(a+1),
    C0=lambda(t-1)+mu+5D/4.

For N>=1, splitting at a>=N/2 and using a+1<=N+1<=2N in the other case gives

    LW/W <=C0-kappa N    on a>=1,
    kappa=min(3D/8,k/8)>0.

This choice is deliberately simple rather than optimized.

## 4. Global geometric Foster and all moments

Set

    zeta=min(lambda/2,kappa),
    R=max(1,ceil((C0+zeta)/kappa)),
    C_F=(C0+zeta)(1+c)t^R.

For a=0, `LW<=-zeta W` at every population. For a>=1,N>=R the same holds. On the remaining finite set, h<=1+c gives

    LW<=-zeta W+C_F

globally. W is normlike and uniformly comparable to t^N, with h>=1 and h<=2t(1+c).

Only constant-rate immigration increases N, so ordinary Poisson domination proves nonexplosion. Weak reversibility makes state communicating classes closed. The Foster inequality proves classwise positive recurrence. Stopped-semigroup estimates followed by invariant concave truncation/Fatou give finite invariant t^N moments without assuming them in advance. Since t can be arbitrarily large, every finite exponential count moment follows. Neither a product-form stationary law nor a fast-fiber equilibrium is required.

## 5. Exact product-Poisson comparator scope for two satellites

For the minimal m=2 network with no other remainder channels, include the reversible neutral channel

    A+2B -> A+2C at gamma,
    A+2C -> A+2B at delta.

A direct detailed-balance product-Poisson candidate has parameters

    z_A=lambda/mu,
    z_B=(alpha_B/beta_B)z_A,
    z_C=(alpha_C/beta_C)z_A.

The two seeded-star edge balances and the core balance force precisely these ratios. The neutral edge additionally requires

    gamma (alpha_B/beta_B)^2
       =delta (alpha_C/beta_C)^2.                       (*)

When (*) holds, every raw reversible pair is individually balanced by the product-Poisson measure; conditioning that measure on any closed communicating class preserves detailed balance. This is a direct conventional comparator.

When (*) fails, this standard product-Poisson route is unavailable. This conclusion can be made classwise here. The A-only states form one closed immigration/death class. All states with B+C>=1 form another class Gamma: raise A to at least two by immigration; use reverse stars to reduce each positive satellite count to one; if B remains, a forward B star creates two B, the neutral conversion transfers those two to C, and reverse C stars reduce C to one. Core deaths then reach `(0,0,1)`. Every move has an enabled reverse. Thus Gamma contains the whole grid with B,C>=1 and A>=0.

For a product-Poisson density, dividing the stationary master equation by that density yields a finite polynomial in falling factorials, with each complex's coefficient equal to its inflow-minus-outflow complex-balance residual. If a conditioned product-Poisson law on Gamma were invariant, this polynomial would vanish on that whole infinite grid and hence identically. Balance at the two leaf complexes forces the two star ratios above; the remaining neutral balance forces (*). Therefore incompatibility rules out a product-Poisson law conditioned on Gamma as well. The A-only class still has its ordinary Poisson law.

No absence of every conceivable non-Poisson product form or other stationary representation is inferred. The explicit bounded service correction proves the required stability without settling those stronger questions.
