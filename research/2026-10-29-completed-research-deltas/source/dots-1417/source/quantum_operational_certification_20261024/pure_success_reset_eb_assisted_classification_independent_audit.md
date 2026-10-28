# Independent receiving: EB classification, assisted distillation, and EB value corollary

26 October 2026. **PASS**, scoped to E(rho)=p V rho V*+q Tr(rho) tau with qutrit input and arbitrary finite output reference. Governing notes: `pure_success_reset_eb_and_assisted_entanglement_classification.md` and, separately, `pure_success_entanglement_breaking_value_corollary.md`.

## Classification and actual operation

With X=d P_OmegaV+I3 tensor Y and T=3(d+TrY), the normalized Choi state has p=3d/T and q tau=3Y/T. If V*PkerY V=0, positivity implies the code lies in suppY. Invertible local whitening on that support yields I+d P_psi, whose squared Schmidt coefficients are the three eigenvalues r_i of V*Y^+V. The antisymmetric partial-transpose eigenvalues are 1-d sqrt(r_i r_j). The displayed 27-product phase average is exact: only matched multisets of phase labels survive, and the duplicate diagonal contribution is counted once. Its nonnegative diagonal residual proves separability INCLUDING d sqrt(r1 r2)=1. Restoring the local whitening and using the TP marginal yields the stated measure-and-prepare channel with the input transpose in its POVM. Thus the EB criterion is exact, not merely a PPT test.

For the reverse strict inequality, the actual encoder W and contraction K=sqrt(kappa) R_W^(-1/2) W*V*Y^(-1) obey K* K<=I. The transmitted half of a normalized qubit Bell pair gives exactly 3kappa/(2T) times [I4+d P_chi]. Its trace, fidelity, and positive fidelity witness agree with the manuscript. Kappa is not necessarily <=1; it is a contraction normalization, not an identity throughput fraction. There is no sender projection loss. Unknown-input heralding is not constant in this distorted-success protocol.

The recurrence increment factors as (1-F)(2F-1)(4F-1)/(8F^2-4F+5). Reapply the fidelity-preserving bilateral Clifford twirl after each successful recurrence round; the next scalar recurrence then applies exactly. The monotone fidelity sequence has limit1, reaches 13/16 in finitely many rounds, and every finite pass probability is positive. Charging the initial Bell-half acceptance and each Ppass/2 factor gives strictly positive asymptotic original-use rate before hashing. This requires known iid sources, ideal local operations, shared randomness and two-way classical communication. It makes no unassisted-capacity, finite-blocklength, or hardware claim.

For visible kernel G!=0, the regularized matrix has r1>=||G||/epsilon and r2>=1/(||Y||+epsilon). The chosen epsilon has epsilon(||Y||+epsilon)=d^2||G||/4. The filter is designed with Y+epsilon I but applied to ORIGINAL Y, so N=I-epsilon JJ* is PSD and <=I. Its actual unnormalized witness is d sqrt(r1 r2)-TrN/2>0. This receives rank-one visible kernel as well as higher ranks without claiming exact noiseless qubit extraction. Invisible kernels are removed; YV=0 and p=0 endpoints are separately correct.

## Primary provenance and corroboration

Independently opened Vidal–Tarrach, https://arxiv.org/pdf/quant-ph/9806094, Eq.(41), which gives pure-state random robustness n1 n2 a1 a2; the manuscript's explicit decomposition makes the conventions self-contained. Independently opened BDSW v2, https://arxiv.org/html/quant-ph/9604024v2, §3.2.1 Eqs.(42)–(43), and its hashing section §3.2.3. Their Bell-pair recurrence and known-iid one-way hashing supply the stated protocol ingredients, not new general distillation results.

Replayed `pure_success_reset_eb_distillation_check.py`: exact recurrence algebra PASS; actual original Choi/contraction, 27-product decomposition and singular original-source replay PASS. The faithful example has F=41/76, charged rate approximately1.15965e-9; the singular rank-one-kernel example approximately3.557e-5. These numerical rates are corroboration of the analytic positive-rate construction, not certified optimal rates. The stated graph irreducibility proof is valid: simple exterior D plus connected off-diagonal C*C and invertible C force every common code/reset reducing projection to be scalar.

## Separate entropy corollary

For d>0, EB implies supported code and positive x_i=eig(dV*Y^+V), x1 x2<=1. With u=x2 in(0,1], diag(x1,x2,x3)<=diag(1/u,u,u). Replayed `pure_success_eb_value_exact_certificate.py`: the exact numerator of exp F-1 is the stated polynomial; its sole negative term -864u^11 is dominated by2835u^10 and all other terms are positive. Thus the endpoint lies in the received initial-F region; downward Loewner closure and the actual-source strict receiving theorem imply D(X)>0. This uses finite supported Y, not a singular inverse substitution across visible kernels. At d=0 the deficit is zero; Y=0 with d>0 is reversible and not EB.

Consequently any negative source in THIS channel family must be non-EB and has the explicit positive two-way-assisted entanglement protocol above. This does not prove positivity for all distillable sources, arbitrary quantum states, or unrestricted WH3.
