# Joint flag-rank/signal quadratic upper at exact erasure

2026-10-27. New finite construction, independent receipt requested. It matches the joint lower exponent only in the full-Choi-program model; its implementation also uses weaker ordinary labelled mixed training.

## Source and exact band geometry

Use the integer-grid family in `joint_flag_rank_signal_choi_lower_bound.md`:1<=r<=D,p=r/D, unknown Haar/unitary U on C3 tensor CD, active flag projector P_r, orthogonal reset on its complement. Haar randomness is NOT needed for the upper bound; it holds uniformly for every U.

The Choi state and contrast are

 J_U=(I_A tensor U)[Phi_3 tensor P_r/D+I9 tensor(I-P_r)/(9D)](I_A tensor U*),
 omega=I_(9D)/(9D), H_j=4T_j-6omega=J_j-3omega.

The nine known A-Weyl rotations have mutually orthogonal positive bands P_j of rank r. Their eigenvalue is2/(3D). On the other active-code Bell directions the eigenvalue is-1/(3D); on reset it is-2/(9D). The common code projector Q=sum_j P_j has rank9r.

Every program T_j and omega commutes with Q, and

 Tr(Q T_j)=Tr(Q omega)=p.

Indeed T_j has eigenvalue1/(3D) on its positive band,1/(12D) on the other8r code directions, and1/(9D) on reset; omega is uniform. Known A-Weyl/control gates preserve Q.

Each ideal corrected band component has Bell-contraction Kraus V_k*/3, where V_k|a>=U|a,k> for active k. The nine bands therefore recover the entire success subsystem exactly and reject reset exactly. The ideal complete target is

 p identity+(1-p)erasure.

No individual flag is identified or supplied to the learner.

## 1. Explicit coherent classifiers and resource cap

Fix0<xi<=1 and set

 L=max(1,ceil log_16[900/(p xi)]),
 eta=(xi/(100L))²,
 M=2^m the least power of two at least768D,
 R=ceil log_2(1/eta),
 S=9LR pi(M-1).

For each label run L fresh coherent QPE classifiers, accepting that label only if all L pass. Rejection retains A,B and advances to the next label. The first accepted label receives its known Bell correction; after all nine fail, erase.

A classifier uses R finite-QPE runs for exp[i pi(H_j+I)/2], with acceptance interval[1/4+1/(12D),3/4), reversible majority, copied decision bit, and coherent uncomputation. Its eigenphase separation from the decision boundaries is at least1/(12D). The complete ideal retained-data binary instrument is within4sqrt(eta) of its Lueders band measurement. In particular coherence WITHIN rank-r bands and within rejection is preserved to that accuracy.

Forward controlled times are(pi/2)2^a, with opposite reverse times. For each controlled time t use

 N_t=ceil[10^6 |t| S/xi]

fresh signed rounds, angles4t/N_t,-6t/N_t. Their total squared pair time Htot obeys

 Htot=sum delta²<=xi/10^6.

The ordinary training cap is

 n_train<=2*10^6 S²/xi+36LRm.                        (1)

Every round consumes one T_j and one omega program, each available from one ordinary labelled physical call or one full Choi copy. Negative times use fresh programs, not inverse preparation. The original noisy datum is one additional call.

## 2. Genuine-code complete error

There are at most9L ideal classifiers. Their complete retained-data instrument errors telescope to at most36Lsqrt(eta)=0.36xi. The signed-pair simulator contributes at most256Htot<=0.000256xi. Thus the complete actual receiver differs uniformly from the ideal band receiver by less than0.361xi on arbitrary code inputs with references. Multiplying by original success mass p gives less than0.361p xi.

A uniform diamond bound is used ONLY on this weight-p branch, not on all reset mass.

## 3. Reset: exact common-sector accounting

Initially reset is supported outside Q. Since programs commute with Q and all known gates preserve it, the exact controlled-collision formulas preserve JOINT Q/complement block diagonality, including all controls and references. Virtual Q measurements can therefore be inserted for analysis without changing the actual state; Q is not implemented as an oracle.

For one controlled partial-SWAP of angle a, an outside input imports Q population with probability at most p sin²a. The identity/swap cross term vanishes between the orthogonal sectors. Summing first-import histories over all collisions bounds total import probability by

 p sum[sin²(4delta)+sin²(6delta)]<=52p Htot
 <=0.000052p xi.                                    (2)

Condition on histories with no import. They form positive CP submaps and remain outside Q. For one fresh classifier, ideal outside acceptance is at most eta, while its simulation error contributes at most256h, where h<=Htot/(9L). The no-import accepted submap is bounded by the full accepted submap, so its acceptance probability is at most

 beta=eta+256h<1/16.

This statement is uniform for arbitrary outside joint states and retained auxiliaries. Consequently all L passes for one label have no-import mass at most beta^L. Across nine labels,

 Pr(reset accepted without import)<=9beta^L
 <=9*16^(-L)<=p xi/100.                             (3)

Earlier rejected labels do not invalidate this: on no-import histories their retained data remains outside the common Q, and all subsequent program batches are fresh.

Equations(2)-(3) give total reset accepted mass less than0.010052p xi. Its complete output error relative to erasure is twice that mass, less than0.020104p xi.

## Complete result and matched scoped exponent

Combining both original-source branches, the actual complete receiver has target p identity+(1-p)erasure and unhalved diamond error less than

 0.382p xi <p xi.                                   (4)

All reject paths are included; accepted labels are corrected and discarded. Rank-r coherence is preserved by coherent classification/uncomputation, and the reset estimate uses exact sector invariance, not an invented whitening or support measurement.

For fixed relative xi, (1) scales as O(D²) times logarithmic factors, namely O(r²/p²) on p=r/D. The companion Choi-program lower bound gives Omega(D²). Thus the joint rank/signal exponent is matched in the full-Choi-program model.

The upper is available through ordinary labelled calls as well, but no matching quadratic lower bound for arbitrary adaptive physical queries is claimed. Nor is the accuracy dependence optimality, reusable-decoder amortization, or a nonzero-deficit mixed-success theorem asserted.
