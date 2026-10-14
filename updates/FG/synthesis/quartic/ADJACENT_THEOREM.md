# A sharp adjacent quartic and an exact scalar–tensor separation

14 October 2026, Australia/Brisbane. Internally derived and independently reconstructed; historical priority, external review and formal proof-assistant verification remain UNKNOWN.

This result is separate from the supplied sharp theorem. It uses a different determinant-square coefficient and shows why a broader heat representation is needed. The full normalized quarter-turn cone and the full nine-coefficient left-SO(2) cone remain open.

## 1. Theorems and exact scope

For A=(x|y) in R^(2×2), set u=|x|², v=|y|², w=x·y, q=det A. Define

    H_ell(A)=u²+v²+4w²+4q²+ell q(u+v),
    K=sqrt(24−8sqrt(3))=3.18490086807250... .

The number K is the root in (3.18490086807,3.18490086808) of

    m(L)=L⁴−48L²+384.

**Theorem 1.** For every real ell, H_ell is quasiconvex if and only if it is rank-one convex if and only if |ell|≤K. For |ell|<K, every bounded Lipschitz domain Ω, every constant A0, and every φ in W^(1,4)_0(Ω;R²) satisfy

    ∫Ω[H_ell(A0+Dφ)−H_ell(A0)]
      ≥ (1−|ell|/K)/6 ∫Ω |Dφ|⁴.

Every member with 3<|ell|≤K is non-polyconvex.

**Theorem 2.** H_K admits a global homogeneous bilinear-SOS corrected heat certificate using a rank-four scalar block and one positive complex tensor square. It admits no certificate using only scalar output-rotation invariants, even if one allows an arbitrary constant positive-definite heat metric, subtraction of γq² for γ≥0, and an arbitrary globally closed homogeneous-quadratic two-form. This impossibility concerns the specified scalar bilinear-SOS representation. It does not concern unrestricted corrected heat positivity or quasiconvexity: the tensor certificate proves the latter.

**Theorem 3.** For any F=A(u²+v²)+Cuv+Ew²+Lq(u+v), a full real 24-monomial bilinear-SOS identity with identity heat metric and a closed quadratic two-form exists if and only if one exists with one common real symmetric 6×6 scalar block and two real symmetric 3×3 complex tensor blocks. All three blocks must be positive semidefinite. This is a complete representation reduction within SOS, not a theorem that such blocks always exist for rank-one-convex F.

## 2. Complete explicit tensor certificate

At a compatible second jet write

    A=(x|y), B1=(X|Y), B2=(Y|Z),
    z+ = (x·X,x·Z,y·Y,x×Y,y×X,y×Z)^T,
    z− = (−y·Z,−y·X,−x·Y,y×Y,x×Z,x×X)^T.

Identify a real output vector (p1,p2) with p1+i p2, and define the complex three-vector

    b−=(xX−i yZ, xZ−i yX, yY−i xY)^T.

Juxtaposition in this last display means complex multiplication, not a scalar product. Put S=VT V^T, where

    V = [ K²/52−9/26,       −7K³/832+19K/104,  3K³/832−23K/104,  K³/416−11K/104
          16/13−7K²/208,     9K³/832−43K/104,  −K³/416+11K/104, −5K³/416+29K/104
          1/2,              0,                0,               0
          0,                1/2,              0,               0
          0,                0,                1/2,             0
          0,                0,                0,               1/2 ].

The symmetric matrix T is specified by its upper-triangular entries:

    T11= 27K³/512−93K²/16−33K/32+1993/16
    T12=−257K³/512+5K²/128+785K/64+1
    T13= 15K³/512+9K²/64−5K−35/8
    T14= 219K³/1024−43K²/256−685K/64+45/8
    T22=−17K³/512−133K²/64+45K/32+561/16
    T23= 43K³/1024+33K²/256−45K/32+137/32
    T24=−35K³/1024−21K²/256+39K/32−165/32
    T33=−K³/128−19K²/256+65/2
    T34= 13K³/1024+259K²/256−3K/4+203/32
    T44=−3K²/256−3K/32+253/16.

The tensor direction is

    v−=(−K³/128−K²/32+3K/16+3/4,
         −K³/128−K²/16+3K/16+1, 1/2)^T.

Let the following linear one-forms be on matrix space, with column differentials dx,dy:

    theta=x×dx+y×dy,
    zeta=x·dy−y·dx,
    theta_a=x×dx−y×dy.

Set

    c1=(651K³−564K²−32928K+17280)/16384,
    c2=−(61K³−848K²−1968K+35936)/4096,
    c3=−(27K³−2976K²−528K+22944)/8192,
    c4=(61K³−19K²−430K+400)/512,
    c5=−(221K³−188K²−3008K+4992)/16384,

    alpha=c1(u+v)theta+c2q theta+c3(u+v)zeta
          +c4q zeta+c5(u−v)theta_a.

Direct polynomial expansion, reducing by m(K)=0, gives the universal identity

    Σ_i D²H_K(A)[Bi,Bi]+(d alpha)_A(B1,B2)
       = z+^T S z+ + z−^T S z− + (1/4)|v−^T b−|².   (1)

The identity holds for every A,X,Y,Z, with no smallness, Fourier, resonance, sign-of-determinant or background restriction. The four leading principal minors of T have exact rational interval enclosures contained in

    (64.02208,64.02210), (525.46759,525.46761),
    (8427.62664,8427.62666), (24664.66604,24664.66607).

Thus T is positive definite, and S is positive semidefinite of rank four. The additional tensor term is a positive squared modulus with weight 1/4. Equation (1) is therefore nonnegative. The verifier checks the identity, the compact primitive, the exact root count and positive rational enclosures; no approximate eigenvalue is an acceptance criterion.

The complete machine-readable data are `checks/TENSOR_CERTIFICATE.json`, SHA256 `1c698739fd8a1982d57b1c66fdb2ac707f8a1f42607f135fbf8f14898a0feb7c`. Every algebraic entry is an ascending four-entry rational coefficient array in 1,K,K²,K³. Verification does not evaluate expression strings or load snapshots.

## 3. From the tensor identity to compatible gradients

For a smooth periodic φ on a square torus Q, define φ_t=e^(tΔ)φ and A_t=A0+Dφ_t. Its derivatives retain B1=(X|Y),B2=(Y|Z). Periodic integration by parts and exactness give

    −d/dt ∫Q[H_K(A_t)−H_K(A0)]
       =∫Q Σ_iD²H_K(A_t)[∂iA_t,∂iA_t]
       =∫Q[z+^T S z+ + z−^T S z− +(1/4)|v−^T b−|²]≥0.

Indeed A_t*(d alpha)=d(A_t*alpha), whose integral is zero. Nonconstant heat modes decay smoothly, so the relative energy tends to zero. Integrating in t proves the nonnegative Jensen gap, and also its explicit representation by the positive right side of (1) integrated over space and time.

Extend a compactly supported smooth perturbation by zero into a larger periodic square. Its initial relative energy outside Ω is zero, giving the zero-boundary inequality on Ω. Approximate any W^(1,4)_0 perturbation by smooth compactly supported ones. Quartic growth and Hölder's inequality give continuity of the energy under that approximation. This proves quasiconvexity of H_K for the full stated class of compatible gradients. Output reflection sends q to −q and proves quasiconvexity of H_−K. Convex combinations prove it for every |ell|≤K.

This uses the established heat/exact-form strategy credited to [Bruno–Pasqualotto](https://arxiv.org/html/2608.06367v1). The new finite construction is the actual tensor certificate for this different boundary input. The general analytic strategy is not claimed as new.

## 4. Global acoustic positivity and sharpness

For the rank-one direction e1⊗(1,k), direct differentiation gives the acoustic matrix

    M_ell(k)=
    [12+8k², 16k,           −2ell k,           ell(3+k²)
     16k,    8+12k²,        −ell(1+3k²),       2ell k
     −2ell k,−ell(1+3k²),    4+8k²,            0
     ell(3+k²),2ell k,       0,                8+4k²].

Put V0=K², j=k². The leading 2×2 minor is 96(j−1/4)²+90>0. The leading 3×3 determinant is

    D3=12[(64−6V0)j³−V0j²+(48−4V0)j+32−V0]
       =(12/5)[(j−2)²(14j+5)+89]
        +12(51/5−V0)(6j³+j²+4j+1)>0,

because 10<V0<51/5 and j≥0. The first diagonal is positive as well.

Define c1=−48(136−10V0) and c2=768(V0−5)>0. Reduction by m(K)=0 gives

    4c2 det M_K(k)=[2c2j+c1(1+j)²]²≥0.            (2)

The leading 3×3 block is positive definite, and its scalar Schur complement is nonnegative by (2); therefore M_K(k)≥0 for every real k. The missing binary direction is obtained by homogeneity and continuity. Left-SO(2) invariance rotates any output direction to e1, so this is global rank-one convexity, not angular sampling.

For sharpness let j be the smaller root in (0,1) of

    j²+(3K²/8−8)j+1=0,

and k=sqrt(j). This is exactly the zero in (2). Set

    C0=[12+8j,16j,−2j; 16,8+12j,−1−3j;
        −2K²,−K²(1+3j),4+8j],
    (r_a,r_b,r_c)^T=adj(C0)(−3−j,−2,0)^T,
    D=det C0>0,
    Acrit=[[K r_a/D, k K r_b/D],[k r_c/D,1]].

The first three acoustic equations follow by the adjugate identity. The fourth reduces to zero modulo m(K) and the displayed quadratic for j. Hence M_K(k)vec(Acrit)=0. At ell=0, M_0(k) consists of the positive first block and the positive diagonal second block diag(4+8j,8+4j). Thus E0=vec(Acrit)^T M_0(k)vec(Acrit)>0. Affine dependence on ell gives

    vec(Acrit)^T M_ell(k)vec(Acrit)=E0(1−ell/K)<0

for every ell>K. Output reflection handles ell<−K. Quasiconvexity implies rank-one convexity, so Theorem 1 is sharp globally.

The interior estimate follows from H0=N/2+H3/2+2q², where N=|A|⁴. Here H3=N+4w²=(|x+y|⁴+|x−y|⁴)/2 is convex, as a sum of fourth powers of norms of linear maps. For a=|ell|/K<1, H_ell=(1−a)H0+aH_sign(ell)K. Therefore H_ell−(1−a)N/2 is quasiconvex. The elementary inequality

    |A+B|⁴−|A|⁴−4|A|² A:B≥|B|⁴/3

follows by expanding its difference as

    2[|A|²|B|²−(A:B)²]+6[A:B+|B|²/3]²≥0.

The vanishing mean gradient then gives the stated constant (1−a)/6.

For h=|ell|>3, H_−h(I)=6−2h<0 and H_−h(diag(1,−1))=6+2h. Put symmetric mass 1/[2(1+t²)] at each ±tI and t²/[2(1+t²)] at each ±diag(1,−1). Its mean matrix and mean determinant are zero. For sufficiently large t its mean energy is negative. Jensen for any convex representation in (A,det A) gives a contradiction. This is a non-polyconvexity witness, not a gradient construction.

## 5. Exact failure of the scalar representation

First fix the identity heat metric and γ=0. The scalar invariants are the twelve entries of (z+,z−). A common 6×6 Gram representation asks for

    E_H(A;B1,B2)+omega_A(B1,B2)
      =z+^T G z+ + z−^T G z−, G≥0, d omega=0.       (3)

The space of homogeneous-quadratic closed two-forms has dimension 45: its 60 coefficients obey 15 independent linear closure constraints. Eliminating this entire space from the 210 coefficients of the bilinear heat polynomial leaves rank 15 on the 21 symmetric scalar Gram entries. Thus every G solving the identity belongs to the six-gauge family freshly derived in `checks/general_c4.py`; this is not a restriction to five guessed primitives. Its six gauges are independent and span the entire affine fiber. Explicitly, for

    F=A(u²+v²)+Cuv+Ew²+Lq(u+v),

write the upper triangular entries of this complete scalar family as

    G11=12A,             G12=2τ3,
    G13=4C+2E−τ0+3τ2/2−τ3,
    G14=3L+2τ1+2τ5,      G15=−3L,
    G16=τ1−τ4/2−τ5,
    G22=2C+2E,           G23=2E+τ0−3τ2/2+τ3,
    G24=−L−τ1+τ4/2+τ5,  G25=−τ4, G26=−L,
    G33=12A+2C+2E−4τ3,
    G34=4L+τ1−3τ4/2−τ5, G35=−3L−τ1+τ4/2+τ5,
    G36=L+2τ1+2τ5,
    G44=4A+2C+τ2−2τ3,   G45=2E−τ0, G46=τ0,
    G55=2C,              G56=−τ2/2+τ3, G66=4A.

For H_K use A=1,C=4,E=0,L=K, since q²=uv−w². The five displayed geometric primitive types in Section 2 generate this same six-dimensional Gram fiber; one additional freedom is a Gram identity. The standalone checker explicitly constructs the complete 60-column two-form map and its closure equations, so the completeness claim can be checked without relying on a symbolic snapshot.

At a pure compatible jet with X=e1,Y=k e1,Z=j e1, any two-form vanishes. The critical acoustic background above makes E_H=0. For a positive G, both nonnegative scalar squares must vanish, so G must annihilate the two resulting six-vectors. With the common denominator D suppressed they are

    p+=(K r_a,Kj r_a,Kj r_b,−j r_c,−D,−jD)^T,
    p−=(−Kj r_b,−K r_b,−K r_a,−D,−j r_c,−r_c)^T.

These constraints uniquely determine all six real gauges. Use columns ∂τiG·p+ stacked above ∂τiG·p−, and select its first six rows. Its determinant, reduced by the two root equations, is

    −22416856829450949084769619332300800 K²j
    −3717355384049500119067363941285888 K²
    +227387484109864744419242414589345792 j
    +37707342057507457630092467393003520.

The isolating rational decimal boxes

    3.184900868072502763337997340968003939319 < K
      <3.1849008680725027633379973409680039393193,
    0.2536457332255324371136369340813433624087 < j
      <0.253645733225532437113636934081343362409

give a strictly negative determinant interval by exact bivariate Horner arithmetic (approximately −8.9354×10¹²). The checker verifies root isolation and those interval signs. This proves rank six at the specified real embedding, without assuming unknown gauges belong to a number field. The already exhibited solution is therefore the unique real solution. Its gauges are

    (−2,3K³/64−9K/4,K²/4−10,3K²/8−3,
     K³/8−K,−K³/64+K/4).

The forced matrix is

    G*=[12,3K²/4−6,6,K³/16−K,−3K,−2K
        3K²/4−6,8,10,K,−K³/8+K,−K
        6,10,32−3K²/2,−K³/8+3K,−K,K³/16−3K
        K³/16−K,K,−K³/8+3K,8−K²/2,2,−2
        −3K,−K³/8+K,−K,2,8,K²/4+2
        −2K,−K,K³/16−3K,−2,K²/4+2,4].

Its principal minor on indices 3,4,5 is 74K²−768<0 because K²<51/5. Consequently (3) is impossible. This is an exact algebraic obstruction, not an optimizer residual.

It also excludes subtraction of γq² for γ>0. Here r_c=−24K²(j−1)²<0 and D>0, so the critical rank-one determinant derivative is (D−j r_c)/D>0. The acoustic Hessian of H_K−γq² on that jet would be −2γ[(D−j r_c)/D]²<0. A positive corrected heat identity cannot have that sign on pure jets, where every alternating correction vanishes. Hence γ must be zero.

## 6. Averaging, all scalar invariants, and complete tensor reduction

The integrands in Theorem 3 are invariant under left output rotations, input quarter-turns, and the paired reflection A→RAT with R=T=diag(1,−1). On the scalar variables the quarter-turn acts as (z+,z−)→(−z−,z+), while the paired reflection acts as (z+,z−)→(z+,−z−). Averaging a positive scalar 12×12 Gram over the reflection kills its cross block; averaging over the quarter-turn makes its two diagonal blocks equal and positive. Thus a scalar12 certificate would give (3).

For a general constant positive heat metric M, quarter-turn averaging gives (tr M/2)I. The correction transforms as det(T) times the matrix-space pullback of omega, which preserves closure; the sign compensates the orientation of the spatial two-form. Averaging and positive rescaling therefore reduce any constant positive metric scalar certificate to (3). The no-go covers this full stated scalar SOS class.

For completeness of the broader representation, also define

    b+=(xX+i yZ,xZ+i yX,yY+i xY)^T.

The real features (z+,z−,Re b+,Im b+,Re b−,Im b−) form an invertible 24×24 transformation of all entry-times-jet monomials. In row-major A-entry-times-jet order its determinant is 262144. Output rotations fix the scalar features and rotate each complex tensor feature through twice the output angle. Averaging first separates the scalar sector and the tensor Hermitian sector. The input quarter-turn acts by b+→−i b+, b−→+i b−, so averaging removes the tensor cross block. The paired reflection complex-conjugates both b±, removing their imaginary skew coefficients. The scalar argument above leaves a common G. Hence every full24 SOS certificate can be written

    z+^T G z+ + z−^T G z− + b+* P+ b+ + b−* P− b−,
    G≥0, P+≥0, P−≥0,

with G real symmetric6 and P± real symmetric3. Conversely these positive terms are full24 bilinear squares. This proves Theorem 3. There are 21+6+6=33 symmetric Gram parameters instead of 300, without losing any certificate in the stated SOS class.

The tensor certificate (1) has P+=0 and P−=v−v−^T/4. Thus the exact scalar failure is bypassed by one tensor direction. No impossibility for non-SOS positivity, general nonlinear flows, the entire quartic problem or a physical technology follows.

## 7. A certified two-parameter band and the remaining gate

Let kappa denote the supplied packet's coefficient-7/2 endpoint. Combining its theorem with Theorem 1 gives, for every 0≤t≤1,

    lambda=(7+t)/2,
    |ell|≤(1−t)kappa+tK

as a quasiconvex region for u²+v²+4w²+lambda q²+ell q(u+v). This follows by convex combinations of the two certified slices; it is not claimed sharp between the endpoints. Nonnegative extra determinant square can also be added. This is the proved interval extension; no unaudited general boundary continuation is asserted.

The next substantive theorem is inclusion of the full C4 acoustic rank-one cone in the complete common6+tensor3+tensor3 closed heat-SOS cone, or an exact obstruction to that inclusion. The scalar-only universal inclusion is now refuted by H_K. The broader inclusion, the general nine-moment gradient completion, arbitrary left-SO(2) quartics and general planar Morrey remain unresolved.

## 8. Portable verification and evidence status

Run from the synthesis directory:

    python3 checks/verify_tensor_boundary.py

This requires SymPy, the accompanying `general_c4.py`, `TENSOR_CERTIFICATE.json` and `SCALAR_UNIQUENESS.json`. It uses no NumPy, optimizer, network, pickle or supplied binary. The finite checks reconstruct the Hessian, compact primitive, root isolation, positive principal minors, all45 closed forms, real-gauge uniqueness, acoustic obstruction, 24-feature rank and covariance actions. The analytic argument is a written proof independently reconstructed by the critic; it is not proof-assistant elaboration.

Acquisition scripts are retained separately. Their floating calculations select a frame and rational tensor weight; exact polynomial identities and rational interval signs decide acceptance. Scalar positivity attempts that failed are preserved as exploratory history; the no-go depends on the exact uniqueness/minor argument instead. All bit lengths, exact field reductions and root-isolation work remain computation, not a free oracle. Historical priority and external correctness remain UNKNOWN; no civilisation-enabling breakthrough is established.
