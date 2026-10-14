# FO quantum-response synthesis: exact dual currents, regularized observations, and scope gates

**Status: conditional mathematical results and finite internal checks; no capability or novelty claim.** The pinned N816 source packet is an unmerged PR84 snapshot and remains `source_derived_unreviewed`. This report reconstructs its principal derivation before evaluating connections to current N798/N810 and the incoming profile-circulation record. It does not promote any producer claim, physical input, priority, or computational advantage.

## Decision

The useful exact representation is the source-current (Thomson/Poisson) dual. For any factored positive operator $A=L^*L$, an explicit row vector $J$ with $L^*J=b$ certifies

\[
  \langle b,A^+b\rangle\leq \|J\|^2,
\]

without supplying a lower spectral gap. Exact feasibility also proves $b\perp\ker A$.

For N816's quantum target, the N810 transition instrument can, under exact ground-state preparation and energy-readout assumptions, estimate a regularized response $\chi_\eta$ from below without a gap. An exact N816 dual witness supplies an upper endpoint, so together they give a conditional interval. A fixed η observation cannot upper-certify the unregularized response uniformly: a two-level family makes $\chi_\eta$ tend to zero while χ diverges. On the matched AKLT N=6 fixture, even ideal regularized lower endpoints at tested η are much weaker than N816's exact primal-plus-Knabe interval; the sufficient shot counts are substantial and exclude the physical interface costs.

The profile-circulation source has an exact finite potential/cycle certificate, but its quartic profile action is not the quadratic response Hilbert space. Shared graph/coboundary vocabulary supplies no transfer. No map satisfying the necessary domain and norm identities was found.

## 1. Pinned inputs and evidence boundary

The active Capital checkout is pinned at `1c45f77e32d6fbd72483aed5014061c7bda4f372`; the concurrent unmerged PR84 snapshot is `5ddabf53324159aa6c88e4fef3b75bc7b8b6c4ff`; the Ultra source commit recorded by N816 is `e7ae999e957d70f98ccb9bd789c3eeb6c8229d30`. The current N816 source input is a separate snapshot, not Capital ancestry. Its intake records 167 source files (~67 MB), 54 selected copied files and only 28 readable critical text/code/result files. The selected-source manifest is SHA256 `2840a2c7b69afc4feeeb9b0d8f35274265c1b28559350c14145a4cd77d4f5eb2`; the principal derivation copied here has SHA256 `28c21589dabeb4b0e29bf09cb3864d5b9c87e5b1e708bf45cdc6eb2cc206ee6a`.

N798 and N810 are current scoped dossiers on the pinned Capital base. Both mark the relevant records `source_derived_unreviewed`; external correctness, novelty, and physical capability remain UNKNOWN. N798's acquired/supplied contract still requires globally valid source envelopes, whole-form lower domination, source/support coverage, and the stated normalization. N810's transition contract requires Gibbs preparation, an operator-norm bound, legal CP filtering, calibrated energy readout, and full preparation/evolution/readout costs. No physical material or quantum device input was acquired here. The pinned PR84 N816 dossier likewise says proof text is located but completeness is not audited; both its math and capability gates stay open.

## 2. N816 principal derivation reconstructed

Let $H=L^*L=\sum_j L_j^*L_j\geq0$ act on a finite-dimensional Hilbert space. Let $\psi$ be a zero-energy ground state, $Z=\langle\psi,\psi\rangle>0$, $V=V^*$, and

\[
 b=\left(V-\frac{\langle\psi,V\psi\rangle}{Z}I\right)\psi.
\]

When the ground state is isolated and nondegenerate, the coefficient of $\lambda^2$ in the ground energy of $H+\lambda V$ is $-\chi$, where

\[
  \chi=\frac{\langle b,H^+b\rangle}{Z};
\]

the second derivative is −2χ. This convention is material when matching a measurement formula.

For arbitrary $x$ and row vectors $w_j$ satisfying the exact source equation $\sum_jL_j^*w_j=b$, define

\[
  \ell(x)=\frac{2\operatorname{Re}\langle b,x\rangle-\langle x,Hx\rangle}{Z},\qquad
  u(w)=\frac{\sum_j\|w_j\|^2}{Z}.
\]

Then $\ell(x)\leq\chi\leq u(w)$, with exact gap

\[
 u(w)-\ell(x)=\frac1Z\sum_j\|w_j-L_jx\|^2.
\]

To see the kernel condition and upper inequality, write $y=H^+b$. Then $Ly$ is the orthogonal projection of every feasible row vector $w$ onto $\operatorname{Ran}L$: $w-Ly\in\ker L^*$, whereas $Ly\in\operatorname{Ran}L$. Thus $\sum_j\|w_j\|^2=\langle b,H^+b\rangle+\sum_j\|w_j-L_jy\|^2$. For any $z\in\ker H=\ker L$, exact feasibility gives $\langle z,b\rangle=\langle Lz,w\rangle=0$. Expanding $\|w-Lx\|^2$ proves the displayed gap identity and both variational bounds. In particular, exact feasibility itself proves source orthogonality to the *full* kernel; centering against one selected ground vector does not.

The N816 compact construction specializes $w_j=\sum_a c_{ja}L_jO_{ja}\psi$. With $a_{ja}=L_j^*L_jO_{ja}\psi$, $A_0$ the column map made from $a_{ja}$, $K=A_0^*A_0$, $g=A_0^*b$, and $h=\langle b,b\rangle$, solve $Kc_0=g$. Its exact least-squares residual is

\[
 \rho=h-g^*c_0=\|b-A_0c_0\|^2.
\]

If $\rho\ne0$, this dictionary returns UNKNOWN. If $\rho=0$, all feasible coefficients are $c=c_0+Tz$, with columns of $T$ spanning $\ker K$. Minimize the *physical row norm* $c^*Mc$, where $M$ includes cross terms between overlapping placements on the same physical row; solve $T^*MTz=-T^*Mc_0$ after exact dependent-column removal. The coefficient identity is not the norm. Fixed local dimension, MPS bond, width and dictionary size make contractions and exact rational elimination polynomial-bit under the encoded-input promises; no all-N feasibility, numerical stability, or practical-accuracy theorem follows.

A small residual does not replace exact membership or a coercive remainder: with $H=\operatorname{diag}(\varepsilon,1)$ and omitted source residual $r=\delta e_1$, the unaccounted response is $\delta^2/\varepsilon$, which is unbounded as $\varepsilon\downarrow0$. Thus N816 fails closed when $\rho\ne0$; it does not infer infeasibility of other dictionaries. Its successful coefficients can be chain-wide even though each row operator has fixed local support. The source also records that nearby-bond-only subsets fail at N=6.

The exact AKLT fixture uses integer-gauge spin-1 tensors, periodic parent projectors $P_2$, $b=S_z(0)\psi$, and $\|b\|^2/Z=2/3$. N=6 requires both three-site placements per bond; a right-placement-only dictionary has rank 71 and rank 72 after adjoining $b$, with a saved exact left-null witness. The corrected both-placement N=6 local-row upper is $159740147/109636215\approx1.45700165771$. Source reports exact response $287145511231/197956185875\approx1.45055083761$, a six-vector Krylov lower $\approx1.45033733557$, and exact feasibility at N=6 and N=12; N=20 is an older membership-only receipt with no optimized upper. The source explicitly corrects an earlier duplicated-row norm error. These remain scoped source claims, not an external review.

The decisive comparator is also in the N816 principal source: exact four-spin patch arithmetic is reported to prove $B^2\geq(2/5)B$, from which the established Knabe finite-size argument gives $H^2\geq H/10$ on the periodic ring for N≥6. Applying the same six-step primal and residual reportedly yields upper 1.45370374115 and interval width 0.00336640558, tighter than the local-row dual width 0.00666432214. I did not independently replay the patch LDL or derive the Knabe inequality; these comparator numbers are attributed source evidence. This removes the supposed advantage from “no gap supplied” on the tested fixture.

## 3. Exact source-current theorem: gap-free upper for a feasible source

**Theorem (finite-dimensional source-current upper).** Let $A=L^*L\succeq0$, let $b$ be a vector, and let $J$ satisfy $L^*J=b$ exactly. Then $b\perp\ker A$, and

\[
  \langle b,A^+b\rangle\leq\|J\|^2.
\]

For a matrix of loads $B$ and feasible row matrix $W$ satisfying $L^*W=B$, the Loewner bound is $B^*A^+B\preceq W^*W$.

**Proof.** Exact feasibility implies $\langle z,b\rangle=\langle Lz,J\rangle=0$ for $z\in\ker A=\ker L$. Put $J_*=LA^+b$. Then $L^*(J-J_*)=0$, so $J-J_*\in\ker L^*=(\operatorname{Ran}L)^\perp$, while $J_*\in\operatorname{Ran}L$. Hence

\[
 \|J\|^2=\|LA^+b\|^2+\|J-J_*\|^2
 =\langle b,A^+b\rangle+\|J-J_*\|^2.
\]

The matrix statement follows columnwise with the same orthogonal decomposition, giving the positive-semidefinite residual $(W-LA^+B)^*(W-LA^+B)$. No lower eigenvalue bound is used. This is the finite-dimensional Thomson/least-norm dual identity; its abstract content is established quadratic duality, not a novelty claim.

**Conditional N798 use.** N798's source/form comparison gives

\[
 \tau_\theta=\frac{\langle w,A_\theta^{-1}w\rangle}{\langle w,1\rangle}
 \leq \frac{\langle u,A_-^{-1}u\rangle}{Z_\ell},
 \quad Z_\ell=\langle\ell,1\rangle>0,
\]

under its supplied global envelopes $\ell\leq w\leq u$, lower-form domination, positivity-preserving inverse and source coverage. If the retained comparison form admits an **exact supplied factor** $A_-=L_-^*L_-$ in the same weighted Hilbert space and one can construct/verify $L_-^*J=u$, then

\[
    \tau_\theta\leq\frac{\|J\|^2}{Z_\ell}.
\]

Thus one can replace a numeric coercivity/gap computation for this source by an exact source-current witness. The theorem just proved is finite-dimensional. A continuum or unbounded N798 realization additionally needs a closed-form/domain argument showing $J$ is in the adjoint domain and $L_-^*J=u$ holds in the stated weighted space. The original envelope, whole-form comparison, positivity, retained source normalization, and exact current construction remain mandatory; this does not make the global physical envelopes free and does not lift the N798 review/capability gates. For multiple retained loads the upper is the matrix $W^*W/Z_\ell$ if the same normalization is valid for the load family.

For a weighted grounded graph $A=D^*CD+K$, with positive edge conductances $C=\operatorname{diag}(c_e)$ and nonnegative killing $K=\operatorname{diag}(k_i)$, a physical edge current $q$ and sink allocation $s$ yield a feasible row witness if

\[
  D^*q+s=b,\quad s_i=0\text{ whenever }k_i=0.
\]

Its squared row norm is $\sum_e q_e^2/c_e+\sum_{i:k_i>0}s_i^2/k_i$. The condition is a direct exact certificate; for graphs with a simple explicit current it can avoid an inverse or a spectral gap. It may be difficult to find the current on general graphs, and solving its minimum-energy problem is itself equivalent to the original Poisson problem.

### Exact grounded-path algorithm and matched cost

Take $n$ interior vertices, $n+1$ positive rational conductances $c_0,\dots,c_n$, Dirichlet endpoint potentials, $A=D^*CD$, and rational source $b_1,\dots,b_n$. Set

\[
 S_0=0,\quad S_i=\sum_{j=1}^i b_j,\quad
 C_0=\frac{\sum_{i=0}^n S_i/c_i}{\sum_{i=0}^n1/c_i},\quad
 q_i=C_0-S_i.
\]

At vertex $i$, $(D^*q)_i=q_{i-1}-q_i=b_i$, hence $q$ is feasible. Among all feasible $q+r$, $D^*r=0$; the cross term vanishes because $q_i/c_i$ is a potential drop at the minimizing current. Therefore

\[
 b^*A^{-1}b=\min_{D^*q=b}\sum_i q_i^2/c_i
 =\sum_i q_i^2/c_i.
\]

For every trial potential $v$, with edge drop $Dv$, the exact gap is

\[
 \sum_i q_i^2/c_i-(2b^*v-v^*Av)
   =\sum_i (q_i-c_i(Dv)_i)^2/c_i.
\]

The expression is implemented with exact `Fraction` arithmetic in `path_flux_check.py`. It checks unit paths $n=1,\ldots,8$, where $b_i=1,c_i=1$ gives $b^*A^{-1}b=n(n+1)(n+2)/12$, and a nonuniform five-vertex rational instance with conductances $(1,2,3,5,7,4)$, source $(1,2,1/2,3,2)$, and response $152217/8152$. The check verifies source divergence, equality to an exact Gaussian solve, and the primal-current gap identity. This validates those finite executions only.

Both the current formula and direct tridiagonal exact solve use $O(n)$ arithmetic operations and storage on the path (integer bit growth depends on rational input and intermediate denominators). The current is a transparent feasible witness and is useful when an inverse is inaccessible; it is not faster on this matched path baseline. On N798 hidden, retained, or continuum operators, no exact local current for the specific $u$ has been supplied in this work. Applying this theorem there remains a **candidate connection** until a source witness and equal-cost strongest comparison are produced.

## 4. Quantum regularized observation: valid lower, not a gap-free upper

Specialize N810's bounded transition instrument to an exact pure ground state $\psi$ of $H\geq0$ and the centered observable $B=V-\langle\psi,V\psi\rangle/Z\,I$, with known $a\geq\|B\|>0$. Assume $b=B\psi\perp\ker H$; a unique ground state suffices, while a degenerate ground space needs exact source-kernel orthogonality. Prepare $\psi$, apply the CP instrument $K_s=B/a$, $K_f=(I-B^2/a^2)^{1/2}$, then measure the energy change $d=E_m-E_0\geq0$ on success. Assign zero on failure or $d=0$, and output

\[
  Y_\eta=a^2\frac{d}{d^2+\eta^2},\quad\eta>0.
\]

Writing $p_m=|\langle m|B|\psi\rangle|^2/Z$, the success probability for outcome $m$ is $p_m/a^2$. Therefore

\[
 \mathbb E Y_\eta
 =\sum_{E_m>E_0}p_m\frac{E_m-E_0}{(E_m-E_0)^2+\eta^2}
 =:\chi_\eta\leq\chi.
\]

Equivalently, $\chi_\eta=Z^{-1}\langle b,H(H^2+\eta^2I)^{-1}b\rangle$.

If $b\perp\ker H$, monotone convergence of the nonnegative spectral terms gives $\chi_\eta\uparrow\chi$ as $\eta\downarrow0$. The random variable is bounded by $a^2/(2\eta)$, since $d/(d^2+\eta^2)\leq1/(2\eta)$. For $n$ independent complete trials Hoeffding gives the sufficient bound


\[
 n\geq\frac{a^4}{8\eta^2\epsilon_{\rm stat}^2}\log\frac{2}{\delta}
\]

using $a^2/(2\eta)$ as the range ceiling. This estimates $\chi_\eta$ with failure probability at most $\delta$ and additive statistical tolerance $\epsilon_{\rm stat}$. To use it as a lower endpoint for $\chi$, subtract finite-resolution, preparation and instrument error bounds from the empirical mean. Under N810's stated nondemolition readout and total-variation contracts, this half-normalized output has readout bias at most $a^2L\zeta$ (where $L=3/\eta^2$ in the zero-temperature limit) and state-preparation/instrument-label error at most $[a^2/(2\eta)](\delta_{\rm prep}+\gamma+2\kappa)$. A noisy energy measurement is admissible only under its nondemolition/function-of-$H$ contract.

Combining with any exact feasible dual witness $J$ for $H=L^*L$ gives a conditional interval

\[
 \max\{0,\overline Y_\eta-\epsilon_{\rm stat}-\epsilon_{\rm sys}\}
 \leq\chi\leq\|J\|^2/Z.
\]

No spectral gap is required for either endpoint. The upper still requires exact input/factor/witness acquisition; the lower still requires the actual ground-state preparation, centered observable filter, energy readout and resolution at the selected η. The interval width can only approach “dual upper minus χ” as η shrinks, and there is no uniform rate without a source-specific low-energy bound. A finite-time or finite-resolution implementation may not reach a desired width.

**Fixed-$\eta$ no-go.** For $H_g=\operatorname{diag}(0,g)$, $\psi=|0\rangle$, and $V=\sigma_x$, one has $\chi=1/g$ and $\chi_\eta=g/(g^2+\eta^2)\to0$ as $g\downarrow0$, for every fixed $\eta>0$. Thus a fixed regularized observation is not an upper bound and cannot uniformly recover or upper-certify the unregularized response over a family with an arbitrarily closing source-visible gap. At $g=0$, the source enters the kernel and the nondegenerate response target ceases to apply. Exact dual feasibility excludes that case by proving $b\perp\ker H$, but does not bound the positive spectrum away from zero.

**N=6 numerical diagnostic.** The owned `hybrid_check.py` rebuilds the copied AKLT projector matrix and performs a float64 eigensolve in the 141-dimensional $S_z=0$ sector. It reproduces the reported spectral $\chi$ to about $3.5\times10^{-15}$, but this is a floating finite-model diagnostic, not an exact proof or a simulated quantum instrument. With $a=1$, results are:

| η | $\chi_\eta$ estimate | χ-$\chi_\eta$ | Safe Hoeffding trials for 0.001 absolute error, 95% |
|---:|---:|---:|---:|
| 1.00 | 0.253289 | 1.197262 | 461,110 |
| 0.50 | 0.621408 | 0.829143 | 1,844,440 |
| 0.25 | 1.060510 | 0.390041 | 7,377,759 |
| 0.10 | 1.366084 | 0.084467 | 46,110,994 |
| 0.05 | 1.428281 | 0.022269 | 184,443,973 |

For comparison, N816 reports exact source response $\chi\approx1.45055084$ and its same six-step primal plus exact acquired Knabe-gap upper $1.45370374$ (width $0.00336641$). At η=0.05, even the ideal hybrid population lower leaves width about 0.02872 to the reported local-row upper, before statistical or instrument error. Those shot counts exclude ground-state preparation, filtering, calibrated global energy readout, η-resolution, control, calibration, noise, failures' runtime, and reset costs. The matched finite comparator already supplies a tighter interval without those quantum measurement costs. This comparison does not show no future acquired quantum interface can help.

## 5. Incoming profile-circulation: a real duality theme, no transfer theorem

The incoming `PROFILE_CIRCULATION.md` reports an exact rank-one convex quartic profile-loop Bregman identity, a zero signed-moment result, and a finite profile graph certificate over 32,805 directed edge/width actions. It reports 104 negative raw strips but no negative cycle, so an exact action potential telescopes on closed walks. It is a profile/action result with a quartic energy and a finite specified graph. N816/N798 response is a Hilbert-space quadratic form with a Poisson source equation and a resistance/current norm. A potential difference around a cycle and a least-energy current under divergence constraints are both cochain/cycle dual patterns, but that does not identify their domains or objective functions.

The transfer would require an explicit map taking profile states/actions to the response state space and proving: (i) the profile action gradient is the same source (b) or (u); (ii) the cycle-closed potential is a feasible (L^*J=b) row witness; and (iii) the profile cost dominates the response row norm in the correct direction with exact scaling and boundary conditions. No such map or inequality appears in the incoming report; the quartic action cannot be silently substituted for the quadratic metric. Classification: **candidate representation analogy only; application incompatible on current evidence**. The profile source's own graph certificate remains scoped to its finite profile model.

## 6. Matched cost and strongest baseline ledger

| Operation | Input/interface actually required | Certificate/output | Dominant costs and strongest matched baseline | Current result |
|---|---|---|---|---|
| N816 compact dual completion | Exact rational FF local factors, exact MPS tensors, centered source, fixed-width dictionary | If exact residual ρ=0, exact physical-row norm upper; else UNKNOWN | Polynomial-bit rational MPS contractions and solve at fixed (d,D,R,s); compare same AKLT input with same six-vector primal plus exact four-site/Knabe coercivity certificate | Valid conditional computation; matched baseline gives narrower N=6 interval. No all-N or acquired-material claim. |
| N798 source-current substitution | Existing global ℓ/u envelopes, lower-form comparison, (Z_\ell>0), exact (A_-=L_-^*L_-), exact current (L_-^*J=u) | τ≤‖J‖²/(Z_\ell), no numerical gap | Cost to construct/verify J must be counted; retained sparse solve, N798 tensor residual/spectral counter, source-aware local-window and static-condensation baselines receive same model and envelopes | Conditional theorem only; no N798 current/input assembled or benchmarked here. |
| Ground-state transition lower | Exact ground prep, centered $B$, known $a\geq\|B\|$, CP filter, nondemolition calibrated energy measurement, chosen $\eta$ and systematic contracts | Lower endpoint for $\chi_\eta\leq\chi$; combined with exact dual upper gives interval | $O(a^4/(\eta^2\epsilon^2)\log(1/\delta))$ safe raw shots under a loose bounded range, plus all state/filter/readout/resolution/control costs; compared against exact AKLT primal+Knabe | Conditional interface; tested eta values do not beat exact finite comparator. |
| Grounded path flow | Rational path, positive conductances, rational b, Dirichlet endpoints | Exact response = exact minimum-energy feasible current | Both flow and best tridiagonal direct solve are O(n) arithmetic/storage; report input bit growth and all setup/check costs | Exact code checks finite cases; no speed or asymptotic advantage. |
| Profile-cycle potential | The finite profile graph/action catalogue and its quartic profile model | Exact finite closed-cycle nonnegativity/potential certificate as reported by incoming source | Graph construction/action-cost acquisition and independent proof review not done here; response Hodge current is not the same target | No transfer to N816/N798 established. |

## 7. Sources, uncertainty, and decisive next gate

The conventional prior-art boundary is substantial. MPS Hylleraas response predates this packet (Sharma & Chan, [arXiv:1408.5092v1](https://arxiv.org/abs/1408.5092), [DOI 10.1063/1.4895977](https://doi.org/10.1063/1.4895977)). Dynamical response from ground-state transitions/phase estimation is also established (Sakuma et al., [arXiv:2404.19554v2](https://arxiv.org/abs/2404.19554), Phys. Rev. A 110, 022618, [DOI 10.1103/PhysRevA.110.022618](https://doi.org/10.1103/PhysRevA.110.022618)). Rall's block-encoding framework includes linear-response estimation and explicitly treats state preparation as a resource assumption ([arXiv:2004.06832v3](https://arxiv.org/abs/2004.06832)). These sources rule out framing generic MPS variational response or spectral transition observation as new. The focused checks recorded below are not exhaustive novelty searches.

The next decisive mathematical/application test is narrow: on a **current N798 retained model with its actual supplied $u,A_-$**, either produce an exact structured current $J$ and verify $L_-^*J=u$, or prove a precise obstruction to a bounded-width/bit-size current under that interface. Charge envelope acquisition, exact factor construction, current search, exact checking, and compare the resulting interval with the best N798 local-window/tensor/static-condensation baselines on the identical source, accuracy, representation, and all-in cost. If current construction merely solves the same full Poisson system at the same cost, stop the claimed capability direction. Separately, a quantum follow-up requires a genuinely acquired finite system where the exact local-row dual upper beats the best same-input gap/residual/SDP bound and an executable ground-state/filter/energy-readout interface with full costs. Refining $\eta$ on the current AKLT fixture is not that test.

Overall result: the exact source-current dual is the strongest reusable mathematical representation found in this lane. Its application to N798 is conditional; the profile-circulation and quantum measurement links do not create an established cross-domain advantage. N816 stays NOT_ACHIEVED / REDESIGN; N798/N810 review, capability, physical acquisition and novelty remain UNKNOWN/open.
