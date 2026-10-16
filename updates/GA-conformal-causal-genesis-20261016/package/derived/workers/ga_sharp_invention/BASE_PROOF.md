# Base result frozen independently of quantitative margin

At unchanged `r=1`, for every periodic `F,H in W^{1,4}(T)`, every periodic
`g in W^{1,4}(T^2)`, every real `s`, and `phi=(F(x)+H(y),g(x,y))`,

\[
\langle J(sI+D\phi)-J(sI)\rangle\ge0.
\]

This qualitative proof needs only the unshifted exact Gram certificate.
With `a=F'`, `b=H'`, `c=g_x`, `d=g_y`, choose

\[
\sigma=(-3s^2b+b^3/2,\ 3s^3+7s^2a+5sa^2+a^3/2).
\]

The first entry depends only on `y` and the second only on `x`. Thus
`div sigma=0`, `<sigma dot Dg>=0`, and `<a>=0`. The exact polynomial identity is

\[
J(sI+D\phi)-2s^4=5s^3a+\sigma\cdot Dg+G,
\]

where the independently frozen `BASE_CERTIFICATE.json` gives `G=z^T Q z`.
Its two blocks are exactly the matrices displayed in `REPORT.md`, section 3.
Their exact positive LDL pivots are

\[
1,1/8,15/256,323/480,6539/65664,7983605/14228864,
1558913/6386884,813607/24942608
\]

and

\[
1,71/256,139/1704,245/4448,79/3840.
\]

Thus `G>=0` pointwise. Integration proves the theorem for smooth data. Strong
periodic `W^{1,4}` approximation of `F,H,g` preserves the separated form and
passes every quartic integral and cubic-stress/gradient pairing to the limit.
This covers `s=0`, `s<0`, arbitrary amplitudes and arbitrary concentration in
the stated class. It does not cover a general two-dimensional first potential.
The all-gradient target remains open.

The rational shifted-matrix bound and nonsharp strict ratio improvement are
additional results in `QUANTITATIVE_ADDENDUM.md`. This base proof remains valid
independently of them. Historical priority is unknown; Gram/SOS certification,
integration by parts, and Sobolev density are classical machinery.
