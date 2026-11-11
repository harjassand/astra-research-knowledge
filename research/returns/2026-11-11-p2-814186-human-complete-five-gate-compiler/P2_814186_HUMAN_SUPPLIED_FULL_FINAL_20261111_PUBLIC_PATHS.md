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

The qualitative forcing-direction replacement in Nersesyan’s Theorem 2.5 is stated along a known strong trajectory. The quantitative spatial synthesis used here is your stronger accepted construction, supplemented by the displayed memory estimates. [arxiv.org](https://arxiv.org/pdf/1403.5369v2?utm_source=chatgpt.com)

---

# 5. A general physical positive-heat operation

This operation permits the three outer filters. It works even when the unwanted magnetic part has amplitude \(O(Q)\) and much larger fixed-order derivative norms.

Let \(\beta_0\) be a smooth reference, possibly unknown, with a supplied bound \(P\ge2\). Assume
\[
\|B_0-\beta_0\|_{H^1}\le\zeta/16,\qquad 0<\zeta\le1.
\]

For any prescribed rational \(0<T\le1\), the following mechanical programme occupies **exactly time \(T\)** and gives
\[
\|B(T)-e^{D_\rho\Delta}\beta_0\|_{H^1}\le\zeta,
\qquad
\|u(T)\|_{H^1}\le U,                                      \tag{30}
\]
where
\[
\rho_0T/2\le D_\rho\le T.                                 \tag{31}
\]
The compiler never evaluates \(D_\rho\).

Choose a fixed computable \(C\ge100\) dominating the estimates below, and set
\[
U=\frac{\zeta\mu^2}{2^{12}CP^2},
\qquad
\eta_{\rm hold}=\frac{\zeta\mu}{2^{12}C},
\]
\[
d_0=
\frac{\zeta^8\mu^{24}}{2^{128}C^{16}P^{32}},
\qquad
J=\left\lceil T/d_0\right\rceil,
\qquad
r=\frac{\zeta}{2^{12}J}.                                  \tag{32}
\]

Compile one common memory-preserving reset with:

- endpoint velocity at most \(U/4\) in \(H^1\);
- magnetic error increment at most \(r\);
- duration \(\ell\le T/(2J)\);
- the uniform reference and state bound \(P\).

Its actual rational duration \(\ell\) is known after compilation. Set
\[
d=T/J-\ell.
\]
Then
\[
T/(2J)\le d\le d_0.
\]
Repeat reset followed by an unforced hold \(J\) times. This fills exactly \(T\).

During holds, let the proof reference solve
\[
\beta_t=\rho(t)\Delta\beta;
\]
during resets, freeze it. Its smooth norm never exceeds \(P\).

## Velocity remains small on every hold

The non-autonomous Stokes formula and the \(H^{-1/2}\) product estimate give
\[
\sup_{\rm hold}\|u\|_{H^1}
\le
U/4+C\mu^{-1}P^2d^{1/4}
+C\eta\mu^{-1/2}d^{1/2}
\le U.                                                    \tag{33}
\]
The chosen \(d_0\) is also below the polynomial local strong-existence threshold.

## One magnetic estimate covers all holds

Put \(e=B-\beta\), \(E=\|e\|_{H^1}\). On each hold,
\[
e_t=\rho\Delta e+\mathcal C_ue+\mathcal C_u\beta+h_B.
\]
Hence
\[
\boxed{
(E^2)'
+\rho_0\|e\|_{H^2}^2
\le
C\rho_0^{-3}U^4E^2
+C\rho_0^{-1}P^2U^2
+C\rho_0^{-1}\eta^2.
}                                                         \tag{34}
\]

Write
\[
a=C\mu^{-3}U^4,\qquad
b=C\mu^{-1}(P^2U^2+\eta^2).
\]
At a reset endpoint, \(E_+\le E_-+r\). Under the bootstrap \(E\le\zeta\),
\[
E_+^2-E_-^2\le2\zeta r+r^2.
\]
Thus over the entire programme,
\[
\boxed{
E(T)^2
\le e^{aT}
\left[
E(0)^2+bT+\sum_{j=1}^J(2\zeta r+r^2)
\right].
}                                                         \tag{35}
\]
The choices (32), together with the reset disturbance budget, make the right side smaller than \(\zeta^2/4\).

This is the required global estimate. No local \(h^{1/4}\) error is summed over \(T/h\) cells. There is no fixed multiplicative loss raised to \(J\).

The total unforced holding time is \(Jd\in[T/2,T]\). Since all heat factors commute,
\[
\beta(T)
=
\exp\!\left(
\Delta\sum_{\rm holds}\int\rho(t)\,dt
\right)\beta_0,
\]
which proves (30)–(31).

Finally,
\[
J\le
1+2^{128}C^{16}P^{32}\zeta^{-8}\mu^{-24}.                  \tag{36}
\]
Every reset argument, including its reciprocal duration and reciprocal tolerance, is polynomial in
\[
P,\zeta^{-1},\mu^{-1},T^{-1},\Lambda.
\]
Thus the complete heat operation has polynomial physical and binary costs for arbitrary polynomial \(P\).

---

# 6. Replacing the three abstract filters by physical ones

For each filter in §2, its exact formal input has the form
\[
L_j+H_j(Q_j),
\]
where:

- \(L_j\) is the retained reference;
- \(L_j\) is independent of the frequency \(Q_j\) being selected;
- the unwanted part is supported above \(Q_j/2\), after the stated frequency separations;
- uniformly for \(|H|\le M\),
  \[
  \|H_j(Q_j)\|_{H^1}\le C_j(1+Q_j)^2.                    \tag{37}
  \]

The coefficient \(C_j\) depends only on \(\Gamma\) and the lower pilot frequencies already chosen. The exponent two follows directly from one curl and one derivative in the \(H^1\) norm.

Given its output error allocation \(\xi_j\), first choose a rational duration
\[
0<T_j\le\tau/32
\]
so that
\[
T_j\|\Delta L_j\|_{H^1}\le\xi_j/8.                        \tag{38}
\]
Then choose \(Q_j\) large enough for separation and
\[
C_j(1+Q_j)^2e^{-\rho_0T_jQ_j^2}
\le\xi_j/8.                                              \tag{39}
\]

This requires only a polynomially large integer. For example, use
\[
e^{-x}\le 4!x^{-4}
\]
and choose \(Q_j\) as a sufficiently large fixed integer power of
\[
2+C_j+\xi_j^{-1}+(\rho_0T_j)^{-1}
+\text{the retained frequency bound}.
\]
The fixed numerical multiplier and power are generated by the precomputation; alternatively they can be chosen directly from the displayed fourth-power estimate.

Only after selecting \(Q_j\) do we instantiate the physical heat operation with its full smooth-reference bound. This bound may be a large polynomial in \(Q_j\). Section 5 permits the already selected \(T_j\); it does not impose \(T_jP^c\ll1\).

The low-frequency heat bias is bounded by (38), the unwanted part by (39), and the physical implementation error by (30).

## Backward selection prevents circularity

Name the chronological operations
\[
S_1,S_2,S_3,F_1,S_4,F_2,S_5,F_3,
\]
where the \(S_i\) are the five gates and the \(F_i\) the filters.

Design them backward:

1. Design the final memory-preserving velocity writer for \((V_N,\Pi_NH)\).
2. Design \(F_3\): its retained reference is \(\Pi_NH\). Choose \(T_3\), then \(Q_3\), then its physical heat parameters.
3. Design \(S_5\), including its microscopic gate frequency and its incoming-error allowance.
4. Design \(F_2\): its retained reference is (11), which depends on \(Q_3\), already fixed. Choose \(T_2,Q_2\), then \(S_4\).
5. Design \(F_1\): its retained reference is (9), which depends on \(Q_2\), already fixed. Choose \(T_1,Q_1\), then \(S_3\).
6. Design \(S_2\), then \(S_1\).
7. Compute the required initial preparation tolerance.

For a service with
\[
e_{\rm out}\le G e_{\rm in}+\sigma
\]
and a known admissible input radius, first assign \(\sigma\) a fixed fraction of its output budget. Construct the service and compute its polynomial \(G\). Then assign its incoming budget.

No later prescribed reference contains an earlier discarded microscopic frequency. An incoming discrepancy is controlled only in \(H^1\), with no bound on its hidden higher derivatives.

There are only five gate services and three outer filters. Therefore all frequency and reciprocal-tolerance choices are compositions of a fixed number of polynomial functions.

---

# 7. Completing the physical programme and covering all weak realizations

Give each of the five gate services, three filters, and final velocity writer a duration cap \(\tau/32\). Let the exact rational duration of their compiled concatenation be \(D\). Then
\[
D\le9\tau/32<\tau/2.
\]

Set
\[
a=\tau/8,\qquad T_0=\tau-D-a.
\]
Thus \(T_0>\tau/2\).

Use the accepted common compiler for endpoint \((0,H)\) on the initial interval of length \(T_0\), with accuracy chosen from the backward error allowance. Follow it by an unforced interval of length \(a\). The magnetic writer and final velocity writer then end exactly at \(\tau\).

## Preparing a small \(H^1\) discrepancy

Let \(b=B-H\). At the eraser endpoint suppose
\[
\|(u,b)\|_2\le\delta_e.
\]
The unforced total fluctuation energy gives
\[
\sup\|(u,b)\|_2\le\delta_e+\eta a,
\qquad
\int_0^a\|\nabla(u,b)\|_2^2
\le C\mu^{-1}(\delta_e+\eta a)^2.                          \tag{40}
\]

At an almost-everywhere regular time in the first half of this interval,
\[
\|(u,b)\|_{H^1}
\le
\frac{C(\delta_e+\eta a)}{\sqrt{\mu a}}.
\]
This is a proof time, not an observation or a selected control time.

The constant-\(H\) coupling cancels in the joint \(H^1\) energy. Consequently,
\[
E_1'+c\mu E_1
\le C\mu^{-3}E_1^3+C\mu^{-1}\eta^2.                       \tag{41}
\]
For the required initial writer allowance \(\beta_0\), reduce it if necessary so that \(\beta_0\le c\mu\), and choose
\[
\delta_e\le c\beta_0\mu a,\qquad
\eta\le c\mu\beta_0.
\]
The end of the prescribed preparation interval then satisfies
\[
\|(u,B-H)\|_{H^1}\le\beta_0.                              \tag{42}
\]
All reciprocal quantities here are polynomial.

## Endpoint error

Assign the backward budgets so that the magnetic programme ends within \(\epsilon/8\) of \(\Pi_NH\) in \(H^1\), and the final velocity operation contributes at most another \(\epsilon/8\) of magnetic error while writing \(V_N\) within \(\epsilon/8\).

Combining these bounds with (2) gives, with room for rational rounding and disturbance budgets,
\[
\|u(\tau)-V\|_2+\|B(\tau)-\Pi H\|_2<\epsilon.
\]
This implies the requested joint Euclidean bound.

## Why every energy weak realization is covered

The preparation argument places every admitted realization in the same small \(H^1\) region at the prescribed writing start time.

On every subsequent physical segment:

- the transformed joint \(H^1\) estimates give controlled strong continuation;
- all carriers are finite smooth fields with ordinary finite amplitudes;
- the disturbances are the actual admitted \(L^\infty_tL^2_x\) disturbances;
- weak–strong uniqueness identifies every energy-admissible weak realization with the controlled strong solution.

Uniqueness is used with zero initial discrepancy. Its potentially large Grönwall coefficient is not used to choose a disturbance tolerance.

At the final time the fields have strong traces. These agree with the required one-sided total-energy trace.

All means are preserved throughout: the magnetic reference and the actual magnetic field retain the same \(H\), and every emitted force has zero mean.

---

# 8. The compiler and its universal resource certificate

Here is the compiler at the level of its deterministic subroutines:

```text
Canonicalize and truncate V and Pi.
Compute the rational normalized curl potential Gamma.

Design the final memory-preserving velocity writer.

For j = 3, 2, 1:
    Choose the outer filter duration from its retained reference.
    Choose the integer pilot frequency Q_j by a polynomial inequality.
    Compile the general physical heat operation.
    Compile the corresponding whole-field magnetic gate.
    Propagate the required input-error allowance backward.

Compile the two encoding gates backward.
Compute the initial H1 preparation allowance.

Compute the exact duration D of the writing programme.
Set a = tau/8 and T0 = tau - D - a.
Compile the accepted (0,H) eraser on [0,T0].
Append the unforced preparation interval.
Append the magnetic programme and final velocity writer.

Choose eta as a fixed fraction of the minimum of all disturbance budgets.
Expand all local time polynomials into ordinary rational time polynomials.
Output the twelve coefficient lists and eta.
```

The reset, heat, and final-writer subroutines have been specified above. The whole-field gate uses your supplied quantitative gate and physical lift, whose closed-memory hypotheses are supplied by §3–§4.

## Fixed finite precomputation

Choose the accepted fixed erasing catalogue and its rational saturation certificates once. Let its depth be \(D_0\). Choose a fixed spatial differentiation order, for example
\[
m_*=64+8D_0.
\]

The precomputation consists of:

1. The accepted erasing-word, long-shear, plane-mode, and two-stage Fourier certificates, including their quantitative polynomial bounds.
2. Product, interpolation, commutator, and elliptic estimates through order \(m_*\).
3. The finite derivative recurrences for the shear and wavepacket flows.
4. The polynomial bounds in the reset, setter, heat, and filter estimates above.

These constants require no norm oracle. For finite Fourier fields use (3). Sobolev and Agmon constants can be bounded by Fourier-shell sums. Elliptic inverse bounds follow by energy estimates and finitely many spatial differentiations. Product and chain-rule coefficients are obtained by finite multi-index enumeration. Every remaining Young inequality uses a fixed rational exponent.

All resulting bounds can be represented by polynomials with nonnegative rational coefficients. Integer ceilings give nonnegative integer-coefficient majorants.

This also specifies the constants \(A,p\): perform symbolic resource accounting on the fixed subroutine dependency graph, substituting the accepted resource polynomials and the newly computed majorants. Let the resulting univariate majorant be \(Q(X)\), enlarged to cover both numerical resources and bit resources. Include the operation count, memory, and description size of the finite precomputation itself.

Define
\[
p=\max(1,\deg Q),
\]
and take \(A\) to be a computable integer exceeding the coefficient sum of the rescaled majorant and the complete fixed precomputation cost. Thus \(A,p\) are defined by a terminating finite arithmetic procedure, chosen once, independently of every variable input.

## Why the accounting yields a fixed polynomial

The relevant points are:

- After truncation, all spatial bounds are polynomial in \(R\).
- The five-gate, three-filter dependency chain has fixed depth.
- The erasing catalogue has fixed saturation depth.
- Variable Fourier velocity synthesis has at most two quadratic stages.
- Repeated heat cells use one common endpoint state bound. Their cost is \(J\) times a polynomial, rather than a polynomial composed with itself \(J\) times.
- The same property holds for the repeated physical-flow cells inside a gate.
- Tiny coefficients are handled by absolute error budgets; no inverse tiny coefficient is charged as a numerical parameter.
- Every actual time interval, including every inserted reset and hold, is included in the rational clock.
- The output force always lies in the twelve fundamental mechanical directions.

The symbolic accounting therefore gives
\[
\eta^{-1}+\sup_t\|f(t)\|_{W^{1,\infty}}
\le AR^p.
\]
Since \(\tau\le1\),
\[
\int_0^\tau\|f(t)\|_{W^{1,\infty}}\,dt\le AR^p
\]
after the same enlargement of \(A\).

Exact rational arithmetic, canonicalization, convolution, root bisection, and paid \(\pi\)-enclosures have polynomial bit cost in \(L+R\). The number of intervals, time-polynomial degrees, output bits, working-memory bits, and individual rational bit lengths satisfy
\[
AR^p\quad\text{or, where input precision enters,}\quad
A(L+R)^p.
\]
Large input denominators affect bit arithmetic. They do not affect the numerical forcing bounds.

The proof-only quantities
\[
H,\quad \nu(t),\quad \rho(t),\quad
\chi,\quad a_\nu,\quad D_\rho,
\]
and the actual-viscosity Navier–Stokes references are never evaluated by the compiler.

---

## Conclusion

The fixed-depth assembly resolves the arbitrary-\(\Pi\) step:

\[
\boxed{
H
\ \xrightarrow{\;2\ \text{encoding gates}\;}
\text{three flux components in pilot modes}
\ \xrightarrow{\;3\ \text{row-writing gates and filters}\;}
\Pi_NH.
}
\]

The memory-preserving reset and general positive-heat estimate make the filters actual operations of the coupled MHD system. The final closed-word velocity writer produces \(V_N\) while retaining the written magnetic response.

Consequently, **under the accepted constructions in the question, one total deterministic twelve-actuator compiler satisfies the complete unknown-flux, unknown time-dependent diffusivity, disturbance, all-energy-weak-realization, variable-target, and uniform polynomial-resource contract.**
