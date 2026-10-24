# Independent audit of the distributed-rod sign alternation

I checked the exact secular expression and the proposed uniform bounds for
`N>=12` a multiple of 12, `2N/3<=n<=3N/4`, `0<mu<=0.01`, and
`delta in [b_n/x_n,2b_n/x_n]`. The pole exclusion and sign alternation both
follow from the displayed estimates; I found no algebraic gap in the
`h_l=min(l,|l-n|)` derivative bound or the `<64 mu/N^2` center-rest bound.
This is an algebra audit of the scalar rod equation, not a statement about
rod routing or a realized material.

## The nth rod and its sign

Set `epsilon=n delta`, so `nx=pi+epsilon` and `nq_j=j pi`. Directly from
the exact rod term,

`T_n=2 b_n (pi+epsilon) cot(epsilon/2)` for even `j`,
`T_n=-2 b_n (pi+epsilon) tan(epsilon/2)` for odd `j`.

Writing `r=delta/(b_n/x_n) in [1,2]` gives
`epsilon=r b_n n^2/pi`. Thus the even term is positive and, since
`cot(epsilon/2)>=3/(2 epsilon)` for `epsilon<1`,

`T_n >= 3 b_n n x/epsilon >= 3 pi x/(2 n) >= 1.5 x_n^2`.

The odd term is nonpositive. Its magnitude is much smaller than `x_n^2`:
exactly

`|T_n(odd)|/x_n^2 = [2 epsilon (pi+epsilon)/(r pi)] tan(epsilon/2)`.

The stated parameter range gives `epsilon<0.002`, so this ratio is
`O(epsilon^2)` and is not needed for the odd sign. Also
`x^2<1.002 x_n^2`.

## Pole check

The interval is short: `delta<=3 mu/N^2`. For `l!=n`, let
`h_l=min(l,|l-n|)`. At the center,

`|sin(l x_n)|=|sin(pi l/n)|>=2 h_l/n`.

Indeed, for `l<n` the distance to the nearest multiple of `pi` is at least
`pi min(l,n-l)/n`; for `l>n`, `l-n<=N-1-n<n/2`, so the nearest pole is at
`pi` and its distance is `pi(l-n)/n`. Since `n<=3N/4`, `h_l/n>=4/(3N)`;
the sine Lipschitz bound then gives, throughout `0<=delta<=3mu/N^2`,

`|sin(l(x_n+delta))| >= (2-9mu/4)h_l/n >= h_l/n > 0`.

So no `l!=n` rod pole occurs on the selected segment. For `l=n`, `x_n` is
the segment's left-end pole, while every selected `delta>0` has
`nx=pi+epsilon` with `0<epsilon<1`, hence is off-pole. Other rod poles may
lie below `x_n`; none is crossed inside the interval. The strict upper
bound `l x<3pi/2` used in the derivative estimate follows from
`l<=N-1`, `n>=2N/3`, and `3mu/N<3pi/(2N)`.

For the stated interval this shortness follows directly from
`delta<=2b_n n/pi` and `n(N-n)<=2N^2/9`:
`delta<=16mu/[3pi(N^2-1)]<3mu/N^2`. Also
`delta/x_n<=9mu/(4pi N)<0.0006`, so `x^2<1.002 x_n^2`.

## Remainder at the pole and its off-center change

Write `C=12mu/[N^2(N^2-1)]`, so `b_l=C(N-l)`. At `x_n`, pair
`l=n-e` and `n+e` for `1<=e<=N-1-n`. Their cosine numerators agree at each
`q_j`, their sine denominators have opposite signs, and

`(n-e)(N-n+e)-(n+e)(N-n-e)=2e(2n-N)`.

Using `|cos A-cos B|<=2` and `sin(pi e/n)>=2e/n`, each pair contributes
at most `4 pi C(2n-N)` in absolute value. Since
`(2n-N)(N-n)<=N^2/8`, all pairs contribute at most
`(pi/2) C N^2`.

The unpaired indices are `1<=l<=2n-N`, where `l/n<=2/3`. Concavity of sine
gives `sin(pi l/n)>=3 sqrt(3) l/(4n)`, and
`sum_(l=1)^(2n-N)(N-l)<=3N^2/8`. Their total is at most
`(2pi/sqrt(3)) C N^2`. Therefore, uniformly in `j`,

`|R_n(x_n,q_j)| <= (pi/2+2pi/sqrt(3)) C N^2 <64 mu/N^2`.

At `N=12` the last coefficient is below `62.9`; it decreases with `N`, so
the `<64` constant is uniform.

Away from the center, differentiation at fixed `q` gives

`|T_l'(x,q)| <=4 b_l l [1/|sin(lx)|+l x/sin^2(lx)]`.

Each positive `h_l` occurs at most three times, hence
`sum 1/h_l<=3N` and `sum 1/h_l^2<=pi^2/2`. Substituting the pole bound,
`lx<3pi/2`, and `n<=3N/4` yields

`sum_(l!=n)|T_l'| <= [108+(81/4)pi^3] mu N^2/(N^2-1) <768 mu`.

Also `delta<=3mu/N^2`, so

`|R_n(x,q_j)| < (64mu+2304mu^2)/N^2 <0.06 x_n^2`.

The last inequality follows from `mu<=0.01` and
`x_n^2>=16pi^2/(9N^2)`. Combining with the nth term,

`D(x,q_j)>0` for even `j`, and `D(x,q_j)<0` for odd `j`,

with margins at least `0.438 x_n^2` and `0.94 x_n^2`, respectively. Thus
the sign alternation is uniform over the whole parameter interval, not just
at its endpoints.

## Finite high-precision check

As a numerical cross-check, I evaluated the exact sums with 70-digit
`mpmath` at small `N=12`, `n=8,9`, `mu=0.01`, both interval endpoints,
and every `j=0,...,n`; all signs matched parity. At large `N=1200`,
`n=800,850,900`, `mu=0.01`, endpoint offsets `r=1,2`, a vectorized scan
over every `j` also had zero parity mismatches. Its smallest parity-adjusted
margin was `0.9892789 x_n^2` (`n=900,r=2,j=0`). Independent 70-digit
checks there gave, for `r=2`, `D/x_n^2` equal to `0.98927893899`,
`-1.00000575628`, `0.99961244111`, `-1.00046609506`, and `0.99957262543`
at `j=0,1,2,899,900`. These finite checks support but do not replace the
uniform bounds above.
