# Exact weighted-stage ledger for the clearance CLT

This is a derivation and exact arithmetic verification of the envelopes used in
`ACTUAL_CLEARANCE_CLT.md`, not an independent mathematical review.

Write `m=Tr`, `N=T^5`, `w=sqrt(Nm)=T^3 sqrt(r)`. On active stages before the
first omitted mark, the common stopped domain has

- `T>=1`, `1<=r<=sqrt(T)` (in the proof actually `r>=10^40`);
- `m/2<=L<=2m`, `w/2<=E<=2w`, `A<=m/16<=m`, `Z=0`, `B<=2N`;
- `|n-N|<=10T` from the original count stop and no earlier A death;
- `H=int A<=10^4 w/N`, `J=int A²<=mH`, and `d=duration<=16w/m²`.

Using upper envelopes as formal positive expressions, set

    U = d+H+(5/2)mH+2wH,
    W = mH+2wH,
    V_E = mH+4wH+8m²d,
    V_L = d+H+4mH+2wH,
    Q_h = 4w²[d+H+6mH+4m²d+2NH]
           +16w²mH+40w³H+128w²m²d,
    R_h = 2wd+24mwH+9m²H+8m²d
           +2wH[10T+2w+8m+2].

These bound the actual integrals of `q_LL, sum lambda|uv|, q_EE,
sum lambda|u|, q_hh, H_h`, respectively. Each expression follows directly
from the exact twelve-channel source formulas:

* `Q<=2AL<=4mA` because the pre-stop imbalance is exactly zero;
* `h<=2wA`, `A(A-1)<=mA`, `A(A-1)²<=m²A`;
* `C+D<=4m`, `CD<=4m²`, `AB<=2NA`;
* `A+E+1<=4w`, `|E-1|<=3w`, and `h+=(A+1)(E+1)<=3mw`.

The Q_h expression keeps all fast AB/CD terms. Its first bracket includes the
full `int AB<=2NH` contribution. No event rate is replaced by its equilibrium.

For all actual connecting jump segments, `l>=r/3` and
`sqrt(r)/3<=e<=3sqrt(r)`, hence `l>=e²/32`. The exact received derivative
constants, after replacing segment e by its lower bound, are

| derivative | ceiling coefficient, multiplying its r power |
|---|---:|
| `b_l`, power `r^-5/2` | `7962624/5` |
| `b_e`, power `r^-2` | `41472` |
| `b_ll`, power `r^-7/2` | `6879707136/7` |
| `b_le`, power `r^-3` | `1177743753216/7` |
| `b_ee`, power `r^-5/2` | `1007952445734912/35` |

Thus all five may be weakened to a common `D=10^14`. The geometry includes the
terminal omitted mark and other first-exit jumps; all increments have
`|Delta L|<=1`, `|Delta E|<=1`. Only m,w>=100 is needed for the padding.

## Residual entries

The five classes from the exact corrector residual are bounded by

    R1 = D r^-5/2 (1+4m)H/T,
    R2 = D r^-2 [mH+4wH+8mH]/T³,
    R3 = D r^-5/2 R_h/(NT),
    Taylor = D[r^-7/2 U/(2T²)+r^-3 W/T^4+r^-5/2 V_E/(2T^6)],
    Product = D[r^-7/2 (3mw)V_L/(NT²)
                  +r^-3 (3mw)V_E/(NT^4)].

Term by term, `R1+R2+R3+Product` is at most

    131059200000000000000 * T^-2 r^-1 < 10^23 T^-2 r^-1.

Taylor is at most `10^23 T^-1 r^-5/2`. This gives the first (21) bound.
The Product line uses post-jump h' through h+, so the exact product-jump
covariation is retained.

## Bracket and jumps

Use the source's exact-envelope coefficients

    a = D r^-5/2/T + (3mw)D r^-7/2/(NT²),
    b = D r^-2/T³ + (3mw)D r^-3/(NT^4),
    c = D r^-5/2/(NT).

Its full bracket is at most

    2[a²U+2abW+b²V_E]+2c²Q_h
      <= 71293440000000000000000000000000000 /(T r^4)
      < 10^40/(T r^4).

The jump bound `a+b+4cw` is at most `1200000000000000/(T r^(5/2))`,
less than `10^16/(T r^(5/2))`. The terminal corrector `2mw D r^-5/2/(NT)`
is at most `2*10^14 T^-2r^-1`, also below its displayed `10^16` ceiling.

## Universal verification rule, not finite samples

`check_tail_envelopes.py` uses only exact Fractions. It expands every positive
expression into monomials `c T^alpha r^beta`. To compare with a chosen target
`T^a r^b`, it checks

    (alpha-a)+max(beta-b,0)/2 <=0.

This is a sufficient universal inequality because `T>=1` and
`1<=r<=sqrt(T)`. It then adds the exact positive coefficients. No numerical
parameter samples, stochastic simulations, empirical fits, or floating-point
power comparisons are used. Ninety-one exact assertions pass, including the
common derivative ceiling, rate envelopes, all residual and bracket terms,
whole-segment padding, and increasing omitted-hazard geometric sum.

The omitted hazard per stage is at most `110000 T^-1 r^(3/2)`; the increasing
geometric sum is less than twice its last term and hence less than
`400000 T^-1/4`. The actual remaining-clock bound at the cutoff uses
`1/(6(1/32)^2)=512/3<200`.

These identities verify the numerical/power ledger. They do not independently
verify the stopping construction, accepted source receipt, CLT, or boundary
continuation; those are ordinary mathematical arguments in the main proof.
