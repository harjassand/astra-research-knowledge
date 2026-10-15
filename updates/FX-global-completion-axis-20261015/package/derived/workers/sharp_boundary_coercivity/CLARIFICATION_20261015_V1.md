# Clarifications to the frozen sharp-boundary coercivity proofs

15 October 2026. Additive clarification following internal audit. This file
does not replace or rewrite `PROOFS.md`, `INPUTS_SHA256.json`, or `STATUS.json`.
The accompanying SHA-256 receipt records their preserved bytes and this
clarification's bytes. External mathematical review, formal verification and
historical originality remain UNKNOWN.

The general all-affine pure fourth-order compatible Jensen margin remains
**UNRESOLVED**. No sharp-J storage transfer follows from these clarifications.

## 1. Equation (6) consists of all outer-product equations

Write

```
X(A)=(a-d,b+c),
Y(A)=(-3b+(2r+1)c,(2r+1)a+3d).
```

The shorthand in frozen equation (6) means

```
X_i(Dpsi) partial_yy psi_j = 0,
Y_i(Dpsi) partial_xx psi_j = 0,
for every i,j in {1,2}.                                  (C1)
```

Equivalently, the two full outer products
`X(Dpsi) tensor psi_yy` and `Y(Dpsi) tensor psi_xx` vanish. This is eight
scalar equations, not a Hadamard product between two two-vectors. The eight
selected kernel rows in frozen equation (5) and `EXACT_REDUCTIONS.json`
give exactly these eight equations.

Consequently, if either component of X is nonzero on an open set, both
components of psi_yy vanish on that open set. Analytic continuation then
makes both components vanish everywhere. The same reasoning applies to Y
and psi_xx. This is the implication used in the rigidity proof.

## 2. Strict Jensen positivity uses the full affine map in X and Y

For the strict-Jensen argument at a prescribed affine matrix B, distinguish
the heat perturbation from the full map:

```
eta_t=exp(tL)phi,
psi_t(x)=Bx+eta_t(x),
A_t=Dpsi_t=B+Deta_t,
D²psi_t=D²eta_t.                                        (C2)
```

The corrected density is `D_r(A_t,D²eta_t)`. Its zero-density implications
are precisely

```
X_i(B+Deta_t) partial_yy eta_(t,j) = 0,
Y_i(B+Deta_t) partial_xx eta_(t,j) = 0,
for every i,j in {1,2}.                                  (C3)
```

Thus X and Y are evaluated on the full affine gradient `B+Deta_t`, not
just on the perturbation gradient. If `X(B+Deta_t)` vanishes identically,
spatial decay of the heat perturbation first yields `X(B)=0`, and then
`X(Deta_t)=0`. The elliptic argument applies to eta_t. The corresponding
statement holds for Y. If neither full strain is identically zero, (C3)
and analyticity force `eta_t,xx=eta_t,yy=0`; its decay removes the resulting
bilinear and affine terms. This is the same affine map used by the frozen
strict-Jensen proof.

For the homogeneous angular argument, B=0, so the full map is simply the
heat convolution of the degree-1/2 homogeneous map.

## 3. The fixed-B annular extension requires an amplitude condition

The zero-background angular margin is homogeneous in amplitude. The
fixed-nonzero-B extension of frozen §5.4 additionally uses bounded
quadratic and cubic cross terms after normalizing the angular profile.

Precisely, let `N(h_T)=1`, and apply the fixed inner/outer radial cutoffs on
the logarithmically long annulus of length T. Uniformly over these
normalized profiles,

```
integral |Dphi_T|⁴ = T+O(1),
integral |Dphi_T|² = O(1),
integral |Dphi_T|³ = O(1).                               (C4)
```

For every fixed B, quartic polarization therefore makes its quadratic
and cubic cross terms O_B(1), and their ratio to the fourth-power norm
tends to zero as T tends to infinity. Together with the positive angular
margin, this excludes a zero ratio for this normalized annular mechanism.

More generally write `h_T=a_T tilde_h_T`, where
`N(tilde_h_T)=1` and `a_T=N(h_T)^(1/4)>0`. The corresponding perturbation
is `phi_T=a_T tilde_phi_T`. The fixed-B cross-term estimate relative to its
fourth-power norm has size at most

```
O_r((|B|²/a_T²+|B|/a_T)/T).                             (C5)
```

In particular the same conclusion follows when amplitudes are bounded
away from zero, `a_T>=a0>0`. The frozen cross-term argument does not cover
arbitrary T-dependent amplitudes tending to zero. Indeed exact quartic
homogeneity gives

```
Gap_B(a_T tilde_phi_T)
 = a_T⁴ Gap_(B/a_T)(tilde_phi_T),                        (C6)
```

where `Gap_B(phi)=integral[J(B+Dphi)-J(B)]`. Small amplitudes at fixed B
therefore amount to a growing effective affine background. Such growing
backgrounds remain part of the unresolved general question. No
counterexample or negative conclusion for those small amplitudes is
asserted here.

The positive angular infimum, the rank-one Bregman bound and strict Jensen
positivity retain their stated scopes. They do not supply a uniform
constant for arbitrary compatible rank-two gradients and affine backgrounds.
