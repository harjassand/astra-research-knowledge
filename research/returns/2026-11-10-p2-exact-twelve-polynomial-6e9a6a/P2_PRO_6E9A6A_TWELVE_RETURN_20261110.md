# P2 completed return

Chat: https://chatgpt.com/c/6af2d0d2-f500-83ec-a7d0-20e80bd42677
Assistant final: 6e9a6a3f-833c-5934-b664-ea24360e0379
Exact held prompt: work/astra-renewed-pro-programmes-20261103/P2_FULL_TWELVE_FUNDAMENTAL_BODY_FORCE_POLYNOMIAL_PRO_20261110.txt
Model shown: Pro.

GAP: native final is truncated at 20,000 characters; accessibility tree is virtualized and equations may render imperfectly. Complete final remains at source chat. No original ZIP visible.

## Native final as available

## Answer: yes, from the constructive premises supplied

There is a reduction to the **exact twelve fundamental shear actuators** that retains polynomial resources.

The additional construction uses rapidly oscillating velocity excursions with two properties:

1. Each excursion has zero time integral, so its physical linearized propagator returns **exactly to the identity**.
2. Its quadratic self-interaction has a prescribed nonzero average, which supplies a forcing direction from the next saturation level.

The important quantitative point is how to assemble these excursions. Below, the averaging errors are represented by explicitly bounded corrections to a prescribed reference path. Their force residuals **add**, and the remaining linear defect can be made smaller than a fixed fraction of viscosity. This permits the blockwise \(H^1\) argument from your enlarged-family theorem to survive the actuator reduction.

The resulting exponent is much larger than \(128\). If \(D\) is the fixed saturation depth computed during preprocessing, one conservative choice is
\[
\boxed{p=256\,32^{D+1}.}
\]
The final time coefficients have degree at most \(3\), and one can retain
\[
\boxed{\eta=\frac1{16\rho},\qquad \eta^{-1}\le32R,}
\]
where
\[
\rho=
2+\lceil M\rceil+\lceil\nu^{-1}\rceil+
\lceil\tau^{-1}\rceil+\lceil\epsilon^{-1}\rceil.
\]

Here is the construction and proof. The enlarged-family theorem is used as the accepted starting theorem; its larger fields occur only in the intermediate construction and analysis. The force ultimately emitted belongs exactly to the twelve-dimensional space in the question.

---

# 1. A fixed, rational saturation certificate

Write
\[
\kappa=2\pi,\qquad
B(u,v)=\mathbb P[(u\cdot\nabla)v],\qquad
L_Fv=B(F,v)+B(v,F),
\]
and introduce the algebraically normalized interaction
\[
\mathcal B(u,v)=\kappa^{-1}B(u,v).
\]

For trigonometric fields with integer wavevectors and rational polarizations, \(\mathcal B\) has rational Fourier coefficients. The Fourier Leray projections
\[
P_k=I-\frac{k\otimes k}{|k|^2},\qquad k\ne0,
\]
are rational matrices.

Let
\[
V_0=\operatorname{span}\left\{
e_i\cos(2\pi x_j),\ e_i\sin(2\pi x_j):i\ne j
\right\}.
\]

During fixed preprocessing, construct finite rational Fourier spaces
\[
V_0\subset V_1\subset\cdots\subset V_D
\tag{1}
\]
such that \(V_D\) contains the enlarged shear family from the supplied theorem.

The finite Fourier saturation needed here is available from the supplied algebraic premise. Nersesyan’s Theorem 4.1 and Proposition 4.3 also supply exact finite-level generation, including the twelve-mode choice, rather than only density of an unspecified collection. :chatgpt-content-reference{index="0"}

## 1.1 Why the certificates support the required signs

If \(a,b\) are individually single divergence-free Fourier modes, then
\[
B(a,a)=B(b,b)=0.
\]
Consequently,
\[
\mathcal B(a+b,a+b)
=\mathcal B(a,b)+\mathcal B(b,a),
\]
and
\[
\mathcal B(a-b,a-b)
=-\mathcal B(a,b)-\mathcal B(b,a).
\tag{2}
\]

Thus both signs of each symmetric interaction are available through negative quadratic squares of fields in the lower space.

Choose a pure-frequency sine/cosine basis at every level. These spaces can be kept invariant under translations, and hence under \(\Delta\). One way to see this is that the operation
\[
V\longmapsto V+\operatorname{span}\{\mathcal B(a,a):a\in V\}
\]
preserves translation invariance. Every finite-dimensional translation-invariant trigonometric space is a sum of Fourier subspaces.

Exact rational linear algebra therefore produces, for every basis vector and its negative at level \(j+1\), certificates of the form
\[
u=\eta(u)-\sum_{\ell=1}^{J_j}
d_\ell(u)\,\mathcal B(\xi_\ell,\xi_\ell),
\qquad d_\ell(u)\ge0,
\tag{3}
\]
where
\[
\eta(u),\xi_\ell\in V_j.
\]
The list of possible \(\xi_\ell\)’s is fixed. For a general rational \(u\in V_{j+1}\), sign splitting of its basis coefficients gives (3) by rational arithmetic.

The certificate coefficients satisfy fixed bounds
\[
\|\eta(u)\|_*+\sum_\ell d_\ell(u)\le C\|u\|_*.
\tag{4}
\]
Here and below \(\|\cdot\|_*\) is a computable coefficient norm on a fixed finite Fourier table, large enough to control every spatial norm used in the proof.

This preprocessing terminates by finite algebraic saturation. Its entire search, rational elimination, Fourier tables, and certificate descriptions are charged to the fixed preprocessing cost.

---

# 2. The enlarged-family reference

Use the supplied enlarged-family construction, with its fixed constants enlarged when necessary below. It gives a prescribed carrier \(w\), a rational force \(f^{(0)}\in V_D\), and the macro-word \(W(s)\).

Use
\[
T=B_*\rho^4,\qquad
s=(B_*^2\rho^6)^{-1},\qquad
n=B_*^9\rho^{28},\qquad
\delta=(B_*\rho^8)^{-1}.
\tag{5}
\]
Then
\[
ns^4=T,\qquad ns^5=(B_*\rho^2)^{-1}.
\]

The fixed integer \(B_*\) is chosen large enough that:

- \(\delta\le\tau/2\);
- the supplied linear word satisfies
  \[
  \|W(s)^nU_0\|_2\le\epsilon/4
  \quad\text{whenever }\|U_0\|_{H^1}\le M;
  \tag{6}
  \]
- the blockwise Sobolev and viscosity estimates have the smallness margins used below;
- \(\delta\le\nu^3/(128C_EM^4)\);
- the numerical endpoint estimate in Section 7 is at most \(\epsilon/4\).

The last requirement only enlarges a fixed constant.

The carrier is zero at the beginning and end of every original pulse, in particular at every macro-block boundary. Its rational enlarged-family force can be rounded so that
\[
r^{(0)}
=
f^{(0)}-\bigl(w_t-\nu\Delta w+B(w,w)\bigr)
\]
satisfies
\[
\|r^{(0)}\|_{L^\infty L^2}\le\frac1{16}.
\tag{7}
\]

Set \(b^{(0)}=w\).

The reduction will construct
\[
f^{(j)}\in V_{D-j},\qquad j=1,\ldots,D.
\]
Only \(f^{(D)}\) is ultimately applied.

---

# 3. One explicit lowering step

Suppose \(f^{(j-1)}\) and a prescribed reference \(b^{(j-1)}\) have been constructed.

Let an integer \(H\ge2\) bound:

- \(f^{(j-1)}\) and its first time derivative inside each polynomial interval;
- \(b^{(j-1)}\) and its first piecewise time derivative;
- the amplitudes of all previously constructed carrier fields;
- the old interval count and the reciprocal of the shortest old interval.

All spatial bounds are in the fixed norm \(\|\cdot\|_*\). Section 5 gives a deterministic numerical envelope that provides these bounds without evaluating a PDE or a norm oracle.

## 3.1 Refine the existing partition

Subdivide each old interval into
\[
N=\lceil K H^6\rceil
\tag{8}
\]
equal rational cells. Here \(K\) is a sufficiently large fixed integer chosen in preprocessing.

In each cell \(I=[a,a+d]\), freeze
\[
u_I=f^{(j-1)}(a+).
\]
Apply the fixed certificate (3):
\[
u_I=\eta_I-\sum_{\ell=1}^{J}
d_{I,\ell}\,\mathcal B(\xi_\ell,\xi_\ell).
\tag{9}
\]

Use \(J\) equal slots in this cell. The list may contain zero-amplitude slots, so its length is fixed.

## 3.2 A cubic carrier with an exact linear reset

Take
\[
p(z)=z(1-z)(2z-1)=-2z^3+3z^2-z.
\]
Its exact identities are
\[
p(0)=p(1)=0,\qquad
\int_0^1p(z)\,dz=0,\qquad
\int_0^1p(z)^2\,dz=\frac1{210}.
\tag{10}
\]
Also,
\[
\int_0^z p(r)\,dr=-\frac12z^2(1-z)^2,
\qquad
\sup_{0\le z\le1}\left|\int_0^zp\right|=\frac1{32}.
\tag{11}
\]

On slot \(\ell\), of length \(d/J\), set
\[
\zeta_j(t)
=
A_{I,\ell}\,
p\!\left(\frac{t-t_{I,\ell}}{d/J}\right)\xi_\ell.
\tag{12}
\]
Choose nonnegative rational amplitudes approximating
\[
A_{I,\ell}
=
\sqrt{\frac{210J\,d_{I,\ell}}{\kappa}}.
\tag{13}
\]

The approximation is chosen so that
\[
\left\|
\eta_I-u_I-\frac1d\int_I B(\zeta_j,\zeta_j)\,dt
\right\|_*
\le H^{-8}.
\tag{14}
\]
This is possible with \(O(\log H)\) precision bits, plus fixed constants. Certified rational approximations of \(\kappa\) and square roots suffice.

The carrier has zero time integral on every slot. During a slot its physical linearized propagator is
\[
\mathcal P_j(t)
=
\exp\!\left(-\chi_j(t)L_{\xi_\ell}\right),
\qquad
\chi_j(t)=\int_{t_{I,\ell}}^t
A_{I,\ell}p\!\left(\frac{r-t_{I,\ell}}{d/J}\right)\,dr.
\tag{15}
\]
It therefore returns **exactly to \(I\)** at the end of each slot.

The quadratic average survives:
\[
\frac1d\int_I B(\zeta_j,\zeta_j)\,dt
=
\frac{\kappa}{210J}
\sum_{\ell=1}^J A_{I,\ell}^2
\mathcal B(\xi_\ell,\xi_\ell).
\tag{16}
\]

## 3.3 The lower-space force

Let \(\eta_j(t)=\eta_I\) on cell \(I\). Choose a rational Fourier multiplier \(\widehat\Delta_j\) approximating \(\Delta\), and set
\[
\boxed{
f^{(j)}
=
\eta_j+\partial_t\zeta_j-\nu\widehat\Delta_j\zeta_j.
}
\tag{17}
\]

The lower space is invariant under \(\Delta\), and under its rational scalar-multiplier approximation. Therefore
\[
f^{(j)}\in V_{D-j}.
\]

Its time coefficients are ordinary rational polynomials of degree at most three. The carrier is continuous and zero at every slot boundary. Thus its derivative in (17) introduces no distributional impulses.

The approximation of \(\Delta\) can be chosen so that
\[
\nu\|(\Delta-\widehat\Delta_j)\zeta_j\|_*
\le H^{-8}.
\tag{18}
\]
For a Fourier wavevector \(k\), this just replaces \(-\kappa^2|k|^2\) by a rational approximation. Again, \(O(\log H)\) precision bits suffice.

---

# 4. Exact reference-path corrections and additive residuals

The next definitions are used to prove what the emitted force does. They do not require a PDE solution.

Define
\[
\begin{aligned}
\partial_t\beta_j
={}&
\eta_j-f^{(j-1)}
-L_{b^{(j-1)}}\zeta_j
-B(\zeta_j,\zeta_j),\\
\beta_j(0)={}&0,
\end{aligned}
\tag{19}
\]
and
\[
b^{(j)}=b^{(j-1)}+\zeta_j+\beta_j.
\tag{20}
\]

All these fields are finite Fourier sums and piecewise polynomials in time. Their coefficients involve only the known controls, \(\nu\), and the fixed constant \(\kappa\). Their Fourier supports lie in a fixed finite table determined during preprocessing.

Define
\[
r^{(j)}
=
f^{(j)}
-\left[
\partial_tb^{(j)}-\nu\Delta b^{(j)}
+B(b^{(j)},b^{(j)})
\right].
\tag{21}
\]

Expansion gives the exact identity
\[
\boxed{
\begin{aligned}
r^{(j)}={}&r^{(j-1)}
+\nu(\Delta-\widehat\Delta_j)\zeta_j
+\nu\Delta\beta_j\\
&-L_{b^{(j-1)}+\zeta_j}\beta_j
-B(\beta_j,\beta_j).
\end{aligned}}
\tag{22}
\]

In particular, an old residual is not multiplied by the amplitude of a later carrier.

## 4.1 Why the primitive \(\beta_j\) is small

On a complete cell \(I\), the mean matching (14) and the time variation of \(f^{(j-1)}\) give
\[
\left\|
\int_I\bigl(\eta_j-f^{(j-1)}-B(\zeta_j,\zeta_j)\bigr)\,dt
\right\|_*
\le |I|H^{-8}+C|I|^2H.
\tag{23}
\]

Also,
\[
\int_I L_{b^{(j-1)}(a)}\zeta_j(t)\,dt=0
\]
because every slot has zero integral. Hence
\[
\begin{aligned}
\left\|\int_I L_{b^{(j-1)}(t)}\zeta_j(t)\,dt\right\|_*
&=
\left\|\int_I
L_{b^{(j-1)}(t)-b^{(j-1)}(a)}\zeta_j(t)\,dt\right\|_*\\
&\le C|I|^2H^2.
\end{aligned}
\tag{24}
\]

An incomplete cell contributes at most \(C|I|H^2\). Since the whole active interval has length at most one,
\[
\sum_{\text{complete cells}}|I|^2
\le d_{\max}\sum|I|
\le d_{\max}.
\]
Thus
\[
\|\beta_j\|_{L^\infty_*}
\le C\bigl(d_{\max}H^2+H^{-8}\bigr).
\tag{25}
\]

By (8), \(d_{\max}\le(KH^6)^{-1}\), so
\[
\boxed{
\|\beta_j\|_{L^\infty_*}\le CH^{-4}.
}
\tag{26}
\]

This is a bound over the entire active interval. It does not grow with the number of microcells.

Equations (18), (22), and (26) now imply
\[
\boxed{
\|r^{(j)}-r^{(j-1)}\|_{L^\infty_*}
\le CH^{-3}.
}
\tag{27}
\]

At the final time,
\[
b^{(D)}(\delta)=\sum_{j=1}^D\beta_j(\delta),
\tag{28}
\]
because \(w\) and all \(\zeta_j\) vanish there. The \(\beta_j\)’s need not reset to zero; their small endpoint values will be included in the total-velocity estimate.

---

# 5. A fixed polynomial hierarchy for every stage

Choose
\[
H_0=K\rho^{160},
\qquad
H_j=K H_{j-1}^{32},\quad j=1,\ldots,D.
\tag{29}
\]
At stage \(j\), use \(H=H_{j-1}\).

The fixed integer \(K\) is selected from the precomputed Fourier, certificate, and operator bounds.

The exponent \(160\) is a coarse bound for the original reference. Its force is \(O(\rho^{66})\), its piecewise time derivative is bounded by a fixed multiple of \(\rho^{102}\), its carrier and carrier derivative are polynomially bounded, and its interval count and inverse pulse length are \(O(\rho^{28})\) and \(O(\rho^{36})\). Thus \(H_0\) covers all the incoming numerical bounds after increasing \(K\).

For one lowering step, the estimates are:

| Quantity | Bound in terms of incoming \(H\) |
|---|---:|
| Carrier amplitude \(\|\zeta_j\|_*\) | \(CH\) |
| Maximum partial impulse \(|\chi_j|\) | \(CH^{-5}\) |
| Correction \(\|\beta_j\|_*\) | \(CH^{-4}\) |
| Added force residual | \(CH^{-3}\) |
| New interval count | \(CH^7\) |
| Reciprocal minimum new interval length | \(CH^7\) |
| \(\|\partial_t\zeta_j\|_*\) | \(CH^8\) |
| \(\|\partial_t^2\zeta_j\|_*\) | \(CH^{15}\) |
| New force and its first piecewise derivative | At most \(CH^{15}\) |

For example, the derivative estimates follow from the inverse slot-length bound and the fixed cubic profile. The larger update \(KH^{32}\) comfortably covers these quantities and the numerical magnitudes introduced by expanding cubic polynomials into global time.

All old breakpoints are retained. In particular, every fast carrier and its propagator reset at every original macro-block boundary.

Summing (26)–(27) over the fixed number \(D\) of levels gives
\[
\|r^{(D)}\|_{L^\infty L^2}
\le\|r^{(0)}\|_{L^\infty L^2}+C_DH_0^{-3},
\tag{30}
\]
and
\[
\left\|\sum_{j=1}^D\beta_j\right\|_{L^\infty_*}
\le C_DH_0^{-4}.
\tag{31}
\]

Choose \(K\), once, so that
\[
\|r^{(D)}\|_{L^\infty L^2}\le\frac14,
\qquad
\|b^{(D)}(\delta)\|_2\le\frac{\epsilon}{16}.
\tag{32}
\]
These are uniform choices: \(\epsilon\ge\rho^{-1}\), while \(H_0^{-4}=K^{-4}\rho^{-640}\).

No physical frequency or amplitude in this hierarchy depends on the binary length \(L\). Bit lengths are accounted for separately in Section 9.

---

# 6. Preserving the macro-word through all the carrier loops

This is the step that prevents a large accumulated-strain factor from reappearing.

Let \(I\) be an original macro-block and let \(P_I^0(t)\) be the inviscid propagator of the original carrier \(w\), starting from \(I\).

Define
\[
\mathcal T(t)=\mathcal P_D(t)\cdots\mathcal P_1(t),
\qquad
Q_I(t)=\mathcal T(t)P_I^0(t).
\tag{33}
\]

At the beginning of the macro-block,
\[
Q_I=I,
\]
and at its end,
\[
\boxed{Q_I=W(s).}
\tag{34}
\]
This identity is exact because every fast factor is \(I\) at both endpoints.

By choosing the fixed small-\(s\) range and \(K\) appropriately,
\[
\|Q_I^{\pm1}\|_{H^m\to H^m}\le2,
\qquad m=0,1,2.
\tag{35}
\]
Indeed, each fast factor has a bound
\[
\|\mathcal P_j^{\pm1}\|_{H^m\to H^m}
\le e^{C_m|\chi_j|},
\]
and \(\sum_j|\chi_j|\le C_DH_0^{-5}\).

## 6.1 Conjugated viscosity

The supplied Laplacian commutator estimate also applies to each fixed finite Fourier direction \(\xi_\ell\):
\[
\|[\Delta,L_{\xi_\ell}]\|_{H^2\to L^2}<\infty.
\]
Its bound is computed from the Fourier coefficients.

Telescoping through the product in (33) gives
\[
\|Q_I^{-1}\Delta Q_I-\Delta\|_{H^2\to L^2}
\le C s+C\sum_j|\chi_j|.
\]
The fixed choices can ensure
\[
\boxed{
\|Q_I^{-1}\Delta Q_I-\Delta\|_{H^2\to L^2}
\le\frac1{16}.
}
\tag{36}
\]

## 6.2 The linear defect can be made smaller than viscosity

Put
\[
b=b^{(D)},
\qquad
\mathcal E(t)=Q_I'(t)Q_I(t)^{-1}+L_{b(t)}.
\tag{37}
\]

An \(H^2\to L^2\) estimate is sufficient. For fixed smooth fields \(F,G\),
\[
[L_F,L_G]:H^2\longrightarrow L^2
\tag{38}
\]
has an explicit bound simply by composition:
\[
L_G:H^2\to H^1,\qquad L_F:H^1\to L^2.
\]
Thus
\[
\|\operatorname{Ad}_{e^{-\chi L_F}}L_G-L_G\|_{H^2\to L^2}
\le C|\chi|\,\|G\|_*,
\tag{39}
\]
for the small impulses used here.

To see the order of the estimates, let
\[
A_\ell=w+\sum_{j=1}^{\ell}\zeta_j,\qquad
Q_\ell=\mathcal P_\ell\cdots\mathcal P_1P_I^0,
\]
and define
\[
R_\ell=Q_\ell'+L_{A_\ell}Q_\ell.
\]
Then
\[
R_0=0,
\]
and direct differentiation gives
\[
\boxed{
R_\ell
=
\mathcal P_\ell R_{\ell-1}
+[L_{A_{\ell-1}},\mathcal P_\ell]Q_{\ell-1}.
}
\tag{40}
\]

The new impulse is charged against the amplitudes of earlier carriers, already bounded by its incoming envelope. Therefore
\[
\|R_\ell-R_{\ell-1}\text{ transported}\|_{H^2\to L^2}
\le C H_{\ell-1}^{-5}H_{\ell-1}
=CH_{\ell-1}^{-4}.
\]
The remaining difference between \(A_D\) and \(b\) is \(\sum_j\beta_j\), which contributes only \(L_{\sum_j\beta_j}\).

It follows that
\[
\|\mathcal E\|_{H^2\to L^2}\le C_DH_0^{-4}.
\tag{41}
\]
Choose \(K\) so that
\[
\boxed{
\|\mathcal E\|_{H^2\to L^2}\le\frac{\nu}{64}.
}
\tag{42}
\]
Again this is uniform because \(\nu\ge\rho^{-1}\).

No future carrier amplitude multiplies an earlier impulse in (40). No inverse of a long contracting word occurs.

## 6.3 A stable global propagator for the reference coordinates

Let \(S_0(t,r)\) be the original enlarged-family inviscid propagator. Define
\[
S_Q(t,r)=\mathcal T(t)S_0(t,r)\mathcal T(r)^{-1}.
\tag{43}
\]
Then
\[
\|S_Q(t,r)\|_{2\to2}\le8,
\qquad
S_Q(\delta,0)=W(s)^n.
\tag{44}
\]

The operators in (33)–(44) are used to estimate the original physical equation. They are not supplied as an extra physical advection.

---

# 7. The nonlinear estimate and all weak realizations

Apply the final emitted force \(f=f^{(D)}\), and put
\[
v=U-b,\qquad g=h+r^{(D)}.
\]
The physical equation gives exactly
\[
v_t+L_bv=\nu\Delta v-B(v,v)+g.
\tag{45}
\]

On a macro-block, set \(v=Q_Iz\). Equations (37) and (45) imply
\[
\boxed{
z_t
=
\nu Q_I^{-1}\Delta Q_Iz
-Q_I^{-1}B(Q_Iz,Q_Iz)
+Q_I^{-1}g
-Q_I^{-1}\mathcal E Q_Iz.
}
\tag{46}
\]

Take
\[
\eta=\frac1{16\rho}.
\]
By (32),
\[
\|g\|_{L^\infty L^2}\le\eta+\frac14<1.
\]

## 7.1 Absorption of the new defect

Let
\[
E=\|z\|_{H^1}^2,\qquad Z=\|z\|_{H^2}.
\]
The conjugated-viscosity error contributes at most
\[
\frac{\nu}{16}Z^2
\]
to the \(H^1\) energy.

By (35) and (42),
\[
\|Q_I^{-1}\mathcal E Q_Iz\|_2
\le4\frac{\nu}{64}Z,
\]
so the linear defect contributes at most another
\[
\frac{\nu}{16}Z^2.
\]

The same explicit Agmon estimate used in the supplied proof gives
\[
\|Q_I^{-1}B(Q_Iz,Q_Iz)\|_2
\le128E^{3/4}Z^{1/2}.
\]
After the same Young inequalities, these two small errors leave
\[
\boxed{
E'+\frac{\nu}{4}Z^2
\le
C_E\nu^{-3}E^3+C_E\nu^{-1}\|g\|_2^2,
\qquad C_E=108\cdot128^4.
}
\tag{47}
\]

The coordinate reset is still exactly \(W(s)\). Thus the supplied reset argument applies with the same \(1+O(s^5)\) loss per macro-block and gives
\[
\boxed{
\sup_{0\le t\le\delta}\|v(t)\|_{H^1}\le4M,
\qquad
\nu\int_0^\delta\|v(t)\|_{H^2}^2\,dt\le64M^2.
}
\tag{48}
\]
Here \(b(0)=0\), because the original carrier, every new carrier, and every correction start at zero.

## 7.2 Strong existence and the all-Leray–Hopf quantifier

For each fixed compiler output and each actual disturbance, local \(H^1\) strong existence applies. The estimates above prevent the transformed norm, and therefore the physical \(H^1\) norm, from diverging during \([0,\delta]\): the prescribed reference \(b\) is finite and smooth in space.

The strong solution therefore continues throughout the active interval. Weak–strong uniqueness identifies every corresponding Leray–Hopf realization with it there. The standard strong-solution framework and uniqueness mechanism are the same ones used in the previous argument. :chatgpt-content-reference{index="1"}

No quantitative stability radius is extracted from a large uniqueness Grönwall factor. The quantitative disturbance estimate is already contained in (47).

## 7.3 Endpoint estimate

Using the generator of \(S_Q\), equation (45) becomes
\[
v_t
=
Q_I'Q_I^{-1}v
+\nu\Delta v-B(v,v)+g-\mathcal Ev.
\]
Variation of constants and (44) give
\[
\begin{aligned}
v(\delta)-W(s)^nU_0
=
\int_0^\delta S_Q(\delta,t)
\bigl[
\nu\Delta v-B(v,v)+g-\mathcal Ev
\bigr]\,dt.
\end{aligned}
\tag{49}
\]

The defect term is controlled alongside viscosity:
\[
\int_0^\delta\|\mathcal Ev\|_2\,dt
\le\frac{\nu}{64}\int_0^\delta\|v\|_{H^2}\,dt.
\]
Using (48), a convenient conservative bound is
\[
\boxed{
\begin{aligned}
\|U(\delta)-W(s)^nU_0\|_2
\le{}&
\|b(\delta)\|_2
+128M\sqrt{\nu\delta}\\
&+3072M^2\delta^{3/4}\nu^{-1/4}
+8\delta.
\end{aligned}}
\tag{50}
\]

For \(\delta=(B_*\rh

## Expanded visible accessibility activity and page material

```text
Browser tab: 1463921639, Title: "Polynomial Navier Stokes Control", URL: "https://chatgpt.com/c/6af2d0d2-f500-83ec-a7d0-20e80bd42677".
0 AXWebArea Polynomial Navier Stokes Control, URL: chatgpt.com/c/6af2d0d2-f500-83ec-a7d0-20e80bd42677
	1 container
		2 container root
			3 container
				4 link Description: Skip to content, Value: chatgpt.com/c/6af2d0d2-f500-83ec-a7d0-20e80bd42677#_r_3v_
				5 container
					6 container app-shell-sidebar
						7 container App navigation
							8 button (collapsed) Home, Secondary Actions: Expand
							9 button (collapsed) Space, Secondary Actions: Expand
							10 button (collapsed) Scheduled, Secondary Actions: Expand
							11 button (collapsed) Plugins, Secondary Actions: Expand
							12 pop up button (collapsed) Explore, Secondary Actions: Expand
							13 button Sites
							14 button (collapsed) Codex, Secondary Actions: Expand
							15 button Projects
							16 container
								17 pop up button (collapsed) Description: Usage, ID: radix-_r_3f_, Secondary Actions: Expand
								18 pop up button (collapsed) Description: Open profile menu, ID: radix-_R_9esujeiud9iqr7dcchej9arad5_, Secondary Actions: Expand
					19 container
						20 button New chat
							21 image
						22 pop up button (collapsed) Polynomial Navier Stokes Control, ID: radix-_r_57_, Secondary Actions: Expand
						23 button Share
						24 checkbox Description: Toggle pinned summary, Value: 1
							25 image
					26 container
						27 container Conversation
							28 container
								29 container (showing 0-500 of 770 items)
									30 splitter Today 6:08 PM
									31 heading You said:, Value: 4
										32 text You said:
									33 container
										34 text Common control of three-dimensional Navier-Stokes with polynomial physical resources  FULL QUESTION. Does there exist ONE fixed finite family G_1,...,G_r of mean-zero divergence-free real trigonometric polynomial fields on the UNIT three-torus, with integer wavevectors and ordinary rational sine/cosine vector coefficients, and a total deterministic compiler with the following property?  For EVERY binary rational M>=1, 0 < nu,tau<=1 and 0 < epsilon<1, the compiler outputs ordinary rational piecewise-polynomial coefficients c_j(t) on  [0,tau] and a positive rational eta. The SAME prescribed force f=sum_j c_j G_j must make  U_t=nu Delta U-P div(U tensor U)+f+h, div U=0, integral U=0, satisfy ||U(tau)||2<=epsilon for EVERY real mean-zero divergence-free ||U0||H1<=M, EVERY mean-zero divergence-free additive disturbance ||h||\_(L-infinity_t L2_x)<=eta, and EVERY corresponding Leray-Hopf realization. Use the one-sided energy trace at the fixed endpoint. The target is small TOTAL velocity. No observation, feedback, initial-dependent force, selected weak solution, extra advection, distributional impulse or parameter-dependent spatial family is supplied.  The new requirement is POLYNOMIAL resources in numerical input size. Put R=2+M+nu^-1+tau^-1+epsilon^-1 and let L be the complete binary input length. There must be fixed explicitly computable constants A>=1 and integer p>=1, chosen once with the spatial family, such that:  \* compiler bit operations, working-memory bits, total output bits, number of time intervals, polynomial degrees and the bit lengths of every rational numerator/denominator are <=A(L+R)^p;  \* eta^-1, sup\_(0<=t<=tau)||f(t)||\_(W1,infinity_x), and integral_0^tau ||f(t)||\_(W1,infinity_x) dt are <=A R^p. Fixed-family selection and its complete description, all constants, searches, rational rounding and PDE estimates must be paid within a specified finite precomputation and these bounds. A and p cannot depend on the variable inputs. Numerical rational heights may be exponential in their stated bit lengths; they are not free real numbers. No PDE, optimization or norm oracle is supplied.  A positive answer must construct and prove this full compiler. A negative answer must obstruct the stated existence claim over all admitted fixed finite families and compilers; showing that one word, one transfer estimate or one forcing ansatz has exponential cost is not a full negative.  The suggested papers and supplied premises are starting points, not a limit on your research. You may read them, seek additional papers, literature, available Astra work or other sources, change mathematical representations, introduce different ideas and methods, and challenge my framing while pursuing the full question. You choose your sources and approach without further permission.  Available starting mathematics, which you may use or bypass:  1. The arbitrary-accuracy endpoint without the polynomial physical-resource requirement has a constructive positive solution using one fixed enlarged rational shear family. Write kappa=2pi and J=(I-Delta)^(-1/2). The physical generators are L_F v=P[(F.grad)v+(v.grad)F]. A fixed macro-word W(s) of actual shear evolutions has underlying vector-pushforward transport EXACTLY identity and  ||W(s)-exp(s^4 D)||\_(L2->L2)<=C0 s^5. Here D is a bounded compact Fourier multiplier with  Sym D(k)<=-c/(1+|k|^2) I on k-perp, k!=0, for fixed computable c>0,C0 and an effective small-s range. Thus  ||W(s)^n-exp(n s^4 D)||<=C0 n s^5 exp(C0 n s^5). The fixed family consists of rationally rotated shears R_j e_i cos(kappa N R_j e_l.x) and their sine partners, i!=l, where R_j are rational rotations and a fixed integer N clears their denominators. A finite signed rational rotation design gives global negative symmetric part; negative word multiplicities use the inverse physical word. All constants and family selection are finite and computably bounded, although enormous. The original twelve-shear restriction is not a premise of the new question.  Choosing auxiliary time T and small s with n=T/s^4 produces ||W(s)^n J||\<gamma for any prescribed gamma. Each physical exponential can be realized by a rational quadratic pulse q(z)=6z(1-z) with the prescribed signed impulse. Only one shear is active at a time, so B(w,w)=0, where B(u,v)=P[(u.grad)v], and the complete path w starts and ends at zero.  2. The same finite-word interaction argument extends to each fixed integer Sobolev order m: there are fixed computable b_m,c_m and a small-s range with  ||W(s)-exp(s^4 D)||\_(H^m->H^m)<=c_m s^5, and every partial macro-word and its inverse have norm <=exp(b_m s). Since D commutes with the scalar Sobolev weights, exp(tD) is a contraction in H^m. Every forward subinterval propagator of n repeated blocks consequently has norm <=exp(2 b_m s+c_m n s^5). One need not invert the full contracting repeated path. The extension follows by differentiating the conjugated divergence-form elliptic inverse five times, with a small-coefficient Neumann bound in the required Sobolev spaces, and then using the exact identity of the underlying endpoint transport. In particular, the inviscid reference can have an H1 bound independent of the accumulated absolute strain.  3. An available nonlinear all-weak comparison uses v_s+L_w v=0 with v(0)=ACTUAL U0 and the reference delta^-1 w(t/delta)+v(t/delta). Its ideal body force is  f_delta=delta^-2(w_s+B(w,w))(t/delta)-nu delta^-1 Delta w(t/delta). The residual is exactly B(v,v)-nu Delta v. If K=integral_0^1 ||grad w||infinity, V bounds ||v||H1, xi bounds rational force error, and C6 is an explicit Sobolev constant, then every admitted realization satisfies  ||U(delta)-S_w U0||2  <=sqrt(8delta/nu)(16V^2+nu V+eta+xi)    \*exp(K+108 C6^6 delta nu^-3 V^4). The subsequent unforced interval adds at most eta(tau-delta) to the L2 norm. This provides a full finite-bit existential compiler, but the displayed sufficient estimate retains exp(K). For n copies of a fixed one-shear-at-a-time macro-word, K=K0 n s=K0 T/s^3 with fixed K0>0. Replacing the inviscid V bound by a stable Sobolev bound does not by itself remove that factor from nonlinear stability. No polynomial-cost conclusion is supplied.  Optional intuition: stable physical propagators and accumulated absolute strain are different quantities. A cancellation useful for a linear propagator need not extend to all three-dimensional weak solutions. These observations identify an interface, not a required solution method.  Optional primary starting point: Koike, Nersesyan, Rissel and Tucsnak, [https://arxiv.org/html/2506.22233v1](https://arxiv.org/html/2506.22233v1), Theorems 2.4, 3.2 and 4.1, construct finite-control Euler trajectories that enhance PASSIVE SCALAR relaxation on a two-dimensional torus. Their scalar stability, known velocity initial state, smoothness and qualitative control costs differ from the full contract here; no total-velocity or polynomial-resource theorem is imported. Other sources and representations are open.  you may use all subagents avaible
									35 button (collapsed) Show more, Secondary Actions: Expand
										36 text Show more
										37 image
									38 button Copy message
										39 image
									40 button Share prompt
									41 button Edit message
										42 image
									43 button (expanded) Worked for 18m 26s, Secondary Actions: Collapse
										44 text Worked for 18m 26s
										45 image
									46 text I’ll investigate the polynomial resource requirement directly, using parallel work on nonlinear stability, alternative constructions, and possible obstructions. I’ll distinguish a full solution from any advance that still leaves part of the compiler unproved.
									47 container Subagent activity
										48 container
											49 button Nonlinear polynomial
											50 text , 
											51 button Alternative constructions
											52 text  and 
											53 button Obstructions audit
											54 text  started working
									55 text Searching arxiv.org
									56 text Filtered source results and assessed pulled-back viscosity
									57 container Subagent activity
										58 container
											59 button Nonlinear polynomial
											60 text  updated
									61 text Searched 20 websites
									62 text Established blockwise H1 and H2 smoothing bounds
									63 text The linear contraction already has polynomial cost under your premises: a contraction factor 
									64 text 𝛾
									65 text  can be obtained with auxiliary time 
									66 container
										67 text 𝑂 (
										68 text 𝛾
										69 container
											70 text − 2
										71 text )
									72 text  and 
									73 container
										74 text 𝑂 (
										75 text 𝛾
										76 container
											77 text − 14
										78 text )
									79 text  blocks. I’m now testing whether changing coordinates within each block—and resetting them at its endpoint—can keep viscosity and nonlinear error under control without the accumulated 
									80 container
										81 text 𝑒 𝐾
									82 text  loss. Checked commutator bounds
									83 container Subagent activity
										84 container
											85 button Alternative constructions
											86 text , 
											87 button Nonlinear polynomial
											88 text  and 
											89 button Obstructions audit
											90 text  updated
									91 text Specified finite precomputation and made constants explicit
									92 text Searched 6 websites
									93 text Checked propagator bounds and chose parameter scales
									94 text Tuned slack constants and bounded compiler complexity
									95 text Fixed constants and scales
									96 container Subagent activity
										97 container
											98 button Nonlinear polynomial
											99 text  finished
									100 text Estimating the H1 energy
									101 text Estimated nonlinear pairing
									102 text Verified energy bootstrap and integrated dissipation estimate
									103 text Checked bounds and selected semigroup constants
									104 text Bounded the Duhamel error with explicit constants
									105 text Derived rational-mode error bound
									106 text Prepared certified Machin bounds and verified disturbed-flow uniqueness
									107 text Established the energy bound
									108 text Derived semigroup decay bound and precomputed rational decay constant
									109 text Chose σ and B and precomputed σ bounds
									110 text Computed derivative and explicit norm bounds
									111 text Estimated bounds and specified piecewise forcing
									112 text Chose dyadic approximation and bounded the compiler constant
									113 text Determined a valid A and clarified supplied premises
									114 text The blockwise approach now gives a concrete estimate. The commutator 
									115 container
										116 text [ Δ ,
										117 text 𝐿
										118 text 𝐹
										119 text ]
									120 text  bounds the change in viscosity within a block by 
									121 container
										122 text 𝑂 ( 𝑠 )
									123 text , which can be absorbed by viscous dissipation. At block boundaries, the supplied 
									124 container
										125 text 𝐻 1
									126 text  estimate costs only 
									127 container
										128 text 1 + 𝑂 (
										129 text 𝑠
										130 text 5
										131 text )
									132 text . I’m checking the resulting nonlinear bound, its extension to every Leray–Hopf solution, and the rational pulse costs before concluding that this closes the question. Verified Agmon estimates and refined weighted energy bounds Checked the B error bound Prepared technical proof, finite precomputation, and pulse coefficient verification Prepared rational pulses, verified regularity, and computed energy identity Checked commutator and uniqueness bounds Derived explicit coefficient bounds
									133 container Subagent activity
										134 container
											135 button Obstructions audit
											136 text  updated
									137 text Searching 2 websites
									138 container Subagent activity
										139 container
											140 button Alternative constructions
											141 text  finished
									142 text Confirmed proof completeness and bounded forward propagation Precomputed fixed-family bounds and chose explicit D0 bounds Precomputed coefficient bounds and set polynomial resource limits Calculated explicit constants Combined decay estimates and verified pulse bounds Computed the explicit force bound Checked novelty and framed theorem from premises The independent audits support the nonlinear argument. A simple parameter choice now gives degree-two rational pulses, at most 
									143 container
										144 text 𝐶
										145 text 𝑅
										146 text 28
									147 text  intervals, force magnitude at most 
									148 container
										149 text 𝐶
										150 text 𝑅
										151 text 66
									152 text , and disturbance tolerance 
									153 container
										154 text 𝜂
										155 container
											156 text − 1
										157 text ≤ 32 𝑅
									158 text . I’m assembling the proof and explicitly accounting for the fixed precomputation and rational approximation of the Laplacian eigenvalues.
									159 container Subagent activity
										160 container
											161 button Obstructions audit
											162 text  finished
									163 text Computed coefficient bounds Computed N_* bounds and set explicit arithmetic limits Checked resource bounds and defined total input handling Verified the energy estimate and checked index bounds Checked the energy-tail bound Refined proof notation and pulse coefficients Set constants and bounds
									164 heading ChatGPT said:, Value: 4
										165 text ChatGPT said:
									166 heading Answer: yes, using the constructive macro-word premises you supplied, Value: 2
										167 text Answer: yes, using the constructive macro-word premises you supplied
									168 text Those premises are sufficient to obtain the full polynomial-resource compiler. The missing step is an 
									169 container
										170 text 𝐻 1
									171 text  estimate in 
									172 text coordinates that reset after each macro-word
									173 text . Within one block, the conjugated Laplacian differs from the ordinary Laplacian by 
									174 container
										175 text 𝑂 ( 𝑠 )
									176 text , so viscosity remains coercive. At the block boundary, resetting the coordinates costs 
									177 container
										178 text 1 + 𝑂 (
										179 text 𝑠
										180 text 5
										181 text )
									182 text  in 
									183 container
										184 text 𝐻 1
									185 text . Consequently, the nonlinear argument depends on 
									186 container
										187 text 𝑛
										188 text 𝑠
										189 text 5
									190 text , which can be kept small, without paying an exponential in the accumulated strain 
									191 container
										192 text 𝑛 𝑠
									193 text . This gives, with fixed computable constants, the following nonoptimized bounds:
									194 table
										195 row
											196 cell
												197 text Resource
											198 cell
												199 text Bound obtained below
										200 row
											201 cell
												202 text Number of time intervals
											203 cell
												204 container
													205 text 𝐶
													206 text 𝑅
													207 text 28
										208 row
											209 cell
												210 text Degree of every time polynomial
											211 cell
												212 text At most 
												213 text 2
										214 row
											215 cell
												216 container
													217 container
														218 text sup ⁡
													219 text 𝑡
													220 text ∣ 𝑓 ( 𝑡 )
													221 text ∣
													222 container
														223 text 𝑊
														224 text 1
														225 text ,
														226 text ∞
											227 cell
												228 container
													229 text 𝐶
													230 text 𝑅
													231 text 66
										232 row
											233 cell
												234 container
													235 text ∫
													236 text 0
													237 text 𝜏
													238 text ∣ 𝑓 ( 𝑡 )
													239 text ∣
													240 container
														241 text 𝑊
														242 text 1
														243 text ,
														244 text ∞
													245 text 𝑑 𝑡
											246 cell
												247 container
													248 text 𝐶
													249 text 𝑅
													250 text 58
										251 row
											252 cell
												253 text Disturbance tolerance
											254 cell
												255 container
													256 text 𝜂
													257 container
														258 text − 1
													259 text ≤ 32 𝑅
										260 row
											261 cell
												262 text Individual rational bit lengths
											263 cell
												264 container
													265 text 𝐶 ( 𝐿 + log ⁡ 𝑅 + 1 )
										266 row
											267 cell
												268 text Total computation, memory, and output
											269 cell
												270 text A fixed polynomial in 
												271 container
													272 text 𝐿 + 𝑅
									273 container
										274 button Copy table
										275 pop up button (collapsed) Description: Expand table, Secondary Actions: Expand
									276 text A common exponent 
									277 container
										278 text 𝑝 = 128
									279 text  is more than sufficient. I specify below how the fixed constant 
									280 text 𝐴
									281 text , including the entire granted fixed-family precomputation, is computed. The proof uses your premises 1–2 as accepted constructive mathematics. The suggested Koike–Nersesyan–Rissel–Tucsnak paper concerns passive-scalar relaxation through controlled two-dimensional Euler flows; the total-velocity estimate needed here is proved below directly for the three-dimensional Navier–Stokes equation. 
									282 link (collapsed) Value: arxiv.org/html/2506.22233v1?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: Relaxation enhancement by controlling incompressible fluid flows, https://arxiv.org/html/2506.22233v1?utm_source=chatgpt.com
									283 heading 1. Fixed data and notation, Value: 2
										284 text 1. Fixed data and notation
									285 text Work on 
									286 container
										287 text 𝑇
										288 text 3
										289 text =
										290 text 𝑅
										291 text 3
										292 text /
										293 text 𝑍
										294 text 3
									295 text , with
									296 container
										297 text ∥ 𝑢
										298 text ∥
										299 container
											300 text 𝐻 𝑚
										301 text = ∥ ( 𝐼 − Δ
										302 text )
										303 container
											304 text 𝑚 / 2
										305 text 𝑢
										306 text ∥
										307 text 2
										308 text .
									309 text All vector fields below are mean-zero and divergence-free. Write
									310 container
										311 text 𝐵 ( 𝑢 , 𝑣 ) = 𝑃 [ ( 𝑢 ⋅ ∇ ) 𝑣 ] ,
										312 text 𝐿
										313 text 𝐹
										314 text 𝑣 = 𝐵 ( 𝐹 , 𝑣 ) + 𝐵 ( 𝑣 , 𝐹 ) ,
									315 text where 
									316 text 𝑃
									317 text  is the Leray projection. Execute the effective fixed-family construction granted in premise 1. Flatten its fixed word into a finite list of shear factors, with signs chosen so that
									318 container
										319 container
											320 text 𝑊 ( 𝑠 ) =
											321 text 𝑒
											322 container
												323 text −
												324 text 𝛼
												325 text 𝑚
												326 text 𝑠
												327 text 𝐿
												328 container
													329 text 𝐹 𝑚
											330 text ⋯
											331 text 𝑒
											332 container
												333 text −
												334 text 𝛼
												335 text 1
												336 text 𝑠
												337 text 𝐿
												338 container
													339 text 𝐹 1
											340 text ,
										341 text (1)
									342 text where
									343 container
										344 text 𝐹
										345 text ℓ
										346 text =
										347 text 𝐺
										348 container
											349 text ȷ ℓ
										350 text ,
										351 text 𝛼
										352 text ℓ
										353 text ∈ 𝑄 .
									354 text The rational design weights are incorporated into the fixed word using its rational pulse descriptions and fixed multiplicities. The fixed precomputation returns:
									355 content list
										356 container
											357 AXListMarker • 
											358 text The complete rational Fourier descriptions of the 
											359 container
												360 text 𝐺 𝑗
											361 text .
										362 container
											363 AXListMarker • 
											364 text The finite signed-letter list 
											365 container
												366 text (
												367 text ȷ
												368 text ℓ
												369 text ,
												370 text 𝛼
												371 text ℓ
												372 text )
												373 container
													374 text ℓ = 1
												375 text 𝑚
											376 text .
										377 container
											378 AXListMarker • 
											379 text A positive rational lower bound 
											380 text 𝑐
											381 text  in
											382 container
												383 text Sym ⁡ 𝐷 ( 𝑘 ) ≤ −
												384 text 𝑐
												385 container
													386 text 1 + ∣ 𝑘
													387 text ∣
													388 text 2
												389 text 𝐼 .
										390 container
											391 AXListMarker • 
											392 text Rational upper bounds 
											393 container
												394 text 𝐶
												395 text 0
												396 text ,
												397 text 𝑐
												398 text 1
												399 text ,
												400 text 𝑏
												401 text 0
												402 text ,
												403 text 𝑏
												404 text 1
												405 text ,
												406 text 𝑏
												407 text 2
											408 text  and a common admissible small-
											409 text 𝑠
											410 text  range, such that
											411 container
												412 container
													413 text ∥ 𝑊 ( 𝑠 ) −
													414 text 𝑒
													415 container
														416 text 𝑠
														417 text 4
														418 text 𝐷
													419 text ∥
													420 container
														421 text 2 → 2
													422 text ≤
													423 text 𝐶
													424 text 0
													425 text 𝑠
													426 text 5
													427 text ,
												428 text (2)
											429 container
												430 container
													431 text ∥ 𝑊 ( 𝑠 ) −
													432 text 𝑒
													433 container
														434 text 𝑠
														435 text 4
														436 text 𝐷
													437 text ∥
													438 container
														439 text 𝐻
														440 text 1
														441 text →
														442 text 𝐻
														443 text 1
													444 text ≤
													445 text 𝑐
													446 text 1
													447 text 𝑠
													448 text 5
													449 text ,
												450 text (3)
											451 text and every partial block and its inverse have 
											452 container
												453 text 𝐻 𝑗
											454 text  norms at most 
											455 container
												456 text 𝑒
												457 container
													458 text 𝑏 𝑗
												459 text 𝑠
											460 text , for 
											461 container
												462 text 𝑗 = 0 , 1 , 2
											463 text .
									464 text Only these three Sobolev orders are needed. Because 
									465 text 𝐷
									466 text  commutes with the scalar Sobolev weights and has negative symmetric part,
									467 container
										468 text ∥
										469 text 𝑒
										470 container
											471 text 𝑡 𝐷
										472 text ∥
										473 container
											474 text 𝐻
											475 text 𝑗
											476 text →
											477 text 𝐻
											478 text 𝑗
										479 text ≤ 1.
									480 text In particular,
									481 container
										482 container
											483 text ∥ 𝑊 ( 𝑠 )
											484 text ∥
											485 container
												486 text 𝐻
												487 text 1
												488 text →
												489 text 𝐻
												490 text 1
											491 text ≤ 1 +
											492 text 𝑐
											493 text 1
											494 text 𝑠
											495 text 5
											496 text .
										497 text (4)
									498 text For a path consisting of 
									499 text 𝑛
									500 text  blocks, the supplied forward-propagator estimate gives
									501 container
										502 container
											503 text ∥ 𝑆 ( 𝑡 , 𝑟 )
											504 text ∥
											505 container
												506 text 2 → 2
											507 text ≤ exp ⁡  ⁣
											508 text (
											509 text 2
											510 container
												511 text 𝑏 0
											512 text 𝑠
											513 text +
											514 container
												515 text 𝐶 0
											516 text 𝑛
											517 container
												518 text 𝑠 5
											519 text )
											520 text , 𝑟 ≤ 𝑡 .
										521 text (5)
									522 text All constants used subsequently will be calculated from this finite data.
									523 heading 2. The new estimate: viscosity survives a change of coordinates within one block, Value: 2
										524 text 2. The new estimate: viscosity survives a change of coordinates within one block
									525 text Let 
									526 container
										527 text 𝑤 ( 𝑡 )
									528 text  be the prescribed shear carrier. During a single pulse,
									529 container
										530 text 𝑤 ( 𝑡 ) = 𝑎 ( 𝑡 )
										531 text 𝐹
										532 text ℓ
										533 text ,
									534 text and over a complete macro-block,
									535 container
										536 text ∫
										537 text block
										538 text ∣ 𝑎 ( 𝑡 ) ∣ 𝑑 𝑡
									539 text summed over its letters equals
									540 container
										541 container
											542 text 𝑠
											543 text ∑
											544 container
												545 text ℓ = 1
											546 text 𝑚
											547 text ∣
											548 text 𝛼
											549 text ℓ
											550 text ∣ .
										551 text (6)
									552 text This quantity is independent of how quickly the block is executed. Let 
									553 container
										554 text 𝐼
										555 text 𝑗
										556 text = [
										557 text 𝑡
										558 text 𝑗
										559 text ,
										560 text 𝑡
										561 container
											562 text 𝑗 + 1
										563 text ]
									564 text  be one macro-block and define its inviscid propagator
									565 container
										566 text 𝑃
										567 text 𝑗
										568 text ( 𝑡 ) = 𝑆 ( 𝑡 ,
										569 text 𝑡
										570 text 𝑗
										571 text ) ,
										572 text ∂
										573 text 𝑡
										574 text 𝑃
										575 text 𝑗
										576 text = −
										577 text 𝐿
										578 container
											579 text 𝑤 ( 𝑡 )
										580 text 𝑃
										581 text 𝑗
										582 text ,
										583 text 𝑃
										584 text 𝑗
										585 text (
										586 text 𝑡
										587 text 𝑗
										588 text ) = 𝐼 .
									589 text Choose a fixed small-
									590 text 𝑠
									591 text  threshold so that
									592 container
										593 container
											594 text ∥
											595 text 𝑃
											596 text 𝑗
											597 text ( 𝑡
											598 text )
											599 container
												600 text ± 1
											601 text ∥
											602 container
												603 text 𝐻
												604 text 𝑎
												605 text →
												606 text 𝐻
												607 text 𝑎
											608 text ≤ 2 , 𝑎 = 0 , 1 , 2.
										609 text (7)
									610 heading 2.1 The commutator has only two derivatives of the unknown, Value: 3
										611 text 2.1 The commutator has only two derivatives of the unknown
									612 text Since 
									613 text 𝑃
									614 text  commutes with 
									615 text Δ
									616 text ,
									617 container
										618 container
											619 container
												620 text [ Δ ,
												621 text 𝐿
												622 text 𝐹
												623 text ] 𝑢 = 𝑃 [
											624 container
												625 text ( ( Δ 𝐹 ) ⋅ ∇ ) 𝑢 + 2
												626 text ∑
												627 container
													628 text 𝑎 = 1
												629 text 3
												630 text ( (
												631 text ∂
												632 text 𝑎
												633 text 𝐹 ) ⋅ ∇ )
												634 text ∂
												635 text 𝑎
												636 text 𝑢
											637 container
												638 text + 2
												639 text ∑
												640 container
													641 text 𝑎 = 1
												642 text 3
												643 text ( (
												644 text ∂
												645 text 𝑎
												646 text 𝑢 ) ⋅ ∇ )
												647 text ∂
												648 text 𝑎
												649 text 𝐹 + ( 𝑢 ⋅ ∇ ) Δ 𝐹 ] .
										650 text (8)
									651 text Therefore
									652 container
										653 container
											654 text ∥ [ Δ ,
											655 text 𝐿
											656 text 𝐹
											657 text ] 𝑢
											658 text ∥
											659 text 2
											660 text ≤
											661 text 𝐶
											662 text 𝐹
											663 text ∥ 𝑢
											664 text ∥
											665 container
												666 text 𝐻 2
											667 text .
										668 text (9)
									669 text Each 
									670 container
										671 text 𝐶 𝐹
									672 text  has an explicit rational upper bound obtained directly from the finite Fourier coefficients of 
									673 text 𝐹
									674 text , using derivatives through order three. For example, replace every factor 
									675 container
										676 text 2 𝜋
									677 text  in a Fourier derivative bound by 
									678 text 8
									679 text , and bound the resulting trigonometric polynomial by the sum of the absolute values of its coefficients. No norm oracle is involved.
									680 heading 2.2 Conjugation changes the Laplacian by , Value: 3
										681 text 2.2 Conjugation changes the Laplacian by 
										682 container
											683 text 𝑂 ( 𝑠 )
									684 text On smooth fields,
									685 container
										686 container
											687 text 𝑑
											688 container
												689 text 𝑑 𝑡
											690 text (
											691 text 𝑃
											692 text 𝑗
											693 container
												694 text − 1
											695 text Δ
											696 text 𝑃
											697 text 𝑗
											698 text ) =
											699 text 𝑃
											700 text 𝑗
											701 container
												702 text − 1
											703 text [
											704 text 𝐿
											705 container
												706 text 𝑤 ( 𝑡 )
											707 text , Δ ]
											708 text 𝑃
											709 text 𝑗
											710 text .
										711 text (10)
									712 text Using (6), (7), and (9), integration gives
									713 container
										714 container
											715 text ∥
											716 text 𝑃
											717 text 𝑗
											718 container
												719 text − 1
											720 text Δ
											721 text 𝑃
											722 text 𝑗
											723 text − Δ
											724 text ∥
											725 container
												726 text 𝐻
												727 text 2
												728 text →
												729 text 𝐿
												730 text 2
											731 text ≤
											732 text 𝐶
											733 text Δ
											734 text 𝑠 .
										735 text (11)
									736 text For example, one may use
									737 container
										738 text 𝐶
										739 text Δ
										740 text = 4
										741 text ∑
										742 container
											743 text ℓ = 1
										744 text 𝑚
										745 text ∣
										746 text 𝛼
										747 text ℓ
										748 text ∣
										749 text 𝐶
										750 container
											751 text 𝐹 ℓ
										752 text .
									753 text The identity and estimate extend from smooth fields by density. Shrink the fixed threshold so that
									754 container
										755 container
											756 text 𝐶
											757 text Δ
											758 text 𝑠 ≤
											759 text 1
											760 text 8
											761 text .
										762 text (12)
									763 text For mean-zero fields on the unit torus,
									764 container
										765 container
											766 text − ⟨ Δ 𝑧 , ( 𝐼 − Δ ) 𝑧 ⟩ = ∥ ∇ 𝑧
											767 text ∥
											768 text 2
											769 text 2
											770 text + ∥ Δ 𝑧
											771 text ∥
											772 text 2
											773 text 2
											774 text ≥
											775 text 1
											776 text 2
											777 text ∥ 𝑧
											778 text ∥
											779 container
												780 text 𝐻 2
											781 text 2
											782 text ,
										783 text (13)
									784 text because every nonzero Laplace eigenvalue is at least 
									785 container
										786 text 4
										787 text 𝜋
										788 text 2
										789 text > 1
									790 text . Equations (11)–(13) give the required coercivity. Crucially, they depend on the impulse in 
									791 text one block
									792 text , rather than the strain accumulated over the entire repeated path.
									793 heading 3. A uniform nonlinear estimate throughout the active interval, Value: 2
										794 text 3. A uniform nonlinear estimate throughout the active interval
									795 text Suppose the carrier occupies 
									796 container
										797 text [ 0 , 𝛿 ]
									798 text , starts and ends at zero, and contains 
									799 text 𝑛
									800 text  complete macro-blocks. Its ideal force is
									801 container
										802 text 𝑓
										803 text ∗
										804 text =
										805 text 𝑤
										806 text 𝑡
										807 text + 𝐵 ( 𝑤 , 𝑤 ) − 𝜈 Δ 𝑤 .
									808 text Only one shear is active at a time, so
									809 container
										810 container
											811 text 𝐵 ( 𝑤 , 𝑤 ) = 0 ,
											812 text 𝑓
											813 text ∗
											814 text =
											815 text 𝑤
											816 text 𝑡
											817 text − 𝜈 Δ 𝑤 .
										818 text (14)
									819 text Allow a rational approximation 
									820 text 𝑓
									821 text  with
									822 container
										823 text ∥ 𝑓 −
										824 text 𝑓
										825 text ∗
										826 text ∥
										827 container
											828 text 𝐿
											829 text ∞
											830 text 𝐿
											831 text 2
										832 text ≤ 𝜉 .
									833 text For each actual disturbance 
									834 text ℎ
									835 text , define
									836 container
										837 text 𝑣 = 𝑈 − 𝑤 , 𝑔 = ℎ + ( 𝑓 −
										838 text 𝑓
										839 text ∗
										840 text ) ,
										841 text 𝑎
										842 text ∗
										843 text = 𝜂 + 𝜉 .
									844 text Then
									845 container
										846 container
											847 text 𝑣
											848 text 𝑡
											849 text +
											850 text 𝐿
											851 text 𝑤
											852 text 𝑣 = 𝜈 Δ 𝑣 − 𝐵 ( 𝑣 , 𝑣 ) + 𝑔 .
										853 text (15)
									854 text Assume for the moment that 
									855 container
										856 text 𝑎
										857 text ∗
										858 text ≤ 1
									859 text .
									860 heading 3.1 Reset the coordinates after each block, Value: 3
										861 text 3.1 Reset the coordinates after each block
									862 text Within block 
									863 text 𝑗
									864 text , set
									865 container
										866 text 𝑧 =
										867 text 𝑃
										868 text 𝑗
										869 container
											870 text − 1
										871 text 𝑣 .
									872 text The transformed equation is
									873 container
										874 container
											875 text 𝑧
											876 text 𝑡
											877 text = 𝜈
											878 text 𝑃
											879 text 𝑗
											880 container
												881 text − 1
											882 text Δ
											883 text 𝑃
											884 text 𝑗
											885 text 𝑧 −
											886 text 𝑃
											887 text 𝑗
											888 container
												889 text − 1
											890 text 𝐵 (
											891 text 𝑃
											892 text 𝑗
											893 text 𝑧 ,
											894 text 𝑃
											895 text 𝑗
											896 text 𝑧 ) +
											897 text 𝑃
											898 text 𝑗
											899 container
												900 text − 1
											901 text 𝑔 .
										902 text (16)
									903 text At the next block boundary the new propagator starts at the identity. Accordingly,
									904 container
										905 container
											906 text 𝑧 (
											907 text 𝑡
											908 container
												909 text 𝑗 + 1
											910 text + ) = 𝑊 ( 𝑠 ) 𝑧 (
											911 text 𝑡
											912 container
												913 text 𝑗 + 1
											914 text − ) .
										915 text (17)
									916 text This reset is an operation in the proof. The physical velocity remains continuous, and the prescribed force is unaffected.
									917 heading 3.2 An explicit nonlinear constant, Value: 3
										918 text 3.2 An explicit nonlinear constant
									919 text An elementary Fourier estimate on the unit torus gives
									920 container
										921 container
											922 text ∥ 𝑢
											923 text ∥
											924 text ∞
											925 text ≤ 16 ∥ 𝑢
											926 text ∥
											927 container
												928 text 𝐻 1
											929 container
												930 text 1 / 2
											931 text ∥ 𝑢
											932 text ∥
											933 container
												934 text 𝐻 2
											935 container
												936 text 1 / 2
											937 text .
										938 text (18)
									939 text Here is one way to make the constant effective. The shell
									940 container
										941 text { 𝑘 ∈
										942 text 𝑍
										943 text 3
										944 text : ∣ 𝑘
										945 text ∣
										946 text ∞
										947 text = 𝑗 }
									948 text contains 
									949 container
										950 text 24
										951 text 𝑗
										952 text 2
										953 text + 2 ≤ 26
										954 text 𝑗
										955 text 2
									956 text  points. Splitting the Fourier sum at
									957 container
										958 text 𝑁 =
										959 text ⌈
										960 container
											961 text ∥
											962 text 𝑢
											963 container
												964 text ∥
												965 text 𝐻
												966 text 2
											967 text ∥
											968 text 𝑢
											969 container
												970 text ∥
												971 text 𝐻
												972 text 1
										973 text ⌉
									974 text bounds the low-frequency reciprocal 
									975 container
										976 text 𝐻 1
									977 text -weight sum by 
									978 container
										979 text 26 𝑁
									980 text , and the high-frequency reciprocal 
									981 container
										982 text 𝐻 2
									983 text -weight sum by 
									984 container
										985 text 26 / 𝑁
									986 text . Cauchy–Schwarz then gives (18). The zero field is immediate. Consequently,
									987 container
										988 container
											989 text ∥ 𝐵 ( 𝑢 , 𝑢 )
											990 text ∥
											991 text 2
											992 text ≤ 16 ∥ 𝑢
											993 text ∥
											994 container
												995 text 𝐻 1
											996 container
												997 text 3 / 2
											998 text ∥ 𝑢
											999 text ∥
											1000 container
												1001 text 𝐻 2
											1002 container
												1003 text 1 / 2
											1004 text .
										1005 text (19)
									1006 text Put
									1007 container
										1008 text 𝐸 = ∥ 𝑧
										1009 text ∥
										1010 container
											1011 text 𝐻 1
										1012 text 2
										1013 text , 𝑍 = ∥ 𝑧
										1014 text ∥
										1015 container
											1016 text 𝐻 2
										1017 text .
									1018 text By (7) and (19),
									1019 container
										1020 container
											1021 text ∥
											1022 text 𝑃
											1023 text 𝑗
											1024 container
												1025 text − 1
											1026 text 𝐵 (
											1027 text 𝑃
											1028 text 𝑗
											1029 text 𝑧 ,
											1030 text 𝑃
											1031 text 𝑗
											1032 text 𝑧 )
											1033 text ∥
											1034 text 2
											1035 text ≤ 128
											1036 text 𝐸
											1037 container
												1038 text 3 / 4
											1039 text 𝑍
											1040 container
												1041 text 1 / 2
											1042 text .
										1043 text (20)
									1044 heading 3.3 The energy inequality, Value: 3
										1045 text 3.3 The energy inequality
									1046 text Pair (16) with 
									1047 container
										1048 text ( 𝐼 − Δ ) 𝑧
									1049 text . Equations (11)–(13) imply
									1050 container
										1051 text 1
										1052 text 2
										1053 text 𝐸
										1054 text ′
										1055 text ≤ −
										1056 text 𝜈
										1057 text 2
										1058 text 𝑍
										1059 text 2
										1060 text +
										1061 text 𝜈
										1062 text 8
										1063 text 𝑍
										1064 text 2
										1065 text + 128
										1066 text 𝐸
										1067 container
											1068 text 3 / 4
										1069 text 𝑍
										1070 container
											1071 text 3 / 2
										1072 text + 2
										1073 text 𝑎
										1074 text ∗
										1075 text 𝑍 .
									1076 text Use
									1077 container
										1078 text 128
										1079 text 𝐸
										1080 container
											1081 text 3 / 4
										1082 text 𝑍
										1083 container
											1084 text 3 / 2
										1085 text ≤
										1086 text 𝜈
										1087 text 8
										1088 text 𝑍
										1089 text 2
										1090 text + 54 ⋅
										1091 text 128
										1092 text 4
										1093 text 𝜈
										1094 container
											1095 text − 3
										1096 text 𝐸
										1097 text 3
										1098 text ,
									1099 text and
									1100 container
										1101 text 2
										1102 text 𝑎
										1103 text ∗
										1104 text 𝑍 ≤
										1105 text 𝜈
										1106 text 8
										1107 text 𝑍
										1108 text 2
										1109 text + 8
										1110 text 𝜈
										1111 container
											1112 text − 1
										1113 text 𝑎
										1114 text ∗
										1115 text 2
										1116 text .
									1117 text Thus, with the explicit integer
									1118 container
										1119 text 𝐶
										1120 text 𝐸
										1121 text = 108 ⋅
										1122 text 128
										1123 text 4
										1124 text ,
									1125 text we have
									1126 container
										1127 container
											1128 text 𝐸
											1129 text ′
											1130 text +
											1131 text 𝜈
											1132 text 4
											1133 text 𝑍
											1134 text 2
											1135 text ≤
											1136 text 𝐶
											1137 text 𝐸
											1138 text 𝜈
											1139 container
												1140 text − 3
											1141 text 𝐸
											1142 text 3
											1143 text +
											1144 text 𝐶
											1145 text 𝐸
											1146 text 𝜈
											1147 container
												1148 text − 1
											1149 text 𝑎
											1150 text ∗
											1151 text 2
											1152 text .
										1153 text (21)
									1154 text There is no carrier amplitude, pulse frequency, 
									1155 container
										1156 text 𝑛 𝑠
									1157 text , or accumulated-strain exponential in this inequality.
									1158 heading 3.4 Accounting for every reset, Value: 3
										1159 text 3.4 Accounting for every reset
									1160 text By (4) and (17),
									1161 container
										1162 text 𝐸 (
										1163 text 𝑡
										1164 container
											1165 text 𝑗 + 1
										1166 text + ) ≤ 𝑞 𝐸 (
										1167 text 𝑡
										1168 container
											1169 text 𝑗 + 1
										1170 text − ) , 𝑞 = ( 1 +
										1171 text 𝑐
										1172 text 1
										1173 text 𝑠
										1174 text 5
										1175 text )
										1176 text 2
										1177 text .
									1178 text Require
									1179 container
										1180 container
											1181 text 𝑞
											1182 text 𝑛
											1183 text ≤ 2.
										1184 text (22)
									1185 text On block 
									1186 text 𝑗
									1187 text , define
									1188 container
										1189 text 𝐸 =
										1190 text 𝑞
										1191 container
											1192 text − 𝑗
										1193 text 𝐸 .
									1194 text It has no upward jump at a reset, and (21) gives
									1195 container
										1196 container
											1197 text 𝐸
											1198 text ′
											1199 text +
											1200 text 𝜈
											1201 text 4
											1202 text 𝑞
											1203 container
												1204 text − 𝑗
											1205 text 𝑍
											1206 text 2
											1207 text ≤ 4
											1208 text 𝐶
											1209 text 𝐸
											1210 text 𝜈
											1211 container
												1212 text − 3
											1213 text 𝐸
											1214 text 3
											1215 text +
											1216 text 𝐶
											1217 text 𝐸
											1218 text 𝜈
											1219 container
												1220 text − 1
											1221 text 𝑎
											1222 text ∗
											1223 text 2
											1224 text .
										1225 text (23)
									1226 text Since 
									1227 container
										1228 text 𝐸 ( 0 ) ≤
										1229 text 𝑀
										1230 text 2
									1231 text , the bootstrap
									1232 container
										1233 text 𝐸 ≤ 2
										1234 text 𝑀
										1235 text 2
									1236 text closes provided
									1237 container
										1238 container
											1239 text 𝛿 ≤
											1240 container
												1241 text 𝜈 3
											1242 container
												1243 text 128
												1244 text 𝐶
												1245 text 𝐸
												1246 text 𝑀
												1247 text 4
											1248 text .
										1249 text (24)
									1250 text Indeed, while the bootstrap holds, the right-hand side of (23) is at most
									1251 container
										1252 text 33
										1253 text 𝐶
										1254 text 𝐸
										1255 text 𝜈
										1256 container
											1257 text − 3
										1258 text 𝑀
										1259 text 6
										1260 text ,
									1261 text using 
									1262 container
										1263 text 𝑎
										1264 text ∗
										1265 text ≤ 1
									1266 text , 
									1267 container
										1268 text 𝑀 ≥ 1
									1269 text , and 
									1270 container
										1271 text 𝜈 ≤ 1
									1272 text . Over (24), this increases the weighted energy by less than 
									1273 container
										1274 text 𝑀 2
									1275 text . Integrating (23), and using 
									1276 container
										1277 text 𝑞
										1278 container
											1279 text − 𝑗
										1280 text ≥ 1 / 2
									1281 text , gives
									1282 container
										1283 text 𝜈
										1284 text ∫
										1285 text 0
										1286 text 𝛿
										1287 text 𝑍
										1288 text 2
										1289 text 𝑑 𝑡 ≤ 16
										1290 text 𝑀
										1291 text 2
										1292 text .
									1293 text Returning to 
									1294 container
										1295 text 𝑣 =
										1296 text 𝑃
										1297 text 𝑗
										1298 text 𝑧
									1299 text ,
									1300 container
										1301 container
											1302 container
												1303 text sup ⁡
											1304 container
												1305 text 0 ≤ 𝑡 ≤ 𝛿
											1306 text ∥ 𝑣 ( 𝑡 )
											1307 text ∥
											1308 container
												1309 text 𝐻 1
											1310 text ≤ 4 𝑀 , 𝜈
											1311 text ∫
											1312 text 0
											1313 text 𝛿
											1314 text ∥ 𝑣 ( 𝑡 )
											1315 text ∥
											1316 container
												1317 text 𝐻 2
											1318 text 2
											1319 text 𝑑 𝑡 ≤ 64
											1320 text 𝑀
											1321 text 2
											1322 text .
										1323 text (25)
									1324 heading 3.5 Why this covers every Leray–Hopf realization, Value: 3
										1325 text 3.5 Why this covers every Leray–Hopf realization
									1326 text For each fixed compiler output, 
									1327 text 𝑤
									1328 text  is continuous, piecewise polynomial in time, and smooth in space. The actual force belongs to 
									1329 container
										1330 text 𝐿
										1331 text 𝑡
										1332 text ∞
										1333 text 𝐿
										1334 text 𝑥
										1335 text 2
									1336 text . Local 
									1337 container
										1338 text 𝐻 1
									1339 text  strong existence therefore applies; the estimate (25) prevents loss of 
									1340 container
										1341 text 𝐻 1
									1342 text  regularity before 
									1343 text 𝛿
									1344 text , so the solution continues throughout the active interval. These are the usual local strong-solution and continuation mechanisms for three-dimensional Navier–Stokes. 
									1345 link (collapsed) Value: virtualmath1.stanford.edu/~ryzhik/notes-256B-24.pdf?utm_source=chatgpt.com, Secondary Actions: Expand, Description: virtualmath1.stanford.edu: https://virtualmath1.stanford.edu/~ryzhik/notes-256B-24.pdf, https://virtualmath1.stanford.edu/~ryzhik/notes-256B-24.pdf?utm_source=chatgpt.com, 1 additional source
									1346 text For each actual 
									1347 text ℎ
									1348 text , this produces
									1349 container
										1350 text 𝑈
										1351 text ∗
										1352 text = 𝑤 + 𝑣 ∈
										1353 text 𝐿
										1354 text ∞
										1355 text ( 0 , 𝛿 ;
										1356 text 𝐻
										1357 text 1
										1358 text ) ∩
										1359 text 𝐿
										1360 text 2
										1361 text ( 0 , 𝛿 ;
										1362 text 𝐻
										1363 text 2
										1364 text ) .
									1365 text Weak–strong uniqueness identifies every corresponding Leray–Hopf solution with 
									1366 container
										1367 text 𝑈 ∗
									1368 text  on that interval. The uniqueness argument may contain a very large finite Grönwall factor. Its initial discrepancy is exactly zero. 
									1369 text No disturbance tolerance or physical resource is chosen using that factor.
									1370 text  Quantitative robustness comes from (21)–(25), applied separately to each actual disturbance.
									1371 heading 4. The resulting endpoint comparison is polynomial, Value: 2
										1372 text 4. The resulting endpoint comparison is polynomial
									1373 text Arrange also that (5) gives
									1374 container
										1375 container
											1376 container
												1377 text sup ⁡
											1378 container
												1379 text 0 ≤ 𝑟 ≤ 𝑡 ≤ 𝛿
											1380 text ∥ 𝑆 ( 𝑡 , 𝑟 )
											1381 text ∥
											1382 container
												1383 text 2 → 2
											1384 text ≤ 2.
										1385 text (26)
									1386 text Equation (15) has the 
									1387 container
										1388 text 𝐿 2
									1389 text  variation-of-constants formula
									1390 container
										1391 container
											1392 text 𝑣 ( 𝛿 ) − 𝑊 ( 𝑠
											1393 text )
											1394 text 𝑛
											1395 text 𝑈
											1396 text 0
											1397 text =
											1398 text ∫
											1399 text 0
											1400 text 𝛿
											1401 text 𝑆 ( 𝛿 , 𝑡 ) [ 𝜈 Δ 𝑣 − 𝐵 ( 𝑣 , 𝑣 ) + 𝑔 ] 𝑑 𝑡 .
										1402 text (27)
									1403 text The residual is in 
									1404 container
										1405 text 𝐿
										1406 text 𝑡
										1407 text 1
										1408 text 𝐿
										1409 text 𝑥
										1410 text 2
									1411 text  by (25), so this is a legitimate strong-solution formula. First,
									1412 container
										1413 text 𝜈
										1414 text ∫
										1415 text 0
										1416 text 𝛿
										1417 text ∥ Δ 𝑣
										1418 text ∥
										1419 text 2
										1420 text 𝑑 𝑡 ≤ 8 𝑀
										1421 container
											1422 text 𝜈 𝛿
										1423 text .
									1424 text Second, by (19), (25), and Hölder,
									1425 container
										1426 container
											1427 text ∫
											1428 text 0
											1429 text 𝛿
											1430 text ∥ 𝐵 ( 𝑣 , 𝑣 )
											1431 text ∥
											1432 text 2
											1433 text 𝑑 𝑡
										1434 container
											1435 text ≤ 16 ( 4 𝑀
											1436 text )
											1437 container
												1438 text 3 / 2
											1439 text 𝛿
											1440 container
												1441 text 3 / 4
											1442 container
												1443 text (
												1444 text ∫
												1445 text 0
												1446 text 𝛿
												1447 text ∥ 𝑣
												1448 text ∥
												1449 container
													1450 text 𝐻 2
												1451 text 2
												1452 text 𝑑 𝑡 )
											1453 container
												1454 text 1 / 4
										1455 container
											1456 text ≤ 384
											1457 text 𝑀
											1458 text 2
											1459 text 𝛿
											1460 container
												1461 text 3 / 4
											1462 text 𝜈
											1463 container
												1464 text − 1 / 4
											1465 text .
									1466 text Multiplying by the forward-propagator bound 
									1467 text 2
									1468 text  yields
									1469 container
										1470 container
											1471 text ∥ 𝑈 ( 𝛿 ) − 𝑊 ( 𝑠
											1472 text )
											1473 text 𝑛
											1474 text 𝑈
											1475 text 0
											1476 text ∥
											1477 text 2
											1478 text ≤ 16 𝑀
											1479 container
												1480 text 𝜈 𝛿
											1481 text + 768
											1482 text 𝑀
											1483 text 2
											1484 text 𝛿
											1485 container
												1486 text 3 / 4
											1487 text 𝜈
											1488 container
												1489 text − 1 / 4
											1490 text + 2
											1491 text 𝑎
											1492 text ∗
											1493 text 𝛿 .
										1494 text (28)
									1495 text Here 
									1496 container
										1497 text 𝑤 ( 𝛿 ) = 0
									1498 text , so the left side concerns 
									1499 text total velocity
									1500 text  at the end of the active interval. This is the quantitative replacement for the supplied estimate containing 
									1501 container
										1502 text 𝑒 𝐾
									1503 text .
									1504 heading 5. Explicit fixed constants and variable parameter choices, Value: 2
										1505 text 5. Explicit fixed constants and variable parameter choices
									1506 heading 5.1 Finish the fixed precomputation, Value: 3
										1507 text 5.1 Finish the fixed precomputation
									1508 text Choose a positive rational 
									1509 text 𝜎
									1510 text  lying in the common admissible range of the supplied estimates and satisfying
									1511 container
										1512 container
											1513 text 𝜎 ≤
											1514 text 1
											1515 container
												1516 text 16 ( 1 +
												1517 text 𝑏
												1518 text 0
												1519 text +
												1520 text 𝑏
												1521 text 1
												1522 text +
												1523 text 𝑏
												1524 text 2
												1525 text +
												1526 text 𝐶
												1527 text Δ
												1528 text )
											1529 text .
										1530 text (29)
									1531 text This ensures all the partial-propagator and commutator requirements above. Choose the integer
									1532 container
										1533 text 𝐶
										1534 text 𝐷
										1535 text = 1 + ⌈
										1536 text 𝑐
										1537 container
											1538 text − 1
										1539 text ⌉ .
									1540 text The Fourier multiplier estimate gives
									1541 container
										1542 container
											1543 text ∥
											1544 text 𝑒
											1545 container
												1546 text 𝑇 𝐷
											1547 text 𝐽
											1548 text ∥
											1549 container
												1550 text 2 → 2
											1551 text ≤
											1552 text 𝐶
											1553 text 𝐷
											1554 text 𝑇
											1555 container
												1556 text − 1 / 2
											1557 text .
										1558 text (30)
									1559 text Indeed, putting 
									1560 container
										1561 text 𝑦 = 1 + ∣ 𝑘
										1562 text ∣
										1563 text 2
									1564 text ,
									1565 container
										1566 container
											1567 text 𝑒
											1568 text −
											1569 text 𝑐
											1570 text 𝑇
											1571 text /
											1572 text 𝑦
										1573 container
											1574 text 1 + 4
											1575 text 𝜋
											1576 text 2
											1577 text ∣ 𝑘
											1578 text ∣
											1579 text 2
										1580 text ≤
										1581 text 𝑦
										1582 container
											1583 text − 1 / 2
										1584 text 𝑒
										1585 container
											1586 text − 𝑐 𝑇 / 𝑦
										1587 text ,
									1588 text whose supremum over 
									1589 container
										1590 text 𝑦 > 0
									1591 text  is 
									1592 container
										1593 text ( 2 𝑒 𝑐 𝑇
										1594 text )
										1595 container
											1596 text − 1 / 2
									1597 text . Now compute a fixed integer 
									1598 container
										1599 text 𝐵 ∗
									1600 text  satisfying
									1601 container
										1602 container
											1603 text 𝐵
											1604 text ∗
											1605 text ≥ max ⁡
											1606 text {
											1607 text 2
											1608 text ,
											1609 container
												1610 text 𝜎
												1611 text −
												1612 text 1
											1613 text ,
											1614 text 16
											1615 container
												1616 text 𝐶 0
											1617 text ,
											1618 text 4
											1619 container
												1620 text 𝑐 1
											1621 text ,
											1622 text 128
											1623 container
												1624 text 𝐶 𝐸
											1625 text ,
											1626 text 64
											1627 container
												1628 text 𝐶 𝐷 2
											1629 text ,
											1630 text (
											1631 text 12
											1632 text ⋅
											1633 text 1024
											1634 container
												1635 text ) 2
											1636 text }
											1637 text .
										1638 text (31)
									1639 text A ceiling of the displayed maximum suffices. Everything in (29)–(31) is fixed, rationally computable, and independent of the variable inputs.
									1640 heading 5.2 Online parameters, Value: 3
										1641 text 5.2 Online parameters
									1642 text For an input 
									1643 container
										1644 text ( 𝑀 , 𝜈 , 𝜏 , 𝜖 )
									1645 text , compute the integer
									1646 container
										1647 container
											1648 text 𝜌 = 2 + ⌈ 𝑀 ⌉ + ⌈
											1649 text 𝜈
											1650 container
												1651 text − 1
											1652 text ⌉ + ⌈
											1653 text 𝜏
											1654 container
												1655 text − 1
											1656 text ⌉ + ⌈
											1657 text 𝜖
											1658 container
												1659 text − 1
											1660 text ⌉ .
										1661 text (32)
									1662 text Then
									1663 container
										1664 container
											1665 text 𝑅 ≤ 𝜌 < 𝑅 + 4 ≤ 2 𝑅 ,
										1666 text (33)
									1667 text and
									1668 container
										1669 text 𝑀 ≤ 𝜌 ,
										1670 text 𝜈
										1671 container
											1672 text − 1
										1673 text ≤ 𝜌 ,
										1674 text 𝜏
										1675 container
											1676 text − 1
										1677 text ≤ 𝜌 ,
										1678 text 𝜖
										1679 container
											1680 text − 1
										1681 text ≤ 𝜌 .
									1682 text Set
									1683 container
										1684 container
											1685 text 𝑇
											1686 container
												1687 text =
												1688 text 𝐵
												1689 text ∗
												1690 text 𝜌
												1691 text 4
												1692 text ,
											1693 text 𝑠
											1694 container
												1695 text =
												1696 text 1
												1697 container
													1698 text 𝐵
													1699 text ∗
													1700 text 2
													1701 text 𝜌
													1702 text 6
												1703 text ,
											1704 text 𝑛
											1705 container
												1706 text =
												1707 text 𝐵
												1708 text ∗
												1709 text 9
												1710 text 𝜌
												1711 text 28
												1712 text ,
											1713 text 𝛿
											1714 container
												1715 text =
												1716 text 1
												1717 container
													1718 text 𝐵
													1719 text ∗
													1720 text 𝜌
													1721 text 8
												1722 text ,
											1723 text 𝜂
											1724 container
												1725 text =
												1726 text 1
												1727 container
													1728 text 16 𝜌
												1729 text .
										1730 text (34)
									1731 text All these quantities are rational, and 
									1732 text 𝑛
									1733 text  is an integer. In particular,
									1734 container
										1735 container
											1736 text 𝑛
											1737 text 𝑠
											1738 text 4
											1739 text = 𝑇 , 𝑛
											1740 text 𝑠
											1741 text 5
											1742 text =
											1743 text 1
											1744 container
												1745 text 𝐵
												1746 text ∗
												1747 text 𝜌
												1748 text 2
											1749 text .
										1750 text (35)
									1751 heading 5.3 Verification of the stability requirements, Value: 3
										1752 text 5.3 Verification of the stability requirements
									1753 text By (29), (31), and (34), 
									1754 container
										1755 text 𝑠 ≤ 𝜎
									1756 text . Moreover,
									1757 container
										1758 text 𝑞
										1759 text 𝑛
										1760 text ≤ exp ⁡ ( 2
										1761 text 𝑐
										1762 text 1
										1763 text 𝑛
										1764 text 𝑠
										1765 text 5
										1766 text ) ≤ exp ⁡ ( 2
										1767 text 𝑐
										1768 text 1
										1769 text /
										1770 text 𝐵
										1771 text ∗
										1772 text ) < 2 ,
									1773 text and
									1774 container
										1775 text exp ⁡ ( 2
										1776 text 𝑏
										1777 text 0
										1778 text 𝑠 +
										1779 text 𝐶
										1780 text 0
										1781 text 𝑛
										1782 text 𝑠
										1783 text 5
										1784 text ) < 2.
									1785 text Thus (22) and (26) hold. Also,
									1786 container
										1787 text 𝜈
										1788 text 3
										1789 text 𝑀
										1790 container
											1791 text − 4
										1792 text ≥
										1793 text 𝜌
										1794 container
											1795 text − 7
										1796 text .
									1797 text Since 
									1798 container
										1799 text 𝐵
										1800 text ∗
										1801 text ≥ 128
										1802 text 𝐶
										1803 text 𝐸
									1804 text ,
									1805 container
										1806 text 𝛿 =
										1807 text 1
										1808 container
											1809 text 𝐵
											1810 text ∗
											1811 text 𝜌
											1812 text 8
										1813 text ≤
										1814 container
											1815 text 𝜈 3
										1816 container
											1817 text 128
											1818 text 𝐶
											1819 text 𝐸
											1820 text 𝑀
											1821 text 4
										1822 text .
									1823 text Finally, 
									1824 container
										1825 text 𝛿 ≤ 𝜏 / 2
									1826 text .
									1827 heading 5.4 Verification of the linear target, Value: 3
										1828 text 5.4 Verification of the linear target
									1829 text By (30),
									1830 container
										1831 container
											1832 text ∥
											1833 text 𝑒
											1834 container
												1835 text 𝑇 𝐷
											1836 text 𝑈
											1837 text 0
											1838 text ∥
											1839 text 2
											1840 text ≤ 𝑀
											1841 text 𝐶
											1842 text 𝐷
											1843 text 𝑇
											1844 container
												1845 text − 1 / 2
											1846 text ≤
											1847 container
												1848 text 𝐶 𝐷
											1849 container
												1850 text 𝐵 ∗
											1851 text 𝜌
											1852 container
												1853 text − 1
											1854 text ≤
											1855 text 𝜖
											1856 text 8
											1857 text .
										1858 text (36)
									1859 text The supplied word error gives
									1860 container
										1861 container
											1862 container
												1863 text ∥ ( 𝑊 ( 𝑠
												1864 text )
												1865 text 𝑛
												1866 text −
												1867 text 𝑒
												1868 container
													1869 text 𝑇 𝐷
												1870 text )
												1871 text 𝑈
												1872 text 0
												1873 text ∥
												1874 text 2
											1875 container
												1876 text ≤ 𝑀
												1877 text 𝐶
												1878 text 0
												1879 text 𝑛
												1880 text 𝑠
												1881 text 5
												1882 text 𝑒
												1883 container
													1884 text 𝐶
													1885 text 0
													1886 text 𝑛
													1887 text 𝑠
													1888 text 5
											1889 container
												1890 text ≤
												1891 container
													1892 text 2
													1893 text 𝐶
													1894 text 0
												1895 container
													1896 text 𝐵 ∗
												1897 text 𝜌
												1898 container
													1899 text − 1
												1900 text ≤
												1901 text 𝜖
												1902 text 8
												1903 text .
										1904 text (37)
									1905 text Therefore
									1906 container
										1907 container
											1908 text ∥ 𝑊 ( 𝑠
											1909 text )
											1910 text 𝑛
											1911 text 𝑈
											1912 text 0
											1913 text ∥
											1914 text 2
											1915 text ≤ 𝜖 / 4.
										1916 text (38)
									1917 heading 5.5 Verification of the nonlinear error, Value: 3
										1918 text 5.5 Verification of the nonlinear error
									1919 text Use 
									1920 container
										1921 text 𝑎
										1922 text ∗
										1923 text ≤ 1
									1924 text  in (28). Its right-hand side is at most
									1925 container
										1926 container
											1927 text 16
											1928 text 𝐵
											1929 text ∗
											1930 container
												1931 text − 1 / 2
											1932 text 𝜌
											1933 container
												1934 text − 3
											1935 text + 768
											1936 text 𝐵
											1937 text ∗
											1938 container
												1939 text − 3 / 4
											1940 text 𝜌
											1941 container
												1942 text − 15 / 4
											1943 text + 2
											1944 text 𝐵
											1945 text ∗
											1946 container
												1947 text − 1
											1948 text 𝜌
											1949 container
												1950 text − 8
											1951 text .
										1952 text (39)
									1953 text Since 
									1954 container
										1955 text 𝜖 ≥
										1956 text 𝜌
										1957 container
											1958 text − 1
									1959 text , the choice
									1960 container
										1961 text 𝐵
										1962 text ∗
										1963 text ≥ ( 12 ⋅ 1024
										1964 text )
										1965 text 2
									1966 text makes (39) at most 
									1967 container
										1968 text 𝜖 / 4
									1969 text . Combining this with (38),
									1970 container
										1971 container
											1972 text ∥ 𝑈 ( 𝛿 )
											1973 text ∥
											1974 text 2
											1975 text ≤ 𝜖 / 2.
										1976 text (40)
									1977 heading 6. The actual rational piecewise-polynomial force, Value: 2
										1978 text 6. The actual rational piecewise-polynomial force
									1979 text It remains to implement the carrier and approximate its viscosity term using rational coefficients.
									1980 heading 6.1 Quadratic pulses, Value: 3
										1981 text 6.1 Quadratic pulses
									1982 text There are 
									1983 container
										1984 text 𝑚 𝑛
									1985 text  pulses. Give each pulse the rational duration
									1986 container
										1987 container
											1988 text 𝑑 =
											1989 text 𝛿
											1990 container
												1991 text 𝑚 𝑛
											1992 text =
											1993 text 1
											1994 container
												1995 text 𝑚
												1996 text 𝐵
												1997 text ∗
												1998 text 10
												1999 text 𝜌
												2000 text 36
											2001 text .
										2002 text (41)
									2003 text Let
									2004 container
										2005 text 𝑞 ( 𝑧 ) = 6 𝑧 ( 1 − 𝑧 ) ,
										2006 text ∫
										2007 text 0
										2008 text 1
										2009 text 𝑞 ( 𝑧 ) 𝑑 𝑧 = 1.
									2010 text For pulse 
									2011 text 𝑖
									2012 text , put
									2013 container
										2014 text 𝑡
										2015 text 𝑖
										2016 text = 𝑖 𝑑 , ℓ = 1 + ( 𝑖
										2017 container
											2018 text m o d
										2019 text 𝑚 ) , 𝜁 =
										2020 container
											2021 text 𝑡 −
											2022 text 𝑡
											2023 text 𝑖
										2024 text 𝑑
										2025 text .
									2026 text Define
									2027 container
										2028 container
											2029 text 𝑤 ( 𝑡 , 𝑥 ) =
											2030 container
												2031 text 𝛼
												2032 text ℓ
												2033 text 𝑠
											2034 text 𝑑
											2035 text 𝑞 ( 𝜁 )
											2036 text 𝐺
											2037 container
												2038 text ȷ ℓ
											2039 text ( 𝑥 ) ,
											2040 text 𝑡
											2041 text 𝑖
											2042 text ≤ 𝑡 ≤
											2043 text 𝑡
											2044 container
												2045 text 𝑖 + 1
											2046 text .
										2047 text (42)
									2048 text Its signed impulse is precisely 
									2049 container
										2050 text 𝛼
										2051 text ℓ
										2052 text 𝑠
									2053 text . Hence the inviscid endpoint operator is exactly 
									2054 container
										2055 text 𝑊 ( 𝑠
										2056 text )
										2057 text 𝑛
									2058 text . The carrier vanishes at every pulse boundary because 
									2059 container
										2060 text 𝑞 ( 0 ) = 𝑞 ( 1 ) = 0
									2061 text . It is continuous throughout, and its time derivative is bounded and piecewise polynomial. This produces ordinary forcing with no distributional impulses.
									2062 heading 6.2 Rational approximation of the Laplacian eigenvalues, Value: 3
										2063 text 6.2 Rational approximation of the Laplacian eigenvalues
									2064 text Each selected shear is a single Fourier mode with an integer wavevector 
									2065 container
										2066 text 𝑘 𝑗
									2067 text , so
									2068 container
										2069 text − Δ
										2070 text 𝐺
										2071 text 𝑗
										2072 text =
										2073 text 𝜅
										2074 text 2
										2075 text ∣
										2076 text 𝑘
										2077 text 𝑗
										2078 text ∣
										2079 text 2
										2080 text 𝐺
										2081 text 𝑗
										2082 text , 𝜅 = 2 𝜋 .
									2083 text The ideal coefficient on a pulse would be
									2084 container
										2085 container
											2086 container
												2087 text 𝛼
												2088 text ℓ
												2089 text 𝑠
											2090 container
												2091 text 𝑑 2
											2092 text 𝑞
											2093 text ′
											2094 text ( 𝜁 ) + 𝜈
											2095 text 𝜅
											2096 text 2
											2097 text ∣
											2098 text 𝑘
											2099 container
												2100 text ȷ ℓ
											2101 text ∣
											2102 text 2
											2103 container
												2104 text 𝛼
												2105 text ℓ
												2106 text 𝑠
											2107 text 𝑑
											2108 text 𝑞 ( 𝜁 ) .
										2109 text (43)
									2110 text Compute a rational dyadic number 
									2111 text 𝜃
									2112 text  approximating 
									2113 container
										2114 text 𝜅 2
									2115 text , and output
									2116 container
										2117 container
											2118 text 𝑐
											2119 container
												2120 text ȷ ℓ
											2121 text ( 𝑡 ) =
											2122 container
												2123 text 𝛼
												2124 text ℓ
												2125 text 𝑠
											2126 container
												2127 text 𝑑 2
											2128 text 𝑞
											2129 text ′
											2130 text ( 𝜁 ) + 𝜈 𝜃 ∣
											2131 text 𝑘
											2132 container
												2133 text ȷ ℓ
											2134 text ∣
											2135 text 2
											2136 container
												2137 text 𝛼
												2138 text ℓ
												2139 text 𝑠
											2140 text 𝑑
											2141 text 𝑞 ( 𝜁 ) .
										2142 text (44)
									2143 text All other coefficients are zero on that pulse. The compiler expands (44) into an ordinary polynomial in 
									2144 text 𝑡
									2145 text . Its degree is at most two, with rational coefficients. For a completely explicit error rule, precompute rational bounds
									2146 container
										2147 text 𝐻
										2148 text 0
										2149 text ≥
										2150 container
											2151 text max ⁡
										2152 text 𝑗
										2153 text ∥
										2154 text 𝐺
										2155 text 𝑗
										2156 text ∥
										2157 text 2
										2158 text ,
										2159 text 𝐾
										2160 text 2
										2161 text ≥
										2162 container
											2163 text max ⁡
										2164 text 𝑗
										2165 text ∣
										2166 text 𝑘
										2167 text 𝑗
										2168 text ∣
										2169 text 2
										2170 text ,
										2171 text 𝛼
										2172 text ∗
										2173 text ≥
										2174 container
											2175 text max ⁡
										2176 text ℓ
										2177 text ∣
										2178 text 𝛼
										2179 text ℓ
										2180 text ∣ ,
									2181 text all at least one, and put
									2182 container
										2183 text 𝐻
										2184 text 𝑤
										2185 text = 2
										2186 text 𝛼
										2187 text ∗
										2188 text 𝑠 / 𝑑 .
									2189 text It suffices to require
									2190 container
										2191 container
											2192 text ∣ 𝜃 −
											2193 text 𝜅
											2194 text 2
											2195 text ∣ ≤
											2196 text 𝜂
											2197 container
												2198 text 1 +
												2199 text 𝐾
												2200 text 2
												2201 text 𝐻
												2202 text 0
												2203 text 𝐻
												2204 text 𝑤
											2205 text .
										2206 text (45)
									2207 text Since 
									2208 container
										2209 text 𝜈 ≤ 1
									2210 text , this guarantees
									2211 container
										2212 container
											2213 text ∥ 𝑓 −
											2214 text 𝑓
											2215 text ∗
											2216 text ∥
											2217 container
												2218 text 𝐿
												2219 text ∞
												2220 text 𝐿
												2221 text 2
											2222 text ≤ 𝜂 .
										2223 text (46)
									2224 text Thus we take
									2225 container
										2226 text 𝜉 = 𝜂 ,
										2227 text 𝑎
										2228 text ∗
										2229 text ≤ 2 𝜂 =
										2230 text 1
										2231 container
											2232 text 8 𝜌
										2233 text < 1 ,
									2234 text as required above. One deterministic rational implementation of (45) uses
									2235 container
										2236 text 𝜋 = 16 arctan ⁡ ( 1 / 5 ) − 4 arctan ⁡ ( 1 / 239 )
									2237 text with the alternating power series and its explicit remainder bounds, followed by rational squaring and dyadic rounding. The required precision is 
									2238 container
										2239 text 𝑂 ( log ⁡ 𝜌 )
									2240 text , with a fixed additive constant from the precomputation.
									2241 heading 6.3 Switch off the control, Value: 3
										2242 text 6.3 Switch off the control
									2243 text Set every 
									2244 container
										2245 text 𝑐
										2246 text 𝑗
										2247 text = 0
									2248 text  on 
									2249 container
										2250 text ( 𝛿 , 𝜏 ]
									2251 text . For every Leray–Hopf continuation, the energy inequality gives
									2252 container
										2253 container
											2254 text ∥ 𝑈 ( 𝑡 )
											2255 text ∥
											2256 text 2
											2257 text ≤ ∥ 𝑈 ( 𝛿 )
											2258 text ∥
											2259 text 2
											2260 text +
											2261 text ∫
											2262 text 𝛿
											2263 text 𝑡
											2264 text ∥ ℎ ( 𝑟 )
											2265 text ∥
											2266 text 2
											2267 text 𝑑 𝑟 .
										2268 text (47)
									2269 text The inequality can be started at 
									2270 text 𝛿
									2271 text  by approaching it through admissible starting times from below, where the solution agrees with the strong solution and is strongly continuous. Taking the specified one-sided energy trace gives the same bound at 
									2272 container
										2273 text 𝑡 = 𝜏
									2274 text . Consequently,
									2275 container
										2276 container
											2277 container
												2278 text ∥ 𝑈 ( 𝜏 )
												2279 text ∥
												2280 text 2
											2281 container
												2282 text ≤
												2283 text 𝜖
												2284 text 2
												2285 text + 𝜂 ( 𝜏 − 𝛿 )
											2286 container
												2287 text ≤
												2288 text 𝜖
												2289 text 2
												2290 text +
												2291 text 1
												2292 container
													2293 text 16 𝜌
											2294 container
												2295 text ≤
												2296 container
													2297 text 9 𝜖
												2298 text 16
												2299 text < 𝜖 .
										2300 text (48)
									2301 text This proves the endpoint contract for every admissible initial state, disturbance, and Leray–Hopf realization.
									2302 heading 7. Physical resource bounds, Value: 2
										2303 text 7. Physical resource bounds
									2304 text The pulse duration (41) gives the exact scalings
									2305 container
										2306 container
											2307 text 𝑠
											2308 text 𝑑
											2309 text = 𝑚
											2310 text 𝐵
											2311 text ∗
											2312 text 8
											2313 text 𝜌
											2314 text 30
											2315 text ,
											2316 text 𝑠
											2317 container
												2318 text 𝑑 2
											2319 text =
											2320 text 𝑚
											2321 text 2
											2322 text 𝐵
											2323 text ∗
											2324 text 18
											2325 text 𝜌
											2326 text 66
											2327 text .
										2328 text (49)
									2329 text All spatial fields belong to the fixed finite family. Choose a fixed rational bound
									2330 container
										2331 text 𝐻
										2332 text 1
										2333 text ≥
										2334 container
											2335 text max ⁡
										2336 text 𝑗
										2337 text ∥
										2338 text 𝐺
										2339 text 𝑗
										2340 text ∥
										2341 container
											2342 text 𝑊
											2343 text 1
											2344 text ,
											2345 text ∞
										2346 text .
									2347 text We may keep 
									2348 container
										2349 text ∣ 𝜃 ∣ ≤ 65
									2350 text , since 
									2351 container
										2352 text 4
										2353 text 𝜋
										2354 text 2
										2355 text < 64
									2356 text . Using
									2357 container
										2358 text ∥ 𝑞
										2359 text ∥
										2360 text ∞
										2361 text =
										2362 text 3
										2363 text 2
										2364 text , ∥
										2365 text 𝑞
										2366 text ′
										2367 text ∥
										2368 text ∞
										2369 text = 6 ,
									2370 text equation (44) gives
									2371 container
										2372 container
											2373 container
												2374 text sup ⁡
											2375 text 𝑡
											2376 text ∥ 𝑓 ( 𝑡 )
											2377 text ∥
											2378 container
												2379 text 𝑊
												2380 text 1
												2381 text ,
												2382 text ∞
											2383 text ≤
											2384 text 𝐶
											2385 text 𝑓
											2386 text 𝜌
											2387 text 66
											2388 text ,
										2389 text (50)
									2390 text where, for example, the fixed computable constant
									2391 container
										2392 container
											2393 text 𝐶
											2394 text 𝑓
											2395 text =
											2396 text 𝐻
											2397 text 1
											2398 text 𝛼
											2399 text ∗
											2400 text (
											2401 text 6
											2402 container
												2403 text 𝑚 2
											2404 container
												2405 text 𝐵 ∗ 18
											2406 text +
											2407 text 100
											2408 container
												2409 text 𝐾 2
											2410 text 𝑚
											2411 container
												2412 text 𝐵 ∗ 8
											2413 text )
										2414 text (51)
									2415 text suffices. The force is supported on 
									2416 container
										2417 text [ 0 , 𝛿 ]
									2418 text , so
									2419 container
										2420 container
											2421 text ∫
											2422 text 0
											2423 text 𝜏
											2424 text ∥ 𝑓 ( 𝑡 )
											2425 text ∥
											2426 container
												2427 text 𝑊
												2428 text 1
												2429 text ,
												2430 text ∞
											2431 text 𝑑 𝑡 ≤
											2432 container
												2433 text 𝐶 𝑓
											2434 container
												2435 text 𝐵 ∗
											2436 text 𝜌
											2437 text 58
											2438 text .
										2439 text (52)
									2440 text Also,
									2441 container
										2442 container
											2443 text 𝜂
											2444 container
												2445 text − 1
											2446 text = 16 𝜌 ≤ 32 𝑅 .
										2447 text (53)
									2448 text Using 
									2449 container
										2450 text 𝜌 ≤ 2 𝑅
									2451 text , these are the claimed polynomial physical bounds. The number of intervals, including the final zero-force interval, is
									2452 container
										2453 container
											2454 text 𝑚 𝑛 + 1 = 𝑚
											2455 text 𝐵
											2456 text ∗
											2457 text 9
											2458 text 𝜌
											2459 text 28
											2460 text + 1.
										2461 text (54)
									2462 heading 8. Bit complexity and payment for the fixed precomputation, Value: 2
										2463 text 8. Bit complexity and payment for the fixed precomputation
									2464 heading 8.1 The online compiler uses finite arithmetic, Value: 3
										2465 text 8.1 The online compiler uses finite arithmetic
									2466 text The online algorithm is:
									2467 content list
										2468 container
											2469 AXListMarker 1. 
											2470 text Read the rational inputs and calculate 
											2471 text 𝜌
											2472 text .
										2473 container
											2474 AXListMarker 2. 
											2475 text Calculate 
											2476 container
												2477 text 𝑠 , 𝑛 , 𝛿 , 𝜂 , 𝑑
											2478 text  using (34) and (41).
										2479 container
											2480 AXListMarker 3. 
											2481 text Calculate the rational approximation 
											2482 text 𝜃
											2483 text  satisfying (45).
										2484 container
											2485 AXListMarker 4. 
											2486 text Emit the 
											2487 container
												2488 text 𝑚 𝑛
											2489 text  quadratic pulse records from (44), expanded in global time.
										2490 container
											2491 AXListMarker 5. 
											2492 text Emit the final zero-force interval and 
											2493 text 𝜂
											2494 text .
									2495 text It evaluates no PDE solution, unknown initial condition, disturbance, optimization problem, or infinite-dimensional norm. The integers 
									2496 text 𝑛
									2497 text , the interval endpoints, and all pulse parameters have 
									2498 container
										2499 text 𝑂 ( 𝐿 + log ⁡ 𝜌 )
									2500 text  bits, with fixed additive constants. Expanding a polynomial into global time can produce coefficients with numerical magnitudes as large as 
									2501 container
										2502 text 𝐶
										2503 text 𝜌
										2504 text 102
									2505 text , because of factors 
									2506 container
										2507 text 𝑑
										2508 text −
										2509 text 3
									2510 text . Their bit lengths are still
									2511 container
										2512 text 𝑂 ( 𝐿 + log ⁡ 𝜌 ) .
									2513 text The actual force values obey (50); the expansion introduces no extra physical cost. The certified arctangent calculation needs polynomially many bit operations in the requested precision. Using elementary exact rational arithmetic, a deliberately loose overall online bound is
									2514 container
										2515 container
											2516 text 𝐶
											2517 container
												2518 text a r i t h
											2519 text (
											2520 text 𝜌
											2521 text 28
											2522 text + 1 ) ( 𝐿 +
											2523 container
												2524 text log ⁡
											2525 text 2
											2526 text 𝜌 + 1
											2527 text )
											2528 text 8
											2529 text ,
										2530 text (55)
									2531 text for a fixed computable 
									2532 container
										2533 text 𝐶
										2534 text a
										2535 text r
										2536 text i
										2537 text t
										2538 text h
									2539 text . Total output bits and working-memory bits satisfy bounds of this form as well.
									2540 heading 8.2 A specified finite precomputation, Value: 3
										2541 text 8.2 A specified finite precomputation
									2542 text The precomputation consists of:
									2543 content list
										2544 container
											2545 AXListMarker 1. 
											2546 text Executing the effective fixed-family and word construction granted in your premises, retaining its full descriptions, bounds, and finite resource certificate.
										2547 container
											2548 AXListMarker 2. 
											2549 text Computing the commutator bounds from the returned Fourier data.
										2550 container
											2551 AXListMarker 3. 
											2552 text Computing 
											2553 container
												2554 text 𝜎 ,
												2555 text 𝐶
												2556 text 𝐷
												2557 text ,
												2558 text 𝐶
												2559 text 𝐸
												2560 text ,
												2561 text 𝐵
												2562 text ∗
											2563 text , and the fixed force and arithmetic bounds.
										2564 container
											2565 AXListMarker 4. 
											2566 text Fixing the exact rational-output encoding and schoolbook arithmetic implementation.
									2567 text This needs only the supplied estimates at orders 
									2568 container
										2569 text 0 , 1 , 2
									2570 text . To give an explicit way of selecting a common resource constant, let 
									2571 container
										2572 text 𝑁
										2573 text ∗
										2574 text ≥
										2575 text 2
										2576 text 20
									2577 text  be a computed integer dominating:
									2578 content list
										2579 container
											2580 AXListMarker • 
											2581 text The certified operation, memory, and description bounds of the entire fixed precomputation.
										2582 container
											2583 AXListMarker • 
											2584 text All fixed list lengths.
										2585 container
											2586 AXListMarker • 
											2587 container
												2588 text 𝐵 ∗
											2589 text , all fixed rational numerator and denominator heights, and the Fourier frequency bounds.
										2590 container
											2591 AXListMarker • 
											2592 text The direct Fourier norm and commutator bounds.
										2593 container
											2594 AXListMarker • 
											2595 text The fixed constants in the elementary arithmetic implementation.
									2596 text Enlarge it, by explicit integer arithmetic, to cover the finitely many fixed constants appearing in (50)–(55). Define
									2597 container
										2598 container
											2599 text 𝑝 = 128 , 𝐴 = ( 2
											2600 text 𝑁
											2601 text ∗
											2602 text )
											2603 text 1024
											2604 text .
										2605 text (56)
									2606 text This is a fixed, explicitly computable choice. The generous powers cover all fixed factors, the replacements 
									2607 container
										2608 text 𝜌 ≤ 2 𝑅
									2609 text , and the elementary arithmetic bound. The variable exponents in (50)–(55) are below 
									2610 text 128
									2611 text . Therefore the construction satisfies
									2612 container
										2613 container
											2614 text bit operations, working-memory bits, total output bits,
											2615 container
												2616 text interval count, degrees, and individual rational bit lengths ≤ 𝐴 ( 𝐿 + 𝑅
												2617 text )
												2618 text 128
												2619 text ,
										2620 text (57)
									2621 text and
									2622 container
										2623 container
											2624 text 𝜂
											2625 container
												2626 text − 1
											2627 text ,
											2628 container
												2629 text sup ⁡
											2630 text 𝑡
											2631 text ∥ 𝑓 ( 𝑡 )
											2632 text ∥
											2633 container
												2634 text 𝑊
												2635 text 1
												2636 text ,
												2637 text ∞
											2638 text ,
											2639 text ∫
											2640 text 0
											2641 text 𝜏
											2642 text ∥ 𝑓 ( 𝑡 )
											2643 text ∥
											2644 container
												2645 text 𝑊
												2646 text 1
												2647 text ,
												2648 text ∞
											2649 text 𝑑 𝑡 ≤ 𝐴
											2650 text 𝑅
											2651 text 128
											2652 text .
										2653 text (58)
									2654 text The first precomputation subroutine is precisely the effective fixed-word construction you supplied as accepted capital. Its full cost is included in 
									2655 text 𝐴
									2656 text ; no numerical rotation design or uncharged search is being introduced here.
									2657 heading What closes the nonlinear interface, Value: 2
										2658 text What closes the nonlinear interface
									2659 text The decisive additional implication is
									2660 container
										2661 text stable partial blocks in 
										2662 text 𝐻
										2663 text 0
										2664 text ,
										2665 text 𝐻
										2666 text 1
										2667 text ,
										2668 text 𝐻
										2669 text 2
										2670 text + [ Δ ,
										2671 text 𝐿
										2672 text 𝐹
										2673 text ] :
										2674 text 𝐻
										2675 text 2
										2676 text →
										2677 text 𝐿
										2678 text 2
										2679 text ⟹ polynomial nonlinear control over a short interval .
									2680 text The proof uses a different coordinate chart for each macro-block. Viscosity is controlled inside that chart, and the supplied 
									2681 container
										2682 text 𝐻 1
									2683 text  endpoint estimate controls the reset. This yields the uniform bounds (25), which make the nonlinear and viscous residuals integrable in 
									2684 container
										2685 text 𝐿 2
									2686 text . The stable forward propagator then gives the polynomial endpoint estimate (28). With the explicit compiler above, the carrier returns to zero, the same force works for the entire prescribed 
									2687 container
										2688 text 𝐻 1
									2689 text  ball, and every admissible realization satisfies the stronger endpoint bound
									2690 container
										2691 text ∥ 𝑈 ( 𝜏 )
										2692 text ∥
										2693 text 2
										2694 text ≤ 9 𝜖 / 16.
									2695 text Thus the full polynomial-resource contract follows from the supplied constructive premises.
									2696 button Copy
										2697 image
									2698 pop up button (collapsed) Description: Rate response, ID: radix-_r_oe_, Secondary Actions: Expand
									2699 checkbox Description: Read aloud, Value: 0
									2700 button Share
									2701 pop up button (collapsed) Description: More actions, ID: radix-_r_ok_, Secondary Actions: Expand
									2702 heading You said:, Value: 4
										2703 text You said:
									2704 container
										2705 text Polynomial common body-force control with twelve fundamental shear actuators  FULL QUESTION. On the UNIT three-torus restrict the physical additive force to EXACTLY the fixed twelve spatial fields  G_ij^c(x)=e_i cos(2pi x_j), G_ij^s(x)=e_i sin(2pi x_j), i!=j. Does there exist a total deterministic compiler that, for EVERY binary rational M>=1,0 < nu,tau<=1 and0 < epsilon<1, outputs ordinary rational piecewise-polynomial time coefficients for these fields and a positive rational eta, such that the SAME prescribed force f makes  U_t=nu Delta U-P div(U tensor U)+f+h, div U=0, integral U=0, satisfy ||U(tau)||2<=epsilon for EVERY real mean-zero divergence-free initial velocity with ||U0||H1<=M, EVERY mean-zero divergence-free disturbance ||h|| _ (L-infinity_t L2_x)<=eta, and EVERY corresponding Leray-Hopf realization? Use the one-sided energy trace at the fixed endpoint. The target is small TOTAL velocity.  No higher spatial forcing modes, extra advection, additional actuators, initial-dependent force, observation, feedback, selected solution or distributional impulse is supplied. The fluid may of course develop other Fourier modes through its own dynamics. The twelve fields and their rational polarizations are fixed once, independently of every variable input.  Retain the full polynomial resource requirement. Put R=2+M+nu^-1+tau^-1+epsilon^-1 and let L be COMPLETE binary input length. There must be fixed explicitly computable A>=1 and integer p>=1 such that compiler bit operations, working-memory bits, total output bits, interval counts, time-polynomial degrees and individual rational bit lengths are <=A(L+R)^p, while eta^-1, sup_t||f(t)|| _ (W1,infinity_x) and integral_0^tau||f(t)|| _ (W1,infinity_x)dt are <=A R^p. Pay all fixed preprocessing, generated-mode tables, frequency/iteration choices, searches, rational rounding and error estimates. No real/PDE/optimization/norm oracle is supplied.  A positive answer must construct and prove this entire compiler. A negative must obstruct all admitted twelve-field controls under the stated contract, not only one word, one saturation implementation or a proof route. Neither a known-initial-state controllability theorem nor a controller for an extra-advection equation closes the full question.  The suggested papers and supplied premises are starting points, not a limit on your research. You may read them, seek additional papers, literature, available Astra work or other sources, change mathematical representations, introduce different ideas and methods, and challenge my framing while pursuing the full question. You choose your sources and approach without further permission.  Available mathematics, to use or bypass:  1. The full polynomial-resource common additive-force endpoint is now constructed with ONE fixed enlarged rationally rotated shear family. Its finite macro-word W(s) has exact underlying transport identity, a bounded compact diagonal generator D with Sym D(k)<=-c/(1+|k|^2), and norm-Taylor error O(s^5) in H0,H1,H2. Stable repetition controls every forward subinterval. The fixed family, word and constants have effective finite precomputation, although that spatial table is enormous. This theorem is not already a twelve-actuator result.  2. Its new nonlinear estimate is quantitative. Within each macro-block let P_j be the inviscid propagator from that block's beginning and set z=P_j^-1(U-w). Partial blocks and inverses have bounded H0,H1,H2 norms. The explicit commutator  [Delta,L_F]:H2->L2 gives  ||P_j^-1 Delta P_j-Delta||\_(H2->L2)<=C_Delta s. Small s preserves viscous coercivity in the H1 energy. The coordinate reset costs only1+O(s^5), so the energy depends on n s^5 rather than total absolute strain n s. Local H1 strong existence, the uniform estimate and weak-strong uniqueness cover EVERY admitted Leray-Hopf realization for each actual disturbance; no small nonzero initial discrepancy is multiplied by an uncontrolled Gronwall factor.  For an active interval of length delta, with ||h+force_rounding_error||\_(L-infinity L2)<=a\_\*<=1, the result gives  sup||U-w||H1<=4M,  nu integral_0^delta||U-w||H2^2<=64M^2,  ||U(delta)-W(s)^n U0||2  <=16M sqrt(nu delta)+768M^2 delta^(3/4)nu^(-1/4)+2a\_\*delta, provided delta<=nu^3/(128 C_E M^4), n s^5 is sufficiently small and each partial block meets the fixed small-s bounds. Here C_E=108\*128^4.  With rho=2+ceil(M)+ceil(nu^-1)+ceil(tau^-1)+ceil(epsilon^-1) and fixed computable B\_\*, choose auxiliary time T=B\_\*rho^4, s=(B\_\*^2rho^6)^-1, n=B\_\*^9rho^28, delta=(B\_\*rho^8)^-1 and eta=(16rho)^-1. Quadratic rational pulses and paid pi-enclosures give an enlarged-family compiler with at most C R^28 intervals, peak force C R^66, integral force C R^58, eta^-1<=32R, and common resource exponent128. Its large fixed constant and spatial family remain part of its actual scope.  3. Twelve-mode algebraic coverage is available, but is not a physical controller. For complex modes a exp(2pi i k.x), b exp(2pi i l.x), symmetric quadratic interaction at k+l is proportional to  P\_(k+l)[(a.l)b+(b.k)a]. Trigonometric phases isolate sums and differences. Starting with the twelve fields gives the out-of-plane polarization at every signed two-coordinate diagonal. Combining such a diagonal with the remaining unit direction gives two polarizations at (1,1,1); combining polarization e1-e2 there with -e3 supplies the missing in-plane polarization at e1+e2. Permutations/signs complete the diagonal planes. Nonparallel unequal-length interactions then generate every fixed finite Fourier target list by finite algebraic steps. Current saturation literature establishes the broader statement too.  The remaining implementation must respect the ACTUAL nonlinear physical equation, common unknown-input quantifier and polynomial costs. Formal quadratic generation is not an identity between the physical linearized generators. A qualitative approximation whose cost grows exponentially in the enlarged carrier size is insufficient. The earlier polynomial three-cosine EXTRA-ADVECTION result has a different drift operator and does not pay this interface.  Optional primary starting point: Nersesyan, [https://arxiv.org/pdf/1403.5369v2](https://arxiv.org/pdf/1403.5369v2), Theorem2.5 and its proof, Theorem4.1/Proposition4.3 and identities4.6-4.12. The twelve fundamental modes are saturating, and the paper replaces forcing directions along a given smooth trajectory. Its H^k, k>=3, initial-dependent qualitative control statement on the2pi-torus does not supply the full common H1/allweak/unit-torus/polynomial contract above. You may develop that bridge or choose another approach.  you may use all subagents avaible
									2706 button (collapsed) Show more, Secondary Actions: Expand
										2707 text Show more
										2708 image
									2709 button Copy message
										2710 image
									2711 button Share prompt
									2712 button Edit message
										2713 image
									2714 button (expanded) Worked for 64m 45s, Secondary Actions: Collapse
										2715 text Worked for 64m 45s
										2716 image
									3623 text I’ll work on the actuator-reduction step directly: whether the twelve fundamental shears can reproduce the enlarged-family construction with polynomial cost and uniform control over unknown initial states. I’ll pursue physical forcing constructions in parallel with direct twelve-shear methods and possible obstructions.
									3624 container Subagent activity
										3625 container
											3626 button Nonlinear polynomial
											3627 text , 
											3628 button Alternative constructions
											3629 text  and 
											3630 button Obstructions audit
											3631 text  updated
									3632 text Developed a fixed-depth bridge
									3633 text Searching arxiv.org
									3634 text Developed high-frequency kick construction and analyzed pulse synthesis Checked signed decompositions and estimated uniform kick errors Constructed a finite-mode carrier and formulated target-chart dynamics Developed H1 stability estimates and factored the transport operator Prepared transport stability lemma Built surrogate-product Q and verified diffusion coercivity Estimated commutator-defect bounds and checked leftmost derivative terms Prepared rational Fourier approximations and proved approximation cost Evaluated piecewise amplitude weights and selected knot-zero carriers Chose adaptive microsteps and checked finite-mode closure Chose residual tolerance and bounded the μ-defect Set energy bootstrap bounds
									3635 container Subagent activity
										3636 container
											3637 button Nonlinear polynomial
											3638 text  finished
									3639 text Refined carrier construction and validated spatial basis Constructed rational certificates and selected zero-mean profiles Derived the residual update Tracked symbolic degree growth and chose a cubic pulse Derived commutator norm bounds and finite-Fourier symbols Computed commutator bounds and made proof constants explicit Chose δ and μ bounds Proved signed-cone and rational interaction coverage A promising construction is to use short velocity excursions with zero time integral. Their linearized flow returns exactly to the identity, while their quadratic Navier–Stokes interaction can generate a missing forcing direction. I’m working out how to repeat this through the fixed saturation table while keeping the averaging errors polynomially small.
									3640 container Subagent activity
										3641 container
											3642 button Alternative constructions
											3643 text , 
											3644 button Nonlinear polynomial
											3645 text  and 
											3646 button Obstructions audit
											3647 text  finished
									3648 text Verified beta bounds and derivative estimates Separated rational bitlength tracking from envelope analysis Set geometric stage bounds and refined rational κ approximations Prepared rational error bounds and selected initial H0 Bounded bit complexity and rational denominator growth Computed resource constants and fixed A from K Checked commutator bounds and solenoidal extensions Bounded the R_F commutator Bounded reset-loop propagators Bounded defect propagation Bounded residual errors and verified breakpoint alignment Checked surrogate propagator stability Fixed B before H0 Simplified the H2 proof Checked constant choices Defined finite support sets and weighted norm Selected K via precomputation and checked old partition tails Refined proof bounds and verified continuity bounds Simplified commutator bounds Established perturbation estimate and fixed explicit parameter choice Checked Hnext dominance and scaling Chose certified precision and bounded residual terms Constructed a phase-complete Fourier span Verified the span identity
									3649 text Searching arxiv.org
									3650 text Verified precomputation and coercivity bounds Fixed nested-space and factor notation consistency Defined the body-force certificate and integrated ζ slot profiles Constructed rational stage polynomials and prepared norm bounds Prepared exact Fourier closure Precomputed force coefficients and included explicit growth bound The construction now has a quantitative closure. Each lowering step produces a force in a smaller Fourier space; a known correction absorbs its averaging mismatch, and the force residuals add without amplification. The rapid-loop propagators reset to the identity at every original macro-block boundary, preserving the contracting word there. The remaining linear defect can be made smaller than a fixed fraction of viscosity. The resulting resource exponent is fixed and computable, though much larger than 128. Derived residual estimates Verified product defect bounds Preprocessed compiler parameters and encoded sign identities Checked rational setup and finite precomputation bounds
									2717 heading ChatGPT said:, Value: 4
										2718 text ChatGPT said:
									2719 heading Answer: yes, from the constructive premises supplied, Value: 2
										2720 text Answer: yes, from the constructive premises supplied
									2721 text There is a reduction to the 
									2722 text exact twelve fundamental shear actuators
									2723 text  that retains polynomial resources. The additional construction uses rapidly oscillating velocity excursions with two properties:
									2724 content list
										2725 container
											2726 AXListMarker 1. 
											2727 text Each excursion has zero time integral, so its physical linearized propagator returns  exactly to the identity .
										2728 container
											2729 AXListMarker 2. 
											2730 text Its quadratic self-interaction has a prescribed nonzero average, which supplies a forcing direction from the next saturation level.
									2731 text The important quantitative point is how to assemble these excursions. Below, the averaging errors are represented by explicitly bounded corrections to a prescribed reference path. Their force residuals 
									2732 text add
									2733 text , and the remaining linear defect can be made smaller than a fixed fraction of viscosity. This permits the blockwise 
									2734 container
										2735 text 𝐻 1
									2736 text  argument from your enlarged-family theorem to survive the actuator reduction. The resulting exponent is much larger than 
									2737 text 128
									2738 text . If 
									2739 text 𝐷
									2740 text  is the fixed saturation depth computed during preprocessing, one conservative choice is
									2741 container
										2742 text 𝑝 = 256
										2743 text 32
										2744 container
											2745 text 𝐷 + 1
										2746 text .
									2747 text The final time coefficients have degree at most 
									2748 text 3
									2749 text , and one can retain
									2750 container
										2751 text 𝜂 =
										2752 text 1
										2753 container
											2754 text 16 𝜌
										2755 text ,
										2756 text 𝜂
										2757 container
											2758 text − 1
										2759 text ≤ 32 𝑅 ,
									2760 text where
									2761 container
										2762 text 𝜌 = 2 + ⌈ 𝑀 ⌉ + ⌈
										2763 text 𝜈
										2764 container
											2765 text − 1
										2766 text ⌉ + ⌈
										2767 text 𝜏
										2768 container
											2769 text − 1
										2770 text ⌉ + ⌈
										2771 text 𝜖
										2772 container
											2773 text − 1
										2774 text ⌉ .
									2775 text Here is the construction and proof. The enlarged-family theorem is used as the accepted starting theorem; its larger fields occur only in the intermediate construction and analysis. The force ultimately emitted belongs exactly to the twelve-dimensional space in the question.
									2776 heading 1. A fixed, rational saturation certificate, Value: 1
										2777 text 1. A fixed, rational saturation certificate
									2778 text Write
									2779 container
										2780 text 𝜅 = 2 𝜋 , 𝐵 ( 𝑢 , 𝑣 ) = 𝑃 [ ( 𝑢 ⋅ ∇ ) 𝑣 ] ,
										2781 text 𝐿
										2782 text 𝐹
										2783 text 𝑣 = 𝐵 ( 𝐹 , 𝑣 ) + 𝐵 ( 𝑣 , 𝐹 ) ,
									2784 text and introduce the algebraically normalized interaction
									2785 container
										2786 text 𝐵 ( 𝑢 , 𝑣 ) =
										2787 text 𝜅
										2788 container
											2789 text − 1
										2790 text 𝐵 ( 𝑢 , 𝑣 ) .
									2791 text For trigonometric fields with integer wavevectors and rational polarizations, 
									2792 text 𝐵
									2793 text  has rational Fourier coefficients. The Fourier Leray projections
									2794 container
										2795 text 𝑃
										2796 text 𝑘
										2797 text = 𝐼 −
										2798 container
											2799 text 𝑘 ⊗ 𝑘
										2800 container
											2801 text ∣ 𝑘
											2802 text ∣
											2803 text 2
										2804 text , 𝑘 ≠ 0 ,
									2805 text are rational matrices. Let
									2806 container
										2807 text 𝑉
										2808 text 0
										2809 text = span ⁡
										2810 text {
										2811 container
											2812 text 𝑒 𝑖
										2813 text cos
										2814 text ⁡
										2815 text (
										2816 text 2
										2817 text 𝜋
										2818 container
											2819 text 𝑥 𝑗
										2820 text )
										2821 text ,
										2822 container
											2823 text 𝑒 𝑖
										2824 text sin
										2825 text ⁡
										2826 text (
										2827 text 2
										2828 text 𝜋
										2829 container
											2830 text 𝑥 𝑗
										2831 text )
										2832 text :
										2833 text 𝑖
										2834 text ≠
										2835 text 𝑗
										2836 text }
										2837 text .
									2838 text During fixed preprocessing, construct finite rational Fourier spaces
									2839 container
										2840 container
											2841 text 𝑉
											2842 text 0
											2843 text ⊂
											2844 text 𝑉
											2845 text 1
											2846 text ⊂ ⋯ ⊂
											2847 text 𝑉
											2848 text 𝐷
										2849 text (1)
									2850 text such that 
									2851 container
										2852 text 𝑉 𝐷
									2853 text  contains the enlarged shear family from the supplied theorem. The finite Fourier saturation needed here is available from the supplied algebraic premise. Nersesyan’s Theorem 4.1 and Proposition 4.3 also supply exact finite-level generation, including the twelve-mode choice, rather than only density of an unspecified collection. 
									2854 link (collapsed) Value: arxiv.org/pdf/1403.5369v2?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: https://arxiv.org/pdf/1403.5369v2, https://arxiv.org/pdf/1403.5369v2?utm_source=chatgpt.com, 1 additional source
									2855 heading 1.1 Why the certificates support the required signs, Value: 2
										2856 text 1.1 Why the certificates support the required signs
									2857 text If 
									2858 container
										2859 text 𝑎 , 𝑏
									2860 text  are individually single divergence-free Fourier modes, then
									2861 container
										2862 text 𝐵 ( 𝑎 , 𝑎 ) = 𝐵 ( 𝑏 , 𝑏 ) = 0.
									2863 text Consequently,
									2864 container
										2865 text 𝐵 ( 𝑎 + 𝑏 , 𝑎 + 𝑏 ) = 𝐵 ( 𝑎 , 𝑏 ) + 𝐵 ( 𝑏 , 𝑎 ) ,
									2866 text and
									2867 container
										2868 container
											2869 text 𝐵 ( 𝑎 − 𝑏 , 𝑎 − 𝑏 ) = − 𝐵 ( 𝑎 , 𝑏 ) − 𝐵 ( 𝑏 , 𝑎 ) .
										2870 text (2)
									2871 text Thus both signs of each symmetric interaction are available through negative quadratic squares of fields in the lower space. Choose a pure-frequency sine/cosine basis at every level. These spaces can be kept invariant under translations, and hence under 
									2872 text Δ
									2873 text . One way to see this is that the operation
									2874 container
										2875 text 𝑉 ⟼ 𝑉 + span ⁡ { 𝐵 ( 𝑎 , 𝑎 ) : 𝑎 ∈ 𝑉 }
									2876 text preserves translation invariance. Every finite-dimensional translation-invariant trigonometric space is a sum of Fourier subspaces. Exact rational linear algebra therefore produces, for every basis vector and its negative at level 
									2877 container
										2878 text 𝑗 + 1
									2879 text , certificates of the form
									2880 container
										2881 container
											2882 text 𝑢 = 𝜂 ( 𝑢 ) −
											2883 text ∑
											2884 container
												2885 text ℓ = 1
											2886 container
												2887 text 𝐽 𝑗
											2888 text 𝑑
											2889 text ℓ
											2890 text ( 𝑢 ) 𝐵 (
											2891 text 𝜉
											2892 text ℓ
											2893 text ,
											2894 text 𝜉
											2895 text ℓ
											2896 text ) ,
											2897 text 𝑑
											2898 text ℓ
											2899 text ( 𝑢 ) ≥ 0 ,
										2900 text (3)
									2901 text where
									2902 container
										2903 text 𝜂 ( 𝑢 ) ,
										2904 text 𝜉
										2905 text ℓ
										2906 text ∈
										2907 text 𝑉
										2908 text 𝑗
										2909 text .
									2910 text The list of possible 
									2911 container
										2912 text 𝜉 ℓ
									2913 text ’s is fixed. For a general rational 
									2914 container
										2915 text 𝑢 ∈
										2916 text 𝑉
										2917 container
											2918 text 𝑗 + 1
									2919 text , sign splitting of its basis coefficients gives (3) by rational arithmetic. The certificate coefficients satisfy fixed bounds
									2920 container
										2921 container
											2922 text ∥ 𝜂 ( 𝑢 )
											2923 text ∥
											2924 text ∗
											2925 text +
											2926 text ∑
											2927 text ℓ
											2928 text 𝑑
											2929 text ℓ
											2930 text ( 𝑢 ) ≤ 𝐶 ∥ 𝑢
											2931 text ∥
											2932 text ∗
											2933 text .
										2934 text (4)
									2935 text Here and below 
									2936 container
										2937 text ∥ ⋅
										2938 text ∥
										2939 text ∗
									2940 text  is a computable coefficient norm on a fixed finite Fourier table, large enough to control every spatial norm used in the proof. This preprocessing terminates by finite algebraic saturation. Its entire search, rational elimination, Fourier tables, and certificate descriptions are charged to the fixed preprocessing cost.
									2941 heading 2. The enlarged-family reference, Value: 1
										2942 text 2. The enlarged-family reference
									2943 text Use the supplied enlarged-family construction, with its fixed constants enlarged when necessary below. It gives a prescribed carrier 
									2944 text 𝑤
									2945 text , a rational force 
									2946 container
										2947 text 𝑓
										2948 container
											2949 text ( 0 )
										2950 text ∈
										2951 text 𝑉
										2952 text 𝐷
									2953 text , and the macro-word 
									2954 container
										2955 text 𝑊 ( 𝑠 )
									2956 text . Use
									2957 container
										2958 container
											2959 text 𝑇 =
											2960 text 𝐵
											2961 text ∗
											2962 text 𝜌
											2963 text 4
											2964 text , 𝑠 = (
											2965 text 𝐵
											2966 text ∗
											2967 text 2
											2968 text 𝜌
											2969 text 6
											2970 text )
											2971 container
												2972 text − 1
											2973 text , 𝑛 =
											2974 text 𝐵
											2975 text ∗
											2976 text 9
											2977 text 𝜌
											2978 text 28
											2979 text , 𝛿 = (
											2980 text 𝐵
											2981 text ∗
											2982 text 𝜌
											2983 text 8
											2984 text )
											2985 container
												2986 text − 1
											2987 text .
										2988 text (5)
									2989 text Then
									2990 container
										2991 text 𝑛
										2992 text 𝑠
										2993 text 4
										2994 text = 𝑇 , 𝑛
										2995 text 𝑠
										2996 text 5
										2997 text = (
										2998 text 𝐵
										2999 text ∗
										3000 text 𝜌
										3001 text 2
										3002 text )
										3003 container
											3004 text − 1
										3005 text .
							3598 container
								3599 text ChatGPT can make mistakes. Check important info.
							3600 container
								3601 button Scroll to bottom
								3602 heading Latest response, Value: 4
									3603 text Latest response
								3604 container
									3605 container
										3606 button (collapsed) Description: Add files and more, Secondary Actions: Expand
										3607 text entry area (settable) Description: Ask ChatGPT, Value: 

											3608 container
												3651 text Ask ChatGPT
										3610 pop up button (collapsed) Description: Select ChatGPT model, ID: radix-_r_4u_, Secondary Actions: Expand
											3611 text Pro
										3612 button Dictate
										3613 button Start Voice
						3614 container
							3615 heading Activity, Value: 3
								3616 text Activity
							3617 button 3 used
								3618 text Subagents
								3619 text 3 used
							3620 button (expanded) Outputs, Secondary Actions: Collapse
							3621 text No outputs yet
		3622 text Response complete

The focused UI element is 2714 button (expanded) Worked for 64m 45s, Secondary Actions: Collapse
```
