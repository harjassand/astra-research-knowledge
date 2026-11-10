# All-r, all-affine adapted-Hessian support: complete candidate proof

9 November2026. Author-constructed computer-assisted mathematical proof, submitted for independent review. No historical novelty or full vector-gradient quasiconvexity claim is made. Earlier failed translators, coefficient allocations and serialization failures remain preserved.

## 1. Density, parameters and theorem

Let r>0, k=(2r+1)/3, ell=3k-1, n=k+1 and m=3k+1. Thus k>1/3 and ell>0. For a real2x2 matrix F with columns F1,F2 write

    u=|F1|^2, v=|F2|^2, j=det F,
    B=ell/(8n), F0=(5k+1)/(2n),
    J_k(F)=B[k^2u^2+v^2+2uv+4kuj-4vj]+F0j^2
          =B(ku-v+2j)^2+ell*uv/4+j^2.

Set

    L_k=diag(2k,-m),
    Lambda_k(A)=2det A+(ell/m)[k|A1|^2-|A2|^2+(3n/2)det A].

**Pointwise theorem.** For every real upper-triangular matrix A and EVERY real symmetric2x2 matrix H,

    J_k(A+L_kH)>=J_k(A)+DJ_k(A):L_kH+Lambda_k(A)det(L_kH).  (1)

The inequality is strict if H!=0. There is no sign, orientation, invertibility, amplitude or frequency restriction.

**Every affine mean, with its adapted class.** For an arbitrary real A, choose a constant R in SO(2) such that R^T A is upper triangular and put L_{k,A}=R L_k. The density and Lambda are invariant under this LEFT target rotation. Thus(1) holds with L_{k,A}H. When A1!=0, choose the first column of R to be A1/|A1| and the second its counterclockwise perpendicular. If A1=0, any R in SO(2) leaves the first column zero, so the construction still applies. No right/source rotation is used.

**Integrated consequence.** For every such affine A, every rectangular periodic torus and every real scalar psi in W^{2,4} on that torus,

    average J_k(A+L_{k,A}D^2psi)>=J_k(A),                 (2)

strictly when D^2psi is nonzero on a set of positive measure. Compactly supported W^{2,4} scalar potentials are included by periodization. This is an adapted SCALAR HESSIAN class, not arbitrary compatible vector gradients, and not a mean-independent fixed L at every A.

For each fixed k>1/3, there is a strictly positive, not numerically specified c_k such that the pointwise remainder in(1) is at least

    c_k[|A|^2|L_kH|^2+|L_kH|^4].                        (3)

One may choose a positive common constant on any fixed compact k interval inside(1/3,infinity). No constant uniform over the whole open half-line is claimed.

## 2. Literal original-density affine matrix

Write

    A=[[alpha,beta],[0,delta]],
    H=[[U,V],[V,W]], x=2kU, y=-mW,
    X=L_kH=[[x,2kV],[-mV,y]], T=V^2.

Let P be8nm times the difference of the two sides of(1), with the left side minus the right side. It is exactly

    P=a^T Q a+C^T a+E,
    a=(alpha,delta,beta),
    M=[[Q,C/2],[C^T/2,E]],  P=(a,1)^T M(a,1).           (4)

The complete rational-polynomial Q,C,E are in MATRIX.json. They are not fitted: construct_fixed_translator.py expands the displayed ORIGINAL J, its exact affine tangent and the displayed Lambda. Its SHA256 is5f5ea6864add01cb168f6c1916c544c16cc2ba5bf65a77e237fb90c10f0dbe25. The source uses the order(alpha,delta,beta), so every mixed affine entry is retained. An executable replay checks the literal identity in(4) rather than trusting a numerical matrix.

Let D1,D2,D3,D4 be the leading principal minors of M. The exact coefficient records satisfy

    D2=ell*sum f2[a,b](x,y)*ell^a*T^b,
    D3=ell^2*sum f3[a,b](x,y)*ell^a*T^b,
    D4=ell^3*sum f4[a,b](x,y)*ell^a*T^b.                 (5)

Every coefficient and its index is listed in Q2.json,Q3.json,M4.json. Q11.json also retains D1. Coefficient identities are checked against determinants of the literal M in the executable replay. The proof below pays complete T=0 blocks, then every positive-T-power coefficient, with two joint parameter-tail groupings. It does not assume that every separate ell coefficient is positive.

## 3. The complete T=0 blocks, for all k

When V=0, the affine beta entry decouples. Its original, unscaled coefficient is

    ell[m(x^2+y^2)+2(1-k)xy]/(4nm)>0                    (6)

for(x,y)!=(0,0), because m>|1-k|. Put

    d=kx^2-y^2, j=xy, E2=d^2+4kj^2=(kx^2+y^2)^2,
    s=k alpha x-delta y, t=alpha y+delta x.

This is an invertible change of the two diagonal means when X!=0. In these variables, with a0=ell/(8n),b0=ell/(2n),c0=(3k^2+12k+1)/(4n) and L=ell(d+3kj)/m, the original unscaled two-mean matrix is

    Qss=6a0-Lj/E2,
    Qst=ell(7k+1)/(4nm)+Ld/(2E2),
    Qtt=(13k+1)/(4n)+Lkj/E2,
    C1=4a0d+2b0j, C2=b0d+2c0j,
    f=a0d^2+b0dj+c0j^2.                                (7)

Here Q(s,t)=Qss*s^2+2Qst*s*t+Qtt*t^2. Literal extraction gives

    det Q=ell N/(4E2 n m^2),
    N=3m^2d^2-m(18k^2+7k+1)dj
                        +(54k^4+69k^3+16k^2+k)j^2.

The discriminant reserve of N is m^2 times

    324k^4+576k^3+107k^2-2k-1
       =4ell^4+(112/3)ell^3+(899/9)ell^2
                                      +(928/9)ell+320/9>0.

Therefore det Q>0. Qss is positive at j=0 and the nonzero(d,j) plane is connected, so Q is positive definite throughout. Alternatively, its explicit numerator is ell[3m d^2-4n dj+24k^2j^2], whose discriminant is negative for k>=1/3.

For the augmented two-mean matrix Mdiag in(s,t,1),

    E2 det Mdiag=ell^2 P4(d,j)/(64n^2m^2),
    P4=2m^2d^4-2m(6k^2-7k-1)d^3j
       +ell(9k^3-23k^2-7k+1)d^2j^2
       +4kell(9k^2+4k-1)dj^3+4kn(33k^2-1)j^4.

This is strictly positive. A complete rational three-square proof is as follows. Put a=2m^2,f=6k^2-7k-1,h=2k-1/3 and

    B=ell^4/9+16ell^3/9+41ell^2/6+88ell/9+16/9,
    C=20ell^4/27+188ell^3/27+50ell^2/3+392ell/27+104/27,
    O=2ell^4/9+22ell^3/9+55ell^2/9+6ell+16/9,
    BC-O^2=(8ell^8+244ell^7+2576ell^6+13006ell^5
       +34520ell^4+48448ell^3+34064ell^2+10240ell+896)/243.

Then exactly

    P4=a[d^2-f*d*j/(2m)-h*j^2]^2
          +B[dj+(O/B)j^2]^2+[(BC-O^2)/B]j^4>0.          (8)

This pays the full diagonal mean Schur, not merely the metric. Together with(6), all four T=0 leading minors are positive for(x,y)!=(0,0). The complete derivation is copied into dependencies/EXACT_DIAGONAL_GRAM_PAYMENT.md, source SHA2563266b6631f45a922f28977e1ca337a87859dc095fbe2f2e2372f34960fed7a95. Equations(7)-(8) make that dependency explicit here.

## 4. Exact certificates for the positive powers of T

D1 is its positive T=0 coefficient plus

    2k^2ell(27k^3+39k^2+13k+1)T>0.

For D2 and D3, every coefficient in(5) with b>=1 is a nonnegative homogeneous binary form in(x,y). The same is true for D4 except for the tails grouped in Sections5-6. These statements are supplied by exact rational Sturm certificates, not sampled signs:

    JOINT_STURM_PROGRESS.json

contains128 declared records. Of these127 have positive certificates. The sole failed record, tail_T1_determinant, belongs to an insufficient THREE-term allocation and is NOT used in this proof. It is retained transparently. Its replacement is Section6. The source fixes the grouping and target list before constructing certificates; source SHA25681e3370c53d2a312dccca0caafe9c8a2a4c31855f5c663aed06450986c282ee9.

For each homogeneous even-degree form p(x,y), the record retains any removed even coordinate factors, all coefficients of the resulting q(x)=p(x,1), its exact rational Sturm chain, and signs at both infinities. The successful records have an even degree, positive leading coefficient and equal sign-variation counts, hence no real roots. Consequently q>0 everywhere and p>=0 everywhere, including y=0 by homogeneity/continuity. No odd/signed factors are removed. Constant forms are included.

The executable replay reconstructs the precise required forms from(5), checks the target set so no coefficient can be omitted, and checks each rational Sturm recurrence and sign count. This is a finite exact mathematical certificate. SymPy is used for rational polynomial arithmetic, not floating root estimates.

## 5. Joint T^2 tail: a quadratic for both signs

For D4's T^2 coefficient, the last three relative ell powers are11,12,13. Define

    Q6=281000x^6-469028x^5y+557859x^4y^2-274008x^3y^3
                                      +243720x^2y^4+25380xy^5+2025y^6,
    Q5=11488x^5-20906x^4y+24855x^3y^2-14094x^2y^3+8694xy^4+648y^5,
    Q4=284x^4-564x^3y+681x^2y^2-432xy^3+216y^4.

Their EXACT group is

    (8/6561)ell^11[Q6+2zQ5+3z^2Q4], z=ell*x.

The fixed binary forms Q4 and3Q6Q4-Q5^2 have positive certificates in the record above, including strictness for(x,y)!=(0,0). Their variation counts are2/2 and5/5, respectively. Thus

    Q6+2zQ5+3z^2Q4
       =3Q4[z+Q5/(3Q4)]^2+(3Q6Q4-Q5^2)/(3Q4)>0         (9)

for either sign of z. At x=y=0 the original group is zero and no division is used. The lower relative ell powers0 through10 are paid individually. All mixed terms in the three high powers are retained.

## 6. Joint T^1 tail: a cubic on the required half-line

The three-term allocation at relative powers9,10,11 was too strong and failed. The successful proof retains the adjacent positive power8 coefficient, using it ONCE within the group. Put

    F8=4[47528x^8-67429x^7y+46000x^6y^2+30846x^5y^3
          +28941x^4y^4+47523x^3y^5+10692x^2y^6-8424xy^7+1053y^8],
    P8=33784x^8-58204x^7y+54811x^6y^2-4098x^5y^3
          +7245x^4y^4+28872x^3y^5-135x^2y^6-2106xy^7+243y^8,
    P6=1764x^6-3598x^5y+4147x^4y^2-1950x^3y^3+747x^2y^4+972xy^5-162y^6,
    P4=164x^4-388x^3y+519x^2y^2-378xy^3+189y^4.

Let f(z)=P4*z^3+2P6*z^2+P8*z+x^2F8. The exact four-coefficient identity is

    x^2*sum_{a=8}^{11} f4[a,1](x,y)ell^a
                      =(8/2187)ell^8 f(ell*x^2).         (10)

F8 and P4 are strictly positive away from(x,y)=(0,0), as certified in the earlier records M4_ell8_T1 and tail_T1_P4, with variations4/4 and2/2 and no coordinate factors. Their positivity is used inside this group, not counted again as a separate reserve.

For a=P4,b=2P6,c=P8,d=x^2F8, form the literal cubic discriminant

    Disc=b^2c^2-4ac^3-4b^3d-27a^2d^2+18abcd.

The homogeneous degree28 binary form -Disc is strictly positive for every(x,y)!=(0,0). The complete polynomial and exact rational Sturm chain are in FOUR_TERM_TAIL_CERTIFICATE.json. For its monic square-free chain, the sign sequences at minus/plus infinity are

    minus: +--+-----+-+--++---+---++--++
    plus:  ++---+-+-----++--+---+--++--+

Both have14 variations; the defining polynomial has positive leading coefficient and degree28. Thus there are no real zeros of(-Disc)(x,1), proving the strict binary-form sign, including y=0. The executable checker uses the full recorded integer/rational coefficients and recurrences, not these compact sign strings alone.

For x!=0, f has positive constant and leading coefficients and strictly negative discriminant. A real cubic with negative discriminant has exactly one real root. Since f(-infinity)<0 and f(0)>0, that root is negative. Hence f(z)>0 for every z>=0, in particular z=ell*x^2. Equation(10) proves positivity of the complete four-term group.

For x=0,y!=0, use the ORIGINAL group without division by x^2:

    sum_{a=8}^{11} f4[a,1](0,y)ell^a
                       =(8/2187)ell^8(4212+243ell)y^8>0.

At x=y=0 the group is zero. Lower relative ell powers0 through7 are paid individually. This covers all coordinate and sign cases and keeps the failed three-term attempt separate.

## 7. Sylvester conclusion and strictness

Every positive-T-power coefficient in D2,D3,D4 is now nonnegative on the whole parameter half-line, with the two complete groups above interpreted jointly. If(x,y)!=(0,0), the T=0 minors are already strictly positive by Section3. If x=y=0 but V!=0, the highest powers T^2,T^3,T^5 of D2,D3,D4 have strictly positive scalar coefficient polynomials in ell; those exact positive constants are included in the certificate target set. D1 is also strictly positive by its explicit T coefficient.

Thus all four leading principal minors of M are strictly positive whenever H!=0. Sylvester's criterion makes M positive definite. Equation(4), divided by the positive8nm, proves(1), including strictness.

For fixed k, restrict X to the unit sphere in the three-dimensional space {L_kH:H symmetric}. M is continuous and positive definite there, so its smallest eigenvalue has a positive minimum. Homogeneity of the original quartic gives a uniform lower bound proportional to |A|^2|X|^2+|X|^4. This proves(3). The same compactness applies jointly over a compact k interval inside the open admissible half-line. No explicit numerical constant, endpoint-uniform constant or claimed computationally acquired threshold is inferred.

## 8. Function spaces and exact remaining scope

For smooth periodic scalar psi, average D^2psi=0 and average det D^2psi=0 by integration by parts. Since det(L_{k,A}D^2psi)=det(L_{k,A})det D^2psi, integrating(1) yields(2). Smooth approximation in W^{2,4} passes all quartic terms and the determinant term; the nonnegative quantitative remainder gives strictness. Periodization includes compactly supported potentials without altering the source lattice. No assumption on the sign of det(A+L_{k,A}D^2psi) is used.

The proof covers all r>0 but ONLY the stated scalar-Hessian adapted perturbations. A general compatible gradient has an additional transverse component. The earned acoustic projection splits the quadratic metric, but its actual mixed cubic/quartic cost remains a separate obligation. Variable reference means/rotations cannot be inserted pointwise without paying their force and compatibility terms. This theorem does not solve full J_r quasiconvexity and does not claim historical novelty.

## 9. Reproducibility, costs, failures and review status

All scientific inputs are exact rational polynomials. The full matrix construction completed once in3.565180082seconds. The diagonal invariant extraction completed0.293945074seconds; the fixed diagonal Gram expansion completed0.104seconds. The joint128-form construction completed1.557101019seconds, returning127 positive certificates and retaining the failed three-term tail. No field or parameter grid or optimizer was used.

The four-term cubic construction initially exitedrc1 only while serializing a rational Sturm coefficient exceeding Python's4300-digit decimal conversion limit. No successful outcome was claimed from that failed run. The original source, stdout/stderr and return code remain. A serialization-only replay lifted that per-process decimal conversion limit; the polynomial, Sturm computation and acceptance test were unchanged. It completed in1.262007640seconds, rc0, with variations14/14. The successful source SHA256 isd6630fe69c344ec7b691988a1b0fc52eebf571af4347d15d45e9b80c81be4c62. The certificate is about1.43MB: large exact-integer representation cost is not hidden.

Core executable/data dependencies are: construct_fixed_translator.py, MATRIX.json, Q11.json,Q2.json,Q3.json,M4.json; construct_diagonal_invariants.py and DIAGONAL_INVARIANTS.json; dependencies/EXACT_DIAGONAL_GRAM_PAYMENT.md; construct_joint_sturm_certificate.py, JOINT_TAIL_FORMS.json, JOINT_STURM_PROGRESS.json and JOINT_STURM_RECEIPT.json; construct_four_term_tail.py and its unchanged-science serialization replay; FOUR_TERM_TAIL_CERTIFICATE.json; and replay_all_k_certificate.py. Manifests bind these files and preserve all failed attempts. The replay script reconstructs the original identity and exact certificate coverage.

This is a COMPLETE author candidate submitted for independent substantive review. The earlier k1 independent review does not automatically cover it. No new capital ZIP, upload, external communication, novelty conclusion or full-gradient claim is licensed merely by these successful construction receipts.
