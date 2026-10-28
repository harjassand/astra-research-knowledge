# A coupled-flow attack and its exact governing obstruction

The source-audited quartic is `F=u^2+v^2+3w^2+16q^2+4q(u-v)`, where
`u=a^2+c^2,v=b^2+d^2,w=ab+cd,q=ad-bc`. The incoming completed proof
excludes constant SPD **spatial** heat certificates. This construction tested
a genuinely broader operation: constant real output-coupled parabolic flows.
The result below still concerns the specified closed-form/bilinear-SOS class,
not all possible monotonicity proofs or quasiconvexity.

## Proposed operation and exact theorem

Let `v_t=sum_(j,k) C^(jk) partial_j partial_k v`, where the real2x2 output
matrices are constant, symmetric in the spatial indices, and have uniformly
positive symmetric principal symbol. On compatible jets
`B1 e2=B2 e1`, integration by parts gives dissipation

`E_C G(A;B)=sum_(j,k) D^2G(A)[B_j,C^(jk) B_k]`.

There is **no** such operator, `gamma>=0`, closed homogeneous-quadratic
matrix-space two-form omega and PSD Gram R on the24 monomials A_i*z_j
satisfying the universal identity

`E_C(F-gamma*q^2)+omega_A(B1,B2)=Z^T R Z`.

This theorem broadens the incoming representation obstruction; it does not
say that F is not quasiconvex. The separate exact determinant-support
construction in `../quartic_alternative/` instead proves F polyconvex.
No new general principle, external priority or full nine-cone result is claimed.

## Reduction of all constant output-coupled operators

F and q^2 are invariant under left output rotations, under column exchange S,
and under `A -> D A D`, with `D=diag(1,-1)`. Conjugate a hypothetical identity
by these actual symmetries and average. Compatible jets transform linearly;
the two-form correction transforms by the oriented pullback and remains
closed/homogeneous; Gram matrices transform by congruence and remain PSD.
The same gamma is retained. Dissipation is linear in the operator coefficients.

First average the output quarter-turn group. The commutant of the90degree
rotation J is `span(I,J)`, so write the spatial coefficient blocks as
`A_jk I+B_jk J`, where both spatial matrices A,B are symmetric. Column exchange
requires `A=SAS,B=SBS`. The correlated output/input reflection requires
`A=DAD,B=-DBD`. Their joint fixed space is therefore

`A=a I, B=b [[0,1],[1,0]]`.

Uniform strong parabolicity survives averaging and gives `a>0`. Divide the
whole certificate by a. It suffices to exclude every real b in

`v_t=Delta v+2b J partial12 v`.

This flow really is admissible: its Fourier symbol is
`-|xi|^2 I-2b xi1 xi2 J`, whose symmetric real part is `-|xi|^2 I`.
It preserves gradient compatibility and smooth periodic modes decay. Its
mixed dissipation is

`E_J G=D^2G[B1,J B2]+D^2G[B2,J B1]`.

The incoming fixed dual did not exclude it: the new exact pairings are
`lambda(E_J F)=-18840469/3125000` and
`lambda(E_J q^2)=-4271173/3125000`. Thus a new governing construction was
needed; numerical failures at selected gamma values would not suffice.

## Compact parameter range and a parameter-dependent exact dual

The compatible plane-wave jet `A=diag(-1,1),B1=e11,B2=0` gives
`E_C(F-gamma q^2)=20-2gamma` after normalization. The mixed term and every
two-form vanish there. Therefore any certificate would require `0<=gamma<=10`.

`EXACT_PARAMETER_SEPARATOR.json` supplies two rational210-vectors L0,L1.
For `t=gamma/10`, put `lambda_gamma=L0+t L1`. Coefficients are ordered by
lexicographic unordered pairs of the four entries of A, then unordered pairs
of the six compatible second-jet coordinates, with
`B1=(z0,z1,z3,z4), B2=(z1,z2,z4,z5)`.

The construction checks exactly:

1. Each L annihilates the pullback of the exterior derivative of all80 cubic
   monomial one-forms. These span the full closed-quadratic two-form space by
   Cartan's identity `omega=(1/4)d(i_E omega)`.
2. The24x24 moment matrices of L0 and L0+L1 have strictly positive exact LDL
   pivots. Their convex interpolation is positive for every t in[0,1], hence
   `lambda_gamma(SOS)>=0` for every admitted PSD Gram.
3. `L0(E_J F)=0`, `L1(E_J F)=10 L0(E_J q^2)`, `L1(E_J q^2)=0`.
   Thus `lambda_gamma(E_J(F-gamma q^2))=0` identically, for every gamma.
4. The degree-two polynomial
   `lambda_gamma(E_I(F-gamma q^2))` has three strictly negative exact
   Bernstein coefficients on t in[0,1]. Their approximate values are
   `-.00714803,-.00716403,-.00718004`; the certificate stores exact rationals.

Applying this functional to any proposed identity gives a negative left side
and a nonnegative right side, a contradiction for every b and gamma. Together
with the averaging and plane-wave calculation this proves the stated theorem.

The exact construction takes about.17s after imports. `parameter_dual.py`
only finds a floating suggestion; `reconstruct_parameter_dual.py` rebuilds all
constraints with exact polynomial/Fraction arithmetic and proves positivity
and strict negativity. A first excessive interior perturbation passed LDL but
lost negativity and was rejected. No numerical status is used as a proof.

## What the result changes

The natural constant coupled-flow repair is decisively ruled out **within this
representation**, including determinant-square subtraction. The actual energy
is resolved by an ordinary global determinant-support certificate instead.
Consequently this test case should be removed from an unresolved-QC search.
The meaningful larger target remains energies outside the acquired
polyconvex/known-QC constructions, or a mechanism for the full invariant cone.
Neither the obstruction nor the positive support theorem solves that target.

Incoming exact certificate/source audit: cleared opportunity-retrieval
`capital_science/helper/n794_symmetric_bridge_audit.md` and its governing
sources. N797 tensor **correction** channels and N800's separate full-energy
fixed-flow counterexample were checked for scope; neither was silently
presented as this new construction. Published initial corpus pin is
63867607218adef378d727987fd92aa7dc42eb5c. All originals remain read-only.
