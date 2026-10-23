# Pointwise obstruction for the binary-mixture SLD source ledger

This checks only whether an instantaneous state-pair inequality of the form

```text
S <= theta Tr(R Gamma(A)) + K Tr(P_e R)
```

can hold for every feasible binary state pair, with fixed finite `theta<1` and finite `K`. It does not alter the frozen Hilbert--Schmidt source and does not construct a reachable sensing protocol.

## Exact feasible state pairs

Use a three-dimensional sample basis `|a>, |e>, |dead>` with no controller, `V=|e><a|+|a><e|`, `Z|a>=|a>`, and `J=|dead><e|`. Fix any nonzero parameter separation `d_s=g0-g1>0` in the allowed interval. For `0<p<1/2`, set

```text
R = (1-p)|a><a| + p|e><e|,
A = -sqrt(p) sigma_y on span{|a>,|e>}, and A|dead>=0,
Q = (R A + A R)/2 = -sqrt(p) sigma_y/2,
rho_0 = R+Q,   rho_1 = R-Q.
```

Both `rho_0` and `rho_1` have trace one. Their nonzero two-by-two blocks have determinant

```text
p(1-p) - p/4 = p(3/4-p) > 0,
```

so they are positive density operators. `A` vanishes on `ker R`, has norm `sqrt(p)<=1`, and satisfies the required Lyapunov equation. Also `C=Tr(QA)=p` and `||Q||_1=sqrt(p)`.

## Source and dissipation terms

Since `A^2=p(P_a+P_e)` and `V` acts only within this subspace, `[V,A^2]=0`. Direct Pauli-block calculation gives

```text
[V,A] = -2 i sqrt(p) (P_a-P_e),
S = i d_s Tr(R[V,A]) - (i d_s/2)Tr(Q[V,A^2])
  = 2 d_s sqrt(p)(1-2p).
```

The generator terms are `kappa[Z,A]^dagger[Z,A]` and `gamma[J,A]^dagger[J,A]`. Their expectations are

```text
Tr(R [Z,A]^dagger[Z,A]) = p,
Tr(R [J,A]^dagger[J,A]) = p(1-p),
Tr(R Gamma(A)) = p[kappa + gamma(1-p)],
Tr(P_e R)=p.
```

Thus the proposed right side is

```text
p { theta[kappa+gamma(1-p)] + K },
```

which is `O(p)` for fixed finite `theta,K`, whereas `S` is positive and `O(sqrt(p))`. The inequality fails for sufficiently small `p`. Reversing the sign of `A` handles the opposite sign of `d_s`.

## Scope

This is an algebraic counterexample among positive binary state pairs satisfying the mixture-SLD definitions. It rules out that universal pointwise closure, even with the mandatory `a-e` coupling operators appearing in `S` and `Gamma`. It does **not** show that this `R,Q,A` is reachable at any time from a common parameter-independent input under the stated dynamics with small completed death risk. Consequently it is not a sensing/acquisition evasion or a refutation of a history-dependent dynamical corrector. It shows that a valid proof must use reachability/history or a compensated functional beyond this instantaneous state-pair inequality.
