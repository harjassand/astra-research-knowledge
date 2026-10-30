# Connector-mediated launch returns: the missing block estimate

Binding completion of the carried-face candidate. The small true-F fast return is NOT by itself sufficient: a traced episode can end at a connector with mixed D=0. This note adds that output explicitly. Constants below concern a fixed finite profile/degree list; all kernels retain actual phase and initial-phase-left flags.

## 1. A fixed launch head receives a small traced connector measure

Fix any finite M. Let Q_R be the positive-D-start first-connector kernel, including every actual output, mixed or not. For each requested s,

    Q_R[ f_s(A_out) 1_{A_out<=2M} ] <= epsilon_n(M,s) f_s(A_in),
    epsilon_n(M,s) ->0.                                      (2)

This is not asserted for all outputs. To derive it, split inputs at J=C log²(2+n). For A_in<=J, the absolute terminal inverse-profile reset bounds the left side by C n^-eta; division by f_s(A_in) loses only (1+J)^s. For A_in>J, the acquired original-A cohort estimate bounds an output below2M by poly(n)exp(-c A_in), once J>4M. Multiplication by (1+A_in)^s is harmless because A_in<=n+a0. Use localization for the actual first-connector/clearing terminal and its bounded A jump. Thus (2) holds uniformly in the actual phase b. The same derivation applies to every fixed larger profile required by a graded continuation.

In W_s, the first connector multiplies exp(lambda B+theta r) by one of finitely many fixed factors; its r change is the known neutral connector change at a fixed input phase. Consequently (2) remains small for fixed lambda,theta. In particular it includes R-to-mixed-L connector outputs. No such output is substituted by R_F.

## 2. A high launch cannot fall into the head for free

Let H_M={D=0,A<=M}. From a launch input A>2M, stop the PURE launch path at its first seed/restoration, section/designated stop, or entry to H_M. The accepted high-A marked-block proof gives

    K_high,head W_s <= delta_M W_s,    delta_M ->0.             (3)

Here is the quantitative reason. Above M, a clearing block includes its ensuing low-phase approach. To reach A<=M from A>2M requires at least M/m ordinary clearing blocks, because only clearing decreases A on the seed-free path. Every block survives the independent seed mark with fixed probability 1-p<1. For M large, the weighted high-birth/low-race perturbation changes its continuation norm by O(1/M), leaving a fixed rho<1. The profile ratio during the crossing is already included in this block norm. Summing the tail of at least M/m surviving blocks gives C rho^(M/m). Additional restoring killing only removes paths. Section/designated stops also only remove paths. This proves (3), rather than supposing a high launch has an instantaneous reset. Rare births are included in the block generating function, not omitted as unweighted errors.

Combining (2), (3), and the fixed-b profile bound yields the explicit connector-mediated estimate

    Q_R [actual subsequent pure-launch path to H_M]
          <= [epsilon_n(2M,s) + C_s delta_M] W_s.             (4)

Outputs with D>0 simply continue as regular inputs and are not counted in this head-return kernel. Actual true-F returns before a connector are added separately with their already small n^-eta profile norm.

## 3. Order of choices and regular-phase contraction

There must be NO argument that exp(-lambda q) C_launch(lambda) tends to zero. Instead:

1. Fixed-b first-connector profile constants C_s are earned BEFORE adding the B tilt, so they are independent of lambda. A high-phase ordinary clearing, with its actual low approach if necessary, lowers the leading B phase by at least one; the low approach changes A only upward. The finite regular-phase leading norm is therefore at most C_* exp(-lambda), where C_* uses these fixed-b constants and the finite grade list, not the full launch Green.
2. Choose lambda with C_* exp(-lambda)<1/4. Then fix the already-earned FULL launch Green/envelope constant C_launch(lambda), which is finite uniformly over every initial A and every restoring hazard. It is an actual global operator bound; its value does not need to be recomputed when a later analytical threshold M is increased.
3. Choose M large. On the regular domain (positive D or high-A launch), a launch's seed/restoration before its first connector enters positive D with unchanged A or a loss at most2, hence profile ratio 1+O(1/M). No full launch Green is multiplied into this leading first-connector row. The remaining high-launch rare birth/low-race terms are O(1/M) with fixed tilt factors, and (3) makes the pure launch descent to the head small. Choose M so these errors and C_launch C_s delta_M fit the available margin.
4. Finally choose the residual exterior cutoff so all R resets, true-F errors, and the fixed-M connector-to-head epsilon_n terms, multiplied by the now FIXED C_launch and regular-phase resolvent constants, fit the remaining margin. Since n>=r-O(1) on the retained exterior phase states, the choice is uniform. Actual exits from that exterior are designated terminal outputs, as in the accepted processor.

An initial low launch is preconditioned by its full non-small launch Green; seed/restoration exits enter the regular row with bounded norm C_launch. Regular-row returns to the launch head have total norm bounded by (4), true-F errors, and the already counted high-launch errors. Their product with C_launch is small by the stated order. Thus the positive block inverse exists on the lifted actual state space. All subsequent phase continuations are summed by this inverse; they are not inserted as an uncontrolled C(lambda) at each clearing. This is the required connector-mediated L-to-R-to-L head estimate AFTER arbitrary phase continuation: the one-pass bound is multiplied by the finite regular resolvent, and the head-loop is a convergent Neumann series.

## 4. From the fixed processor head to logarithmic bad section outputs

The fixed M head is only a construction device for the phase Green. The final signed-section bad set still uses A<=K(r)=C log²(2+r). For fixed-b R outputs into that growing bad set, the proof of (2) works with J a sufficiently larger multiple of log² n; alternatively use a larger terminal inverse profile to pay K's fixed powers before the input split. It gives a vanishing weighted connector measure on the actual bad output. The unrestricted complete-cycle inverse-profile identity then bounds all remaining corrected outputs, and the actual-output inequality

    (1+r_out)^(-eta) <= epsilon0 f_m(A_out)

on bad positive-D outputs supplies the old small cross block. No replacement of output residual by input residual is permitted. The source and negative event estimates in the main note therefore apply after this repaired processor, not before its existence has been earned.

This completion is a proposed proof, subject to independent review alongside the main note. It explicitly replaces the main note's overly abbreviated assertion that small R_F alone suffices for the full phase construction.
