# P2 completed return — 657d797e

Chat: https://chatgpt.com/c/6af2d0d2-f500-83ec-a7d0-20e80bd42677
Model: GPT-6 Pro, as observed. Exact question: `work/astra-renewed-pro-programmes-20261103/P2_POLYNOMIAL_PHYSICAL_COST_FULL_PRO_20261110.txt` (approved one-final-LF omission). No original ZIP appeared in the response or visible outputs.

The native reader limits the response to 20,000 characters. Its Markdown prefix is preserved below, followed by the full visible answer and activity in the browser accessibility representation, which splits mathematical notation across elements. The native serialization is not literal source-byte identity.

## Native response prefix (truncated at 20,000 characters)

## Answer: yes, using the constructive macro-word premises you supplied

Those premises are sufficient to obtain the full polynomial-resource compiler.

The missing step is an \(H^1\) estimate in **coordinates that reset after each macro-word**. Within one block, the conjugated Laplacian differs from the ordinary Laplacian by \(O(s)\), so viscosity remains coercive. At the block boundary, resetting the coordinates costs \(1+O(s^5)\) in \(H^1\). Consequently, the nonlinear argument depends on \(ns^5\), which can be kept small, without paying an exponential in the accumulated strain \(ns\).

This gives, with fixed computable constants, the following nonoptimized bounds:

| Resource | Bound obtained below |
|---|---:|
| Number of time intervals | \(C R^{28}\) |
| Degree of every time polynomial | At most \(2\) |
| \(\displaystyle\sup_t\|f(t)\|_{W^{1,\infty}}\) | \(C R^{66}\) |
| \(\displaystyle\int_0^\tau\|f(t)\|_{W^{1,\infty}}\,dt\) | \(C R^{58}\) |
| Disturbance tolerance | \(\eta^{-1}\le 32R\) |
| Individual rational bit lengths | \(C(L+\log R+1)\) |
| Total computation, memory, and output | A fixed polynomial in \(L+R\) |

A common exponent **\(p=128\)** is more than sufficient. I specify below how the fixed constant \(A\), including the entire granted fixed-family precomputation, is computed.

The proof uses your premises 1–2 as accepted constructive mathematics. The suggested Koike–Nersesyan–Rissel–Tucsnak paper concerns passive-scalar relaxation through controlled two-dimensional Euler flows; the total-velocity estimate needed here is proved below directly for the three-dimensional Navier–Stokes equation. :chatgpt-content-reference{index="0"}

---

## 1. Fixed data and notation

Work on \(\mathbb T^3=\mathbb R^3/\mathbb Z^3\), with
\[
\|u\|_{H^m}=\|(I-\Delta)^{m/2}u\|_2.
\]
All vector fields below are mean-zero and divergence-free. Write
\[
B(u,v)=\mathbb P[(u\cdot\nabla)v],
\qquad
L_Fv=B(F,v)+B(v,F),
\]
where \(\mathbb P\) is the Leray projection.

Execute the effective fixed-family construction granted in premise 1. Flatten its fixed word into a finite list of shear factors, with signs chosen so that
\[
W(s)
=
e^{-\alpha_m sL_{F_m}}\cdots e^{-\alpha_1sL_{F_1}},
\tag{1}
\]
where
\[
F_\ell=G_{\jmath_\ell},\qquad \alpha_\ell\in\mathbb Q.
\]
The rational design weights are incorporated into the fixed word using its rational pulse descriptions and fixed multiplicities.

The fixed precomputation returns:

- The complete rational Fourier descriptions of the \(G_j\).
- The finite signed-letter list \((\jmath_\ell,\alpha_\ell)_{\ell=1}^m\).
- A positive rational lower bound \(c\) in
  \[
  \operatorname{Sym}D(k)\le-\frac{c}{1+|k|^2}I.
  \]
- Rational upper bounds \(C_0,c_1,b_0,b_1,b_2\) and a common admissible small-\(s\) range, such that
  \[
  \|W(s)-e^{s^4D}\|_{2\to2}\le C_0s^5,
  \tag{2}
  \]
  \[
  \|W(s)-e^{s^4D}\|_{H^1\to H^1}\le c_1s^5,
  \tag{3}
  \]
  and every partial block and its inverse have \(H^j\) norms at most \(e^{b_js}\), for \(j=0,1,2\).

Only these three Sobolev orders are needed.

Because \(D\) commutes with the scalar Sobolev weights and has negative symmetric part,
\[
\|e^{tD}\|_{H^j\to H^j}\le1.
\]
In particular,
\[
\|W(s)\|_{H^1\to H^1}\le1+c_1s^5.
\tag{4}
\]

For a path consisting of \(n\) blocks, the supplied forward-propagator estimate gives
\[
\|S(t,r)\|_{2\to2}
\le
\exp\!\left(2b_0s+C_0ns^5\right),
\qquad r\le t.
\tag{5}
\]

All constants used subsequently will be calculated from this finite data.

---

## 2. The new estimate: viscosity survives a change of coordinates within one block

Let \(w(t)\) be the prescribed shear carrier. During a single pulse,
\[
w(t)=a(t)F_\ell,
\]
and over a complete macro-block,
\[
\int_{\text{block}}|a(t)|\,dt
\]
summed over its letters equals
\[
s\sum_{\ell=1}^m|\alpha_\ell|.
\tag{6}
\]

This quantity is independent of how quickly the block is executed.

Let \(I_j=[t_j,t_{j+1}]\) be one macro-block and define its inviscid propagator
\[
P_j(t)=S(t,t_j),\qquad
\partial_tP_j=-L_{w(t)}P_j,\qquad P_j(t_j)=I.
\]

Choose a fixed small-\(s\) threshold so that
\[
\|P_j(t)^{\pm1}\|_{H^a\to H^a}\le2,
\qquad a=0,1,2.
\tag{7}
\]

### 2.1 The commutator has only two derivatives of the unknown

Since \(\mathbb P\) commutes with \(\Delta\),
\[
\begin{aligned}
[\Delta,L_F]u
=\mathbb P\Big[
&((\Delta F)\cdot\nabla)u
+2\sum_{a=1}^3((\partial_aF)\cdot\nabla)\partial_a u\\
&+2\sum_{a=1}^3((\partial_a u)\cdot\nabla)\partial_aF
+(u\cdot\nabla)\Delta F
\Big].
\end{aligned}
\tag{8}
\]
Therefore
\[
\|[\Delta,L_F]u\|_2\le C_F\|u\|_{H^2}.
\tag{9}
\]

Each \(C_F\) has an explicit rational upper bound obtained directly from the finite Fourier coefficients of \(F\), using derivatives through order three. For example, replace every factor \(2\pi\) in a Fourier derivative bound by \(8\), and bound the resulting trigonometric polynomial by the sum of the absolute values of its coefficients. No norm oracle is involved.

### 2.2 Conjugation changes the Laplacian by \(O(s)\)

On smooth fields,
\[
\frac{d}{dt}\bigl(P_j^{-1}\Delta P_j\bigr)
=
P_j^{-1}[L_{w(t)},\Delta]P_j.
\tag{10}
\]
Using (6), (7), and (9), integration gives
\[
\boxed{
\|P_j^{-1}\Delta P_j-\Delta\|_{H^2\to L^2}
\le C_\Delta s.
}
\tag{11}
\]
For example, one may use
\[
C_\Delta=4\sum_{\ell=1}^m|\alpha_\ell|C_{F_\ell}.
\]
The identity and estimate extend from smooth fields by density.

Shrink the fixed threshold so that
\[
C_\Delta s\le\frac18.
\tag{12}
\]

For mean-zero fields on the unit torus,
\[
-\langle\Delta z,(I-\Delta)z\rangle
=
\|\nabla z\|_2^2+\|\Delta z\|_2^2
\ge\frac12\|z\|_{H^2}^2,
\tag{13}
\]
because every nonzero Laplace eigenvalue is at least \(4\pi^2>1\).

Equations (11)–(13) give the required coercivity. Crucially, they depend on the impulse in **one block**, rather than the strain accumulated over the entire repeated path.

---

## 3. A uniform nonlinear estimate throughout the active interval

Suppose the carrier occupies \([0,\delta]\), starts and ends at zero, and contains \(n\) complete macro-blocks.

Its ideal force is
\[
f_*=w_t+B(w,w)-\nu\Delta w.
\]
Only one shear is active at a time, so
\[
B(w,w)=0,\qquad f_*=w_t-\nu\Delta w.
\tag{14}
\]

Allow a rational approximation \(f\) with
\[
\|f-f_*\|_{L^\infty L^2}\le\xi.
\]
For each actual disturbance \(h\), define
\[
v=U-w,\qquad g=h+(f-f_*),\qquad a_*=\eta+\xi.
\]
Then
\[
v_t+L_wv=\nu\Delta v-B(v,v)+g.
\tag{15}
\]

Assume for the moment that \(a_*\le1\).

### 3.1 Reset the coordinates after each block

Within block \(j\), set
\[
z=P_j^{-1}v.
\]
The transformed equation is
\[
z_t
=
\nu P_j^{-1}\Delta P_jz
-P_j^{-1}B(P_jz,P_jz)
+P_j^{-1}g.
\tag{16}
\]

At the next block boundary the new propagator starts at the identity. Accordingly,
\[
z(t_{j+1}+)=W(s)z(t_{j+1}-).
\tag{17}
\]

This reset is an operation in the proof. The physical velocity remains continuous, and the prescribed force is unaffected.

### 3.2 An explicit nonlinear constant

An elementary Fourier estimate on the unit torus gives
\[
\|u\|_\infty
\le16\|u\|_{H^1}^{1/2}\|u\|_{H^2}^{1/2}.
\tag{18}
\]
Here is one way to make the constant effective. The shell
\[
\{k\in\mathbb Z^3:|k|_\infty=j\}
\]
contains \(24j^2+2\le26j^2\) points. Splitting the Fourier sum at
\[
N=\left\lceil\frac{\|u\|_{H^2}}{\|u\|_{H^1}}\right\rceil
\]
bounds the low-frequency reciprocal \(H^1\)-weight sum by \(26N\), and the high-frequency reciprocal \(H^2\)-weight sum by \(26/N\). Cauchy–Schwarz then gives (18). The zero field is immediate.

Consequently,
\[
\|B(u,u)\|_2
\le16\|u\|_{H^1}^{3/2}\|u\|_{H^2}^{1/2}.
\tag{19}
\]

Put
\[
E=\|z\|_{H^1}^2,\qquad Z=\|z\|_{H^2}.
\]
By (7) and (19),
\[
\|P_j^{-1}B(P_jz,P_jz)\|_2
\le128E^{3/4}Z^{1/2}.
\tag{20}
\]

### 3.3 The energy inequality

Pair (16) with \((I-\Delta)z\). Equations (11)–(13) imply
\[
\frac12E'
\le
-\frac{\nu}{2}Z^2+\frac{\nu}{8}Z^2
+128E^{3/4}Z^{3/2}+2a_*Z.
\]
Use
\[
128E^{3/4}Z^{3/2}
\le
\frac{\nu}{8}Z^2
+54\cdot128^4\nu^{-3}E^3,
\]
and
\[
2a_*Z\le\frac{\nu}{8}Z^2+8\nu^{-1}a_*^2.
\]
Thus, with the explicit integer
\[
C_E=108\cdot128^4,
\]
we have
\[
\boxed{
E'+\frac{\nu}{4}Z^2
\le C_E\nu^{-3}E^3+C_E\nu^{-1}a_*^2.
}
\tag{21}
\]

There is no carrier amplitude, pulse frequency, \(ns\), or accumulated-strain exponential in this inequality.

### 3.4 Accounting for every reset

By (4) and (17),
\[
E(t_{j+1}+)\le qE(t_{j+1}-),
\qquad q=(1+c_1s^5)^2.
\]
Require
\[
q^n\le2.
\tag{22}
\]

On block \(j\), define
\[
\mathcal E=q^{-j}E.
\]
It has no upward jump at a reset, and (21) gives
\[
\mathcal E'
+\frac{\nu}{4}q^{-j}Z^2
\le4C_E\nu^{-3}\mathcal E^3+C_E\nu^{-1}a_*^2.
\tag{23}
\]

Since \(\mathcal E(0)\le M^2\), the bootstrap
\[
\mathcal E\le2M^2
\]
closes provided
\[
\boxed{
\delta\le\frac{\nu^3}{128C_EM^4}.
}
\tag{24}
\]
Indeed, while the bootstrap holds, the right-hand side of (23) is at most
\[
33C_E\nu^{-3}M^6,
\]
using \(a_*\le1\), \(M\ge1\), and \(\nu\le1\). Over (24), this increases the weighted energy by less than \(M^2\).

Integrating (23), and using \(q^{-j}\ge1/2\), gives
\[
\nu\int_0^\delta Z^2\,dt\le16M^2.
\]
Returning to \(v=P_jz\),
\[
\boxed{
\sup_{0\le t\le\delta}\|v(t)\|_{H^1}\le4M,
\qquad
\nu\int_0^\delta\|v(t)\|_{H^2}^2\,dt\le64M^2.
}
\tag{25}
\]

### 3.5 Why this covers every Leray–Hopf realization

For each fixed compiler output, \(w\) is continuous, piecewise polynomial in time, and smooth in space. The actual force belongs to \(L^\infty_tL^2_x\). Local \(H^1\) strong existence therefore applies; the estimate (25) prevents loss of \(H^1\) regularity before \(\delta\), so the solution continues throughout the active interval. These are the usual local strong-solution and continuation mechanisms for three-dimensional Navier–Stokes. :chatgpt-content-reference{index="1"}

For each actual \(h\), this produces
\[
U_*=w+v\in L^\infty(0,\delta;H^1)\cap L^2(0,\delta;H^2).
\]
Weak–strong uniqueness identifies every corresponding Leray–Hopf solution with \(U_*\) on that interval.

The uniqueness argument may contain a very large finite Grönwall factor. Its initial discrepancy is exactly zero. **No disturbance tolerance or physical resource is chosen using that factor.** Quantitative robustness comes from (21)–(25), applied separately to each actual disturbance.

---

## 4. The resulting endpoint comparison is polynomial

Arrange also that (5) gives
\[
\sup_{0\le r\le t\le\delta}\|S(t,r)\|_{2\to2}\le2.
\tag{26}
\]

Equation (15) has the \(L^2\) variation-of-constants formula
\[
v(\delta)-W(s)^nU_0
=
\int_0^\delta
S(\delta,t)\bigl[\nu\Delta v-B(v,v)+g\bigr]\,dt.
\tag{27}
\]
The residual is in \(L^1_tL^2_x\) by (25), so this is a legitimate strong-solution formula.

First,
\[
\nu\int_0^\delta\|\Delta v\|_2\,dt
\le8M\sqrt{\nu\delta}.
\]
Second, by (19), (25), and Hölder,
\[
\begin{aligned}
\int_0^\delta\|B(v,v)\|_2\,dt
&\le
16(4M)^{3/2}\delta^{3/4}
\left(\int_0^\delta\|v\|_{H^2}^2\,dt\right)^{1/4}\\
&\le384M^2\delta^{3/4}\nu^{-1/4}.
\end{aligned}
\]
Multiplying by the forward-propagator bound \(2\) yields
\[
\boxed{
\|U(\delta)-W(s)^nU_0\|_2
\le
16M\sqrt{\nu\delta}
+768M^2\delta^{3/4}\nu^{-1/4}
+2a_*\delta.
}
\tag{28}
\]
Here \(w(\delta)=0\), so the left side concerns **total velocity** at the end of the active interval.

This is the quantitative replacement for the supplied estimate containing \(e^K\).

---

## 5. Explicit fixed constants and variable parameter choices

### 5.1 Finish the fixed precomputation

Choose a positive rational \(\sigma\) lying in the common admissible range of the supplied estimates and satisfying
\[
\sigma\le
\frac{1}{16(1+b_0+b_1+b_2+C_\Delta)}.
\tag{29}
\]
This ensures all the partial-propagator and commutator requirements above.

Choose the integer
\[
C_D=1+\lceil c^{-1}\rceil.
\]
The Fourier multiplier estimate gives
\[
\|e^{TD}J\|_{2\to2}\le C_DT^{-1/2}.
\tag{30}
\]
Indeed, putting \(y=1+|k|^2\),
\[
\frac{e^{-cT/y}}{\sqrt{1+4\pi^2|k|^2}}
\le y^{-1/2}e^{-cT/y},
\]
whose supremum over \(y>0\) is \((2ecT)^{-1/2}\).

Now compute a fixed integer \(B_*\) satisfying
\[
\boxed{
B_*\ge
\max\left\{
2,\sigma^{-1},16C_0,4c_1,
128C_E,64C_D^2,(12\cdot1024)^2
\right\}.
}
\tag{31}
\]
A ceiling of the displayed maximum suffices.

Everything in (29)–(31) is fixed, rationally computable, and independent of the variable inputs.

### 5.2 Online parameters

For an input \((M,\nu,\tau,\epsilon)\), compute the integer
\[
\rho=
2+\lceil M\rceil+\lceil\nu^{-1}\rceil
+\lceil\tau^{-1}\rceil+\lceil\epsilon^{-1}\rceil.
\tag{32}
\]
Then
\[
R\le\rho<R+4\le2R,
\tag{33}
\]
and
\[
M\le\rho,\qquad
\nu^{-1}\le\rho,\qquad
\tau^{-1}\le\rho,\qquad
\epsilon^{-1}\le\rho.
\]

Set
\[
\boxed{
\begin{aligned}
T&=B_*\rho^4,\\
s&=\frac1{B_*^2\rho^6},\\
n&=B_*^9\rho^{28},\\
\delta&=\frac1{B_*\rho^8},\\
\eta&=\frac1{16\rho}.
\end{aligned}}
\tag{34}
\]
All these quantities are rational, and \(n\) is an integer. In particular,
\[
ns^4=T,\qquad ns^5=\frac1{B_*\rho^2}.
\tag{35}
\]

### 5.3 Verification of the stability requirements

By (29), (31), and (34), \(s\le\sigma\).

Moreover,
\[
q^n
\le\exp(2c_1ns^5)
\le\exp(2c_1/B_*)<2,
\]
and
\[
\exp(2b_0s+C_0ns^5)<2.
\]
Thus (22) and (26) hold.

Also,
\[
\nu^3M^{-4}\ge\rho^{-7}.
\]
Since \(B_*\ge128C_E\),
\[
\delta=\frac1{B_*\rho^8}
\le\frac{\nu^3}{128C_EM^4}.
\]
Finally, \(\delta\le\tau/2\).

### 5.4 Verification of the linear target

By (30),
\[
\|e^{TD}U_0\|_2
\le MC_DT^{-1/2}
\le\frac{C_D}{\sqrt{B_*}}\rho^{-1}
\le\frac{\epsilon}{8}.
\tag{36}
\]

The supplied word error gives
\[
\begin{aligned}
\|(W(s)^n-e^{TD})U_0\|_2
&\le MC_0ns^5e^{C_0ns^5}\\
&\le\frac{2C_0}{B_*}\rho^{-1}
\le\frac{\epsilon}{8}.
\end{aligned}
\tag{37}
\]
Therefore
\[
\boxed{\|W(s)^nU_0\|_2\le\epsilon/4.}
\tag{38}
\]

### 5.5 Verification of the nonlinear error

Use \(a_*\le1\) in (28). Its right-hand side is at most
\[
16B_*^{-1/2}\rho^{-3}
+
768B_*^{-3/4}\rho^{-15/4}
+
2B_*^{-1}\rho^{-8}.
\tag{39}
\]
Since \(\epsilon\ge\rho^{-1}\), the choice
\[
B_*\ge(12\cdot1024)^2
\]
makes (39) at most \(\epsilon/4\).

Combining this with (38),
\[
\boxed{\|U(\delta)\|_2\le\epsilon/2.}
\tag{40}
\]

---

## 6. The actual rational piecewise-polynomial force

It remains to implement the carrier and approximate its viscosity term using rational coefficients.

### 6.1 Quadratic pulses

There are \(mn\) pulses. Give each pulse the rational duration
\[
d=\frac{\delta}{mn}
=\frac1{mB_*^{10}\rho^{36}}.
\tag{41}
\]
Let
\[
q(z)=6z(1-z),\qquad \int_0^1q(z)\,dz=1.
\]

For pulse \(i\), put
\[
t_i=id,\qquad
\ell=1+(i\bmod m),\qquad
\zeta=\frac{t-t_i}{d}.
\]
Define
\[
w(t,x)
=
\frac{\alpha_\ell s}{d}q(\zeta)G_{\jmath_\ell}(x),
\qquad t_i\le t\le t_{i+1}.
\tag{42}
\]
Its signed impulse is precisely \(\alpha_\ell s\). Hence the inviscid endpoint operator is exactly \(W(s)^n\).

The carrier vanishes at every pulse boundary because \(q(0)=q(1)=0\). It is continuous throughout, and its time derivative is bounded and piecewise polynomial. This produces ordinary forcing with no distributional impulses.

### 6.2 Rational approximation of the Laplacian eigenvalues

Each selected shear is a single Fourier mode with an integer wavevector \(k_j\), so
\[
-\Delta G_j=\kappa^2|k_j|^2G_j,\qquad \kappa=2\pi.
\]
The ideal coefficient on a pulse would be
\[
\frac{\alpha_\ell s}{d^2}q'(\zeta)
+
\nu\kappa^2|k_{\jmath_\ell}|^2
\frac{\alpha_\ell s}{d}q(\zeta).
\tag{43}
\]

Compute a rational dyadic number \(\theta\) approximating \(\kappa^2\), and output
\[
\boxed{
c_{\jmath_\ell}(t)
=
\frac{\alpha_\ell s}{d^2}q'(\zeta)
+
\nu\theta|k_{\jmath_\ell}|^2
\frac{\alpha_\ell s}{d}q(\zeta).
}
\tag{44}
\]
All other coefficients are zero on that pulse.

The compiler expands (44) into an ordinary polynomial in \(t\). Its degree is at most two, with rational coefficients.

For a completely explicit error rule, precompute rational bounds
\[
H_0\ge\max_j\|G_j\|_2,\quad
K_2\ge\max_j|k_j|^2,\quad
\alpha_*\ge\max_\ell|\alpha_\ell|,
\]
all at least one, and put
\[
H_w=2\alpha_*s/d.
\]
It suffices to require
\[
|\theta-\kappa^2|
\le
\frac{\eta}{1+K_2H_0H_w}.
\tag{45}
\]
Since \(\nu\le1\), this guarantees
\[
\|f-f_*\|_{L^\infty L^2}\le\eta.
\tag{46}
\]
Thus we take
\[
\xi=\eta,\qquad a_*\le2\eta=\frac1{8\rho}<1,
\]
as required above.

One deterministic rational implementation of (45) uses
\[
\pi=16\arctan(1/5)-4\arctan(1/239)
\]
with the alternating power series and its explicit remainder bounds, followed by rational squaring and dyadic rounding. The required precision is \(O(\log\rho)\), with a fixed additive constant from the precomputation.

### 6.3 Switch off the control

Set every \(c_j=0\) on \((\delta,\tau]\).

For every Leray–Hopf continuation, the energy inequality gives
\[
\|U(t)\|_2
\le\|U(\delta)\|_2+\int_\delta^t\|h(r)\|_2\,dr.
\tag{47}
\]
The inequality can be started at \(\delta\) by approaching it through admissible starting times from below, where the solution agrees with the strong solution and is strongly continuous. Taking the specified one-sided energy trace gives the same bound at \(t=\tau\).

Consequently,
\[
\begin{aligned}
\|U(\tau)\|_2
&\le\frac{\epsilon}{2}+\eta(\tau-\delta)\\
&\le\frac{\epsilon}{2}+\frac1{16\rho}\\
&\le\frac{9\epsilon}{16}
<\epsilon.
\end{aligned}
\tag{48}
\]

This proves the endpoint contract for every admissible initial state, disturbance, and Leray–Hopf realization.

---

## 7. Physical resource bounds

The pulse duration (41) gives the exact scalings
\[
\frac{s}{d}=mB_*^8\rho^{30},
\qquad
\frac{s}{d^2}=m^2B_*^{18}\rho^{66}.
\tag{49}
\]
All spatial fields belong to the fixed finite family.

Choose a fixed rational bound
\[
H_1\ge\max_j\|G_j\|_{W^{1,\infty}}.
\]
We may keep \(|\theta|\le65\), since \(4\pi^2<64\). Using
\[
\|q\|_\infty=\frac32,\qquad \|q'\|_\infty=6,
\]
equation (44) gives
\[
\sup_t\|f(t)\|_{W^{1,\infty}}
\le C_f\rho^{66},
\tag{50}
\]
where, for example, the fixed computable constant
\[
C_f=
H_1\alpha_*
\left(6m^2B_*^{18}+100K_2mB_*^8\right)
\tag{51}
\]
suffices.

The force is supported on \([0,\delta]\), so
\[
\int_0^\tau\|f(t)\|_{W^{1,\infty}}\,dt
\le\frac{C_f}{B_*}\rho^{58}.
\tag{52}
\]
Also,
\[
\eta^{-1}=16\rho\le32R.
\tag{53}
\]
Using \(\rho\le2R\), these are the claimed polynomial physical bounds.

The number of intervals, including the final zero-force interval, is
\[
mn+1=mB_*^9\rho^{28}+1.
\tag{54}
\]

---

## 8. Bit complexity and payment for the fixed precomputation

### 8.1 The online compiler uses finite arithmetic

The online algorithm is:

1. Read the rational inputs and calculate \(\rho\).
2. Calculate \(s,n,\delta,\eta,d\) using (34) and (41).
3. Calculate the rational approximation \(\theta\) satisfying (45).
4. Emit the \(mn\) quadratic pulse records from (44), expanded in global time.
5. Emit the final zero-force interval and \(\eta\).

It evaluates no PDE solution, unknown initial condition, disturbance, optimization problem, or infinite-dimensional norm.

The integers \(n\), the interval endpoints, and all pulse parameters have \(O(L+\log\rho)\) bits, with fixed additive constants.

Expanding a polynomial into global time can produce coefficients with numerical magnitudes as large as \(C\rho^{102}\), because of factors \(d^{-3}\). Their bit lengths are still
\[
O(L+\log\rho).
\]
The actual force values obey (50); the expansion introduces no extra physical cost.

The certified arctangent calculation needs polynomially many bit operations in the requested precision. Using elementary exact rational arithmetic, a deliberately loose overall online bound is
\[
C_{\rm arith}(\rho^{28}+1)
(L+\log_2\rho+1)^8,
\tag{55}
\]
for a fixed computable \(C_{\rm arith}\). Total output bits and working-memory bits satisfy bounds of this form as well.

### 8.2 A specified finite precomputation

The precomputation consists of:

1. Executing the effective fixed-family and word construction granted in your premises, retaining its full descriptions, bounds, and finite resource certificate.
2. Computing the commutator bounds from the returned Fourier data.
3. Computing \(\sigma,C_D,C_E,B_*\), and the fixed force and arithmetic bounds.
4. Fixing the exact rational-output encoding and sc

## Complete visible response (accessibility representation)

heading ChatGPT said:, Value: 4
									45 text ChatGPT said:
								46 heading Answer: yes, using the constructive macro-word premises you supplied, Value: 2
									47 text Answer: yes, using the constructive macro-word premises you supplied
								48 text Those premises are sufficient to obtain the full polynomial-resource compiler. The missing step is an 
								49 container
									50 text 𝐻 1
								51 text  estimate in 
								52 text coordinates that reset after each macro-word
								53 text . Within one block, the conjugated Laplacian differs from the ordinary Laplacian by 
								54 container
									55 text 𝑂 ( 𝑠 )
								56 text , so viscosity remains coercive. At the block boundary, resetting the coordinates costs 
								57 container
									58 text 1 + 𝑂 (
									59 text 𝑠
									60 text 5
									61 text )
								62 text  in 
								63 container
									64 text 𝐻 1
								65 text . Consequently, the nonlinear argument depends on 
								66 container
									67 text 𝑛
									68 text 𝑠
									69 text 5
								70 text , which can be kept small, without paying an exponential in the accumulated strain 
								71 container
									72 text 𝑛 𝑠
								73 text . This gives, with fixed computable constants, the following nonoptimized bounds:
								74 table
									75 row
										76 cell
											77 text Resource
										78 cell
											79 text Bound obtained below
									80 row
										81 cell
											82 text Number of time intervals
										83 cell
											84 container
												85 text 𝐶
												86 text 𝑅
												87 text 28
									88 row
										89 cell
											90 text Degree of every time polynomial
										91 cell
											92 text At most 
											93 text 2
									94 row
										95 cell
											96 container
												97 container
													98 text sup ⁡
												99 text 𝑡
												100 text ∣ 𝑓 ( 𝑡 )
												101 text ∣
												102 container
													103 text 𝑊
													104 text 1
													105 text ,
													106 text ∞
										107 cell
											108 container
												109 text 𝐶
												110 text 𝑅
												111 text 66
									112 row
										113 cell
											114 container
												115 text ∫
												116 text 0
												117 text 𝜏
												118 text ∣ 𝑓 ( 𝑡 )
												119 text ∣
												120 container
													121 text 𝑊
													122 text 1
													123 text ,
													124 text ∞
												125 text 𝑑 𝑡
										126 cell
											127 container
												128 text 𝐶
												129 text 𝑅
												130 text 58
									131 row
										132 cell
											133 text Disturbance tolerance
										134 cell
											135 container
												136 text 𝜂
												137 container
													138 text − 1
												139 text ≤ 32 𝑅
									140 row
										141 cell
											142 text Individual rational bit lengths
										143 cell
											144 container
												145 text 𝐶 ( 𝐿 + log ⁡ 𝑅 + 1 )
									146 row
										147 cell
											148 text Total computation, memory, and output
										149 cell
											150 text A fixed polynomial in 
											151 container
												152 text 𝐿 + 𝑅
								153 container
									154 button Copy table
									155 pop up button (collapsed) Description: Expand table, Secondary Actions: Expand
								156 text A common exponent 
								157 container
									158 text 𝑝 = 128
								159 text  is more than sufficient. I specify below how the fixed constant 
								160 text 𝐴
								161 text , including the entire granted fixed-family precomputation, is computed. The proof uses your premises 1–2 as accepted constructive mathematics. The suggested Koike–Nersesyan–Rissel–Tucsnak paper concerns passive-scalar relaxation through controlled two-dimensional Euler flows; the total-velocity estimate needed here is proved below directly for the three-dimensional Navier–Stokes equation. 
								162 link (collapsed) Value: arxiv.org/html/2506.22233v1?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: Relaxation enhancement by controlling incompressible fluid flows, https://arxiv.org/html/2506.22233v1?utm_source=chatgpt.com
								163 heading 1. Fixed data and notation, Value: 2
									164 text 1. Fixed data and notation
								165 text Work on 
								166 container
									167 text 𝑇
									168 text 3
									169 text =
									170 text 𝑅
									171 text 3
									172 text /
									173 text 𝑍
									174 text 3
								175 text , with
								176 container
									177 text ∥ 𝑢
									178 text ∥
									179 container
										180 text 𝐻 𝑚
									181 text = ∥ ( 𝐼 − Δ
									182 text )
									183 container
										184 text 𝑚 / 2
									185 text 𝑢
									186 text ∥
									187 text 2
									188 text .
								189 text All vector fields below are mean-zero and divergence-free. Write
								190 container
									191 text 𝐵 ( 𝑢 , 𝑣 ) = 𝑃 [ ( 𝑢 ⋅ ∇ ) 𝑣 ] ,
									192 text 𝐿
									193 text 𝐹
									194 text 𝑣 = 𝐵 ( 𝐹 , 𝑣 ) + 𝐵 ( 𝑣 , 𝐹 ) ,
								195 text where 
								196 text 𝑃
								197 text  is the Leray projection. Execute the effective fixed-family construction granted in premise 1. Flatten its fixed word into a finite list of shear factors, with signs chosen so that
								198 container
									199 container
										200 text 𝑊 ( 𝑠 ) =
										201 text 𝑒
										202 container
											203 text −
											204 text 𝛼
											205 text 𝑚
											206 text 𝑠
											207 text 𝐿
											208 container
												209 text 𝐹 𝑚
										210 text ⋯
										211 text 𝑒
										212 container
											213 text −
											214 text 𝛼
											215 text 1
											216 text 𝑠
											217 text 𝐿
											218 container
												219 text 𝐹 1
										220 text ,
									221 text (1)
								222 text where
								223 container
									224 text 𝐹
									225 text ℓ
									226 text =
									227 text 𝐺
									228 container
										229 text ȷ ℓ
									230 text ,
									231 text 𝛼
									232 text ℓ
									233 text ∈ 𝑄 .
								234 text The rational design weights are incorporated into the fixed word using its rational pulse descriptions and fixed multiplicities. The fixed precomputation returns:
								235 content list
									236 container
										237 AXListMarker • 
										238 text The complete rational Fourier descriptions of the 
										239 container
											240 text 𝐺 𝑗
										241 text .
									242 container
										243 AXListMarker • 
										244 text The finite signed-letter list 
										245 container
											246 text (
											247 text ȷ
											248 text ℓ
											249 text ,
											250 text 𝛼
											251 text ℓ
											252 text )
											253 container
												254 text ℓ = 1
											255 text 𝑚
										256 text .
									257 container
										258 AXListMarker • 
										259 text A positive rational lower bound 
										260 text 𝑐
										261 text  in
										262 container
											263 text Sym ⁡ 𝐷 ( 𝑘 ) ≤ −
											264 text 𝑐
											265 container
												266 text 1 + ∣ 𝑘
												267 text ∣
												268 text 2
											269 text 𝐼 .
									270 container
										271 AXListMarker • 
										272 text Rational upper bounds 
										273 container
											274 text 𝐶
											275 text 0
											276 text ,
											277 text 𝑐
											278 text 1
											279 text ,
											280 text 𝑏
											281 text 0
											282 text ,
											283 text 𝑏
											284 text 1
											285 text ,
											286 text 𝑏
											287 text 2
										288 text  and a common admissible small-
										289 text 𝑠
										290 text  range, such that
										291 container
											292 container
												293 text ∥ 𝑊 ( 𝑠 ) −
												294 text 𝑒
												295 container
													296 text 𝑠
													297 text 4
													298 text 𝐷
												299 text ∥
												300 container
													301 text 2 → 2
												302 text ≤
												303 text 𝐶
												304 text 0
												305 text 𝑠
												306 text 5
												307 text ,
											308 text (2)
										309 container
											310 container
												311 text ∥ 𝑊 ( 𝑠 ) −
												312 text 𝑒
												313 container
													314 text 𝑠
													315 text 4
													316 text 𝐷
												317 text ∥
												318 container
													319 text 𝐻
													320 text 1
													321 text →
													322 text 𝐻
													323 text 1
												324 text ≤
												325 text 𝑐
												326 text 1
												327 text 𝑠
												328 text 5
												329 text ,
											330 text (3)
										331 text and every partial block and its inverse have 
										332 container
											333 text 𝐻 𝑗
										334 text  norms at most 
										335 container
											336 text 𝑒
											337 container
												338 text 𝑏 𝑗
											339 text 𝑠
										340 text , for 
										341 container
											342 text 𝑗 = 0 , 1 , 2
										343 text .
								344 text Only these three Sobolev orders are needed. Because 
								345 text 𝐷
								346 text  commutes with the scalar Sobolev weights and has negative symmetric part,
								347 container
									348 text ∥
									349 text 𝑒
									350 container
										351 text 𝑡 𝐷
									352 text ∥
									353 container
										354 text 𝐻
										355 text 𝑗
										356 text →
										357 text 𝐻
										358 text 𝑗
									359 text ≤ 1.
								360 text In particular,
								361 container
									362 container
										363 text ∥ 𝑊 ( 𝑠 )
										364 text ∥
										365 container
											366 text 𝐻
											367 text 1
											368 text →
											369 text 𝐻
											370 text 1
										371 text ≤ 1 +
										372 text 𝑐
										373 text 1
										374 text 𝑠
										375 text 5
										376 text .
									377 text (4)
								378 text For a path consisting of 
								379 text 𝑛
								380 text  blocks, the supplied forward-propagator estimate gives
								381 container
									382 container
										383 text ∥ 𝑆 ( 𝑡 , 𝑟 )
										384 text ∥
										385 container
											386 text 2 → 2
										387 text ≤ exp ⁡  ⁣
										388 text (
										389 text 2
										390 container
											391 text 𝑏 0
										392 text 𝑠
										393 text +
										394 container
											395 text 𝐶 0
										396 text 𝑛
										397 container
											398 text 𝑠 5
										399 text )
										400 text , 𝑟 ≤ 𝑡 .
									401 text (5)
								402 text All constants used subsequently will be calculated from this finite data.
								403 heading 2. The new estimate: viscosity survives a change of coordinates within one block, Value: 2
									404 text 2. The new estimate: viscosity survives a change of coordinates within one block
								405 text Let 
								406 container
									407 text 𝑤 ( 𝑡 )
								408 text  be the prescribed shear carrier. During a single pulse,
								409 container
									410 text 𝑤 ( 𝑡 ) = 𝑎 ( 𝑡 )
									411 text 𝐹
									412 text ℓ
									413 text ,
								414 text and over a complete macro-block,
								415 container
									416 text ∫
									417 text block
									418 text ∣ 𝑎 ( 𝑡 ) ∣ 𝑑 𝑡
								419 text summed over its letters equals
								420 container
									421 container
										422 text 𝑠
										423 text ∑
										424 container
											425 text ℓ = 1
										426 text 𝑚
										427 text ∣
										428 text 𝛼
										429 text ℓ
										430 text ∣ .
									431 text (6)
								432 text This quantity is independent of how quickly the block is executed. Let 
								433 container
									434 text 𝐼
									435 text 𝑗
									436 text = [
									437 text 𝑡
									438 text 𝑗
									439 text ,
									440 text 𝑡
									441 container
										442 text 𝑗 + 1
									443 text ]
								444 text  be one macro-block and define its inviscid propagator
								445 container
									446 text 𝑃
									447 text 𝑗
									448 text ( 𝑡 ) = 𝑆 ( 𝑡 ,
									449 text 𝑡
									450 text 𝑗
									451 text ) ,
									452 text ∂
									453 text 𝑡
									454 text 𝑃
									455 text 𝑗
									456 text = −
									457 text 𝐿
									458 container
										459 text 𝑤 ( 𝑡 )
									460 text 𝑃
									461 text 𝑗
									462 text ,
									463 text 𝑃
									464 text 𝑗
									465 text (
									466 text 𝑡
									467 text 𝑗
									468 text ) = 𝐼 .
								469 text Choose a fixed small-
								470 text 𝑠
								471 text  threshold so that
								472 container
									473 container
										474 text ∥
										475 text 𝑃
										476 text 𝑗
										477 text ( 𝑡
										478 text )
										479 container
											480 text ± 1
										481 text ∥
										482 container
											483 text 𝐻
											484 text 𝑎
											485 text →
											486 text 𝐻
											487 text 𝑎
										488 text ≤ 2 , 𝑎 = 0 , 1 , 2.
									489 text (7)
								490 heading 2.1 The commutator has only two derivatives of the unknown, Value: 3
									491 text 2.1 The commutator has only two derivatives of the unknown
								492 text Since 
								493 text 𝑃
								494 text  commutes with 
								495 text Δ
								496 text ,
								497 container
									498 container
										499 container
											500 text [ Δ ,
											501 text 𝐿
											502 text 𝐹
											503 text ] 𝑢 = 𝑃 [
										504 container
											505 text ( ( Δ 𝐹 ) ⋅ ∇ ) 𝑢 + 2
											506 text ∑
											507 container
												508 text 𝑎 = 1
											509 text 3
											510 text ( (
											511 text ∂
											512 text 𝑎
											513 text 𝐹 ) ⋅ ∇ )
											514 text ∂
											515 text 𝑎
											516 text 𝑢
										517 container
											518 text + 2
											519 text ∑
											520 container
												521 text 𝑎 = 1
											522 text 3
											523 text ( (
											524 text ∂
											525 text 𝑎
											526 text 𝑢 ) ⋅ ∇ )
											527 text ∂
											528 text 𝑎
											529 text 𝐹 + ( 𝑢 ⋅ ∇ ) Δ 𝐹 ] .
									530 text (8)
								531 text Therefore
								532 container
									533 container
										534 text ∥ [ Δ ,
										535 text 𝐿
										536 text 𝐹
										537 text ] 𝑢
										538 text ∥
										539 text 2
										540 text ≤
										541 text 𝐶
										542 text 𝐹
										543 text ∥ 𝑢
										544 text ∥
										545 container
											546 text 𝐻 2
										547 text .
									548 text (9)
								549 text Each 
								550 container
									551 text 𝐶 𝐹
								552 text  has an explicit rational upper bound obtained directly from the finite Fourier coefficients of 
								553 text 𝐹
								554 text , using derivatives through order three. For example, replace every factor 
								555 container
									556 text 2 𝜋
								557 text  in a Fourier derivative bound by 
								558 text 8
								559 text , and bound the resulting trigonometric polynomial by the sum of the absolute values of its coefficients. No norm oracle is involved.
								560 heading 2.2 Conjugation changes the Laplacian by , Value: 3
									561 text 2.2 Conjugation changes the Laplacian by 
									562 container
										563 text 𝑂 ( 𝑠 )
								564 text On smooth fields,
								565 container
									566 container
										567 text 𝑑
										568 container
											569 text 𝑑 𝑡
										570 text (
										571 text 𝑃
										572 text 𝑗
										573 container
											574 text − 1
										575 text Δ
										576 text 𝑃
										577 text 𝑗
										578 text ) =
										579 text 𝑃
										580 text 𝑗
										581 container
											582 text − 1
										583 text [
										584 text 𝐿
										585 container
											586 text 𝑤 ( 𝑡 )
										587 text , Δ ]
										588 text 𝑃
										589 text 𝑗
										590 text .
									591 text (10)
								592 text Using (6), (7), and (9), integration gives
								593 container
									594 container
										595 text ∥
										596 text 𝑃
										597 text 𝑗
										598 container
											599 text − 1
										600 text Δ
										601 text 𝑃
										602 text 𝑗
										603 text − Δ
										604 text ∥
										605 container
											606 text 𝐻
											607 text 2
											608 text →
											609 text 𝐿
											610 text 2
										611 text ≤
										612 text 𝐶
										613 text Δ
										614 text 𝑠 .
									615 text (11)
								616 text For example, one may use
								617 container
									618 text 𝐶
									619 text Δ
									620 text = 4
									621 text ∑
									622 container
										623 text ℓ = 1
									624 text 𝑚
									625 text ∣
									626 text 𝛼
									627 text ℓ
									628 text ∣
									629 text 𝐶
									630 container
										631 text 𝐹 ℓ
									632 text .
								633 text The identity and estimate extend from smooth fields by density. Shrink the fixed threshold so that
								634 container
									635 container
										636 text 𝐶
										637 text Δ
										638 text 𝑠 ≤
										639 text 1
										640 text 8
										641 text .
									642 text (12)
								643 text For mean-zero fields on the unit torus,
								644 container
									645 container
										646 text − ⟨ Δ 𝑧 , ( 𝐼 − Δ ) 𝑧 ⟩ = ∥ ∇ 𝑧
										647 text ∥
										648 text 2
										649 text 2
										650 text + ∥ Δ 𝑧
										651 text ∥
										652 text 2
										653 text 2
										654 text ≥
										655 text 1
										656 text 2
										657 text ∥ 𝑧
										658 text ∥
										659 container
											660 text 𝐻 2
										661 text 2
										662 text ,
									663 text (13)
								664 text because every nonzero Laplace eigenvalue is at least 
								665 container
									666 text 4
									667 text 𝜋
									668 text 2
									669 text > 1
								670 text . Equations (11)–(13) give the required coercivity. Crucially, they depend on the impulse in 
								671 text one block
								672 text , rather than the strain accumulated over the entire repeated path.
								673 heading 3. A uniform nonlinear estimate throughout the active interval, Value: 2
									674 text 3. A uniform nonlinear estimate throughout the active interval
								675 text Suppose the carrier occupies 
								676 container
									677 text [ 0 , 𝛿 ]
								678 text , starts and ends at zero, and contains 
								679 text 𝑛
								680 text  complete macro-blocks. Its ideal force is
								681 container
									682 text 𝑓
									683 text ∗
									684 text =
									685 text 𝑤
									686 text 𝑡
									687 text + 𝐵 ( 𝑤 , 𝑤 ) − 𝜈 Δ 𝑤 .
								688 text Only one shear is active at a time, so
								689 container
									690 container
										691 text 𝐵 ( 𝑤 , 𝑤 ) = 0 ,
										692 text 𝑓
										693 text ∗
										694 text =
										695 text 𝑤
										696 text 𝑡
										697 text − 𝜈 Δ 𝑤 .
									698 text (14)
								699 text Allow a rational approximation 
								700 text 𝑓
								701 text  with
								702 container
									703 text ∥ 𝑓 −
									704 text 𝑓
									705 text ∗
									706 text ∥
									707 container
										708 text 𝐿
										709 text ∞
										710 text 𝐿
										711 text 2
									712 text ≤ 𝜉 .
								713 text For each actual disturbance 
								714 text ℎ
								715 text , define
								716 container
									717 text 𝑣 = 𝑈 − 𝑤 , 𝑔 = ℎ + ( 𝑓 −
									718 text 𝑓
									719 text ∗
									720 text ) ,
									721 text 𝑎
									722 text ∗
									723 text = 𝜂 + 𝜉 .
								724 text Then
								725 container
									726 container
										727 text 𝑣
										728 text 𝑡
										729 text +
										730 text 𝐿
										731 text 𝑤
										732 text 𝑣 = 𝜈 Δ 𝑣 − 𝐵 ( 𝑣 , 𝑣 ) + 𝑔 .
									733 text (15)
								734 text Assume for the moment that 
								735 container
									736 text 𝑎
									737 text ∗
									738 text ≤ 1
								739 text .
								740 heading 3.1 Reset the coordinates after each block, Value: 3
									741 text 3.1 Reset the coordinates after each block
								742 text Within block 
								743 text 𝑗
								744 text , set
								745 container
									746 text 𝑧 =
									747 text 𝑃
									748 text 𝑗
									749 container
										750 text − 1
									751 text 𝑣 .
								752 text The transformed equation is
								753 container
									754 container
										755 text 𝑧
										756 text 𝑡
										757 text = 𝜈
										758 text 𝑃
										759 text 𝑗
										760 container
											761 text − 1
										762 text Δ
										763 text 𝑃
										764 text 𝑗
										765 text 𝑧 −
										766 text 𝑃
										767 text 𝑗
										768 container
											769 text − 1
										770 text 𝐵 (
										771 text 𝑃
										772 text 𝑗
										773 text 𝑧 ,
										774 text 𝑃
										775 text 𝑗
										776 text 𝑧 ) +
										777 text 𝑃
										778 text 𝑗
										779 container
											780 text − 1
										781 text 𝑔 .
									782 text (16)
								783 text At the next block boundary the new propagator starts at the identity. Accordingly,
								784 container
									785 container
										786 text 𝑧 (
										787 text 𝑡
										788 container
											789 text 𝑗 + 1
										790 text + ) = 𝑊 ( 𝑠 ) 𝑧 (
										791 text 𝑡
										792 container
											793 text 𝑗 + 1
										794 text − ) .
									795 text (17)
								796 text This reset is an operation in the proof. The physical velocity remains continuous, and the prescribed force is unaffected.
								797 heading 3.2 An explicit nonlinear constant, Value: 3
									798 text 3.2 An explicit nonlinear constant
								799 text An elementary Fourier estimate on the unit torus gives
								800 container
									801 container
										802 text ∥ 𝑢
										803 text ∥
										804 text ∞
										805 text ≤ 16 ∥ 𝑢
										806 text ∥
										807 container
											808 text 𝐻 1
										809 container
											810 text 1 / 2
										811 text ∥ 𝑢
										812 text ∥
										813 container
											814 text 𝐻 2
										815 container
											816 text 1 / 2
										817 text .
									818 text (18)
								819 text Here is one way to make the constant effective. The shell
								820 container
									821 text { 𝑘 ∈
									822 text 𝑍
									823 text 3
									824 text : ∣ 𝑘
									825 text ∣
									826 text ∞
									827 text = 𝑗 }
								828 text contains 
								829 container
									830 text 24
									831 text 𝑗
									832 text 2
									833 text + 2 ≤ 26
									834 text 𝑗
									835 text 2
								836 text  points. Splitting the Fourier sum at
								837 container
									838 text 𝑁 =
									839 text ⌈
									840 container
										841 text ∥
										842 text 𝑢
										843 container
											844 text ∥
											845 text 𝐻
											846 text 2
										847 text ∥
										848 text 𝑢
										849 container
											850 text ∥
											851 text 𝐻
											852 text 1
									853 text ⌉
								854 text bounds the low-frequency reciprocal 
								855 container
									856 text 𝐻 1
								857 text -weight sum by 
								858 container
									859 text 26 𝑁
								860 text , and the high-frequency reciprocal 
								861 container
									862 text 𝐻 2
								863 text -weight sum by 
								864 container
									865 text 26 / 𝑁
								866 text . Cauchy–Schwarz then gives (18). The zero field is immediate. Consequently,
								867 container
									868 container
										869 text ∥ 𝐵 ( 𝑢 , 𝑢 )
										870 text ∥
										871 text 2
										872 text ≤ 16 ∥ 𝑢
										873 text ∥
										874 container
											875 text 𝐻 1
										876 container
											877 text 3 / 2
										878 text ∥ 𝑢
										879 text ∥
										880 container
											881 text 𝐻 2
										882 container
											883 text 1 / 2
										884 text .
									885 text (19)
								886 text Put
								887 container
									888 text 𝐸 = ∥ 𝑧
									889 text ∥
									890 container
										891 text 𝐻 1
									892 text 2
									893 text , 𝑍 = ∥ 𝑧
									894 text ∥
									895 container
										896 text 𝐻 2
									897 text .
								898 text By (7) and (19),
								899 container
									900 container
										901 text ∥
										902 text 𝑃
										903 text 𝑗
										904 container
											905 text − 1
										906 text 𝐵 (
										907 text 𝑃
										908 text 𝑗
										909 text 𝑧 ,
										910 text 𝑃
										911 text 𝑗
										912 text 𝑧 )
										913 text ∥
										914 text 2
										915 text ≤ 128
										916 text 𝐸
										917 container
											918 text 3 / 4
										919 text 𝑍
										920 container
											921 text 1 / 2
										922 text .
									923 text (20)
								924 heading 3.3 The energy inequality, Value: 3
									925 text 3.3 The energy inequality
								926 text Pair (16) with 
								927 container
									928 text ( 𝐼 − Δ ) 𝑧
								929 text . Equations (11)–(13) imply
								930 container
									931 text 1
									932 text 2
									933 text 𝐸
									934 text ′
									935 text ≤ −
									936 text 𝜈
									937 text 2
									938 text 𝑍
									939 text 2
									940 text +
									941 text 𝜈
									942 text 8
									943 text 𝑍
									944 text 2
									945 text + 128
									946 text 𝐸
									947 container
										948 text 3 / 4
									949 text 𝑍
									950 container
										951 text 3 / 2
									952 text + 2
									953 text 𝑎
									954 text ∗
									955 text 𝑍 .
								956 text Use
								957 container
									958 text 128
									959 text 𝐸
									960 container
										961 text 3 / 4
									962 text 𝑍
									963 container
										964 text 3 / 2
									965 text ≤
									966 text 𝜈
									967 text 8
									968 text 𝑍
									969 text 2
									970 text + 54 ⋅
									971 text 128
									972 text 4
									973 text 𝜈
									974 container
										975 text − 3
									976 text 𝐸
									977 text 3
									978 text ,
								979 text and
								980 container
									981 text 2
									982 text 𝑎
									983 text ∗
									984 text 𝑍 ≤
									985 text 𝜈
									986 text 8
									987 text 𝑍
									988 text 2
									989 text + 8
									990 text 𝜈
									991 container
										992 text − 1
									993 text 𝑎
									994 text ∗
									995 text 2
									996 text .
								997 text Thus, with the explicit integer
								998 container
									999 text 𝐶
									1000 text 𝐸
									1001 text = 108 ⋅
									1002 text 128
									1003 text 4
									1004 text ,
								1005 text we have
								1006 container
									1007 container
										1008 text 𝐸
										1009 text ′
										1010 text +
										1011 text 𝜈
										1012 text 4
										1013 text 𝑍
										1014 text 2
										1015 text ≤
										1016 text 𝐶
										1017 text 𝐸
										1018 text 𝜈
										1019 container
											1020 text − 3
										1021 text 𝐸
										1022 text 3
										1023 text +
										1024 text 𝐶
										1025 text 𝐸
										1026 text 𝜈
										1027 container
											1028 text − 1
										1029 text 𝑎
										1030 text ∗
										1031 text 2
										1032 text .
									1033 text (21)
								1034 text There is no carrier amplitude, pulse frequency, 
								1035 container
									1036 text 𝑛 𝑠
								1037 text , or accumulated-strain exponential in this inequality.
								1038 heading 3.4 Accounting for every reset, Value: 3
									1039 text 3.4 Accounting for every reset
								1040 text By (4) and (17),
								1041 container
									1042 text 𝐸 (
									1043 text 𝑡
									1044 container
										1045 text 𝑗 + 1
									1046 text + ) ≤ 𝑞 𝐸 (
									1047 text 𝑡
									1048 container
										1049 text 𝑗 + 1
									1050 text − ) , 𝑞 = ( 1 +
									1051 text 𝑐
									1052 text 1
									1053 text 𝑠
									1054 text 5
									1055 text )
									1056 text 2
									1057 text .
								1058 text Require
								1059 container
									1060 container
										1061 text 𝑞
										1062 text 𝑛
										1063 text ≤ 2.
									1064 text (22)
								1065 text On block 
								1066 text 𝑗
								1067 text , define
								1068 container
									1069 text 𝐸 =
									1070 text 𝑞
									1071 container
										1072 text − 𝑗
									1073 text 𝐸 .
								1074 text It has no upward jump at a reset, and (21) gives
								1075 container
									1076 container
										1077 text 𝐸
										1078 text ′
										1079 text +
										1080 text 𝜈
										1081 text 4
										1082 text 𝑞
										1083 container
											1084 text − 𝑗
										1085 text 𝑍
										1086 text 2
										1087 text ≤ 4
										1088 text 𝐶
										1089 text 𝐸
										1090 text 𝜈
										1091 container
											1092 text − 3
										1093 text 𝐸
										1094 text 3
										1095 text +
										1096 text 𝐶
										1097 text 𝐸
										1098 text 𝜈
										1099 container
											1100 text − 1
										1101 text 𝑎
										1102 text ∗
										1103 text 2
										1104 text .
									1105 text (23)
								1106 text Since 
								1107 container
									1108 text 𝐸 ( 0 ) ≤
									1109 text 𝑀
									1110 text 2
								1111 text , the bootstrap
								1112 container
									1113 text 𝐸 ≤ 2
									1114 text 𝑀
									1115 text 2
								1116 text closes provided
								1117 container
									1118 container
										1119 text 𝛿 ≤
										1120 container
											1121 text 𝜈 3
										1122 container
											1123 text 128
											1124 text 𝐶
											1125 text 𝐸
											1126 text 𝑀
											1127 text 4
										1128 text .
									1129 text (24)
								1130 text Indeed, while the bootstrap holds, the right-hand side of (23) is at most
								1131 container
									1132 text 33
									1133 text 𝐶
									1134 text 𝐸
									1135 text 𝜈
									1136 container
										1137 text − 3
									1138 text 𝑀
									1139 text 6
									1140 text ,
								1141 text using 
								1142 container
									1143 text 𝑎
									1144 text ∗
									1145 text ≤ 1
								1146 text , 
								1147 container
									1148 text 𝑀 ≥ 1
								1149 text , and 
								1150 container
									1151 text 𝜈 ≤ 1
								1152 text . Over (24), this increases the weighted energy by less than 
								1153 container
									1154 text 𝑀 2
								1155 text . Integrating (23), and using 
								1156 container
									1157 text 𝑞
									1158 container
										1159 text − 𝑗
									1160 text ≥ 1 / 2
								1161 text , gives
								1162 container
									1163 text 𝜈
									1164 text ∫
									1165 text 0
									1166 text 𝛿
									1167 text 𝑍
									1168 text 2
									1169 text 𝑑 𝑡 ≤ 16
									1170 text 𝑀
									1171 text 2
									1172 text .
								1173 text Returning to 
								1174 container
									1175 text 𝑣 =
									1176 text 𝑃
									1177 text 𝑗
									1178 text 𝑧
								1179 text ,
								1180 container
									1181 container
										1182 container
											1183 text sup ⁡
										1184 container
											1185 text 0 ≤ 𝑡 ≤ 𝛿
										1186 text ∥ 𝑣 ( 𝑡 )
										1187 text ∥
										1188 container
											1189 text 𝐻 1
										1190 text ≤ 4 𝑀 , 𝜈
										1191 text ∫
										1192 text 0
										1193 text 𝛿
										1194 text ∥ 𝑣 ( 𝑡 )
										1195 text ∥
										1196 container
											1197 text 𝐻 2
										1198 text 2
										1199 text 𝑑 𝑡 ≤ 64
										1200 text 𝑀
										1201 text 2
										1202 text .
									1203 text (25)
								1204 heading 3.5 Why this covers every Leray–Hopf realization, Value: 3
									1205 text 3.5 Why this covers every Leray–Hopf realization
								1206 text For each fixed compiler output, 
								1207 text 𝑤
								1208 text  is continuous, piecewise polynomial in time, and smooth in space. The actual force belongs to 
								1209 container
									1210 text 𝐿
									1211 text 𝑡
									1212 text ∞
									1213 text 𝐿
									1214 text 𝑥
									1215 text 2
								1216 text . Local 
								1217 container
									1218 text 𝐻 1
								1219 text  strong existence therefore applies; the estimate (25) prevents loss of 
								1220 container
									1221 text 𝐻 1
								1222 text  regularity before 
								1223 text 𝛿
								1224 text , so the solution continues throughout the active interval. These are the usual local strong-solution and continuation mechanisms for three-dimensional Navier–Stokes. 
								1225 link (collapsed) Value: virtualmath1.stanford.edu/~ryzhik/notes-256B-24.pdf?utm_source=chatgpt.com, Secondary Actions: Expand, Description: virtualmath1.stanford.edu: https://virtualmath1.stanford.edu/~ryzhik/notes-256B-24.pdf, https://virtualmath1.stanford.edu/~ryzhik/notes-256B-24.pdf?utm_source=chatgpt.com, 1 additional source
								1226 text For each actual 
								1227 text ℎ
								1228 text , this produces
								1229 container
									1230 text 𝑈
									1231 text ∗
									1232 text = 𝑤 + 𝑣 ∈
									1233 text 𝐿
									1234 text ∞
									1235 text ( 0 , 𝛿 ;
									1236 text 𝐻
									1237 text 1
									1238 text ) ∩
									1239 text 𝐿
									1240 text 2
									1241 text ( 0 , 𝛿 ;
									1242 text 𝐻
									1243 text 2
									1244 text ) .
								1245 text Weak–strong uniqueness identifies every corresponding Leray–Hopf solution with 
								1246 container
									1247 text 𝑈 ∗
								1248 text  on that interval. The uniqueness argument may contain a very large finite Grönwall factor. Its initial discrepancy is exactly zero. 
								1249 text No disturbance tolerance or physical resource is chosen using that factor.
								1250 text  Quantitative robustness comes from (21)–(25), applied separately to each actual disturbance.
								1251 heading 4. The resulting endpoint comparison is polynomial, Value: 2
									1252 text 4. The resulting endpoint comparison is polynomial
								1253 text Arrange also that (5) gives
								1254 container
									1255 container
										1256 container
											1257 text sup ⁡
										1258 container
											1259 text 0 ≤ 𝑟 ≤ 𝑡 ≤ 𝛿
										1260 text ∥ 𝑆 ( 𝑡 , 𝑟 )
										1261 text ∥
										1262 container
											1263 text 2 → 2
										1264 text ≤ 2.
									1265 text (26)
								1266 text Equation (15) has the 
								1267 container
									1268 text 𝐿 2
								1269 text  variation-of-constants formula
								1270 container
									1271 container
										1272 text 𝑣 ( 𝛿 ) − 𝑊 ( 𝑠
										1273 text )
										1274 text 𝑛
										1275 text 𝑈
										1276 text 0
										1277 text =
										1278 text ∫
										1279 text 0
										1280 text 𝛿
										1281 text 𝑆 ( 𝛿 , 𝑡 ) [ 𝜈 Δ 𝑣 − 𝐵 ( 𝑣 , 𝑣 ) + 𝑔 ] 𝑑 𝑡 .
									1282 text (27)
								1283 text The residual is in 
								1284 container
									1285 text 𝐿
									1286 text 𝑡
									1287 text 1
									1288 text 𝐿
									1289 text 𝑥
									1290 text 2
								1291 text  by (25), so this is a legitimate strong-solution formula. First,
								1292 container
									1293 text 𝜈
									1294 text ∫
									1295 text 0
									1296 text 𝛿
									1297 text ∥ Δ 𝑣
									1298 text ∥
									1299 text 2
									1300 text 𝑑 𝑡 ≤ 8 𝑀
									1301 container
										1302 text 𝜈 𝛿
									1303 text .
								1304 text Second, by (19), (25), and Hölder,
								1305 container
									1306 container
										1307 text ∫
										1308 text 0
										1309 text 𝛿
										1310 text ∥ 𝐵 ( 𝑣 , 𝑣 )
										1311 text ∥
										1312 text 2
										1313 text 𝑑 𝑡
									1314 container
										1315 text ≤ 16 ( 4 𝑀
										1316 text )
										1317 container
											1318 text 3 / 2
										1319 text 𝛿
										1320 container
											1321 text 3 / 4
										1322 container
											1323 text (
											1324 text ∫
											1325 text 0
											1326 text 𝛿
											1327 text ∥ 𝑣
											1328 text ∥
											1329 container
												1330 text 𝐻 2
											1331 text 2
											1332 text 𝑑 𝑡 )
										1333 container
											1334 text 1 / 4
									1335 container
										1336 text ≤ 384
										1337 text 𝑀
										1338 text 2
										1339 text 𝛿
										1340 container
											1341 text 3 / 4
										1342 text 𝜈
										1343 container
											1344 text − 1 / 4
										1345 text .
								1346 text Multiplying by the forward-propagator bound 
								1347 text 2
								1348 text  yields
								1349 container
									1350 container
										1351 text ∥ 𝑈 ( 𝛿 ) − 𝑊 ( 𝑠
										1352 text )
										1353 text 𝑛
										1354 text 𝑈
										1355 text 0
										1356 text ∥
										1357 text 2
										1358 text ≤ 16 𝑀
										1359 container
											1360 text 𝜈 𝛿
										1361 text + 768
										1362 text 𝑀
										1363 text 2
										1364 text 𝛿
										1365 container
											1366 text 3 / 4
										1367 text 𝜈
										1368 container
											1369 text − 1 / 4
										1370 text + 2
										1371 text 𝑎
										1372 text ∗
										1373 text 𝛿 .
									1374 text (28)
								1375 text Here 
								1376 container
									1377 text 𝑤 ( 𝛿 ) = 0
								1378 text , so the left side concerns 
								1379 text total velocity
								1380 text  at the end of the active interval. This is the quantitative replacement for the supplied estimate containing 
								1381 container
									1382 text 𝑒 𝐾
								1383 text .
								1384 heading 5. Explicit fixed constants and variable parameter choices, Value: 2
									1385 text 5. Explicit fixed constants and variable parameter choices
								1386 heading 5.1 Finish the fixed precomputation, Value: 3
									1387 text 5.1 Finish the fixed precomputation
								1388 text Choose a positive rational 
								1389 text 𝜎
								1390 text  lying in the common admissible range of the supplied estimates and satisfying
								1391 container
									1392 container
										1393 text 𝜎 ≤
										1394 text 1
										1395 container
											1396 text 16 ( 1 +
											1397 text 𝑏
											1398 text 0
											1399 text +
											1400 text 𝑏
											1401 text 1
											1402 text +
											1403 text 𝑏
											1404 text 2
											1405 text +
											1406 text 𝐶
											1407 text Δ
											1408 text )
										1409 text .
									1410 text (29)
								1411 text This ensures all the partial-propagator and commutator requirements above. Choose the integer
								1412 container
									1413 text 𝐶
									1414 text 𝐷
									1415 text = 1 + ⌈
									1416 text 𝑐
									1417 container
										1418 text − 1
									1419 text ⌉ .
								1420 text The Fourier multiplier estimate gives
								1421 container
									1422 container
										1423 text ∥
										1424 text 𝑒
										1425 container
											1426 text 𝑇 𝐷
										1427 text 𝐽
										1428 text ∥
										1429 container
											1430 text 2 → 2
										1431 text ≤
										1432 text 𝐶
										1433 text 𝐷
										1434 text 𝑇
										1435 container
											1436 text − 1 / 2
										1437 text .
									1438 text (30)
								1439 text Indeed, putting 
								1440 container
									1441 text 𝑦 = 1 + ∣ 𝑘
									1442 text ∣
									1443 text 2
								1444 text ,
								1445 container
									1446 container
										1447 text 𝑒
										1448 text −
										1449 text 𝑐
										1450 text 𝑇
										1451 text /
										1452 text 𝑦
									1453 container
										1454 text 1 + 4
										1455 text 𝜋
										1456 text 2
										1457 text ∣ 𝑘
										1458 text ∣
										1459 text 2
									1460 text ≤
									1461 text 𝑦
									1462 container
										1463 text − 1 / 2
									1464 text 𝑒
									1465 container
										1466 text − 𝑐 𝑇 / 𝑦
									1467 text ,
								1468 text whose supremum over 
								1469 container
									1470 text 𝑦 > 0
								1471 text  is 
								1472 container
									1473 text ( 2 𝑒 𝑐 𝑇
									1474 text )
									1475 container
										1476 text − 1 / 2
								1477 text . Now compute a fixed integer 
								1478 container
									1479 text 𝐵 ∗
								1480 text  satisfying
								1481 container
									1482 container
										1483 text 𝐵
										1484 text ∗
										1485 text ≥ max ⁡
										1486 text {
										1487 text 2
										1488 text ,
										1489 container
											1490 text 𝜎
											1491 text −
											1492 text 1
										1493 text ,
										1494 text 16
										1495 container
											1496 text 𝐶 0
										1497 text ,
										1498 text 4
										1499 container
											1500 text 𝑐 1
										1501 text ,
										1502 text 128
										1503 container
											1504 text 𝐶 𝐸
										1505 text ,
										1506 text 64
										1507 container
											1508 text 𝐶 𝐷 2
										1509 text ,
										1510 text (
										1511 text 12
										1512 text ⋅
										1513 text 1024
										1514 container
											1515 text ) 2
										1516 text }
										1517 text .
									1518 text (31)
								1519 text A ceiling of the displayed maximum suffices. Everything in (29)–(31) is fixed, rationally computable, and independent of the variable inputs.
								1520 heading 5.2 Online parameters, Value: 3
									1521 text 5.2 Online parameters
								1522 text For an input 
								1523 container
									1524 text ( 𝑀 , 𝜈 , 𝜏 , 𝜖 )
								1525 text , compute the integer
								1526 container
									1527 container
										1528 text 𝜌 = 2 + ⌈ 𝑀 ⌉ + ⌈
										1529 text 𝜈
										1530 container
											1531 text − 1
										1532 text ⌉ + ⌈
										1533 text 𝜏
										1534 container
											1535 text − 1
										1536 text ⌉ + ⌈
										1537 text 𝜖
										1538 container
											1539 text − 1
										1540 text ⌉ .
									1541 text (32)
								1542 text Then
								1543 container
									1544 container
										1545 text 𝑅 ≤ 𝜌 < 𝑅 + 4 ≤ 2 𝑅 ,
									1546 text (33)
								1547 text and
								1548 container
									1549 text 𝑀 ≤ 𝜌 ,
									1550 text 𝜈
									1551 container
										1552 text − 1
									1553 text ≤ 𝜌 ,
									1554 text 𝜏
									1555 container
										1556 text − 1
									1557 text ≤ 𝜌 ,
									1558 text 𝜖
									1559 container
										1560 text − 1
									1561 text ≤ 𝜌 .
								1562 text Set
								1563 container
									1564 container
										1565 text 𝑇
										1566 container
											1567 text =
											1568 text 𝐵
											1569 text ∗
											1570 text 𝜌
											1571 text 4
											1572 text ,
										1573 text 𝑠
										1574 container
											1575 text =
											1576 text 1
											1577 container
												1578 text 𝐵
												1579 text ∗
												1580 text 2
												1581 text 𝜌
												1582 text 6
											1583 text ,
										1584 text 𝑛
										1585 container
											1586 text =
											1587 text 𝐵
											1588 text ∗
											1589 text 9
											1590 text 𝜌
											1591 text 28
											1592 text ,
										1593 text 𝛿
										1594 container
											1595 text =
											1596 text 1
											1597 container
												1598 text 𝐵
												1599 text ∗
												1600 text 𝜌
												1601 text 8
											1602 text ,
										1603 text 𝜂
										1604 container
											1605 text =
											1606 text 1
											1607 container
												1608 text 16 𝜌
											1609 text .
									1610 text (34)
								1611 text All these quantities are rational, and 
								1612 text 𝑛
								1613 text  is an integer. In particular,
								1614 container
									1615 container
										1616 text 𝑛
										1617 text 𝑠
										1618 text 4
										1619 text = 𝑇 , 𝑛
										1620 text 𝑠
										1621 text 5
										1622 text =
										1623 text 1
										1624 container
											1625 text 𝐵
											1626 text ∗
											1627 text 𝜌
											1628 text 2
										1629 text .
									1630 text (35)
								1631 heading 5.3 Verification of the stability requirements, Value: 3
									1632 text 5.3 Verification of the stability requirements
								1633 text By (29), (31), and (34), 
								1634 container
									1635 text 𝑠 ≤ 𝜎
								1636 text . Moreover,
								1637 container
									1638 text 𝑞
									1639 text 𝑛
									1640 text ≤ exp ⁡ ( 2
									1641 text 𝑐
									1642 text 1
									1643 text 𝑛
									1644 text 𝑠
									1645 text 5
									1646 text ) ≤ exp ⁡ ( 2
									1647 text 𝑐
									1648 text 1
									1649 text /
									1650 text 𝐵
									1651 text ∗
									1652 text ) < 2 ,
								1653 text and
								1654 container
									1655 text exp ⁡ ( 2
									1656 text 𝑏
									1657 text 0
									1658 text 𝑠 +
									1659 text 𝐶
									1660 text 0
									1661 text 𝑛
									1662 text 𝑠
									1663 text 5
									1664 text ) < 2.
								1665 text Thus (22) and (26) hold. Also,
								1666 container
									1667 text 𝜈
									1668 text 3
									1669 text 𝑀
									1670 container
										1671 text − 4
									1672 text ≥
									1673 text 𝜌
									1674 container
										1675 text − 7
									1676 text .
								1677 text Since 
								1678 container
									1679 text 𝐵
									1680 text ∗
									1681 text ≥ 128
									1682 text 𝐶
									1683 text 𝐸
								1684 text ,
								1685 container
									1686 text 𝛿 =
									1687 text 1
									1688 container
										1689 text 𝐵
										1690 text ∗
										1691 text 𝜌
										1692 text 8
									1693 text ≤
									1694 container
										1695 text 𝜈 3
									1696 container
										1697 text 128
										1698 text 𝐶
										1699 text 𝐸
										1700 text 𝑀
										1701 text 4
									1702 text .
								1703 text Finally, 
								1704 container
									1705 text 𝛿 ≤ 𝜏 / 2
								1706 text .
								1707 heading 5.4 Verification of the linear target, Value: 3
									1708 text 5.4 Verification of the linear target
								1709 text By (30),
								1710 container
									1711 container
										1712 text ∥
										1713 text 𝑒
										1714 container
											1715 text 𝑇 𝐷
										1716 text 𝑈
										1717 text 0
										1718 text ∥
										1719 text 2
										1720 text ≤ 𝑀
										1721 text 𝐶
										1722 text 𝐷
										1723 text 𝑇
										1724 container
											1725 text − 1 / 2
										1726 text ≤
										1727 container
											1728 text 𝐶 𝐷
										1729 container
											1730 text 𝐵 ∗
										1731 text 𝜌
										1732 container
											1733 text − 1
										1734 text ≤
										1735 text 𝜖
										1736 text 8
										1737 text .
									1738 text (36)
								1739 text The supplied word error gives
								1740 container
									1741 container
										1742 container
											1743 text ∥ ( 𝑊 ( 𝑠
											1744 text )
											1745 text 𝑛
											1746 text −
											1747 text 𝑒
											1748 container
												1749 text 𝑇 𝐷
											1750 text )
											1751 text 𝑈
											1752 text 0
											1753 text ∥
											1754 text 2
										1755 container
											1756 text ≤ 𝑀
											1757 text 𝐶
											1758 text 0
											1759 text 𝑛
											1760 text 𝑠
											1761 text 5
											1762 text 𝑒
											1763 container
												1764 text 𝐶
												1765 text 0
												1766 text 𝑛
												1767 text 𝑠
												1768 text 5
										1769 container
											1770 text ≤
											1771 container
												1772 text 2
												1773 text 𝐶
												1774 text 0
											1775 container
												1776 text 𝐵 ∗
											1777 text 𝜌
											1778 container
												1779 text − 1
											1780 text ≤
											1781 text 𝜖
											1782 text 8
											1783 text .
									1784 text (37)
								1785 text Therefore
								1786 container
									1787 container
										1788 text ∥ 𝑊 ( 𝑠
										1789 text )
										1790 text 𝑛
										1791 text 𝑈
										1792 text 0
										1793 text ∥
										1794 text 2
										1795 text ≤ 𝜖 / 4.
									1796 text (38)
								1797 heading 5.5 Verification of the nonlinear error, Value: 3
									1798 text 5.5 Verification of the nonlinear error
								1799 text Use 
								1800 container
									1801 text 𝑎
									1802 text ∗
									1803 text ≤ 1
								1804 text  in (28). Its right-hand side is at most
								1805 container
									1806 container
										1807 text 16
										1808 text 𝐵
										1809 text ∗
										1810 container
											1811 text − 1 / 2
										1812 text 𝜌
										1813 container
											1814 text − 3
										1815 text + 768
										1816 text 𝐵
										1817 text ∗
										1818 container
											1819 text − 3 / 4
										1820 text 𝜌
										1821 container
											1822 text − 15 / 4
										1823 text + 2
										1824 text 𝐵
										1825 text ∗
										1826 container
											1827 text − 1
										1828 text 𝜌
										1829 container
											1830 text − 8
										1831 text .
									1832 text (39)
								1833 text Since 
								1834 container
									1835 text 𝜖 ≥
									1836 text 𝜌
									1837 container
										1838 text − 1
								1839 text , the choice
								1840 container
									1841 text 𝐵
									1842 text ∗
									1843 text ≥ ( 12 ⋅ 1024
									1844 text )
									1845 text 2
								1846 text makes (39) at most 
								1847 container
									1848 text 𝜖 / 4
								1849 text . Combining this with (38),
								1850 container
									1851 container
										1852 text ∥ 𝑈 ( 𝛿 )
										1853 text ∥
										1854 text 2
										1855 text ≤ 𝜖 / 2.
									1856 text (40)
								1857 heading 6. The actual rational piecewise-polynomial force, Value: 2
									1858 text 6. The actual rational piecewise-polynomial force
								1859 text It remains to implement the carrier and approximate its viscosity term using rational coefficients.
								1860 heading 6.1 Quadratic pulses, Value: 3
									1861 text 6.1 Quadratic pulses
								1862 text There are 
								1863 container
									1864 text 𝑚 𝑛
								1865 text  pulses. Give each pulse the rational duration
								1866 container
									1867 container
										1868 text 𝑑 =
										1869 text 𝛿
										1870 container
											1871 text 𝑚 𝑛
										1872 text =
										1873 text 1
										1874 container
											1875 text 𝑚
											1876 text 𝐵
											1877 text ∗
											1878 text 10
											1879 text 𝜌
											1880 text 36
										1881 text .
									1882 text (41)
								1883 text Let
								1884 container
									1885 text 𝑞 ( 𝑧 ) = 6 𝑧 ( 1 − 𝑧 ) ,
									1886 text ∫
									1887 text 0
									1888 text 1
									1889 text 𝑞 ( 𝑧 ) 𝑑 𝑧 = 1.
								1890 text For pulse 
								1891 text 𝑖
								1892 text , put
								1893 container
									1894 text 𝑡
									1895 text 𝑖
									1896 text = 𝑖 𝑑 , ℓ = 1 + ( 𝑖
									1897 container
										1898 text m o d
									1899 text 𝑚 ) , 𝜁 =
									1900 container
										1901 text 𝑡 −
										1902 text 𝑡
										1903 text 𝑖
									1904 text 𝑑
									1905 text .
								1906 text Define
								1907 container
									1908 container
										1909 text 𝑤 ( 𝑡 , 𝑥 ) =
										1910 container
											1911 text 𝛼
											1912 text ℓ
											1913 text 𝑠
										1914 text 𝑑
										1915 text 𝑞 ( 𝜁 )
										1916 text 𝐺
										1917 container
											1918 text ȷ ℓ
										1919 text ( 𝑥 ) ,
										1920 text 𝑡
										1921 text 𝑖
										1922 text ≤ 𝑡 ≤
										1923 text 𝑡
										1924 container
											1925 text 𝑖 + 1
										1926 text .
									1927 text (42)
								1928 text Its signed impulse is precisely 
								1929 container
									1930 text 𝛼
									1931 text ℓ
									1932 text 𝑠
								1933 text . Hence the inviscid endpoint operator is exactly 
								1934 container
									1935 text 𝑊 ( 𝑠
									1936 text )
									1937 text 𝑛
								1938 text . The carrier vanishes at every pulse boundary because 
								1939 container
									1940 text 𝑞 ( 0 ) = 𝑞 ( 1 ) = 0
								1941 text . It is continuous throughout, and its time derivative is bounded and piecewise polynomial. This produces ordinary forcing with no distributional impulses.
								1942 heading 6.2 Rational approximation of the Laplacian eigenvalues, Value: 3
									1943 text 6.2 Rational approximation of the Laplacian eigenvalues
								1944 text Each selected shear is a single Fourier mode with an integer wavevector 
								1945 container
									1946 text 𝑘 𝑗
								1947 text , so
								1948 container
									1949 text − Δ
									1950 text 𝐺
									1951 text 𝑗
									1952 text =
									1953 text 𝜅
									1954 text 2
									1955 text ∣
									1956 text 𝑘
									1957 text 𝑗
									1958 text ∣
									1959 text 2
									1960 text 𝐺
									1961 text 𝑗
									1962 text , 𝜅 = 2 𝜋 .
								1963 text The ideal coefficient on a pulse would be
								1964 container
									1965 container
										1966 container
											1967 text 𝛼
											1968 text ℓ
											1969 text 𝑠
										1970 container
											1971 text 𝑑 2
										1972 text 𝑞
										1973 text ′
										1974 text ( 𝜁 ) + 𝜈
										1975 text 𝜅
										1976 text 2
										1977 text ∣
										1978 text 𝑘
										1979 container
											1980 text ȷ ℓ
										1981 text ∣
										1982 text 2
										1983 container
											1984 text 𝛼
											1985 text ℓ
											1986 text 𝑠
										1987 text 𝑑
										1988 text 𝑞 ( 𝜁 ) .
									1989 text (43)
								1990 text Compute a rational dyadic number 
								1991 text 𝜃
								1992 text  approximating 
								1993 container
									1994 text 𝜅 2
								1995 text , and output
								1996 container
									1997 container
										1998 text 𝑐
										1999 container
											2000 text ȷ ℓ
										2001 text ( 𝑡 ) =
										2002 container
											2003 text 𝛼
											2004 text ℓ
											2005 text 𝑠
										2006 container
											2007 text 𝑑 2
										2008 text 𝑞
										2009 text ′
										2010 text ( 𝜁 ) + 𝜈 𝜃 ∣
										2011 text 𝑘
										2012 container
											2013 text ȷ ℓ
										2014 text ∣
										2015 text 2
										2016 container
											2017 text 𝛼
											2018 text ℓ
											2019 text 𝑠
										2020 text 𝑑
										2021 text 𝑞 ( 𝜁 ) .
									2022 text (44)
								2023 text All other coefficients are zero on that pulse. The compiler expands (44) into an ordinary polynomial in 
								2024 text 𝑡
								2025 text . Its degree is at most two, with rational coefficients. For a completely explicit error rule, precompute rational bounds
								2026 container
									2027 text 𝐻
									2028 text 0
									2029 text ≥
									2030 container
										2031 text max ⁡
									2032 text 𝑗
									2033 text ∥
									2034 text 𝐺
									2035 text 𝑗
									2036 text ∥
									2037 text 2
									2038 text ,
									2039 text 𝐾
									2040 text 2
									2041 text ≥
									2042 container
										2043 text max ⁡
									2044 text 𝑗
									2045 text ∣
									2046 text 𝑘
									2047 text 𝑗
									2048 text ∣
									2049 text 2
									2050 text ,
									2051 text 𝛼
									2052 text ∗
									2053 text ≥
									2054 container
										2055 text max ⁡
									2056 text ℓ
									2057 text ∣
									2058 text 𝛼
									2059 text ℓ
									2060 text ∣ ,
								2061 text all at least one, and put
								2062 container
									2063 text 𝐻
									2064 text 𝑤
									2065 text = 2
									2066 text 𝛼
									2067 text ∗
									2068 text 𝑠 / 𝑑 .
								2069 text It suffices to require
								2070 container
									2071 container
										2072 text ∣ 𝜃 −
										2073 text 𝜅
										2074 text 2
										2075 text ∣ ≤
										2076 text 𝜂
										2077 container
											2078 text 1 +
											2079 text 𝐾
											2080 text 2
											2081 text 𝐻
											2082 text 0
											2083 text 𝐻
											2084 text 𝑤
										2085 text .
									2086 text (45)
								2087 text Since 
								2088 container
									2089 text 𝜈 ≤ 1
								2090 text , this guarantees
								2091 container
									2092 container
										2093 text ∥ 𝑓 −
										2094 text 𝑓
										2095 text ∗
										2096 text ∥
										2097 container
											2098 text 𝐿
											2099 text ∞
											2100 text 𝐿
											2101 text 2
										2102 text ≤ 𝜂 .
									2103 text (46)
								2104 text Thus we take
								2105 container
									2106 text 𝜉 = 𝜂 ,
									2107 text 𝑎
									2108 text ∗
									2109 text ≤ 2 𝜂 =
									2110 text 1
									2111 container
										2112 text 8 𝜌
									2113 text < 1 ,
								2114 text as required above. One deterministic rational implementation of (45) uses
								2115 container
									2116 text 𝜋 = 16 arctan ⁡ ( 1 / 5 ) − 4 arctan ⁡ ( 1 / 239 )
								2117 text with the alternating power series and its explicit remainder bounds, followed by rational squaring and dyadic rounding. The required precision is 
								2118 container
									2119 text 𝑂 ( log ⁡ 𝜌 )
								2120 text , with a fixed additive constant from the precomputation.
								2121 heading 6.3 Switch off the control, Value: 3
									2122 text 6.3 Switch off the control
								2123 text Set every 
								2124 container
									2125 text 𝑐
									2126 text 𝑗
									2127 text = 0
								2128 text  on 
								2129 container
									2130 text ( 𝛿 , 𝜏 ]
								2131 text . For every Leray–Hopf continuation, the energy inequality gives
								2132 container
									2133 container
										2134 text ∥ 𝑈 ( 𝑡 )
										2135 text ∥
										2136 text 2
										2137 text ≤ ∥ 𝑈 ( 𝛿 )
										2138 text ∥
										2139 text 2
										2140 text +
										2141 text ∫
										2142 text 𝛿
										2143 text 𝑡
										2144 text ∥ ℎ ( 𝑟 )
										2145 text ∥
										2146 text 2
										2147 text 𝑑 𝑟 .
									2148 text (47)
								2149 text The inequality can be started at 
								2150 text 𝛿
								2151 text  by approaching it through admissible starting times from below, where the solution agrees with the strong solution and is strongly continuous. Taking the specified one-sided energy trace gives the same bound at 
								2152 container
									2153 text 𝑡 = 𝜏
								2154 text . Consequently,
								2155 container
									2156 container
										2157 container
											2158 text ∥ 𝑈 ( 𝜏 )
											2159 text ∥
											2160 text 2
										2161 container
											2162 text ≤
											2163 text 𝜖
											2164 text 2
											2165 text + 𝜂 ( 𝜏 − 𝛿 )
										2166 container
											2167 text ≤
											2168 text 𝜖
											2169 text 2
											2170 text +
											2171 text 1
											2172 container
												2173 text 16 𝜌
										2174 container
											2175 text ≤
											2176 container
												2177 text 9 𝜖
											2178 text 16
											2179 text < 𝜖 .
									2180 text (48)
								2181 text This proves the endpoint contract for every admissible initial state, disturbance, and Leray–Hopf realization.
								2182 heading 7. Physical resource bounds, Value: 2
									2183 text 7. Physical resource bounds
								2184 text The pulse duration (41) gives the exact scalings
								2185 container
									2186 container
										2187 text 𝑠
										2188 text 𝑑
										2189 text = 𝑚
										2190 text 𝐵
										2191 text ∗
										2192 text 8
										2193 text 𝜌
										2194 text 30
										2195 text ,
										2196 text 𝑠
										2197 container
											2198 text 𝑑 2
										2199 text =
										2200 text 𝑚
										2201 text 2
										2202 text 𝐵
										2203 text ∗
										2204 text 18
										2205 text 𝜌
										2206 text 66
										2207 text .
									2208 text (49)
								2209 text All spatial fields belong to the fixed finite family. Choose a fixed rational bound
								2210 container
									2211 text 𝐻
									2212 text 1
									2213 text ≥
									2214 container
										2215 text max ⁡
									2216 text 𝑗
									2217 text ∥
									2218 text 𝐺
									2219 text 𝑗
									2220 text ∥
									2221 container
										2222 text 𝑊
										2223 text 1
										2224 text ,
										2225 text ∞
									2226 text .
								2227 text We may keep 
								2228 container
									2229 text ∣ 𝜃 ∣ ≤ 65
								2230 text , since 
								2231 container
									2232 text 4
									2233 text 𝜋
									2234 text 2
									2235 text < 64
								2236 text . Using
								2237 container
									2238 text ∥ 𝑞
									2239 text ∥
									2240 text ∞
									2241 text =
									2242 text 3
									2243 text 2
									2244 text , ∥
									2245 text 𝑞
									2246 text ′
									2247 text ∥
									2248 text ∞
									2249 text = 6 ,
								2250 text equation (44) gives
								2251 container
									2252 container
										2253 container
											2254 text sup ⁡
										2255 text 𝑡
										2256 text ∥ 𝑓 ( 𝑡 )
										2257 text ∥
										2258 container
											2259 text 𝑊
											2260 text 1
											2261 text ,
											2262 text ∞
										2263 text ≤
										2264 text 𝐶
										2265 text 𝑓
										2266 text 𝜌
										2267 text 66
										2268 text ,
									2269 text (50)
								2270 text where, for example, the fixed computable constant
								2271 container
									2272 container
										2273 text 𝐶
										2274 text 𝑓
										2275 text =
										2276 text 𝐻
										2277 text 1
										2278 text 𝛼
										2279 text ∗
										2280 text (
										2281 text 6
										2282 container
											2283 text 𝑚 2
										2284 container
											2285 text 𝐵 ∗ 18
										2286 text +
										2287 text 100
										2288 container
											2289 text 𝐾 2
										2290 text 𝑚
										2291 container
											2292 text 𝐵 ∗ 8
										2293 text )
									2294 text (51)
								2295 text suffices. The force is supported on 
								2296 container
									2297 text [ 0 , 𝛿 ]
								2298 text , so
								2299 container
									2300 container
										2301 text ∫
										2302 text 0
										2303 text 𝜏
										2304 text ∥ 𝑓 ( 𝑡 )
										2305 text ∥
										2306 container
											2307 text 𝑊
											2308 text 1
											2309 text ,
											2310 text ∞
										2311 text 𝑑 𝑡 ≤
										2312 container
											2313 text 𝐶 𝑓
										2314 container
											2315 text 𝐵 ∗
										2316 text 𝜌
										2317 text 58
										2318 text .
									2319 text (52)
								2320 text Also,
								2321 container
									2322 container
										2323 text 𝜂
										2324 container
											2325 text − 1
										2326 text = 16 𝜌 ≤ 32 𝑅 .
									2327 text (53)
								2328 text Using 
								2329 container
									2330 text 𝜌 ≤ 2 𝑅
								2331 text , these are the claimed polynomial physical bounds. The number of intervals, including the final zero-force interval, is
								2332 container
									2333 container
										2334 text 𝑚 𝑛 + 1 = 𝑚
										2335 text 𝐵
										2336 text ∗
										2337 text 9
										2338 text 𝜌
										2339 text 28
										2340 text + 1.
									2341 text (54)
								2342 heading 8. Bit complexity and payment for the fixed precomputation, Value: 2
									2343 text 8. Bit complexity and payment for the fixed precomputation
								2344 heading 8.1 The online compiler uses finite arithmetic, Value: 3
									2345 text 8.1 The online compiler uses finite arithmetic
								2346 text The online algorithm is:
								2347 content list
									2348 container
										2349 AXListMarker 1. 
										2350 text Read the rational inputs and calculate 
										2351 text 𝜌
										2352 text .
									2353 container
										2354 AXListMarker 2. 
										2355 text Calculate 
										2356 container
											2357 text 𝑠 , 𝑛 , 𝛿 , 𝜂 , 𝑑
										2358 text  using (34) and (41).
									2359 container
										2360 AXListMarker 3. 
										2361 text Calculate the rational approximation 
										2362 text 𝜃
										2363 text  satisfying (45).
									2364 container
										2365 AXListMarker 4. 
										2366 text Emit the 
										2367 container
											2368 text 𝑚 𝑛
										2369 text  quadratic pulse records from (44), expanded in global time.
									2370 container
										2371 AXListMarker 5. 
										2372 text Emit the final zero-force interval and 
										2373 text 𝜂
										2374 text .
								2375 text It evaluates no PDE solution, unknown initial condition, disturbance, optimization problem, or infinite-dimensional norm. The integers 
								2376 text 𝑛
								2377 text , the interval endpoints, and all pulse parameters have 
								2378 container
									2379 text 𝑂 ( 𝐿 + log ⁡ 𝜌 )
								2380 text  bits, with fixed additive constants. Expanding a polynomial into global time can produce coefficients with numerical magnitudes as large as 
								2381 container
									2382 text 𝐶
									2383 text 𝜌
									2384 text 102
								2385 text , because of factors 
								2386 container
									2387 text 𝑑
									2388 text −
									2389 text 3
								2390 text . Their bit lengths are still
								2391 container
									2392 text 𝑂 ( 𝐿 + log ⁡ 𝜌 ) .
								2393 text The actual force values obey (50); the expansion introduces no extra physical cost. The certified arctangent calculation needs polynomially many bit operations in the requested precision. Using elementary exact rational arithmetic, a deliberately loose overall online bound is
								2394 container
									2395 container
										2396 text 𝐶
										2397 container
											2398 text a r i t h
										2399 text (
										2400 text 𝜌
										2401 text 28
										2402 text + 1 ) ( 𝐿 +
										2403 container
											2404 text log ⁡
										2405 text 2
										2406 text 𝜌 + 1
										2407 text )
										2408 text 8
										2409 text ,
									2410 text (55)
								2411 text for a fixed computable 
								2412 container
									2413 text 𝐶
									2414 text a
									2415 text r
									2416 text i
									2417 text t
									2418 text h
								2419 text . Total output bits and working-memory bits satisfy bounds of this form as well.
								2420 heading 8.2 A specified finite precomputation, Value: 3
									2421 text 8.2 A specified finite precomputation
								2422 text The precomputation consists of:
								2423 content list
									2424 container
										2425 AXListMarker 1. 
										2426 text Executing the effective fixed-family and word construction granted in your premises, retaining its full descriptions, bounds, and finite resource certificate.
									2427 container
										2428 AXListMarker 2. 
										2429 text Computing the commutator bounds from the returned Fourier data.
									2430 container
										2431 AXListMarker 3. 
										2432 text Computing 
										2433 container
											2434 text 𝜎 ,
											2435 text 𝐶
											2436 text 𝐷
											2437 text ,
											2438 text 𝐶
											2439 text 𝐸
											2440 text ,
											2441 text 𝐵
											2442 text ∗
										2443 text , and the fixed force and arithmetic bounds.
									2444 container
										2445 AXListMarker 4. 
										2446 text Fixing the exact rational-output encoding and schoolbook arithmetic implementation.
								2447 text This needs only the supplied estimates at orders 
								2448 container
									2449 text 0 , 1 , 2
								2450 text . To give an explicit way of selecting a common resource constant, let 
								2451 container
									2452 text 𝑁
									2453 text ∗
									2454 text ≥
									2455 text 2
									2456 text 20
								2457 text  be a computed integer dominating:
								2458 content list
									2459 container
										2460 AXListMarker • 
										2461 text The certified operation, memory, and description bounds of the entire fixed precomputation.
									2462 container
										2463 AXListMarker • 
										2464 text All fixed list lengths.
									2465 container
										2466 AXListMarker • 
										2467 container
											2468 text 𝐵 ∗
										2469 text , all fixed rational numerator and denominator heights, and the Fourier frequency bounds.
									2470 container
										2471 AXListMarker • 
										2472 text The direct Fourier norm and commutator bounds.
									2473 container
										2474 AXListMarker • 
										2475 text The fixed constants in the elementary arithmetic implementation.
								2476 text Enlarge it, by explicit integer arithmetic, to cover the finitely many fixed constants appearing in (50)–(55). Define
								2477 container
									2478 container
										2479 text 𝑝 = 128 , 𝐴 = ( 2
										2480 text 𝑁
										2481 text ∗
										2482 text )
										2483 text 1024
										2484 text .
									2485 text (56)
								2486 text This is a fixed, explicitly computable choice. The generous powers cover all fixed factors, the replacements 
								2487 container
									2488 text 𝜌 ≤ 2 𝑅
								2489 text , and the elementary arithmetic bound. The variable exponents in (50)–(55) are below 
								2490 text 128
								2491 text . Therefore the construction satisfies
								2492 container
									2493 container
										2494 text bit operations, working-memory bits, total output bits,
										2495 container
											2496 text interval count, degrees, and individual rational bit lengths ≤ 𝐴 ( 𝐿 + 𝑅
											2497 text )
											2498 text 128
											2499 text ,
									2500 text (57)
								2501 text and
								2502 container
									2503 container
										2504 text 𝜂
										2505 container
											2506 text − 1
										2507 text ,
										2508 container
											2509 text sup ⁡
										2510 text 𝑡
										2511 text ∥ 𝑓 ( 𝑡 )
										2512 text ∥
										2513 container
											2514 text 𝑊
											2515 text 1
											2516 text ,
											2517 text ∞
										2518 text ,
										2519 text ∫
										2520 text 0
										2521 text 𝜏
										2522 text ∥ 𝑓 ( 𝑡 )
										2523 text ∥
										2524 container
											2525 text 𝑊
											2526 text 1
											2527 text ,
											2528 text ∞
										2529 text 𝑑 𝑡 ≤ 𝐴
										2530 text 𝑅
										2531 text 128
										2532 text .
									2533 text (58)
								2534 text The first precomputation subroutine is precisely the effective fixed-word construction you supplied as accepted capital. Its full cost is included in 
								2535 text 𝐴
								2536 text ; no numerical rotation design or uncharged search is being introduced here.
								2537 heading What closes the nonlinear interface, Value: 2
									2538 text What closes the nonlinear interface
								2539 text The decisive additional implication is
								2540 container
									2541 text stable partial blocks in 
									2542 text 𝐻
									2543 text 0
									2544 text ,
									2545 text 𝐻
									2546 text 1
									2547 text ,
									2548 text 𝐻
									2549 text 2
									2550 text + [ Δ ,
									2551 text 𝐿
									2552 text 𝐹
									2553 text ] :
									2554 text 𝐻
									2555 text 2
									2556 text →
									2557 text 𝐿
									2558 text 2
									2559 text ⟹ polynomial nonlinear control over a short interval .
								2560 text The proof uses a different coordinate chart for each macro-block. Viscosity is controlled inside that chart, and the supplied 
								2561 container
									2562 text 𝐻 1
								2563 text  endpoint estimate controls the reset. This yields the uniform bounds (25), which make the nonlinear and viscous residuals integrable in 
								2564 container
									2565 text 𝐿 2
								2566 text . The stable forward propagator then gives the polynomial endpoint estimate (28). With the explicit compiler above, the carrier returns to zero, the same force works for the entire prescribed 
								2567 container
									2568 text 𝐻 1
								2569 text  ball, and every admissible realization satisfies the stronger endpoint bound
								2570 container
									2571 text ∥ 𝑈 ( 𝜏 )
									2572 text ∥
									2573 text 2
									2574 text ≤ 9 𝜖 / 16.
								2575 text Thus the full polynomial-resource contract follows from the supplied constructive premises.
								2576 

## Available visible activity (accessibility representation)

button (expanded) Worked for 18m 26s, Secondary Actions: Collapse
									42 text Worked for 18m 26s
									43 image
								2612 text I’ll investigate the polynomial resource requirement directly, using parallel work on nonlinear stability, alternative constructions, and possible obstructions. I’ll distinguish a full solution from any advance that still leaves part of the compiler unproved.
								2613 container Subagent activity
									2614 container
										2615 button Nonlinear polynomial
										2616 text , 
										2617 button Alternative constructions
										2618 text  and 
										2619 button Obstructions audit
										2620 text  started working
								2621 text Searching arxiv.org
								2622 text Filtered source results and assessed pulled-back viscosity
								2623 container Subagent activity
									2624 container
										2625 button Nonlinear polynomial
										2626 text  updated
								2627 text Searched 20 websites
								2628 text Established blockwise H1 and H2 smoothing bounds
								2629 text The linear contraction already has polynomial cost under your premises: a contraction factor 
								2630 text 𝛾
								2631 text  can be obtained with auxiliary time 
								2632 container
									2633 text 𝑂 (
									2634 text 𝛾
									2635 container
										2636 text − 2
									2637 text )
								2638 text  and 
								2639 container
									2640 text 𝑂 (
									2641 text 𝛾
									2642 container
										2643 text − 14
									2644 text )
								2645 text  blocks. I’m now testing whether changing coordinates within each block—and resetting them at its endpoint—can keep viscosity and nonlinear error under control without the accumulated 
								2646 container
									2647 text 𝑒 𝐾
								2648 text  loss. Checked commutator bounds
								2649 container Subagent activity
									2650 container
										2651 button Alternative constructions
										2652 text , 
										2653 button Nonlinear polynomial
										2654 text  and 
										2655 button Obstructions audit
										2656 text  updated
								2657 text Specified finite precomputation and made constants explicit
								2658 text Searched 6 websites
								2659 text Checked propagator bounds and chose parameter scales
								2660 text Tuned slack constants and bounded compiler complexity
								2661 text Fixed constants and scales
								2662 container Subagent activity
									2663 container
										2664 button Nonlinear polynomial
										2665 text  finished
								2666 text Estimating the H1 energy
								2667 text Estimated nonlinear pairing
								2668 text Verified energy bootstrap and integrated dissipation estimate
								2669 text Checked bounds and selected semigroup constants
								2670 text Bounded the Duhamel error with explicit constants
								2671 text Derived rational-mode error bound
								2672 text Prepared certified Machin bounds and verified disturbed-flow uniqueness
								2673 text Established the energy bound
								2674 text Derived semigroup decay bound and precomputed rational decay constant
								2675 text Chose σ and B and precomputed σ bounds
								2676 text Computed derivative and explicit norm bounds
								2677 text Estimated bounds and specified piecewise forcing
								2678 text Chose dyadic approximation and bounded the compiler constant
								2679 text Determined a valid A and clarified supplied premises
								2680 text The blockwise approach now gives a concrete estimate. The commutator 
								2681 container
									2682 text [ Δ ,
									2683 text 𝐿
									2684 text 𝐹
									2685 text ]
								2686 text  bounds the change in viscosity within a block by 
								2687 container
									2688 text 𝑂 ( 𝑠 )
								2689 text , which can be absorbed by viscous dissipation. At block boundaries, the supplied 
								2690 container
									2691 text 𝐻 1
								2692 text  estimate costs only 
								2693 container
									2694 text 1 + 𝑂 (
									2695 text 𝑠
									2696 text 5
									2697 text )
								2698 text . I’m checking the resulting nonlinear bound, its extension to every Leray–Hopf solution, and the rational pulse costs before concluding that this closes the question. Verified Agmon estimates and refined weighted energy bounds Checked the B error bound Prepared technical proof, finite precomputation, and pulse coefficient verification Prepared rational pulses, verified regularity, and computed energy identity Checked commutator and uniqueness bounds Derived explicit coefficient bounds
								2699 container Subagent activity
									2700 container
										2701 button Obstructions audit
										2702 text  updated
								2703 text Searching 2 websites
								2704 container Subagent activity
									2705 container
										2706 button Alternative constructions
										2707 text  finished
								2708 text Confirmed proof completeness and bounded forward propagation Precomputed fixed-family bounds and chose explicit D0 bounds Precomputed coefficient bounds and set polynomial resource limits Calculated explicit constants Combined decay estimates and verified pulse bounds Computed the explicit force bound Checked novelty and framed theorem from premises The independent audits support the nonlinear argument. A simple parameter choice now gives degree-two rational pulses, at most 
								2709 container
									2710 text 𝐶
									2711 text 𝑅
									2712 text 28
								2713 text  intervals, force magnitude at most 
								2714 container
									2715 text 𝐶
									2716 text 𝑅
									2717 text 66
								2718 text , and disturbance tolerance 
								2719 container
									2720 text 𝜂
									2721 container
										2722 text − 1
									2723 text ≤ 32 𝑅
								2724 text . I’m assembling the proof and explicitly accounting for the fixed precomputation and rational approximation of the Laplacian eigenvalues.
								2725 container Subagent activity
									2726 container
										2727 button Obstructions audit
										2728 text  finished
								2729 text Computed coefficient bounds Computed N_* bounds and set explicit arithmetic limits Checked resource bounds and defined total input handling Verified the energy estimate and checked index bounds Checked the energy-tail bound Refined proof notation and pulse coefficients Set constants and bounds
								44 

