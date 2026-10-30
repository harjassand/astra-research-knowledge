# Exact spectral first-exit flags and weighted multirecord receiving bounds
30 October 2026. Root working construction. This is a linear-map expansion of actual CP compressed propagators, NOT physical fault histories. Independent review and full growth instantiation remain required.

## 1. Exact triangular decomposition
Fix a finite selected set S of classical record blocks during one stage. Let P_j be commuting phase-basin projections, e.g. min(number of ones,number of zeros)<=delta n_j, and Q_j=I-P_j. Cuts for different records are disjoint. The actual full generator L has normal CPTP evolution and the complete-loss compressed propagators below are assumed well defined and CP/TNI.

For already-marked D subset S, let R=S\D, P_R=product_(j in R)P_j, and K_D(X)=P_R L(P_R X P_R)P_R on the P_R corner. For alpha subset R define

 E_alpha=product_(j in alpha)Q_j product_(j in R\alpha)P_j.

For nonempty J subset R define, on P_R-supported X,

 Gamma_(J|D)(X)=sum_(alpha union beta=J) E_alpha L(X) E_beta.

Then L(X)=K_D(X)+sum_(J nonempty)Gamma_(J|D)(X), EXACTLY. Each Gamma output is supported on P_(R\J) on both sides. It need not be positive or Hermiticity preserving individually. Its ket/bra off-diagonal sectors are retained.

Define triangular components v_D by

 v_empty(0)=rho0, v_D(0)=0 otherwise,
 v_D'=K_D(v_D)+sum_(nonempty J subset D) Gamma_(J|D\J)(v_(D\J)).

Every v_D stays supported in its remaining cuts. Summing equations gives (sum_D v_D)'=L(sum_D v_D); thus sum_D v_D is the actual state. A mark is retained even if the physical record later reenters its basin. No monitoring, collapse, independent trajectory, or positive record is asserted. This identity is finite linear algebra, with Duhamel interpretation for the declared normal propagators.

## 2. Local boundary strips and dropping weights
Let F_j=exp(s h_j), with h_j the physical phase-error count, and F_R=product_(j in R)F_j. Assume [F_j,P_j]=0 and F_j>=I. A local system leg changes at most q bits and touches at most q records. For a newly violated record j, its SOURCE on the corresponding ket or bra must lie in h_j>=delta n_j-q. Hence

 ||R_j F_j^(-1/2)|| <= exp[-s(delta n_j-q)/2].

In each Gamma ket/bra term, every j in J has such a source strip on at least one side. Retaining all other weights and using their local relative-congruence bound yields a complete weighted norm estimate of form

 ||Gamma_(J|D)||_(F_R -> F_(R\J))
 <= c_(J,D) exp[-(s/2)sum_(j in J)(delta n_j-q)].       (1)

For Hamiltonian and loss legs one side may remain in P throughout; the other still supplies the factor. Complete gain legs can put a record outside on both sides, which only improves the bound. General joint HP perturbations use a finite system-leg expansion, retaining bath coefficient maps and their cb norms. The physical nominal majority channel lies within one record, so its Gamma creates only one mark even though its read body may contain many fixed-degree sites. Bounded-body cross-record noise creates at most q new marks.

The weights are dropped ONLY for newly marked records. Their subsequent internal state may be arbitrary. This avoids trying to keep a wrong-consensus state under its former correct-phase potential.

The rate coefficients must satisfy a genuine incidence budget such as sum_(J containing j)c_(J,D)<=C n_j (nominal rates fixed) at each stage. It follows from the actual finite-body/per-site decomposition if all untouched bath-only terms vanish from Gamma; it is not a bound by the full unselected-device norm.

## 3. CP intervals and the joint norm, rather than marginal gentle sums
If K_D^*F_R<=a_R(t)F_R on its corner, CP gives

 ||T_D(t,s)||_(F_R(s) -> F_R(t))<=exp(integral_s^t a_R(u)du).

This is the complete weighted trace norm, so signed v_D may be propagated. For atomic expander majority, the nominal negative H drift plus local noise gives a_R<=C eta sum_(j in R)n_j inside the phase basin. QND quantum reads annihilate these classical phase weights. No spatial deletion of a majority dissipator is used: the actual generator is spectrally compressed as a whole.

Suppose a specified first-bad growth stage k_j has block size n_(k_j) and total earlier active site-time at most C0 n_(k_j), as in geometric growth with fixed-duration stages. Then the CP interval factor is exp[C eta C0 sum_j n_(k_j)]. The barrier factors in (1) can absorb this at sufficiently small fixed eta. Fixed-stage end tests can be inserted by the same exact good/bad projection decomposition, provided their real CP transition has the required weighted moment bound.

A useful abstract counting bound: after removing the barrier factors, an irreversible flag process with subset insertion rates c_J and sum_(J containing j) integral c_J<=C V_j has coefficient generating function bounded by exp(sum_J integral c_J z_J). Taking z_j=(1+C V_j)^-1 bounds the all-selected coefficient by exp(C|S|) product_j(1+C V_j). Thus, IF the preceding weighted comparisons are simultaneously valid, the inclusive all-selected bad norm has the form

 C^|S| product_j [(1+C n_(k_j)) exp(-c n_(k_j))].     (2)

Sum over possible first-bad stages independently in this nonnegative majorant. Since n_k grows geometrically, the effective parameter sum_k C(1+C n_k)exp(-c n_k) is uniformly small when the fixed seed size is large. No final-block-volume or number-of-growth-stages factor is needed.

This generating-function argument bounds norms of the exact signed expansion; it does not turn it into a positive physical error process. Rate budgets, stage transitions and initial weighted norms must be verified for the actual construction before (2) is used.

## 4. Scope still to earn
- Actual global phase moment transport through soft target reset, parameter sharpening, copy and change of stage cut; local rooted port moments alone are insufficient.
- Initial seed capture/common input module. Constant-size seed encoding can be included in the initial source circuit, but its joint error-support law must be stated.
- Exact integration with the quantum reference frame. Good classical phase labels may be retained coherently; if a record is marked bad, a proof may need to retain its last logical phase label. Copying a phase label into an ANALYTIC register and later coherently erasing it has a finite norm cost per marked record; it is not automatically a physical CP flag or a free immutable record. No factor exponential in ALL records is acceptable.
- Bounded-strength bad-record ports must be received by the actual hot-support quantum theorem; their internal states alone can be relegated to bath.
- A native majority compiler is a separate resource setting. The spectral-cut identity itself works for the declared atomic majority generator and does not require cutting its spatial dissipators.

The exact identity in section1 and local strip mechanism in section2 are the main proposed advance. The full staged capture and quantum-classical consumer are not established by this note alone.
