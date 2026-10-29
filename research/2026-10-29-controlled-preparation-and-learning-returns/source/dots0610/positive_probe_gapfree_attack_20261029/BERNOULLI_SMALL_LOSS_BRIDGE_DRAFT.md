# Positive Bell-sign probe and small-loss linear-bandit bridge (draft)
2026-10-29. New proposed proof extension; not independently accepted. Exact real-valued sampling/moment operations are specified below, but a resource-certified finite-precision implementation remains open. No executed learning advantage is claimed.

## 1. Physical observation rather than exact expected loss
For one selected edge, let S_C=(I+sum_ab C_ab sigma_a tensor sigma_b)/2 on that edge, tensored with identity spectators, C in SO(3). Prepare a uniformly random member of its four twisted Bell eigenstates, and maximally mixed spectators. Record its swap sign; after one full-array source call, measure in the same Bell basis and record Y=1 exactly if the sign changed. A change between two positive-sign Bell states is NOT a failure.

The averaged physical input is I_D/D, independent of C and the Bell label. Conditional on the prior history, assume the source is a single CPTP map not informed of the private current setting. Let A_k be its effective Kraus operators after fixing its current memory density matrix. Direct expansion in the swap-sign eigenbasis gives
q_t(C)=E[Y|history,C]=(1/(4D)) sum_k ||[S_C,A_k]||_HS^2.
Thus q_t is a positive quadratic form x(C)^T H_t x(C), x(C)=vec(C), H_t>=0. Explicitly H_ab,cd=Re sum_k Tr([sigma_a sigma_b,A_k]†[sigma_c sigma_d,A_k])/(16D). This formula permits nonunital channels. If every relevant Kraus commutes with one fixed true S_C*, then q_t(C*)=0 for every current memory state. Identity noise gives the observed Y=0 with certainty, not merely a zero mean signed estimator.

One probe consumes one full-array source use, two-qubit twisted Bell preparation/readout, and classical randomization/preparation of the spectators. It does not query all edges simultaneously. No source-memory reset is assumed. Private label, frame setting and current role, and trusted or error-budgeted control are essential. Imperfect physical controls can create positive comparator loss.

## 2. Fixed finite feature dimension and a finite action oracle
Use the symmetric feature phi(C)=svec(x(C)x(C)^T), with the matching symmetric inner-product convention, dimension at most45. Compress to its actual linear span if necessary; no claim that45 is minimal. Loss is linear in these features and lies in[0,1] for every allowed action.

SO(3) Haar orthogonality gives E_C xx^T=I_9/3. Hence Tr H_t=3 E_C q_t(C)<=3, and ||H_t||op<=3. Because H_t x*=0 under the common-zero promise,
q_t(C)<=3 ||C-C*||_F^2.
This is a quadratic approximation penalty, not a Lipschitz penalty proportional to the distance.

For a finite horizon T, an explicit Euler-angle grid gives an epsilon Frobenius cover of SO(3) with O(epsilon^-3) rotations. For example discretize each angle in Rz(alpha)Ry(beta)Rz(gamma), and use ||R_axis(a)-R_axis(b)||F<=sqrt2 |a-b| plus a telescoping product bound. Set the mesh sufficiently fine that epsilon<=T^-1/2. The nearest grid rotation is a fixed comparator on every realized adaptive history and has total loss at most3. The grid size is O(T^(3/2)); this is potentially enormous but finite, and independent of source Hilbert dimension except for the one-edge interface.

Linear optimization over this finite feature set is plain enumeration. Membership in its convex hull and unbiased rounding are finite linear programs. Given x in the convex hull, solve nonnegative weights summing to1 with weighted feature vector x, and sample a rotation accordingly. Caratheodory reduction uses at most r+1 rotations, r the affine dimension. Do NOT execute a generic fractional matrix as a physical rotation: execute one sampled genuine SO(3) action. Neither approximate nearest-rotation rounding nor spectral rounding is asserted to preserve the mean.

The feature hull has affine constraints (including constant trace), so continuous densities are with respect to relative Lebesgue measure on its affine hull. The uncentered second-moment matrix is inverted only on the linear span of the actions. This is a bookkeeping extension of the standard convex-hull algorithm, not an assumption of full45-dimensional volume.

## 3. Literature premise and actual Bernoulli extension
Primary premise: Ito, Hirahara, Soma and Yoshida, NeurIPS2020, Tight First- and Second-Order Regret Bounds for Adversarial Linear Bandits, Theorem1 and Appendix B (especially estimator unbiasedness and the stability term). The published first-order theorem is stated for exact linear scalar feedback. We do not claim that citation alone establishes a quantum shot-noise interface.
Main paper: https://proceedings.neurips.cc/paper/2020/file/15bb63b28926cd083b15e3b97567bbea-Paper.pdf
Full appendix: https://proceedings.neurips.cc/paper/2020/file/15bb63b28926cd083b15e3b97567bbea-Supplemental.pdf

Use their convex-hull exponential-density/truncated-sampling algorithm with predictor m=0. At round t, sample its truncated convex action x_t, round to a physical feature a_t with E[a_t|history,x_t]=x_t, and observe the actual Bernoulli Y_t. Let S_t=E[x_t x_t^T|history] under the truncated distribution. Replace the scalar feedback in the estimator by Y_t:
 ghat_t=Y_t S_t^-1 x_t.
Then conditional expectation is exact:
 E[ghat_t|history]=S_t^-1 E_x[x E(Y|x,history)]=S_t^-1 E_x[xx^T] ell_t=ell_t.
The environment may adapt to all prior history, including its quantum memory; it must not anticipate current private randomization. The comparator is evaluated on the same actual conditional channels, not an invented counterfactual memory trajectory.

Every deterministic exponential-density potential calculation in Appendix B is a calculation on the realized estimator sequence, so remains unchanged. The truncation geometry is chosen before the physical shot and is unchanged. Its stability estimate uses the scalar response only through its absolute bound and its square. Here |Y_t|<=1 and Y_t^2=Y_t. The final conversion from estimated regret to true conditional mean loss uses only the unbiasedness identity just proved. Thus the same argument gives
 E sum_t <ell_t,a_t-a*> <= 4 d eta gamma^2 E sum_t Y_t^2 + d log(T)/eta +3
for fixed gamma>=4log(10dT) and eta<=1/(sqrt(800d) gamma), where d is the retained linear-span dimension (an upper bound45 suffices). The entropy volume exponent is the affine dimension, which is no larger than d, so using d in this bound is conservative even for an affinely constrained feature hull.

Choose gamma=4log(10dT) and eta=1/(8d gamma^2), T>=2. This satisfies the step-size constraint. Write X=E sum_t q_t(C_t)=E sum_t Y_t and L*=E sum_t q_t(C_grid*). Since Y²=Y,
 X-L* <= X/2 + 8 d^2 gamma^2 log(T)+3,
 hence X <= 2L* +16 d^2 gamma^2 log(T)+6.
The explicit finite-grid comparator has L*<=3, giving a polylogarithmic expected cumulative probe loss, O(d² log³T), without an excitation gap. This is not a high-probability confidence sequence and does not identify an unexcited frame. Markov conversion would lose a factor1/delta; no sharper tail is claimed here.

## 4. What remains before an operational claim
The preceding extension is a proposed mathematical bridge, to be independently checked against the complete potential proof. The action oracle and unbiased convex rounding have explicit finite definitions, but the algorithm still samples an exponentially tilted convex-body density and computes its truncated second moments. Exact real-oracle operations are not a compiled finite-precision controller. The paper discusses polynomial-time approximate convex sampling given optimization oracles; its error tolerances must be instantiated for this action hull and Bernoulli extension, including conditioning of S_t. No such resource-certified implementation or walltime benchmark has yet been supplied here.

A finite SO3 grid also needs finite gate-synthesis/calibration error accounting. The T^(3/2)-sized enumeration and convex-body routines may be wholly impractical despite logarithmic source loss. One edge is queried per physical call; a star with many edges must budget allocation, causal learning updates and the conversion from cumulative probe loss to encoding performance. This note alone does not replace the completed multi-role readiness/guard theorem. The constants 16d²gamma²logT are very large. Practical cost superiority is not claimed.
