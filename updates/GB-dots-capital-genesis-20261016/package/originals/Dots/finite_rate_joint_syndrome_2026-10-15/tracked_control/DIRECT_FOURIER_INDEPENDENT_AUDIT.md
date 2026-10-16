# Direct global-Fourier audit: finite-rate subset effects without a parity-preserving baseline

Date: 2026-10-15. The proposed strengthening independently verified. This is stronger than the Choi-lift proof in INDEPENDENT_AUDIT.md: its mathematical effect theorem allows reused supports, noncommuting baseline dynamics, and overlapping intervals, provided the exact private additive-control interface holds. Physical support/history composition remains separate.

## 1. Exact interface and result

On a finite joint memory/bath/dilation Hilbert space suppose

 H_{f,xi}(t)=H_base(t)+sum_{i in S} (-1)^{f_i} xi_i(t) A_i(t), (A)

where:
- f_i are independent uniform bits, independent of initial input and all other randomness.
- xi_i are independent rate-gamma_i telegraph signs, initially +1 at pulse start, independent of the f_i, input and all conditioned parameters.
- H_base and A_i are independent of ALL selected f_i and xi_i trajectories.
- H_base,A_i are Hermitian, ||A_i(t)||<=J_i, and A_i vanishes outside a fixed interval I_i of length tau_i.
- Baseline dynamics admits a common unitary/isometric dilation independent of the selected bits and trajectories. Prescribed seed-independent interventions may be included.

There is no commutation requirement on H_base, on distinct A_i, or on their memory supports. An arbitrarily large finite persistent bath and untouched reference are allowed.

Let U_{f,xi} be the full propagator. For the selected bits take its odd Fourier coefficient

 K_{S,xi}=2^(-|S|)sum_f (-1)^(sum_i f_i) U_{f,xi}.

Then the POSITIVE effect satisfies

 E_xi K_{S,xi}^dagger K_{S,xi}
 <= product_{i in S} B(J_i,gamma_i,tau_i) I,               (1)

where

 B(J,gamma,tau)=1/2{exp(-gamma tau)
       [cosh(d tau)+(gamma/d)sinh(d tau)]-1},
 d=sqrt(gamma^2+4J^2),

and B<=1/2[exp(2J^2 tau/gamma)-1] for gamma>0. Its continuous gamma=0 value is sinh^2(J tau). No gamma/J separation is needed.

If other initial-frame coordinates are also Fourier transformed, sum all their character labels. Parseval is exactly averaging their fixed values in (1). The same bound holds uniformly conditional on their other exogenous variables, followed by averaging. Genuine dilation outcomes are summed at the effect level, not conditioned and normalized.

## 2. Proof: Fourier parity replaces physical parity

Take the interaction picture of H_base, which is independent of the selected stochastic signs. The transformed A_i preserve their norms, irrespective of noncommuting data/bath dynamics. Expand the full propagator in its convergent Dyson series.

The selected initial-bit Fourier transform kills every word having an even number of insertions of some selected species. Thus each surviving ket word has an odd count for EVERY i in S. In K^dagger K, each bra word also has odd counts. Combining them gives 2m_i insertions, m_i>=1, for species i.

For their ordered combined times u_{i,1}<...<u_{i,2m_i} inside I_i, averaging its independent telegraph process gives the nonnegative kernel

 exp[-2gamma_i sum_r(u_{i,2r}-u_{i,2r-1})].

The matrix-element magnitude of the operator product is bounded by product_i J_i^(2m_i)||psi||^2. Each species has 2^(2m_i-1) possible ket/bra colorings with odd ket count. Summing all Dyson word orders partitions the product of the per-species ordered simplices, so there is no extra interleaving factorial, even when intervals overlap or nest.

The positive scalar majorant therefore factorizes as

 product_i sum_{m>=1}2^(2m-1)J_i^(2m) I_m(gamma_i,tau_i).

The exact kernel integral and its bound are

 I_m=1/m! integral_{v_r>=0,sum v_r<=tau}
          (tau-sum v_r)^m exp(-2gamma sum v_r) product_r dv_r
     <=tau^m/[m!(2gamma)^m].

The exact sum is B, obtained as E sinh^2(J integral_I xi). This proves (1) for every joint input vector and hence as an operator inequality. Noncommuting bath operators never move, and no physical parity-sector assumption enters.

Contrast with the earlier endpoint theorem: there parity conservation by H_base forced odd Dyson counts. Here the actual private-bit Fourier projection does that job, so H_base can contain arbitrary selected-bit-independent corrections or memory dynamics.

### Alternate exact proof using virtual seed qubits

Introduce one MATHEMATICAL seed qubit c_i initialized in |+>_X for every selected initial bit. In its Z basis, the controlled Hamiltonian is H_base+sum_i xi_i(t) Z_{c_i} tensor A_i(t). The final X outcome -1 on all selected seed qubits has amplitude exactly K_{S,xi}. Tracing seed qubits recovers the original classical initial-seed average; measuring X is a change of Kraus basis, not additional physical controller access.

Conjugate this controlled trajectory by product_i X_{c_i}^{N_i(t)}. It fixes the initial |+> seeds and commutes with the final X-label projectors. Between jumps it removes xi_i from the Hamiltonian; a jump becomes X_{c_i}. Averaging gives exactly

 L_lift=-i[I_c tensor H_base+sum_i Z_{c_i} tensor A_i,.]
          +sum_i gamma_i(Ad(X_{c_i})-I),

with each coupling and dephaser active only on its own interval. This is the simultaneous endpoint theorem with selected parity X_{c_i}, and interaction Z_{c_i} tensor A_i. The physical H_base automatically commutes with every VIRTUAL selected parity even if it acts arbitrarily on the physical data/bath. Hence that theorem proves (1) directly, including different pulse intervals. The seed ancillas are a finite Stinespring/Fourier representation, not added physical devices. They may not be exposed as unqualified online control records.

## 3. Derivation from a privately initialized, continuously refreshed Pauli frame

For pulse i let g_i(t) be its own full-Pauli frame, applied through an exact physical compilation which yields an additive conjugated error term g_i(t)^dagger V_i(t)g_i(t), and no other dependence on that pulse's private coordinates. Pick one Pauli generator P_i from the initial frame and condition all other frame coordinates and their update trajectories.

Write the remaining frame contribution as P_i^(f_i+N_i(t)) times the conditioned Pauli product. Pauli order phases disappear under conjugation. If V_i^cond is the interaction after the other coordinates' conjugation, decompose

 V_i^+=(V_i^cond+P_i V_i^cond P_i)/2,
 V_i^-=(V_i^cond-P_i V_i^cond P_i)/2.

Then the actual pulse term is exactly

 V_i^+ + (-1)^{f_i}(-1)^{N_i(t)} V_i^-.

The even term is independent of BOTH the selected initial bit AND its full selected Poisson path; the odd term has norm at most ||V_i||. All selected even terms belong to H_base. Other pulse terms and ideal operations belong there only if they are genuinely independent of these selected bits and paths in the SAME common dilation.

This is the crucial strengthened independence check. It would fail if a controller could read selected updates and change another term, if compiler-following errors had additional frame dependence, if randomizer gate errors were uncharged, or if physical wrapper transformations left selected dependence in correction operations.

For a full m_i-bit initial frame, a nonzero pulse character has at least one odd bit. Union over one witness bit per marked pulse and apply (1). With common per-pulse rates/strengths,

 effect(all marked pulse characters nonzero)
 <=product_{i in S} q_i I,
 q_i=min{1,m_i B(J_i,gamma_i,tau_i)}.                     (2)

With different generator rates one may use sum_{j=1}^{m_i}B(J_i,gamma_ij,tau_i) instead. For an n_i-qubit full Pauli frame, m_i=2n_i. The union does not assert independent generator errors. Caps follow by dropping indices with an uncapped factor above one and proving the bound on the retained subset.

## 4. Actual Kraus meaning, conditioning, and support

Independent averaging of the physical initial private frames gives a complete actual channel. Its full Fourier transform is a unitary change of Kraus representation, so the effects in (1)-(2) are positive effects of a complete GLOBAL Kraus family. They need not be available online. The selected refresh trajectories are averaged as exogenous Kraus indices, and all physical/dilation record indices are summed.

Unlike the finite-patch endpoint bound, there is no requirement to insert actual syndrome measurements at intermediate times or assume a sector-definite data state. The operator inequality is uniform over arbitrary joint inputs and bath correlations from the outset.

To reuse the existing completion-time support theorem, one still needs its actual locality/cleanliness conditions. Every inserted memory Pauli from pulse i continues to have the initial-frame character of that Pauli; the internal telegraph signs change coefficients but not that initial character. Thus full initial-frame characters still select the net local Pauli of each pulse after justified termwise memory-only regrouping. For a full Pauli frame, zero character fixes identity on the pulse's entire support. Nonzero character is charged on that pulse support. Shared-bath operators remain chronologically ordered.

This explains why the effect theorem can improve a pulse budget from action-squared to a finite-rate B budget without introducing a new causal record. It does NOT independently prove that arbitrary physical reused/overlapping pulse circuits satisfy the exact additive interface or the common-decoder support theorem. Those geometric/compiler obligations remain as in the existing qualified pulse theorem.

## 5. Numerical stress test and audit verdict

check_direct_fourier.py computes the exact averaged GLOBAL Fourier effects using a classical telegraph register and a coherent initial-bit register. It maximizes over the full physical joint-input space. It includes reused physical support, overlapping formal intervals, and a baseline Hamiltonian that does not commute with the selected interaction generators. The overlapping case tests the algebraic theorem only, not admissibility under a clean physical pulse compiler.

Verdict: the direct construction is valid under (A) and the explicit conditioning/dilation qualifications. It is the preferred effect proof for the existing additive private-pulse framework; the Choi route remains a useful special-case physical interpretation. Neither route qualifies noisy randomizers/controllers or proves a fully autonomous continuous-coherent-noise memory threshold.
