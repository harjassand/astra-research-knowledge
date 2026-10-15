# Coverage of a possible full finite-H projection theorem

This file audits the logical gluing and normalized-contact coverage only.
It does not inspect or assume the proposed current generic-angle proof.
Historical novelty and external correctness are UNKNOWN.

Let V be the full nine-dimensional left-SO(2)-invariant quartic space,
H=(|A|^2-2det A)^2, and pi:V->V/span{H}. Let R and Q denote the global
rank-one-convex and all-background quasiconvex cones, with the usual
bounded Lipschitz-domain W_0^(1,4) formulation (or its smooth test version
followed by strong approximation).

Suppose F+alpha H belongs to R for some finite alpha. Because D2H(I)=0,
q(R)=D2F(I)[R,R] is nonnegative on all real rank-one R.

If q is positive on every nonzero rank-one R, it has a positive minimum
on the compact unit rank-one set. Write a nonzero conformal background as
U=rQ0, with r>0 and Q0 in SO(2). Left invariance and quartic homogeneity
give

    D2F(U)[R,R] = r^2 D2F(I)[Q0^T R,Q0^T R].

Thus strict positivity at I gives uniform strict conformal LH. The
inherited Iwaniec--Kristensen completion corollary gives some finite
beta for which F+beta H belongs to Q.

Otherwise compactness produces a nonzero rank-one R=eta tensor xi with
q(R)=0. Choose P in SO(2) with P^T xi=|xi|e1 and define

    F_tilde(A)=F(P A P^T).

Conjugation preserves I and H, preserves left SO(2) invariance, and
preserves ROC. It preserves QC by the corresponding orthogonal domain
coordinate change and target rotation; the statement quantifies over all
bounded Lipschitz test domains and all admissible perturbations.
The contact becomes

    (P^T eta) tensor e1

up to a nonzero scalar, irrelevant to acoustic vanishing. If the second
component of P^T eta is nonzero, scale it to obtain (t,1) tensor e1.
This gives the trace-free case t=0 and the generic cases t!=0. If that
second component is zero, the contact is e11 (the parallel/nonshear case).
These cases exhaust all nonzero rank-one contacts at I.

Consequently a theorem with the following **exact** scope would suffice:

    For every real t!=0 and every F_tilde in V with contact
    D2F_tilde(I)[(t,1) tensor e1, (t,1) tensor e1]=0,
    if some finite alpha makes F_tilde+alpha H ROC,
    then some finite beta makes F_tilde+beta H QC at every background.

The source quartic may first be restricted to its full critical-contact
span by acoustic stationarity; no other unproved coefficient restriction
may be inserted. The implication must include all ROC-admissible
degenerate/zero boundary cases, both signs of t, and the same test-function
and domain quantifiers. It need not give a bound uniform as t tends to
zero or infinity. The t=0 and parallel cases are handled by the existing
complete shear and nonshear finite-projection theorems.

If those three contact theorems and the strict theorem hold with the
stated scope, then pi(R) is contained in pi(Q). The reverse containment
follows from QC implying ROC, so pi(R)=pi(Q) in the full eight-dimensional
quotient. The range predicate in STRUCTURAL_PROOF.md then characterizes
both finite-completion projections. This would still not equate the
least ROC and QC alpha for a prescribed class, nor prove that every raw
ROC quartic is QC.

No coverage gap or additional contact type occurs in this gluing logic.
The remaining obligation is the actual universal generic-angle theorem
with all the hypotheses and boundary cases above.
