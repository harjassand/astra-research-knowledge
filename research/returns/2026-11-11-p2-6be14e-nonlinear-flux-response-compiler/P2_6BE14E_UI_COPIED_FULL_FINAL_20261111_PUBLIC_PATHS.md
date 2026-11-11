# P2 completed return

Chat: https://chatgpt.com/c/6af2d0d2-f500-83ec-a7d0-20e80bd42677
User turn: b345d5fd-e29e-4282-9b68-04566e251efa; final: 6be14e57-4978-53ed-9829-08d896fc4e32; UI model: Pro.
Exact prompt source: work/astra-renewed-pro-programmes-20261103/P2_FULL_NONLINEAR_RESPONSE_AFTER_BACKGROUND_CLEARING_PRO_20261111.txt (SHA-256 f1292ce2f26dc13c42366e6065e662d9534db5d5114ae8f16c3ed5d7c3b41340; one terminal LF omitted at posting).
Capture: same-chat UI Copy; native first 20,000 characters match after whitespace and UI-citation normalization, and the visible ending is present. No database-byte identity asserted. The current activity and helper panels were not captured; the accessibility view presented older history. The outputs panel said no outputs yet; ZIP availability otherwise unknown.

## Complete UI-copied final

**Yes—relative to the full constructions accepted in the question, the compiler can be completed.** The useful change is to finish all magnetic arithmetic while velocity is still disposable, prepare **one batch** of readout packets, and write the unknown even velocity only once. A subsequent mechanical amplification word preserves the magnetic output.

Two estimates make this possible:

1. A dyadic combination of the earlier contracting Euler words has a uniform contraction rate on any prescribed finite Fourier band, while its norm on the entire space remains bounded independently of that band. Reversing this word gives a **polynomially bounded velocity amplifier** with a closed magnetic induction word.
2. If all final readout packets use one common carrier direction, their higher nonlinear output is \(O(Q^{-1}\operatorname{polylog}Q)\), rather than merely \(O(\sigma^3)\). The carrier \(Q\) can therefore be chosen *after* the amplifier gain, without an incompatible error requirement.

Below I give the construction and explain the physical register operations, error propagation, coefficient blindness, and resource certificate. The earlier accepted compilers are used as paid subroutines, with their fixed computable constants.

Write
\[
\kappa=2\pi,\qquad \mu=\min(\nu_-,\rho_-).
\]

## 1. The programme and its order of construction

After truncating the spatial input, write
\[
U_N(x,h)=U_{0,N}(x)+\sum_{j=1}^3h_jR_{j,N}(x,h).
\]
The three \(R_{j,N}\) and \(Z_N\) are odd polynomials, with the coefficient bound supplied by your arithmetic reduction.

The physical programme has the following stages.

| Stage | Physical endpoint or purpose |
|---|---|
| Common erasure and preparation | Reach a small \(H^1\) neighbourhood of \((0,H)\). |
| Magnetic register computation | Evaluate and store \(Z_N,R_{1,N},R_{2,N},R_{3,N}\). Velocity may be reset throughout. |
| Internal material signal | Generate copies of \(\rho(t_0)h_j\), within a prescribed error, without observing \(\rho\). |
| One final magnetic loading operation | Prepare \(H+Z_N\) together with all readout packets; return velocity close to zero. |
| One unforced readout and clearing window | Produce a small, preconditioned copy of \(U_N-U_{0,N}\), and clear all packet output. |
| Mechanical velocity amplification | Recover \(U_N-U_{0,N}\), preserving \(H+Z_N\). |
| Known joint-memory increment | Add \(U_{0,N}\), preserving both unknown fields. |

The important parameter order is:

1. choose the spatial cutoff and logical code space;
2. choose the final amplifier and its gain bound;
3. allocate logical arithmetic errors;
4. choose the final readout carrier;
5. choose physical loading, rounding, disturbance, and continuation tolerances.

There is no repeated loading after the unknown velocity has been written.

---

## 2. Input reduction has polynomial numerical cost

Aggregate duplicate entries exactly, and discard spatial frequencies with
\[
|k|_\infty>N,\qquad
N=\left\lceil \frac{64K}{\epsilon}\right\rceil.
\]
Since \(|h^\alpha|\le1\) for \(|h|\le1\), the coefficient hypothesis gives
\[
\sup_{|h|\le1}
\left(
\|U(h)-U_N(h)\|_2+
\|Z(h)-Z_N(h)\|_2
\right)
\le \frac{K}{7(N+1)}
<\frac{\epsilon}{64}.
\tag{1}
\]

This is a direct comparison of the binary input wavevectors with \(N\). It does not enumerate up to a discarded frequency.

For each nonzero even multi-index, distribute its coefficient according to
\[
(R_j)_{\alpha-e_j}
=\frac{\alpha_j}{|\alpha|}U_\alpha.
\tag{2}
\]
The total coefficient bound is retained. In particular, no unknown \(h_j\) is divided out.

There are polynomially many retained spatial entries and at most \((D+1)^3\) relevant monomial indices. The accepted eleven-register Horner programme therefore has
\[
N_{\mathrm{arith}}\le C(D+1)^3
\tag{3}
\]
whole-register assignments. Its ideal assignments are nonexpansive in the register sum norm.

The remaining issue is to implement those assignments physically with an absolute local error. That requires more than multiplying individual gate stability estimates.

---

## 3. Completing the physical magnetic register stage

### 3.1 The reset estimate needed for composition

The accepted magnetic-memory reset proof gives more structure than an endpoint estimate with an additive error. In its transformed coordinates, the large carriers have been removed, the conjugated diffusions have common coercive forms, and the only discrete velocity factor is
\[
\prod_{\mathrm{blocks}}(1+Cs^5).
\]

Linearize these actual transformed equations about a smooth reference in a supplied envelope. For a homogeneous variation, the same product inequalities and coercivity give
\[
\frac{d}{dt}E+cP^{-1}\mathcal D\le PE,
\tag{4}
\]
where \(P\) is a fixed polynomial of the reference, geometry, and reciprocal-diffusivity bounds. There is no additive residual in this variation equation.

Consequently, by choosing the reset duration and \(ns^5\) budget sufficiently small, the normalized magnetic endpoint block \(C\) satisfies
\[
\|C\|_{H^1\to H^1}\le1+\delta.
\tag{5}
\]
At one fixed higher spatial order,
\[
\|(C-I)v\|_{H^1}
\le P d^\alpha\|v\|_{H^m},
\tag{6}
\]
with fixed \(m,\alpha>0\).

The velocity-output derivative can also be made small. First apply the contracting velocity word in \(L^2\); then linearize the actual short \(H^1\) upgrade. Its bound has the form
\[
\|\dot u_{\rm out}\|_{H^1}
\le
\frac{C\|\dot u_{\rm raw}\|_2}{\sqrt{\mu\ell}}
+P\ell^{1/4}\|(\dot u_{\rm in},\dot B_{\rm in})\|_{H^1}.
\tag{7}
\]
Choose \(\ell\) first, then the contraction accuracy and compressed-word duration.

The second variation has a quadratic source. The \(H^1/H^2\) energy bounds give a positive power of duration:
\[
\|F(z+e)-F(z)-DF(z)e\|_{H^1}
\le P d^{\alpha_*}\|e\|_{H^1}^2
\tag{8}
\]
on a polynomial continuation ball.

These estimates are obtained from the transformed reset equations, rather than by differentiating an inequality containing an additive error. The relevant equations and same-coordinate energy estimate are in the [accepted reset construction, §3](https://github.com/harjassand/astra-research-knowledge/blob/31100cf85bfe60ae54bcc2b7be4d16f0f4cd5497/research/returns/2026-11-11-p2-814186-human-complete-five-gate-compiler/P2_814186_HUMAN_SUPPLIED_FULL_FINAL_20261111_PUBLIC_PATHS.md).

### 3.2 Actual magnetic transitions when velocity is disposable

For a fundamental shear \(F\), apply
\[
q(t)=\frac ah\,6(t/h)(1-t/h),\qquad f=q'F.
\]
Only in the proof define
\[
x'+\kappa^2\nu(t)x=q',\qquad
\alpha(t)=\int_0^t x(s)\,ds.
\]
Uniformly over the coefficient histories,
\[
|\alpha(h)-a|\le C|a|h,\qquad |x(h)|\le C|a|.
\tag{9}
\]

Pull the perturbations back by the joint Euler/induction coordinates
\[
\operatorname{diag}(E_{\alpha(t)},M_{\alpha(t)}).
\]
The large carrier cancels. The accepted Euler Gårding estimate and the explicit magnetic conjugated diffusion give polynomial common-form bounds. The remaining coupled terms have polynomial reference envelopes independent of compression.

After this pulse, reset the velocity tail while preserving magnetic memory in the same prefix metric. This realizes \(M_a\), to prescribed accuracy, with velocity returned close to zero.

The single-shear affine-viscosity identity is respected: the pulse itself is not asserted to have a common zero velocity endpoint. The following actual reset removes that tail.

Also, no false operator-norm continuity is used. Although \(M_{\alpha(h)-a}-I\) need not be small in \(H^1\) operator norm,
\[
\|M_{\alpha(h)-a}\|_{H^1\to H^1}
\le1+C|\alpha(h)-a|.
\tag{10}
\]

### 3.3 Physically realizing the directional filters

Use the four fundamental phases
\[
\sin,\quad\cos,\quad-\sin,\quad-\cos.
\]
For each phase, load \(M_a\), reset velocity, hold unforced briefly, unload \(M_{-a}\), and reset again.

Their full conjugated magnetic diffusions average exactly to
\[
\Delta+\frac{\kappa^2a^2}{2}\partial_{ii}.
\tag{11}
\]
Thus the comparison filter is
\[
S_i=\exp[D_i(\Delta+\chi_i\partial_{ii})],
\qquad \chi_i=\frac{\kappa^2a^2}{2},
\tag{12}
\]
where the unknown \(D_i\) has known positive upper and lower bounds.

Three separate estimates pay the actual implementation.

**Coupled holds.** The whole-macro Duhamel estimate bounds Lorentz-generated velocity and its feedback into induction by
\[
CP^2\sqrt{T\ell}\sup_{t\le T}\|b(t)\|_{H^1}
+CP\sqrt T\,r_*,
\tag{13}
\]
where \(\ell\) is the largest hold length and \(r_*\) is the reset velocity tolerance. This is a whole-macro estimate, with no cell-count multiplier.

**Carrier and reset jumps.** Group the transitions between adjacent holds into a normalized jump \(C_j\). From (5)–(6),
\[
\|C_j\|\le1+\delta_j,\qquad
\|(C_j-I)v\|_{H^1}\le\varepsilon_j\|v\|_{H^m}.
\]
The elementary adjoint estimate
\[
\|(C_j^*-I)v\|_{H^1}^2
\le
C\delta_j\|v\|_{H^1}^2
+2\varepsilon_j\|v\|_{H^1}\|v\|_{H^m}
\tag{14}
\]
allows an immediately following heat hold to smooth the jump error. The terminal jump uses the preceding heat hold. The resulting bound is
\[
N_{\mathrm{cell}}P\ell^{-m/2}
\sqrt{\max_j(\delta_j+\varepsilon_j)}.
\tag{15}
\]
Every quantity here is polynomially payable.

**Coefficient histories.** Freeze coefficients only in the proof on cells of length at most \(\ell\). The form error is bounded by a polynomial times \(\Lambda\ell\). The accepted common-form averaging estimate applies without coefficient samples or an \(H\)-maximal-regularity assertion.

If a whole filter is too long for one Gårding exponent, divide it into polynomially many macros. Compare each macro with its enhanced heat operator and telescope against those commuting contractions. Raw Gårding factors are not multiplied over the complete filter.

These arguments include constant fields. Thus they pay the unknown-mean contribution as well as mean-zero errors.

For definiteness, a conservative schedule can use a rational master envelope \(\mathcal H\ge2\), polynomial in all requested bounds and reciprocal errors, with
\[
N_{\rm macro}=\lceil100\mathcal H T\rceil,\qquad
N_{\rm cycle}=\lceil\mathcal H^{64}\rceil,
\]
local jump errors at most \(\mathcal H^{-8192}\), and transition/reset durations at most
\[
\mathcal H^{-b},\qquad
b=\left\lceil 2^{20}/\min(\alpha_{\rm reset},1/4)\right\rceil.
\tag{16}
\]
Increasing the fixed prefactor handles the finitely many estimates. The exponent is independent of the code count and \(D\).

### 3.4 Actual finite-rank restoration

Now implement
\[
\mathcal R_D=S_yT_1(\Phi)S_xS_z.
\]
It is helpful to separate code attenuation from leakage. Define
\[
\widehat{\mathcal R}_D
=e^{D_y\Delta}P_yT_1(\Phi)
 e^{D_x\Delta}P_xe^{D_z\Delta}P_z.
\tag{17}
\]
On a routed code coefficient, this inserts factors
\[
e^{-\kappa^2n_{\rm in}^2(D_x+D_z)}
e^{-\kappa^2n_{\rm out}^2D_y}.
\tag{18}
\]
Their modulus is at most one. A routing matrix nonexpansive in the register sum norm remains nonexpansive after these factors.

Their difference from one contributes the logical error
\[
CF^2(D_x+D_y+D_z)K.
\tag{19}
\]
The unwanted-mode leakage satisfies
\[
\|\mathcal R_D-\widehat{\mathcal R}_D\|_{H^1\to H^1}
\le
P(D_{\min}^{-1},\Phi,F)
e^{-c\min_i\chi_iD_i}.
\tag{20}
\]

Choose the isotropic times from the logical error budget first. Then choose the enhanced diffusion sufficiently large for the physical leakage budget. All choices use known bounds on \(D_i\), never their actual values.

This is an actual mechanical restore. The averages in (17) are comparison operators, not additional actuators.

### 3.5 A fixed-depth decoder for unknown coefficients

The restore can route and copy unknown code coefficients. The following fixed-depth construction decodes them into any prescribed finite solenoidal field linear in those coefficients.

For known basis fields \(F_\ell\), compute rational normalized curl potentials
\[
F_\ell=\kappa^{-1}\operatorname{curl}A_\ell.
\]
Prepare three code banks
\[
B_i=\sum_\ell r_\ell w_\ell(y_i),\qquad y_i\ne i.
\]
Apply
\[
T_i(\phi_i),\qquad
\phi_i=2\sum_\ell A_{i\ell}(x)w_\ell(y_i).
\tag{21}
\]

Diagonal code products produce the required field
\[
\sum_\ell r_\ell F_\ell.
\]
Cross products and terms involving the mean or previously written low fields stay at the code scale. Choose three separated code scales and filter after each gate.

The three banks themselves can be prepared from one bank with two additional scalar gates and filters: route copies to two \(B_2(z)\) groups, move the higher group to two \(B_3(x)\) groups, then move one of those to \(B_1(y)\). A fixed hierarchy
\[
S_1\gg G_1\gg F_1\gg S_2\gg G_2\gg N_{\rm output}
\tag{22}
\]
suffices.

There are only five decoding/preparation gates after the initial router. Their depth does not grow with the catalogue. In particular, this operation can prepare a complete packet list from unknown registers while consuming its temporary banks.

### 3.6 Multiplication and the actual-state rebase

For
\[
(d,s)\longmapsto(h_i^2d+s,0),
\tag{23}
\]
route the selected register and flux signals into the accepted cubic packet configuration, run its short physical window, apply the general positive-heat service, and restore the desired cubic code into the destination.

Idle registers cause no new leading slow term. In the strong cubic scaling
\[
Q=q^4,\qquad A=q^6,\qquad T=q^{-11},
\]
the pure cubic slow term has scale
\[
A^3QT^2=1.
\]
Replacing a packet leaf by a bounded background leaf gains \(A^{-1}=q^{-6}\). The mixed slow contribution is therefore below the accepted \(q^{-2}\) error after increasing \(q\) polynomially. High output is physically removed by the heat service. Velocity may be reset.

Before **every** logical assignment, perform the accepted genuine smoothing from the actual incoming \(H^1\) state. Its zero-disturbance reference starts from that state and includes all historical errors. Choose this smoothing time from the logical tolerance, obtaining one uniform polynomial smooth envelope. Then perform an actual identity restore.

Only after that physical restore use the actual extracted code coefficients as the next proof reference. The force does not evaluate them.

Thus a completed assignment satisfies
\[
E_{\rm code}^{\,\mathrm{new}}
\le E_{\rm code}^{\,\mathrm{old}}+\delta_{\rm log},
\tag{24}
\]
with a separately paid physical off-code remainder. Historical code errors pass through the nonexpansive logical map; historical rough errors are carried into a genuine smooth reference and physically cleared.

Taking
\[
\delta_{\rm log}\le
\frac{\delta_{\rm arithmetic}}{C(N_{\mathrm{arith}}+1)}
\tag{25}
\]
completes the variable-degree register machine with a fixed resource exponent.

---

## 4. A polynomial velocity amplifier preserving magnetic memory

A single dilation of the old contracting symbol would be insufficient: its low-frequency gap vanishes. A dyadic combination supplies the needed uniform band coverage.

### 4.1 The bounded dyadic symbol

The fixed rational rotation construction underlying the accepted eraser gives a real transverse symbol \(\bar d\) with
\[
\operatorname{Sym}\bar d(\xi)
\le-c_d\min(|\xi|^2,|\xi|^{-2})P_\xi,
\]
\[
\|\bar d(\xi)\|
\le C_d\min(|\xi|^2,|\xi|^{-2}),
\qquad \xi\ne0,
\tag{26}
\]
for fixed computable constants. The second bound follows from its full-matrix low/high expansions and a finite bound on the fixed middle annulus. These are the continuum symbol estimates in the [fixed shear-word construction, §§1–4](https://github.com/harjassand/astra-research-knowledge/blob/31100cf85bfe60ae54bcc2b7be4d16f0f4cd5497/research/returns/2026-11-10-p2-rotated-shear-global-compiler-de0d6f/P2_PRO_DE0D6F_RETURN_20261110_PUBLIC_PATHS.md).

Let \(N_0\) be its fixed frequency denominator clearer and set
\[
J=\lceil\log_2N\rceil,\qquad
\mathcal D_N(k)=c_*\sum_{j=0}^J
\bar d\!\left(\frac{k}{2^jN_0}\right).
\tag{27}
\]
The geometric tails give
\[
\sup_{k\ne0}\sum_{j=0}^J
\left\|c_*\bar d\!\left(\frac{k}{2^jN_0}\right)\right\|
\le C_0,
\tag{28}
\]
independently of \(N\). On the requested band,
\[
\operatorname{Sym}\mathcal D_N(k)\le-c_0I,
\qquad 1\le|k|\le N,
\tag{29}
\]
where \(c_0>0\) is fixed. Frequencies below \(N_0\) merely reduce this fixed constant.

Choose an integer auxiliary time \(T_a=O(\log g)\), and put
\[
C_N=e^{T_a\mathcal D_N},\qquad
A_N=e^{-T_a\mathcal D_N}.
\]
Then
\[
\|C_N\Pi_N\|_{H^m\to H^m}\le g^{-1},
\qquad
\|A_N\|_{H^m\to H^m}\le Cg^\beta,
\tag{30}
\]
for a fixed computable \(\beta\), on the entire mean-zero space.

The final readout target will be
\[
W=C_N(U_N-U_{0,N}).
\tag{31}
\]
It has a correspondingly small coefficient bound.

### 4.2 Actual words and coefficient-independent forcing

Use the inverse physical superwords at the dyadic spatial scales. Their induction maps close exactly. The matrices at different scales need not commute: (28) bounds the product-formula error pointwise by \(Cs^8\), uniformly in the number of scales.

For each required fixed Sobolev order, a bound
\[
B_N\le C(1+N)^b
\tag{32}
\]
pays the spatially dilated Taylor and affine remainders. Choose a rational \(s\) and integer \(n\) with \(ns^4\) approximating \(T_a\), such that
\[
nB_Ns^5g^\beta\le\delta_a.
\tag{33}
\]
All prefix norms are bounded by a fixed power of \(g\).

For frozen viscosity, reversing a physical affine word
\[
z\longmapsto W_sz+b_s
\]
gives
\[
z\longmapsto W_s^{-1}z-W_s^{-1}b_s.
\]
The translated superword’s \(O(s^5)\) affine cancellation is therefore retained. For varying viscosity, the accumulated discrepancy is bounded by
\[
C\Lambda d_a B_Nns\,g^\beta,
\tag{34}
\]
where \(d_a\) is the physical amplification duration. Choose \(d_a\) inverse-polynomially small to pay this and the smooth nonlinear, Lorentz, and diffusive residuals.

### 4.3 Implementing the generated shears with twelve actuators

The known velocity translation construction extends to preserving **both** unknown smooth fields. Initialize its reference by
\[
v(0)=u_{\rm old},\qquad
v_t+L_{qF}v=\nu(t)\Delta(qF)+gG.
\tag{35}
\]
Then
\[
v=E_\alpha u_{\rm old}
+\text{viscosity corrector}
+\text{known source response}.
\]
The carrier terms cancel exactly as before. On a complete closed translation word,
\[
E_{\rm end}=M_{\rm end}=I.
\]
All remaining coupled residuals have polynomial envelopes independent of compression. The fixed-depth plane-mode and quadratic synthesis therefore supplies arbitrary **known** Fourier increments preserving both fields.

To implement an amplifier shear letter, add a known large carrier \(\pm\lambda F\), hold unforced for its prescribed impulse divided by \(\lambda\), and remove it by a known increment. Choose \(\lambda\) first; then choose the increment-call durations and tolerances.

The affine viscous contribution during the holds is included in (34), not discarded. All emitted forces are in the twelve original directions.

The result is an actual service
\[
(u,B)\longmapsto(A_Nu,B)+\text{error},
\tag{36}
\]
with whole-space polynomial error gain, ordinary rational time coefficients, and a polynomial reciprocal disturbance budget.

---

## 5. One collinear packet batch writes the complete even velocity

The original \(O(\sigma^3)\) remainder would not suffice after an amplifier with a potentially large fixed exponent \(\beta\). The following estimate resolves that problem.

### 5.1 A common carrier direction suppresses the first interaction

Take
\[
k_s=Qn_s\ell+\omega_s,\qquad
0<|n_s|\le J_p,\quad |\omega_s|\le F_p.
\]
For a solenoidal polarization \(a_s\),
\[
\ell\cdot a_s=-\frac{\omega_s\cdot a_s}{Qn_s}.
\]
Hence
\[
a_s\cdot k_t
=a_s\cdot\left(\omega_t-\frac{n_t}{n_s}\omega_s\right),
\]
and therefore
\[
|a_s\cdot k_t|\le F_p(1+J_p)|a_s|.
\tag{37}
\]
There is no \(Q\) factor.

The exact non-autonomous constant-\(H\) propagator preserves each spatial polarization: at a fixed frequency it mixes only the two scalar velocity/magnetic amplitudes. Thus (37) remains valid for the freely propagated initial packet.

Let
\[
v=S_Hp_Q,\qquad z_2=\mathfrak B(v,v),
\]
with packet critical budget \(\sigma\le c\mu\). The improved forcing bound gives
\[
\sup_{t\le T}\|z_2(t)\|_{X^0}
\le P_{\rm geom}\frac{\sigma^2}{\mu}.
\]
Consequently,
\[
\gamma(z_2)
\le P_{\rm geom}\sigma^2\sqrt{T/\mu}.
\tag{38}
\]

For the paid clearing time
\[
T\asymp\frac{\operatorname{polylog}(Q)}{\mu Q^2},
\]
this is \(Q^{-1}\) times a polynomial in the earlier envelopes and logarithms.

### 5.2 The whole higher remainder gains \(Q^{-1}\)

Writing \(w=z-v\),
\[
w=z_2+\mathfrak B(v,w)+\mathfrak B(w,v)+\mathfrak B(w,w).
\]
The \(\gamma\)-contraction estimate gives
\[
\gamma(w)\le2\gamma(z_2).
\]
Thus
\[
\|z-v-z_2\|_{E_T}
\le
\frac{P_{\rm geom}\sigma^3
       \sqrt{\operatorname{polylog}(Q)}}{\mu^2Q}.
\tag{39}
\]

To obtain the complete slow \(H^1\) bound, retain carrier labels in the homogeneous expansion. A degree-\(n\) zero-carrier term has frequency at most \(nF_p\). Its conversion from \(X^{-1}\) to \(H^1\) costs \(C(1+nF_p)^2\).

Apply the same contraction with a complex packet-amplitude parameter of modulus at most two. Cauchy estimates give a geometric degree majorant, so the \(n^2\) factors sum. The zero-carrier higher output still has the bound (39), with another fixed polynomial factor.

All nonzero-carrier output is paid by the supplied physical high-output clearing estimate. For degrees \(n\le n_*\), its frequency is at least \(Q/2\); the logarithmic \(n_*\) pays the entire remaining tail.

Therefore the complete unwanted physical output obeys
\[
\boxed{
\|E_{\rm packet}\|_{H^1}
\le
C\zeta+
\frac{P\,\operatorname{polylog}(Q)}{Q}.
}
\tag{40}
\]
The supplied mixed-background terms also decay with \(Q\). They include the complete Lorentz and induction interactions.

This permits \(Q\) to be chosen last so that (40) is below \(\epsilon/(Cg^\beta)\), for any fixed \(\beta\).

### 5.3 Every desired polarization is available in one direction

For \(|m|_\infty\le N\), let
\[
L_0=2N+1,\qquad \ell=(1,L_0,L_0^2).
\]
For every nonzero retained integer \(m\),
\[
m\cdot\ell\ne0,\qquad m\times\ell\ne0.
\]
These follow from the positional-size inequalities.

Set
\[
q_m=P_{\ell^\perp}m,\qquad a=\frac{q_m}{|q_m|^2}.
\]
Then \(a\cdot m=1\) and \(a\perp\ell\).

For a tag \(n\), put
\[
k=Qn\ell,\qquad l=m-k.
\]
Given rational \(d\perp m\), define
\[
\Delta_{m,n}=2Qn(m\cdot\ell)-|m|^2,
\]
\[
\beta_{m,n}
=-\frac{Qn|m|^2(d\cdot\ell)}{\Delta_{m,n}},
\qquad
b=d-\beta_{m,n}a+\frac{2\beta_{m,n}m}{|m|^2}.
\tag{41}
\]
Direct substitution gives
\[
a\perp k,\qquad b\perp l,\qquad
P_m[(a\cdot m)b+(b\cdot m)a]=d.
\tag{42}
\]
For \(Q\ge6N^2\),
\[
|a|\le CN^2,\qquad |b|\le CN^6|d|.
\]
All inverses in (41) concern known integers with polynomial lower bounds.

Use \(d=P_me_j\) to represent arbitrary vector coefficients. Assign a distinct positive tag to each programmed pair. The only quadratic zero-carrier interactions are its intended pair, its real conjugate, and zero-mode self-pairs, which vanish by mean conservation. Higher accidental tag relations are already covered by (40).

### 5.4 Cancelling the unknown resistivity internally

For a magnetic pair, the leading velocity multiplier is
\[
\frac{iQ^2\sigma^2}
{\kappa\rho(t_0)(|k|^2+|l|^2)}
\tag{43}
\]
times the programmed product and polarization.

Generate an internal copy of \(\rho(t_0)h_j\) shortly before loading. This can be done in the exact parallel sector
\[
u=e_2v(z),\qquad B=H+e_2b(z).
\]
Two coded copies at known distinct frequencies give
\[
\frac{b_n(t)-b_N(t)}
{\kappa^2(N^2-n^2)t}
=\bar\rho_t\,r+O(Pt)|r|,
\tag{44}
\]
with the complete coupled propagator included. The coefficient is never observed.

Put this signal in the first packet and the appropriate preconditioned odd \(R_j\) coefficient in the second. Known rational approximations to
\[
\frac{\kappa(|k|^2+|l|^2)}{Q^2\sigma^2}
\]
and a sine/cosine phase cancel (43).

The normalization error is bounded by polynomial multiples of
\[
\frac{|\bar\rho_t-\rho(t_0)|}{\rho_-}
+\frac{\Lambda T}{\rho_-}
+N^2T
+\frac{M}{\mu Q}
+(MN+N^2)T
+e^{-c\mu Q^2T}.
\tag{45}
\]
Produce the internal signal after the variable-degree arithmetic, and compress the subsequent preparation into a prescribed short interval. Lipschitz continuity then pays the elapsed-time discrepancy.

### 5.5 Fitting the whole target within the weak-packet budget

Let \(P_{\rm tag}\) be the computable polynomial envelope for all tags, polarizations, and coefficient normalizations. Normalize duplicated first-packet signals, compensating in the second factors.

It suffices that
\[
\|W\|_{\rm coefficient}
\le\frac{\sigma^2}{4P_{\rm tag}}.
\tag{46}
\]
Choose \(g\) polynomially large to ensure this through (30)–(31). The register decoder then prepares the *entire* packet list together with \(H+Z_N\), with velocity close to zero.

The packet reference uses the actual computed register values. Their logical errors affect the leading readout through a known polynomial map independent of \(Q\). They are not treated as an \(O(Q^2)\) incoming-field error. Only fresh physical preparation errors are assigned the smaller, carrier-dependent tolerance after \(Q\) is fixed.

The single unforced window consequently ends at
\[
u=W+\text{small error},\qquad
B=H+Z_N+\text{small error},
\tag{47}
\]
with the complete physical high output included in the error.

Apply the amplifier (36), then add the known \(U_{0,N}\).

---

## 6. The deterministic compiler

Here is the resulting algorithm.

```text
1. Canonicalize the complete rational input lists.
   Truncate spatial frequencies at N = ceil(64 K / epsilon).

2. Form U0, Z, R1, R2, R3 and the eleven-register Horner schedule.

3. Construct the dyadic Fourier multiplier D_N.
   Choose the weak-packet budget sigma, preconditioning gain g,
   amplifier word, and its whole-space gain certificate G_amp.

4. Allocate logical arithmetic and target-coefficient errors
   below epsilon / poly(G_amp, tag bounds, assignment count).

5. Compile the magnetic arithmetic:
   actual smoothing, physical restore, fixed-depth assignment,
   positive heat, and physical restore for each assignment.

6. Construct the single collinear packet catalogue.
   Choose Q by explicit polynomial inequalities paying
   the complete clearing, background, and amplifier error budgets.

7. Compile the final internal rho signals and the fixed-depth
   whole-packet loader, within the required short time window.

8. Compile the unforced readout window, the amplifier,
   and the final known U0 joint-memory increment.

9. Compute the exact rational duration of these stages.
   Prepend the common eraser and H1 preparation to end exactly at tau.

10. Choose eta as a dyadic rational below every certified
    disturbance budget. Emit all twelve rational time coefficients.
```

Every choice uses integer arithmetic, rational arithmetic, ceilings, dyadic searches with explicit bounds, and rational enclosures of fixed constants. Matrix exponentials needed for preconditioning are only \(3\times3\) matrices at finitely many known Fourier frequencies; scaling and Taylor remainder bounds compute them to the required accuracy.

No step evaluates a PDE solution, register value, flux component, diffusivity, or norm supplied by an oracle.

---

## 7. Universal polynomial resources

Here is a precise way to obtain universal constants rather than merely assert their existence.

In fixed precomputation:

1. generate the constants and resource exponents of the accepted subroutines;
2. generate the fixed shear-word table and the constants in (26);
3. compute \(c_0,C_0,\beta\) in (28)–(30);
4. generate the finite-order product, form, smoothing, and Fourier-envelope bounds used above;
5. propagate numerical exponents through the fixed list of construction templates.

For exponent propagation, addition takes a maximum plus a fixed allowance, multiplication adds exponents, and a fixed power multiplies them. The only exponential in a variable parameter is
\[
e^{C_0T_a}\le Cg^\beta,
\]
which is explicitly replaced by this fixed power. The logarithmic clearing factors are bounded using integer bit lengths.

Variable loops contribute their iteration counts to the resource bound. They do not recurse the state-envelope exponent:

- every arithmetic assignment returns to the same code band and logical ball;
- every restore uses the same smoothing envelope;
- the decoder has fixed depth;
- there is one final weak readout;
- there is one amplifier with whole-space gain \(g^\beta\).

Let \(p_0\) dominate the finitely many accepted service exponents and let \(b_0\) dominate the fixed-order envelope degrees just generated. A deliberately excessive bound can be selected in the form
\[
p=
2^{40}(1+p_0+b_0+\beta)^{\,2^{20}},
\tag{48}
\]
with the constant \(A\) obtained by the same finite coefficient propagation and enlarged to include the entire fixed precomputation. Equivalently, the precomputation can output the smaller exponent obtained directly from its bound expressions.

All these quantities are independent of \(D\), the target catalogue, the coefficient rectangle, and the actual histories.

The resulting bounds are
\[
\begin{aligned}
&\text{bit operations, memory, output bits, intervals, degrees,
rational bit lengths}
\le A(L+R)^p,\\
&\eta^{-1}
+\sup_t\|f(t)\|_{W^{1,\infty}}
+\int_0^\tau\|f(t)\|_{W^{1,\infty}}\,dt
\le AR^p,
\end{aligned}
\tag{49}
\]
after increasing \(A\).

Tiny input coefficients are handled by absolute-error rounding or omission. No inverse target coefficient is used. Complete input denominators affect binary work and precision; they do not introduce uncharged numerical amplitudes.

Every shortening of time is paid through the corresponding ordinary carrier height, derivative force, interval count, and rational precision.

---

## 8. Unknown initial data, disturbances, and every energy weak realization

Give all writing stages a total duration below \(\tau/2\). Their exact rational duration is known after compilation. Use the remaining initial time for the accepted common eraser and a prescribed unforced preparation interval.

The eraser gives a small joint \(L^2\) error relative to \((0,H)\). The fluctuation energy inequality supplies a regular time with small \(H^1\) norm during the preparation interval. The constant-\(H\) terms cancel in joint energy. A small-data \(H^1\) continuation estimate then yields the required handoff at the **prescribed** writing start time. The regular time is used only in the proof.

On every subsequent segment:

- the strong estimate uses the actual admitted disturbance;
- the continuation ball has inverse-polynomial radius;
- the physical reference may depend on the unknown state and coefficient history;
- the emitted force depends only on the supplied inputs and certified envelopes.

Weak–strong uniqueness then identifies every energy-admissible realization with the controlled strong realization over the writing stages. It is used with zero initial discrepancy, after the robust estimate; an uncontrolled uniqueness exponential does not determine \(\eta\).

Allocate the arithmetic, loading, readout, amplification, and final-increment errors so that
\[
\|u(\tau)-U_N(H/M)\|_{H^1}
+\|B(\tau)-H-Z_N(H/M)\|_{H^1}
\le \epsilon/2.
\tag{50}
\]
Combining this with (1) gives the required joint \(L^2\) error strictly below \(\epsilon\).

The final strong trace agrees with the specified one-sided energy trace. Magnetic mean conservation holds throughout, and every inverse used in the construction concerns a known geometric integer or a supplied positive bound.

**The unresolved repeated-loader problem is therefore avoidable.** Actual magnetic register computation supplies the unknown odd quantities first; one collinear batch writes the complete even response; and the bounded mechanical amplifier restores its size while retaining the already written magnetic field.