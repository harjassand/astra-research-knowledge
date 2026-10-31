# Independent review: energy-controlled first corrector

Verdict: scoped mathematical PASS for the stated logical-output model-error bound. This is not a new full compiler, a retained-source-process approximation, or a novelty/practical-advantage claim.

Source fully read: ENERGY_FIRST_CORRECTOR_CANDIDATE.md, SHA-256 0580c0ead11604faeac5f1f2b219f3c274979f8ef0f345a3430ee652a2ee4671. Review date: 2026-10-31. The source receives the native finite dark generator with no extra source Hamiltonian, positive gap g, drift kappa, centered Hermitian K, and system-only H0/instruments.

## Exact first-corrector algebra

Write P_s for the dark projector. S=H_Q^{-1}QKP_s+P_sKQH_Q^{-1} is Hermitian and purely off-diagonal. Its norm is the norm of its QP block, at most b/g. For a system observable O, F(O)=i[S,I tensor O] is off-diagonal and has complete norm at most 2s.

In G†F=sum L_j† F L_j−{H,F}, the anticommutator cancels exactly the QP and PQ blocks of VP. Centering removes the PP block of VP. Every recycling term has QQ support because L_jP_s=0. Consequently G†F+VP is exactly the displayed B, including QLQ recycling; no perfect-reset-source assumption has entered.

After conjugating B by H_Q^{-1/2}, the QQ commutator costs 2b/g. The recycling map has Kraus L_j H_Q^{-1/2} and complete norm ||sum H_Q^{-1/2}L_j†L_jH_Q^{-1/2}||=2. It therefore costs at most 4s. Thus beta=2b/g+4s bounds the relative complete norm. For any reference-extended state and Hermitian unit observable, |Tr rho B(O)|<=beta Tr(H rho). This is a state-weighted estimate, not a small global norm claim.

The PP block of VF gives the CP effective stack sqrt(2)H_Q^{-1/2}K|psi>, with the same orientation as the separately reviewed generic dark reduction. Its complete generator norm is at most 4bs. A=VF−PD has zero PP block and complete norm at most 8bs. The gentle estimate ||rho−P_s rho P_s||_1<=2sqrt(Tr Qrho), together with Tr Qrho<=E/g, gives the stated 16bs sqrt(E/g) bound. The final residual term has norm at most gamma0=2d/g+8bs^2, since the off-diagonal extraction of [H0,K] gives ||[H0,S]||<=d/g.

The exact residual is therefore sqrt(lambda)B+(VF−PD)+lambda^{-1/2}([L0,F]−FD). No full source resolvent appears in these estimates.

## State-weighted controlled Duhamel

Use the common intertwiner P+lambda^{-1/2}F on every interval. Telescope so the evolution before an inserted residual is the actual physical evolution, while the observable after it evolves under the effective channel and future instruments. The latter is a complete contraction; the former is an actual reference-extended state whose unconditional source energy obeys the stated energy inequality. This orientation is essential: one must not replace that energy by an unproved energy of an arbitrary hybrid state.

System-only trace-preserving instruments, including adaptive retained classical records, preserve the unconditional source energy. Summing interval integrals consequently uses the same global actual-state energy bound. The two endpoints cost 4s/sqrt(lambda), not a fresh endpoint penalty at every control. Each acquired control commutator costs nu_j/sqrt(lambda), with the safe nu_j<=4s. The sharper unitary and decomposed sufficient bounds are valid. No rare conditioned outcome is certified separately.

The all-rate energy inequality E'<=−lambda kappa E/2+2C^2/kappa implies E(t)<=E0 exp(−lambda kappa t/2)+4C^2/(lambda kappa^2). Integrating this and its square-root upper bound gives exactly 2E0/(lambda kappa)+4C^2T/(lambda kappa^2) and 4sqrt(E0)/(lambda kappa)+2CT/(sqrt(lambda)kappa). Substitution produces the displayed coefficients 2 beta E0/kappa, 4 beta C^2T/kappa^2, 32bsCT/(kappa sqrt(g)), and the separate 64bs sqrt(E0)/(lambda kappa sqrt(g)). They are consistent.

For the optional energy-form assumption, sqrt(lambda)>=2a_E/kappa first leaves damping lambda kappa/2. Young's inequality spends half of that and gives E'<=−lambda kappa E/4+4r_E^2/kappa. The displayed integrated bounds and substitution are correct. Neither proof applies normalized-state Jensen to an unnormalized tilted process.

## Independent recycling diagnostic

I wrote and executed check_first_corrector_independent.py, with a three-state source having jumps sqrt(2)|0><1|, sqrt(2)|0><2|, sqrt(2)|1><2|. It has H=diag(0,1,2), G†H=diag(0,−2,−6), and genuine QLQ recycling. Thirty complex centered source-qubit couplings and Hermitian observables gave maximum exact-algebra residual 2.81e−15 and CP-stack orientation residual 4.18e−15 in floating arithmetic. The output is first_corrector_independent_checks.json. These checks support indexing/sign inspection only; the proof above is the certificate, not the numerical values.

## Scope and acquisition boundary

The conclusion is for complete retained system/reference/system-only-record outputs, with arbitrary initial quantum correlations satisfying the actual energy promise. E0<=h gives a uniform-input fallback; it need not be dimension-independent. Source interventions and retained source output are excluded. Displayed inverse-lambda estimates require lambda>0; lambda=0 admits the trivial distance-2 bound. The effective stack, psi preparation, H inverse-square-root operation, actual K block normalization, effective execution, controls and synthesis costs still require acquisition and accounting. A small norm b or s alone does not supply a tight block encoding. C or r_E can still carry substantial model-size costs. This removes the global return-resolvent constant from this logical error certificate; it does not yet establish a cheaper practical simulator or a new general elimination principle.
