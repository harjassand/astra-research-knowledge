# A whole-domain harmonic-stability operation and its acquisition boundary

## 1. Question, prior and exact scope

The desired operation is to qualify candidate crystalline matter against arbitrarily long-wavelength and off-grid mechanical instabilities without treating a finite phonon plot as a proof. The present result is a finite certificate for a specified rational harmonic model, together with a proper central-force alias showing why a finite-supercell source does not automatically acquire that model as the true infinite-crystal Hessian. It is not a specimen-stability or synthesis certificate.

The Fourier formulation and rigorous reciprocal-space discretization are established. Hudson–Ortner, [On the stability of Bravais lattices and their Cauchy–Born approximations](https://doi.org/10.1051/m2an/2011014), Theorem3.6 and section4, provide the relevant ordinary baseline; in particular their treatment does not simply ignore the acoustic origin. Bernstein positivity and subdivision are also established validated-numerics tools. The construction here combines rational torus charts with an exact acoustic block blow-up, so ordinary polynomial positivity routines can consume a multi-site crystal without a vanishing absolute eigenvalue at the origin. Historical priority of that adaptation is UNKNOWN.

Let H_R be finitely supported real rational n-by-n force-constant blocks, n=3p, with H_-R=H_R^T. In the cell-periodic Bloch gauge define

    D(q)=sum_R H_R exp(i R.q),   q in the three-torus.

Positive masses do not affect its inertia, so they are omitted for this stability statement. Let T stack p copies of I3, and let Z=[T,Q] be any fixed invertible rational contrast basis. Assume D(0)T=0 and the acoustic first derivatives T^T partial_j D(0)T=0 exactly. These identities are checked, not inferred from small numerical residuals. Additional soft modes or quartic acoustic degeneracies fall outside the strict-coercivity case below.

## 2. Finite rational torus cover

For each center bit vector c in{0,1}^3, set

    exp(i q_j)=(-1)^c_j (1+i x_j)^2/(1+x_j^2),  -1<=x_j<=1.

These eight closed charts cover the torus. Write m_j=max_R|R_j| and

    Q0(x)=product_j(1+x_j^2)^m_j >0,
    P_c(x)=Q0(x) D(q(x)).

P_c is an exactly Hermitian Gaussian-rational matrix polynomial, of separate degree at most2m_j. No trigonometric approximation is used. In seven charts, c!=0, q cannot be the acoustic origin; ordinary strict matrix-polynomial positivity suffices.

## 3. Exact removal of the acoustic zero

In the zero-center chart write Z^T P_0 Z=[[A,B],[B*,C]]. The assumed identities imply that A has no constant or linear monomials and B has no constant monomial. For each dominant coordinate k and sign s, substitute

    x_k=s r,  x_j=r u,  x_l=r v,
    0<=r<=1,  -1<=u,v<=1.

The six boxes cover the original x-cube. The congruence

    W_ks(r,u,v)=diag(r^-1 I3,I) Z^T P_0(x) Z diag(r^-1 I3,I)

extends to a Gaussian-rational polynomial at r=0: divide A by r^2 and B by r exactly. The code asserts every required divisibility coefficient. For r>0 the congruence is invertible; positivity of W therefore proves D(q)>0 there.

At r=0 let w have dominant coordinate s and other coordinates u,v. The limit is the finite acoustic/optical matrix

    [[A2(w),B1(w)],[B1(w)*,C0]],

where, with M_j(w)=sum_R(R.w)^j H_R,

    A2=-2 T^T M_2 T,  B1=2i T^T M_1 Q,  C0=Q^T D(0)Q.

Its positivity is equivalent to C0>0 and positivity of the relaxed acoustic tensor A2-B1 C0^-1 B1*. Thus the operation retains the acoustic/optical coupling rather than replacing a multi-site crystal by an unrelaxed elastic approximation.

If D is positive away from0, C0>0 and the relaxed acoustic tensor is uniformly positive for all directions, the thirteen compact polynomial matrices are uniformly positive. Conversely a positive certificate for those matrices pays these conditions and the entire wave-vector domain. Fourier transformation then gives positive gradient/contrast coercivity for every periodicity, with translations factored out. Free surfaces, defects, finite-amplitude stability and thermodynamic phase selection are not covered.

## 4. Finite exact positivity receiver

On each compact box expand W (or a regular P_c) in tensor Bernstein form. Its value is a convex combination of its Hermitian coefficient matrices. A box is accepted only after a Gaussian-dyadic square matrix S_N has been proposed and EVERY integer coefficient B_N, with common positive denominator d, satisfies strict diagonal dominance of

    V_N=S_N* B_N S_N:
    (V_N)_ii > sum_(j!=i)(|Re(V_N)_ij|+|Im(V_N)_ij|).

All accepted multiplications and inequalities are Python-integer operations; Hermitian symmetry is checked exactly. Positive V_N implies S_N is invertible and hence B_N>0. Numerical eigensolvers only propose S_N. Their accuracy and convergence are not consumed by the receiver.

If the minimum integer dominance margin is a>0, each matrix on that box is bounded below by

    eta I,  eta=a/[d ||S_N||_F^2].

The dyadic scale of S cancels. Failed boxes are bisected by exact midpoint de Casteljau subdivision. Prefix-free leaf paths with sum2^-depth=1 cover the original box. A nonpositive Bernstein coefficient is not an instability witness.

Strict positivity on a compact box guarantees some finite Bernstein/subdivision certificate, since coefficients converge uniformly to values on sufficiently small boxes. This gives a semidecision procedure using exact Hermitian LDL tests, or an enumeration of rational congruences. It does NOT prove polynomial complexity or guaranteed success of the particular capped, fixed-24-bit numerical proposer. At an exact stability boundary termination is not asserted.

## 5. Acquired finite source and computation

The sole source is the public Phonopy silicon example at commit ea3c269be8502f4fde4db31870725d8dcb3f27d3: a two-atom primitive cell, 2x2x2 supercell and one displaced VASP calculation. Exact original Git blob bytes and the cached-view relation are retained in source_cache/TRANSPORT_RECEIPT.json. The numerical UTF-8 views differ only by one trailing LF, which affects none of their data.

model_from_source.py fits rational harmonic blocks by24 exact site symmetries, minimum-image averaging, reciprocity symmetrization and an explicit acoustic sum-rule repair. Its MODEL.json has45 Laurent blocks and maximum exponent2 in each direction. The maximum entry of the sum-rule repair is1.41421356237309e-6 eV/Angstrom^2. This repaired, symmetry-fitted finite-displacement INTERPOLANT is the exact object certified. Finite-displacement truncation, supercell aliases, DFT/model discrepancy and physical force-constant errors have not been warranted. It is not claimed to reproduce every raw finite-displacement force exactly.

An initial20,000-node attempt completed all six acoustic boxes but exhausted its cap during the first regular chart. Its incomplete receipt and leaves are preserved. Exact primitive-axis permutation covariance and D(-q)=conjugate(D(q)) then reduce this particular model to one acoustic box and three regular Hamming-weight representatives. complete_by_symmetry.py reuses the existing accepted leaves, checks the covariance for all Laurent blocks and completes those four representatives. The ordinary comparator receives the same symmetry.

The final exact certificate has7929 leaves. Its common lower bound for these four polynomial-chart matrices is

    122245487073788818180000000 /
    14028656185615979331461332353 >0.

The initial capped attempt cost159.704101 seconds; symmetry continuation cost58.686824 seconds, about218.390926 seconds combined. This is whole-domain positivity for the specified finite harmonic model, not another sampled plot. GLOBAL_CERTIFICATE.json and LEAVES.json.gz retain the actual arithmetic witnesses. No physical experiment or new electronic-structure calculation was performed.

## 6. Compatible uncertainty must retain the zero structure

For a supplied affine uncertainty family H_R(t), the constraints in section1 must hold for EVERY admissible t. Transform each uncertainty direction by the same exact charts and leaf subdivisions. For each retained S_N and coefficient, a sufficient robust gate subtracts from the nominal row dominance margin the sum of the parameter radii times the corresponding absolute diagonal and off-diagonal perturbation row bounds. If every remainder is positive, the entire uncertainty family is certified. This is a finite linear/rational receiver; the actual uncertainty radii are a separate acquisition input.

A free absolute perturbation bound on D is insufficient at an acoustic zero. Nor does a small unweighted coefficient error control arbitrarily long-range acoustic curvature: a term of strength delta at lattice distance L has curvature of order delta L^2. A physical interpretation therefore needs a qualified spatial-tail/moment or equivalent structured response error contract. The published finite source supplies no such contract. No physical uncertainty family has been consumed by the current certificate.

There is also an explicit sufficient finite-noise radius for the executed model. Allow real reciprocal coefficient errors on the FULL cube[-2,2]^3, with each entry bounded by delta, preserving D(0)T=0 and the zero acoustic first derivatives. The scalar Cayley numerator of exponent R has complex coefficient l1 norm at most L_R=2^(6+|R|_1); sum over the full cube is52^3=140608. A6-by-6 entry bound delta gives operator norm at most6delta. The rational contrast matrix Z has squared operator norm2. After block extraction, acoustic division and evaluation on any blow-up cube, each block error is at most12delta sum L_R; the full two-by-two block matrix error is at most24delta sum L_R. The regular charts have the smaller6delta sum L_R bound. Terms that would have negative r powers vanish by the exact stated identities; no division of an unknown residual is allowed.

Thus, with eta equal to the displayed common chart lower bound, delta<=eta/[48*140608] retains at least half the chart margin and certifies EVERY model in that structured error box. UNCERTAINTY_RADIUS.json stores this exact sufficient radius (approximately1.2911e-9 eV/Angstrom^2). Its exact range/support and error conditions are unacquired physical inputs, not consequences of the public force file. The bound is conservative and is not a necessary tolerance.

## 7. A central-force alias, not just a missing plot point

Let P=[[0,1,1],[1,0,1],[1,1,0]], in units a/2, and let r run over

    e1,e2,e3,e1-e2,e1-e3,e2-e3.

For each sublattice add central springs joining a site to its neighbours at shifts2r, with negative longitudinal curvature -a0. Their Bloch correction is

    Delta D(q)=-2 a0 sum_r[1-cos(2 r.q)]
                       diag(N_r,N_r),
    N_r=(P r)(P r)^T/2.

It is real reciprocal, satisfies the translational sum rule and has zero extension on each infinitesimal rigid rotation. At ALL eight2x2x2 commensurate wave vectors it is identically zero, regardless of strength. At every source-sized two-cell-periodic displacement history the corresponding bond vectors are unchanged. A smooth radial pair bump with zero value/first derivative and second derivative -a0 at the isolated bond length therefore adds no force to those source histories.

This can be a central pair interaction of the identical atoms, not a labelled artificial onsite force. The shell has squared radius8 in units(a/2)^2. The nearest other same/cross-sublattice shells have squared radii27/4 and35/4. For the supplied lattice constant their radial gap is greater than .3525698 Angstrom. A smooth bump supported within .1 Angstrom of the shell cannot touch another pair during relative displacements at most .021 Angstrom, which covers twice the exact source displacement norm. The code also bounds all omitted lattice translations in this shell-isolation calculation. The added local energy can be made bounded with a smooth compact bump; no global many-body thermodynamic stability theorem is asserted.

certify_alias.py adds this correction to the certified interpolant. For strength a0=7 and trial vector (0,1,-1,0,1,-1), at exact phase exp(iq1)=(63+16i)/65, the Rayleigh quotient changes from +.3534619941269064 to -.49482202954173266. At reduced q=(1/4,0,0) it changes from +11.644201958932198 to -2.355798041067802. Both are exact rational inequalities. The strength is constructed directly from those two trial inequalities, not fitted by a parameter grid. The initial unit-strength trial did not give this negative Rayleigh witness and is retained as a control.

These are two different statements: (i) the executed stable interpolant and its unstable modification have identical commensurate HARMONIC data; (ii) adding the central bump leaves the actual finite-supercell SOURCE FORCE experiment unchanged on any compatible background Hamiltonian. We do not claim that the repaired harmonic interpolant itself exactly fits every nonlinear source force or that real silicon has the added interaction. A known full Hamiltonian could exclude this freedom, but then that Hamiltonian is an additional input. The data-only acquisition implication is refuted.

## 8. Operational consequence and strongest ordinary route

An unqualified31^3 plot is a weak comparator and is not the claimed baseline. Equally informed ordinary validated Fourier/derivative/interval methods, including acoustic endpoint analysis, can certify a specified model; the Hudson–Ortner analysis is already a primary example. The current algebraic receiver is an executable adaptation of established tools, without a proved speed advantage over a strong such solver.

For physical acquisition the alias is an information obstruction applying equally to every inference algorithm using only the same supercell histories. More repeats or exact arithmetic do not see it. A warranted range/tail bound, a warranted constitutive Hamiltonian, or new noncommensurate/longer-cell response information is required. Arbitrary-q density-functional perturbation theory is an established possible additional operation; it is not granted by the current force file. The quarter-q witness gives a concrete discriminator, not an executed new DFT calculation. Thus the whole-model certification operation is acquired, while the hoped-for data-only physical qualification/discovery multiplier remains NOT_ACQUIRED.
