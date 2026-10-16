# Quantitative addendum to the frozen base stress proof

The exact rational matrices in `BASE_CERTIFICATE.json` satisfy

\[
Q_E-I/128>0,\qquad Q_O-I/128>0.
\]

`verify.py` checks all rational leading principal minors; their ratios are
retained as `quantitative_floor_ldl_pivots` in
`SEPARATED_STRESS_EXACT_CERTIFICATE.json`. This proof uses no approximate
floating eigenvalues. It gives

\[
G\ge\frac1{128}(M_4+s^2(a^2+c^2+d^2)),
\]

with `M_4` the sum of squares of all ten quadratic gradient monomials. Thus

\[
\langle J(sI+D\phi)-J(sI)\rangle
\ge\frac1{256}\langle|D\phi|^4\rangle
 +\frac{s^2}{128}\langle a^2+c^2+d^2\rangle
\]

for the stated separated-first-potential class. Moving this budget to the
left of `A+sC+s^2Q` and taking its discriminant gives the exact improvement

\[
C^2\le4(A-\langle M_4\rangle/128)
         (Q-\langle a^2+c^2+d^2\rangle/128).
\]

Here `<ad>=0`, so `Q=4<a^2>+<c^2+d^2>`. Since
`J(V)<=9|V|^4/16`, `<M_4>>=8A/9`, and
`<a^2+c^2+d^2>>=Q/4`, the ratio when `AQ>0` is at most
`73073/73728<1`. None of these constants is claimed optimal.

This addendum does not enlarge the allowed first-potential class and is not
an all-gradient estimate.
