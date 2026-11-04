# Adaptive finite-bath Schur certificate: a materially better practical gate

2026-11-03. Mathematical mechanism derived and independently checked. Numerical values are exploratory floating-point tests, not an interval-certified continuum calculation. This is a potentially useful certification layer for optimized bath/NRG methods, not a demonstrated faster solver or a new invention of Schur complements.

## Result

The enormous uniform localization depth is unnecessary for *a posteriori* spectral certification when a small selected bath passes a computable complement-energy gate. For the U=4, Delta=1, D=2, Gamma=0.5 superconducting Anderson benchmark, a retained bath of 12 spin modes (total Fock dimension 16384) passes the gate up to excitation 0.8: complement lower-bound candidate lies 0.998997 above the retained ground. Lower/upper Schur matrices both have three low levels below the 0.8 threshold (ground doublet plus singlet). The isolated singlet absolute-energy interval has width 0.002079 from this inexpensive version. These conclusions use numerically observed eigenvalues and need certified matrix arithmetic before being called certificates. The 16-spin-mode test completed in 110.94 seconds (full Fock dimension 262144): ground interval candidate [-2.183242395495,-2.183242383671], singlet interval candidate [-1.647861709560,-1.647657250438], and excitation interval candidate [0.535380674111,0.535585145057], width 0.000204471. Thus the numerical Schur gate reaches the requested 0.001 energy tolerance with 16 bath spin modes. Complement clearance is q-mu0=0.998999960641 and the 0.8-window count sandwich again agrees on three levels. Full-Fock construction was resource-heavy; symmetry-restricted implementation is the next necessary improvement. These are not rigorous numerical certificates until quadrature, ground lower bounds and eigenvalue-index validation are paid.

## Exact finite-bath theorem

Let h be positive and bounded, split one-particle space into a retained K containing the impurity source and its complement:

h = [[A,T*],[T,D]].

Let P be the Fock projection onto tail vacuum; Q=1-P. Use graded tensor conventions for fermionic impurity modes. The finite retained Hamiltonian is H_K=dGamma(A)+V. For any 0<=s<inf spec D define

A_eff(s)=A-T*(D-s)^(-1)T,
q_s=e_min(dGamma(A_eff(s))+V)+s.

A lower bound on the finite ground energy can replace the exact value, preserving validity. By completing a positive square,

h >= A_eff(s) direct-sum s I.

Second quantization preserves this inequality; adding V gives H >= H_eff(s) tensor I+s N_tail. Since N_tail>=1 on Q, QHQ>=q_s Q. This controls all hopping terms surviving inside Q; simply replacing QHQ by an independent tail Hamiltonian would be incorrect.

For t<q_s define W=dGamma(T*T) on retained Fock space and

M_plus(t)=H_K-t,
M_minus(t)=H_K-t-W/(q_s-t).

Since PHQ QHP=W exactly on tail vacuum, the true Feshbach matrix satisfies

M_minus(t) <= S(t)=H_K-t-PHQ(QHQ-t)^(-1)QHP <= M_plus(t).

Inertia of H-t equals inertia of S(t), since QHQ-t is positive. Therefore, with strictly negative eigenvalue counts n_-,

n_-(M_plus(t)) <= N_H(t) <= n_-(M_minus(t)).

Here N_H(t) counts full eigenvalues strictly below t, including multiplicity. When the two computable counts agree, the full count is certified. This gives a no-missing-state certificate, not merely a residual bound for individual Ritz pairs. Cutoffs coinciding with exact levels need a separation promise or intervals.

For an ordered retained level mu_k<q_s, let ell_k be the kth eigenvalue of H_K-W/(q_s-mu_k). Then

ell_k <= lambda_k(H) <= mu_k.

Proof of the lower bound: for t<ell_k<=mu_k, M_minus(t)>=H_K-W/(q_s-mu_k)-t, which has at most k-1 negative eigenvalues; hence N_H(t)<=k-1. The upper bound is minmax. Both endpoints can be replaced by outward numerical bounds.

A more accurate enclosure solves the monotone scalar condition lambda_k(H_K-W/(q_s-t))=t by bisection. More structured positive resolvent bounds can replace the scalar (q_s-t)^(-1), but no such improvement is needed for the first gate.

## One-particle data and continuum obligations

For s<inf spec h, the inverse block identity gives

A_eff(s)=s I+[P_K(h-s)^(-1)P_K]^(-1).

This shortcut is not automatically valid for the larger range s<inf spec D if h-s is singular. The boundary operator is T*T=P_K h^2 P_K-A^2. These are small one-particle moment/resolvent matrices, accessible to quadrature or finite input. Their errors must be enclosed, with PSD inequalities rounded outward; no continuum convergence follows merely from changing quadrature sizes.

The exploratory code uses 600-point Gauss-Legendre quadrature of the flat normal band as a large finite BCS bath, not a certified continuum. Retained K consists of powers of positive quasiparticle energy multiplying the particle and hole source form factors, separately for both spins. Source containment and the actual Galerkin property are essential; a free fitted surrogate not embedded in the original bath does not automatically inherit these certificates.

## Why this may be a capability rather than a bound polish

The certificate can accept an adaptively selected finite bath without proving every possible target state is close to it in advance. A posteriori ground energy of a boundary-modified cluster controls all omitted many-body states. A second cluster solve measures the effect of omitted modes through boundary occupation rather than bounding the boundary operator by a large scalar norm. This dramatically improves the demonstrated numerical gate from the a priori 10^805 Fock dimension, while preserving exact state counting in the analytic construction.

The practical deliverable would be a certified wrapper around existing small-bath solvers: verify moment/resolvent matrices; lower-bound H_eff; calculate inertia of M_plus and M_minus at requested cutoffs; return either proved counts and energy intervals or an explicit failure requiring a larger bath. It is allowed to fail. Symmetry sectors reduce the matrix calculations and are compatible with all inequalities. SU(2) or S_z helps computation but cannot alone repair the prior worst-case exponent.

The main remaining gate is rigorous sparse inertia/ground lower bounds at competitive cost, not an additional many-body-tail theorem. eigsh Ritz values alone are insufficient: their residuals do not prove eigenvalue index or completeness. Dense sector diagonalization, interval LDL* inertia, or another verified lower-eigenvalue method must pay this bill. The 12-mode cluster's largest fixed-S_z sector has dimension 3432; 16 modes gives 48620. These are substantial but ordinary finite numerical-analysis objects, unlike the original worst-case space.

## Existing methods and claim limits

Baran, Frost and Paaske already show accurate small optimized surrogate baths against NRG and QMC: https://arxiv.org/abs/2307.11646 . Zalom's gap-edge NRG already targets this physical spectroscopy: https://arxiv.org/abs/2307.07479 . Standard Feshbach/Schur theory and eigenvalue enclosure methods precede this construction. The proposed contribution, if borne out by full verified arithmetic and a literature audit, is a practical *a posteriori completeness certificate* for finite-source massive-bath spectroscopy using a cheaply computable one-particle completion bound. It does not establish new access to the spectra themselves, a runtime advantage over NRG/DMRG, or significance beyond this regime.

Files: schur_gate.py, schur_gate_results.json, schur_gate_refine.py, schur_gate_refine_results.json. No arbitrary continuum cutoff, fitted-bath error, or interval roundoff allowance has been silently declared paid.

## Subsequent numerical-rigor audit

A separate exact-rational LDL implementation certifies complete inertia for the U=4, N=2 physical midpoint bath. It does not certify the adaptive 12/16-mode calculation. `RIGOROUS_NUMERICS_AUDIT.md` gives the explicit all-sector positivity test required for a certified q, the continuum moment enclosure pipeline, and the large-sector cost obstacle. The adaptive numerical result remains exploratory; no certified continuum interval or large-sector completeness count has yet been produced.

### Rank-eight rational-source update

The later rational-source construction and complete eigenbasis validator remove the previous large-sector bottleneck for this input. `verified_sector_spectrum_results.json` encloses q and all ordered retained spectra, obtaining excitation [0.53508161286,0.53580779182] and a count of three below the true ground plus 0.8. Largest sector is 252. See `RIGOROUS_NUMERICS_AUDIT.md` for explicit floating-point validation assumptions and the separate continuum quadrature-audit dependency. This does not retroactively certify the earlier 16-mode data or establish comparative speedup.

## Subsequent decisive rational-space gate

A source-containing rational space K=span{S,(h-1/2)^{-1}S} reduces the retained bath to eight spin modes, total Fock dimension1024, with largest S_z sector252. For the same U4 benchmark the exploratory ground interval width is0.00035736, singlet width0.00036880, hence excitation width0.00072616, already below0.001. Polynomial Krylov required16spin modes for a narrower interval and110.94seconds in the unoptimized full-Fock implementation. The rational representation is therefore a substantial implementation change, not a constant improvement to the original uniform localization bound.

Continuum-input interval arithmetic is implemented in verified_moments.py and documented in VERIFIED_CONTINUUM_MOMENTS.md. Complete finite-matrix eigenbasis validation is implemented independently by the verification worker in verified_sector_spectrum.py; consult its current results rather than the exploratory values above. This includes finite ground lower bound for q, continuum coefficient radii, complete sector spectra, and explicit IEEE roundoff budgets. Independent audit/reproduction remains appropriate before presenting the prototype as an established validated solver.

For an honest same-dimension comparator, same_size_surrogate.py independently implements the published Matsubara hybridization fit prescription of Baran, Frost and Paaske, using4paired bath levels at precisely U4,D2,Delta1,Gamma0.5. Fit plus complete sector diagonalization took0.061seconds and gives excitation0.536269232079; its full Fock dimension is also1024. This is not the authors' software and not an NRG/DMRG head-to-head. It confirms that small-bath spectra at this resource level are already standard. The candidate new capability is a certified continuum interval and proof that no level was missed in the specified window, not merely producing a plausible spectral number. No controlled NRG/DMRG speed or memory superiority has been measured.
