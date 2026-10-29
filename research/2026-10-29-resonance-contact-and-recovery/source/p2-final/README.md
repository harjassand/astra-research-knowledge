# Astra P2: causal measurement noise, quantum memory and complete correction

Scientific checkpoint: **29 October 2026 Australia/Brisbane**. This is new work in place. The preceding causal receiver, finite-energy construction, pulse certificates and actual failed accumulator comparison remain in `p2_mediator/` with their original reviews. No prior package is re-exported here.

## Main consequence

An acquired finite-batch field-feature model can now be compiled into a noisy causal measurement with an explicit quantum-storage schedule. The design space has an exact finite-matrix description. A separate theorem converts a delivered receiver into a complete source-correction allowance while retaining **all actual raw outcomes**, without an input-energy restriction on the original field in the ideal supplied model.

The strongest deterministic Gaussian alternative is included: allowing finite squeezing, fresh Gaussian states/channels and linear feedforward does not improve the ideal retained-mode versus final reported-measurement-noise frontier. A passive/vacuum/homodyne implementation attains it. Fresh mode count, energy/gain, internal loss topology and output deadlines are separate resources.

This is a foundational instrument and synthesis result. It does not establish a scalable computing advantage or acquire a native source/receiver interface.

## 1. The exact causal noise–memory criterion

For field-feature columns f_(i,t), use Q=a+a†, P=i(a†-a), [Q,P]=2i and W(f)=exp(i Phi(f)). Define Omega_t=Im Gram(f_t). The target final Gaussian POVM has characteristic function

    Mhat(u)=W(Fu) exp(-u^T N u/2), F=direct_sum_t f_t.

For arbitrary normal inputs and arbitrary references, this POVM is realizable with at most q_t retained canonical modes at each arrival cut **if and only if** there is a real skew path S_0=S_T=0 such that

    rank S_t<=2q_t,
    Gamma_t=S_t-S_(t-1)-Omega_t,
    N_t+i Gamma_t>=0, N_t real symmetric,
    sum_t N_t=N.

The receiver factors each positive matrix as fresh detector-vacuum features and applies the accepted passive compression lemma to the augmented field. Its prefix commutator is S_t. Thus all cuts belong to one compatible physical receiver rather than separately optimized incompatible fragments.

The exact no-noise theorem is recovered by S_t=sum_(s<=t)Omega_s when the total field is isotropic. With no quantum retention, S_t=0 and all local incompatibility is paid as added measurement noise. For positive definite weight W and a fixed path, the sharp weighted variance cost is

    sum_t Tr|i W^(1/2)Gamma_t W^(1/2)|.

For two batches with local forms K,-K and positive skew singular values kappa_1>=...>=kappa_r of W^(1/2)K W^(1/2), the optimum with q retained modes is exactly `4 sum_(j>q) kappa_j`. Executed example kappa=(3,2,1), W=I:

| Retained modes | Exact optimal trace noise |
|---:|---:|
| 0 | 24 |
| 1 | 12 |
| 2 | 4 |
| 3 | 0 |

The general path optimization is rank constrained and can be difficult. This is an exact characterization and synthesis rule from a feasible certificate, not a general fast optimizer. Fixed deterministic linear Gaussian processing is covered; arbitrary adaptive measurement axes, nonlinear reporting and non-Gaussian resources are not.

The reported POVM can coarsen a larger raw record. Its all-reference measurement identity alone does not establish a full-record source eraser. That bridge is separately constructed next.

## 2. The complete-record bridge

Let the actual source dilation be a specified controlled Weyl operation with intended diagonal gate G_S and source labels z_i=+1,-1. The receiver's vacuum features g are mathematical measurement coefficients; the actual hardware never couples the source to these auxiliary modes.

For comparison only, add those controlled auxiliary displacements to the source operation. The augmented family is exactly erased by the delivered receiver and its local feedback. Actual and comparison unitaries differ solely by a controlled displacement on independent detector vacuum. Their purification overlap is at least exp(-d²/2), where

    d²=max_z z^T N z.

Therefore the complete corrected source/reference/**entire raw-record** half-trace error is bounded uniformly by

    epsilon<=sqrt(1-exp(-d²)).

The original source, field and reference may be correlated; the original field need not have finite energy. The ideal comparison is to the same receiver on the common baseline state, preserving its measurement assemblage. The result uses a specified independent detector supply. Physical calibration errors on arbitrarily energetic fields are not made small by this theorem; they still require their own matched energy/control contract.

This representation change matters. A feature-cutoff comparison displaces an unknown original field and needs its moment bound. This comparison leaves that field unchanged and charges a known detector state instead. The earlier finite-energy projection can remain much sharper on its narrower input promise, and is preserved.

## 3. The operation determines the optimization

Two exact failures changed the design rule. In a three-batch four-source example with one retained mode, keeping the largest skew block independently at each cut costs trace noise 8, while keeping one plane costs 6. Per-cut best-rank truncation is not a general optimum.

The source alphabet also matters. After a common rational Hadamard rotation of the physical feature coordinates, those trace costs stay 8 and 6, but the optimal fixed-path sign objectives are 8 and 12. Thus optimizing mean-square noise can choose the worse complete-error allowance.

Root proved an exact fixed-path minimax formula. With C_n=conv{zz^T : z_i=+1,-1},

    min_(N_t+iGamma_t>=0) max_z z^T(sum_tN_t)z
      = max_(X in C_n) sum_t Tr|i X^(1/2)Gamma_t X^(1/2)|.

One common adversarial correlation matrix is used across all batches. Exact primal/dual certificates prove the values 6,8,12,8 in the four example variants, even after optimizing covariance on each fixed path. The elliptope gives an explicitly labelled upper relaxation. This optimizes a sufficient complete-instrument allowance, not actual channel error or the best path among all choices.

## 4. Detection, delay and a stronger conventional loss mechanism

Uniform homodyne efficiency eta has an exact correction in the passive receiver model. Let R=sum_t Re Gram(f_t). The ideal path criterion applies to the transformed noise budget

    B=eta N-(1-eta)R.

The weighted optimum becomes `[F_q(W)+(1-eta)Tr(WR)]/eta`, where F_q is the ideal path optimum. Large commuting features therefore still pay detector noise through the real Gram matrix. This theorem assumes lossless retained modes, common detector efficiency and independent vacuum loss inputs; it does not move arbitrary memory decay into a detector parameter.

A separate explicit two-bin operation includes one lossy stored mode. Before storage, tap the first arrival, heterodyne the reflected port, and keep that classical record. Choose tap transmissivity equal to known memory transmissivity tau. After storage, perform an ordinary Bell measurement with the second arrival and add the appropriately weighted early record. The tap-vacuum contribution cancels. All four actual records are specified.

For target (Q_1+Q_2,P_1-P_2), the ideal output covariance is `2(1-tau)I`. With common detector efficiency eta:

| Receiver under the stated passive assumptions | Added covariance |
|---|---|
| Exact optimum with zero quantum retention | `2(2-eta)/eta I` |
| Constructed tap/early-record receiver with one lossy mode | `2(2-tau-eta)/eta I` |

The constructed trace-noise improvement holds for every tau>0 in this pure-loss model. A thermal storage input of occupation n_e adds `2(1-tau)n_e I`; improvement then requires `tau/eta>(1-tau)n_e`. These are exact measurement comparisons, not gate/device error rates or universal storage thresholds. The receiver is not proved optimal over all coherent memory strategies.

The tap/feedforward mechanism is established conventional optical-amplifier machinery (Josse et al.). It is deliberately used to remove the weak inverse-gain route's apparent 50% threshold. Active squeezing before inefficient detectors is an extra resource excluded from the passive inefficient-detector optimum; the ideal Gaussian universality theorem does not rule it out.

## 5. The materially different alternative preserved

For a Z-diagonal source propagator satisfying Pi U_z Pi=U_(-z), its exact operator Walsh coefficients A_e have bath parity (-1)^|e|. An odd X-repetition code syndrome and a known initial/final bath charge select one error class. Correction gives identity on the logical subsystem tensored with a bath instrument, including arbitrary known-sector correlations and all true parity-refining outcomes.

The symmetry admits mutually noncommuting bounded parity-odd contacts, including Z_i sin Phi(f). This directly uses the preceding nonlinear-contact machinery without assuming it has a controlled-Weyl dilation. A complete core-and-no-return-packet parity boundary composes across storage epochs without resetting the bath state, provided the core readout is nondestructive and sector preserving.

Root corrected an initially overbroad signal/noise argument: a known code-preserving diagonal target G can factor from the symmetry-qualified error operation and is preserved, even if the total propagator lacks that covariance. The proof and 2,048 added direct matrix-element checks establish this; its many-body physical control remains unacquired.

Photon-parity recovery for n=1 is prior art and already stores one logical qubit without the repetition overhead. A single collective charge also limits universal correction rate for the full diagonal error family. Known-sector startup, complete parity collection, reliable code syndrome extraction and untagged errors remain material. This is a useful extension and competing mechanism, with no computing advantage claimed.

## Proofs, execution and actual review map

| Result | Proof / executable | Actual review location |
|---|---|---|
| Noise–memory path and exact two-batch optimum | `measurement_frontier/NOISE_MEMORY_PATH_THEOREM.md`; `noise_memory_checks.py/json` | `reviews/path_theorem/` |
| Active Gaussian comparison and passive attainment | `PASSIVE_UNIVERSALITY.md` | `reviews/universality/` |
| Complete raw-record conversion | `COMPLETE_RECORD_CONVERSION.md` | `reviews/complete_record/` |
| Source-alphabet minimax and exact certificates | `ALPHABET_NOISE_OPTIMIZATION.md`; `alphabet_certificates.py/json` | `reviews/alphabet/` |
| Uniform detector-efficiency frontier | `UNIFORM_DETECTION_FRONTIER.md` | `reviews/loss/` |
| Zero-memory benchmark and lossy Bell receiver | `noise_challenge/ZERO_MEMORY_NOISE.md` with `ZERO_MEMORY_SIGN_CORRECTION.md`; `LOSSY_BELL_WITH_EARLY_RECORD.md`; `exact_noise_checks.py/json` | `reviews/loss/` |
| Symmetry/code alternative and corrected target factor | `code_alternative/PARITY_ASSISTED_CODE.md`; `parity_code_exact.py/json` | `reviews/parity/` |

Proof headers retain their authored status; version-pinned actual review files supply the later verdict. Read the specified scope rather than inferring validation from co-location. Historical priority and external peer review remain unestablished.

Executed evidence includes eight complete receiver designs, exact two-batch/multi-cut identities, four source-alphabet primal/dual certificates, six lossy Bell cases and thirty tap comparisons, detector/thermal checks, and exact finite-bath Pauli/charge examples. Reviewers independently replayed the saved results and added separate algebraic audits. Floating passive matrices have residuals below 1.56e-15; these are diagnostics. Exact rational certificates and analytic bounds are separate from numerical diagnostics and physical error.

See `SOURCE_DECISION_AND_CORRECTIONS.md` for current Astra governing conditions, primary ancestry, useful failures and the operational frontier. `REPRODUCE.md` gives safe replay instructions. No computation or download is promised after this checkpoint ends.
