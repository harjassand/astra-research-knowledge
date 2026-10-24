# Independent audit: elastic-interface E6/E7 certificate

## Verdict

E6 and E7 are valid sufficient bounds for the declared unstressed linear model, under the stated hypotheses `K_w >= 0`, `R_v >= 0`, positive material/conduction parameters, and `L(q) <= L_max`. The piecewise argument covers every `q >= 0`: the low band uses E6/E7 and the high band is already stable from the chosen `q_bar`. I found no interval gap. The exact rational certificate is separated correctly from the finite floating Airy and ionic-transfer diagnostics.

This conclusion is for E1--E4 and their boundary conditions; it does not validate the assumed material-property conjunction, residual stress, contact, or the nonlinear/finite-amplitude skin problem.

## E6 derivation

Write `k_+=k_plus`, `k_-=k_minus`, `a=(k_++k_-)/2`, and `c=(k_+-k_-)/2`. The reduced bottom-face stiffness after top-face equilibration is

`k_eff(K_w)=a-c^2/(a+K_w)`, and the top/bottom displacement ratio is `m=-c/(a+K_w)`. Therefore

`k_eff(0)=2 k_+ k_-/(k_++k_-)=2k_+/(1+k_+/k_-)`,

and, at fixed `q`, `d k_eff/dK_w=c^2/(a+K_w)^2=m^2`.

For `0<q<=q_bar`, the given partial-fraction identity implies `k_- >= k_-0`; monotonicity of `k_+` gives `k_+<=k_+bar`. Hence

`m(q,K_w)=(k_--k_+)/(k_-+k_++2K_w) >= (k_-0-k_+bar)/(k_-0+k_+bar+2K_w)=m_min`.

For the integral from foundation zero to `K_w`, the same lower bound applies at every intermediate foundation value `s<=K_w`, since its denominator is no larger. Thus the foundation contribution is at least `K_w m_min^2`.

Also, with `l=qb/2`,

`k_+ = l/(b c_e) integral_0^l 2t tanh(t) sech^2(t) dt`.

On `0<=t<=l`, `tanh(t)>=t tanh(l)/l` and `sech^2(t)>=sech^2(l)`. This yields

`2 k_+ >= B q^4 [tanh(l)/l] sech^2(l)`.

Both bracket factors decrease with `l`; for `l<=l_bar`, replace them by their values at `l_bar`. Finally `k_+/k_-<=k_+bar/k_-0`, so the harmonic-mean expression for `k_eff(0)` gives `k_eff(0)>=c_B B q^4`. Adding the foundation contribution proves E6. The `q=0` case follows by the continuous limit; its `Bq^4` term vanishes.

## E7 and interval coverage

Set `y=q^2`. Since `p S` is nonnegative, `L(q)<=L_max` gives `C+L(q)pS<=H(y)`. The power series for `cosh(b sqrt(rho y))` and `sqrt(y)sinh(b sqrt(rho y))` have nonnegative coefficients, so `H` is convex. A convex function lies below the chord joining its endpoint values, hence on `[0,y_bar]`,

`H(y)<=1+K y`, where `K=(H(y_bar)-1)/y_bar`.

On the part of this interval where `chi<G`, E6 implies

`1-chi/G <= A(y)=w0-a0 y-c0 y^2`.

Here `A(y)>0` necessarily, since the left side is positive. Consequently the positive product can be bounded as

`N/G <= A(y)(1+K y)-m_min(1+k_n R_v)`.

The first term expands to the cubic shown in E7. Therefore its maximum being strictly less than `m_min(1+k_n R_v)` proves `N<0` throughout the low band wherever `chi<G`; where `chi>=G`, the original numerator is immediately negative because `C+LpS>0`, `m>=0`, and `R_v>=0`. The denominator in E4 is positive for `q>0` (`r C+S/p+L(C+r pS)>0`), so this is the needed sign of the transfer. At high q, `k_eff>=k_+` for `K_w>=0`, and monotone `Gamma q^2+nu_m k_+(q)` is already above `G` at `q_bar`; thus all `q>=q_bar` have `N<0`. The uniform galvanostatic mode is separately removed as the note states.

## Exact rational implementation audit

`hyperbolic_bounds` sums positive Taylor series for `cosh(sqrt(x2))` and `sinh(sqrt(x2))/sqrt(x2)`. After order 14, each next-term ratio is the recorded `x2/denominator`; later ratios decrease, so `last_term*r/(1-r)` is a rigorous tail upper bound whenever `r<1`. The `kp_bounds` lower and upper expressions propagate these positive bounds with the correct denominator directions. The code's `c_B=sl/(ell*cu^3)/(1+kplus_upper/kminus0)` is precisely a rational lower bound for `[tanh(ell)/ell] sech^2(ell)/(1+kplus_upper/kminus0)`.

The endpoint upper `hu` uses `sinh(x)=x[sinh(x)/x]` and `p=kn sqrt(rho) sqrt(y)`, so its `L_max*kn*rho*b*y*sh` term has the right factors. The 128-bin cubic Bernstein calculation is an exact rational upper bound: on each bin the cubic is a convex combination of its four Bernstein coefficients, so the largest coefficient bounds the entire bin. Its power-to-Bernstein conversion is correct.

Re-evaluating the rational routine without writing the results file reproduces the reported comparisons: `chi_lower(q_bar)=243.0632229 > G=192.3076923 V/m`; `m_min=0.99821620`; `c_B=0.93453856`; and the E7 left/right values are `5.15079560 > 1.30475773`. These are strict margins for the exact declared parameter fractions, not measured-parameter uncertainty bounds.

The 24 Airy boundary solves and floating ionic boundary solves are useful independent implementation/sign diagnostics only at their sampled inputs. They do not prove all-q stability. The all-q conclusion instead follows from the analytic E6/E7 inequalities and exact rational enclosures above. The separate `q=10000/m` instability witness likewise proves one rational point for its comparator, not a sampled-band conclusion.
