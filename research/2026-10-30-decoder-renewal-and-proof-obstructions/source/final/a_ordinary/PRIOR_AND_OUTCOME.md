# Strong ordinary construction and the remaining active operation

The target is recovery of an ALREADY encoded arbitrary payload under
N(rho)=U(rho tensor I_r/r)U^*, with fixed logical dimension k and unknown U.
Every ordinary competitor gets the same forward physical-query and known-
control contract. A theorem about a supplied Stinespring inverse, virtual
expectation estimation, a heralded discarded datum, or forward re-encoding
does not complete this task without another charged operation.

The strongest constructed working baseline in this folder is
`FLAT_RDS_RECOVERY.md`: ordinary random dilation plus the flat Petz identity
and explicit known-amplitude amplification. It recovers every payload, with
all references, using O(k^2 r^2/epsilon) original calls acquired offline.
The ideal recovery uses exactly 2r+1 reflected-code calls; its unknown output-
mean inverse disappears under the EXACT flat promise. Original source calls
after the payload arrives are zero, but the consumed quantum programme and
the O(r^2/epsilon) online collision sequence remain real resources. This is
an upper bound, not an optimality or practical-speed claim.

## Controlling predecessors and their actual supplied operations

1. Yoshida et al., [2512.21260v2](https://arxiv.org/html/2512.21260v2),
   Theorem 3, Lemma 6 and Theorem 5: forward native queries supply a JOINT
   common-frame random dilation/conditional-dilation channel and then sample-
   programmed reflection calls. Theorem 13's least-Kraus-rank Petz application
   has the opposite input/output dimension ratio to this encoding; it is not
   invoked as an unproved one-line solution. The explicit composition here
   supplies the correct expanding-channel port.

2. The full [Uhlmann/Petz primary2509.03619v3](https://arxiv.org/pdf/2509.03619v3),
   Proposition 35 and Section 10, really DOES give a forward-only construction
   of the necessary isometry/adjoint code blocks. It cannot be dismissed for
   lacking a native inverse. Its displayed Eq. (336) source cost specializes,
   with k fixed, D proportional to r, lambda_min=1/(kr) and tau_min=1/r, to
   a conservative tilde-O(r^6/epsilon^2) first branch, plus its separately
   acknowledged density-factor costs. Its O(log(kD)) simultaneous register
   width and programme-stream latency are admitted. This is a working generic
   baseline, not a lower bound or the best specialization to the flat class.
   The complete primary PDF pages 68--69 (PDF72--73) were read; the shorter
   older HTML preview was not used to infer an absent supplier.

3. Yoshida--Miyazaki--Murao,
   [2507.10784v4](https://arxiv.org/html/2507.10784v4), Corollary 2: forward
   isometry storage/retrieval has query cost Theta(1/sqrt(epsilon)) at fixed
   input dimension. `FORWARD_SAR_PORT_AND_LIMIT.md` gives an actual common-
   frame RDS/PBT transfer to m adaptive FORWARD dilation slots with
   O(m^(3/2)/sqrt(epsilon)) original N calls, including resource preparation.
   This is a real operation, but it neither supplies the required reflection
   nor purifies an already encoded B payload. The same proof gives the native
   Omega(1/epsilon) precision obstruction for that reflection shortcut.

4. [2401.10137v3](https://arxiv.org/html/2401.10137v3), Corollaries 6 and 11:
   four adaptive forward qubit-isometry calls suffice for exact deterministic
   inversion on the supplied isometry range. This stronger pure endpoint is
   granted. Its code contract does not determine its action on
   I_E/r tensor N(rho); code weight 1/r^2 is NOT a universal inverse-quality
   upper bound. Two explicit CPTP completions demonstrate the distinction.

5. Optimized qubit PBT has exact fidelity cos^2(pi/(n+2)), with explicit
   resource weights from [0901.2975](https://arxiv.org/html/0901.2975),
   Section IV.2. [2312.03188v2](https://arxiv.org/pdf/2312.03188v2), Theorem 1,
   supplies polynomial PBT measurement circuits; it explicitly leaves general
   optimized deterministic-resource preparation open. The qubit ballot-path
   construction in this folder pays the needed special case rather than
   importing that open operation.

6. Quintino--Ebler [2109.08202v3](https://arxiv.org/html/2109.08202v3),
   Section 5.2, gives exact optimal parallel qubit-inversion fidelity
   cos^2(pi/(Q+3)); Section 6/Figure 8 gives computer-assisted sequential
   two-query .7500. The later isometry primary transfers and optimizes these
   pure-source values. The root comb's pure Q2 endpoints therefore reproduce
   a known adaptive separation. No such formula for mixed r is inherited.

## Decision

The ordinary inverse is already a complete quantum operation with a quadratic
r source bill. The live missing operation is an active query-to-recovery
construction that bypasses the particular long reflection-programme lift.
The new SAR transfer clarifies one available adaptive resource; the exact
unknown-state comparison separates it from the reflection resource. These
facts do not decide whether linear-r recovery exists.

The accepted N1104 lower bounds are kept separate: physical adaptive queries
cost at least Omega(r) at fixed accuracy, while iid normalized-Choi programmes
can require Omega(r^2). The RDS supplier uses physical-channel preprocessing
on coherent joint logical inputs. It is not silently replaceable by the
same number of iid Choi copies. A finite small-Q optimization, including a
mixed-r adaptive gap, is neither an asymptotic upper bound nor a hardness
claim. The root and C retain ownership of those independent constructions.

## What was actually acquired and spent

Two all-parameter mathematical circuit constructions and one exact all-n
source-query obstruction are written here. Selected primary bytes and their
hashes are saved in `source_entry/SOURCES.json`; the existing full Uhlmann
PDF was reused READ ONLY. The PBT circuit theorem and full Uhlmann port pages
were visually inspected where PDF layout mattered. One attempted command
found `pdftotext` absent; bundled pypdf extraction was used without installing
anything. A web-source timeout was retained as an access failure and one
ordinary direct primary download then succeeded.

Original physical/source calls: 0. Quantum circuits executed: 0. New scientific
samplers, optimizers or many-body/source fixtures run: 0. The explicit ballot
DP is a proven polynomial resource algorithm, not an implemented end-to-end
quantum preparer. No hardware, wall-clock advantage, historical priority or
linear-r recovery has been established. Research reading/writing wall time
was not separately instrumented and is UNKNOWN rather than estimated.
