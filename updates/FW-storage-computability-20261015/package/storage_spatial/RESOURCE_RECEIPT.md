# Explicit resource receipt: U=(cos y,sin y), B=0, target width 0.01

## Result

A fully finite parameter selection is certified by 33 exact rational/integer checks in `verify_resource_bounds.py`, with machine-readable output `resource_receipt.json`:

- Original horizon N=10^22.
- Padding delta=10^-6.
- Anisotropic heat time s=10^-40, with the certified d1=4897/5000,d2=5103/5000.
- Common rectangular Fourier cutoff K=10^44 in both coordinates.
- Rational real/imaginary coefficient radius Cbar=10^21.
- Global coefficient-grid spacing rho=10^-640.
- Real parameter dimension d=2(2K+1)^2, approximately 8×10^88.
- Each coordinate has fewer than 10^662 grid points.
- The logarithm to base 10 of the total grid cardinality is bounded by 662d, approximately 5.296×10^91, and is strictly less than 10^93.

This is a rigorous sufficient construction, not a lower bound on every possible algorithm's cost. Its explicit exhaustive grid is overwhelmingly impractical. No grid was enumerated, no objective was evaluated, and no approximate storage value is claimed. Running the parameter-bound checker establishes only the displayed error and resource bounds.

## Endpoint, horizon, and gradient budgets

For E(x,y)=xU(y), |DE|^2=1+x^2, so ||DE||_4^4=1+2/3+1/5=28/15 and M=120(28/15)=224. The finite-horizon theorem has E*=2M/gamma=1,120,000,000 and error <=6960 E* (N-1)^(-3/4). The exact inequality

(6960 E*)^4 < (1/1000)^4 (N-1)^3

certifies horizon error below 0.001. Near-minimizers with error below one satisfy R^4=(2M+1)/gamma=1,122,500,000<184^4.

For the fixed polynomial return r=1-h, h=35t^4-84t^5+70t^6-20t^7, we have 0<=h<=1 and |h'|<=35/16<3. Therefore |D(rU)|<=4 and its fourth-power energy is <=256. It follows that Rtot<200. On the reference interior ||DW||_4<=4N^(1/4), so Lw<=188N. Also P=N+4delta+1<2×10^22 and L=N+2delta<10^24, implying L^(1/4)<10^6.

The polynomial coefficient sums give |h''|<=5040 and |h'''|<=23520. Since d1,d2<2, reference bounds A0<11000, A1<60000 are valid, with the interior x-rescaling only improving them. Exterior K_ref=||DW||_infinity<=4.

## Heat leakage without numerical exponentials

Write x0=10^27. The principal off-diagonal exponent delta^2/(4d1s) exceeds x0. For every integer k>=1, (k-1/2)^2>=k/4, so the kth image exponent is at least P^2 k/(16d1s)>=x0+k. Using e>2, the entire x image bracket is bounded by 3 exp(-x0).

The elementary bounds 3<pi<4 and d1>0.9,d2>1 give heat prefactors at most s^(-1/2) and 3s^(-1/2). Thus

q <=9s^(-1)exp(-x0) <=216/(s x0^4) <10^-65,

where exp(-x)<=4!/x^4 follows directly from the exponential power series.

Consequently

e0<=11000s+188N^2×10^-65<2×10^-19,
e1<=60000s+188N×10^-65<7×10^-36.

The theorem's exact endpoint repair has h0<8×10^-30. Hence, using B=0,

DIF_L(Rtot,h0)<180(8×10^-30)201^3<10^-19,
Eext<3×180(7×10^-36)5^3<10^-30.

The padding budget is delta Cpad=120×10^-6=0.00012.

## Fourier tails by a rational Gaussian majorant

Set a=10^-84. The bounds P<2×10^22, d1>0.9, 2pi>6 give

s[d1(2pi k/P)^2+d2n^2] >=a(k^2+n^2).

For S0=sum_Z exp(-aj^2), S1=sum_Z |j|exp(-aj^2), elementary Gaussian integral estimates give

S0<=3×10^42,   S1<=4×10^84.

For the weighted estimate, use |j|exp(-aj^2)<=a^(-1/2)exp(-(a/2)j^2), then the same Gaussian integral. Beyond K=10^44 the summands are decreasing, and

Tail0=sum_|j|>K exp(-aj^2)<=exp(-aK^2)/(aK)=10^40 exp(-10000),
Tail1=sum_|j|>K |j|exp(-aj^2)<=exp(-aK^2)/a=10^84 exp(-10000).

The finite exponential-series inequality yields

exp(-10000)<=100!/10000^100<=100^100/10000^100=10^-200.

Also |Vhat|<=200P^(3/4)<Cbar=10^21, verified by raising both sides to the fourth power. Taking the union of the two coordinate tails and using |xi_kn|<=|k|+|n| gives

T0<=Cbar(2 Tail0 S0)<=6×10^-97,
T1<=Cbar·2(Tail1 S0+Tail0 S1)<7×10^-53.

Thus t0<2×10^-46 and the additional action error is below 180(2×10^-46)202^3<10^-36. Total spatial error is less than 0.001.

## Compact global-grid cost

Use the theorem's explicit 2cos/-2sin conjugate-pair basis, with two output coordinates. The coefficient radius is Cbar, without a missing factor of two. The dimension d=2(2K+1)^2 includes harmless constant coordinates whose endpoint-repaired basis is zero.

For every repaired basis, its pointwise gradient is bounded by 10K. Therefore B_j=10^51 bounds its gradient L4 norm, because L^(1/4)<10^6. The deliberately loose aggregate bounds are

d<10^90,   S=sum_j B_j<10^141,
A_box=||D(theta_x U)||_4+Cbar S<10^163.

With rho=10^-640, the exact theorem's grid gap satisfies

gerr<=180 rho S A_box^3<10^-7.

A coordinate grid including both box endpoints has 2Cbar/rho+1<10^662 points. Therefore log10(cardinality)<662d<10^93. This is a direct sufficient enumeration count, not a computational-complexity lower bound.

If the full grid were eventually evaluated with interval width at most 0.001 per objective, the theorem's final interval would have width at most horizon_error+spatial_error+grid_error+0.001<0.01. Evaluation of a computable quartic integral to that precision is a finite operation at every grid point. It has not been performed here.

## Evidence and limits

`verify_resource_bounds.py` is newly written standard-library Fraction/integer arithmetic. It checks the constants, exponent majorants, horizon fourth-power inequality, coefficient radius, all final error comparisons, dimension, and cardinality bound. The analytic Gaussian inequalities are proved above; the checker checks their rational numerical instantiation, not their formal analytic proof.

These choices intentionally leave wide slack and are not optimized. They demonstrate that the spatial closure is effective rather than merely a density argument. They also make clear that this particular certified exhaustive construction is not a usable numerical storage solver at accuracy 0.01.


Integration evidence status: `source_derived_unreviewed`. Audit verdicts and primary-source reading statements above are attributed to the supplied research, not new external review. This intake replays only its three own exact verification scripts. The conclusion applies to the particular certified Heat18 quartic G, not the full quartic cone, PR97’s newly exposed ROC ray, or general Morrey questions.
