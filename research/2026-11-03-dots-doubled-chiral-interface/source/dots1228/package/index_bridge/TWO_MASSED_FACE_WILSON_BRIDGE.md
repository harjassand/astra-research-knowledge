# Two independently massed Wilson faces: uniform static endpoint gap and additive charge

## Statement and scope

The one-face audited bridge extends to independent unitary textures U0,U1 on BOTH faces. With an explicit conservative parameter choice, a two-layer normal slab already has a one-particle Fermi gap >=M/3, uniformly in lateral volume. The total filled charge is the sum of the two oppositely oriented odd indices. This is a static endpoint theorem for the actual nearest-neighbor Wilson model, not a proof of the rotor-hopping/joint interface gap.

Use the same Wilson root m=-1, physical spacing a, doubled particle/hole convention, onsite symmetry action and x-AP spin structure as WILSON_LOW_HIGH_LOCALIZER_TRANSFER.md. Let

 B=max_j sum_i||partial_i Uj||,
 B0=max_j spatial Lipschitz constant(Uj).

Both textures may be the original PL barycentric maps; no smooth Fourier-tail oracle is required. Assume M>=12B, choose Lambda=1000M and aM<=10^-6. M need NOT exceed pmin. Fix normal thickness exactly L=2 lattice layers. The UV grid can always be refined further to fit the torus.

## Actual local Hamiltonian and symmetry

H=diag(h,-h)+V, with the two flavor copies implicit, and

 V=[[0,M(P0 U0+P1 U1)],[M(U0^*P0+U1^*P1),0]].

P0,P1 project to disjoint physical normal layers, so ||V||=M, not2M. This is still nearest-neighbor in four spatial directions plus onsite boundary masses. Both Uj transform by the same left multiplication D(alpha)Uj. Thus the original onsite V action on the first flavor doublet and the neutral second doublet implements exact covariance on both faces. Axial number is conserved. The two textures are independently specifiable fields transforming under the same global symmetry; no additional independent global symmetry is asserted.

## Exact two-layer normal algebra

At k=ap, b=sum_i(1-cos k_i). The normal SSH matrix is bI-S. For L=2 its smallest singular value is

 nu(b)=(sqrt(1+4b²)-1)/2 <= b²,

while the other is (sqrt(1+4b²)+1)/2>=1. Write theta(b)=arctan(2b)/2. The smallest right/left singular vectors are opposite normal-chirality vectors with amplitudes c=cos theta at their own face and s=sin theta at the other. In particular |s|<=b and |1-c|<=b²/2. Their kinetic operators are respectively +sigma.sin(k)/a and -sigma.sin(k)/a, with normal hybridization norm nu/a.

Let P retain these two branches only for physical |p|<=Lambda. Q=1-P. P is free-Hamiltonian invariant. The previously proved global trigonometric/normal-chain estimate gives

 gap(QH0Q)>=gH=.4Lambda.

It covers the full Brillouin zone, all Wilson doublers and both normal singular values; no half-space approximation is used. The high block Q(H0+V)Q has gap >=gH-M and balanced inertia, because V can be turned off within this gap and the doubled free high block has paired signs.

## Low block and exact Schur reduction

Within P, order first by near/far normal chirality, then particle/hole species. Define C,S as diagonal Fourier multipliers cos theta(b(k)),sin theta(b(k)). Boundary masses commute with the normal-chirality matrix. Therefore there is NO direct near/far mass matrix element. The two face-diagonal compressed mass operators are exactly

  M(C U0,grid C+S U1,grid S),
  M(S U0,grid S+C U1,grid C),

up to harmless consistently chosen signs of S. Here Uj,grid are low Fourier compressions of the sampled onsite textures. Since ||S||<=b_* and ||C-I||<=b_*²/2, their difference from the desired mass operators M U0,grid and M U1,grid is at most3M b_*², with

 b_*=(aLambda)²/2<=5*10^-7.

The full low block also contains normal hybridization with norm <=b_*²/a. This is compared against M, NOT against a vanishing far-face momentum gap.

Exact inertia congruence gives

 inertia(H)=inertia(HQ)+inertia(S_eff),
 S_eff=PHP-PVQ HQ^-1 QVP.

The correction on the ENTIRE low block has norm <=M²/(gH-M). Unlike the one-massed-face problem, no small far-sector scale is present.

## Comparison with two continuum finite localizers

Compare S_eff to

 L0=[[D_Lambda,M U0,Lambda],[M U0,Lambda^*,-D_Lambda]],
 L1=[[-D_Lambda,M U1,Lambda],[M U1,Lambda^*,+D_Lambda]].

Each has gap >=M/2 by the odd-localizer theorem, since M>=12B and Lambda>2M. Their direct sum therefore has the same gap. The cutoff serves only as an analytical subspace; the actual implemented H is the local Wilson slab.

A sufficient bound on the comparison error is

 E2 = a²Lambda³
    + M[20aLambda+sqrt(3)B0 a+3b_*²]
    + b_*²/a
    + M²/(gH-M).

The sampled-mass estimate is the exact cell-embedding argument already audited: J^*R is diagonal product sinc, ||J-R||<=aLambda/sqrt12, and the pointwise cell sampling error is bounded by the spatial Lipschitz constant. Thus the displayed20 is conservative, with no hidden dimension factor, oracle or regularity beyond Lipschitz.

For the chosen ledger, B0<=B<=M/12 and

 E2/M <= .001+.020+sqrt(3)*10^-6/12
          +3(5*10^-7)²+2.5*10^-7+1/399 < .024.

Consequently gap(S_eff)>.476M, and its inertia equals that of L0 direct-summed with L1. Schur congruence has condition bound (1+M/(gH-M))²=(1+1/399)². Hence

 gap(H) >= min(gH-M,.476M)/(1+1/399)² > M/3.

This bound is independent of lateral volume and of pmin. AP is used only to invoke the invertible-D localizer theorem, not as the source of the endpoint Fermi gap.

## Additive index and decorations

Write Wj=(24pi²)^-1 integral tr(Uj^-1dUj)^3. The exact orientation calibration gives Index(D+,Uj)=Wj and Index(D-,Uj)=-Wj. High-sector signature is zero, so

 Qslab=Nnegative-dim(H)/2=-W0+W1.

For the barycentric conventions Wj=-sj, this is

 Qslab=s0-s1.

The two correctly oriented decoration sectors must therefore have charges Qdec,0=-s0 and Qdec,1=+s1. Their sum cancels Qslab exactly. Swapping the two physical root orientations reverses these assignments. This is arithmetic from earned indices, not assumed anomaly cancellation. If the pre-existing decoration Hamiltonians have unique static ground states and uniform gap Delta_dec, the tensor-product slab-plus-decoration endpoint is unique with gap >=min(M/3,Delta_dec), and total compensated charge is the declared reference charge.

This statement does not supply the deformation between distinct texture configurations or prove that their compensating matter ground states admit all desired local rotor updates. It provides the uniformly gapped static input for that separate construction.

## Resource and locality ledger

Normal thickness is2 sites, physical thickness2a. Per coarse lateral rotor cell of side ell and K=B ell, selecting M>=12B and aM<=10^-6 entails at least (12*10^6 K)^3*2 slab sites under this conservative choice, with the existing fixed onsite orbital count. Hopping norms are O(1/a), at least10^6M. These are enormous existence resources, not a proposed simulation.

Spatial range, local norms and the Fermi gap are uniform as lateral volume grows. Standard resolvent locality for a gapped finite-range free-fermion Hamiltonian therefore applies to its occupied projector; the projector is genuinely spatially quasilocal. Its decay constants depend on the paid ratio localnorm/gap, here of order10^6, rather than on lateral size. This conclusion concerns spatial locality at each fixed texture. It does NOT by itself establish continuity or locality in rotor configuration space across cochain rounding walls, nor a joint interacting gap.

## Uniform extension to every normal thickness and static half-space limit

The explicit L=2 formulas are convenient, but the theorem is NOT limited to a bilayer. For every L>=2, use the previously audited general SSH trial-vector bounds:

  nu<=b^L<=b²,
  |r_own-1|<=b²+2b^L<=3b²,
  |r_remote|<=b^(L-1)+2b^L<=(5/4)b^(L-1) for b<=1/8.

The two face-diagonal masses are again R U0 R+S U1 S and S U0 S+R U1 R. Since ||R||<=1, the ownface correction is <=6Mb_*² and the remote contribution <=(25/16)Mb_*². Replace3Mb_*² in E2 by8Mb_*²; all other inequalities remain valid, including normal hybridization <=b_*²/a and the high-sector gap. The numerical ledger still gives E2/M<.024 and full gap>=M/3, UNIFORMLY IN BOTH LATERAL VOLUME AND ALL L>=2.

Thus2 is a sufficient minimal normal thickness for the static construction, while arbitrarily thick slabs have the same endpoint gap. With a,M fixed, pushing the second massed face to infinity produces a genuinely gapped static half-space operator. For any finitely supported half-space vector psi, sufficiently large finite slabs act identically on psi and on its one-hop neighborhood; their uniform inequality ||H_L psi||>=M||psi||/3 therefore passes directly to H_half. Density gives H_half²>=(M/3)². No assumption that the far face is physically fixed to an invariant identity texture is needed: its correctly transforming mass is simply taken outside every compact set.

This half-space conclusion is still static. Transporting the uniform gap to a rotor-coupled many-body family requires the independent collective construction.

Independent static audit: audit_passive_memory_receiver checked the two-face L=2 algebra, full Schur bound, multiplicities, onsite symmetry and uniform gap. The general-L extension uses exactly the earlier independently checked normal-vector estimates; it changes only an insignificant profile-error coefficient.

## Finite local texture updates: no parameter differentiability assumption

If a local rotor update changes the texture Hamiltonian only on a bounded spatial set S, write Delta h=h'-h. Both endpoints obey the uniform gap and finite-range/norm bounds. On a common contour enclosing the negative spectrum,

  P'-P=(1/(2pi i)) integral (z-h')^-1 Delta h (z-h)^-1 dz.

Weighted resolvent conjugation is elementary here: for a graph-Lipschitz distance weight f, the perturbation e^(mu f) h e^(-mu f)-h has norm at most zJ(e^mu-1), where z is the bounded hopping degree and J a hopping norm bound. Choosing this below half the contour distance to the spectrum gives exponential resolvent kernels. The displayed difference consequently decays in d(x,S)+d(y,S), with constants depending on the paid UV size of S and J/g but not total volume. This remains true for finite, discontinuous changes across rounding walls: it is a resolvent identity, not a derivative expansion.

For the canonical doubled one-particle purification, W(P)=[[I-P,P],[-P,I-P]] is unitary and equals the exponential of (pi/2)[[0,P],[-P,0]]. Thus W itself is spatially quasilocal, and the difference of its generators for P',P is localized near S. Duhamel plus the finite-time locality bound makes the relative W(P')W(P)^* quasilocal near S. Number-conserving second quantization is an exact representation with the vacuum phase fixed, so no hidden projective implementer phase is assumed.

This provides a useful input for conjugating bounded local rotor-update terms. It does not license conjugation of an unbounded differential rotor kinetic operator through discontinuous texture maps; that requires a separate domain analysis or a different bounded-update model.

Audit addendum: the independent auditor also passed the all-L>=2 profile constants, uniform gap, and finitely-supported-vector half-space argument.
