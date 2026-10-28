# Astra Pro3 — Acquiring global nonlinear response operations from passive rank-one interventions

**27 October 2026.** Independent continuation of Pro3's reusable-learning role. These results concern exact or noise-bounded **synthetic mathematical sources**, not laboratory apparatus, newly discovered physical laws, verified novelty, or general causal discovery. The source classes, observation calls, compatibility guarantees, and important failures are separated below. Source scripts, observations, and read-only checkers are saved as actual files alongside this note.

## 1. Scientific question and strongest result

The earlier Pro3 programme reconstructed a positive sparse pair-interaction graph and an affine two-anchor factorial quotient from Schur boundary reactions. An added fourth-order interaction forced a justified rejection. Its successor learned a one-dimensional nonlinear intervention family under a **supplied** third-derivative bound, but did not warrant unknown directions or the supplied bound physically.

The current continuation first proves a derivative and 126-coordinate transfer contract from **passive affine-conductance structure** (Section 2). Its stronger construction then **acquires the entire nonlinear response of a rank-one affine network**, with no supplied actuator-family labels, interaction signs, sparsity, finite polynomial degree, state-space rank, or specified future histories (Sections 3–6). It uses only exact native boundary scalar readings; the lack of robustness to bounded noise is genuine and important.

In an executed 128-control, four-node synthetic grounded network, the stronger compiler needed **510 native scalar reactions**: one baseline, 256 singleton, and 253 paired reactions. It discovered centered latent rank two and predicted 50 *later-specified* histories exactly, including simultaneous nonzero activation of all 128 controls. All 510 reactions, all 8,256 distinct hidden Gram entries, and the 50 transfers were separately verified by determinant/cofactor calculations. A shifted-reference variant recovered a 128-control model with an **initially dark** actuator, discovered rank three, again using 510 calls, and predicted the original zero-dose state and 49 other unseen histories exactly. This latter call count is fixture-specific: the new rank emerged at the final actuator, so did not increase earlier pair tests.

No claim of superiority over an equally informed Nyström/active-kernel or inverse-network learner is made. The gain here is a particular operational transition within Astra: **scalar physical experiments → a source-compatible, compact reusable nonlinear response operator → new mixed interventions without the source**.

## 2. Physically warranted curvature and approximate control transfer

### 2.1 Physical interface

For a grounded passive conductance operator, suppose

\[
Q(u)=Q_0+\sum_{i=0}^{n-1}u_iV_i,\qquad Q_0\succeq L\succ0,\qquad V_i\succeq0, \qquad u_i\ge0,
\]

with a single measured boundary reaction obtained from the Schur complement of \(G(u)=Q(u)+\frac32e_0e_0^T\):

\[
R(u)=\frac32+\frac1{Z(u)},\qquad Z(u)=e_0^TQ(u)^{-1}e_0.
\]

The learner receives **R only**. The lower physical matrix \(L\) and actuator norm bounds are independently warranted specifications, not a handed-over microscopic source. The source can contain unknown internal conductances. The specified positive-semidefinite affine dependence is stronger than passivity alone; the earlier nonlinear Schur-compatible fixture was **not** proved to satisfy it.

Define \(\zeta=e_0^TL^{-1}e_0\) and \(\tau_i=\|L^{-1/2}V_iL^{-1/2}\|_2\). For an affine intervention direction \(D=\sum d_iV_i\), let \(\tau_D=\|L^{-1/2}DL^{-1/2}\|_2\). The resolvent identity yields, for any sequence of \(k\) actuator directions,

\[
\left|\partial_{d_1}\cdots\partial_{d_k}Z(u)\right|
 \le k!\zeta\prod_{j=1}^k\tau_{d_j}. \tag{1}
\]

**Proof.** Differentiating \(Q^{-1}\) produces the sum of the \(k!\) ordered products of \(k\) direction matrices and \(k+1\) copies of \(Q^{-1}\). After conjugating by \(L^{1/2}\), \(0\prec L^{1/2}Q^{-1}L^{1/2}\preceq I\) because \(Q\succeq L\). Every term is bounded by \(\zeta\prod\tau\), including when some directions have negative coefficients; only the *physical evaluation points* must have positive-definite \(Q\).

Choose two anchors at doses \(A=1/20\), a modifier line \(xV_X+(B-x)V_Y\) with \(B=1/10\), and a four-corner factorial contrast

\[
f(x)=\frac{Z(A,A,x,B-x)-Z(A,0,x,B-x)-Z(0,A,x,B-x)+Z(0,0,x,B-x)}{A^2}.
\]

The double fundamental-theorem-of-calculus integral in the anchor amplitudes and (1), with directions \(V_a,V_b,V_X-V_Y\), prove

\[
\boxed{\sup_{x\in[0,B]}|f'''(x)|\le120\zeta\tau_a\tau_b\tau_{X-Y}^{3}.}\tag{2}
\]

This bound needs no known quadratic coefficient, sign, global polynomial degree, or sparsity promise. It *does* require fixed affine conductance matrices and the independent lower spectral certification. The physical source might have a much smaller true derivative: the bound is conservative but sound.

### 2.2 Global transfer from physically similar controls

Suppose a known hardware map assigns any actual modifier \(j\) to a prototype \(p(j)\) and independently bounds

\[
\|L^{-1/2}(V_j-V_{p(j)})L^{-1/2}\|_2\le\eta_j.
\]

For any allowed modifier history \(w\), let \(Pw\) sum its doses within prototype families, without changing the anchor doses or total modifier dose. Applying the three-direction version of (1) along the straight path from \(Q(w)\) to \(Q(Pw)\), which stays in the positive-definite cone, proves

\[
\boxed{|H(w)-H(Pw)|\le 6\zeta\tau_a\tau_b\sum_j\eta_jw_j.}\tag{3}
\]

This is a physically warranted *operator-distance transfer certificate*, not a claim that the native measurements discover the hardware map. It tolerates signed, arbitrarily high-order nonlinearities in the factorial response of the affine inverse source.

An exact-rational four-node test with 126 modifiers and two certified prototype families produced:

- Nine prototype factorial settings, costing **36 native scalar R reactions** (four four-corner reactions each), under correlated raw sensor error at most \(10^{-8}\) and independently assumed affine drift in the reciprocal instrument reading. The \((+,-,-,+)\) chronological four-corner arrangement annihilates that drift.
- An independent physical derivative bound \(K=122.305945877\ldots\), without knowing the actual internal matrices or response curvature.
- A global full-dose operator-transfer radius \(\mathcal E=0.0002919064002\ldots\).
- **100** later random multi-coordinate histories independently enclosed by local quadratic-interpolation uncertainty plus \(\mathcal E\), with largest observed verification-only midpoint error \(3.88897395\times10^{-6}\).
- **20** later arbitrary nonnegative linear per-lag cost objectives compiled without source calls. A cost-aware robust policy derived pessimistic and optimistic lag-specific prices \(c_j\pm 6\zeta\tau_a\tau_b\eta_j\), optimizing the certified lower response against all possible unknown actuator deviations. Its largest guaranteed global regret was \(0.000613474115\), versus \(0.000627439806\) using a uniform tube. The mean certificate improvement was \(2.5959\times10^{-5}\).

These are results from a **different**, reconstructed affine-conductance network, not a replay of the unavailable original archived nonlinear source. The guarantee applies to full modifier dose \(B=1/10\), both anchors fixed at \(1/20\), that passive source and its physical similarity specifications; it is not a global causal law for arbitrary time histories.

### 2.3 Two decisive identical-transcript failures

At all 36 measured prototype reactions, two independently constructed alternative passive sources reproduce the observations **exactly**. Replacing one unmeasured shunt by another valid PSD shunt while removing the assumed hardware-similarity guarantee changes a later factorial response by **0.117525538**. Retaining PSD passivity and the hardware families but permitting a compactly activated \(C^3\), non-affine port conductance \(a b\,256t^4(1-t)^4\) between historical dose settings produces a later factorial change **0.297597335**. Thus neither similarity nor affine dependence follows from passivity plus a finite successful test record. They are independent engineering premises that must be warranted.

## 3. Stronger theory: exact global response learning with rank-one actuators

### 3.1 Contract

Assume a *fixed* but unknown positive-definite real matrix \(Q_0\) and *unknown* physical vectors \(v_1,\ldots,v_n\) such that

\[
Q(u)=Q_0+\sum_i u_iv_iv_i^T, \quad Z(u)=e^TQ(u)^{-1}e,
\quad R(u)=\tfrac32+1/Z(u),
\]

for arbitrary nonnegative histories with \(\sum_i u_i\le\delta=1/5\). **Each native call returns one exact rational scalar R**; it has no finite instrument error or uncalibrated drift. The learner knows only this rank-one positive-semidefinite source *class* and physical dose language, not the vectors, microscopic dimension, Gram rank, similarity classes or response law.

For the first version assume every source-port coupling

\[
h_i=e^TQ_0^{-1}v_i\ne0. \tag{4}
\]

Section 5 removes the zero-reference form of this requirement for physically relevant actuators by acquiring at a generic illuminated reference. Rank-one is a genuine structural assumption; not every passive actuator is rank-one, and an arbitrary unknown nonlinear \(Q(u)\) is excluded.

### 3.2 A source-native, entirely observable Gram representation

Put \(b=Q_0^{-1/2}e\), \(a_i=Q_0^{-1/2}v_i\), \(z_0=b^Tb\), and \(P_i=(b^Ta_i)^2=h_i^2>0\). Normalize \(t_i=a_i/h_i\), so \(b^Tt_i=1\), and decompose

\[
t_i=b/z_0+s_i,\qquad b^Ts_i=0.
\]

The **centered Gram**

\[
S_{ij}=s_i^Ts_j,
\qquad T_{ij}=t_i^Tt_j=1/z_0+S_{ij}
\]

is positive semidefinite, and \(\mathrm{rank}(S)\le \dim(Q_0)-1\). All signs of vector couplings are represented in \(T_{ij}\), despite every physical actuator being PSD. In particular, there is no positivity assumption on the *interaction coefficients*.

Woodbury's identity, for any support where the doses are positive, gives

\[
\boxed{Z(u)=z_0-\mathbf1^T\!\left[\mathrm{diag}\!\left(\frac1{u_iP_i}\right)+T_{\mathrm{supp}(u)}\right]^{-1}\!\mathbf1.}\tag{5}
\]

Zero doses are handled by restricting the support. Therefore the observed baseline \(z_0\), positive singleton strengths \(P_i\), and centered Gram \(S\) determine **every future allowable mixed response**, without recovering the microscopic vectors or a physical mechanism. This is an identifiable *operational quotient* of all compatible sources, not microscopic identification.

### 3.3 Singleton acquisition from two nonnegative doses

For a one-coordinate experiment of dose \(t>0\), Sherman–Morrison yields

\[
L_i(t):=z_0-Z(te_i)=\frac{tP_i}{1+t\alpha_i},\qquad
\alpha_i=a_i^Ta_i=P_iT_{ii}.
\]

Consequently

\[
\boxed{\frac1{L_i(t)}=\frac1{tP_i}+T_{ii}.}\tag{6}
\]

Two exact native scalar observations at distinct positive doses recover \(P_i\) and \(T_{ii}\), provided (4) holds. Both must be charged: **\(2n\) native reactions**, plus one common baseline. The physical source is not giving the learner \(L_i\) directly; it gives \(R\), converted exactly into \(Z\) by \(Z=(R-3/2)^{-1}\).

### 3.4 One paired experiment suffices under PSD-adaptive excitation

With singleton parameters already acquired, fix distinct positions \(i,j\) and two nonnegative simultaneous doses \(u,v>0\). Define

\[
A=T_{ii}+\frac1{uP_i},\quad B=T_{jj}+\frac1{vP_j},
\quad t=T_{ij},\quad \ell=z_0-Z(ue_i+ve_j).
\]

The inverse of the observed two-by-two Woodbury block gives

\[
\boxed{\ell=\frac{A+B-2t}{AB-t^2}.}\tag{7}
\]

The unknown signed interaction \(t\) solves a quadratic,

\[
\ell t^2-2t+(A+B-\ell AB)=0.
\]

At most two algebraic roots exist, and an arbitrary large-dose experiment may not distinguish them. However the Gram PSD property implies \(|t|\le\sqrt{T_{ii}T_{jj}}\). Choose the experimenter's *known, positive* doses adaptively so that

\[
0<u\le\min\left(\frac\delta2,\frac1{P_i(M+1)}\right),\quad
0<v\le\min\left(\frac\delta2,\frac1{P_j(M+1)}\right),
\quad M=\max(T_{ii},T_{jj}).
\tag{8}
\]

Then \(A,B>M\ge\sqrt{T_{ii}T_{jj}}\). On the whole physically feasible interval,

\[
\frac{\partial\ell}{\partial t}
=-\frac{2(A-t)(B-t)}{(AB-t^2)^2}<0.\tag{9}
\]

Thus exactly **one** of the two quadratic roots is physically admissible and \(T_{ij}\) is acquired by *one* paired native scalar observation, without assuming the interaction sign. The centered-PSD constraint \((T_{ij}-1/z_0)^2\le (T_{ii}-1/z_0)(T_{jj}-1/z_0)\) supplies a further physical consistency check. A contradictory record must return `UNKNOWN` or `CONTRACT_REJECTED`, not a fictional source law. In exact rational arithmetic the correct discriminant square root is rational; the executed programme checks this exactly.

The earlier working two-pair inversion used **763** native readings on the same source. The single-pair, PSD-adaptive construction reduces the calls by **253**, without changing the exact source class or later result. This reduction uses positivity of the *physical Gram*, not positivity of signed causal interactions.

### 3.5 Adaptively discover the latent rank without a supplied rank cap

Set \(S_{ij}=T_{ij}-1/z_0\) and retain the acquired \(S_{ii}\). Start with no landmark columns. For each actuator \(i\), obtain one pair measurement against every existing landmark, giving column \(c_i=S_{L,i}\) and landmark block \(W=S_{L,L}\). Calculate

\[
\rho_i=S_{ii}-c_i^TW^{-1}c_i.\tag{10}
\]

Since \(S\) is PSD, \(\rho_i\ge0\). The Gram-vector distance from actuator \(i\) to the landmark span is exactly \(\rho_i\):

- If \(\rho_i>0\), promote \(i\) to a new independent landmark. Old vectors already proved to lie in the earlier span can be extended into this column by a known inner product, requiring **no rereading of old actuators**.
- If \(\rho_i=0\), the vector is **proved** to lie in that span. Its inner products with any future vector are already determined by its coordinates; retain them.

At the end every vector lies in the discovered span, and the *entire* centered Gram is uniquely determined:

\[
\boxed{S_{ij}=c_i^TW^{-1}c_j.}\tag{11}
\]

This is exact PSD Nyström completion, not a heuristic rank truncation. Its zero residuals are sound **because of the assumed PSD source class and exact observations**, not because finite experimental success certifies arbitrary physical rank. If there are \(r\) discovered landmarks among \(n\) actuators, no more than \(nr-r(r+1)/2\) distinct pair targets are necessary for this sequential procedure, each now costing one scalar reaction. The total exact-source budget obeys

\[
\boxed{1+2n+nr-r(r+1)/2}\tag{12}
\]

for nonzero port couplings. If rank grows with \(n\), the benefit disappears. The generic model has approximately \((r+1)n-r(r-1)/2+1\) free real parameters; that **parameter count is context, not an unconditional lower bound** for all adaptive exact-real query models.

### 3.6 Compile arbitrary later interventions with only an r-by-r inverse

The retained object is \((z_0,P_i,c_i,W)\), not a dense 128-by-128 source matrix. For a future input, let

\[
d_i=u_iP_i,\quad s=\sum_i d_i,\quad q=\sum_i d_ic_i,\quad H=W+\sum_i d_ic_ic_i^T.
\]

The block Schur complement of the port-aligned Gram coordinates gives

\[
\boxed{Z(u)=\frac{z_0^2}{z_0+s-q^TH^{-1}q}.}\tag{13}
\]

Each subsequent permitted history costs \(O(nr^2+r^3)\) arithmetic and an \(r\times r\) inverse, with **zero** source calls. Rational bit complexity, retained coefficients and hardware arithmetic are additional costs, not hidden free resources.

For the fixed 128-actuator synthetic source, the algorithm discovered \(r=2\) with landmarks at indices 0 and 1. It used **1 baseline + 256 singleton + 253 paired = 510** scalar reactions. Fifty subsequently generated histories, including one using all 128 interventions, were answered **exactly**, without a further native reading. The separate verifier recomputed **all 510** native Schur reaction scalars by determinant ratios, independently reconstructed **8,256** entries of the actual source Gram, and checked all fifty compiled responses against the hidden four-node network. These validations are finite checks of an algebraic theorem whose stated generality comes from the proof, not the number of checks.

## 4. Source assumptions, information and comparison

The learner does **not** acquire arbitrary nonlinear histories. It acquires a complete operational law for a declared *fixed rank-one affine positive-definite source with exact calibrated scalar observations*. Its known physical source class is substantial: finite-dimensional SPD response, exact repeatability, rank-one PSD actuators, no unmodeled nonlinear dependence or drift, and—in the zero-reference variant—nonzero native source-port couplings.

The result handles arbitrarily high polynomial orders in the **resulting rational response** without reconstructing those interactions term by term. It permits signed cross-interactions because off-diagonal Gram entries are signed. An equally informed retaining algorithm can implement Woodbury, kernel reconstruction and adaptive Nyström and tie its source calls. This is **not** a claim to historical priority for inverse network identification or Nyström methods. Relevant precedents include Drineas and Mahoney, *On the Nyström Method for Approximating a Gram Matrix for Improved Kernel-Based Learning* (JMLR 2005), https://jmlr.csail.mit.edu/beta/papers/v6/drineas05a.html, and Lawler and Sylvester, *Determining Resistances from Boundary Measurements in Finite Networks* (SIAM 1989), https://doi.org/10.1137/0402019. The additional formulation here is the charged one-port dose-limited observation and the observable centered Gram compiler.

## 5. The stronger continuation: illuminating initially invisible actuators

A serious failure of zero-reference singleton identification is \(h_i=0\). Consider a two-dimensional source with \(Q_0=I\), port \(e=(1,0)\), dark actuator \(v_d=(0,1)\), and bright actuator \(v_b=(1,1)\). The dark actuator has \(Z(te_d)=1\) for **every** dose \(t\), yet with both actuators at dose 0.1 it changes the port response by \(-0.0006361323155\ldots\) compared with the bright actuator alone. Rejecting every zero-singleton actuator as irrelevant would be unsound.

### 5.1 Generic positive reference theorem

The coupling

\[
h_i(w)=e^T\left(Q_0+\sum_jw_jv_jv_j^T\right)^{-1}v_i
\]

is a **real-analytic rational function** of \(w\) throughout the positive-definite control domain. If actuator \(i\) is relevant to any admissible source reaction, \(h_i\) cannot vanish identically: \(\partial Z/\partial w_i=-h_i(w)^2\), so identical vanishing would make the scalar response independent of that actuator on the connected domain. A nonzero real-analytic function has a zero set of Lebesgue measure zero. Since there are finitely many actuators, a reference chosen from an absolutely continuous distribution on a full-dimensional open set of small, positive feasible controls will, **with probability one**, make every globally relevant actuator's coupling nonzero simultaneously.

Now perform the rank-one acquisition *relative* to this actual physical reference \(w_*\), measuring native controls \(w_*+\Delta\) with \(\Delta\ge0\) and a reserved dose margin. The acquired operator represents \(Q(w_*)\) and the unchanged actuator vectors. For a later physical admissible history \(w\), the **computational displacement** \(\Delta=w-w_*\) can have negative coordinates; the actual physical requested \(w\) still has only nonnegative controls. Woodbury's identity is algebraically valid for the signed displacement because \(Q(w)\succ0\); the orthogonal Schur block in (13) remains positive definite and the compiled prediction remains exact. Thus the learner can transfer back to **the zero-dose state** even though it acquired at a positive reference.

This almost-sure statement is not a finite-grid sampling guarantee, not a bound on the number of samples needed to locate a numerically *well-conditioned* reference, and not a proof from observing a single rational seed. Truly globally irrelevant controls can be omitted only when irrelevance is otherwise proved; a deterministically failed positive seed should return `UNKNOWN` or prompt another seed.

### 5.2 Actual initially dark execution

The source was altered to include a rank-one PSD actuator at lag 127 of the form \(v_d=e_3-c e_0\), with rational \(c\) selected so \(e_0^TQ_0^{-1}v_d=0\) exactly. All original singleton measurements of this actuator at zero baseline are identical to the no-intervention response. A dense **rational** reference using total physical dose \(1/20\) was chosen, and its actual effectiveness independently checked. Acquisition singleton and adaptive pair probes never exceeded the total physical dose \(1/5\). The acquired rank became three, but that third direction entered only at the last index, so the actual cost was again **510** reactions. There was no requirement that the zero-dose response be measured during acquisition.

Fifty later physical histories were answered **exactly**, including the no-intervention source, the originally dark actuator alone, its combined action with another actuator, and all 128 simultaneously activated. This required relative **signed arithmetic**, not negative physical interventions. A second independent checker reproduced **510** actual physical reactions, **8,256** centered Gram entries, and all **50** mixed predictions by source-native determinant ratios. The synthetic reference was an explicitly verified *rational instance*, not evidence that arbitrary finite random seeds are safe.

## 6. Decisive precision floor

**No finite noisy experiment establishes the exact Gram equalities for an unrestricted continuum of compatible real source parameters.** Even on the original, truly rank-one passive synthetic source, changing one recorded paired native \(R\) by \(+5\times10^{-9}\) (within the stated hypothetical \(10^{-8}\) bounded-error allowance) causes the exact two-pair consistency identity \(g_{ij}^2=k_{ij}^2/(P_iP_j)\) to fail. It also shifts one recovered off-diagonal kernel entry by about \(1.9673\times10^{-4}\). A learner that insists on exact identities for noisy observations would **falsely reject the true physical source**. The one-pair rational-discriminant method is equally an exact-data construction: with noise its algebraic square root need not be rational, and an interval rather than a unique exact coupling is warranted.

The shifted-source dark actuator illustrates the excitation problem quantitatively. After illumination its singleton coupling squared was only about \(1.41618\times10^{-7}\). Its raw native change at added dose 0.05 was approximately \(1.97432\times10^{-8}\), *below* the \(2\times10^{-8}\) indistinguishability separation for two adversarial sensors each bounded by \(10^{-8}\). At dose 0.1 the change is larger, but precise global Gram reconstruction still requires an explicit noise-aware feasibility and conditioning analysis. Repetition alone cannot remove unknown **adversarial correlated** errors.

The right next mechanism is a **PSD-consistent interval Gram learner**. Once landmark entries and diagonal Schur complements are enclosed, Cauchy–Schwarz supplies

\[
\big|S_{ij}-c_i^TW^{-1}c_j\big|\le\sqrt{\rho_i\rho_j}
\tag{14}
\]

for every actual PSD completion, where \(\rho_i=S_{ii}-c_i^TW^{-1}c_i\ge0\). This is exact for known entries, and can be combined with sound interval arithmetic or semidefinite feasibility when entries are uncertain. **The work here has not yet executed a full globally sound noisy interval compiler**, and no noisy analogue of the 510-call global result is claimed. In ill-conditioned or insufficiently excited cases `UNKNOWN` is necessary. The earlier 36-call derivative/tube operation remains a separate *actual noise-enclosed* partial learner under a stronger hardware-similarity contract.

## 7. Preserved substantive source material

The executable files and saved outputs below are ordinary reproducible scientific artifacts in the current conversation working directory. No Astra GitHub repository mutation was performed.

- `astra_passive_transfer.py`, `astra_passive_transfer_results.json`: 36-call source-dependent derivative certification, 100 unmeasured histories and 20 task-conditioned robust control designs.
- `astra_passive_independent_verify.py`, `astra_passive_independent_verify_results.json`: independent 36 raw Schur observations, 100 history checks and 20 task checks.
- `astra_passive_limits.py`, `astra_passive_limits_results.json`: identical-transcript similarity and non-affine source counterconstructions.
- `astra_rankone_global_acquisition.py`, `astra_rankone_global_acquisition_results.json`: first working two-pair 763-call complete-source compiler.
- `astra_rankone_independent_verify.py`, `astra_rankone_independent_verify_results.json`: independent complete 763-reaction source verification, Gram and future transfer checks.
- `astra_rankone_one_pair.py`, `astra_rankone_one_pair_results.json`: improved 510-call single-pair PSD-feasibility compiler.
- `astra_rankone_one_pair_independent_verify.py`, `astra_rankone_one_pair_independent_verify_results.json`: independent full 510-reaction and 8,256-entry native verifier.
- `astra_rankone_precision_obstructions.py`, `astra_rankone_precision_obstructions_results.json`: bounded-noise false exact-rejection and a previously dark interaction.
- `astra_rankone_shifted_global.py`, `astra_rankone_shifted_global_results.json`: positive-reference illumination, relative signed compiler and genuinely dark-actuator source.
- `astra_rankone_shifted_independent_verify.py`, `astra_rankone_shifted_independent_verify_results.json`: independent 510 reaction, 8,256 Gram and signed-deployment verification.

The original handoff and previously mounted source files remain unchanged. **Scientific standing:** conditional mathematical proofs and independently replayed synthetic capability. **Not established:** real instrument use, finite-sensor-precision global identification, arbitrary nonlinear/source-drifting transfer, historical priority, or civilisation-level capability in practice.
