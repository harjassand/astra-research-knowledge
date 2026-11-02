# Actual normalization of all hidden inventories above a raw anchor threshold

Author theorem. No global recurrence conclusion is asserted. This is an actual
stopped operation, including every competing channel, for any finite number
of ordered C3 ports and any pair-transfer core graph.

Port i has reactions 0 -> A_i B_i -> 2A_i+B_i+C_i ->
3A_i+2B_i+2C_i -> 0, with arbitrary positive rates alpha_i0,...,alpha_i3.
Core edges transfer two B,C units from i to j, catalyzed by A_i A_j,
with arbitrary fixed positive rates. Every actual core jump is retained.
The six-species diagnostic is the two-port case, with core rates2 and1.

## Raw coordinates and acquired constants

For physical nonnegative counts set

    r_i=B_i-C_i, t_i=min(B_i,C_i),
    R+=sum max(r_i,0), R-=sum max(-r_i,0),
    O=sum(t_i mod2), J=sum floor(t_i/2),
    V=3R+ +2O+J,       Psi=V+a R-.                     (H1)

Every core jump preserves r_i, O and J, hence preserves Psi EXACTLY. Neither
the number nor the rate of those core jumps is suppressed.

Put B0=sum alpha_i0, b0=min alpha_i0, and

    f0=min_i{alpha_i1,2alpha_i2,8alpha_i3},
    D=max_i{alpha_i0/alpha_i1,
             2(alpha_i0+alpha_i1)/alpha_i2,
             3(alpha_i0+alpha_i1+alpha_i2)/alpha_i3}.

Choose an integer a>=4+8B0/b0 and an integer

    L>=max{3,2aD,12B0/f0}.                              (H2)

These are explicit finite arithmetic on the raw rate list. The transfer
rates do not enter the threshold because the core preserves (H1).

## Frontier classification is a proof device, not a controlled trajectory

At an anchor A_i>=L, classify one source as follows:

* t_i>=2: source3 (terminal), fast;
* t_i=1: source2, fast;
* t_i=0,r_i>0: source1, fast;
* t_i=0,r_i<0: source0, slow activation;
* t_i=r_i=0: source0, empty input.

Let F,S,E be their total fast, slow and empty-input hazards; let H be the
total hazard of all the OTHER raw block channels. Thus the complete genuine
noncore hazard is q_nc=F+S+E+H. No reaction has been deleted.

The exact frontier increments are respectively

    delta Psi=-1,-1,-1,2-a,3.                           (H3)

Every other raw block increment is at most a, and its absolute value is at
most a+1. For example source1 at r<=0 increases R- by1, while source0 at
r<0 decreases it. Thus signed pair residuals are handled by the same physical
quantity, without projecting to a positive packet profile.

Exact falling-factorial divisions give

    H<=D/L F.                                          (H4)

For t=1, divide source0 and source1 by source2; for t>=2 divide sources0,1,2
by source3. For t=0,r>0 divide source0 by source1. When t=0,r<0 or the port
is empty, every other source is disabled by an exact factorial zero. These
are all cases. In particular (H4) is uniform in ALL hidden populations.

Consequently the ACTUAL generator satisfies

    L_actual Psi <= -(1-aD/L)F -(a-2)S +3E
                 <= -F/2 -(a-2)S +3E.                 (H5)

If V>0, at least one fast source is enabled and F>=f0 L>=12B0. Since E<=B0,
the right side is at most -F/4-(a-2)S. If V=0 but R_minus>0, all minority counts
are zero and at least one slow activation is enabled, so S>=b0; the choice
of a gives 3E<=3B0<=(a-2)S/2. Combining these cases and (H4) yields

    L_actual Psi <= -q_nc/8 <= -B0/8                   (H6)

whenever hidden inventory is nonempty and every anchor is at least L.

For completeness, in the first case q_nc<2F+S because E<=F/12 and
H<=F/(2a). In the second case F=H=0 and
q_nc<=S+B0<=((a+4)/6)S. These imply (H6) for a>=4.

## Common physical return and actual output contract

Start at any state with all anchors>=L and some hidden inventory. Stop at

    sigma=first{all B_i=C_i=0 OR min_i A_i<L}.           (H7)

The terminal reaction is the only possible downward anchor crossing. No
anchor is frozen, and the endpoint is its actual landing, including its
remaining inventories. With the SAME globally defined nonnegative Psi,

    E[Psi(X_sigma)+(1/8) integral_0^sigma q_nc(X_t)dt]
        <=Psi(x),
    E sigma <=8Psi(x)/B0,
    E J_nc(sigma)<=8Psi(x).                             (H8)

Here J_nc counts ALL genuine block reactions, including every unwanted
source and every empty input. An expected total CORE activity bound is not
claimed. Localization and (H6) prove (H8); no stationary fiber, spectral gap,
neighboring receiving law or infinite-rate limit is assumed.

There is no explosion before sigma. The finite expected number of noncore
jumps implies finitely many such jumps a.s. Between consecutive noncore
jumps, all anchors, pair differences and total hidden inventory are fixed,
so the core visits a finite fiber with finite rates. Thus infinitely many
core jumps cannot accumulate in one such interval. This also justifies
removing the localization and retains the genuine physical clock.

## Uniform tails and axis busy periods

All noncore increments of Psi have absolute value <=b=a+1, and all core
increments are zero. Choose

    0<theta<=min{1/b,1/(8 e b^2)}.

Taylor's inequality and (H6) give, before (H7),

    L exp(theta Psi) <= -(theta/16)q_nc exp(theta Psi).

Therefore

    E exp(theta Psi(X_sigma)+(theta B0/16)sigma)
         <=exp(theta Psi(x)).                           (H9)

At successive actual noncore events the conditional multiplicative decrease
is at most 1-theta/16; the intervening core path does not change Psi. Hence
with gamma=theta/32,

    E exp(theta Psi(X_sigma)+gamma J_nc(sigma))
         <=exp(theta Psi(x)).                           (H10)

This is a LOCAL high-anchor drainage tail, not an exponential recurrence
claim for the full network.

Starting on an arbitrary joint anchor axis with every A_i>=L, include the
first genuine input and then use (H7). The first holding time has mean1/B0;
the input leaves Psi=3 and all anchors still>=L. Thus the complete actual
axis busy period, stopped at its next axis return OR actual low-anchor exit,
has

    E sigma_busy<=25/B0,  E J_nc,busy<=25,               (H11)

and uniform positive exponential moments of its noncore count and physical
duration. Every competing path is included. Since anchors change by at most3
per noncore event, a low-anchor exit from an axis whose minimum anchor is
A_min requires at least (A_min-L)/3 noncore events. Its probability and all
fixed noncore-count-weighted tails are exponentially small in A_min-L.

## Scope and the genuine remaining operation

This proves an actual population-controlled normalization for arbitrary
unbounded hidden inventories and pair differences in the high-anchor region,
and an acquired, uniformly integrable joint-axis return kernel. It is much
stronger than a coordinate function merely defined on those states.

Psi is not proper in the anchors. (H8) receives every boundary output in the
same Psi, but a GLOBAL proper receiving quantity still has to value those
anchors and connect their low-anchor landings. The axis kernel's inward
quadratic drift and the low-anchor/large-difference feedback are not supplied
by (H8). Those are the next proof obligations. No unrestricted weak
reversibility result, full six-species recurrence theorem, numerical advantage
or historical-priority claim follows yet.
