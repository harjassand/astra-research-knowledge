# Earned scientific checkpoint

The fixed task is `packet/MATH_TASK.md`: resolve QC for the entire exceptional s=1/3 ROC polynomial face. The central question is still open. Original proof and code for this attempt are frozen beside this capsule; read `REPORT.md` and `verify.py` for the exact constructions. These are scientific assets rather than a required next method.

Coordinates x=(a+d,c-b), y=(a-d,c+b), eta(y)=(y1^2-y2^2,2y1y2), J(y1,y2)=(-y2,y1) give F0=3F_(1/3)=2|x|^2|y|^2+|y|^4. Work with P=3p. After removing the four argument-translation cubics, the extra cubic is C_M=x dot M eta(y), with arbitrary real 2x2 M. The complete cubic space is x dot[tau|y|^2+M eta(y)]+(beta dot y)(|x|^2+|y|^2). The four M coordinates are genuine nontranslation modes.

For unit u,v the rank-one condition is |u|=|v|=1. The derived sharp global ROC criterion is

Q(u,v)>=|M eta(v)|^2/8+(u dot M J eta(v))^2/4.

The completed-square identity and explicit minimizing background are in REPORT.md §3. For block-diagonal Q=x^T A x+y^T D y, the criterion is a 2x2 homogeneous binary quartic matrix being PSD; three exact univariate tests of degree <=4,4,8 give a finite membership operation including weak boundaries. For a full cross quadratic the same inequality is exact, but the original attempt did not simplify its two-angle elimination into a comparable finite classifier.

For Q=nu(|x|^2+|y|^2), the exact ROC threshold is (2 sigma1(M)^2+sigma2(M)^2)/16. For M=I it is 3/16. Below that threshold the explicit Hessian witness is NOT a QC separation because ROC already fails.

A compatible heat certificate was constructed for C=Re[kappa conjugate(X)Y^2], X=x1+i x2, Y=y1+i y2, when nu>=|kappa|^2/4. It factors the primary leading corrected density into three complex squares and supplies a closed linear cubic two-form and a constant quadratic correction. For kappa=1 it yields QC for nu>=1/4.

There is also a proved obstruction: with that PRIMARY leading heat correction fixed, no closed linear cubic correction and constant quadratic correction can certify nu<1/4. Symmetry reduces every allowed cubic correction to one parameter, and exact degenerating compatible jets prove the bound. This is a pointwise-certificate barrier, not an integrated compatible negative-energy field, not a QC violation, and not a theorem excluding another leading primitive or non-heat proof.

The concrete open family is F0+Re[conjugate(X)Y^2]+nu(|x|^2+|y|^2), 3/16<=nu<1/4. The full target also contains the other two M directions and all cross quadratic terms. The packet's general Schur/moment criteria and inherited factorization/kernel count remain predecessors.

Root read the complete argument and reran `verify.py` successfully, including exact cubic maps, completed squares, threshold cases, closed forms and the full fixed-leading correction family. That is a source-exposed scoped check, not historical-priority evidence. No numerical search or finite field list establishes global QC.

Continue the same central scientific question from these earned facts. The exact proofs, successful constructions and failed certificate class are available equally in this checkpoint to all continuations; no sibling result or next method is supplied.
