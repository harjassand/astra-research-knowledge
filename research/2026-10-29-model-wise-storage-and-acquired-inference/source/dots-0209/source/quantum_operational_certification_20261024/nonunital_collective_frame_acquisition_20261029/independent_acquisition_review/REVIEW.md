# Independent review — nonunital common-bank frame acquisition
2026-10-29 UTC. Reviewer: review_robust_algebra_boundary.

## Decision
**Accepted at the stated conditional structural/calibration interface**, including retained memory and the finite probability bound. No load-bearing correction found. The four probe programs and their results were reviewed; exact, stationary million-shot, and retained-memory million-shot programs were rerun from frozen copies, and all JSON values match the originals exactly. The v3 output is exactly the corresponding three-checkpoint prefix of the v4 rerun. This is a mathematical/mechanism review, not hardware validation, a historical novelty finding, or an efficiency advantage against an equally informed conventional learner.

Frozen originals are in `frozen/`; source hashes are in `check_independent.json`. Author files were not modified. Earlier LPN receipt remains unchanged and separate.

## 1. Kernel and nonunital interface
Let F_{r-1} include every previous physical preparation/measurement record and whatever additional past classical source history is needed to define its conditional memory state. Fresh probe systems are product with that state. Current private coins are independent of it. If all Kraus operators of the complete current data-memory operation commute with a fixed twisted swap S tensor I_B, trace preservation implies

  N_joint†(S tensor I_B)=S tensor I_B.

Evaluating on any conditional bath state gives the same full-data adjoint fixed point. Inserting maximally mixed spectators and tracing their outputs preserves the pair fixed point: the spectator normalized partial trace of S tensor I is S. The adjoint of any trace-preserving pair channel fixes I, whether or not the Schrödinger channel fixes I. Since S=(I+sum C_ab P_a tensor P_b)/2, the full 16-row coefficient matrix satisfies (T-J)vec(C)=0.

The lower-degree rows are not removable without a new proof. This follows because an adjoint image of a pair correlation can contain one-body and identity coefficients; Schrödinger nonunitality permits the identity coefficient. The actual Lindblad fixture has nonzero lower-degree coefficients, about0.623382 in Frobenius norm. Its full channel Choi matrix is positive to numerical precision, trace preservation error1.85e-15, and nonunitality is genuine rather than normalization error.

The fixed-point statement holds for every current conditional memory state. Averaging the actual predictable matrices therefore retains the same kernel pathwise. This is not the stationary average, the unconditional bath average, or any future channel. Nothing here infers a deployment promise from acquisition data.

## 2. Single-bank physical estimator
For local axis c uniform over3 and sign u uniform over2,

  E[rho]=I/2, E[3u 1_{c=p}rho]=P_p/2.

Independent all-site choices make the expectation of the signed weighted global input exactly (P_p on i tensor P_q on root tensor identities elsewhere)/2^n. It does not matter whether the actual global channel couples the pair to every spectator: linearity permits averaging the independent spectators before applying the conditional channel. This is why the all-site random signs matter.

Uniform independent local output axes give E[9 1_{z_i=a,z_root=b} y_i y_root | output state]=Tr[(P_a tensor P_b)rho_pair]. Joint outcomes need not be independent. Combining these identities gives E[X_r|F_{r-1}]=T_r for every entry. Every star edge and all144 entries use one common sequence of physical calls. Four counters per edge per shot are updated, not four different channels or banks. Arbitrary cross-entry and cross-edge correlations do not invalidate the final union bound.

The stationary source program uses all-site input configurations and one joint n-site output distribution per call. The retained-memory programs propagate a genuine pure bath vector through one joint unitary, draw one simultaneous output bitstring, update the bath with its normalized conditional amplitude, and choose the next source variant from the previous output parity. They do not reset the bath or supply its simulator state to the learner. Output axes are sampled before the multiplication in code but are not used by the source operation; this is equivalent to private post-isolation choice. The predictable occupation matrix is computed from the PRE-call bath Bloch vector and variant; the time ordering is correct.

## 3. Finite martingale bound
For one entry, |X|<=81. Squaring removes outcome signs. Averaging independent output settings gives a factor9. Each nonidentity input feature has second moment3, so the exact second moments are9,27,81 according to zero, one, or two nonidentity input indices. Thus E[X²|F_{r-1}]<=81 for every source. Since N_pair† maps Hermitian contractions to Hermitian contractions, |T_entry|<=1. Consequently the centered increment D=X-T has |D|<=82 and conditional variance<=81.

For completeness, the scalar exponential-series argument gives

  E[exp(lambda D)|F] <= exp(lambda²*81/[2(1-82lambda/3)]), 0<=lambda<3/82.

Indeed |E[D^k|F]|<=82^(k-2)E[D²|F] for k>=2, and k!>=2*3^(k-2). Iteration and exponential Markov give the one-sided Bernstein bound with denominator2(81+82eta/3); apply to both signs. For eta<=1 this denominator is at most650/3<220. A union bound over144(n-1) entries therefore gives exactly the claimed sufficient m>=220 eta^-2 log(288(n-1)/delta). An entrywise radius eta implies Frobenius, hence operator, radius sqrt(16*9)eta=12eta. No independence between calls, coordinates, or edges was used.

For adaptive stopping, this fixed-epoch statement must be confidence-spent over the declared epochs. It is not an anytime guarantee with one unchanged delta. Fresh epochs, with error/confidence targets making their union probability at most delta, work under the continuing common-kernel promise. Eventual completion additionally needs enough predictable excitation and decreasing error radii; there is no finite gap-free guarantee.

## 4. Gap and rounding
On the concentration event, let e=12eta. The promised normalized true vector c=vec(C)/sqrt(3) has Mbar c=0, so s1(Mhat)<=e. Weyl gives s2(Mbar)>=s2(Mhat)-e>=gL. Positive gL and the promised kernel imply one-dimensional kernel. The estimated unit smallest right-singular vector v satisfies ||Mbar v||<=2e, whence sin(angle(v,±c))<=2e/gL and min||v±c||<=2sqrt(2)e/gL.

After reshaping sqrt(3)v, its distance to the correct signed rotation is at most r=2sqrt(6)e/gL. The two compact components SO(3) and -SO(3) have Frobenius separation2: for rotations R,Q, ||R+Q||F²=6+2Tr(R^TQ)>=4. Therefore r<1 separates the sign branch. Projection onto the nearer component followed by sign selection has error at most2r=4sqrt(6)e/gL. The code's two proper polar projections implement this operation. Choosing root frame I leaves only a common unknown global rotation, irrelevant to the singlet target.

Small residual or observed gap is not proof of the common-algebra promise. Large residual can reject a promised model at the confidence level, but a small residual cannot validate it. Current-gap certification likewise cannot establish future commutation or a future bath model.

## 5. Transfer scope
The frame-to-memory transfer uses the separate reviewed `unknown_collective_noise_encoder_20261029/TWIRLED_FRAME_VARIANCE_BOUND_v9.md` and its `independent_variance_review` receipt, not a new empirical inference. Substituting the new e=12eta into its generic 24*pi²*n*e²/gL² formula is consistent. The old numeric substitution e<=9eta must NOT be reused here. Singlet encoding domain, code-dimension choice K>d0/2, fresh independent payload, full joint deployment-algebra premise, and retired-key physical logical twirl are inherited conditions. An untwirled individual-key channel or revealed-key service is not covered. Calibration and compiler/control errors remain separate. This review does not recertify the separate sequential guard; it accepts only the distinction that a guard at its own specified interface can serve model-free validation of a fixed candidate, whereas the acquisition result is conditional completeness.

## 6. Independent evidence and quantitative limitation
`check_independent.py` deterministically enumerates all1,296 product-Pauli inputs on4 sites. For all3 star edges it checks every signed weighted input identity and every rectangular coefficient expectation. Weighted-input discrepancy is exactly0; largest coefficient discrepancy is3.3306690738754696e-16. It separately tests Choi positivity/Hermiticity, trace preservation, and all16 input-feature second moments. Source/result hashes are included in `check_independent.json`.

`rerun_exact.json`, `rerun_stationary.json`, and `rerun_retained_v4.json` match original JSON objects exactly. The1m retained-memory errors0.0662–0.0721 are diagnostic, not confidence certification. For illustration at delta=.05, n=4 and m=1m, the declared sufficient bound gives eta≈.0463315 and e≈.555978, already larger than the actual occupation gap≈.353606. It cannot establish the sign/frame stop condition at that shot count. This limitation is explicitly acknowledged by the author and is retained here.

Conclusion: the construction genuinely removes the iid/reset/random-unitary restriction from this conditional frame-acquisition mechanism, but not the common unknown collective-algebra, private-setting, calibrated-control, or excitation assumptions. No claim of generic initially unknown-noise recovery is supported.
