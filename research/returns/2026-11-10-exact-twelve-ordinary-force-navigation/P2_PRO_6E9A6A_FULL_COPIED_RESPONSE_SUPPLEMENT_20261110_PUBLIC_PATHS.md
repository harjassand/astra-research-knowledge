# P2 completed final: full copied response supplement

Source: https://chatgpt.com/c/6af2d0d2-f500-83ec-a7d0-20e80bd42677
Final: 6e9a6a3f-833c-5934-b664-ea24360e0379
Prompt: work/astra-renewed-pro-programmes-20261103/P2_FULL_TWELVE_FUNDAMENTAL_BODY_FORCE_POLYNOMIAL_PRO_20261110.txt
Supplement to P2_PRO_6E9A6A_TWELVE_RETURN_20261110.md. Captured via the final response Copy control and a separate TextEdit view; this is the complete visible copied text, with TextEdit accessibility serialization (including list formatting), not a byte-identity guarantee against native source.

---

**Answer: yes, from the constructive premises supplied**
There is a reduction to the **exact twelve fundamental shear actuators** that retains polynomial resources.
The additional construction uses rapidly oscillating velocity excursions with two properties:
	1	Each excursion has zero time integral, so its physical linearized propagator returns **exactly to the identity**.
	2	Its quadratic self-interaction has a prescribed nonzero average, which supplies a forcing direction from the next saturation level.
The important quantitative point is how to assemble these excursions. Below, the averaging errors are represented by explicitly bounded corrections to a prescribed reference path. Their force residuals **add**, and the remaining linear defect can be made smaller than a fixed fraction of viscosity. This permits the blockwise \(H^1\) argument from your enlarged-family theorem to survive the actuator reduction.
The resulting exponent is much larger than \(128\). If \(D\) is the fixed saturation depth computed during preprocessing, one conservative choice is
\[ \boxed{p=256\,32^{D+1}.} \]
The final time coefficients have degree at most \(3\), and one can retain
\[ \boxed{\eta=\frac1{16\rho},\qquad \eta^{-1}\le32R,} \]
where
\[ \rho= 2+\lceil M\rceil+\lceil\nu^{-1}\rceil+ \lceil\tau^{-1}\rceil+\lceil\epsilon^{-1}\rceil. \]
Here is the construction and proof. The enlarged-family theorem is used as the accepted starting theorem; its larger fields occur only in the intermediate construction and analysis. The force ultimately emitted belongs exactly to the twelve-dimensional space in the question.

**1. A fixed, rational saturation certificate**
Write
\[ \kappa=2\pi,\qquad B(u,v)=\mathbb P[(u\cdot\nabla)v],\qquad L_Fv=B(F,v)+B(v,F), \]
and introduce the algebraically normalized interaction
\[ \mathcal B(u,v)=\kappa^{-1}B(u,v). \]
For trigonometric fields with integer wavevectors and rational polarizations, \(\mathcal B\) has rational Fourier coefficients. The Fourier Leray projections
\[ P_k=I-\frac{k\otimes k}{|k|^2},\qquad k\ne0, \]
are rational matrices.
Let
\[ V_0=\operatorname{span}\left\{ e_i\cos(2\pi x_j),\ e_i\sin(2\pi x_j):i\ne j \right\}. \]
During fixed preprocessing, construct finite rational Fourier spaces
\[ V_0\subset V_1\subset\cdots\subset V_D \tag{1} \]
such that \(V_D\) contains the enlarged shear family from the supplied theorem.
The finite Fourier saturation needed here is available from the supplied algebraic premise. Nersesyan’s Theorem 4.1 and Proposition 4.3 also supply exact finite-level generation, including the twelve-mode choice, rather than only density of an unspecified collection. <u>[arxiv.org](arxiv.org/pdf/1403.5369v2?utm_source=chatgpt.com)</u>
**1.1 Why the certificates support the required signs**
If \(a,b\) are individually single divergence-free Fourier modes, then
\[ B(a,a)=B(b,b)=0. \]
Consequently,
\[ \mathcal B(a+b,a+b) =\mathcal B(a,b)+\mathcal B(b,a), \]
and
\[ \mathcal B(a-b,a-b) =-\mathcal B(a,b)-\mathcal B(b,a). \tag{2} \]
Thus both signs of each symmetric interaction are available through negative quadratic squares of fields in the lower space.
Choose a pure-frequency sine/cosine basis at every level. These spaces can be kept invariant under translations, and hence under \(\Delta\). One way to see this is that the operation
\[ V\longmapsto V+\operatorname{span}\{\mathcal B(a,a):a\in V\} \]
preserves translation invariance. Every finite-dimensional translation-invariant trigonometric space is a sum of Fourier subspaces.
Exact rational linear algebra therefore produces, for every basis vector and its negative at level \(j+1\), certificates of the form
\[ u=\eta(u)-\sum_{\ell=1}^{J_j} d_\ell(u)\,\mathcal B(\xi_\ell,\xi_\ell), \qquad d_\ell(u)\ge0, \tag{3} \]
where
\[ \eta(u),\xi_\ell\in V_j. \]
The list of possible \(\xi_\ell\)’s is fixed. For a general rational \(u\in V_{j+1}\), sign splitting of its basis coefficients gives (3) by rational arithmetic.
The certificate coefficients satisfy fixed bounds
\[ \|\eta(u)\|_*+\sum_\ell d_\ell(u)\le C\|u\|_*. \tag{4} \]
Here and below \(\|\cdot\|_*\) is a computable coefficient norm on a fixed finite Fourier table, large enough to control every spatial norm used in the proof.
This preprocessing terminates by finite algebraic saturation. Its entire search, rational elimination, Fourier tables, and certificate descriptions are charged to the fixed preprocessing cost.

**2. The enlarged-family reference**
Use the supplied enlarged-family construction, with its fixed constants enlarged when necessary below. It gives a prescribed carrier \(w\), a rational force \(f^{(0)}\in V_D\), and the macro-word \(W(s)\).
Use
\[ T=B_*\rho^4,\qquad s=(B_*^2\rho^6)^{-1},\qquad n=B_*^9\rho^{28},\qquad \delta=(B_*\rho^8)^{-1}. \tag{5} \]
Then
\[ ns^4=T,\qquad ns^5=(B_*\rho^2)^{-1}. \]
The fixed integer \(B_*\) is chosen large enough that:
	•	\(\delta\le\tau/2\);
	•	the supplied linear word satisfies\[ \|W(s)^nU_0\|_2\le\epsilon/4 \quad\text{whenever }\|U_0\|_{H^1}\le M; \tag{6} \]
	•	the blockwise Sobolev and viscosity estimates have the smallness margins used below;
	•	\(\delta\le\nu^3/(128C_EM^4)\);
	•	the numerical endpoint estimate in Section 7 is at most \(\epsilon/4\).
The last requirement only enlarges a fixed constant.
The carrier is zero at the beginning and end of every original pulse, in particular at every macro-block boundary. Its rational enlarged-family force can be rounded so that
\[ r^{(0)} = f^{(0)}-\bigl(w_t-\nu\Delta w+B(w,w)\bigr) \]
satisfies
\[ \|r^{(0)}\|_{L^\infty L^2}\le\frac1{16}. \tag{7} \]
Set \(b^{(0)}=w\).
The reduction will construct
\[ f^{(j)}\in V_{D-j},\qquad j=1,\ldots,D. \]
Only \(f^{(D)}\) is ultimately applied.

**3. One explicit lowering step**
Suppose \(f^{(j-1)}\) and a prescribed reference \(b^{(j-1)}\) have been constructed.
Let an integer \(H\ge2\) bound:
	•	\(f^{(j-1)}\) and its first time derivative inside each polynomial interval;
	•	\(b^{(j-1)}\) and its first piecewise time derivative;
	•	the amplitudes of all previously constructed carrier fields;
	•	the old interval count and the reciprocal of the shortest old interval.
All spatial bounds are in the fixed norm \(\|\cdot\|_*\). Section 5 gives a deterministic numerical envelope that provides these bounds without evaluating a PDE or a norm oracle.
**3.1 Refine the existing partition**
Subdivide each old interval into
\[ N=\lceil K H^6\rceil \tag{8} \]
equal rational cells. Here \(K\) is a sufficiently large fixed integer chosen in preprocessing.
In each cell \(I=[a,a+d]\), freeze
\[ u_I=f^{(j-1)}(a+). \]
Apply the fixed certificate (3):
\[ u_I=\eta_I-\sum_{\ell=1}^{J} d_{I,\ell}\,\mathcal B(\xi_\ell,\xi_\ell). \tag{9} \]
Use \(J\) equal slots in this cell. The list may contain zero-amplitude slots, so its length is fixed.
**3.2 A cubic carrier with an exact linear reset**
Take
\[ p(z)=z(1-z)(2z-1)=-2z^3+3z^2-z. \]
Its exact identities are
\[ p(0)=p(1)=0,\qquad \int_0^1p(z)\,dz=0,\qquad \int_0^1p(z)^2\,dz=\frac1{210}. \tag{10} \]
Also,
\[ \int_0^z p(r)\,dr=-\frac12z^2(1-z)^2, \qquad \sup_{0\le z\le1}\left|\int_0^zp\right|=\frac1{32}. \tag{11} \]
On slot \(\ell\), of length \(d/J\), set
\[ \zeta_j(t) = A_{I,\ell}\, p\!\left(\frac{t-t_{I,\ell}}{d/J}\right)\xi_\ell. \tag{12} \]
Choose nonnegative rational amplitudes approximating
\[ A_{I,\ell} = \sqrt{\frac{210J\,d_{I,\ell}}{\kappa}}. \tag{13} \]
The approximation is chosen so that
\[ \left\| \eta_I-u_I-\frac1d\int_I B(\zeta_j,\zeta_j)\,dt \right\|_* \le H^{-8}. \tag{14} \]
This is possible with \(O(\log H)\) precision bits, plus fixed constants. Certified rational approximations of \(\kappa\) and square roots suffice.
The carrier has zero time integral on every slot. During a slot its physical linearized propagator is
\[ \mathcal P_j(t) = \exp\!\left(-\chi_j(t)L_{\xi_\ell}\right), \qquad \chi_j(t)=\int_{t_{I,\ell}}^t A_{I,\ell}p\!\left(\frac{r-t_{I,\ell}}{d/J}\right)\,dr. \tag{15} \]
It therefore returns **exactly to \(I\)** at the end of each slot.
The quadratic average survives:
\[ \frac1d\int_I B(\zeta_j,\zeta_j)\,dt = \frac{\kappa}{210J} \sum_{\ell=1}^J A_{I,\ell}^2 \mathcal B(\xi_\ell,\xi_\ell). \tag{16} \]
**3.3 The lower-space force**
Let \(\eta_j(t)=\eta_I\) on cell \(I\). Choose a rational Fourier multiplier \(\widehat\Delta_j\) approximating \(\Delta\), and set
\[ \boxed{ f^{(j)} = \eta_j+\partial_t\zeta_j-\nu\widehat\Delta_j\zeta_j. } \tag{17} \]
The lower space is invariant under \(\Delta\), and under its rational scalar-multiplier approximation. Therefore
\[ f^{(j)}\in V_{D-j}. \]
Its time coefficients are ordinary rational polynomials of degree at most three. The carrier is continuous and zero at every slot boundary. Thus its derivative in (17) introduces no distributional impulses.
The approximation of \(\Delta\) can be chosen so that
\[ \nu\|(\Delta-\widehat\Delta_j)\zeta_j\|_* \le H^{-8}. \tag{18} \]
For a Fourier wavevector \(k\), this just replaces \(-\kappa^2|k|^2\) by a rational approximation. Again, \(O(\log H)\) precision bits suffice.

**4. Exact reference-path corrections and additive residuals**
The next definitions are used to prove what the emitted force does. They do not require a PDE solution.
Define
\[ \begin{aligned} \partial_t\beta_j ={}& \eta_j-f^{(j-1)} -L_{b^{(j-1)}}\zeta_j -B(\zeta_j,\zeta_j),\\ \beta_j(0)={}&0, \end{aligned} \tag{19} \]
and
\[ b^{(j)}=b^{(j-1)}+\zeta_j+\beta_j. \tag{20} \]
All these fields are finite Fourier sums and piecewise polynomials in time. Their coefficients involve only the known controls, \(\nu\), and the fixed constant \(\kappa\). Their Fourier supports lie in a fixed finite table determined during preprocessing.
Define
\[ r^{(j)} = f^{(j)} -\left[ \partial_tb^{(j)}-\nu\Delta b^{(j)} +B(b^{(j)},b^{(j)}) \right]. \tag{21} \]
Expansion gives the exact identity
\[ \boxed{ \begin{aligned} r^{(j)}={}&r^{(j-1)} +\nu(\Delta-\widehat\Delta_j)\zeta_j +\nu\Delta\beta_j\\ &-L_{b^{(j-1)}+\zeta_j}\beta_j -B(\beta_j,\beta_j). \end{aligned}} \tag{22} \]
In particular, an old residual is not multiplied by the amplitude of a later carrier.
**4.1 Why the primitive \(\beta_j\) is small**
On a complete cell \(I\), the mean matching (14) and the time variation of \(f^{(j-1)}\) give
\[ \left\| \int_I\bigl(\eta_j-f^{(j-1)}-B(\zeta_j,\zeta_j)\bigr)\,dt \right\|_* \le |I|H^{-8}+C|I|^2H. \tag{23} \]
Also,
\[ \int_I L_{b^{(j-1)}(a)}\zeta_j(t)\,dt=0 \]
because every slot has zero integral. Hence
\[ \begin{aligned} \left\|\int_I L_{b^{(j-1)}(t)}\zeta_j(t)\,dt\right\|_* &= \left\|\int_I L_{b^{(j-1)}(t)-b^{(j-1)}(a)}\zeta_j(t)\,dt\right\|_*\\ &\le C|I|^2H^2. \end{aligned} \tag{24} \]
An incomplete cell contributes at most \(C|I|H^2\). Since the whole active interval has length at most one,
\[ \sum_{\text{complete cells}}|I|^2 \le d_{\max}\sum|I| \le d_{\max}. \]
Thus
\[ \|\beta_j\|_{L^\infty_*} \le C\bigl(d_{\max}H^2+H^{-8}\bigr). \tag{25} \]
By (8), \(d_{\max}\le(KH^6)^{-1}\), so
\[ \boxed{ \|\beta_j\|_{L^\infty_*}\le CH^{-4}. } \tag{26} \]
This is a bound over the entire active interval. It does not grow with the number of microcells.
Equations (18), (22), and (26) now imply
\[ \boxed{ \|r^{(j)}-r^{(j-1)}\|_{L^\infty_*} \le CH^{-3}. } \tag{27} \]
At the final time,
\[ b^{(D)}(\delta)=\sum_{j=1}^D\beta_j(\delta), \tag{28} \]
because \(w\) and all \(\zeta_j\) vanish there. The \(\beta_j\)’s need not reset to zero; their small endpoint values will be included in the total-velocity estimate.

**5. A fixed polynomial hierarchy for every stage**
Choose
\[ H_0=K\rho^{160}, \qquad H_j=K H_{j-1}^{32},\quad j=1,\ldots,D. \tag{29} \]
At stage \(j\), use \(H=H_{j-1}\).
The fixed integer \(K\) is selected from the precomputed Fourier, certificate, and operator bounds.
The exponent \(160\) is a coarse bound for the original reference. Its force is \(O(\rho^{66})\), its piecewise time derivative is bounded by a fixed multiple of \(\rho^{102}\), its carrier and carrier derivative are polynomially bounded, and its interval count and inverse pulse length are \(O(\rho^{28})\) and \(O(\rho^{36})\). Thus \(H_0\) covers all the incoming numerical bounds after increasing \(K\).
For one lowering step, the estimates are:
**Quantity
Bound in terms of incoming \(H\)**
Carrier amplitude \(|\zeta_j|_*\)
\(CH\)
Maximum partial impulse (
\chi_j
Correction \(|\beta_j|_*\)
\(CH^{-4}\)
Added force residual
\(CH^{-3}\)
New interval count
\(CH^7\)
Reciprocal minimum new interval length
\(CH^7\)
\(|\partial_t\zeta_j|_*\)
\(CH^8\)
\(|\partial_t^2\zeta_j|_*\)
\(CH^{15}\)
New force and its first piecewise derivative
At most \(CH^{15}\)
For example, the derivative estimates follow from the inverse slot-length bound and the fixed cubic profile. The larger update \(KH^{32}\) comfortably covers these quantities and the numerical magnitudes introduced by expanding cubic polynomials into global time.
All old breakpoints are retained. In particular, every fast carrier and its propagator reset at every original macro-block boundary.
Summing (26)–(27) over the fixed number \(D\) of levels gives
\[ \|r^{(D)}\|_{L^\infty L^2} \le\|r^{(0)}\|_{L^\infty L^2}+C_DH_0^{-3}, \tag{30} \]
and
\[ \left\|\sum_{j=1}^D\beta_j\right\|_{L^\infty_*} \le C_DH_0^{-4}. \tag{31} \]
Choose \(K\), once, so that
\[ \|r^{(D)}\|_{L^\infty L^2}\le\frac14, \qquad \|b^{(D)}(\delta)\|_2\le\frac{\epsilon}{16}. \tag{32} \]
These are uniform choices: \(\epsilon\ge\rho^{-1}\), while \(H_0^{-4}=K^{-4}\rho^{-640}\).
No physical frequency or amplitude in this hierarchy depends on the binary length \(L\). Bit lengths are accounted for separately in Section 9.

**6. Preserving the macro-word through all the carrier loops**
This is the step that prevents a large accumulated-strain factor from reappearing.
Let \(I\) be an original macro-block and let \(P_I^0(t)\) be the inviscid propagator of the original carrier \(w\), starting from \(I\).
Define
\[ \mathcal T(t)=\mathcal P_D(t)\cdots\mathcal P_1(t), \qquad Q_I(t)=\mathcal T(t)P_I^0(t). \tag{33} \]
At the beginning of the macro-block,
\[ Q_I=I, \]
and at its end,
\[ \boxed{Q_I=W(s).} \tag{34} \]
This identity is exact because every fast factor is \(I\) at both endpoints.
By choosing the fixed small-\(s\) range and \(K\) appropriately,
\[ \|Q_I^{\pm1}\|_{H^m\to H^m}\le2, \qquad m=0,1,2. \tag{35} \]
Indeed, each fast factor has a bound
\[ \|\mathcal P_j^{\pm1}\|_{H^m\to H^m} \le e^{C_m|\chi_j|}, \]
and \(\sum_j|\chi_j|\le C_DH_0^{-5}\).
**6.1 Conjugated viscosity**
The supplied Laplacian commutator estimate also applies to each fixed finite Fourier direction \(\xi_\ell\):
\[ \|[\Delta,L_{\xi_\ell}]\|_{H^2\to L^2}<\infty. \]
Its bound is computed from the Fourier coefficients.
Telescoping through the product in (33) gives
\[ \|Q_I^{-1}\Delta Q_I-\Delta\|_{H^2\to L^2} \le C s+C\sum_j|\chi_j|. \]
The fixed choices can ensure
\[ \boxed{ \|Q_I^{-1}\Delta Q_I-\Delta\|_{H^2\to L^2} \le\frac1{16}. } \tag{36} \]
**6.2 The linear defect can be made smaller than viscosity**
Put
\[ b=b^{(D)}, \qquad \mathcal E(t)=Q_I'(t)Q_I(t)^{-1}+L_{b(t)}. \tag{37} \]
An \(H^2\to L^2\) estimate is sufficient. For fixed smooth fields \(F,G\),
\[ [L_F,L_G]:H^2\longrightarrow L^2 \tag{38} \]
has an explicit bound simply by composition:
\[ L_G:H^2\to H^1,\qquad L_F:H^1\to L^2. \]
Thus
\[ \|\operatorname{Ad}_{e^{-\chi L_F}}L_G-L_G\|_{H^2\to L^2} \le C|\chi|\,\|G\|_*, \tag{39} \]
for the small impulses used here.
To see the order of the estimates, let
\[ A_\ell=w+\sum_{j=1}^{\ell}\zeta_j,\qquad Q_\ell=\mathcal P_\ell\cdots\mathcal P_1P_I^0, \]
and define
\[ R_\ell=Q_\ell'+L_{A_\ell}Q_\ell. \]
Then
\[ R_0=0, \]
and direct differentiation gives
\[ \boxed{ R_\ell = \mathcal P_\ell R_{\ell-1} +[L_{A_{\ell-1}},\mathcal P_\ell]Q_{\ell-1}. } \tag{40} \]
The new impulse is charged against the amplitudes of earlier carriers, already bounded by its incoming envelope. Therefore
\[ \|R_\ell-R_{\ell-1}\text{ transported}\|_{H^2\to L^2} \le C H_{\ell-1}^{-5}H_{\ell-1} =CH_{\ell-1}^{-4}. \]
The remaining difference between \(A_D\) and \(b\) is \(\sum_j\beta_j\), which contributes only \(L_{\sum_j\beta_j}\).
It follows that
\[ \|\mathcal E\|_{H^2\to L^2}\le C_DH_0^{-4}. \tag{41} \]
Choose \(K\) so that
\[ \boxed{ \|\mathcal E\|_{H^2\to L^2}\le\frac{\nu}{64}. } \tag{42} \]
Again this is uniform because \(\nu\ge\rho^{-1}\).
No future carrier amplitude multiplies an earlier impulse in (40). No inverse of a long contracting word occurs.
**6.3 A stable global propagator for the reference coordinates**
Let \(S_0(t,r)\) be the original enlarged-family inviscid propagator. Define
\[ S_Q(t,r)=\mathcal T(t)S_0(t,r)\mathcal T(r)^{-1}. \tag{43} \]
Then
\[ \|S_Q(t,r)\|_{2\to2}\le8, \qquad S_Q(\delta,0)=W(s)^n. \tag{44} \]
The operators in (33)–(44) are used to estimate the original physical equation. They are not supplied as an extra physical advection.

**7. The nonlinear estimate and all weak realizations**
Apply the final emitted force \(f=f^{(D)}\), and put
\[ v=U-b,\qquad g=h+r^{(D)}. \]
The physical equation gives exactly
\[ v_t+L_bv=\nu\Delta v-B(v,v)+g. \tag{45} \]
On a macro-block, set \(v=Q_Iz\). Equations (37) and (45) imply
\[ \boxed{ z_t = \nu Q_I^{-1}\Delta Q_Iz -Q_I^{-1}B(Q_Iz,Q_Iz) +Q_I^{-1}g -Q_I^{-1}\mathcal E Q_Iz. } \tag{46} \]
Take
\[ \eta=\frac1{16\rho}. \]
By (32),
\[ \|g\|_{L^\infty L^2}\le\eta+\frac14<1. \]
**7.1 Absorption of the new defect**
Let
\[ E=\|z\|_{H^1}^2,\qquad Z=\|z\|_{H^2}. \]
The conjugated-viscosity error contributes at most
\[ \frac{\nu}{16}Z^2 \]
to the \(H^1\) energy.
By (35) and (42),
\[ \|Q_I^{-1}\mathcal E Q_Iz\|_2 \le4\frac{\nu}{64}Z, \]
so the linear defect contributes at most another
\[ \frac{\nu}{16}Z^2. \]
The same explicit Agmon estimate used in the supplied proof gives
\[ \|Q_I^{-1}B(Q_Iz,Q_Iz)\|_2 \le128E^{3/4}Z^{1/2}. \]
After the same Young inequalities, these two small errors leave
\[ \boxed{ E'+\frac{\nu}{4}Z^2 \le C_E\nu^{-3}E^3+C_E\nu^{-1}\|g\|_2^2, \qquad C_E=108\cdot128^4. } \tag{47} \]
The coordinate reset is still exactly \(W(s)\). Thus the supplied reset argument applies with the same \(1+O(s^5)\) loss per macro-block and gives
\[ \boxed{ \sup_{0\le t\le\delta}\|v(t)\|_{H^1}\le4M, \qquad \nu\int_0^\delta\|v(t)\|_{H^2}^2\,dt\le64M^2. } \tag{48} \]
Here \(b(0)=0\), because the original carrier, every new carrier, and every correction start at zero.
**7.2 Strong existence and the all-Leray–Hopf quantifier**
For each fixed compiler output and each actual disturbance, local \(H^1\) strong existence applies. The estimates above prevent the transformed norm, and therefore the physical \(H^1\) norm, from diverging during \([0,\delta]\): the prescribed reference \(b\) is finite and smooth in space.
The strong solution therefore continues throughout the active interval. Weak–strong uniqueness identifies every corresponding Leray–Hopf realization with it there. The standard strong-solution framework and uniqueness mechanism are the same ones used in the previous argument. <u>[virtualmath1.stanford.edu](virtualmath1.stanford.edu/~ryzhik/notes-256B-24.pdf?utm_source=chatgpt.com)</u>
No quantitative stability radius is extracted from a large uniqueness Grönwall factor. The quantitative disturbance estimate is already contained in (47).
**7.3 Endpoint estimate**
Using the generator of \(S_Q\), equation (45) becomes
\[ v_t = Q_I'Q_I^{-1}v +\nu\Delta v-B(v,v)+g-\mathcal Ev. \]
Variation of constants and (44) give
\[ \begin{aligned} v(\delta)-W(s)^nU_0 = \int_0^\delta S_Q(\delta,t) \bigl[ \nu\Delta v-B(v,v)+g-\mathcal Ev \bigr]\,dt. \end{aligned} \tag{49} \]
The defect term is controlled alongside viscosity:
\[ \int_0^\delta\|\mathcal Ev\|_2\,dt \le\frac{\nu}{64}\int_0^\delta\|v\|_{H^2}\,dt. \]
Using (48), a convenient conservative bound is
\[ \boxed{ \begin{aligned} \|U(\delta)-W(s)^nU_0\|_2 \le{}& \|b(\delta)\|_2 +128M\sqrt{\nu\delta}\\ &+3072M^2\delta^{3/4}\nu^{-1/4} +8\delta. \end{aligned}} \tag{50} \]
For \(\delta=(B_*\rho^8)^{-1}\), the three numerical error terms are at most
\[ 128B_*^{-1/2}\rho^{-3} + 3072B_*^{-3/4}\rho^{-15/4} + 8B_*^{-1}\rho^{-8}. \tag{51} \]
A fixed sufficiently large \(B_*\) makes their sum at most \(\epsilon/4\).
Combining (6), (32), and (50),
\[ \|U(\delta)\|_2 \le\frac{\epsilon}{4}+\frac{\epsilon}{4}+\frac{\epsilon}{16} =\frac{9\epsilon}{16}. \tag{52} \]
Set the force to zero after \(\delta\). The Leray–Hopf energy inequality gives, with the specified one-sided endpoint energy trace,
\[ \begin{aligned} \|U(\tau)\|_2 &\le\|U(\delta)\|_2+\eta(\tau-\delta)\\ &\le\frac{9\epsilon}{16}+\frac{\epsilon}{16}\\ &=\boxed{\frac{5\epsilon}{8}<\epsilon}. \end{aligned} \tag{53} \]
Starting the energy inequality at \(\delta\) is justified by strong continuity there, or by approaching through admissible starting times from below.

**8. The emitted compiler**
The online algorithm is finite and explicit:
Input: rational M, nu, tau, epsilon.

1. Compute rho, s, n, delta and eta.
2. Construct the rational enlarged-family pulse force f^(0).
3. Set H = K rho^160.

4. For j = 1,...,D:
     a. Refine every existing active-time interval into
        ceil(K H^6) equal cells.
     b. On each cell, evaluate f^(j-1) at its left endpoint.
     c. Apply the stored rational signed-quadratic certificate.
     d. Compute rational carrier amplitudes with certified
        quadratic-mean error.
     e. Emit eta_j + zeta_j' - nu hatDelta_j zeta_j
        in the next lower Fourier space.
     f. Set H = K H^32.

5. Express f^(D) in the twelve prescribed fundamental fields.
6. Append the zero-force interval (delta,tau].
7. Return the twelve coefficient functions and eta.
The compiler never needs to compute \(b^{(j)}\), \(\beta_j\), \(Q_I\), or any fluid trajectory. Their estimates justify the predetermined envelopes.
The higher-mode residual \(r^{(D)}\) is the mismatch of an analytical reference path; it is **not an additional applied force**. The physical force emitted in step 5 lies exactly in \(V_0\).

**9. Complete resource accounting
9.1 Numerical resources**
Solving the recurrence (29) gives
\[ H_D = K^{(32^{D+1}-1)/31}\, \rho^{160\,32^D}. \tag{54} \]
The final force obeys
\[ \sup_t\|f(t)\|_{W^{1,\infty}}\le C H_D, \]
and, since \(\tau\le1\),
\[ \int_0^\tau\|f(t)\|_{W^{1,\infty}}\,dt\le C H_D. \tag{55} \]
The interval count is also at most \(CH_D\). Every final time polynomial has degree at most \(3\).
Moreover,
\[ \eta^{-1}=16\rho\le32R. \tag{56} \]
The large exponent in (54) is fixed because \(D\) was computed from the fixed enlarged target family before receiving variable inputs.
**9.2 Rational precision and bit operations**
The numerical envelope \(H_j\) is kept separate from binary input length. This matters when an input rational has a long denominator but a bounded numerical value.
At a lowering step, the compiler uses only:
	•	rational polynomial evaluation;
	•	fixed rational linear maps and sign tests;
	•	rational subdivision of intervals;
	•	certified approximations of \(\kappa,\kappa^2\);
	•	rational square-root approximation;
	•	fixed-degree polynomial expansion.
The amplitude and Laplacian tolerances require \(O(\log H_j)\) precision bits, with fixed additive constants. For example, certified errors of order \(K^{-1}H_j^{-12}\) in the scalar approximations are more than sufficient for (14) and (18).
If \(B_j\) is the maximum bit length of a coefficient or breakpoint at stage \(j\), ordinary rational arithmetic gives
\[ B_{j+1}\le C(B_j+\log H_j). \tag{57} \]
Therefore
\[ B_D\le C_D(L+\log\rho+1). \tag{58} \]
Expanded global-time coefficients can be much larger numerically than the actual force on a short interval. Their bit lengths are still covered by (58), and the physical norm is governed by (55).
Using schoolbook integer arithmetic, a conservative bound for total computation, output, and memory is
\[ C_D(H_D+1)(L+\log\rho+1)^8. \tag{59} \]
**9.3 Fixed preprocessing and the constants \(A,p\)**
The preprocessing performs:
	1	The granted effective enlarged-family construction.
	2	Exact rational saturation until that fixed family is included.
	3	Extraction of all signed quadratic certificates.
	4	Construction of the finite Fourier support tables for the reference corrections.
	5	Calculation of spatial multiplication, Laplacian, and commutator bounds by finite Fourier coefficient estimates.
	6	Selection of \(B_*\) and \(K\) from the explicit inequalities above.
	7	Calculation of the resource constants and the integer exponent.
All searches in this list concern fixed data. Their termination follows from the granted enlarged-family construction and finite Fourier saturation. Their full operation counts, memory bounds, and descriptions are included in the fixed resource constant.
Choose
\[ \boxed{p=256\,32^{D+1}.} \tag{60} \]
It dominates \(160\,32^D\), the arithmetic exponents in (59), and the original enlarged-family resource exponent.
After enlarging the fixed integer \(K\) to dominate all fixed preprocessing and arithmetic constants, one may take, for example,
\[ \boxed{A=(2K)^{p^2}.} \tag{61} \]
Both are explicitly computable in the fixed preprocessing. The choices of \(K\) only require finite rational inequalities; all variable powers appearing in the error bounds decrease with \(\rho\), so their uniform smallness can be enforced once.
Using \(\rho\le2R\), equations (54)–(61) establish
\[ \begin{gathered} \text{bit operations, working-memory bits, total output bits,}\\ \text{interval count, polynomial degrees, and rational bit lengths} \le A(L+R)^p, \end{gathered} \tag{62} \]
and
\[ \eta^{-1},\qquad \sup_t\|f(t)\|_{W^{1,\infty}},\qquad \int_0^\tau\|f(t)\|_{W^{1,\infty}}\,dt \le AR^p. \tag{63} \]

**The completed implication**
The missing actuator-reduction step is supplied by the combination
\[ \boxed{ \begin{gathered} \text{signed quadratic Fourier certificates}\\ +\ \text{zero-integral carrier loops with exact linear resets}\\ +\ \text{small explicit reference corrections}\\ +\ \text{a linear defect absorbable by viscosity}. \end{gathered}} \]
This preserves the contracting macro-word at its endpoints while replacing every enlarged forcing direction through a fixed number of polynomial-cost stages.
The resulting prescribed force uses exactly the twelve admitted spatial fields, is independent of \(U_0\) and \(h\), and satisfies, for every admitted Leray–Hopf realization,
\[ \boxed{\|U(\tau)\|_2\le5\epsilon/8.} \]
Thus the full twelve-actuator polynomial-resource contract follows from the supplied constructive premises.
