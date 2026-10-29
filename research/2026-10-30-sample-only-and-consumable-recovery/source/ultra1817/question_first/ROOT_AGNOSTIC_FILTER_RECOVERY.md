# Learn the actual channel: effective rank and recoverability are separate

30 October 2026. **PROPOSED; complete independent whole challenge pending.**
Root personally develops the central approximate-competitor principle. B owns
copy-acquired common spectral filtering and threshold resources. C owns the
N1291 transfer and finite uniform small-irrep preparation. A independently
challenges the complete operation. No source, device or numerical fixture has
been run for this construction.

## 1. A stronger question than closeness to an exact encoder

Let N:C^k -> C^D be one fixed memoryless CPTP source. Its actual mean output is
A=N(I_k/k). Suppose there EXISTS a mathematical recovery R0 with

    F_e(R0 N,I_k/k)>=1-kappa.                           (1.1)

No R0 gate, adjoint, Stinespring oracle or description is supplied. Let

    tail_d0(A)=sum_(j>d0) lambda_j(A)<=tau.              (1.2)

The index d0 is a supplied intrinsic-size upper bound; tau and kappa can be
analysis parameters rather than values known to the algorithm. Conditions(1.1)
and(1.2) are independent. We do NOT assume N is diamond-close to a particular
perfect mixed-isometry source. This removes the previous exact-model supplier
instead of comparing every training carrier with that unknown ideal channel.

Physical access is paid: forward source calls accept entangled Choi inputs;
fresh copies of A are made by N(I_k/k); all Choi training outputs and references
can stay coherent until the late payload arrives. Known carrier controls and
joint reference-safe compression are available with their actual gate/storage
costs. This is a one-batch quantum operation, not a reusable classical decoder
learned before an unlimited late stream or an uncontrolled memoryful source.

## 2. One actual spectral cutoff

Choose a rational threshold c in[a,2a], and let Pi=1_[c,infinity)(A). Define

    F(rho)=Pi N(rho)Pi
             direct_sum Tr[(I-Pi)N(rho)] |fail><fail|.

The flag is orthogonal to retained carrier space. Its mean rank is at most
floor(1/a)+1. With t=Tr[(I-Pi)A], the top-d0 eigenvalues below cutoff contribute
at most2d0 a and the remainder contributes at most tau, so

    t<=tau+2d0 a.                                     (2.1)

This elementary tail bound uses the actual A; it is not a tomography estimate
or an assumption that all source outputs are uniformly near one subspace.

For comparison only, rho<=I gives worst-case input/reference rejection probability
at most k t, and gentle filtering would bound channel disturbance by O(sqrt(kt)).
Inserting that bound into a fidelity-square-root recovery chain would be needlessly
weak. The following direct Bell-target calculation is the central new interface.

## 3. A direct approximate recovery competitor after filtering

Purify the normalized Choi state of R0 N to |Psi>. Let P be the Bell target
projector on logical output/reference, tensored with identity on all environments.
Then ||(I-P)Psi||^2<=kappa. Include a Stinespring isometry for R0. Conjugating
the retained-output projector Pi through that isometry gives a projection M on
its image (extend by zero on the orthogonal complement). Since the entire source
state lies in that image,

    ||(I-M)Psi||^2=t.

Set u=(I-M)Psi. The pass branch's Bell success is ||P M Psi||^2. Expand:

    ||P M Psi||^2
      =||P Psi||^2-2 Re<P Psi,u>+||P u||^2,
    <P Psi,u>=<Psi,u>-<(I-P)Psi,u>
               =t-<(I-P)Psi,u>.

Cauchy therefore yields

    F_e(R0_ext F)>=1-kappa-2t-2sqrt(kappa*t)
                    >=1-2kappa-3t.                   (3.1)

Here R0_ext agrees with R0 on the retained original-output sector and sends the
flag to any fixed logical state. The failure branch adds a nonnegative Bell
success probability, so discarding it in the lower bound is legitimate. The
purification is solely a proof object, not free accessible side information.

This bound allows an already imperfect recovery, avoids a fourth-root tail/noise
loss, and does not multiply physical source noise by the training count. If
kappa=0, the sharper overlap argument gives F_e>= (1-t)^2. C independently
developed that exact-competitor case; root generalized it to arbitrary kappa by
the cross-term identity above.

## 4. Acquire the actual filtered channel in one common frame

Use the accepted N1291 joint-compression identity on ALL filtered training outputs
and one filtered payload, leaving their external references untouched. Since
the actual F has common support of dimension d<=floor(1/a)+1, the joint state
equals a mixture with ONE latent Haar U on the small output carrier:

    J_(F_U)^tensorN tensor (id_ref tensor F_U)(payload),
    F_U=Ad_U F_small.

This equality holds for arbitrary joint inputs on the common support. The exact
mixed-isometry assumption in N1291 entered only through its perfect competitor,
which(3.1) replaces. Neither U nor a new query port for F_U is given to the learner.
The recovery competitor transported into that common frame is used only in proof.

The ordinary small-space finite tomography, exact TP repair, positivity ridge,
rational physical fallback and conditioned learned-matrix Petz construction can
be applied to the ACTUAL F_U. Carry N1291's factor-two all-accepted inverse floor
and positive-part fidelity correction. On a good record the learned channel
Fhat has half-diamond error<=delta from F_U. If zeta=2kappa+3t, its mathematical
competitor on Fhat has fidelity>=max(0,1-zeta-delta). Barnum--Knill then gives
learned Petz fidelity on Fhat at least that number squared. Returning to actual
F_U loses at most another delta. For all nonnegative zeta,delta the resulting
coarse bound is

    F_e(Petz_Fhat F_U)>=1-2zeta-3delta.

If zeta+delta>1, the right side is already negative and follows from fidelity>=0;
one never squares an invalid negative lower bound. The normalized-Choi estimate
then gives, on good records,

    halfdiamond(Petz_Fhat F_U,id_k)
        <=k sqrt(4kappa+6t+3delta).                   (4.1)

Averaging the actual shared-frame/measurement mixture and paying bad-record
weight beta, plus total reference-safe implementation error gamma, yields

    halfdiamond(decoded,id_k)
      <=k sqrt(4kappa+6tau+12d0 a+3delta)+beta+gamma.  (4.2)

No N-times channel-to-ideal-noise comparison occurs. Training is i.i.d. from
THIS actual F. Only the simulation/compilation approximation to its fixed ideal
filter is divided by the number of training/payload uses.

## 5. A noise-oblivious accuracy schedule

For 0<epsilon<=1 choose, conservatively,

    a=epsilon^2/(192 k^2 d0),
    delta=epsilon^2/(48 k^2),
    beta=epsilon/4, gamma=epsilon/4,
    threshold-gap failure budget q=epsilon/8.

The accuracy-only term in(4.2) is at most epsilon/(2sqrt(2)); adding beta,gamma,q
is below epsilon. Thus the proposed complete operation gives

    halfdiamond(decoded,id_k)
        <=epsilon+k sqrt(4kappa+6 tail_d0(A)).         (5.1)

This is the averaged physical CPTP decoder, including its actual threshold,
training-measurement and controller randomness. It is not a certificate for
every observed classical record or a high-probability guarantee for a reusable
decoder subsequently detached from this batch.

It does not need numerical values of kappa or the tail. It does not verify those
promises or learn an optimal d0. The bound can be vacuous. A useful result still
requires an approximately recoverable source and a sufficiently small intrinsic
mean-output tail.

## 6. Essential acquisition and control ports still being qualified

B's random threshold must be literal finite rational sampling. In[a,2a], there
are at most O(1/a) relevant eigenvalues. A rational grid gives gap-failure bound
O(g/a^2)+O(1/[a M_grid]); hence g proportional to q a^2 and sufficiently large
polynomial M_grid pay a useful gap with probability>=1-q. There is no spectral
value oracle or free decision of equality with an unknown eigenvalue.

The filter must preserve coherence WITHIN its pass subspace: coherently estimate
phase, compute only the binary threshold flag, UNCOMPUTE the phase register and
measure only that flag. Discarding a full eigenvalue estimate would dephase the
retained channel and invalidate(3.1). Controlled density-matrix exponentiation
using fresh A copies and partial swaps can pay reference-safe per-use precision;
its original-source copies, controls and all returned states count. Per-filter
error O(gamma/(N+1)) pays the total training/payload approximation, without an
N*kappa or N*tail term. Source drift is excluded.

The retained dimension grows with inverse epsilon. N1291's fixed-d GT enumeration
does not give uniform polynomial gates here. C's finite Haar-polar port addresses
this: prepare an easy highest-weight GT basis vector, inverse uniform small-d
Schur, then apply ONE sampled finite approximation to a Haar unitary to every
small carrier. Irrep twirling supplies the mixed irrep without enumeration.
Finite Gaussian/polar generation, conditioning, known unitary synthesis and the
same-unitary tensor error must be paid. A finite distribution of unitaries has
TV1 from continuous Haar; a reference-safe CHANNEL coupling is the required
argument. This port is still under independent whole challenge.

Ambient carrier qubits/logD, coherent training storage NlogD, references, source
copy production, small-space matrices, protected payload and total controls are
all substantive resources. No pure state, decoder frame, unknown adjoint, exact
source inverse or physical filtering hardware is silently supplied.

## Status

The substantive prospective result is approximate recovery acquisition from an
opaque actual channel with separate recoverability and effective-rank promises,
at one-batch coherent access. Ordinary spectral simulation, joint compression,
tomography and Petz reversal are fully credited machinery. B/C/A challenge the
remaining filter and uniform-compilation interfaces. Exactness, source hashes
and prior packets alone are not acceptance of this new composition; physical
performance and historical priority remain unestablished.
