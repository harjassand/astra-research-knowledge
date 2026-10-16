# Receiving audit: mixed-source continuation, version 1

Date: 16 October 2026. Verdict: **PASS**, with the source floor explicitly
retained as a necessary-condition budget rather than an all-gradient bound.
This addendum preserves all original r=1 audit files.

Input: `../ga_sharp_invention/MIXED_SOURCE_CONTINUATION.md`.
Independent reproduction: `python3 mixed_source_exact_audit.py`.
All **12 exact check groups pass**, using rational polynomial arithmetic and
exact circular moments from the receiving audit's own standard-library code.
The source hash and code hashes are saved in `MIXED_SOURCE_AUDIT_RECEIPT.json`.

For the original r=1 stress and smooth compatible fields,

\[
E_s=\langle G_s\rangle-X_s,\qquad
X_s=\left\langle g\left(4s^2+10sf_x+\frac32|Df|^2\right)f_{xy}\right\rangle.
\]

Since G_s is bounded below by the certified nonnegative reserve,
E_s<0 necessarily implies

\[
X_s>\langle G_s\rangle
\ge\frac1{128}\langle M_4+s^2(a^2+c^2+d^2)\rangle.
\]

The inequality X_s greater than the small floor is not sufficient for a
negative map. The displayed falsifier is correct: take

\[
f=\sin(x+y),\qquad g=-\sin(x+y).
\]

Then a=b=cos(x+y), c=d=-cos(x+y), det Dphi=0 pointwise, and

\[
X_s=2s^2+3/8,\qquad E_s=s^2+3/4,\qquad
\langle G_s\rangle=3s^2+9/8.
\]

The independently reconstructed means are

\[
\langle M_4\rangle=15/4,\qquad
\langle a^2+c^2+d^2\rangle=3/2.
\]

In fact the exact excess over the small reserve is

\[
\boxed{X_s-\frac1{128}\langle M_4+s^2(a^2+c^2+d^2)\rangle
=\frac{509}{256}s^2+\frac{177}{512}>0}
\]

for every real s. Meanwhile E_s>0. This decisively refutes universal
domination of X_s by that small floor. It does not refute domination by
the exact G_s, and it does not refute the target Jensen inequality.

The concentration calculation is also correct for compactly supported
smooth plane data. Under

\[
\phi_\epsilon(x)=\epsilon^{1/2}\phi((x-x_0)/\epsilon),
\quad s_\epsilon=\epsilon^{-1/2}s,
\]

the area contributes exponent 2, g contributes 1/2, the quadratic
coefficient of f_xy contributes -1, and f_xy contributes -3/2. The source
exponents sum to zero. The quartic residual, Jensen gap after subtracting
the constant background, and small floor each scale with exponent -2 in
their integrands and are invariant after integration. Thus compact
concentration is retained exactly. On a fixed torus, this statement applies
when the rescaled compact support fits inside the cell; normalized averages
then merely add the same fixed area factor. It does not preserve separation
of a general first potential.

Finally the local-null-stress classification is valid. Suppose a C^1 law
S(a,b) on R^2 has div S(Df)=0 for every smooth scalar f. Arbitrary gradient
and symmetric Hessian jets at a point give

\[
S_{1,a}=0,\qquad S_{2,b}=0,\qquad S_{1,b}+S_{2,a}=0.
\]

The first two identities imply S_1=p(b) and S_2=q(a). Since p'(b)+q'(a)=0
for all independent a,b, these derivatives are opposite constants. Hence

\[
S(a,b)=(-\lambda b+u,\lambda a+v).
\]

The constants are independent of a,b; they may depend on externally fixed
parameters such as s. This excludes a nonlinear stress depending only on Df
that is divergence-free for every scalar f. It does not exclude nonlinear
stresses on a restricted conservation class, nonlocal stresses, or laws using
additional derivatives or potentials. The classification and integration
arguments are analytic reasoning, not machine-formalized theorems.

The mixed-source continuation therefore has correct algebra, a decisive
counterexample to an invalid shortcut, and the correct unresolved obligation.
It supplies no all-gradient QC proof or historical priority conclusion.
