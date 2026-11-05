# Restricted higher-dimensional LTI completeness by vacuum padding

2026-11-05. Internal proof candidate, not an established theorem or a priority claim. The primary concrete application is a square lattice with square-patch interactions. The proof is stated for fixed spatial dimension p because the counting argument is identical. It does not prove generic injective-PEPS completeness.

## 1. Exact class, hierarchy, and proposed conclusion

Fix p>=1, local dimension d>=2, patch side R>=1, and

    K={0,...,R-1}^p.

Let h be a positive operator on this FULL CUBICAL patch, with

    ker h=span{|0_K>},
    c Q_K <= h <= M Q_K,
    Q_K=I-|0_K><0_K|, c>0, M=||h||.

There is one translation h_x per lattice site. No commutation, particle-number conservation, or positivity of overlap anticommutators is assumed. The full-cube hypothesis is deliberate: an arbitrary sparse support need not allow the boundary covering operation below.

For integer L>=max(R,2), define anchor cube A_L={0,...,L-1}^p, difference cube D_L=A_L-A_L, and the CENTERED larger physical SDP window

    Lambda_L=D_L+K={-L+1,...,L+R-2}^p.

A feasible dual rho on Lambda_L is positive, satisfies Tr(rho h_0)=1, and is locally translation invariant: every operator and translate that both fit in Lambda_L have equal expectation. Equivalently impose the full matrix equality of opposite-face partial traces in each coordinate direction. This is not merely invariance of one-site marginals.

Set

    q_L=h_0^2 + (1/2) sum_(z in D_L, z!=0) {h_0,h_z},
    gamma_L=inf_rho Tr(rho q_L).

The half sum is essential: it takes one representative of each unordered displacement after LTI. In more than one dimension a corner anchor would not contain mixed-sign displacements. Lambda_L explicitly avoids that error.

The inequality gamma_L<=Delta_N can first be proved without duality: average a normalized first excited torus eigenstate over translations, restrict it to Lambda_L, and divide by its positive local energy. Summing q_L over the torus retains each selected unordered pair exactly once. Every omitted pair is disjoint and positive, so its dual objective is at most Delta_N. A conservative sufficient size is N>=4L+4R in each coordinate. Section 3 establishes finite value and Slater duality, after which the corresponding finite-dimensional local-coboundary primal gives genuine positive lower certificates. These are explicitly defined rectangular LTI levels, not an undocumented claim about a particular implementation's 2D level numbering.

The proposed result is: for a model-dependent C independent of L,N,

    gamma_L >= Delta_N-C/L  for every N>=L+3R,
    lim_L gamma_L = lim_N Delta_N.

The same limit equals the product-state GNS gap. Translation-covariant finite-depth local unitary images give an explicit entangled PEPS class with the same conclusion, as explained in section 7.

Gap existence is elementary here and is NOT the new proposed conclusion: H_N>=c sum_x Q_(K+x), whose unique kernel is the product vacuum and whose first positive eigenvalue is at least R^p c, for sufficiently large tori. A one-site excitation gives Delta_N<=R^p M.

## 2. Pair moments, and why bounded objective matters

Choose one representative D_L^+ of each pair {z,-z}. Put

    a=Tr(rho h_0^2), b_z=Tr(rho {h_0,h_z}), v=a+sum_(z in D_L^+) b_z.

LTI transports every pair and single interaction that fits; b_z=b_(-z). We have

    0<=a<=M,
    b_z>=-2M,
    b_z>=0 whenever ||z||_infinity>=R.

Let J=((2R-1)^p-1)/2 be the number of potentially overlapping nonzero displacements up to sign. Then

    B(v):=sum_(disjoint z in D_L^+) b_z <= v+2MJ.       (1)

The nonnegative sum is therefore uniformly bounded on near-minimizers, since gamma_L<=R^p M and we may use v<=(R^p+1)M. Define B_*=M(R^p+1+2J).

LTI alone would NOT bound boundary second moments by surface area: highly correlated excitation mixtures can have surface-area-squared moments. Equation (1), paid for by the bounded H^2 dual objective, is indispensable.

## 3. The unchanged interior

The retained physical cube is U=A_L+K, of side u=L+R-1, and

    H_A=sum_(x in A_L) h_x, m=L^p.

All its moments can be evaluated in rho_U. In particular Tr(rho H_A)=m, and

    Tr(rho H_A^2)=m a+sum_(z in D_L^+) c_z b_z,
    c_z=product_j (L-|z_j|).

Here 0<=c_z<=m. For overlapping z, m-c_z<=p(R-1)L^(p-1). Only those finitely many b_z can be negative. Therefore

    Tr(rho H_A^2)<=m v+C_0 L^(p-1),
    C_0=2M J p(R-1).                                  (2)

Equation (2) bounds the dual objective below by -C_0/L, since H_A^2 is positive. Its value is also finite above by the explicit feasible states in section 1. The normalized identity is strictly feasible. Finite-dimensional SDP Slater duality therefore identifies the finite primal and dual values and supplies an optimal local-coboundary primal certificate. This order matters: no unproved primal attainment or dual compactness is used to obtain the near-optimal objective bound. No dual optimizer is needed below; use a near-minimizing sequence.

## 4. Exact padding and boundary compression

Embed rho_U in an N^p periodic torus and put every site outside U in |0>, with N>=L+3R. This is the explicit positive, generally unnormalized output nu. All interactions wholly outside U annihilate its support.

The nonzero boundary terms are indexed by

    Y={-R+1,...,u-1}^p minus A_L,
    s=|Y|=(L+2R-2)^p-L^p=O_R,p(L^(p-1)).

Write H_N=H_A+V+H_out, V=sum_(y in Y) h_y. H_out nu^(1/2)=0, so the first and second moments of H_N are those of H_A+V. Note that H_out need not annihilate H_A nu^(1/2); this does not matter because the second moment is the squared norm of H_N nu^(1/2).

For each y, clamp each coordinate to [0,L-1], obtaining a(y) in A_L. The intersection T_y=(K+y) intersect U is contained in K+a(y). Vacuum-compress h_y to an operator B_y on U. Then

    0<=B_y<=M Q_(T_y)<=M Q_(K+a(y))<=(M/c) h_(a(y)).  (3)

Write kappa=M/c. The displacement ||y-a(y)||_infinity is at most R-1. The number of y assigned to one anchor is at most P=(2R-1)^p. Every B_y has expectation at most kappa.

IMPORTANT: compression of h_y h_z is not generally B_y B_z. The proof only factors it for far pairs whose original physical supports are disjoint. Near pairs are controlled before compression by operator inequalities.

## 5. Direct cross-moment and seam-square bounds

### Interior/seam cross moment

For x in A_L with ||x-a(y)||_infinity>=R, h_x is disjoint from both B_y and h_(a(y)). Positivity on disjoint tensor factors gives

    Tr(nu {h_x,h_y})=Tr(rho {h_x,B_y})
       <=kappa Tr(rho {h_x,h_(a(y))}).                 (4)

For each unordered displacement z the number of such pairs (x,y) is at most 2s. Sum (4) using (1). The remaining near pairs number at most sP; for each, before compression,

    {h_x,h_y}<=h_x^2+h_y^2<=M(h_x+h_y),

so their expectation is at most M(1+kappa). Hence

    Tr(nu {H_A,V})
       <=s[2 kappa B(v)+P M(1+kappa)].                (5)

This direct pair count is what avoids a Cauchy-Schwarz error of order sqrt(surface/volume).

### Boundary second moment

Diagonal terms satisfy Tr(nu h_y^2)<=M kappa. Classify a pair as near if ||a(y)-a(z)||_infinity<3R. For each y there are at most

    T=P(6R-1)^p

possible z in this near class. Since {h_y,h_z}<=M(h_y+h_z), its total contribution is at most s T M kappa.

For the remaining far pairs, original supports h_y,h_z are disjoint because clamping moved each anchor by at most R-1. Their assigned interior supports are also disjoint. Vacuum compression now factors exactly, and

    compressed {h_y,h_z}={B_y,B_z}
       <=kappa^2 {h_(a(y)),h_(a(z))}.                 (6)

For each unordered displacement, there are at most 2Ps such pairs. All these displacements are in D_L and are disjoint. Thus

    Tr(nu V^2)<=s[M kappa(1+T)+2 kappa^2 P B(v)].     (7)

The thick outside collar ensures boundary terms on opposite faces cannot acquire a spurious overlap through the periodic seam. The N>=L+3R condition is a conservative sufficient choice.

## 6. Finish the comparison

All boundary terms are positive, so Tr(nu H_N)>=m. Equations (2),(5),(7) give

    Tr(nu H_N^2)<=m v+C_0 L^(p-1)+s C_1,
    C_1=2 kappa B_*+P M(1+kappa)
          +M kappa(1+T)+2 kappa^2 P B_*.

For L>=R, s<=2p(R-1)3^(p-1)L^(p-1). The finite periodic spectral inequality H_N^2>=Delta_N H_N therefore yields

    Delta_N<=v+C/L,
    C=C_0+2p(R-1)3^(p-1) C_1.                         (8)

These deliberately loose constants are explicit and uniform over the dual witness. Taking v down to gamma_L proves the comparison without any attainment or trace-normalization assumption.

The hierarchy is monotone: restriction of a larger-window feasible rho remains LTI, and the additional displacement shell consists only of disjoint positive anticommutators. It is bounded above by R^p M. Let G=lim gamma_L. Certification gives G<=liminf Delta_N. Since (8) holds for EVERY N>=L+3R, it also gives limsup Delta_N<=gamma_L+C/L for every L, hence limsup Delta_N<=G. The periodic limit exists and equals G.

For the product-state GNS representation, rho_U can instead be padded by the vacuum on the entire infinite lattice. It is a positive trace-class finite-excitation state; all H and H^2 moments above are the same. The strict local lower bound gives a positive GNS gap and a unique vacuum. H_GNS^2>=Delta_GNS H_GNS implies gamma_L>=Delta_GNS-C/L. Conversely, any fixed local centered excitation is a periodic variational state for sufficiently large tori with exactly the same energy and norm, so gamma_L<=Delta_GNS after taking the local form-core infimum. This identifies the same limit with Delta_GNS.

## 7. A concrete entangled 2D PEPS class

Let alpha be a one-site-translation-covariant finite-depth local-unitary automorphism, with propagation radius w in the coordinate sup norm, realized compatibly on every sufficiently large periodic torus. Set h'_x=alpha(h_x). Its ground state is the corresponding circuit image of the vacuum, a finite-depth-circuit PEPS. Its terms need not commute. Spectra and GNS dynamics are unitarily equivalent to those of h.

Define the target hierarchy with exactly the same displacement set D_L, interactions h'_x, and the explicitly enlarged physical window

    Lambda'_L=Lambda_L+{-w,...,w}^p,
    q'_L=alpha(q_L).

Take L>=max(R+2w,2), so D_L contains every possible overlapping displacement of h'. Any feasible target dual rho' pulls back to a positive source functional by

    Tr(sigma X)=Tr(rho' alpha(X)), X supported on Lambda_L.

Finite propagation makes this well-defined within Lambda'_L. Positivity, energy normalization, and full local TI are preserved because alpha is a unital *-homomorphism commuting with translations. Thus sigma is a feasible source dual with exactly the same objective. Consequently

    gamma'_L>=gamma_L.

Ordinary soundness for h' gives gamma'_L<=Delta_GNS, while section 6 gives gamma_L>=Delta_GNS-C/L. Therefore the target rectangular hierarchy converges with the same O(1/L) comparison, at the price of a fixed physical collar 2w. No ambiguous index shift or omitted overlapping displacement is needed in this definition. Equivalently, local positive certificates and translation coboundaries push forward under alpha.

This statement is restricted to explicitly given one-site-translation-covariant circuits with the stated torus compatibility. Fixed-period circuits after blocking would require separate generator/normalization bookkeeping and are not included in the audited primary statement. Nor is a finite-depth disentangler inferred for a general PEPS.

Concrete example: take any strictly positive 15 by 15 matrix on the orthogonal complement of |0000> as a 2 by 2 qubit interaction. Generic choices have noncommuting translates. Conjugate them by the square-lattice circuit consisting of on-site Hadamards followed by CZ on every nearest-neighbor edge. The unique ground state is the square graph/cluster state, while the conjugated Hamiltonian is generally noncommuting. The combined circuit is translation covariant and has propagation radius w=1. A finite edge coloring schedules its commuting CZ gates at bounded depth, including on odd-size finite tori. No claim is made that this class has intrinsic topological order or that gap existence was unknown.

## 8. Resource and novelty limits

For p=2 the SDP window has (2L+R-2)^2 physical sites and PSD dimension d^((2L+R-2)^2). Thus the theorem is not an efficient numerical algorithm. Achieving an error epsilon from this loose bound requires L>=C/epsilon, with exponential-in-epsilon^-2 matrix size. Explicitly conjugating by a fixed-depth circuit changes only fixed support constants, not this scaling.

The sparse test in `check_padding.py` executes the complete padding moment operation for a particular feasible translation-invariant one-particle marginal. It does not solve the SDP or establish its optimum numerically. The proof is for all feasible dual witnesses, including entangled and noncompactly normalized ones. The finite 3 by 3 spectrum is merely an example check, not a thermodynamic gap estimate or performance comparison.

Existing results already prove positivity and stability for many product/finite-depth and PEPS parents. The candidate contribution, if correct and new, is exact-value completeness of this specified LTI hierarchy and its surface/volume comparison. Generic PEPS boundary factorization theorems are not being relabeled as a general repair theorem. Independent proof and priority review remain required.
