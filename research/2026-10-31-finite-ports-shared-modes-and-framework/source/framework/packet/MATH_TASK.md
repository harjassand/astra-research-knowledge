# Exceptional polynomial face: scientific task and fixed capital

Find the strongest correct resolution of a genuinely unresolved quasiconvexity problem. For A=(a,b;c,d), let T=|A|^2, D=det(A), and

F_s=T^2-4sTD+(6s^2-2)D^2.

Fix s=1/3 and consider every polynomial p(A)=F_(1/3)(A)+C(A)+Q(A)+L(A)+d, where C is any homogeneous cubic and Q any homogeneous quadratic in the four entries. Affine terms do not affect the question. ROC means rank-one convex on all R^(2x2); QC means the usual inequality for all means and actual compatible gradient test fields, not free probability measures on matrices.

The central question is whether ALL globally ROC p in this fixed-leading face are QC. Seek a structural resolution: a compatible QC construction/classification or a genuinely ROC polynomial and an actual gradient energy violation. Obtain the sharp lower-quadratic membership structure for the nontranslation modes as part of a useful positive resolution. You own the representation and may introduce new objects or principles. A correct nontrivial intermediate theorem is worth retaining, but the central question remains visible.

What is ALREADY known and supplied equally:

* F_(1/3)=(T-2D)(T+(2/3)D). The conformal null geometry and this factorisation are preliminaries, not the requested discovery.
* F_s is QC for |s|<=1 by the primary compatible heat certificate. The full homogeneous quartic ROC ray is exposed for |s|<1, including s=1/3.
* For |s|<1 excluding +/-1/3, the admissible cubic kernel is exactly the four translation cubics DF_s:V. Hence every ROC polynomial has unique form cF_s(A+V)+Q_reduced+affine, with Q_reduced ROC; the entire 20D face is QC. At s=1/3 the cubic kernel has dimension EIGHT, so this theorem does not cover four additional modes. Their existence and rank are already known. Do not silently apply the rigid theorem at its exception.
* The acoustic pairs are R=u tensor v and K=U diag(s,1)V^T, where U=(x,-y;y,x) for u=(x,y) and similarly V for v. Admissible cubics obey grad C(R) dot K=0 for every pair. The standard-library rotational receiver reconstructs the whole cubic map. Its certificate and exceptional ranks are included.
* A general exact ROC elimination is already known: p''(A)[R,R]=A^T H_F(R) A+2 grad C(R) dot A+2Q(R), H_F(R)=F''(R). For every rank-one R one needs grad C(R) in range H_F(R) and 2Q(R)>=grad C(R)^T H_F(R)^+ grad C(R). Limits near singular acoustics must also be respected. Merely restating this infinite inequality is not a sharp new effective classification.
* A general COMPATIBLE moment reduction is already known. For an actual periodic gradient G=Dphi with mean zero, write H=<F''(G)>, v=<DF(G)>, w=<DC(G)>, f=<F(G)>, c=<C(G)>, q=<Q(G)>. All background means and amplitudes are safe iff [[H,v,w],[v^T,2f,c],[w^T,c,2q]] is PSD. Given QC F and ROC p, the remaining condition is r^2<=ab with a=2f-v^T H^+v, b=2q-w^T H^+w, r=c-v^T H^+w. This criterion and its witness reconstruction are supplied, not a new solution. The exact eight-mode detector in the sibling source concerns a DIFFERENT leading quartic and cannot be imported at s=1/3 by similar vocabulary.

Read governing sources as needed under this packet's `math/` directory: `rotational_faces/PROOF.txt`, `receive.py`, `classify.py`, `certificate.json`; `quadratic_boundary/PROOF.txt` and its operation sources; required `hopf_structure/` helpers; and `primary_appendix.html` (Bruno--Pasqualotto, arXiv:2608.06367v1). Original source bytes and provenance are in `SOURCES.txt`. Imported homogeneous QC and earlier translation-normal-form arguments retain their source credits.

Do not supply a correction-selector oracle, assume a pointwise minimizer is a gradient, replace compatibility by arbitrary matrix distributions, or call a non-ROC negative fixture a separation. Numerical searches can discover candidates; consequential claims need a valid proof/certificate or an actual compatible counterexample at their stated scope. A finite list of passing fields is not global QC. A positive answer here does not settle general Morrey; a genuine planar ROC/non-QC example would have much larger consequences.

Develop one substantial result, using the strongest available approach. Keep the target fixed while revising internal representations when useful. An unfinished but rigorous construction is preferable to an unsupported complete claim. Preserve both successful and failed scientific attacks in ordinary proof/code artifacts.
