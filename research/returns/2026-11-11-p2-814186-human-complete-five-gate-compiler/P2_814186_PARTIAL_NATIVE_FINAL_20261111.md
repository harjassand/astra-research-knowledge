# P2 partial native final — capture blocked

Chat: https://chatgpt.com/c/6af2d0d2-f500-83ec-a7d0-20e80bd42677
User turn: d94de0b1-8ece-477a-8e18-a94e6e2e6e54; assistant: 814186bc-d852-520f-a7ac-e3cc2e422330.
Question: P2_FULL_MAGNETIC_FLUX_RESPONSE_AFTER_WHOLE_FIELD_GATES_PRO_20261111.txt.

This is only the first 20,000 characters returned by the native reader; the final is truncated. The full visible answer, expanded activity and three helper panels are not yet saved. TextEdit and Stickies timed out after desktop unlock. No archive or components were collected. Do not treat this as the full return.

## Partial native final

**Yes—using the constructions you now accept, the full contract can be obtained.** The assembly can be made with **five scalar-field magnetic gates and three positive-time filters**, followed by a velocity writer that preserves the magnetic response already written.

The fixed number of magnetic gates is decisive. Their number does not grow with the target’s Fourier support. Their coefficients and frequencies grow polynomially, and their approximation errors can be assigned backward through a fixed list of operations.

Two additional physical estimates are needed:

1. A velocity reset that preserves a smooth magnetic reference, with a quantitative bound for an arbitrary \(H^1\) discrepancy around that reference.
2. A positive-heat operation that works for an arbitrary polynomial smooth-field bound over a prescribed total time. This is needed because the unwanted modes produced by the outer filters can be larger than the packets in your fourth premise.

I give those estimates, the five-gate algebra, and the compiler and resource accounting below. Throughout, the earlier quantitative constructions are used as accepted premises; the new magnetic assembly and the memory estimates are the additions.

---

# 1. Notation, truncation, and computable bounds

Write
\[
\kappa=2\pi,\qquad
D_j=\kappa^{-1}\partial_j,\qquad
\mathscr C=\kappa^{-1}\operatorname{curl}.
\]
Normalized derivatives send rational Fourier fields to rational Fourier fields.

For velocity, use
\[
\mathcal B(v,w)=\mathbb P[(v\cdot\nabla)w],
\]
and for induction use
\[
\mathcal C_v b=(b\cdot\nabla)v-(v\cdot\nabla)b.
\]

The scalar gates used below are
\[
\boxed{\quad
\mathcal T_i(\phi)B
   =B+\mathscr C(e_i\phi B_i).
\quad}                                                    \tag{1}
\]
This normalization is obtained from your whole-field gate by changing its second impulse to
\[
b_*=\frac{2}{\kappa^2q^2}.
\]
Indeed, its mixed term has coefficient \(ab_*\kappa Q/2=1/\kappa\). A rational enclosure of \(b_*\) is used in the emitted programme, with the resulting error included in the gate budget.

No operator-norm convergence of \(\mathcal T_i(\phi)\) on the whole \(H^1\) space is used. Every application is to a prescribed smooth reference plus an arbitrary \(H^1\) discrepancy.

## Truncating the complete input

First canonicalize the Fourier lists: combine duplicate frequencies, identify the \(\pm k\) representations, and combine their rational coefficients exactly. This prevents large cancelling input coefficients from entering numerical resource bounds.

Set
\[
N=\left\lceil \frac{128MK}{\epsilon}\right\rceil
\]
and discard all nonconstant modes with \(|k|>N\). Integer comparisons against \(N^2\) suffice; no enumeration up to a binary-encoded input frequency is performed.

Denote the resulting fields by \(V_N,\Pi_N\). Their constant terms remain \(0,I\), respectively, and
\[
\|V-V_N\|_2+\sup_{|H|\le M}\|(\Pi-\Pi_N)H\|_2
\le \frac{\epsilon}{32}.                                  \tag{2}
\]
The numerical constant here is deliberately generous.

For a finite Fourier field \(F\), use rational bounds of the form
\[
\mathcal E_m(F)
=
1+\sum_k
\bigl(|F_k^c|_1+|F_k^s|_1\bigr)(1+7|k|_1)^m.               \tag{3}
\]
They bound all required fixed-order spatial norms. After canonicalization and truncation,
\[
\mathcal E_m(V_N)+\mathcal E_m(\Pi_N)
\le C_mK(1+N)^{m+3}.
\]
Thus these numerical bounds are polynomial in \(R\), independently of the original coefficient denominators and original maximum frequency.

One may replace the lower diffusivity bounds by
\[
\nu_0=\frac1{\lceil\nu_-^{-1}\rceil},\qquad
\rho_0=\frac1{\lceil\rho_-^{-1}\rceil},\qquad
\mu=\min(\nu_0,\rho_0).
\]
Then
\[
\nu_-/2\le\nu_0\le\nu_-,
\qquad
\rho_-/2\le\rho_0\le\rho_-.
\]
All controllers can be compiled for the larger rectangles
\([\nu_0,1]\times[\rho_0,1]\). In particular, no numerical bound depends on an inverse interval width.

Below, \(P\) denotes a computable positive polynomial in the explicitly listed numerical bounds. Its coefficients and degree are fixed by the finite precomputation described in §8. It never denotes an unevaluated PDE norm.

---

# 2. Five gates suffice for every admissible matrix target

This is the algebraic assembly that removes the growing-depth problem.

Because \(\Pi_N-I\) has mean zero and solenoidal columns, compute a rational Fourier matrix potential \(\Gamma\) satisfying
\[
\mathscr C\Gamma=\Pi_N-I
\]
columnwise. For \(m\ne0\), one choice is
\[
\widehat{\Gamma^{(j)}}(m)
=
\frac{i\,m\times\widehat{(\Pi_N-I)^{(j)}}(m)}{|m|^2}.        \tag{4}
\]
In real sine/cosine coordinates this uses only rational arithmetic.

Write \(\Gamma_1,\Gamma_2,\Gamma_3\) for its rows. Then
\[
\Pi_NH
=
H+\sum_{i=1}^3\mathscr C(e_i\Gamma_iH).                    \tag{5}
\]

Choose three separated integer frequencies
\[
Q_1\gg Q_2\gg Q_3\gg N.
\]
Their quantitative selection is given later. Define
\[
w(\theta)=(\sin\theta,\cos\theta,\sin2\theta).
\]
The identities
\[
\langle w_j\rangle=0,\qquad
\langle w_jw_\ell\rangle=\tfrac12\delta_{j\ell}              \tag{6}
\]
will read the components of \(H\) from temporary Fourier signals in the same magnetic field.

## Gates 1 and 2: encode all three components in the first component

Starting from \(B=H\), apply
\[
\mathcal T_2\!\left(\frac{\cos(\kappa Q_1x_3)}{Q_1}\right),
\qquad
\mathcal T_3\!\left(-\frac{\cos(\kappa Q_1x_2)}{Q_1}\right).
\]
The result is exactly
\[
\begin{aligned}
B_1&=H_1+\sin(\kappa Q_1x_3)H_2
                +\sin(\kappa Q_1x_2)H_3,\\
B_2&=H_2,\qquad B_3=H_3.
\end{aligned}                                             \tag{7}
\]
These are simultaneous encodings in one physical magnetic field. There is no combination of separate experiments.

## Gate 3: write the first row of the potential

Choose the row
\[
\chi_2(x_3)=
\left(
-\frac{\cos(\kappa Q_2x_3)}{Q_2},
\frac{\sin(\kappa Q_2x_3)}{Q_2},
-\frac{\cos(2\kappa Q_2x_3)}{2Q_2}
\right),
\]
so that
\[
D_3\chi_2=w(\kappa Q_2x_3).
\]
Put
\[
A_1=\Gamma_1+\chi_2
\]
and
\[
\phi_1
=
A_{11}
+2A_{12}\sin(\kappa Q_1x_3)
+2A_{13}\sin(\kappa Q_1x_2).                               \tag{8}
\]

The part of \(\phi_1B_1\) without a nonzero \(Q_1\) carrier is exactly \(A_1H\). Consequently, applying \(\mathcal T_1(\phi_1)\) and removing the nonzero \(Q_1\) carriers leaves
\[
\boxed{
\Sigma_1H
=
H+\mathscr C(e_1\Gamma_1H)
  +e_2w(\kappa Q_2x_3)H.
}                                                         \tag{9}
\]

The \(Q_1\) signals in \(B_1\) are removed by this filter. They are not assumed to cancel algebraically.

## Gate 4: write the second row

Choose \(\chi_3(x_1)\) by the corresponding formula, with
\[
D_1\chi_3=w(\kappa Q_3x_1).
\]
Put
\[
A_2=\Gamma_2+\chi_3,
\qquad
\phi_2=2\sum_{j=1}^3 A_{2j}w_j(\kappa Q_2x_3).             \tag{10}
\]

The second component of (9) is
\[
B_2=(e_2^T+D_3\Gamma_1)H+w(\kappa Q_2x_3)H.
\]
By (6), the low part of \(\phi_2B_2\) is \(A_2H\). The product with the base row has a nonzero \(Q_2\) carrier.

After \(\mathcal T_2(\phi_2)\) and the second filter, the reference is
\[
\boxed{
\Sigma_2H
=
H+\mathscr C(e_1\Gamma_1H)
 +\mathscr C(e_2\Gamma_2H)
 +e_3w(\kappa Q_3x_1)H.
}                                                         \tag{11}
\]

## Gate 5: write the third row

Set
\[
\phi_3
=
2\sum_{j=1}^3\Gamma_{3j}w_j(\kappa Q_3x_1).                \tag{12}
\]
The low part of \(\phi_3B_3\), with \(B\) given by (11), is \(\Gamma_3H\). Thus \(\mathcal T_3(\phi_3)\), followed by the third filter, gives
\[
H+\sum_{i=1}^3\mathscr C(e_i\Gamma_iH)=\Pi_NH.              \tag{13}
\]

This proves the exact reference identity using **five gates and three filters**.

Only mean and divergence constraints on \(\Pi_N\) were used. No inverse of \(\Pi_N\), determinant condition, commuting-column condition, or factorization of \(\Pi_N\) as a flow derivative appears.

The remaining task is to realize the filters and preserve the written field during the mechanical operations.

---

# 3. Velocity resets that preserve magnetic memory

Here “preserving memory” means a bound relative to a smooth reference. It does not assert uniform \(H^1\)-continuity of heat at zero time.

The required reset has the following form. Given a smooth reference \(\beta\), an arbitrary \(H^1\) error \(e\), and a known joint \(H^1\) bound, it makes velocity \(H^1\)-small while ensuring
\[
\|e_{\rm out}\|_{H^1}
\le (1+P\delta^\alpha)\|e_{\rm in}\|_{H^1}
       +P\delta^\alpha,                                   \tag{14}
\]
for a fixed \(\alpha>0\). The same statement holds in a fixed induction-prefix metric. Its force uses bounds on \(\beta\), not the value of \(\beta\).

The substantive point is that this estimate survives the actual twelve-actuator lowering.

## 3.1 An explicit lowering cell

Use
\[
\psi(z)=z(1-z)(1-2z).
\]
Then
\[
\psi(0)=\psi(1)=0,\qquad
\int_0^1\psi=0,\qquad
\int_0^1\psi^2=\frac1{210},
\]
and
\[
\Psi(z)=\int_0^z\psi
       =\tfrac12z^2(1-z)^2.
\]

On a cell of duration \(h\), let
\[
q(t)=a\psi(t/h),\qquad
Q(t)=ah\Psi(t/h),\qquad
\zeta=qF.
\]
Thus
\[
Q(0)=Q(h)=0,\qquad
\beta_Q:=\sup|Q|=\frac{|a|h}{32}.
\]
The emitted contribution is \(q'F\), an ordinary rational quadratic pulse when \(a,h\) are rational.

Set
\[
L_Fv=\mathcal B(F,v)+\mathcal B(v,F),\qquad
E_Q=e^{-QL_F},
\]
and make the exact change of variables
\[
y=E_Q^{-1}(u-qF).
\]
For actual force \(q'F+f_{\rm low}\), the momentum equation becomes
\[
\begin{aligned}
y_t={}&
\nu E_Q^{-1}\Delta E_Qy
-E_Q^{-1}\mathcal B(E_Qy,E_Qy)
-q^2E_Q^{-1}\mathcal B(F,F)\\
&+\nu qE_Q^{-1}\Delta F
+E_Q^{-1}\bigl(f_{\rm low}+\mathcal B(B,B)+h_u\bigr).
\end{aligned}                                             \tag{15}
\]

The desired virtual quadratic force is
\[
-\frac{a^2}{210}\mathcal B(F,F).
\]
The signed quadratic certificates in the accepted construction supply the required signs and directions.

Let \(g\) be the difference between the smooth source in (15) and the desired virtual source. On the cell define, only in the proof,
\[
\bar g=h^{-1}\int_0^h g(t)\,dt,\qquad
\chi(t)=\int_0^t(g(s)-\bar g)\,ds.
\]
Then
\[
\chi(0)=\chi(h)=0.
\]

Through every fixed spatial order required below,
\[
\|\chi\|_{H^k}
\le
C_F\bigl[a^2h+\beta_Q+
 \beta_Qh\|f_{\rm low}\|_{H^{k+1}}\bigr](1+\Lambda h),       \tag{16}
\]
and
\[
\|\bar g\|_{H^k}
\le
C_F\beta_Q
\bigl(a^2+\Lambda+\|f_{\rm low}\|_{H^{k+1}}\bigr).           \tag{17}
\]
Freezing a rational time polynomial on the cell adds the corresponding explicitly bounded time-variation error.

For the viscosity term, the relevant identity is
\[
qE_Q^{-1}\Delta F
=
\frac{d}{dt}
\left(\int_0^{Q(t)}e^{sL_F}\Delta F\,ds\right).
\]
Integration by parts against the Lipschitz function \(\nu(t)\) gives a zero-endpoint primitive of size \(C_F\beta_Q(1+\Lambda h)\) and a cell-average residual of size \(C_F\Lambda\beta_Q\). No value of \(\nu\) is evaluated or emitted.

The amplitudes can be obtained by rational square-root bisection to an absolute forcing tolerance. Coefficients below that absolute tolerance are omitted. Consequently no inverse of a tiny target coefficient enters a numerical bound.

## 3.2 The correct magnetic reference

Define
\[
M_Q=e^{Q\mathcal C_F}.
\]
Suppose \(w_0\) is the inner smooth carrier and \(R_0(t)\) its intended induction propagator. The momentum normal form has
\[
u=qF+E_Q(w_0+v+\chi).
\]

Use the magnetic reference propagator
\[
N(t)=M_Q(t)R_0(t).                                        \tag{18}
\]
Its carrier velocity is \(qF+M_Qw_0\). Hence the actual induction remainder is exactly
\[
u-(qF+M_Qw_0)
=
E_Qv+(E_Q-M_Q)w_0+E_Q\chi.                                \tag{19}
\]

The two generators differ by an order-zero operator:
\[
-L_F-\mathcal C_F=-2\mathbb P[(\,\cdot\,\nabla)F].
\]
In particular,
\[
\|(E_Q-M_Q)w_0\|_{H^1}
\le C_F\beta_Q\|w_0\|_{H^2}.                              \tag{20}
\]

Choose the faster cell length after the inner carrier and its amplitudes have been fixed. It can be chosen so that
\[
C_F\beta_Q(1+\|w_0\|_{H^k})^2,\qquad
C_F\|\chi\|_{H^k}(1+\|w_0\|_{H^k})^2
\]
are below the assigned coercivity and residual budgets.

This is a polynomial choice. For example, form a rational bound \(H_*\ge2\) for all already fixed quantities, reciprocal tolerances, and coefficients in these inequalities, and take
\[
h\le H_*^{-q_*},
\]
where the fixed integer \(q_*\) is chosen in the finite precomputation to dominate the finitely many powers involved.

At each lowering-cell endpoint,
\[
E_Q=M_Q=I,\qquad \chi=0.                                  \tag{21}
\]
Thus if the inner magnetic word returns to identity, so does the complete magnetic proof reference.

For nested lowering, repeat (19). Each next phase is selected after the inner amplitudes are fixed. The erasing catalogue has fixed depth, and the variable-target writer has fixed depth. The resulting powers therefore remain universal.

## 3.3 Joint energy and independence from erasure accuracy

The added linear velocity defect is bounded by
\[
C_F\beta_Q(1+\|w_0\|_{H^k})\|v\|_{H^2},
\]
and is absorbed by viscosity. The smooth defects are bounded by (16)–(17) and the phase choices.

The sharp nonlinear estimates are
\[
\|\mathcal B(v,v)\|_2
\le C\|v\|_{H^1}^{3/2}\|v\|_{H^2}^{1/2},
\]
\[
\|\mathcal B(B,B)\|_2
\le C\|B\|_{H^1}^{3/2}\|B\|_{H^2}^{1/2}.                  \tag{22}
\]

The old stable velocity block coordinate and the magnetic coordinate (18) therefore give
\[
Y'+c_*\mathcal D\le C_*(1+Y)^3.                           \tag{23}
\]
Here \(c_*^{-1},C_*\) are polynomial in the state and smooth-memory bounds and reciprocal diffusivities. They do not grow with the number of lowering cells or with the compression speed.

The only discrete velocity factor is the accepted
\[
\prod_{\rm blocks}(1+Cs^5)\le e^{Cns^5}.
\]
There is no magnetic coordinate jump at complete blocks.

The actual-viscosity affine corrector can remain in the bounded remainder. The accepted order-four cancellation gives, through the required fixed orders,
\[
\|a_\nu\|
\le C\bigl(s+ns^5+\Lambda\delta s\bigr).                   \tag{24}
\]
Its defining equation cancels the large viscosity term. The remaining estimates use its spatial norms, not a large time derivative.

Choosing the physical duration below the explicit local threshold in (23) yields a raw endpoint \(H^1\) bound independent of the requested small velocity \(L^2\) tolerance. The old contracting word still supplies that \(L^2\) tolerance.

This independence is needed for the next step.

## 3.4 Upgrading the reset endpoint to \(H^1\)

Let the raw endpoint satisfy
\[
\|u\|_2\le\sigma_0,\qquad
\|(u,B)\|_{H^1}\le P_0,
\]
where \(P_0\) is independent of \(\sigma_0\).

Append a short unforced interval \(\ell\). The scalar non-autonomous Stokes propagator is
\[
S_\nu(t,s)=
\exp\!\left(\Delta\int_s^t\nu(r)\,dr\right).
\]
Using
\[
\|\mathcal B(a,b)\|_{H^{-1/2}}
\le C\|a\|_{H^1}\|b\|_{H^1},
\]
one obtains
\[
\|u(\ell)\|_{H^1}
\le
\frac{C\sigma_0}{\sqrt{\mu\ell}}
+C\mu^{-1}P_0^2\ell^{1/4}
+C\eta\sqrt{\ell/\mu}.                                    \tag{25}
\]

First choose \(\ell\) from the required velocity and magnetic budgets. Then choose, conservatively,
\[
\sigma_0\le \frac{\sigma\mu\ell}{16C}.
\]
All reciprocals remain polynomial.

For magnetic error in a fixed prefix metric, let \(N(t)\) be the closed reference propagator and write
\[
B=N(t)(\beta+z).
\]
Its equation is
\[
z_t
=
\rho N^{-1}\Delta N(z+\beta)
+\mathcal C_{N^{-1}v}(z+\beta)+N^{-1}h_B.
\]
Conjugated scalar diffusion has
\[
\operatorname{Re}
\langle N^{-1}\Delta Nz,z\rangle_{H^1}
\le-\alpha_0\|z\|_{H^2}^2+\omega_0\|z\|_{H^1}^2,           \tag{26}
\]
with polynomial reciprocal coercivity and lower-order constant.

Together with
\[
\|\mathcal C_vz\|_2
\le C\|v\|_{H^1}\|z\|_{H^1}^{1/2}\|z\|_{H^2}^{1/2},
\]
this gives
\[
\boxed{
\|z_{\rm out}\|_{H^1}
\le (1+P\delta)\|z_{\rm in}\|_{H^1}+P\sqrt\delta.
}                                                         \tag{27}
\]

Both endpoint norms use the same prefix metric. There is no fixed metric-conversion loss at every reset.

This proves the required memory-preserving reset, including the structural condition needed by your conditional ideal-flow lift.

---

# 4. A velocity writer preserving the magnetic response

The final velocity writer is obtained from closed translations, rather than from a tracking interpretation of the old endpoint theorem.

For a fundamental shear \(F\), choose \(q(t)\) so its phase
\[
\alpha(t)=\int_0^tq(s)\,ds
\]
goes \(0\to a\to0\), with a plateau at \(a\). Apply
\[
f=q'F+gG,
\]
where \(G\) is a fundamental actuator and \(g\) is supported on the plateau.

Let \(E_\alpha=e^{-\alpha L_F}\). Define the proof reference
\[
v_t+L_{qF}v=\nu(t)\Delta(qF)+gG.
\]
Then \(u_*=qF+v\) has residual
\[
u_{*,t}-\nu\Delta u_*+\mathcal B(u_*,u_*)-f
=
\mathcal B(v,v)-\nu\Delta v.                               \tag{28}
\]
All large carrier terms have cancelled.

For one shear, the viscosity corrector is
\[
r_\nu(t)=\Delta F\int_0^t\nu(s)q(s)\,ds.
\]
Its endpoint is \(O(P\Lambda T)\), since \(\int q=0\). For a fixed two-shear conjugation word, the frozen-viscosity affine terms cancel under the forward/inverse word, and the Lipschitz remainder has the same \(P\Lambda T\) bound.

The magnetic reference follows the corresponding closed induction word and returns exactly to its initial smooth field. The joint estimates above give endpoint error factors \(1+\text{small}\).

### The Gårding estimate for complete conjugation prefixes

For completeness, this estimate follows from the accepted fundamental-shear bounds, not merely from bounded operator norms.

Write
\[
E_a=M_aZ_a.
\]
Then
\[
Z_a'=K_aZ_a,\qquad
K_a=M_a^{-1}\bigl(-2\mathbb P[(\,\cdot\,\nabla)F]\bigr)M_a.
\]
The pulled-back Leray projector is expressed through a scalar elliptic inverse:
\[
M_a^{-1}\mathbb PM_a
=
I-g_a\nabla\bigl(\operatorname{div}(g_a\nabla)\bigr)^{-1}
\operatorname{div}.
\]
Its coefficient, ellipticity, and fixed-order inverse estimates are polynomial in the shear impulse.

For every scalar second-order \(L\),
\[
[L,K_a]:H^1\longrightarrow L^2
\]
has a polynomial bound. The inverse term is handled by
\[
[L,A^{-1}]=-A^{-1}[L,A]A^{-1};
\]
the middle commutator has order at most three. Consequently
\[
[L,Z_a]
=
\int_0^a Z_aZ_s^{-1}[L,K_s]Z_s\,ds
\]
has a polynomial bound using the accepted polynomial propagator and inverse bounds.

It follows that \(E_a^{-1}\Delta E_a\) has a scalar elliptic second-order principal part and a remainder bounded \(H^1\to L^2\). This property persists under the fixed number of shear factors in the plane-mode words. Pairing with \((I-\Delta)z\) gives the required polynomial \(H^1\) Gårding estimate.

### Quadratic closure

Suppose translations in two Fourier shears \(F,G\) are available. Choose the sign of
\[
K=F\pm G
\]
so that \(-\mathcal B(K,K)\) has the desired signed cross interaction.

To produce the corresponding velocity increment, use three translations
\[
+bK,\qquad -2bK,\qquad +bK,
\]
separated by two unforced holds of duration \(\delta/2\), with
\[
b^2\delta=|c|.
\]
The magnetic carrier phases are \(+b\delta/2\) and \(-b\delta/2\); their total induction map is identity.

The smooth residual has \(L^1_tH^1_x\) budget
\[
P\left(\frac{|c|}{b}+\frac{|c|}{b^2}\right).               \tag{29}
\]
It is estimated in this norm, or removed by a small proof-only primitive. An \(L^2_tL^2_x\) estimate alone would not give the required smallness.

Choose \(b\) polynomially large, then choose the durations of the translation subcalls. The accepted plane-mode synthesis and at-most-two quadratic stages now give the arbitrary Fourier velocity writer while preserving arbitrary smooth magnetic memory.

The number of Fourier terms is polynomial, and every complete translation word has an endpoint factor \(1+\text{small}\). Prefix bounds are sums of prescribed increments; they are not repeatedly raised to a power.

The qualitative forcing-direction replacement in Nersesyan’s Theorem 2.5 is stated along a known strong trajectory. The qu