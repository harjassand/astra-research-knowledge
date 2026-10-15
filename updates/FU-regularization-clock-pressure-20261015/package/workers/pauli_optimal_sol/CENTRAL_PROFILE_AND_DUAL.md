# Central profile reduction and unclosed optimality gate

This continuation follows the independent freeze. The root subsequently reported that other new workers independently obtained the same plateau construction. This is a coordination fact, not external verification or proof of optimality.

Use normalized g≥0 with `2∫s g=1`. Define the nonnegative upper eigenvalue slack

`B(r)=2r g(r+1)−∫[|r−1|,r+1]g(s)ds`, `r>0`.

For 0<r<1 also define the nonnegative lower slack

`A(r)=∫[1−r,1+r]g(s)ds−2r g(1−r)`.

An exact moment identity is

`v=23/9−(8/9)∫[0,1]s(1−s²)g(s)ds`

`   +(1/3)∫[0,∞)(r²+4r+4/3)B(r)dr`.

The identity follows by computing Ij=∫r^jB(r)dr for j=0,1,2 and eliminating J0,J2. It holds when the displayed integrals are finite; finite second scalar noise moment ensures J3 finite, which controls these nonnegative slack integrals.

Thus the gap below 23/9 is produced by the scalar profile inside the unit radius and penalized by every failure to be a pure positive-spin POVM. The plateau construction makes B identically zero and A identically zero on (0,1).

Within the pure-spin subclass B=0, put

`f(u)=g(1−u)`, `H(u)=g(1+u)`, `0<u<1`.

Differentiating `2u H(u)=∫[1−u,1+u]g` gives

`2u H'(u)+H(u)=f(u)`.

Hence

`H(u)=C/sqrt(u)+(1/(2sqrt(u)))∫[0,u] f(v)/sqrt(v)dv`.

The remaining positivity A≥0 is precisely f≤H. Equivalently,

`H'≤0`, `H+2uH'≥0`;

that is, H is nonincreasing and sqrt(u)H is nondecreasing. The plateau has constant H and C=0. The singular homogeneous branch C/sqrt(u) is the shifted generalized Dickman branch. This identifies a useful cone of central profiles, but does not by itself prove the plateau minimizes variance.

An exact dual certificate for global optimality could use nonnegative multipliers λ(r), r>0, and μ(r), 0<r<1, such that

`s³−3v_*s = 2(s−1)λ(s−1)1_{s≥1}−∫[|s−1|,s+1]λ(r)dr`

` +1_{0<s<2}∫[|s−1|,1]μ(r)dr−2(1−s)μ(1−s)1_{s<1}`.

Integrating against g would then prove `v≥v_*`, provided all integrability and endpoint terms are justified. For s≥2 only the first line remains, an advanced integral equation. Polynomial λ gives the old 23/9 constant; a nonpolynomial correction is essential to reach the plateau value. Numerical LP duals are not a substitute for positive analytic multipliers or endpoint control.
