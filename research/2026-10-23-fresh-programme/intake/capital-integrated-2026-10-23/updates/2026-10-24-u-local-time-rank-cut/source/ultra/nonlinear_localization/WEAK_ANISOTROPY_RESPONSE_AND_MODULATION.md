# Weak fourfold breaking: coupled response and the actual metastability gate

24 October 2026. Sol continuation of the frozen finite-inertia q / KG model.
No new material, numerical fixture, or hardware operation. Primary science
is available from the beginning: the nonlinear-resonance/normal-form method
of [Soffer–Weinstein](https://arxiv.org/html/chao-dyn/9807003v1) is the direct
ancestor. Its Theorem 1.1 concerns small data near a linear bound state for
a three-dimensional KG equation with potential. It cannot be quoted as a
lifetime theorem for a finite circular state of this one-dimensional point
model. Its distinction between a computed resonance and a controlled
dispersive normal form is the relevant standard here.

The chosen mechanism is slow loss of the bound orbit's full energy through
coupled anisotropy sidebands, with a modulation remainder to be proved.
The exact/no-periodic obstruction and a frozen-circle power estimate alone
do not establish finite-horizon retention or decay.

## 1. Exact decomposition and a specified open sector

Represent the two real components by z=q1+i q2. For the previous positive
fourfold perturbation, the restoring force is exactly

```
(gamma+3 epsilon/4)|z|^2 z+(epsilon/4) conjugate(z)^3.
```

Write gamma_bar=gamma+3epsilon/4. Include that isotropic shift in the
reference circular family; it is not counted as a radiative effect. For
the first bounded attack choose a fixed compact frequency interval in

```
max(Omega_lin, omega_c/3)<Omega<omega_c.
```

Endpoints, the linear branch origin and thresholds are excluded by fixed
margins. This is an analytical sector, not a selected numerical fixture.
Let A^2=−a(Omega)/gamma_bar and B=gamma_bar A^2>0, with the previous
a(Omega)=omega0^2−Omega^2−g^2/(2c sqrt(omega_c^2−Omega^2)).

Use exp(+i nu t). The causal outgoing self-energy at an open frequency is

```
Sigma(nu)=−i sign(nu) eta_nu,
eta_nu=g^2/[2c sqrt(nu^2−omega_c^2)]>0.
```

Below threshold Sigma(nu)=g^2/[2c sqrt(omega_c^2−nu^2)]. These signs follow
from the causal boundary value, not an arbitrary loss term.

## 2. The first-order response is a two-channel scattering problem

Linearization about z0=A exp(i Omega t) couples a perturbation w to its
conjugate through B exp(2i Omega t) conjugate(w). The fourfold forcing
therefore requires

```
z=z0+epsilon[b exp(−3i Omega t)+d exp(5i Omega t)]+O(epsilon^2).
```

Define

```
a3=omega0^2−9Omega^2+2B,
a5=omega0^2−25Omega^2+2B,
eta3=eta_{3Omega}, eta5=eta_{5Omega},
M=[[a3−i eta3, B], [B,a5−i eta5]].
```

The response amplitudes solve
`M (b,conjugate(d))^T=(−A^3/4,0)^T`. Both diagonal imaginary parts have the
same negative sign after conjugating the second equation. Thus
`−Im(x^* M x)=eta3|x1|^2+eta5|x2|^2>0`, proving invertibility. Since
eta5>0 and B>0, b and d are both nonzero. This is the full first-order
outgoing *linearized* response; it is not a solution of the unforced
nonlinear problem for arbitrarily long time.

For circular two-component radiation, the outgoing energy flux associated
with a complex coefficient epsilon a exp(i nu t) is
`P_nu=epsilon^2 |nu| eta_nu |a|^2`; this is twice the scalar cosine formula.
The first candidate energy-loss coefficient is therefore

```
Gamma_E(Omega)=3Omega eta3 |b|^2+5Omega eta5 |d|^2>0,
P_candidate=epsilon^2 Gamma_E.
```

## 3. Angular-momentum backreaction is consistent, not omitted

The anisotropic potential left after the isotropic shift is
`epsilon Re(z^4)/16`. Hence exact torque is
`L_dot=epsilon Im(z^4)/4`. Substitution of the two-channel first-order
response gives the averaged second-order torque

```
<L_dot>=epsilon^2 A^3 Im(b)
       =−4epsilon^2(eta3|b|^2+eta5|d|^2).
```

The second equality follows directly by taking the imaginary part of
`x^* M x=x^*(−A^3/4,0)`. The radiation's angular momentum per unit energy
is 1/nu, with its sign. Thus its angular flux is
`epsilon^2[−eta3|b|^2+eta5|d|^2]`. Subtracting this from the torque gives

```
Omega dot(L_bound)=−epsilon^2 Gamma_E,
dot(H_bound)=−epsilon^2 Gamma_E,
```

to this formal order, using the circular family's exact dH/dL=Omega.
There is no hidden conservation of L once anisotropy is present. A single
orbit parameter is consistent with these balances; energy alone was not
used to erase the broken-symmetry torque.

The corresponding modulation *candidate* is

```
H_bound'(Omega) Omega_dot=−epsilon^2 Gamma_E(Omega),
```

with full field-inclusive H_bound, not bare oscillator energy. H_bound'>0
on this branch. The integral epsilon^−2 integral H_bound'/Gamma_E dOmega
is only a candidate drift time until a uniform approximation theorem is
proved. It is not reported as the lifetime of an actual prepared state.

## 4. An exact useful spectral reduction in this open sector

For the unperturbed rotating-frame linearization define
`f(nu)=omega0^2−nu^2−Sigma(nu)` below the cutoff. It is strictly concave
on (−omega_c,omega_c), and f(Omega)=−B. A nonzero real gap-mode frequency
sigma in (0,Delta), Delta=omega_c−Omega, would require

```
[f(Omega−sigma)+2B][f(Omega+sigma)+2B]−B^2=0.
```

Since Delta<2Omega in the selected sector, |Omega−sigma|<Omega and the
first factor exceeds B. Strict concavity makes the sum of the two factors
less than 2B. If the other factor is positive their product is less than
B^2; if nonpositive the product is nonpositive. The displayed determinant
is therefore strictly negative. Outside this gap an open lab-frequency
channel forces its oscillator coefficient to zero for an L2 eigenstate;
the nonzero coupling B then forces the other one to zero. Thus there is
no nonzero L2 internal mode in this sector. The phase/family neutral
subspace at sigma=0 must still be separated explicitly.

This spectrum argument is not yet a dispersive estimate. A plausible next
lemma is that the point-port continuum resolvent, after neutral subtraction,
has square-root threshold jumps and an integrable t^−3/2 local kernel.
That lemma, its parameter uniformity, and the slow-modulation nonlinear
normal form are to be checked rather than assumed.

## 5. The finite-horizon theorem that is actually needed

The substantive target is a controlled modulation approximation on
t=O(epsilon^−2), while Omega remains in the chosen compact sector. It must
bound the local deviation from the moving circle/first-order sidebands and
the accumulated remainder in the Omega equation; only that can justify
the candidate drift time. Global small distance to one fixed orbit is
inappropriate after O(1) energy has propagated into radiation.

Initial data must be supplied by the finite local preparation, not by a
non-normalizable stationary outgoing wave. Its transient and preparation
error must be bounded relative to epsilon; a fixed error independent of
epsilon cannot silently be discarded in an epsilon^2 rate statement.
The retarded field and no-incoming condition matter. Energy-norm closeness
alone permits remote incoming packets with later local effects and is not
a dispersive preparation condition. The actual earlier empty-field ramp
has additional causal structure, which must be used if needed.

Exact available reduction: eliminating the field gives the local oscillator
a retarded Bessel-memory equation, with the homogeneous field term fixed
by the actual prepared state. A finite-horizon proof can work at this port,
but must control its neutral projection, continuum memory, and nonlinear
backreaction together. No frozen periodic far-field ansatz supplies that
proof. Until it is completed, status is self-consistent response/modulation
candidate, NOT an actual lifetime or nonlinear decay theorem.
