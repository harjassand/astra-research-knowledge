**Yes—relative to the accepted initial-data compiler and its underlying quantitative constructions, the continuously forced problem can also be completed.** The necessary addition is a forcing-aware theorem for the active operations. The small-disturbance guarantee of the earlier compiler is not sufficient by itself.

The decisive estimate concerns the directional filters inside the router. Their live-input error need not become small in \(H^1\) when the filter is shortened. What can be obtained is:

\[
\boxed{
\text{small live-input error in }L^2
\quad+\quad
\text{an }H^1\text{ bound independent of the short filter time}.
}
\]

A separately chosen, genuinely unforced smoothing interval then makes the endpoint error small in \(H^1\). The input remains present during that interval.

Once this interface is established, the fluid can accumulate the actual input integrals on short holds, refresh its existing registers, and perform the sparse polynomial calculation near the endpoint. Contributions arriving during active operations are bounded against the **original full-interval features**, while their physical contamination is paid by the new estimates.

Below is the construction and its parameter ordering.

---

## 1. Input bounds and the intended code

Write
\[
\kappa=2\pi,\qquad
\mu=\min(\nu_-,\rho_-).
\]

For the live input, let
\[
\mathcal G_m
=
\operatorname*{ess\,sup}_{t\in[0,\tau]}
\|G_\theta(t)\|_{H^m}.
\]
Orthogonality of the ports gives
\[
\mathcal G_0\le\sqrt{2q_1},
\qquad
\mathcal G_m\le C_m\sqrt{q_1}(1+N)^m.
\tag{1}
\]
In the compiler, use rational polynomial majorants of these quantities. Only finitely many fixed spatial orders will be required.

The exact port coefficient is
\[
c_j(B)=\frac{\langle B,g_j\rangle}{\|g_j\|_2^2}.
\tag{2}
\]
Here
\[
\|g_j\|_2^2=\frac{|p_j|^2}{2}\in[1/2,2].
\]
Thus \(c_j\) is an explicitly known rational combination of at most three coordinate Fourier integrals. No Gram inversion or unknown normalization is needed.

As before, discard initial probes above a cutoff
\[
N_{\rm initial}
=
\left\lceil \frac{C KD}{\epsilon}\right\rceil,
\tag{3}
\]
and truncate output spatial frequencies above
\[
N_{\rm output}
=
\left\lceil \frac{C K}{\epsilon}\right\rceil.
\tag{4}
\]
The corresponding target errors are bounded by \(CKD/N_{\rm initial}\) and \(CK/N_{\rm output}\). The compiler compares the listed binary integers with these cutoffs.

Reserve
\[
C_{\rm slots}=C(q_0+q_1+q_2+S+1)
\]
canonical slots. Choose distinct base frequencies
\[
n_a\in[F_0,2F_0),
\qquad F_0>N+C_{\rm slots}+1.
\tag{5}
\]
The doubled frequencies \(2n_a\) occupy a disjoint bank. Every code frequency is outside the complete input band.

A canonical magnetic state has the form
\[
B=H+e_3\sum_a r_a\sin(\kappa n_a x_2),
\qquad u\approx0.
\tag{6}
\]
The intended initial-source values and temporal partial integrals have modulus at most one. A fixed enlarged code ball, such as \(|r_a|\le3\), will be justified by the error induction.

---

## 2. Live input through active words with fixed geometry

The actual carrier-coordinate construction used by the accepted mechanical lift writes the magnetic field as
\[
B=N(t)(\beta+z),
\]
where \(N(t)\) is the induction prefix of the intended word together with the faster lowering prefixes.

With live input, the transformed induction equation acquires exactly the additional term
\[
\boxed{N(t)^{-1}G_\theta(t).}
\tag{7}
\]

There is no time derivative of \(\theta\), no derivative of the carrier coefficient multiplying \(G_\theta\), and no separate magnetic actuator.

Fix the dimensionless impulses, spatial catalogue, target amplitudes, and word accuracy first. The prefix and inverse-prefix bounds then have the form
\[
\sup_t\|N(t)^{\pm1}\|_{H^{m_*}\to H^{m_*}}
\le P_{\rm geom},
\tag{8}
\]
independently of the final physical compression parameter.

The existing transformed joint energy estimate has polynomial coercivity and lower-order constants independent of that compression speed. Adding (7) contributes a source term bounded by the known spatial norm \(P_{\rm geom}\mathcal G_{m_*}\). Consequently, on the paid continuation ball, the additional endpoint error is bounded by
\[
\boxed{
P_{\rm geom}\mathcal G_{m_*}\,d^\alpha,
}
\tag{9}
\]
where \(d\) is the subsequently chosen word duration and \(\alpha>0\) is fixed. A conservative choice is \(\alpha=1/2\).

This is an estimate from the transformed equations. It does not substitute \(\mathcal G_0\) for the old small \(\eta\).

The large carrier terms are cancelled by the same coordinate change as in the input-free construction. At each lowering level, the faster phase is chosen after the inner carrier amplitude is fixed. The new source integrals sum over actual time; they do not acquire a factor equal to the number of lowering cells. The relevant carrier-coordinate and reset equations are those in the [accepted whole-field construction](https://github.com/harjassand/astra-research-knowledge/blob/31100cf85bfe60ae54bcc2b7be4d16f0f4cd5497/research/returns/2026-11-11-p2-814186-human-complete-five-gate-compiler/P2_814186_HUMAN_SUPPLIED_FULL_FINAL_20261111_PUBLIC_PATHS.md).

### Reset tails have a separate parameter

An \(H^1\) velocity reset includes a genuine smoothing tail. Its order of construction is:

1. Choose the tail duration from its error allowance, the live-input norm, and the available clock.
2. Choose the required raw velocity \(L^2\) accuracy.
3. Fix the raw erasing word’s geometry.
4. Compress that raw word to pay (9).

This prevents the eraser geometry from depending on the same duration whose smallness is supposed to suppress its input response.

Known translations and the final velocity amplifier admit the same ordering once their geometric parameters are fixed.

---

## 3. The new directional-filter estimate

This is the main additional argument.

For a fundamental shear induction map \(M_a\),
\[
\|M_a^{\pm1}\|_{L^2\to L^2}\le C(1+a),
\qquad
\|M_a^{\pm1}\|_{H^1\to H^1}\le C(1+a)^2.
\tag{10}
\]

A directional filter needs an enhancement budget
\[
a^2D_{\rm hold}\asymp B_{\rm mix},
\tag{11}
\]
where \(D_{\rm hold}\) is its total principal holding time and \(B_{\rm mix}\) includes the required lower-resistivity factor.

Therefore
\[
D_{\rm hold}(1+a)^2\mathcal G_1
\]
need not tend to zero. A direct \(H^1\) shortening argument fails here.

### 3.1 A uniform source-insertion bound on two spaces

For the four signed sine/cosine shear phases, put
\[
A_j=M_j^{-1}\Delta M_j.
\]
Their exact average is
\[
\overline A=\Delta+\chi\partial_{ii},
\qquad \chi\asymp a^2.
\tag{12}
\]

At Sobolev orders \(s=0,1\), these operators have common form domain \(H^{s+1}\), polynomial reciprocal coercivity, and polynomial spatial-commutator bounds.

Divide the filter into macros of length
\[
\vartheta\le P(a,\mu^{-1})^{-1}.
\tag{13}
\]
The common Gårding estimate bounds every partial macro propagator by an absolute constant.

There is a quantitative averaging estimate on **both** \(L^2\) and \(H^1\). If \(h\) is the complete four-phase cycle length, then
\[
\boxed{
\|U_{\rm macro}-S_{\rm macro}\|_{H^s\to H^s}
\le
P(a,\mu^{-1})
\left[\sqrt{h/\vartheta}+\Lambda h\right],
\qquad s=0,1.
}
\tag{14}
\]
Here \(S_{\rm macro}\) is the corresponding enhanced-heat contraction.

For completeness, the rate follows from a spatial smoothing and primitive argument:

- Freeze \(\rho\) only in the proof on each complete cycle.
- The primitive of
  \[
  \rho_{\rm frozen}(A_{\rm phase}-\overline A)
  \]
  is an order-two operator of size \(P(a)h\), vanishing at cycle boundaries.
- In Duhamel’s formula, the boundary layers of length \(h\) are estimated by splitting one derivative onto each propagator. Their contribution is
  \[
  P(a)\sqrt{h/\vartheta}.
  \]
- On the interior, integrate the primitive by parts. The resulting order-four products are bounded by splitting two derivatives onto each propagator:
  \[
  P(a)h\int_h^{\vartheta-h}
  \frac{dt}{t(\vartheta-t)}
  \le
  P(a)\frac h\vartheta\log(\vartheta/h).
  \]
  This is absorbed into the square-root bound.
- The coefficient-freezing residual contributes \(P(a)\Lambda h\).

The required smoothing estimates come from weighted spatial derivative energies and their adjoint versions. No time differentiation of the switching operators or of \(G_\theta\) is used.

Choose the complete-macro operator errors so that their sum is at most one. A source inserted at any time passes through a bounded remainder of its current macro and then through complete macros satisfying
\[
\prod_j(1+\varepsilon_j)\le e.
\]
Thus
\[
\boxed{
\sup_{0\le s\le D_{\rm hold}}
\|U(D_{\rm hold},s)\|_{H^j\to H^j}
\le C,\qquad j=0,1,
}
\tag{15}
\]
with \(C\) independent of \(a\), the number of macros, and the insertion time.

This is the estimate that an input-free endpoint theorem alone would not supply.

### 3.2 Bound the live forcing without averaging its history

In normalized coordinates, the source on each hold is
\[
M_{\rm phase}^{-1}G_\theta.
\]
Equations (10) and (15) give
\[
E_0
\le C\mathcal G_0D_{\rm hold}(1+a),
\]
\[
E_1
\le C\mathcal G_1D_{\rm hold}(1+a)^2.
\tag{16}
\]

Using (11),
\[
\boxed{
E_0\le
C\mathcal G_0
\left(D_{\rm hold}+\sqrt{B_{\rm mix}D_{\rm hold}}\right),
}
\tag{17}
\]
while
\[
\boxed{
E_1\le C\mathcal G_1(1+B_{\rm mix}).
}
\tag{18}
\]

The first bound tends to zero. The second provides a raw \(H^1\) envelope independent of \(D_{\rm hold}\).

These bounds permit \(\theta\) to switch arbitrarily rapidly or align adversarially with the shear phases.

### 3.3 Include the full coupled implementation

During the physical holds, use the comparison equation
\[
\beta_t
=
\rho(t)A_{\rm phase}\beta
+
M_{\rm phase}^{-1}G_\theta.
\tag{19}
\]
The live source then cancels from the magnetic error equation.

The preceding kernel argument gives the required endpoint \(H^1\) bound. At any fixed higher spatial order, its envelope may grow polynomially in \(a\), which is sufficient for compiling the physical holds and resets.

Choose the small hold lengths, disposable-velocity tolerances, and reset accuracies after those envelopes are fixed. The whole-macro Lorentz/induction estimates then make the physical error arbitrarily small at polynomial cost.

During load, unload, and reset periods, use (9). Their total duration and source error are separately budgeted. The input acts throughout.

### 3.4 A genuine smoothing tail closes the \(H^1\) estimate

The parameter ordering needs one further distinction.

At the raw unloaded endpoint, decompose
\[
z_{\rm raw}=z_{\rm target}+e_h+e_G,
\qquad z=(u,B-H),
\tag{20}
\]
where:

- \(e_h\) contains homogeneous leakage, baseline heat bias, physical implementation errors, and small endpoint velocity;
- \(e_G\) is the forced-hold contribution estimated in (17)–(18).

Arrange
\[
\|e_h\|_{H^1}\le\delta/20.
\]
Choose \(B_{\rm mix}\) from this homogeneous \(H^1\) leakage allowance and the already fixed smooth-reference envelope. Direct enhanced-heat damping permits this choice independently of \(D_{\rm hold}\).

The raw endpoint has a bound
\[
P_{\rm raw}
=
C\left(P_{\rm in}+\mathcal G_1(1+B_{\rm mix})+1\right).
\tag{21}
\]

Append an unforced interval of duration \(\ell\), with the input still present. The joint constant-\(H\) semigroup contracts \(e_h\) in \(H^1\), while smoothing \(e_G\) from \(L^2\). The nonlinear Duhamel estimate gives
\[
\begin{aligned}
\|z_{\rm out}-z_{\rm target}\|_{H^1}
\le{}&
\delta/20
+
\frac{C E_0}{\sqrt{\mu\ell}}\\
&+
CP_{\rm raw}^2\mu^{-3/4}\ell^{1/4}
+
C(\mathcal G_0+\eta)\sqrt{\ell/\mu}
+
P_{\rm target}\ell .
\end{aligned}
\tag{22}
\]
The last term includes the smooth target’s constant-\(H\) coupling as well as diffusion.

The noncircular choice is:

1. Fix \(B_{\rm mix}\) from the homogeneous error budget.
2. Compute \(P_{\rm raw}\).
3. Choose \(\ell\) from \(P_{\rm raw}\), the error budget, local continuation, and the available clock.
4. Choose \(D_{\rm hold}\) so that
   \[
   \mathcal G_0
   \sqrt{B_{\rm mix}D_{\rm hold}}
   \ll\delta\sqrt{\mu\ell},
   \tag{23}
   \]
   and so that baseline heat bias is small.
5. Choose \(a\), macro/cycle counts, and physical accuracies.

Only \(e_G\) receives the factor \(\ell^{-1/2}\). Applying that factor to the homogeneous leakage as well would create an unnecessary parameter circle.

Every reciprocal parameter in this construction is polynomial.

---

## 4. The remaining active components

The directional filter was the adverse geometry-duration case. The other components admit separate forcing-aware estimates.

### Scalar transitions and their heat windows

The scalar-gate construction fixes its dimensionless packet geometry before physically compressing the flow words. Its positive-heat window has a duration decreasing as a fixed inverse power of its packet parameter; the [recorded passive prefix construction](https://github.com/harjassand/astra-research-knowledge/blob/main/knowledge/units/U1799-passive-whole-field-wavepacket-gate-with-polynomial-prefix-bounds/v0001.json) uses
\[
Q=q^4,\qquad T_{\rm heat}=\rho_0^{-1}q^{-7},
\]
with polynomial prefix and inverse-prefix bounds.

Pay input during the flow words by (9). On the positive-heat holds, use
\[
\beta_t=\rho(t)\Delta\beta+G_\theta
\]
as the comparison reference. Relative to the input-free heat target, its source contribution is at most
\[
T_{\rm heat}\mathcal G_1.
\tag{24}
\]
The spatial envelope used for the physical implementation is at most \(P+T_{\rm heat}\mathcal G_m\). Input during intervening resets is paid by their separately compressed words.

### Initial smoothing of a router

Start the smoothing reference from the entire actual incoming \(H^1\) state and include the actual live input, with only the small rough disturbance omitted.

For a requested raw Fourier feature at frequency at most \(N_p\),
\[
|\ell_j(B(s))-\ell_j(B(0))|
\le
Cs\left(PN_p^2+P^2N_p+\mathcal G_0+\eta\right).
\tag{25}
\]
Choose \(s\) from this feature budget and the available clock before selecting the later controlled-stage parameters.

Because \(G_\theta\) has paid bounds at every required fixed spatial order, the reference gains the needed spatial regularity despite merely measurable time dependence.

Combining this smoothing step, the simultaneous encoder, the upgraded scalar transitions, and the filters in Section 3 gives the live-router contract
\[
\boxed{
(u_{\rm in},B_{\rm in})
\longmapsto
\left(
0,\,
H+\operatorname{Code}\bigl(\mathsf K\,\ell(B_{\rm in})\bigr)
\right)
+\text{an absolute }H^1\text{ error }\delta .
}
\tag{26}
\]
It holds uniformly on a supplied actual \(H^1\) ball, under an arbitrary prescribed duration cap, with polynomial costs including the input spatial bounds.

The target in (26) uses the coefficients at the **start of that invocation**. It is not a later smoothed-state target.

---

## 5. Live input during the natural packet windows

The ternary and final readout windows have their own physical time scales. They require direct estimates.

Let \(z^*\) be the smooth input-free reference, and let \(z\) start from the same state with live \(G_\theta\). Put
\[
e_0=\|z-z^*\|_2,\qquad e_1=\|z-z^*\|_{H^1},
\]
\[
L_1(t)=C\|\nabla z^*(t)\|_\infty,\qquad
L_2(t)=C\|\nabla^2z^*(t)\|_\infty.
\]

Joint MHD cancellation gives
\[
e_0'\le L_1e_0+\mathcal G_0.
\]
Hence
\[
e_0(t)\le
\exp\!\left(\int_0^tL_1\right)\mathcal G_0t.
\tag{27}
\]

The one-derivative estimate is
\[
e_1'
\le
C(1+L_1)e_1
+C L_2e_0
+C\mu^{-3}e_1^5
+\mathcal G_1.
\tag{28}
\]

The second reference derivatives multiply the \(L^2\) error. Since the live-input difference starts at zero, this supplies an extra factor of \(t\).

Define
\[
J_2(T)=\int_0^TtL_2(t)\,dt.
\]
A continuation argument gives
\[
e_1(T)
\le
C e^{C(T+\int L_1)}
\left[\mathcal G_1T+\mathcal G_0J_2(T)\right],
\tag{29}
\]
provided the resulting bound satisfies the explicit polynomial smallness condition for the \(e_1^5\) term. The packet choices below ensure that condition.

### Strong ternary interaction

For
\[
Q=\ell^4,\qquad A=\ell^6,\qquad T_c=\ell^{-11},
\]
the prepared finite-packet reference has
\[
L_1\le CAQ,\qquad L_2\le CAQ^2.
\]
Therefore
\[
\int_0^{T_c}L_1\le C\ell^{-1},
\qquad
J_2(T_c)\le C\ell^{-8},
\]
and
\[
\boxed{
E_{\rm live,ternary}^{H^1}
\le
C\left(\mathcal G_1\ell^{-11}
+\mathcal G_0\ell^{-8}\right).
}
\tag{30}
\]

This decreases with the same packet parameter already used to pay the cubic remainder. Its post-interaction cleanup uses the live router.

### Weak final readout

Let the total packet critical norm be \(\sigma\le c\mu\), and let
\[
T_Q\asymp\frac{\mathcal L(Q)}{\mu Q^2},
\tag{31}
\]
where \(\mathcal L\) is the paid logarithmic clearing factor.

For the packet remainder around the smooth background, use the joint Fourier norms
\[
X^m=\sum_{k\ne0}|k|^m
\left(|\widehat u_k|^2+|\widehat b_k|^2\right)^{1/2}.
\]
The constant-\(H\) coupling is skew-Hermitian. The small-critical estimate and parabolic interpolation give
\[
\sup X^{-1}\le2\sigma,\qquad
\int_0^{T_Q}X^1\,dt\le C\sigma/\mu,
\]
\[
X^2(t)\le C\sigma(\mu t)^{-3/2}.
\tag{32}
\]
The smooth background contributes fixed polynomial terms. Consequently,
\[
\int_0^{T_Q}L_1
\le PT_Q+C\sigma/\mu,
\]
\[
J_2(T_Q)
\le
C\left(PT_Q^2+
\sigma\mu^{-3/2}\sqrt{T_Q}\right).
\tag{33}
\]

Substitution into (29) yields
\[
\boxed{
E_{\rm live,readout}^{H^1}
\le
C\left[
\mathcal G_1T_Q+
\mathcal G_0PT_Q^2+
\mathcal G_0\sigma\mu^{-3/2}\sqrt{T_Q}
\right].
}
\tag{34}
\]
In particular, this is a fixed polynomial factor times
\[
\frac{\operatorname{polylog}Q}{Q}.
\]

Choose the amplifier and its gain first, then \(Q\) so that (34) is below its incoming-error allowance. This is a polynomial choice.

The live references themselves have paid higher spatial envelopes: take the background reference with the actual \(G_\theta\), and apply the packet estimates to its remainder. The genuinely small rough disturbances are then handled around that live reference, with \(\eta\) selected last.

No temporal derivative of \(\theta\) appears.

---

## 6. Streaming acquisition on the original time interval

We can now build the streaming part.

Compile initial capture and the final sparse calculation/writer under small duration caps. Let their actual rational durations be
\[
T_{\rm cap},\qquad T_{\rm fin}.
\]
The storage interval is
\[
I=[T_{\rm cap},\tau-T_{\rm fin}],
\qquad T=|I|\ge\tau/2.
\]

Choose \(J\) and divide \(I\) into equal cells of length
\[
\Delta=T/J.
\]

### Average the known weights

For each temporal feature and grid cell, compute
\[
\bar w_{\ell j}
=
\frac1\Delta\int_{I_j}w_\ell(t)\,dt.
\tag{35}
\]
This integral is evaluated exactly from the supplied rational interval lists. It never evaluates \(\theta\).

For a step-function interval, only its boundary cells incur a cell-averaging error. Thus
\[
\sum_\ell
\|w_\ell1_I-\bar w_\ell\|_{L^1}
\le2K_t\Delta.
\tag{36}
\]
Also,
\[
\|\bar w_\ell\|_1\le1,
\qquad
\sum_\ell|\bar w_{\ell j}|\le K_t.
\tag{37}
\]

An extremely short input interval contributes a small rational number to (35). The only division is by \(\Delta\), whose reciprocal is polynomial. No inverse minimum weight-interval length occurs.

### One streaming cell

Each cell consists of:

1. A live router that copies every current register to its base and doubled frequencies, clears the input band, and resets velocity.
2. An unforced hold of duration \(d_j\).
3. A live router that refreshes the old registers, adds the new temporal contributions, and clears the temporary modes.

The input is present in every stage.

On the hold, let
\[
I_{p,j}=\int_{\text{hold }j}\theta_p(t)\,dt.
\]
The full coupled short-time equations give
\[
c_p(B_{\rm hold,end})
=
I_{p,j}+O(Pd_j^2),
\tag{38}
\]
because the initial input-band coefficient and its initial diffusion projection have been cleared, and velocity starts at zero.

For a copied code value \(a\),
\[
b_n(d_j)
=
a-\kappa^2n^2a\int_{\rm hold}\rho+O(Pd_j^2),
\]
\[
b_{2n}(d_j)
=
a-4\kappa^2n^2a\int_{\rm hold}\rho+O(Pd_j^2).
\tag{39}
\]

The update rows are therefore
\[
\text{initial source:}\qquad
\frac{4b_n-b_{2n}}3,
\]
\[
\text{temporal register }\ell:\qquad
\frac{4b_n-b_{2n}}3
+\bar w_{\ell j}\,c_{j(\ell)}(B).
\tag{40}
\]

These are known rational routing matrices. The raw-integral representation includes the known factors of two for sine amplitudes and the port normalization in (2).

There is no division by \(d_j\).

### Accumulation and stability

On the bounded code ball, one ideal cell has the form
\[
F_j^\theta(a)=a+W_jI_j+E_j^\theta(a),
\]
with
\[
\|E_j^\theta(a)\|_\infty+
\|DE_j^\theta(a)\|
\le Pd_j^2.
\tag{41}
\]
Here \(P\) includes the code band, input spatial norms, \(K_t\), and coefficient bounds.

The physical cell satisfies
\[
a^{j+1}=F_j^\theta(a^j)+\xi_j,
\qquad
\|\xi_j\|_\infty\le\gamma.
\tag{42}
\]

Since \(d_j\le\Delta\le1/J\),
\[
\sum_jd_j^2\le1/J.
\]
Thus
\[
E_J
\le
e^{P/J}
\left(E_0+\frac PJ+J\gamma\right).
\tag{43}
\]

Choose
\[
J\ge C(P+K_t+1)\delta_{\rm feat}^{-1},
\qquad
\gamma\le\frac{\delta_{\rm feat}}{CJ},
\tag{44}
\]
and enlarge \(J\) to cover the local full-space continuation requirement.

The intended temporal partial sums have modulus at most one by (37). Equation (43) keeps the actual code in its fixed enlarged ball.

---

## 7. Account for input during every active operation

Let \(\mathcal A\) be the union of:

- initial capture;
- all active streaming routers and their smoothing/reset intervals;
- final arithmetic, preparation, packet readout, amplification, and writing.

Choose a total time allowance
\[
|\mathcal A|\le\sigma,
\qquad
\sigma\le
\min\left\{\frac{\tau}{8},
\frac{\delta_{\rm feat}}{C K_t}\right\}.
\tag{45}
\]

The temporal value accumulated by the ideal streaming schedule is
\[
\widehat h_\ell
=
\sum_j\bar w_{\ell j}
\int_{\text{hold }j}\theta_{j(\ell)}(t)\,dt.
\]
For the original full-interval feature,
\[
h_\ell=\int_0^\tau
w_\ell(t)\theta_{j(\ell)}(t)\,dt,
\]
we have, uniformly over all measurable histories,
\[
\boxed{
|h_\ell-\widehat h_\ell|
\le2K_t\Delta+K_t\sigma.
}
\tag{46}
\]

The physical contamination during \(\mathcal A\) is paid by Sections 2–5. Equation (46) pays the temporal feature contribution not accumulated on holds.

These are two distinct error terms. Small omitted measure is not being used to excuse uncontrolled physical contamination.

### Exact clock

After capture and final computation are compiled, \(T\) is known exactly.

After choosing \(J\), compile each cell’s two active routers under caps whose total is at most
\[
\frac{\sigma}{CJ}.
\]
Let their actual total duration be \(h_j\). Set
\[
d_j=\Delta-h_j.
\tag{47}
\]
The caps ensure \(d_j\ge\Delta/2>0\).

The routing matrices do not depend on \(d_j\), and their estimates are uniform for \(0\le d_j\le\Delta\). Therefore no implicit compilation equation is required. Every cell ends at its prescribed rational grid boundary, and the entire programme ends exactly at \(\tau\).

---

## 8. Sparse calculation and final output

At the end of streaming, the bank contains approximations to:

- the original conserved means and retained initial probes;
- all requested full-interval temporal features.

The accepted sparse arithmetic schedule applies to this enlarged source list. For each nonconstant even monomial, select one factor:
\[
h^\alpha=h_jh^{\alpha-e_j}.
\]
Compute the odd remainder by ternary assignments. Each odd monomial is similarly built by starting from one factor and multiplying two at a time.

The count remains
\[
N_{\rm arith}\le CS(D+1),
\tag{48}
\]
with polynomially many slots.

Each ternary stage uses (30), and each routing/cleanup stage uses (26). Source and arithmetic errors are chosen below
\[
\delta_{\rm feat}\le\frac{\epsilon}{C K(D+1)}.
\tag{49}
\]
Taking the constant sufficiently large also ensures \(D\delta_{\rm feat}\ll1\).

On the resulting enlarged coordinate cube,
\[
\|U(\cdot,h)-U(\cdot,\widetilde h)\|_2
+
\|Z(\cdot,h)-Z(\cdot,\widetilde h)\|_2
\le
CKD\|h-\widetilde h\|_\infty.
\tag{50}
\]
Product-chain growth is bounded by
\[
(1+C\delta_{\rm feat})^D\le C.
\]

The final odd magnetic output and preconditioned even readout packets are prepared together. Internal \(\rho\)-weighted sources can still be formed from copied high code modes: the full coupled short-hold expansion with live low-band input gives the same first-order decay difference, with an \(O(Ps)\) error after the known division by \(s\). The code band is above \(N\), so the input has no direct projection onto those modes.

Then use one final weak packet batch, the accepted flat-band amplifier, and the known degree-zero velocity increment. Equation (34) pays the input during the packet window; equation (9) pays it during the fixed-geometry amplifier and translations.

All these intervals are included in \(\mathcal A\).

---

## 9. Compiler and universal resource certificate

The deterministic compiler can be organized as follows.

```text
1. Canonicalize all rational lists and aggregate duplicates.
   Truncate initial probes and output spatial frequencies.

2. Compute exact port norms and their rational Fourier readout rows.
   Compute fixed-order uniform spatial bounds for the live input.

3. Choose the canonical band above N and all required code slots.
   Build the O(SD) sparse arithmetic schedule.

4. Allocate feature, arithmetic, physical, and final-output errors.
   Choose the total active-time allowance sigma.

5. Compile live initial capture and the live final computation
   under their assigned parts of sigma.

6. Compute their exact rational durations and the remaining interval.

7. Choose J from the uniform streaming hold bounds.
   Compute exact rational cell averages of the known step weights.

8. Compile the active copy and update routers for each cell.
   Set each hold duration to its cell length minus active overhead.

9. Concatenate capture, streaming cells, arithmetic, and final writing.

10. Choose eta below every uniform small-rough-disturbance threshold.
    Emit the twelve ordinary rational piecewise-polynomial coefficients.
```

The parameter graph has fixed depth.

- The smooth envelope before a router is chosen before its controlled-stage parameters.
- A fixed-geometry word is compressed only after its geometry is fixed.
- A directional filter chooses \(B_{\rm mix}\), then its smoothing tail, then its short hold time and shear amplitude.
- Natural packet windows pay their live input through explicit decay in the packet parameter.
- Every streaming cell and arithmetic assignment returns to the same canonical band.
- Variable repetitions multiply a common per-operation cost; they do not recursively increase its exponent.

Known-weight averaging requires only polynomially many rational interval-overlap operations, for example \(O(JS_tq_2)\) as a simple upper bound. Tiny original interval lengths affect binary arithmetic, not physical time scales.

### Computable universal \(A,p\)

Use the accepted primitive resource polynomials as fixed inputs. Add the finite-order estimates proved above:

- shear prefix bounds;
- the two-space macro rate (14);
- source-insertion bounds (16);
- smoothing and continuation bounds;
- packet source bounds (30) and (34);
- streaming and weight-averaging bounds.

All constants can be majorized using finite Fourier product estimates, explicit shear coefficients, \(2\pi<7\), fixed-order spatial energy estimates, and rational Young inequalities.

Propagate these bounds symbolically through the fixed dependency graph and multiply by the polynomial loop counts. Replace logarithms, ceilings, and fixed powers by integer-polynomial majorants. Let the resulting univariate majorant be \(Q(X)\), including the finite precomputation cost. Set
\[
p=\max(1,\deg Q),
\qquad
A=1+\left\lceil\sum_m|[X^m]Q|\right\rceil,
\tag{51}
\]
after a fixed enlargement for the finitely many normalizations.

This is a terminating arithmetic prescription for universal constants independent of every variable input and history. It gives
\[
\begin{aligned}
&\text{bit operations, memory bits, output bits, interval count,}\\
&\text{degrees and individual rational bit lengths}
\le A(L+R)^p,
\end{aligned}
\tag{52}
\]
and
\[
\eta^{-1}
+
\sup_t\|f(t)\|_{W^{1,\infty}}
+
\int_0^\tau\|f(t)\|_{W^{1,\infty}}\,dt
\le AR^p.
\tag{53}
\]

Tiny known coefficients are handled with absolute error budgets. No inverse input value, inverse tiny weight interval, or inverse small target coefficient enters the numerical resource bound.

---

## 10. Energy realizations, symmetry, and the endpoint

The energy inequality used throughout is the actual forced one:
\[
\begin{aligned}
\frac12\|(u,B)(t)\|_2^2
&+\int_s^t
\left(\nu\|\nabla u\|_2^2+\rho\|\nabla B\|_2^2\right)\,dr\\
&\le
\frac12\|(u,B)(s)\|_2^2\\
&\quad+
\int_s^t
\left[
\langle f+h_u,u\rangle
+
\langle G_\theta+h_B,B\rangle
\right]\,dr .
\end{aligned}
\tag{54}
\]

The references receiving \(G_\theta\) exist with the stated spatial bounds for bounded measurable histories. Their values are proof quantities and are never evaluated by the compiler.

The initial short interval and the controlled continuation estimates cover the actual \(H^1\) initial state, including its unknown velocity. Subsequent routers, holds, and packet stages maintain controlled strong continuation. Weak–strong uniqueness, applied with the same actual coefficients, live input, force, and rough disturbances, identifies every energy-admissible realization with the controlled strong solution on these segments.

All ports and chosen forces have zero spatial mean, so \(H\) remains exactly conserved. The register operations and final readout retain the simultaneous magnetic/input reversal symmetry. No independence or nonzero-value assumption is used.

Choose the budgets so that truncation, feature acquisition, weight approximation, omitted temporal contribution, streaming error, arithmetic error, and final physical error sum to less than \(\epsilon\). Then
\[
\begin{aligned}
&\|u(\tau)-U(x,h(B_0,\theta))\|_2\\
&\qquad+
\|B(\tau)-H-Z(x,h(B_0,\theta))\|_2
<\epsilon,
\end{aligned}
\tag{55}
\]
which implies the requested joint Euclidean bound. The final strong trace agrees with the specified one-sided energy trace.

**The additional theorem is therefore the live-input active-stage interface, especially the two-space directional-filter estimate.** With that estimate and the direct packet forcing bounds, the streaming accumulation, retained memory, sparse computation, and exact clock form one ordinary mechanical programme for the original full-interval data contract.