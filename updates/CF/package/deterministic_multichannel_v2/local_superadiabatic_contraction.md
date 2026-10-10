# Local superadiabatic contraction from height-free projector bounds

Date: 2026-10-09. Status: derived analytic construction and local propagator estimate. It supplies the local normal form, not a completed complexity proof for evaluating it or a treatment of crossing cores.

Companion result: algebraic_rotation_gap_lemma.md proves the required original projector and relative-gap bounds on radius R=d/poly(n,p).

## 1. Hypotheses and notation

Let H(z) be holomorphic on D(x,R), Hermitian for real z, with analytic individual spectral projectors P_i(z), i=1,...,r<=n. Allow persistent eigenvalue multiplicities, with each P_i projecting onto the full eigenspace. Assume

    ||P_i(z)|| <= 2.

Fix a partition of the indices into A<=n clusters S_a. Also assume

    ||P_a(z)|| <= 2,  P_a=sum_{i in S_a}P_i,
    |lambda_i(z)-lambda_j(z)| >= g
       whenever i and j belong to different clusters.

All these bounds hold throughout the disk. The companion algebraic theorem supplies them from a center gap g0 with g=g0/2. There is no assumed bound on ||H||/g.

For a small holomorphic perturbation E, denote the continued cluster projector of H+E by P_a(E). Define

    K(E) = i sum_a P_a(E)' P_a(E).

If E is Hermitian on the real interval, K(E) is Hermitian there.

## 2. Contours give a norm-independent projector perturbation bound

At each fixed z, surround a designated cluster by the union of disks of radius g/4 about its eigenvalues. Let Gamma_a be the full oriented boundary of that union, including boundaries of holes if present. This is a finite collection of circular arcs; tangencies can be treated by a limiting contour. Its total length is at most

    length(Gamma_a) <= (pi/2) n g.

Every point of Gamma_a is at distance at least g/4 from every eigenvalue of H: it is outside all open selected disks, and every unselected eigenvalue is at distance at least g-g/4=3g/4 from the center generating any boundary arc. The original resolvent has the spectral representation

    R_0(zeta) = (zeta I-H)^(-1)
              = sum_i P_i/(zeta-lambda_i).

Hence ||R_0||<=8n/g on Gamma_a. If ||E||<=g/(16n), the Neumann series yields

    ||R_E(zeta)|| <= 16n/g.

For two such perturbations E,F, the resolvent identity and Riesz integral give

    ||P_a(E)-P_a(F)||
      <= [length(Gamma_a)/(2pi)] (16n/g)^2 ||E-F||
      <= (64 n^3/g) ||E-F||.                    (1)

Using one original resolvent improves the E-versus-zero estimate to

    ||P_a(E)-P_a|| <= (32 n^3/g)||E||.         (2)

These constants depend polynomially on n and do not depend on the diameter of a cluster, the total spectral width, ||H||, or any within-cluster gap. In particular, the contour need not be a single circle enclosing the whole cluster. The union-of-small-disks construction avoids spectral-diameter dependence.

The projectors are holomorphic in z: a contour can be fixed near any one z, while homotopy H+sE, 0<=s<=1, identifies the same selected cluster throughout the disk. The resulting local Riesz projections agree on overlaps.

Choose the smaller invariant perturbation ball

    eta = g/(128 n^3).

Then (2) gives ||P_a(E)||<=2.25<3 for ||E||<=eta, and all resolvent hypotheses hold.

## 3. The connection map is Lipschitz after one Cauchy loss

Suppose E,F are holomorphic and bounded by eta on a disk D_outer, and D_inner is concentric with radius smaller by h>0. Cauchy's estimate, (1), and the bound 3 give

    ||P_a(E)'||_inner <= 3/h,
    ||P_a(E)'-P_a(F)'||_inner
        <= (64 n^3/(g h)) ||E-F||_outer.

Use

    P_a(E)'P_a(E)-P_a(F)'P_a(F)
      = (P_a(E)'-P_a(F)')P_a(E)
        +P_a(F)'(P_a(E)-P_a(F)).

Summing A<=n clusters proves

    ||K(E)||_inner <= 9n/h,
    ||K(E)-K(F)||_inner
        <= (384 n^4/(g h)) ||E-F||_outer.      (3)

When E=0, the original bound 2 gives ||K(0)||_inner<=4n/h.

## 4. Iteration, domains, and invariant bounds

Spend a fixed initial strip before starting the equal-width iteration. Since the original projectors have norm at most 2 on D(x,R), Cauchy gives

    ||K_0||_{D(x,3R/4)} <= 16n/R.

This avoids an unnecessary factor N in the final connection amplitude. Fix an integer N>=1, set delta=Omega^(-1), and define

    h = R/(4N),
    D_j = D(x,3R/4-jh),  j=0,...,N.

Thus D_N has radius R/2. Put K_{-1}=0. Let P_0a=P_a and K_0=K(0), with K_0 considered on D_0. Recursively, for j>=1,

    H_j = H-delta K_{j-1}      on D_{j-1},
    P_ja = cluster projector of H_j on D_{j-1},
    K_j = i sum_a P_ja' P_ja  on D_j.

Assume

    Omega g R >= 4096 n^4 (N+1).              (4)

Set

    q = 384 n^4/(Omega g h)
      = 1536 n^4 N/(Omega g R) <= 1/2.

An invariant-ball and geometric-series induction gives both

    ||K_j||_{D_j} <= 32n/R,
    ||K_j-K_{j-1}||_{D_j} <= (16n/R)q^j.     (5)

Here are the bootstrap details. If ||K_{j-1}||<=32n/R, (4) implies delta||K_{j-1}||<=g/(128n^3)=eta, so the projector perturbation bounds apply to H_j. Apply (3) on D_{j-1} with an h-wide loss, comparing E=-delta K_{j-1} and F=-delta K_{j-2}. This yields the contraction factor q for their connection difference on D_j. Summing the resulting geometric series together with the original bound 16n/R gives ||K_j||<=32n/R and closes the induction. For j=1 the comparison is with F=0.

Thus every H_j stays in the invariant perturbation ball about H and every P_ja is bounded by 3. No algebraicity of the iterated H_j or P_ja is used. Crucially, their connection amplitudes are O(n/R), independent of N. The numerical constants are conservative and not optimized.

## 5. Exact intertwining and propagator error

For any differentiable complete orthogonal family P_a on the real line, define S=sum_a P_a'P_a. Differentiating sum_a P_a^2=I shows S*=-S, so K=iS is Hermitian. Differentiating P_aP_b=delta_ab P_a gives

    [S,P_a]=P_a',  hence [K,P_a]=iP_a'.

Therefore the Hamiltonian

    H_ad,N = H_N + delta K_N
           = H + delta (K_N-K_{N-1})

generates an evolution that exactly intertwines the spectral subspaces of H_N. Explicitly, if

    i V'=Omega H_ad,N V,

then V(t,s)*P_Na(t)V(t,s)=P_Na(s).

Both this evolution and the original iU'=Omega H U are unitary along the real line. Duhamel's inequality therefore contains no exponentially growing Gronwall factor. On any real panel of length ell<=R contained in D(x,R/2), with identical initial data,

    ||U-V|| <= ell ||K_N-K_{N-1}||
             <= (16n ell/R) q^N
             <= 16n 2^(-N).                  (6)

Choosing N>=ceil(log_2(16n/epsilon)) makes this error at most epsilon. Thus the local analytic decoupling threshold is polynomial in n,p and logarithmic precision after using R=d/poly(n,p). The Kato transport generated by K_N has action at most 32n on such a panel, independent of N.

## 6. Relevance to small-action clusters

Set b=T/(Omega R). Form clusters by merging consecutive center gaps at most b. Then each original cluster has center diameter at most nb, and distinct clusters are separated at the center by more than b. The companion relative-gap theorem gives, on a suitable common disk,

    within-cluster pairwise gaps <= 2nb,
    cross-cluster pairwise gaps >= b/2.

Taking g=b/2, the sufficient choice T>=8192n^4(N+1) ensures (4), as well as the weaker weighted-contour smallness condition below. If a threshold is instead expressed with d rather than R, it must additionally pay the polynomial factor d/R.

Choose one original algebraic eigenvalue lambda_ref,a(t) in each cluster as its scalar phase reference. This leaves phase acquisition in the original algebraic class, instead of introducing the iterated quantity trace(H_N P_Na).

There is also a complex analytic bounded-block estimate. For a fixed cluster use the union of disks of radius a=b/8 around its original eigenvalues. Its boundary has length at most 2pi n a. The original resolvent is bounded by 2n/a, because external eigenvalues are at distance at least b/2-a>=a. For E_j=H_j-H, the estimate ||E_j||<=32n/(Omega R) implies a convergent Neumann series and perturbed resolvent bound 4n/a whenever T>=1024n^2. The weighted Riesz formula gives

    (H_j-lambda_ref,a I)P_ja
      = (1/(2pi i)) integral_Gamma
          (zeta-lambda_ref,a) (zeta I-H_j)^(-1) d zeta.

On the contour, |zeta-lambda_ref,a|<=2nb+a. Consequently

    ||(H_j-lambda_ref,a I)P_ja||
       <= 4n^2(2nb+b/8) <= 9n^3 b.            (7)

The important choice is contour radius b/8, rather than g/4: the latter could insert a very large external gap into the small-action estimate. The normal-form threshold already permits taking T at least the stated polynomial bound.

After multiplication by Omega and panel length R, (7) leaves action O(n^3 T). On the real line, Weyl's estimate gives the sharper intuitive statement that the perturbation adds only O(n) action. The Kato frame is unitary there and costs only O(n) action as well.

This supplies the local structural reason the construction can combine direct small-action cluster evolution with high-order decoupling. It does not yet bound the arithmetic cost of evaluating the iterative projectors/frames or integrating the original algebraic scalar phases.

## 7. What remains outside this proof

- A deterministic representation and stable polynomial-cost evaluation of the analytic iteration, parallel-transport frames, and block ODEs. Direct symbolic algebra may expand degrees badly; the proof does not endorse that representation.
- Certified extraction and integration of large scalar phases, with dependence logarithmic in Omega and polynomial in input height and requested bits.
- A global discriminant-root-distance covering with crossing cores and rigorous termination at real roots. The local disk result cannot be applied at a real root itself.
- Error accumulation and compatible transition maps between local panels.

The supplied normal-form contraction is valid under its explicit local hypotheses. It should be used as a proved local component, without treating the outstanding global and computational steps as already settled.

