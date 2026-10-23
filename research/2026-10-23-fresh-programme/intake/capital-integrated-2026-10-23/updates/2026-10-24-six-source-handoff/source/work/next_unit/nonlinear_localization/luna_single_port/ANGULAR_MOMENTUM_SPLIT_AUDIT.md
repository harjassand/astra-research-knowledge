# Angular-momentum split for the finite-energy remainder

24 October 2026. Short algebra/regularity addendum to
`../WEAK_ANISOTROPY_RESPONSE_AND_MODULATION.md`. Conditional on its stated
local bootstrap and finite-energy Hamiltonian flow; this is not a separate
lifetime proof.

## Charge derivative and signs

Use the corrected coordinates
`X=R_Theta(Phi(J)+W)`, `w=W_q`, with `Jdot=O(epsilon^2)` and
`gammadot=Theta_dot-Omega(J)=O(epsilon^2)`. The full Noether charge is
quadratic, so the exact decomposition is

```text
L(X)=J+ell1(J,W)+L(W),
ell1=DL(Phi(J))W.
```

On the local bootstrap `U(W)<=C epsilon`, `ell1=O(epsilon)` uniformly. The
quadratic rotating-frame Hamiltonian has radial point term
`B (Re w)^2`, `B=gamma_bar A^2`. Its torque on `L(W)` is
`2B Re(w) Im(w)=B Im(w^2)`. The isotropic field/backbone coupling and the
`-Omega(J)L` term are rotationally invariant and contribute no torque to
this quadratic charge. The anisotropic potential is
`epsilon Re(e^(4iTheta)(A+w)^4)/16`. Rotating `w` while holding the profile
fixed gives its leading torque on `L(W)` as
`-epsilon A^3 Im(conj(w)e^(-4iTheta))/4`; the omitted terms are
`O(epsilon |w|^2)`. The cubic remainder of the isotropic point potential is
`O(|w|^3)`. The slow profile-forcing terms pair linearly with `W` and are
`O((|Jdot|+|gammadot|)U)` in the seminorm used in the source note. Therefore

```text
L(W)_dot = B Im(w^2)
           - epsilon A^3 Im(conj(w)e^(-4iTheta))/4
           + O(epsilon^3),
```

under `U<=C epsilon`. In particular, the anisotropy sign is fixed by the
positive full-state torque `L(X)_dot=epsilon Im(z^4)/4`.

With
`w=epsilon[b e^(-4iTheta)+d e^(4iTheta)]+r`, fast-phase averaging gives

```text
mean L(W)_dot
 = epsilon^2 [2B Im(bd)+A^3 Im(b)/4]
   + O(epsilon |r|+|r|^2+epsilon^3)
 = epsilon^2 [-eta3 |b|^2+eta5 |d|^2]
   + O(epsilon |r|+|r|^2+epsilon^3).
```

Here the second sideband row yields `B Im(bd)=eta5 |d|^2`, and the open-channel
dissipativity identity yields
`A^3 Im(b)=-4(eta3 |b|^2+eta5 |d|^2)`. The displayed coefficient is the
angular-momentum rate entering the finite-energy remainder, and matches the
signed angular flux of the two outgoing sidebands. No stationary outgoing
field is inserted into `L(W)`.

The total exact torque has mean `epsilon^2 A^3 Im(b)` at this order. Subtracting
the `L(W)` balance from it in

```text
J(t)-J(0) = integral_0^t L(X)_dot ds
            - [ell1(t)-ell1(0)] - [L(W)(t)-L(W)(0)]
```

gives the action coefficient
`-epsilon^2(3 eta3 |b|^2+5 eta5 |d|^2)`. The `ell1` contribution is an
`O(epsilon)` endpoint term; the zero-mean fast pieces have bounded phase
primitives on the compact sector. The integrated substitution error is
controlled by `integral(epsilon |r|+|r|^2+epsilon^3) ds`, as in the main
modulation estimate.

## Why far radiation does not invalidate the local derivative

`L(W)` itself need not be small: the finite-energy outgoing remainder can
accumulate `O(1)` angular momentum over the `O(epsilon^-2)` horizon. The
argument uses its derivative, not a claim `L(W)=O(epsilon^2)`. In the weak
balance, all non-invariant forcing is either the anisotropic point force or
the local radial Hessian; the coupling and field terms cancel by the
simultaneous-rotation symmetry. The profile derivatives have exponentially
decaying field components, so their pairings with the actual finite-energy
`W` are well-defined and are explicitly included in `U(W)`. Thus an `O(1)`
far-field energy is compatible with the `O(epsilon^3)` profile-forcing
remainder, provided the stated local seminorm bootstrap holds. Global energy
smallness of `W` is neither used nor available.

For energy-class data, `L(W)` is a continuous quadratic functional because
the field variables lie in `H^1 x L^2` and the point variables are finite
dimensional. The integrated Noether balance follows first for smooth
finite-energy solutions and then by energy-space approximation, assuming the
well-posed energy-conserving flow in the source model. A pointwise-in-time
derivative formula for arbitrary weak solutions is not needed. This makes the
angular accounting legitimate at energy regularity; it does not supply the
separate local `U(W)=O(epsilon)` or dispersive estimates required by the
modulation proof.
