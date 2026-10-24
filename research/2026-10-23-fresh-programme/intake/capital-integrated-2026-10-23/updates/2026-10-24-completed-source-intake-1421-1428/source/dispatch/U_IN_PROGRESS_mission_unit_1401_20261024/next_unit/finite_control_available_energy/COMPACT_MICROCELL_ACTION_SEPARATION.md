# Compact microcell action separation

Status: FROZEN; root full internal governing-source review and independent second-Sol full review passed on the reviewed predecessor ff75f6268d2c610f143f287501af26942b93edc483ccf926e7b6edb1f672e2bf. This is internal proof review, not external certification or physical validation. The exact fixed-workspace routing lemma below is part of the proof, not an inference from an unweighted orbit-closure theorem. Priority is UNKNOWN. This is a statement about prescribed classical phase-space Hamiltonians; the fixed-slew, fixed spatial-library, mechanical/electromagnetic implementation gate remains OPEN.

## 1. The operation and the resource it separates

Use the fixed standard canonical coordinates \((q,p)\in\mathbb R^2\times\mathbb R^2\), Euclidean metric and symplectic form. Put

\[
C=[-1,1]^4,\qquad \rho_0=\tfrac1{16}\mathbf1_C,
\qquad H_b=\tfrac12\sum_{j=1}^2\nu_j(q_j^2+p_j^2),
\quad \nu_1>\nu_2>0.
\]

Let

\[
a=(\nu_2/\nu_1)^{1/4},\quad A=\operatorname{diag}(a,a^{-1}),
\quad T(q,p)=(Aq,Ap),\quad \rho_T=\tfrac1{16}\mathbf1_{T(C)}.
\]

The map \(T\) preserves volume and is not symplectic unless \(a=1\). It is a comparator for the target density, not an asserted canonical map.

**Theorem.** There is one compact set \(K\), depending only on \(a\), such that for every \(d,\eta>0\) a smooth compactly supported Hamiltonian path \(G_t\), flat near both time endpoints, has flow \(\phi_t\) satisfying

\[
\operatorname{supp}G_t\subset K,\qquad
\phi_t(C)\subset K\quad(0\le t\le1),
\]
\[
\int_0^1\bigl(\max G_t-\min G_t\bigr)\,dt<\eta,
\qquad \|\phi_{1*}\rho_0-\rho_T\|_1<d. \tag{1}
\]

The generator's supremum norm can also be made arbitrarily small. The common compact set does not grow as \(d,\eta\downarrow0\).

Consequently a fixed bulk bare-energy decrease is compatible with action tending to zero:

\[
E_0=\frac{\nu_1+\nu_2}{3},\qquad
E_T=\frac{2\sqrt{\nu_1\nu_2}}3,\qquad
W_*:=E_0-E_T=\frac{(\sqrt{\nu_1}-\sqrt{\nu_2})^2}{3}>0. \tag{2}
\]

The target is not claimed to be the full Gardner optimum. The result separates integrated Hamiltonian amplitude from deformation/resolution: it is not a low actuator-energy or fixed-bandwidth claim.

## 2. A torus rearrangement with a fixed momentum workspace

Write \(\mathbb T^2=\mathbb R^2/\mathbb Z^2\), and \(B=[-1,1]^2\). For every \(s>0\) there is a smooth Hamiltonian path \(h_t(Q,P)\) on \(\mathbb T^2\times\mathbb R^2\), flat near its time endpoints, whose time-one map \(\psi\) obeys

\[
\|\mathbf1_{\psi(\mathbb T^2\times B)}-
\mathbf1_{\mathbb T^2\times AB}\|_1<s. \tag{3}
\]

Moreover, every \(h_t\) is supported in one fixed momentum box \(P\in[-R_*,R_*]^2\), where \(R_*\) depends only on \(A\), not on \(s\). Its norms, derivatives, path length and lifted winding may depend on \(s\).

Here is a literal construction of the support assertion. Choose an integer \(R>2+\max(a,a^{-1})\), use mesh side \(h=1/N\) on the torus and on \([-R,R]^2\), and take every mesh slot, including zero-density slots. Replace each four-dimensional cell by its concentric guarded core of side \((1-\theta)h\), \(0<\theta<1\). The two sets in (3) have equal volume. Their boundary cells have total volume \(O_A(h)\). Matching source and target interior occupied cells, and extending that matching to a permutation of all slots, therefore mismatches only \(O_A(h)\) volume. Removing all guards costs \(O_R(\theta)\) volume. It suffices to implement this finite core permutation exactly.

Perform the following Hamiltonian motions of the tracked cores.

1. Move each core center \((Q_i,P_i)\) to \((Q_i,4P_i)\), by the simultaneous path \((Q_i,\lambda P_i)\), \(1\le\lambda\le4\), keeping each core's shape. Cores with different \(Q\) centers remain separated in a \(Q\) coordinate. Cores with the same \(Q\) center remain separated by their expanding momentum-center spacing. All separations have positive guard margins.
2. About each new center apply the local canonical linear map \((\Delta Q,\Delta P)\mapsto(\Delta Q/2,2\Delta P)\). During this deformation, distinct \(Q\) slots have spacing \(h\) and \(Q\)-width at most \((1-\theta)h\); cores in a common \(Q\) slot have momentum spacing \(4h\) and momentum width at most \(2(1-\theta)h\). They remain disjoint. At the end, core widths are \((1-\theta)h/2\) in each \(Q\) coordinate and \(2(1-\theta)h\) in each \(P\) coordinate.
3. Permute these separated rectangles using one spare momentum-grid slot just outside the finite occupied grid. A vacancy means an untracked slot, not an empty region of phase space. Each permutation cycle can be effected by parking its first tracked core there, shifting the other cycle members into the successive vacancies, and returning the parked core.
4. Undo the local canonical squeeze about the final centers, and then contract all momentum centers from \(4P_i\) back to \(P_i\). The same separation estimates apply in reverse.

The routing in step 3 has a direct corridor proof. Move a core first from its \(Q_1\) center to an adjacent half-grid value. Its distance from every other \(Q_1\) grid center there is \(h/2\), whereas the sum of the two core half-widths is \((1-\theta)h/2\). That entire half-grid hyperplane is free of all stationary tracked cores. On it, adjust \(Q_2,P_2\) to their target values and \(P_1\) to a half-grid value adjacent to the vacant target momentum slot. A momentum half-grid hyperplane has distance \(2h\) from every momentum center, while the sum of the corresponding half-widths is \(2(1-\theta)h\). Holding that momentum coordinate fixed allows \(Q_1\) to move to its target center. Finally enter the vacant target along \(P_1\). At the entry and exit legs, different remaining grid coordinates separate every other core. Periodicity of \(Q_1\) causes no obstruction. One exterior spare slot and these corridors fit in a momentum box, for example \([-4R-10,4R+10]^2\), independent of \(N,\theta\).

Every motion just used has a smooth ambient Hamiltonian realization. A translation has a linear Hamiltonian on a neighborhood of the moving core. A local canonical squeeze has a quadratic Hamiltonian there. Multiply by smooth bumps equal to one on the tracked core and a positive collar, with support disjoint from the other tracked cores. Finite positive guard clearances permit such collars throughout each motion. For the simultaneous stretches the supports are disjoint; for routing only one core moves at a time. A local torus chart suffices on each core and collar, splitting a path into finitely many chart intervals if needed. All supports stay in the fixed momentum box. Smooth time schedules, flat at concatenation endpoints, preserve the exact core motions. Derivatives may be large but are finite at each chosen \(N,\theta\).

Thus the ambient map is injective and maps every tracked core to its prescribed target core. Untracked gap material cannot enter a target tracked core, and all source gap mass is bounded by the removed-guard volume. Taking \(h,\theta\) small proves (3). Smooth compact momentum support also confines every trajectory with initially bounded momentum to that fixed box or its unchanged initial momentum. This proves the workspace lemma without assigning a uniform derivative or action bound to the fast map.

## 3. Conformal microcells and the first stage

Lift \(h_t\) periodically to \(\mathbb R^2_Q\times\mathbb R^2_P\). Its lifted flow commutes with integer translations in \(Q\). For a fixed selected \(h\), both forward and inverse lifted \(Q\) displacements are uniformly bounded by some finite \(M_h\): its derivatives are bounded on the compact torus/momentum support. Outside that momentum support the flow is the identity.

The noncanonical coordinate scaling \(F_\epsilon(Q,P)=(\epsilon Q,P)\) is conformally symplectic, \(F_\epsilon^*\omega=\epsilon\omega\). Accordingly

\[
G^q_{\epsilon,t}(q,p)=\epsilon h_t(q/\epsilon,p)
\]

has equations \(\dot q=\epsilon h_P,\ \dot p=-h_Q\) and flow exactly \(F_\epsilon\psi_tF_\epsilon^{-1}\). It changes macroscopic \(q\) by at most \(\epsilon M_h\), while its momentum may change by order one. Its amplitude and integrated oscillation are multiplied by \(\epsilon\).

Choose \(\epsilon M_h<1\), and multiply this generator by a fixed smooth cutoff in \(q\), equal to one on \([-2,2]^2\) and supported in \([-3,3]^2\). Every trajectory starting in \(C\) under the uncut lift remains in that unit-cutoff region, so uniqueness makes the cutoff flow identical on the entire stock, including gap material. The generator is now compactly supported. Its oscillation is no larger than \(\epsilon\operatorname{osc}h_t\), because the fast compactly supported generator's range contains zero.

Let \(f_h(Q,p)=\mathbf1_{\psi(\mathbb T^2\times B)}(Q,p)\). Away from a \(q\)-boundary layer of thickness \(O(\epsilon M_h)\), the physical output density is

\[
\tfrac1{16}\mathbf1_B(q)f_h(q/\epsilon,p).
\]

The boundary-layer error tends to zero in \(L^1\), since momentum stays in the fixed box and density is bounded by \(1/16\). For any bounded periodic integrand with this fixed compact momentum support, integration over the \(q\) rectangle converges to its torus average: tile the rectangle by full \(\epsilon\)-cells and bound its remaining boundary cells by their volume. Thus

\[
\limsup_{\epsilon\downarrow0}
\|\phi^q_{\epsilon*}\rho_0-ho_1\|_1
\le\tfrac{|B|}{16}\,
\|f_h-\mathbf1_{\mathbb T^2\times AB}\|_1,
\quad
\rho_1=\tfrac1{16}\mathbf1_B(q)\mathbf1_{AB}(p). \tag{4}
\]

First choose the fast approximation (3), then choose its microperiod. Equation (4) therefore supplies arbitrary first-stage accuracy. It does not assume a uniform excursion bound over an accuracy-varying family of fast maps.

## 4. Dual stage, composition and common compactness

Apply the same workspace lemma through the canonical coordinate swap \((q,P)\mapsto(P,-q)\): explicitly, from a selected path \(\widetilde h_t\) of Section 2 take \(k_t(q,P)=\widetilde h_t(P,-q)\). This generator is periodic in \(P\), compact in \(q\), and approximately replaces \(\mathbf1_B(q)\) by \(\mathbf1_{AB}(q)\) when the fast momentum phase is uniform. The sign does not change these sets because \(B\) and \(AB\) are centrally symmetric.

The dual lift

\[
G^p_{\zeta,t}(q,p)=\zeta k_t(q,p/\zeta)
\]

has equations \(\dot q=k_P,\ \dot p=-\zeta k_q\). Its macroscopic momentum displacement is at most \(\zeta M_k\). Choose a fixed momentum cutoff equal to one on the first-stage support box plus a unit margin. Choosing \(\zeta M_k<1\) makes that cutoff exact on the whole first-stage stock. The complementary \(q\) coordinate is confined by the fixed fast support box. The rectangle-tiling argument used in (4), now on \(AB\) in momentum, proves arbitrary second-stage accuracy on the product input \(\rho_1\). Incomplete cells at its possibly incommensurate edges have vanishing volume.

Hamiltonian pushforward is an exact \(L^1\) isometry. Hence the error from the first stage is not amplified by the second, however large its derivatives:

\[
\|\phi^p_{\zeta*}\phi^q_{\epsilon*}\rho_0-\rho_T\|_1
\le \|\phi^q_{\epsilon*}\rho_0-\rho_1\|_1
+\|\phi^p_{\zeta*}\rho_1-\rho_T\|_1. \tag{5}
\]

For a requested accuracy choose both fast maps first. Their complementary-coordinate support boxes depend only on \(A\), while their finite periodic-coordinate excursions and norms may depend on the accuracy. Choose \(\epsilon,\zeta\) afterward so that (5) is below \(d\), both scaled excursions are below a unit margin, and

\[
\epsilon\int\operatorname{osc}h_t\,dt+
\zeta\int\operatorname{osc}k_t\,dt<\eta. \tag{6}
\]

The same choice makes both generator suprema as small as desired. Concatenate the two flat-ended paths, rescaling their time intervals; Hamiltonian length is additive and invariant under positive time reparametrization. Their supports lie in one fixed phase-space box. A compactly supported smooth Hamiltonian flow cannot carry any trajectory out through the exterior region where its vector field vanishes. This includes all untracked gap material. Enlarge the fixed box slightly to obtain \(K\). This proves (1), including the common trajectory region and the no-outlier quantifier.

## 5. Energy, linear passivity and a literal cyclic control

The stock has mean zero and covariance \(I_4/3\), giving (2). For a linear symplectic matrix \(S\), let \(r_{q_j},r_{p_j}\) be its canonical output rows. Their symplectic inner product is one, so

\[
1\le\|r_{q_j}\|\|r_{p_j}\|,
\qquad \|r_{q_j}\|^2+\|r_{p_j}\|^2\ge2.
\]

Therefore

\[
E(S_*\rho_0)=\tfrac16\sum_j\nu_j
(\|r_{q_j}\|^2+\|r_{p_j}\|^2)\ge E_0. \tag{7}
\]

The energy decrease in (2) is thus unavailable to every linear canonical map. It does not imply that the input is thermally passive or free to prepare.

Both endpoint densities in (1) are supported in the same compact set, so

\[
|E(\phi_{1*}\rho_0)-E_T|
\le \|H_b\|_{L^\infty(K)}d. \tag{8}
\]

A prescribed cyclic Hamiltonian \(H_b+V_t\), with \(V\) returning smoothly to zero, can implement the same limiting energy change with small integrated control oscillation. This requires explicitly allowing arbitrary phase-space-dependent control, including a bare-Hamiltonian counterterm. To see the ledger literally, enclose all compact generator supports in a fixed Euclidean ball and take \(\chi=1\) on a larger ball, with compact support. Bare \(H_b\) flow is a pair of orthogonal rotations and preserves these balls.

For a small \(\lambda>0\), first ramp \(V\) smoothly from zero to \(-\chi H_b\) over time \(\lambda\). On the stock this is a short rescaled bare rotation. On the next interval of length \(\lambda\), use

\[
V_t=\chi\bigl(\lambda^{-1}G_{(t-\lambda)/\lambda}-H_b\bigr). \tag{9}
\]

On the stock the total Hamiltonian is exactly the compressed compact generator. Finally ramp \(-\chi H_b\) back to zero over time \(\lambda\). Flat-ended \(G\) and flat ramp schedules make the control smooth. Choose the microperiods after \(\lambda\) so that \(\|G\|_\infty\le\lambda\). Then \(\|V\|_\infty\) is bounded by one plus a fixed compact bound for \(H_b\), uniformly in accuracy and duration. Its integrated oscillation tends to zero with \(\lambda\).

The on-ramp rotates the finite-perimeter initial cube by \(O(\lambda)\), so its initial-density error is \(O(\lambda)\) in \(L^1\). Pushforward through the central map preserves that norm exactly; no pointwise or derivative-amplified error claim is needed. The off-ramp preserves bare energy. All trajectories, including initial perturbation mass, stay in the fixed ball. Equations (5) and (8) therefore retain the limiting energy drop \(W_*\). A final \(L^1\) target statement also follows because the short bare rotation of the rectangular target changes it by \(O_A(\lambda)\).

For this literal prescribed cyclic control, Liouville's equation gives the exact signed particle-work identity

\[
\int dt\int\rho_t\,\partial_tV_t\,dz
=E_{\rm final}-E_0. \tag{10}
\]

Thus negative work on the particles approaches \(-W_*\). The control returns to its baseline; the stock does not. Preparation and state reset are additional resources. No autonomous load, controller efficiency or repeatable engine is constructed.

This separation does not rely essentially on the cube's sharp boundary. Choose once a compact smooth product density, identical and even in all four coordinates, sufficiently close to \(\rho_0\) in \(L^1\). Its covariance is \(cI\), so (7) still forbids linear canonical extraction. Common compactness bounds the change in the work contrast between the two inputs by \(2\|H_b\|_\infty\) times their \(L^1\) distance, uniformly over the constructed maps. A fixed sufficiently close smooth stock therefore retains a fixed positive decrease, for example \(W_*/2\), while action tends to zero. No Gaussian tail extension is used.

## 6. What is paid, and what is not inferred

Each instance has finite smooth controls. Across the sequence there is no uniform spatial derivative, temporal slew, phase-space resolution or fixed primitive-library bound. The cyclic realization (9) uses momentum-dependent control and cancellation of the bare kinetic energy. Its small amplitude–time area is not a bound on \(\partial_tV\), force, electromagnetic field energy, generator loss, or the work in (10).

A fast map that is itself mechanical admits a different exact scaling: \(h=P^2/2+\sum u_j(\tau)V_j(Q)\) becomes \(H=p^2/2+\sum u_j(t/\epsilon)V_j(q/\epsilon)\) over duration \(\epsilon T\). That preserves the kinetic coefficient but changes the spatial wavelengths and temporal modulation. It supplies no fixed-slew or fixed-library implementation of the present composite operation. The existing mechanical controllability theorem likewise gives no inherited action/excursion bound.

Small Hofer length does not mean convergence of these maps to a non-symplectic map in \(C^0\). The convergence asserted here is of transported densities in \(L^1\). Nor does it assert exact displacement of any fixed-capacity ball. Those missing conclusions are why ordinary Hofer nondegeneracy and exact displacement-energy lower bounds are not contradicted.

The operation is a classical resource separation. The finite-slew, physical mechanical/electromagnetic, preparation, autonomous load and reset gates are unacquired. No fusion, device advantage or mission-achievement claim follows.

## 7. Primary ancestry and internal dependencies

[Kazandjian–Pozzoli–Sigalotti, arXiv:2509.24960v2](https://arxiv.org/html/2509.24960v2), Theorems 3, 7 and 9, supplies the strong Hamiltonian orbit-closure and finite mechanical-library controllability ancestry. Its topology/cost statements alone do not provide the common-workspace/action conclusion here. [Schlenk, *On a Question of Dusa McDuff*, IMRN 2003](https://libra.unine.ch/server/api/core/bitstreams/59a5c261-d6d9-4ee0-9d0e-c942793c57bf/content), Theorems 1.2 and 2.4, already establishes strong geometric effects at arbitrarily small Hofer distance; its specified output is a slice-area functional, not this density/energy target with a common compact workspace. The bounded comparison did not establish priority of the present joint statement. **Priority remains UNKNOWN.**

Bounded internal checks and completed full-source reviews:

- [Conformal lift algebra](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/finite_control_available_energy/luna_resolvent_algebra/AMPLITUDE_ACTION_SCALING_AUDIT.md) and [compact-stock linear audit](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/finite_control_available_energy/luna_resolvent_algebra/COMPACT_STOCK_LINEAR_AUDIT.md).
- [Common support and cyclic work check](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/finite_control_available_energy/luna_boxcar/COMPACT_SUPPORT_AND_CYCLIC_WORK_CHECK.md), conditional there on the routing lemma supplied explicitly in Section 2 here, and the [literal Sections 5–6 readback](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/finite_control_available_energy/luna_boxcar/COMPACT_MICROCELL_SECTIONS5_6_READBACK.md).
- [Hofer/density primary boundary](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/finite_control_available_energy/luna_random_lag_sources/HOFER_SMALL_DENSITY_ORBIT_CHECK.md).
- [SinglePort's literal Sections 2–4 readback](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/finite_control_available_energy/luna_single_port/COMPACT_ROUTING_READBACK.md) passed the guarded-core corridor widths, ghost vacancy, support, homogenization and composition quantifiers; its requested explicit canonical-swap formula is included above. Root independently reconstructed the guarded-core route and checked the compact energy and cyclic \(L^1\)-error bookkeeping before this source was written.

Root and the independent second Sol (`/root/proof_audit`) both read the full reviewed predecessor and passed the guarded-core routing, whole-isotopy lift/cutoff bounds, inverse-density formula, strong absolute-error homogenization, dual composition, common workspace, cyclic-control ledger and smooth-stock extension. All four existing bounded readbacks were retained. The final change is review status only; the exact reviewed predecessor is preserved in `reviewed_predecessors/COMPACT_MICROCELL_ACTION_SEPARATION.ff75f6268d2c610f143f287501af26942b93edc483ccf926e7b6edb1f672e2bf.md`.

All preceding frozen sources are unchanged. No numerical fixture, optimization or external experiment is used in this proof.
