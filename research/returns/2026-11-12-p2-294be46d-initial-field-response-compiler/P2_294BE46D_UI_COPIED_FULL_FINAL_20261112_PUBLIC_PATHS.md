**Yes—relative to the quantitative backend constructions explicitly accepted in your question, the initial-data compiler can be completed.** The new steps are:

1. A **simultaneous finite-Fourier router** that acquires all retained features before discarding any unread information.
2. A **regenerative magnetic memory** that cancels first-order resistive loss using two copies at frequencies \(n\) and \(2n\).
3. A sparse arithmetic implementation using independent three-input products, with \(O(SD)\) assignments.

The router is also the main error-control device. It has a uniform, absolute endpoint guarantee relative to the features of its **actual incoming state**. Historical errors therefore pass through the intended finite-dimensional operation. They do not acquire a new microscopic implementation gain at every assignment.

The physical order is
\[
\boxed{
\text{capture initial features}
\;\longrightarrow\;
\text{regenerative storage}
\;\longrightarrow\;
\text{sparse arithmetic}
\;\longrightarrow\;
\text{final magnetic and velocity write}.
}
\]

I give the new constructions, their composition, and the resource certificate below. The conclusion uses the accepted scalar-transition, reset, directional-restore, decoder, and final-readout services at their stated **uniform smooth-reference, prescribed-duration, and rough-perturbation contracts**.

Write
\[
\kappa=2\pi,\qquad
\mu=\min(\nu_-,\rho_-),\qquad
\mathscr C=\kappa^{-1}\operatorname{curl}.
\]

## 1. Reduce the input without expanding the polynomial catalogue

Canonicalize and aggregate the complete rational input first.

Choose
\[
N_{\rm probe}
=
\left\lceil \frac{2^{16}KD}{\epsilon}\right\rceil,
\qquad
N_{\rm out}
=
\left\lceil \frac{2^{16}K}{\epsilon}\right\rceil.
\]

For a probe with \(|k|_\infty>N_{\rm probe}\), the initial \(H^1\) bound gives
\[
\left|
M^{-1}\int B_{0,i}\psi_k
\right|
\le \frac{C}{|k|}.
\]
Replace that formal input by zero. A monomial of degree at most \(D\), evaluated on the unit coordinate cube, has Lipschitz constant at most \(D\) in the maximum norm. Thus the resulting joint target error is bounded by
\[
\frac{CKD}{N_{\rm probe}}.
\tag{1}
\]

Discard output spatial frequencies above \(N_{\rm out}\). The coefficient envelope gives a further \(L^2\) target error at most
\[
\frac{CK}{N_{\rm out}}.
\tag{2}
\]

Both cutoffs are applied by integer comparison to the listed frequencies. There is no loop to an input frequency’s numerical maximum.

Let \(r\le q+3\) denote the retained source count, including the three mean coordinates. Means will be treated as \(k=0\), cosine features.

For each listed nonconstant even monomial, choose one index \(j\) with positive exponent:
\[
h^\alpha=h_jh^{\alpha-e_j}.
\tag{3}
\]
The second factor is odd. Every odd monomial can be formed by starting with one source and multiplying two further source factors at a time.

Consequently, it is enough to compute:

- the odd monomials appearing in \(Z\);
- one odd monomial \(h^{\alpha-e_j}\) for every nonconstant even term of \(U\);
- the retained original sources.

This requires at most
\[
N_{\rm arith}\le C S(D+1)
\tag{4}
\]
assignments and \(C(r+S+1)\) code slots. No parity-sector enumeration is used.

## 2. A paid finite-Fourier router

Here is the new service that makes both acquisition and repeated computation possible.

### Router lemma

Suppose the actual input to one invocation satisfies
\[
\|(u_{\rm in},B_{\rm in})\|_{H^1}\le P,
\qquad H=\int B_{\rm in}.
\]
List \(r\) raw real Fourier features
\[
x_j=\int (B_{\rm in})_{i_j}\psi_j,
\qquad |k_j|_\infty\le N.
\]
Zero-frequency cosine features are permitted.

Let \(\mathsf K=(K_{\ell j})\) be a known rational matrix and let \(f_\ell\) be distinct positive integer output frequencies. Define
\[
K_1=\max\left(1,\sum_{\ell,j}|K_{\ell j}|\right),
\qquad F=\max_\ell f_\ell.
\]

For every error tolerance \(\delta>0\) and duration cap \(t_*>0\), there is an ordinary mechanical programme, using the twelve actuators, whose duration is at most \(t_*\) and whose endpoint satisfies
\[
\begin{aligned}
\|u_{\rm out}\|_{H^1}
+
\left\|
B_{\rm out}
-
H-e_3\sum_\ell(\mathsf Kx)_\ell
       \sin(\kappa f_\ell x_2)
\right\|_{H^1}
\le\delta .
\end{aligned}
\tag{5}
\]

The guarantee is uniform over the entire \(H^1\) input ball, all admitted coefficient histories, and all disturbances below a supplied positive budget. Its numerical costs and reciprocal disturbance tolerance are bounded by a fixed polynomial in
\[
2+P+N+F+r+\#\{\ell\}+K_1+\delta^{-1}+t_*^{-1}
+\mu^{-1}+\Lambda.
\tag{6}
\]

The force never receives \(x\). Equation (5) describes the physical endpoint.

### 2.1 Three transitions pack all source coordinates

First establish the ideal algebra for a smooth field \(B\). Set
\[
T_i(\phi)B=B+\mathscr C(e_i\phi B_i).
\]

Choose an integer \(n\ge12(N+1)\), and put
\[
v=e_1+e_3,\qquad
B_*=8(r+1),
\]
\[
a_j=c_j=jn,\qquad
b_j=B_*jn,\qquad m_j=b_je_3.
\]

Define
\[
\phi_1
=
\sum_{j:i_j=1}
\frac{\cos\!\bigl(\kappa(a_jv-k_j)\cdot x\bigr)}{a_j},
\tag{7}
\]
\[
\phi_3
=
-\sum_{j:i_j=3}
\frac{\cos\!\bigl(\kappa(c_je_1-k_j)\cdot x\bigr)}{c_j}.
\tag{8}
\]

Use the source anchors
\[
s_j=
\begin{cases}
a_jv,&i_j=1,\\
k_j,&i_j=2,\\
c_je_1,&i_j=3,
\end{cases}
\qquad
\lambda_j=b_je_3-s_j,
\]
and set
\[
\phi_2
=
\sum_{j:i_j\in\{1,3\}}
\frac{2\cos(\kappa\lambda_j\cdot x)}{b_j}
-
\sum_{j:i_j=2}
\frac{\sin(\kappa\lambda_j\cdot x)}{b_j}.
\tag{9}
\]

Apply all three transitions before any projection:
\[
\widetilde B=T_2(\phi_2)T_3(\phi_3)T_1(\phi_1)B.
\]

Their selected coefficients satisfy
\[
\boxed{
\widehat{\widetilde B}_1(m_j)
=
\frac12\widehat B_{i_j}(k_j)+e_j,
\qquad
|e_j|\le \frac{C r^9\|B\|_{H^1}}{n}.
}
\tag{10}
\]

This is simultaneous packing in one magnetic field.

### 2.2 Why the desired coefficients and aliases have these forms

The Fourier multiplier of the added part is
\[
\widehat{\mathscr C(e_i\phi B_i)}(\xi)
=
i(\xi\times e_i)
\sum_\mu\widehat\phi(\mu)\widehat B_i(\xi-\mu).
\tag{11}
\]

For a coordinate-1 probe, the first transition creates the shadow
\[
\widehat B_2(a_jv)
=
\frac{i}{2}\widehat B_1(k_j)+\text{aliases}.
\]
For a coordinate-3 probe, the second transition creates
\[
\widehat B_2(c_je_1)
=
\frac{i}{2}\widehat B_3(k_j)+\text{aliases}.
\]
At \(m_j=b_je_3\), the component-1 multiplier of the last transition is \(-ib_j\). Its cosine mask therefore sends either shadow to
\[
(-i)\frac{i}{2}\widehat B_{i_j}(k_j)
=
\frac12\widehat B_{i_j}(k_j).
\]
The negative sine mask in (9) gives the same coefficient directly from \(B_2(k_j)\).

For the aliases, expand the fixed three-transition composition. Each selected output coefficient has at most \(20r^3\) Fourier paths.

A wrong final tag contains \(b_j-b_\ell\), or \(b_j+b_\ell\), whose magnitude exceeds the possible cancellation from the earlier shadows. For the matching final tag, the directions \(e_1+e_3\) and \(e_1\) leave exactly one path back to a low input frequency. Every other path has an integer carrier remainder of magnitude at least \(n\), plus at most three probe frequencies. Hence its original input frequency has magnitude at least \(n/2\).

All intermediate frequencies are bounded by \(50r^2n\). Each mask coefficient is at most \(1/n\), so every differential multiplier is bounded by \(50r^2\). Finally,
\[
|\widehat B(\xi)|\le \frac{C\|B\|_{H^1}}{|\xi|}.
\]
These estimates give (10), with a universal computable constant.

The argument includes negative frequencies, real conjugates, duplicate probes, and \(k=0\) mean probes.

### 2.3 One rank restore extracts the requested quadratures

Write \(y=x_2,z=x_3\), and let
\[
\chi_j(z)=
\begin{cases}
\cos(\kappa b_jz),&\psi_j\text{ is cosine},\\
\sin(\kappa b_jz),&\psi_j\text{ is sine}.
\end{cases}
\]
Define
\[
\Phi(y,z)
=
\sum_{\ell,j}
\frac{2K_{\ell j}}{f_\ell}
\cos(\kappa f_\ell y)\chi_j(z).
\tag{12}
\]

The ideal restore is
\[
\mathcal R=P_zT_1(\Phi)P_yP_x,
\tag{13}
\]
where \(P_x,P_y,P_z\) are coordinate averages.

The first two averages retain the transverse \(z\)-bank. The final average removes its old nonconstant components. Since
\[
[\mathscr C(e_1\Phi B_1)]_3
=
-\kappa^{-1}\partial_y(\Phi B_1),
\]
the output is
\[
H+e_3\sum_\ell
\left(\sum_jK_{\ell j}x_j+\text{alias error}\right)
\sin(\kappa f_\ell y).
\tag{14}
\]

The factors of two are important: a real sine or cosine field amplitude is twice its corresponding raw Fourier integral.

Equation (13) is a coordinate permutation of the accepted finite-rank restore, with its known matrix-routing extension. The scalar-transition and magnetic-preserving reset contracts used here are the whole-field contracts of the [earlier construction](https://github.com/harjassand/astra-research-knowledge/blob/31100cf85bfe60ae54bcc2b7be4d16f0f4cd5497/research/returns/2026-11-11-p2-814186-human-complete-five-gate-compiler/P2_814186_HUMAN_SUPPLIED_FULL_FINAL_20261111_PUBLIC_PATHS.md); the underlying rank-restore identity is recorded in the [register construction](https://github.com/harjassand/astra-research-knowledge/blob/main/research/returns/2026-11-11-p2-79394f-complete-nonlinear-registers/P2_79394F_UI_COPIED_FULL_FINAL_20261111_PUBLIC_PATHS.md).

### 2.4 Physical realization on an arbitrary actual \(H^1\) input

An individual ideal \(T_i\) can lose a spatial derivative. Its physical realization must therefore use the accepted smooth-reference contract.

Choose a genuine initial unforced interval
\[
s\le
\min\left\{
\frac{t_*}{8},
\frac{c\mu^3}{(1+P)^4},
\frac{\delta}
{C(1+F)K_1(PN^2+P^2N+1)}
\right\}.
\tag{15}
\]

The weak induction test gives
\[
|x_j(s)-x_j(0)|
\le Cs(PN^2+P^2N+\eta).
\tag{16}
\]
Thus this interval preserves the requested features to the allocated accuracy.

Start a zero-disturbance reference from the **same entire actual input state**. At time \(s\), it has fixed-order smooth envelopes polynomial in
\[
P,\quad \mu^{-1},\quad s^{-1}.
\]
Use sufficiently many fixed derivatives to cover the four scalar transitions. Apply the accepted velocity reset while preserving this whole smooth magnetic reference, then realize (7)–(13).

Choose
\[
n\ge
\max\left\{
12(N+1),
\frac{C(1+F)K_1r^9P}{\delta}
\right\}.
\tag{17}
\]
This pays the aliases in the final \(H^1\) code norm.

After \(s,n\), and the smooth envelopes are fixed, allocate the physical transition, reset, restore, and rounding tolerances backward through this fixed number of stages. Choose the disturbance budget last.

Only the new disturbance discrepancy incurs the microscopic robustness gains. Earlier errors belong to the actual input whose features appear on the right side of (5).

This proves the router lemma. In particular, it proves acquisition from the original initial time: apply it with matrix entries incorporating \(M^{-1}\), and with no preceding magnetic eraser.

## 3. Retain the acquired sources by two-frequency regeneration

Reserve
\[
C_{\rm slots}=C(r+S+1)
\]
canonical slots, with distinct frequencies
\[
f_j\in[C_{\rm slots}+1,\,2C_{\rm slots}].
\tag{18}
\]
The doubled frequencies \(2f_j\) form a disjoint bank. The capture router can write directly into this band.

During storage use the exact sector
\[
u=e_3v(y,t),\qquad B=H+e_3b(y,t).
\]
The full equations reduce to
\[
v_t=\nu(t)v_{yy}+H_2b_y,\qquad
b_t=\rho(t)b_{yy}+H_2v_y.
\tag{19}
\]

For frequency \(n\), with \(\lambda_n=\kappa n\),
\[
\frac{d}{dt}
\binom{v_n}{b_n}
=
\begin{pmatrix}
-\nu(t)\lambda_n^2&iH_2\lambda_n\\
iH_2\lambda_n&-\rho(t)\lambda_n^2
\end{pmatrix}
\binom{v_n}{b_n}.
\tag{20}
\]
Its propagator is contractive.

Starting from \(v_n(0)=0,\ b_n(0)=r\), write
\[
b_n(d)=K_n(d)r.
\]
Twice integrating the equation, and using contraction for the remainder, gives
\[
K_n(d)
=
1-\lambda_n^2\int_0^d\rho(t)\,dt+R_n(d),
\]
\[
|R_n(d)|
\le
\frac12(\lambda_n^2+M\lambda_n)^2d^2.
\tag{21}
\]

No coefficient has been frozen or sampled.

### 3.1 Copy, hold, recombine

One refresh cycle does the following:

1. Use the router to place two copies of every current actual source value at \(n\) and \(2n\), with velocity reset.
2. Hold unforced for duration \(d\).
3. Use the router to return
   \[
   \frac{4b_n(d)-b_{2n}(d)}3
   \]
   to the canonical slot, clearing the temporary bank and disposable velocity.

Both copies coexist in the same fluid.

The ideal multiplier is
\[
\Phi_n(d)=\frac{4K_n(d)-K_{2n}(d)}3.
\]
Because \(\lambda_{2n}^2=4\lambda_n^2\),
\[
\boxed{
|\Phi_n(d)-1|\le P_0d^2.
}
\tag{22}
\]
For base frequencies \(n\le F\), one explicit rational choice is
\[
P_0=2^{14}(1+M)^2F^4.
\tag{23}
\]

This cancels the complete first-order term containing the unknown integral of \(\rho\). There is no inverse diffusion operation.

### 3.2 Physical errors and repetition

The router lemma and the short-hold perturbation estimate give the actual recurrence
\[
r^{j+1}=\Phi_jr^j+\xi_j,
\qquad
\|\xi_j\|_\infty\le\delta_{\rm local}.
\tag{24}
\]

Old errors in \(r^j\) are copied identically into both lanes. They pass through \(\Phi_j\). The absolute coefficient sum \(5/3\) affects fresh copy errors within one cycle; it is not a historical-error multiplier repeated \(J\) times.

For \(J\) cycles with \(d_j\le1/J\),
\[
\|r^J-r^0\|_\infty
\le
e^{P_0/J}
\left(
\frac{P_0\|r^0\|_\infty}{J}
+
J\delta_{\rm local}
\right).
\tag{25}
\]

For a memory tolerance \(\delta_{\rm mem}\), choose
\[
J\ge
\frac{64P_0(B+1)}{\delta_{\rm mem}},
\qquad
\delta_{\rm local}\le\frac{\delta_{\rm mem}}{64J},
\tag{26}
\]
where \(B\) bounds the current source amplitudes.

Also enlarge \(J\) to dominate the fixed polynomial local-continuation bound for the canonical code envelope and \(\mu^{-1}\). Each hold then has a bounded perturbation gain for full-space \(H^1\) errors and rough \(L^\infty_tL^2_x\) disturbances.

Copying and recombination are routers with fixed known rational matrices. Their raw-integral matrices include the factors of two needed to read stored sine amplitudes. All their fresh errors can be assigned below \(\delta_{\rm local}\) at polynomial cost.

### 3.3 Fill the prescribed clock exactly

Compile capture and the final computation with total duration below \(\tau/2\). Let their exact rational durations leave
\[
T_{\rm store}=\tau-T_{\rm capture}-T_{\rm compute}\ge\tau/2.
\]

Choose \(J\) first. Compile the active parts of one refresh cycle with total rational duration
\[
h\le \frac{T_{\rm store}}{2J},
\]
uniformly for a main hold of any duration at most \(T_{\rm store}/J\). The copy and recombination matrices do not depend on the hold duration.

Now set
\[
d=\frac{T_{\rm store}}J-h.
\tag{27}
\]
Then
\[
d\ge \frac{T_{\rm store}}{2J}>0,
\qquad
J(h+d)=T_{\rm store}
\]
exactly.

This pays the active overhead and avoids an implicit clock equation.

## 4. A three-input magnetic product

The variable-input arithmetic needs a product of three arbitrary stored odd values, not only a diagonal \(h_i^2r\) operation.

Here is an explicit triad.

Choose
\[
p_1=Qe_1,\qquad
p_2=Qe_2,\qquad
p_3=-Q(e_1+e_2)+e_3,
\]
with polarizations
\[
a_1=e_2,\qquad a_2=e_3,\qquad a_3=e_1-e_2.
\]
Each polarization is perpendicular to its wavevector.

For three current stored values \(x,y,z\), prepare positive Fourier coefficients
\[
Ax\,a_1,\qquad
Ay\,a_2,\qquad
A\frac{z}{2\kappa^2}\,a_3,
\tag{28}
\]
and their conjugates. Retain the idle source and result registers in the low canonical bank. Velocity is disposable and reset before the short interaction.

The accepted fixed-depth decoder prepares this field because its dependence on all stored values is linear.

### 4.1 Leading coefficient

For arbitrary Fourier amplitudes \(Ax,Ay,Aw\), the cubic calculation gives
\[
\widehat B_{e_3}''(0)
=
2\kappa^2QA^3xyw(e_1-e_2).
\]
Thus its leading coefficient at time \(T_c\) is
\[
\widehat B_{e_3}(T_c)
=
\kappa^2QA^3T_c^2xyw(e_1-e_2).
\tag{29}
\]

Set
\[
Q=\ell^4,\qquad A=\ell^6,\qquad T_c=\ell^{-11}.
\tag{30}
\]
Then \(QA^3T_c^2=1\). With \(w=z/(2\kappa^2)\), the leading **real cosine field amplitude** is
\[
\boxed{xyz(e_1-e_2)\cos(\kappa x_3).}
\tag{31}
\]

A final router reads twice the component-1 raw cosine integral, giving the register value \(xyz\).

The normalization uses only a known constant. Its rational approximation is included in the fresh local error budget.

### 4.2 Complete coupled remainder

The prepared reference is a finite Fourier field. Rescale
\[
\xi=Qx,\qquad s=AQt,\qquad b=B/A,\qquad v=u/A.
\tag{32}
\]
The packet frequencies in \(\xi\) are uniformly bounded. The idle bank has amplitude \(O(P/A)\) and frequency at most \(F/Q\). The scaled diffusion coefficients are bounded by
\[
Q/A=\ell^{-2},
\]
and the terminal scaled time is
\[
s_*=AQT_c=\ell^{-1}.
\]

A fixed analytic Wiener norm therefore supplies a uniform reference lifespan. At the selected low mode, the outer induction derivative contributes \(Q^{-1}\). The higher nonlinear and diffusive cubic errors have physical bounds
\[
CAQ^{-1}s_*^4=C\ell^{-2},
\]
\[
CAQ^{-1}(Q/A)s_*^3=C\ell^{-3}.
\tag{33}
\]
Terms containing the bounded idle field have additional small factors; their constants are fixed polynomials of the code envelope and its frequency.

The pure packet lattice cannot reach a nonzero idle-bank frequency along \(y\) below \(Q\). Idle-coefficient changes are consequently paid by their small direct diffusion and the mixed terms.

For the vector of all retained idle coefficients and the new product coefficient, the resulting bound has the form
\[
\|\text{selected error}\|_\infty
\le
P_{\rm code}\ell^{-2}.
\tag{34}
\]

The reference has fixed-order Sobolev bounds polynomial in \(\ell\), and
\[
\int_0^{T_c}
\|\nabla(u_{\rm ref},B_{\rm ref})\|_\infty\,dt
\le C\ell^{-1}.
\tag{35}
\]

For arbitrary incoming errors and rough disturbances, use the two-norm estimate. Schematically, with squared errors \(E_0,E_1\),
\[
E_0'
\le C L_1E_0+C\mu^{-1}\eta^2,
\]
\[
E_1'
\le
C(1+L_1)E_1
+C L_2^2E_0
+C\mu^{-3}E_1^3
+C\mu^{-1}\eta^2,
\tag{36}
\]
where \(L_1\) contains first reference derivatives and \(L_2\) contains second derivatives.

Equation (35) controls the exponential. The second derivatives multiply the already-controlled \(L^2\) error and produce a polynomial gain. A paid inverse-polynomial continuation radius controls the cubic error term.

### 4.3 Actual cleanup and overwrite

At the short interaction endpoint, the complete actual \(H^1\) envelope is polynomial in \(\ell\). Invoke the new router with that envelope. It reads:

- the idle canonical coefficients;
- the new low product coefficient;

and writes the requested updated canonical bank.

Its tiny initial smoothing interval pays any further change in those coefficients. Its subsequent packing and restore physically discard the high packets and unused low modes.

Thus a full ternary assignment has a uniform absolute code error \(\gamma\), returns velocity close to zero, and returns to the same fixed canonical band. Choose \(\ell\) polynomially large from \(\gamma^{-1}\), the code bounds, and the duration cap.

The microscopic carrier is absent from the next assignment’s endpoint envelope.

## 5. Sparse arithmetic and its error bound

For each required odd monomial:

1. Copy its first source into a work slot.
2. Read the remaining factors in pairs.
3. Apply the ternary assignment
   \[
   w\longmapsto h_a h_b w.
   \]
4. Route the completed product to its retained result slot.

A source exponent written in binary is expanded into this factor schedule in \(O(D)\) work per listed monomial. This is charged by the numerical degree \(D\).

Every physical assignment retains the source slots and previous result slots. Its output router clears the old work representation and installs the new one.

Choose, for example,
\[
\delta_s=\frac{\epsilon}{2^{20}K(D+1)},
\qquad
\gamma=\frac{\delta_s}{100(N_{\rm arith}+1)}.
\tag{37}
\]
Give capture and storage errors at most \(\delta_s\) each. The total source drift during arithmetic is at most \(N_{\rm arith}\gamma\).

Let \(E_s\) bound the resulting error of every source relative to its retained original value. Then
\[
E_s\le 3\delta_s,
\qquad DE_s\ll1.
\]

In a product chain, multiplying two approximate source values has gain at most
\[
(1+E_s)^2.
\]
Over degree at most \(D\), the total factor is bounded by
\[
(1+E_s)^D\le e^{DE_s}\le C.
\tag{38}
\]
The product error is therefore at most
\[
CD(E_s+\gamma).
\tag{39}
\]

The output coefficient envelope converts this into a target-field error at most
\[
CKD(E_s+\gamma).
\tag{40}
\]

All partial products remain in a fixed bounded interval. All code fields consequently have a common polynomial \(H^1\) envelope depending on the canonical frequency and slot count. That bound is proved by the preceding error induction; it is not an assumption about independent inputs.

No step divides by a source value. Zero coordinates, repeated coordinates, and arbitrary correlations cause no special case.

## 6. Connect the computed values to the accepted final writer

After sparse arithmetic, the retained data have the form
\[
Z_N(x,h)=\sum_\ell Z_\ell(x)p_\ell(h),
\]
\[
U_N(x,h)-U_{0,N}(x)
=
\sum_\ell F_\ell(x)h_{j_\ell}q_\ell(h),
\tag{41}
\]
where every \(p_\ell,q_\ell\) is odd.

The accepted final writer applies to these stored payloads:

- Its decoder is linear in the unknown stored coefficients.
- Its constant-\(H\) propagation estimates use the bound on \(H\), not a relation between \(H\) and the payloads.
- Its internal resistivity signal works for an arbitrary copied register value.

For the last point, the same parallel-sector calculation gives
\[
\frac{b_n(s)-b_{2n}(s)}
{3\kappa^2n^2s}
=
\bar\rho_s r+O(Ps)r.
\tag{42}
\]
Thus \(\rho\)-weighted copies of the stored sources can be formed internally before the bank is consumed.

Prepare \(H+Z_N\) and the entire preconditioned collinear readout batch together. Perform the single readout and clearing window, apply the accepted flat-band velocity amplifier, and add the known \(U_{0,N}\).

The primitive operations are unchanged; their payload count and envelopes are now polynomial in \(q,S,D\). The final packet count is polynomial in \(S\).

Logical source and arithmetic errors are charged through (40). Fresh preparation and readout residuals are separately chosen below the amplifier’s polynomial gain budget. A final router can provide the required fresh physical input accuracy while retaining the actual computed coefficients.

## 7. Deterministic compiler and parameter order

A complete compilation algorithm is:

```text
1. Canonicalize and aggregate the complete sparse rational input.

2. Discard high probes by the KD/epsilon cutoff.
   Substitute zero for those variables.
   Truncate output spatial frequencies by the K/epsilon cutoff.

3. Form the O(SD) odd-product schedule.
   Choose a canonical bank with C(q + S + 1) slots.
   Reserve disjoint doubled-frequency and temporary banks.

4. Choose source, memory, arithmetic, and final-output error budgets.
   Construct the accepted final readout and amplifier for the
   retained output band and packet catalogue.

5. Compile initial capture with the finite-Fourier router:
   genuine initial smoothing, magnetic-preserving velocity reset,
   simultaneous packing, and physical rank restore.
   Cap its total duration below tau/4.

6. Compile sparse arithmetic and the final writer.
   Cap their total duration below tau/4.

7. Compute their exact rational durations.
   Let T_store be the remaining time.

8. Choose the polynomial number J of refresh cycles.
   Compile their active template under the cap T_store/(2J).
   Set the unforced hold d = T_store/J - h.

9. Concatenate:
   capture; J refresh cycles; arithmetic; final writer.

10. Choose one positive dyadic eta below all uniform disturbance
    thresholds, and emit the ordinary rational time polynomials.
```

The significant dependency directions are:

- Initial smoothing is chosen before capture’s microscopic carrier.
- The canonical code band is chosen independently of all microscopic carriers.
- Memory cycle count is chosen before local refresh accuracies.
- Refresh active duration is compiled before the exact hold duration is set.
- Each arithmetic assignment has fixed internal depth and returns to the canonical band.
- Disturbance tolerance is chosen after the physical gains are known.

There is no parameter condition requiring an old error \(a\) to satisfy
\[
a\,G_{\rm physical}(a^{-1})\ll a.
\]
The uniform router removes that circularity by targeting the actual incoming coefficients with a fresh absolute error.

## 8. Universal polynomial resources

All new services have fixed construction depth.

The router uses three packing transitions and one rank restore, regardless of the number of probes. Its masks have polynomially many listed Fourier entries and polynomial maximum frequency after truncation.

A ternary assignment consists of a fixed number of routers, a fixed-depth decoder, and one short packet interaction. The resource exponent does not depend on the monomial degree.

The variable repetitions are
\[
N_{\rm arith}\le CS(D+1),
\qquad
J\le \operatorname{poly}
\bigl(M,q,S,K,D,\mu^{-1},\epsilon^{-1},\tau^{-1}\bigr).
\tag{43}
\]
They multiply a common per-operation cost. They do not repeatedly exponentiate a state envelope.

In particular:

- Capture ends in the canonical band.
- Every refresh ends in that band with bounded source values.
- Every arithmetic assignment ends in that band with bounded partial products.
- The final write is one instance of the accepted polynomial backend.

### Explicit computation of \(A,p\)

Use the computable resource polynomials of the accepted services as fixed inputs to a finite precomputation. Add:

1. The integer Fourier-path bounds in (10).
2. The local smoothing and two-norm estimates through the fixed required spatial order.
3. The exact memory bound (23).
4. The fixed analytic packet bounds used in (33)–(36).
5. Rational arithmetic, rounding, convolution, and clock-accounting bounds.

Represent every bound by a polynomial with nonnegative rational coefficients, replacing logarithms and ceilings by elementary integer-polynomial majorants.

Substitute those polynomials through the fixed dependency graph above, and multiply by the loop counts in (43). Let \(Q(X)\) be the resulting univariate majorant, enlarged to include the finite precomputation itself. Define
\[
p=\max(1,\deg Q),
\qquad
A=1+\left\lceil\sum_m |[X^m]Q|\right\rceil,
\tag{44}
\]
after a fixed enlargement for the finitely many normalizations.

This is a terminating arithmetic prescription for universal constants. Neither depends on \(q,S,D\), the input frequencies, or the actual histories.

It gives
\[
\begin{aligned}
&\text{bit operations, memory bits, output bits, interval count,}\\
&\text{time-polynomial degrees and individual rational bit lengths}
\le A(L+R)^p,
\end{aligned}
\tag{45}
\]
and
\[
\eta^{-1}
+
\sup_{t\in[0,\tau]}\|f(t)\|_{W^{1,\infty}}
\le AR^p.
\tag{46}
\]
Since \(\tau\le1\),
\[
\int_0^\tau\|f(t)\|_{W^{1,\infty}}\,dt\le AR^p
\tag{47}
\]
after the same fixed enlargement.

Large input denominators affect binary arithmetic. Tiny coefficients are rounded or omitted against absolute error budgets; their reciprocals never enter a physical parameter. The numerical maximum of a discarded probe frequency never enters a physical bound.

## 9. Initial velocity, disturbances, all weak realizations, and the endpoint

The capture router begins from the actual joint \(H^1\) state. Its preliminary local interval and magnetic-preserving velocity reset handle the unknown \(u_0\). Its target remains the magnetic feature vector at the start of that invocation, with the initial drift paid by (16).

For the complete programme:

- Every reference may depend on the actual unknown state and coefficient history only inside the proof.
- Every emitted waveform depends solely on the supplied lists, bounds, tolerances, and rational clock.
- All active services use the actual non-autonomous dissipative equations.
- Storage holds use the exact coupled sector, with full-space perturbations paid separately.
- Packet stages use controlled strong references and polynomial two-norm perturbation bounds.
- The router includes all old errors in its actual input; none is discarded by a change of proof reference.

Local strong continuation covers the initial interval and every subsequent controlled segment. Weak–strong uniqueness identifies every corresponding Leray–Hopf energy-admissible realization with that strong realization. It is used with zero initial discrepancy; a uniqueness exponential is not used to choose \(\eta\).

All physical stages preserve the magnetic mean \(H\). The code operations are linear or odd cubic in magnetic data, and the final Lorentz readout is even. The construction therefore includes \(H=0\), \(B_0=0\), zero features, irrational fields, and correlated or duplicate probes.

Allocate the truncation, capture, storage, arithmetic, rounding, and final-write budgets so that
\[
\begin{aligned}
&\|u(\tau)-U(x,h(B_0))\|_2\\
&\qquad+
\|B(\tau)-H-Z(x,h(B_0))\|_2
<\epsilon.
\end{aligned}
\tag{48}
\]
This implies the requested joint Euclidean error bound. The final strong trace agrees with the specified one-sided energy trace.

**The additional input operation is therefore supplied by the simultaneous router, and the prescribed-time obstruction is resolved by two-frequency regeneration.** With those two constructions, the accepted backend extends from conserved-flux data to finitely many unobserved initial magnetic features, with sparse variable-input arithmetic and a universal polynomial resource bound.