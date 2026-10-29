# Independent review: stationary-residual Schur native-regret certificate

28 October2026. PASS_SCOPED_SAME_CHANNEL_SCHUR_CERTIFICATE. Bound source version only; later changes need explicit receiving. Original source unchanged.

Read the complete governing source. For exact physical B, the identity Q_sym P=−(I⊗sum[C_j,B_j])P/2 has the correct order and sign. Partial logical trace of each commutator vanishes, proving PQ_symP=0 for arbitrary Hermitian contrasts, without a positive-noise-model premise. This exact identity is why a block-Schur repair is legitimate even though the stationary off-diagonal residual is nonzero.

If W>=kappa on P-perp and ||Z||<=z, lambda=(sqrt(kappa²+4z²)−kappa)/2 satisfies lambda(kappa+lambda)=z². The lower block W+lambda is strictly positive; its Schur complement is nonnegative. At z=0, the zero off-diagonal block yields positivity directly. Therefore Y_sym+lambda I is a true recovery-SDP dual feasible witness. TrY_sym=J_C(B) gives native entanglement-fidelity regret at most d lambda/4. The rational upper bound z²/kappa and cap1 are valid. No physical source realization of a fitted model is used: this concerns the actual measured channel.

Independent exact fixture `qubit_extractor_schur_independent_check_20261028.py/.json` shows the sharper square-root bound is SHARP. For actual qubit unitary U=[[c,−s],[s,c]], identity candidate and c²>s², Q_sym=2c²I−2P_U; kappa=2(c²−s²), z²=4c²s², lambda=2s². The upper bound d lambda/4=s² equals actual regret against inverse-unitary recovery. Three rational instances verify the kernel, transverse gap, PSD repair and exact regret. No acquisition draws or optimizer execution are claimed.

## Ordinary holdout and finite confidence

The declared independent stationary holdout has M=3(d²−1) experiments with n calls each. For uniform private input sign, signed outcome expectation equals Tr(P_l C_j). Orthogonality gives Frobenius squared error <=(d²−1)eta²/d<=d eta². Hoeffding eta=sqrt(2log(2M/beta)/n) and a simultaneous union bound are conservative and correct. The identity coefficient is exactly zero for the actual TP channel.

Each C error has operator norm<=a. The Y_sym error is<=3a and H error<=3a, so Q error<=6a; compression gives the stated stationarity and transverse-gap errors. Outward arithmetic allowances must be additional. With an exactly optimal candidate, true gap kappa0, exact empirical spectral computation and a<=kappa0/24, kappa_cert>=kappa0−12a>=kappa0/2 and z_cert<=12a. Hence regret<=72d a²/kappa0=144d²log(2M/beta)/(kappa0 n). This n is PER coefficient; total cost is M n, not n.

Training independence/frozen candidate, fixed allocation and a common stationary restarted channel are explicit source conditions. The proof does not justify arbitrary drifting per-setting channels or reuse of a post-selected confidence bank. Calibration/readout/control imperfections are charged separately, not absorbed by exact algebra. Under these conditions the certificate is finite but may abstain at practical budgets.

## Scope

Received only same-actual-channel full-CPTP native oracle regret for the accessible output used in the contrasts. Not received: generator distance, source-family membership, global locality, complete-memory recovery, arbitrary future noise, efficient empirical advantage or historical priority. Standard recovery-SDP dual repair is correctly credited. General localization requires its separate source and review.
