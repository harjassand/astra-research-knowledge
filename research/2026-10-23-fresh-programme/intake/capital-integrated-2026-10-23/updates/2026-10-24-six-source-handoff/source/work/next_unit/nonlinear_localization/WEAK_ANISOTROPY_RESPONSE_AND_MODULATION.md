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

Final internal status: the nonlinear compact-sector slow-time construction
in Sections 6–10 passed the consequential independent root check, supported
by the bounded algebra, kernel and angular-balance audits named below.
It establishes the stated `epsilon^−2` drift law for this model and paid
preparation. This is internal proof checking, not external certification,
novelty clearance, an acquired experiment or practical advantage.

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

This spectrum argument alone is not a dispersive estimate. The subsequent
linear check in Section 6 closes the neutral-subtracted local kernel gate;
it does not by itself prove nonlinear modulation. The moving-history
construction below is separated from that linear result.

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
proof. The following sections give the proof construction and the precise
estimates it uses. The internal check closes these estimates at the stated
compact-sector/model scope; no pre-existing general lifetime theorem or
hardware capability is being invoked.

## 6. Causal sheets, completed resolvent elements, and local kernels

The safe continuation uses one Laplace variable with `Re s>0`. In rotating
Nambu coordinates the oscillator matrix is

```
M_Omega(s) = [
 [(s+iOmega)^2+omega0^2+2B-g^2/(2c sqrt((s+iOmega)^2+omega_c^2)), B],
 [B, (s-iOmega)^2+omega0^2+2B-g^2/(2c sqrt((s-iOmega)^2+omega_c^2))]
],
```

where both square roots have positive real part. At `s=0+−i sigma`, the
two lab frequencies are `Omega−sigma` and `−Omega−sigma`. At
`sigma=4Omega` this gives exactly the matrix in Section 2. Continuing
`f(Omega−sigma)` with the same outgoing sign as `f(Omega+sigma)` after a
cut, rather than using this Laplace matrix, would put a channel on the
wrong sheet. In particular it would invalidate the both-open dissipativity
argument.

There are four separated branch points, `s=±i(omega_c±Omega)`. At any
one of them let `kappa` be the vanishing channel square root and let `A_*`
be the finite companion diagonal. Direct inversion gives

```
R_jj = −2c kappa/g^2 + O(kappa^2),
R_jk = O(kappa),
R_kk = 1/A_* + O(kappa).
```

At an inner threshold the companion is
`f(2Omega−omega_c)+2B>B>0`; at an outer threshold it is already open and
has a nonzero imaginary part. Thus the vanishing-channel expansion is
nondegenerate throughout the fixed compact sector. At zero, the determinant
is `(B f''(Omega)−f'(Omega)^2) sigma^2+O(sigma^4)`, with nonzero negative
coefficient. The full phase/family Laurent principal part has orders two
and one and must both be removed. Positivity of the quadratic
`H−Omega L` on the symplectic phase quotient excludes off-axis physical
sheet eigenvalues. Section 4 excludes every other real pole.

The completed field resolvent is also needed, rather than only `R=M^−1`.
With

```
G_j(x)=exp(−kappa_j |x|/c)/(2c kappa_j),
```

its diagonal field block is
`G_j(x−y)+g^2 G_j(x)R_jj G_j(y)` and its cross-channel block is
`g^2 G_j(x)R_jk G_k(y)`. The `1/kappa_j` terms in the first expression
cancel. For example its singular free part and feedback correction combine
as

```
[exp(−kappa|x−y|/c)−exp(−kappa(|x|+|y|)/c)]/(2c kappa)+O(1).
```

Point/profile and profile/profile elements therefore have a finite limit
and a square-root correction at each edge. This cancellation must be done
on the **complete unprojected** element. Only then subtract that element's
full neutral principal part. Substituting `R−P0` alone inside the old field
Schur formula is not the full continuum projection.

All profile sources and observations used below are oscillator vectors or
finite sums of `|x|^m exp(−a|x|)`, with bounded finite `m` and
`a>=a_min>0`. The two basic pairings, writing `s0=kappa/c`, are

```
integral G_kappa(x) exp(−a|x|) dx = 1/[kappa(ca+kappa)],

double integral exp(−a|x|)G_kappa(x−y)exp(−b|y|) dxdy
 = 2(a+b+s0)/[c^2 s0(a+b)(a+s0)(b+s0)].
```

Polynomial moments follow by differentiating in `a,b`. In the double
pairing the leading `2/(c kappa ab)` is canceled by the point feedback.
At high frequency its expansion begins with
`2/[c^2(a+b)](s0^−2−ab s0^−4+(a+b)ab s0^−5+...)`:
the apparent order-three term cancels. Thus its retarded/advanced jump is
`O(|sigma|^−5)`. Oscillator/profile completed elements have integrable
high-frequency jumps as well. At most two first-order-state frequency
factors leave an integrable jump. The `−I` term in the momentum-from-position
block must be retained when making that first-order conversion; otherwise
one can manufacture a spurious contact term.

Consequently the full neutral-projected semigroup matrix elements between
the stated local observations and point/profile source families obey

```
|local observation of exp(A_Omega t) Pc_Omega source|
 <= C (1+t)^−3/2 * source coefficient bound,   t>=0,
```

uniformly on the compact sector and on the compact profile-parameter sets.
Indeed their cut jumps are smooth away from the four edges, have only
square-root edge cusps, and have integrable high-frequency derivatives.
Partition into edge neighborhoods and smooth pieces, use the elementary
square-root Fourier endpoint estimate at the edges and integration by
parts elsewhere. There is no residual pole and no polynomial part at
infinity. Energy-space boundedness gives the finite-time bound. This is a
finite family of local matrix-element estimates, **not** an asserted
weighted-space scattering theorem. The bare eliminated Bessel memory
still has a nonintegrable absolute `t^−1/2` tail.

This linear gate was independently checked in
`luna_boxcar/DRESSED_THRESHOLD_KERNEL_CHECK.md`. Parameter differentiation
of the kernel generally introduces a `t` factor in the edge phase, so its
derivative need not be in `L1`. The argument below does not assume `L1`
Lipschitz dependence of the entire kernel on `Omega`.

## 7. Full-state neutral coordinates and their first normal form

Let `X=(q,p,u,v)`, let `R_theta` rotate both physical components of every
coordinate, and write the reference state at phase zero as `Phi(I)`, where
`I=L_b(Omega)` and `Omega=Omega(I)`. Denote the component rotation generator
by `Jrot`. The standard symplectic form is

```
W(X,Y)=q_X.p_Y−p_X.q_Y+integral(u_X.v_Y−v_X.u_Y).
```

The full oscillator-plus-field tangents satisfy
`W(T_theta,T_I)=1`, where `T_theta=Jrot Phi` and `T_I=Phi_I`.
For an actual finite-energy state choose

```
X=R_theta(Phi(I)+Z),
W(Z,T_theta)=W(Z,T_I)=0.
```

This is a local implicit-function chart. It needs small point coordinates
and small pairings with the exponentially localized tangents and their
first few derivatives, not small total radiation energy. Use the local
seminorm `U(Z)` consisting of `|Z_q|+|Z_p|` and the absolute values of
these pairings, uniformly over a slightly larger fixed compact branch.
Including derivatives through order three suffices below. This seminorm
is not presented as a full field-energy norm.

Put `gamma_dot=theta_dot−Omega(I)`. The exact rotating remainder equation is

```
Z_dot=A_I Z+N2(Z)+epsilon P_theta(Phi+Z)
      −I_dot Phi_I−gamma_dot Jrot(Phi+Z),
```

where `N2=O(|Z_q|^2)` and `P_theta` is the point-supported fourfold force.
Here `A_I T_theta=0` and `A_I T_I=Omega'(I)T_theta`. Differentiating the
two constraints gives the exact two-by-two modulation matrix

```
[(1+W(Z,Jrot Phi_I)),  −W(Jrot Z,T_theta)      ] [I_dot    ]
[−W(Z,Phi_II),         (1+W(Jrot Z,Phi_I))    ] [gamma_dot]
 = [−W(N2+epsilon P_theta,T_theta),
     W(N2+epsilon P_theta,Phi_I)]^T.
```

Every matrix correction is a local pairing controlled by `U`. Since
`V0(I)=A(I)^4/16`, inversion for small `U` gives

```
I_dot=4epsilon V0 sin(4theta)+O(U^2+epsilon U),
theta_dot=Omega(I)+epsilon V0' cos(4theta)+O(U^2+epsilon U).
```

Under the bootstrap `U<=B0 epsilon`, the two remainders are `O(epsilon^2)`.
The explicit first-order canonical change, with
`G=V0(I) sin(4theta)/(4Omega(I))`, is

```
Jslow=I+epsilon [V0/Omega]cos(4theta)+O(epsilon^2),
Theta=theta−epsilon partial_I[V0/(4Omega)]sin(4theta)+O(epsilon^2).
```

It may be defined by its nonsingular exact generating map. Direct
differentiation gives
`Jslow_dot=O(epsilon^2)` and
`Theta_dot=Omega(Jslow)+O(epsilon^2)` under that bootstrap. The inverse
signs are `I=Jslow−epsilon(V0/Omega)cos(4Theta)+...` and
`theta=Theta+epsilon partial_I[V0/(4Omega)]sin(4Theta)+...`.
The `Omega' V0/Omega` term from changing action cancels the corresponding
phase term. Root independently derived this same full-state normal form
in `work/next_unit/root/MOVING_NEUTRAL_FIRST_NORMAL_FORM.txt`.

## 8. Exact current-time freezing, without discarding outgoing history

Fix an observation time `t`, set `I_*=I(t)`, `Omega_*=Omega(I_*)`, and
for `0<=s<=t` put

```
psi_t(s)=theta(s)−theta(t)−Omega_*(s−t),
Y_t(s)=R_{psi_t(s)} Z(s).
```

This is a single exact gauge change on the entire past interval, with a
different frozen representation permitted for each observation time.
The free oscillator/field generator commutes with component rotations.
As a result,

```
dY_t/ds=A_* Y_t+B_t(s)Y_t
 +R_psi[N2(Z)+epsilon P_theta(Phi+Z)
        −I_dot Phi_I−gamma_dot Jrot Phi],
```

where `B_t(s)` is **only** the point-supported Hessian difference
`R_psi N'(Phi(I(s)))R_psi^−1−N'(Phi(I_*))`.
There is no global `Jrot` times the far outgoing field in `B_t`.
At `s=t`, `Y_t(t)=Z(t)=Pc_* Z(t)`. Variation of constants followed by
this full frozen projection is therefore exact:

```
Z(t)=Pc_* exp(A_*t) R_{psi_t(0)}Z(0)
 +integral_0^t Pc_* exp(A_*(t−s)) {
     B_t(s)R_psi Z(s)+R_psi[N2+epsilon P_theta(Phi+Z)
                         −I_dot Phi_I−gamma_dot Jrot Phi]
   } ds.
```

It is not an identity obtained from the two point-resolvent residues alone.
All past state dependence is retained inside the integral.

At zero mismatch `Pc_* Phi_I(I_*)=Pc_* Jrot Phi(I_*)=0`.
Thus the two profile-source terms acquire a factor
`min(2,C(|I(s)−I(t)|+|psi_t(s)|))` after this projection. The Hessian
difference and the difference between the actual fourfold forcing and its
frozen periodic forcing have the same type of factor. The finite-profile
kernel estimate of Section 6 applies to these differences by the mean
value formula within the compact profile families.

The first normal form, still under `U<=B0 epsilon`, gives for lag `ell=t−s`

```
|I(s)−I(t)| <= C(epsilon+epsilon^2 ell),
|psi_t(s)| <= C(epsilon+epsilon ell+epsilon^2 ell+epsilon^2 ell^2).
```

The `epsilon ell` term is retained: the frozen frequency is the **raw**
current `Omega(I(t))`, which differs by `O(epsilon)` from its corrected
slow frequency. It must not be silently removed. With
`k(ell)=(1+ell)^−3/2`, the elementary split estimates are

```
integral_0^infinity k(ell) min(2,C epsilon ell) d ell = O(sqrt(epsilon)),
integral_0^infinity k(ell) min(2,C epsilon^2 ell^2) d ell = O(sqrt(epsilon)),
integral_0^infinity k(ell) min(2,C epsilon^2 ell) d ell = O(epsilon).
```

For the squared-phase term split at `ell=epsilon^−1`; for the linear
phase term split at the same scale. No absolute first moment is assumed.

For fixed `Omega`, let `Z1c(theta,I)` denote the **local** limiting
continuum response to the first-order frozen periodic forcing, defined
by the convergent projected causal convolution from lag zero to infinity.
This definition is made only in the local matrix elements above, not by
projecting an infinite-energy stationary outgoing field. It is bounded
and smooth in the compact parameters; the harmonic frequencies are away
from all thresholds and zero. The omitted finite-start tail is at most
`C epsilon(1+t)^−1/2` by the absolute kernel tail.

Consequently the displayed exact Duhamel identity yields the bootstrap
estimate

```
U(Z(t)) <= C0 epsilon+C1 sigma_prep
          +C(B0)epsilon sqrt(epsilon)+C(B0)epsilon^2,
```

as long as `U<=B0 epsilon` and the corrected action remains in the chosen
compact sector. First choose `B0>2C0`, then take epsilon small and
`sigma_prep=o(epsilon)`. This improves the bootstrap. Keeping the frozen
first-order response instead of just its norm gives the sharper local
estimate

```
U(Z(t)−epsilon Z1c(theta(t),I(t)))
 <= C[sigma_prep+epsilon^(3/2)+epsilon(1+t)^−1/2],
              0<=t<=S epsilon^−2,
```

with constants depending on the fixed compact sector and `S`, not on the
length of the outgoing front. A known fixed-duration smooth force startup
adds its explicit causal local transient, discussed in Section 10. No
small weighted norm of that entire outgoing front has been assumed.

## 9. Exact angular bookkeeping closes the averaged coefficient

The first normal form already supplies slow `J=Jslow,Theta`, with
`J_dot=O(epsilon^2)` and `gamma_dot=Theta_dot−Omega(J)=O(epsilon^2)`.
Use the **actual finite-energy** remainder in these mean coordinates,

```
X=R_Theta(Phi(J)+W),  w=W_q1+iW_q2.
```

Combining the neutral micromotion with `Z1c` recovers the full frozen
first-order response: at the nonzero forcing frequency the neutral and
continuum resolvent parts add to the original resolvent. Equivalently,
the first-order neutral equations are
`delta I_dot=4V0 sin(4Theta)` and
`delta theta_dot=Omega' delta I+V0' cos(4Theta)`, with periodic solution
`delta I=−(V0/Omega)cos(4Theta)` and
`delta theta=partial_I[V0/(4Omega)]sin(4Theta)`.
These are precisely the inverse first normal form. Thus

```
w=epsilon[b(J)e^(−4iTheta)+d(J)e^(4iTheta)]+r,
|r| <= C[sigma_prep+epsilon^(3/2)+epsilon(1+t)^−1/2].
```

Constant neutral offsets are absorbed into the initial `J,Theta`. This
recombination is essential: the projected continuum coefficients alone
are not `b,d`.

Angular momentum is quadratic, so it has the exact decomposition

```
L(X)=J+ell1(J,W)+L(W),
ell1=DL(Phi(J))W.
```

The linear term `ell1=O(epsilon)` is a pairing with an exponentially
localized profile. In contrast `L(W)` can be order one because it includes
all radiation already emitted. It is always the actual finite-energy
quantity; a stationary outgoing approximation is **never** inserted into
this global integral.

Differentiate `L(W)` with its exact equation. The entire isotropic free
oscillator/field coupling commutes with rotation and gives zero net
angular torque. The fixed-orbit Hessian term `−B conjugate(w)` gives
`+B Im(w^2)`. The leading fourfold force gives
`−epsilon A^3 Im(conjugate(w)e^(−4iTheta))/4`.
The remaining isotropic torque is cubic in `w`; the further anisotropic
torque is `O(epsilon|w|^2)`. Profile forcing is multiplied by
`J_dot,gamma_dot=O(epsilon^2)` and pairs with the locally `O(epsilon)`
remainder. Finally `DL(W)Jrot W=0` exactly. Therefore

```
d L(W)/dt
 = B Im(w^2)−epsilon A^3 Im(conjugate(w)e^(−4iTheta))/4+R3,
|R3| <= C epsilon^3.
```

This identity uses only local quantities on its right, even though the
left includes the order-one far radiation. It also holds as the integrated
energy-class balance: the field integration-by-parts terms cancel by
skew rotation and the point-coupling terms cancel between oscillator and
field. Smooth finite-energy approximations give the same identity by
continuity; no flux boundary or scattering decomposition is presumed.

The exact total anisotropic torque is

```
d L(X)/dt=epsilon Im(e^(4iTheta)(A+w)^4)/4.
```

Subtract the previous identity and keep `ell1` as an endpoint term. Since
`Im(conjugate(w)e^(−4iTheta))=−Im(e^(4iTheta)w)`, the result is

```
J(t)−J(0)+ell1(t)−ell1(0)
 = integral_0^t {
     epsilon A^4 sin(4Theta)/4
    +3epsilon A^3 Im(e^(4iTheta)w)/4−B Im(w^2)
   } ds + O(epsilon^3 t).
```

For the first fast term use the primitive
`−epsilon A^4 cos(4Theta)/(16Omega(J))`.
Its derivative differs by only `O(epsilon^3)` because `J_dot` and
`Theta_dot−Omega(J)` are `O(epsilon^2)`. No derivative of the latter
is required. The order-two nonconstant harmonics have bounded analogous
primitives at frequency `8Omega`; their accumulated error is `O(epsilon^2)`.
The constant order-two coefficient is exactly

```
(3A^3/4)Im b−2B Im(bd)
 =−3eta3|b|^2−5eta5|d|^2,
```

using `B Im(bd)=eta5|d|^2` and
`A^3 Im b=−4(eta3|b|^2+eta5|d|^2)`.
Equivalently the mean rate of the actual `L(W)` is
`epsilon^2[−eta3|b|^2+eta5|d|^2]`, while the mean total torque has
coefficient `A^3 Im b`. This recovers the Section 3 radiation bookkeeping
without assuming the global radiation has a stationary spatial profile.

The substitution error is bounded by

```
C[epsilon r_loc+r_loc^2+epsilon^3],
r_loc=C[sigma_prep+epsilon^(3/2)+epsilon(1+t)^−1/2].
```

Including the `O(epsilon)` endpoint terms, its integrated bound on
`0<=t<=S epsilon^−2` is

```
O_S(sigma_prep/epsilon+(sigma_prep/epsilon)^2+sqrt(epsilon)
    +epsilon+epsilon^2 log(1/epsilon)) = o(1).
```

Consequently the actual corrected action obeys the integral relation

```
J(t)−J(0)=−epsilon^2 integral_0^t D_epsilon(J(s)) ds+rho_epsilon(t),
sup_{t<=S epsilon^−2}|rho_epsilon(t)|=o(1),
D_epsilon=3eta3|b|^2+5eta5|d|^2=Gamma_E/Omega>0.
```

Here the subscript is literal: `gamma_bar=gamma+3epsilon/4` makes the
family, `A,b,d` and the action-to-frequency map epsilon-dependent.
These smooth functions converge uniformly with their first derivatives
on the compact sector to `D0`. Integral-equation Gronwall on slow time
therefore gives, before exit from that sector,

```
sup_{0<=tau<=S}|J(tau/epsilon^2)−I_*(tau)|=o(1),
d I_*/d tau=−D0(I_*),  I_*(0)=lim J(0).
```

The alternative formal carrier calculation independently checks the same
coefficient: its imaginary derivative term is `(L_b'/A)Omega_dot`, not
the bare oscillator derivative. The details are in
`luna_resolvent_algebra/CARRIER_SOLVABILITY_ADDENDUM.md`; the proof here
uses the exact integrated angular balance instead of presuming a uniform
WKB expansion on the long horizon.

This gives the nonlinear slow-time statement for a fixed compact portion
of the bound-state family and the specified finite-energy preparation.
Its dependencies are the literal causal sheet, full neutral projection,
finite local profile seminorm, known perturbation/force authority during
preparation, and the positive well-posed Hamiltonian flow. It says nothing
about the branch origin, approaching a field threshold, decay to zero, or
an arbitrary approximate preparation with uncontrolled incoming field.

## 10. Actual preparation, force return, and the retained inventory

The initial state here is supplied by the previous empty-field local
preparation. The prescribed following force must include the **known**
fourfold force and the `gamma_bar` shift for its whole duration. It is
not legitimate to let a long isotropic ramp run with the perturbation
uncompensated. The model, empty initial field, and both local force
quadratures are supplied control information.

For a fixed smooth endpoint-flat ramp, any fixed number `m` of integrations
by parts gives `sqrt(Eerr)<=C_m Tprep^−m` at fixed compact target. Thus one
can choose a finite paid `Tprep(epsilon)` and fixed sufficiently high
endpoint flatness with `sigma_prep=o(epsilon)`, even with
`Tprep=o(epsilon^−2)`. This uses only the energy error from the known causal
ramp; no small weighted scattering norm is asserted. For the frozen
continuum evolution, positivity on the phase quotient gives a uniform
energy bound for this `sigma_prep` initial error, enough for the first
term in Section 8 for every current frozen frequency.

A bounded final force step leaves the state continuous and gives the
clean initial condition above if actuator bandwidth is unconstrained. If
a smooth force return is required, retain a fixed-duration known taper.
The fourfold cancellation force on that taper is `O(epsilon)` even as
`sigma_prep` tends to zero. It is an explicit compact point-force history,
not hidden inside `sigma_prep=o(epsilon)`. Its linear local continuum
response decays with the same kernels, its neutral part shifts initial
action/phase by `O(epsilon)`, and its fixed-time nonlinear correction is
`O(epsilon^2)`. It therefore adds a decaying `O(epsilon)` startup layer
whose contribution to the integrated modulation residual is `o(1)`.
The isotropic shutdown estimate alone does not prove that statement.

During exact following, the signed additional anisotropic preparation work
is the change of `epsilon Re(z_d^4)/16`, hence `O(epsilon)` at fixed target.
Its gross absolute work can be `O(epsilon(1+Omega Tprep))`; the input drive
is not declared cheap merely because signed work is small. Baseline
preparation work, torque impulse, field footprint and any returned control
energy retain the previous full-cycle ledger. With `Tprep` chosen to grow
slower than `epsilon^−1`, arbitrary fixed-order endpoint flatness can make
the required error small while also making this extra gross work vanish.
This is a mathematical control scaling, not an acquired actuator.

The actual unforced perturbed system conserves `H_epsilon`, not angular
momentum. Its positive coercive energy bounds the global finite-energy
solution. The emitted field can carry `O(1)` energy out to distance
`O(c epsilon^−2)`. The proof does not call that field globally small or
reidentify it as a stationary infinite-energy outgoing wave. The
field-inclusive family inventories `H_b(I), L_b(I)` and dressing length
`c/sqrt(omega_c^2−Omega^2)` remain charged.

There is an actual finite-energy inventory identity, without assuming a
free-radiation scattering split. Define

```
E_field(W)=1/2 integral(|W_v|^2+c^2|partial_x W_u|^2+omega_c^2|W_u|^2).
```

Expansion about the current family gives
`H_epsilon(X)=H_b,epsilon(J)+Omega(J)ell1+E_field(W)+O(epsilon)`.
The oscillator remainder is locally `O(epsilon)`, and the coupling
`−g W_q.W_u(0)` is `O(epsilon)` by the uniform global energy trace bound.
Thus conservation and the paid near-circle initial preparation imply

```
E_field(W(t))=H_b,epsilon(J(0))−H_b,epsilon(J(t))+O(epsilon).
```

This is the actual remainder field, not a stationary outgoing wave of
infinite energy. In the slow-time limit its energy increase is the full
family-energy decrease. No claim of asymptotic completeness is needed.

Frozen after the internal consequential proof check. The result is a
controlled nonlinear compact-sector `epsilon^−2` slow-drift theorem for
the stated model/preparation, beyond the frozen-circle rate. It is not an
external certification, novelty finding, hardware validation, universal
retention bound, or threshold/branch-origin/decay-to-zero theorem.
