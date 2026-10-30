# Workspace/history healing: bundled-loss corrected extension

Status (2026-10-29 bundled-loss erratum): the finite-path implication below uses the corrected complete-instrument premise. For the actual declared repaired, ownership-checked, finite-monitor generator, those full operator identities and this finite-rate application have now been independently reviewed in `producer-workspace/SCOPED_REVIEW.md`, especially sections 1–3. This is not acceptance of the former stronger individual-loss premise. General variants remain conditional on the displayed identities; clock-basis enumeration alone is insufficient.

## Candidate full bad projector

For hub h:

- in structurally inconsistent clock sectors or abort phases, B_h=I on its data/workspace;
- in structurally consistent acquisition A_i or verification Q_i sectors, B_h=I_data tensor (I-|0><0|_workspace);
- in a consistent executing sector G_t, B_h=I-U_(h,t)(I_data tensor |0><0|_workspace)U_(h,t)^*, where U_(h,t) is the known circuit prefix.

This is block-diagonal in clock POSITION/ownership labels. Therefore clock-label monitor projectors commute with B_h; no workspace/syndrome measurement is required.

## Required global algebra

For EVERY other hub's gate, acquisition, cleanup, abort drive, and reset, verify the appropriate full operator conditions:

 [H_e,B_h]=0,
 J_(e,s)(I-B_h)=(I-B_h)J_(e,s)(I-B_h) for every resolved gain s,
 A_e=sum_s J_(e,s)^*J_(e,s),
 [A_e,B_h]=0 for each complete instrument e.

Individual syndrome losses J_(e,s)^*J_(e,s) need not commute with B_h. The no-jump/path estimates use A_e, while gain terms remain separately resolved and are summed over outcomes for the selected reset event.

Indeed, for C_e=sum_s J_(e,s)^* B_h J_(e,s), good-range invariance gives C_e=B_h C_e B_h<=B_h A_e B_h=A_e B_h. Hence the whole instrument satisfies D_e^*(B_h)=C_e-A_e B_h<=0. Individual dissipators need not be nonpositive. Together with Hamiltonian commutation these imply L^*B_h<=0. Checking only classical owner flags or arrows does not establish the data-dependent identities. In particular another hub's dirty computation must not be able to alter a good hub's pending dressed data sector; actual ownership guards/disjoint held resources must supply that fact.

## Uniform local path once the identities hold

After a joint CLOCK-only projection of the hub/resource patch, a bad state lies in one of three cases:

1. Inconsistent clock or abort: use the structural two-step p->R->Q_0 path.
2. Consistent A_i/Q_i with dirty workspace: the state is supported on workspace complement Q_w. A one-site reset |p,0><p,s> (s!=0), summed over s, has total intensity kappa_w Q_w and maps to a good state. The optional s=0 self-loop makes a complete Poisson overwrite but is not necessary.
3. Consistent G_t with dirty history: reverse t known circuit gates. All required resources are ALREADY owned, so no acquisition or external availability is needed. The unitary reverse maps B_h exactly to I_data tensor Q_w at G_0=A_k. Then apply the workspace reset.

With at most ell circuit steps, the selected path length is

 L=max(2,ell+1).

Every coherent selected block is an isometry; the final workspace reset has uniform bundled intensity on the eligible dirty sector. The local no-jump loss need only be diagonal in clock POSITION, not scalar on workspace. Thus the CP-Dyson and finite monitor-window proof applies unchanged. In particular, none of the numerical constants below changes: they bound summed losses and bundled reset intensities, not individual syndrome-loss commutators.

## Explicit constants and conclusion

Use local bounds B, g_min (minimum reverse/abort coupling), kappa_min (minimum reset intensity), and patch size n. Set

 delta<=min{1/(16B),g_min^2/(16B^3)},
 p_0=min{g_min^2 delta^2/4,kappa_min delta/4,1/4},
 epsilon<=min{1/(16B),p_0^L/[8B(L+1)]}.

For direct Poisson clock dephasing, w=exp(-n gamma epsilon)(gamma epsilon)^n/n!, T=Ldelta+(L+1)epsilon, and c=(p_0^L/2)w^(L+1)exp(-n gamma Ldelta).

For label-resolved reset monitors with a preliminary flush, use w_mon=alpha(epsilon/n)^n exp[-kappa_m(n-1)epsilon], T=Ldelta+(L+2)epsilon, and c=(p_0^L/2)w_mon^(L+2)exp(-kappa_m n Ldelta).

For the independently reviewed actual generator, and for any variant satisfying the full bundled algebra above,

 T_T^*(B_h)<=(1-c)B_h,
 Tr(rho_t B_h)<=(1-c)^floor(t/T)Tr(rho_0 B_h)

for arbitrary physical initial states, including data/workspace/reference entanglement. This is full quantum-flag weight contraction. Do not identify it automatically with a classical first-healing stopping time.

## Not a logical-correctness theorem

A dirty hub may corrupt its fixed data support before its workspace/history defect is erased. B_h=0 means a consistent pending history and clean workspace relative to the actual current data, not that the data equals the fault-free logical state. Bounding the resulting data-fault cluster and obtaining an error-correction threshold remain separate tasks.

## Bundled-loss source correction and review provenance

The earlier source demanded `[J_s^*J_s,B_h]=0` for every individual reset. That is a sufficient but unnecessarily strong hypothesis and is FALSE in general for the actual terminal syndrome channels. It is superseded here by individual good-range preservation plus commutation of the summed complete-instrument loss. Separately resolved channels are retained; this is not a coherent merging of Kraus gains.

Exact negative regressions: `producer-workspace/check_reset_loss_nuance.py` and `.json`; independent counterpart `producer-workspace/check_bundled_loss.py` and `.json`. They exhibit noncommuting individual losses and commuting summed loss while good-range preservation holds.

The revised actual-generator acceptance is `producer-workspace/SCOPED_REVIEW.md`, sections 2–3. Construction proof: `producer-workspace/COMMUTING_HISTORY_DEFECT_PROOF.md`; its separate construction audit is `INDEPENDENT_AUDIT.md` in that directory. The previous local-healing audit reviewed the earlier conditional theorem and is not silently re-labeled as an audit of corrected source bytes. Pre-correction text is preserved alongside this file with suffix `.PRE_BUNDLED_ERRATUM.md`; old/new hashes are recorded in `BUNDLED_LOSS_ERRATUM_MANIFEST.json`.
