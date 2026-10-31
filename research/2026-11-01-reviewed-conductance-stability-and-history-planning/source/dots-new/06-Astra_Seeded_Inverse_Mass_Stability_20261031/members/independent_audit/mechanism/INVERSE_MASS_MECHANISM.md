# Independent check of inverse acquired mass for the hard seeded lift

This is a mechanism-level proof, not acceptance of a frozen compiler. Consider

    0 <-> A,
    2A+B -> A+B+C at alpha1; reverse beta1,
    2A+C -> A+2B at alpha2; reverse beta2,
    A+B+C -> A+2C at alpha3; reverse beta3.

All rates are positive. Only the core changes total count N. The no-go for every positive normlike `F(A,N)` is proved separately; the correction below resolves mediator B as well.

## Exact channel estimates

Choose `0<eta<=min(1/4,beta1/(4 alpha3))`. On A>=1 put

    R=A+eta B,   h=1+c/R,   0<c<=1.

At A=0 patch `h=2t(1+c)`. Let `W=t^N h`.

For an internal R increment z, the exact h increment is `-c z/[R(R+z)]`. The R increments of the six channels in the displayed order are `-1,+1,-(1-2eta),+(1-2eta),-eta,+eta`.

The mixed BC pair contributes at most

    c A BC/R^2 [-beta1/2+alpha3 eta/(1-eta)]<=0.

Indeed R>=1, R+1<=2R, R-eta>=(1-eta)R, and the eta bound gives `alpha3 eta/(1-eta)<=beta1/3`.

Let `r=A-1`, `alpha=max(alpha1,alpha2)`. The two A-loss channels are enabled only at A>=2. Then R>=2, their negative increments have magnitude at most one, and the total positive contribution is at most

    2c A alpha r(B+C)/R^2.

The positive R increments in the pure-B and pure-C reverse channels give the upper bounds

    -c A u(B)_2/R^2,    -c A v(C)_2/R^2,
    u=beta2/4,          v=beta3 eta/2.

The first-layer A=1 case causes no singularity: both A-loss propensities vanish, and every remaining R remains positive.

Therefore, using r<=A and A>=1,

    L_internal h <=(c A/R^2)
        [A L_B B+A L_C C-uB^2-vC^2],
    L_B=2alpha+u,    L_C=2alpha+v.

Completing the two squares and using R>=A, h>=1, h<=1+c yields

    L_internal h/h
       <=c K_eta A-c A(uB^2+vC^2)/[2(1+c)R^2],
    K_eta=L_B^2/(2u)+L_C^2/(2v).

## Core, exact acquisition and termination

On A>=1 immigration decreases h, giving quotient at most `lambda(t-1)`. At A>=2 death gives at most `-D A+mu`, where `D=mu(1-1/t)`. At A=1 death to the patched layer contributes at most `3mu`; hence the uniform bound is `-D A+3mu+D`. At A=0 immigration gives quotient at most `-lambda/2`, with equality only when B zero.

Take

    c=min(1,D/(4K_eta)),
    C0=lambda(t-1)+3mu+D,
    zeta=min(lambda/4,D/4,1).

Then on A>=1,

    LW/W<=C0-3D A/4-c A(uB^2+vC^2)/[2(1+c)R^2].       (1)

Halve eta until

    c u/[4(1+c)eta^2]>=C0+zeta.                         (2)

This acquisition terminates without an unspecified lifetime or equilibrium oracle. Write `k=beta3/2` and note, for eta<=1,

    K_eta <= Kbar/eta,
    Kbar=(2alpha+u)^2/(2u)+2alpha^2/k+2alpha+k/2.

With `c0=min(1,D/(4Kbar))`, we have `c>=c0 eta`, so the left side of (2) is at least `c0 u/(8eta)`. Therefore every eta at most `c0 u/[8(C0+zeta)]` passes. One may choose this explicit bound directly; halving is only a potentially less conservative exact search.

## Finite exception acquisition

Define integers

    A_cut=ceil[4(C0+zeta)/(3D)],
    B_cut=ceil[3A_cut/eta],
    Rbar=A_cut+eta B_cut,
    C_cut=ceil_sqrt[u Rbar^2/(2v eta^2)].

First handle `A>=A_cut` using the linear death term. In the remaining branch `1<=A<A_cut`, if `B>=B_cut`, then `R<=(4/3)eta B`, so

    (uB^2+vC^2)/R^2 >=u/(2eta^2).

**The restriction A<A_cut is necessary for this particular ratio claim.** If also `B<B_cut`, then R<=Rbar; the C cutoff gives the same ratio whenever C>=C_cut. In either case the negative last term in (1) is at least `A(C0+zeta)>=C0+zeta`, leaving quotient at most `-zeta`. The entire A-zero face already has quotient at most `-lambda/2<=-zeta`.

Thus only the finite positive-A box

    1<=A<A_cut, 0<=B<B_cut, 0<=C<C_cut

remains. With `S=A_cut+B_cut+C_cut`, an explicit global Foster constant is

    C_F=(C0+zeta)(1+c)t^S.

The bound is conservative and may remain factored. It does not require enumerating the finite box. Poisson immigration domination proves nonexplosion, reversibility makes classes closed, and the same noncircular stopped-semigroup argument gives every finite exponential invariant total-count moment, because t was arbitrary.

This is an inverse, mediator-sensitive mass correction. It is not a disguised `F(A,N)` function, and it does not use a product-form conditional distribution or a protected-token lifetime assumption.
