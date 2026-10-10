# Fresh primitive attempt: finite repair composition

Date: 2026-10-10. Status: **closed after acquisition falsification**.

This attempt did not produce a new foundational capability. Its useful result is a precise reason to reject one proposed operation before investing in an abstract theory around it.

## Proposed operation and intended capability

The intended capability was to solve a coupled nonlinear constraint or optimization problem by a prescribed finite sequence of cheap local repairs, with no contraction-rate dependence and no global solve hidden in the repairs.

The candidate operation was a *repair sweep*: compose idempotent maps R_i whose fixed sets express the desired local conditions, assuming distant maps commute and neighboring maps satisfy

    R_i R_(i+1) R_i = R_(i+1) R_i R_(i+1).

These are the familiar 0-Hecke relations. The longest-element product in type A has n(n-1)/2 factors and absorbs each generator, so its output is fixed by every repair. **That algebra is established, not an invention here.** The important acquisition question was whether natural local solvers for consequential coupled systems satisfy the relations.

They generally do not, already for smooth strongly convex optimization. Relaxing the relations to small error does not rescue a uniform correctness guarantee.

## 1. Known projection lemma

Let P,Q be orthogonal projections on a real or complex Hilbert space. Then

    PQP = QPQ  if and only if  PQ = QP.

Proof of the nontrivial direction: put C=(I-Q)PQ. Then

    CC* = (I-Q)PQP(I-Q) = (I-Q)QPQ(I-Q) = 0.

Hence C=0, so PQ=QPQ; taking adjoints gives QP=QPQ.

This exact result is established: Bikchentaev (2008), Theorem 4.3, states the equivalence and credits earlier work. No novelty is claimed for this lemma.

## 2. Acquisition obstruction for nonlinear local minimizers

Let F be C² near a minimizer x*, with positive-definite Hessian H at x*. Let U be a full-column-rank matrix specifying a local update subspace. Assume the local minimizer map

    R_U(x) = argmin { F(z) : z in x + range(U) }

is defined near x*, with the branch near x*. Strong convexity locally and the implicit function theorem suffice for the local statement; global strong convexity suffices for a globally unique map.

Writing R_U(x)=x+U a(x), its first-order condition is

    Uᵀ ∇F(x+U a(x)) = 0.

Differentiate at x*, where a(x*)=0:

    D R_U(x*) = P_U := I - U(UᵀHU)^(-1)UᵀH.

P_U is idempotent and self-adjoint in the H inner product. It is the H-orthogonal projection onto the H-orthogonal complement of range(U).

If two such maps R_U,R_V satisfy the braid relation in a neighborhood of x*, then differentiating the identity at their common fixed point gives

    P_U P_V P_U = P_V P_U P_V.

The known projection lemma forces P_U P_V=P_V P_U.

**Consequence:** generic coupled coordinate or block minimizers cannot furnish the required repair algebra. The proposed finite sweep would demand a special compatibility already at first order. This is an application of established projection geometry, not a claim of a new general theorem.

### Exact two-variable counterexample

Take

    F(x,y) = (x² + 2ρxy + y²)/2,   0 < |ρ| < 1.

Its Hessian is positive definite. Exact coordinate minimizers are

    R(x,y)=(-ρy,y),   S(x,y)=(x,-ρx).

Their matrices P,Q obey

    PQP=ρ²P,   QPQ=ρ²Q.

They do not satisfy the braid relation for nonzero ρ. At ρ=1/2 and initial point (0,1),

    RSR(0,1)=(-1/8,1/4),   SRS(0,1)=(0,0).

The first result has F=3/128, while the unique optimum is zero at (0,0). No finite sequence consisting solely of these exact coordinate repairs can reach (0,0) from a point with both coordinates nonzero: each update preserves nonzero coordinates when ρ is nonzero. This does not rule out algorithms using additional operations.

## 3. Small braid error does not certify closeness to a common solution

This failure does not require a changing norm or nonlinear maps. In Euclidean R² let P project onto span(e₁), and Q project onto span(q), with

    q=(cos θ,sin θ),   0 < θ < π/2.

Write c=cos θ and s=sin θ. These are exact idempotent nonexpansive repairs. Their common fixed set is {0}, and

    PQP=c²P,   QPQ=c²Q,
    ||PQP-QPQ||₂=c²s.

For the proposed three-step sweep W=PQP and unit input e₁,

    W e₁=c² e₁,
    distance(W e₁, Fix(P) ∩ Fix(Q))=c²,
    ||P W e₁-W e₁||=0,
    ||Q W e₁-W e₁||=c²s.

As θ tends to zero, the braid defect and every local residual tend to zero, but distance to the common solution tends to one. Therefore there is no bound tending to zero that converts small braid defect alone into distance-to-feasibility after this sweep, even in dimension two.

The iterative version is equally explicit: for unit q in range(Q),

    (QP)^k q = c^(2k) q.

For every fixed number of sweeps k, the error tends to one while the braid defect tends to zero. Any rescue needs a separately acquired intersection-regularity or angle bound. Charging that missing global information to a new primitive would not solve its acquisition problem.

The angle dependence is standard alternating-projection geometry. This example is used to falsify the proposed approximate repair certificate, not claimed as a new discovery about projections.

## Sources checked

1. A. M. Bikchentaev, *On the representation of elements of a von Neumann algebra in the form of finite sums of products of projections. III. Commutators in C*-algebras*, Sbornik: Mathematics 199:4 (2008), 477–493. Theorem 4.3, page 484, includes PQP=QPQ iff PQ=QP. Primary publisher/archive record: https://www.mathnet.ru/sm3851 . DOI: https://doi.org/10.1070/SM2008v199n04ABEH003929 . Indexed primary full text: https://www.mathnet.ru/php/getFT.phtml?jrnid=sm&paperid=3851&what=fullteng .
2. SageMath's implementation documentation gives the defining 0-Hecke projection, braid and commutation relations. https://sporadic.stanford.edu/reference/monoids/sage/monoids/hecke_monoid.html . This is official implementation documentation, not the original discovery source.
3. S. Kayalar and H. L. Weinert, *Error bounds for the method of alternating projections*, Mathematics of Control, Signals, and Systems 1 (1988), 43–59, DOI https://doi.org/10.1007/BF02551235 . The article identity was verified; full primary text was not retrieved. The explicit two-dimensional calculations above are self-contained and do not rely on an uninspected theorem from it.
4. S. Reich and R. Zalas, *The optimal error bound for the method of simultaneous projections*, primary research record https://arxiv.org/abs/1704.00308 and journal https://www.sciencedirect.com/science/article/pii/S0021904517301065 . This identifies the standard Friedrichs-angle context and attributes the alternating-projection equality to Kayalar and Weinert.

## Reproduce

Run `python independent_programme/fresh_primitive_20261010/verify_repair_obstruction.py` from the workspace root. The script checks exact rational identities, tests every repair word through length 12 on a point with both coordinates nonzero, and checks the explicit small-angle formulas. It writes `verification.json` beside itself. The mathematical proofs above establish the general statements; finite tests are supplementary.

## Decision

Close this candidate. Do not expand it into a specialist approximate-identity paper and do not report the standard 0-Hecke absorption law as new elimination power. A further attempt should begin with an independently consequential problem class and an operation that supplies its missing capability, with acquisition cost explicit.
