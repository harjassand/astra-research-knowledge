# Extra-mode onset with a finite, almost minimal total-stiffness budget

This is a connected resource consequence of PROOF.md. The sharp global optimum under *both* a compliance cap and a spring-sum cap remains open. Here the construction proves a strict feasible improvement with both resources charged and identifies the exact feasibility boundary. Full intervals and positive parts are in the final section of CERTIFICATE.md.

## 1. Exact feasibility threshold for any positive graph

Let kappa be the sum of all internal spring constants and kappa_inc the sum incident to the backbone. In physical displacement coordinates the relative internal-CM readout has force vector

f_b=-1, f_j=m_j/(M-m), sum f_j=0.

The static response Lx=f has CM compliance C=f^T L^+ f and spring energy

C=sum_edges k_e(x_u-x_v)^2.

At the backbone, force balance and Cauchy-Schwarz give

1=[sum_inc k_e(x_b-x_j)]²
 <=kappa_inc sum_inc k_e(x_b-x_j)²
 <=kappa_inc C<=kappa C.

Consequently any design with C<=Cmax requires kappa>=1/Cmax. If the common total budget is exactly kappa_max=1/Cmax, every inequality is equality. No positive nonincident spring can occur, so the graph is a star (parallel edges may be combined). All side displacements are equal in the static response and k_j is proportional to m_j. Its visible dynamics is exactly one pendant of side mass M-m and spring 1/Cmax; the other relative modes are dark. Thus extra modes cannot help at this exact minimum total-stiffness budget. A budget below it is infeasible.

This is a physical static-force inequality over arbitrary internal topology. It does not rely on the special three-band parametrization.

## 2. A branch-splitting construction immediately above the minimum

For the normalized resource point m=1,M=2,K=1,theta=1/2, choose Cmax=C=1/20. The exact minimum total internal stiffness is 20; the optimized legal one-pendant is k=20. Let p0<r0<s0 be its three positive band edges, with r0²=t0=40, and fit its three-moment dual R0=g+lambda/w+a w+nu/w³. This pendant has a<0. The exact interval certificate proves

R0(8) is between -0.000292058515344058011632 and
                    -0.000292058515344058011631.

Fix H=64 and let delta>0 be small. Set

A_l=4-delta,
B_l=2H/(H+delta),
t(delta)=(A_l-B_l)/{B_l[(1+C)/2-1/B_l+delta/(H(H+delta))]}.

Use the two low bands of (A_l,B_l,sqrt(t(delta))) and append the band [sqrt(H),sqrt(H+delta)]. For every sufficiently small positive delta these bands strictly interlace and preserve original backbone mass 1, total mass 2 and compliance C=1/20 exactly. Positive-star synthesis therefore gives two actual side masses and two finite positive springs.

At delta=0 the high band has zero width and the low spectrum is precisely the k=20 pendant. The exact moment derivatives and the three zero endpoint values of R0 imply

dJ/ddelta at zero = R0(sqrt(H))/(2sqrt(H)).

The low endpoint contributions vanish in this expression; the complete logarithmic, trace and compliance moment derivatives cancel. At H=64 this derivative is strictly negative, enclosed in

[-0.000018253657209003625727,-0.000018253657209003625726].

The total star spring sum follows from the rational Stieltjes response or frozen F's high-frequency coefficient. Its exact first derivative is

dkappa/ddelta at zero
 =(H-r0²)(H-p0²)(H-s0²)/(4H²)
 =255/128>0.

In particular kappa(delta) tends to 20 as delta decreases to zero. Therefore, for **every** total internal-spring budget kappa_max>20, there is a finite positive two-branch star with C_CM=1/20, kappa<kappa_max and J<J_optimized_pendant. At kappa_max=20, Section 1 proves that improvement is impossible. This proves the exact onset of extra-mode advantage at this compliance point; it does not give the maximizing gain at each larger spring budget.

The mechanism is a genuine admissible spectral variation. The negative high-frequency dual region supplies the first-order gain, and inverse synthesis pays its mass and spring costs. Failure of the pendant dual alone would not have established this conclusion.

## 3. A completely explicit finite example with kappa<20.02

Choose delta=1/100, H=64. Then

A_l=399/100,
B_l=12800/6401,
t=8154867599/204211900,
kappa=40883205203/2042119000
      =20.019991588639055804289563....

The three bands are

[0,1.378494003067400653561993...]
union [6.319284878149041582345053...,6.482523864569289845674772...]
union [8,8.000624975587844662388667...].

The Stieltjes response is q(z)=(z²+c z+d)/[z(z+t)(z+64)], with

c=171361086787/2042119000,
d=65238940792/51052975.

The explicit star formulas in PROOF.md section 4.2, with H=64, give certified positive parts

side mass 1 = 0.999337726607370960907862...,
side mass 2 = 0.000662273392629039092137...,
side spring 1 = 19.977657435641150709046539...,
side spring 2 = 0.042334152997905095243024....

Backbone mass is exactly 1, total mass exactly 2, intercell spring 1 and CM compliance exactly 1/20. The small second mass is a reported output cost; connector geometry/mass and robustness are not supplied.

With all three bands included, exact enclosures prove

1.142045204871334444544427 < J < 1.142045204871334444544428,
0.000000182670737317172171 < J_pendant-J
                               <0.000000182670737317172172.

Both designs receive C_CM<=1/20 and total internal stiffness <=20.02. The strongest pendant still chooses k=20, since its full Bose objective increases above the already known unconstrained optimum k*=2.729088.... The gain is extremely small (about 1.6e-7 in relative conductance), so it is a mathematical topology advantage at matched budgets, not evidence of practical thermal insulation.

## 4. A finite spring cap rules out approaching the escape infimum

The sharp nonattained infimum at C=1/20 has trace Ahat<4. Any sequence approaching it has I_n=integral Rhat(chi_n-chihat) tending to zero, since all other terms in the sharp dual difference are nonnegative. Thus chi_n converges to chihat in L1 on compact frequency intervals away from its three zero endpoints. Bounded indicators make arbitrarily small neighborhoods of those endpoints negligible for the trace moment.

If internal spring sum were uniformly bounded, frozen F's exact incident-stiffness identity would bound

E_n=sum(beta²-alpha²)=integral 4w³ chi_n(w)dw.

The trace tails are then uniformly bounded by

integral_0^epsilon 2w chi_n dw<=epsilon²,
integral_R^infinity 2w chi_n dw<=E_n/(2R²).

Compact convergence plus these two tails would force T(chi_n) to converge to T(chihat)=Ahat<4, contradicting T(chi_n)=4. Therefore every fixed finite spring-sum cap has a strictly positive gap above that escape infimum. A high-order network cannot evade this conclusion by spreading the escaping trace over many bands.

This does not yet quantify the optimum gap as a function of kappa_max or prove the minimal active order of its exact optimizer. That jointly charged frontier is the remaining mathematical obligation most directly relevant to finite material resources.
