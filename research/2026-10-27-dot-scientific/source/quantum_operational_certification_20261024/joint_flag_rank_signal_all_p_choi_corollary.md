# All-real-p joint rank/signal Choi lower bound by known erasure dilution

2026-10-27. Corollary candidate, independent audit requested. No stronger adaptive physical-query lower bound is inferred.

Fix any integer r>=1 and any real0<p<=1. Set

 D=floor(r/p), p'=r/D>=p, c=p/p'=pD/r.

Since floor(x)>=x/2 for x>=1, D>=r/(2p) and c>=1/2. Use the canonical integer-grid rank-r channel E_(p',U) from `joint_flag_rank_signal_choi_lower_bound.md` on a3D-dimensional output block. Add one fixed orthogonal output vector |e> and define

 E_(p,U)=c E_(p',U)+(1-c)Tr(·)|e><e|.

Its success probability is exactly p, its mixed success flag still has rank r, and its reset is orthogonal to the whole success code. Its output dimension is3D+1. At p=1 the extra sector has zero weight and can be omitted.

The channel family still has Delta=0: the original canonical block contributes c times its homogeneous zero deficit, while the extra replacement block has zero deficit separately. This is a direct-sum calculation, not a general mixed-input value theorem.

## Exact program/data simulation

The known receiver channel C acts as the identity embedding with probability c and otherwise replaces the state by |e>. Then E_(p,U)=C composed E_(p',U). One normalized Choi copy of the diluted source is exactly

 (id_A tensor C)(J_(p',U)),

and one diluted datum is C applied to the corresponding canonical datum. Thus any n-program learner for the diluted family can be simulated using n canonical Choi copies, the same independent canonical datum, and known coins. No U-dependent correction or additional program copies are needed.

If that learner approximates p identity+(1-p)erasure within complete unhalved error at most nu p,0<nu<=1/4, its accepted classical label information is at least p/4 by the received conditional-Fano lemma. The canonical entropy-increment bound remains

 I(label:canonical programs,data)<=1024r n/(9D³).

Consequently

 n>=9pD³/(4096r)=9cD²/4096
   >=9r²/(32768p²).                                (1)

The extra coin/erasure processing can only reduce accessible label information, so the comparison direction is correct.

This establishes the quadratic joint rank/signal lower exponent for EVERY real p in the full-Choi-program model on an explicit orthogonal-reset mixed-flag subclass. Together with the rank-bounded soft-threshold receiver, the fixed-relative-accuracy exponents r²/p² match up to logarithmic factors (with p0 chosen at the relevant worst-case success scale). Numerical constants and accuracy dependence are not asserted optimal.
