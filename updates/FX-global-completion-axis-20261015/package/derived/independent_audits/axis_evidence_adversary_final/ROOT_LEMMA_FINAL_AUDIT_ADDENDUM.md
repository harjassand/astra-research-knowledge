# Independent final audit addendum: order/volume identified set

Date: 2026-10-15. This is a new audit directory. The original worker evidence package, original sources and pinned worktree remain frozen and unmodified.

**Verdict on the reviewed root snapshot: the unrestricted positive-floor theorem, restricted-support qualification, counterexample and sharp numerical intervals are correct. One zero-floor closure sentence requires qualification: joint-pair closure and closure of the fixed-W identified set are different.** A minor notation change and a tautological checker assertion are also recorded below. No acquired physical interface or same-domain rewrite is certified.

## Exact reviewed bytes

The complete snapshot receipt is `ROOT_SNAPSHOT_RECEIPT.json`. The initial reviewed root files have these SHA256 values:

| File | SHA256 |
|---|---|
| `root/ORDER_VOLUME_IDENTIFICATION.md` | `07080c10681d6b43808ce079c03a71f34661f9aef77be16021531fb0c0a1adda` |
| `root/check_order_volume_identification.py` | `58a7ebbd407cd2b23cf4da05c815ed62cc05ee6b92c270c43dea29b31a6b52ef` |
| `root/ORDER_VOLUME_CHECK.json` | `1cf0a319ddbdbe6b5d32b8e7b9bb84fd7ec519ad0d69d7aca4902e3d439d5d46` |

The root bounds-correction receipt links the erroneous displayed bounds to the corrected intervals. The scope-correction receipt records addition of unrestricted support, and the fixture-correction receipt records replacement of accidentally orthogonal rank-one vectors. These records are retained as source history; their existence does not establish any physical result.

## Positive-floor theorem and support scope

For unrestricted unit axes and a common 0<s<1, the inequalities s²M<=W<=M with trace M=f are necessary. They are sufficient because P=(W-s²M)/(1-s²) and R=(M-W)/(1-s²) are PSD, M=P+R and W=P+s²R. Independent spectral atoms at order 1 and s realize these matrices without a common eigenbasis. W must be symmetric PSD; the Loewner inequalities impose symmetry on M and M>=W>=0. The scalar feasibility bounds trace W<=f<=trace W/s² are sufficient for nonzero W by M=(f/trace W)W. If W=0, a positive floor forces f=0 and M=0. At s=1, exact feasibility requires M=W and f=trace W.

The final root text correctly makes the unrestricted-support premise explicit. For a prescribed finite set of axes n_i, the exact continuous-mixture model instead uses M=sum m_i n_i n_i^T, W=sum w_i n_i n_i^T, s²m_i<=w_i<=m_i and sum m_i=f. Sufficiency follows by assigning S_i=sqrt(w_i/m_i) when m_i>0; if m_i=0 the inequalities force w_i=0. The matrix sandwich alone may produce forbidden spectral axes. Known per-parent masses, indivisible grains or coupling between intervention arms require additional constraints. The displayed independent-arm bounds do not impose same-domain coupling.

## Independent sharp-bound calculation

The additive two-arm construction gives M1=M2=diag(1/2,1/2,0), W1=diag(8/25,2/25,0), W2=diag(2/25,8/25,0). The normalized intensity contrast differs by 6/5 while volume-axis reorientation is zero.

For s=2/5 and f=1, pinching in the common diagonal basis of W and T=diag(1,-1,0) preserves feasibility and objective. In arm 1:

    8/25 <= m_x <= 2,
    2/25 <= m_y <= 1/2,
    m_z=0, m_x+m_y=1.

Thus m_x lies in [1/2,23/25] and D1=2m_x-1 lies in [0,21/25]. The endpoint matrices are diag(1/2,1/2,0) and diag(23/25,2/25,0). Arm 2 swaps x and y, giving D2 in [-21/25,0]. Independent arms therefore give D1-D2 in [0,42/25]. Convex interpolation gives every intermediate value. The upper bound on the other coordinate is essential to the zero lower endpoint; the corrected root result includes it.

`check_independent.py` constructs both domain sums explicitly and enumerates all vertices of the box intersected with the trace hyperplane. This is an independent exact calculation, not a copy of root water-filling. All 17 independent checks passed. A byte-identical copy of the root checker was executed inside this new directory; its 17 checks passed without rewriting root outputs.

## Zero-floor exactness and the closure correction

Retain the upper order bound: the premise here is **0<S<=1**, without an acquired common positive lower floor. Over unrestricted axes, the exact feasible pairs satisfy W<=M and ker W=ker M, in addition to symmetry, PSD and trace M=f. Necessity of equal kernels follows because an integral of S²(v.n)² can vanish only when the corresponding volume moment vanishes. On their common finite-dimensional support, a positive minimum generalized eigenvalue supplies an existential floor, so the positive-floor construction proves sufficiency.

There are two different closure statements:

1. **Joint pairs, with W allowed to vary.** Dropping kernel equality gives the closure. Given any W<=M, choose W_epsilon=W+epsilon(M-W). For 0<epsilon<=1, W_epsilon<=M and ker W_epsilon=ker M. These exact positive-order pairs converge to (M,W).
2. **An identified set with fixed supplied W and fixed f.** Dropping kernel equality generally does not give its closure. The exact fiber is already closed. Let K=ker W. Since W is positive definite on K-perp, the exact fiber is equivalently M>=W, trace M=f, and M annihilates K. Those are closed conditions. For fixed f it is also bounded.

For example, fix W=diag(1,0,0) and f=2. The exact fiber contains only M=diag(2,0,0). The broader zero-order point M_bad=diag(1,1,0) satisfies W<=M_bad but is a positive distance from this fiber and cannot be a limit with W fixed. It is a joint limit through W_epsilon=diag(1,epsilon,0). The even simpler fixed fiber W=0,f>0 is empty; its closure cannot become the nonempty PSD trace-f set.

The reviewed root sentence saying that dropping support equality gives "its closure" occurs in a discussion of supplied W and should therefore explicitly say **closure of the joint (M,W) model when W may vary**. This also clarifies the closure language in the earlier frozen worker audit. In a calibrated measurement-uncertainty model W may vary, but the actual allowed uncertainty set must be included; one cannot silently replace a fixed-W exact claim by joint closure.

## Minor checker and notation observations

The root assertion named `unchanged_volume_axis_tensor` currently checks `M==M`. It is tautological; the displayed domain construction proves equality, and the independent checker here explicitly computes both arms. Replacing that assertion would improve check meaning without changing the theorem.

The root document first defines Q=M/f, but its counterexample later calls a normalized intensity contrast D=Qxx-Qyy. Use D_int=(Wxx-Wyy)/trace W there, reserving Q for the volume target, to remove this notation collision.

## Physical and historical boundaries

These are mathematical information operations after f, W and any promised floor or support are supplied. They do not acquire those inputs. Coherent interference, incomplete integration, contamination, intensity scale, local-order heterogeneity and changing sampled material can invalidate the scattering-to-W interface. No raw response establishing that interface, stress-induced retained writing, or same-domain rewrite was acquired in this audit. Even a certified volume-tensor change can be caused by domain replacement or phase growth/loss. The tools are classical linear/semidefinite moment methods; historical novelty and practical experimental efficiency are not established.
