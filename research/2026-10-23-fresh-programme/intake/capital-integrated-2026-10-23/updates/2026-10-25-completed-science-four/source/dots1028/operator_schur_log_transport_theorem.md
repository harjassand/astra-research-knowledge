# Positive resolvent transport gives a noncommutative Schur-log inequality

2026-10-25. New operator theorem extending the scalar singular-boundary transport. Noncommuting environmental coefficients are retained; this is not a scalar-to-matrix entropy lift.

## 1. The operator integral

Let beta>=4, W0=beta(beta-2), and let H,V be finite-dimensional positive semidefinite matrices satisfying H+V<=W0 I. For r>0 put

D_r(s)=(r+s)(V+sI)+sH,
K_r(H,V)=integral_0^infinity [s/(r+s)] D_r(s)^{-1} ds.

Then K_1(H,V)>=2K_beta(H,V) in Loewner order.

For s>0 the denominator is faithful. Near zero D_r(s)>=rsI, so the integrand is bounded by I/r^2. At infinity it is bounded by I/s^2. The integral therefore converges in operator norm, including singular H,V.

## 2. Exact positive transport, without commuting H and V

Set R=(beta-1)^2 and Delta=W0 I-H-V>=0. Use the positive baseline measures and matching map from rank_one_schur_log_transport_general_cap.md:

mu_1(ds)=ds/[(s+1)(s+R)],
mu_beta(dt)=2dt/[(t+beta)(t+beta+R-1)],
z=sqrt((s+1)/(s+R)),
t=beta[(beta-1)z-1]/(1-z).

They have exactly equal cumulative mass under this map. Let N1=s(s+R), Nb=t(t+beta+R-1). The two integrals become

K_1=integral [D_1(s)/N1]^{-1} dmu_1,
2K_beta=integral [D_beta(t)/Nb]^{-1} dmu_beta.

Now

D_1/N1=I-(s/N1)Delta+(1/N1)V,
D_beta/Nb=I-(t/Nb)Delta+(beta/Nb)V.

The difference of the second and first is a positive linear combination of Delta and V. Indeed, after multiplying by the positive scalar N1 Nb, its coefficients are

s t (t-s+beta-1)>=0,
beta s(s+R)-t(t+beta+R-1)>=0.

The exact positive factorizations are established in the scalar transport note. Thus D_1/N1<=D_beta/Nb. Both operators are faithful, so inversion reverses this order, proving the integrand comparison. Positive integration gives the theorem. No products of noncommuting positive operators are asserted positive.

## 3. A genuine block-matrix logarithm receiver

Let Z be any rectangular matrix from an environmental space to an upper space, and let V>0 on the environmental space. Assume

Z*Z+V<=W0 I.

Define the faithful block pencil

X_r=[[rI+ZZ*, Z sqrt(V)], [sqrt(V) Z*, V]],

and let Q denote compression onto the upper space. The Schur complement is rI>0. Direct block inversion and Woodbury give

Q(X_r+sI)^{-1}Q
=I/(r+s)-[s/(r+s)] Z D_r(s)^{-1} Z*,

where H=Z*Z. Integrating the logarithmic resolvent identity yields exactly

Q log(X_r) Q -log r I = Z K_r(H,V) Z*.

Consequently

Q log(X_1)Q >= 2 Q log(X_beta)Q -2log beta I.

This inequality is genuinely noncommutative and allows arbitrary upper and environmental dimensions and ranks, subject to the displayed operator resource bound. It preserves the entire Schur cross block; there is no assumed common eigenbasis, measurement, or free removal of coherences.

## 4. Exact boundary of the receiving claim

For a flat rank-k singular source A=aQ and a faithful comparison B with Schur complement (a/R)I on Q, an appropriate rescaling puts B in the X_1 form. The theorem can exclude a positive compressed survivor if the rescaled environmental operator Z*Z+V obeys W0 I. However, equal total trace by itself only controls Tr(Z*Z+V); for k>1 it does not imply this operator cap. It must be checked, derived from a compatible structure, or explicitly retained as an assumption.

Thus this supplies a real higher-rank noncommutative logarithmic interface, not yet a proof of the general higher-rank singular exclusion or the full WH3 target. The missing trace-to-operator allocation cannot be silently inserted.
