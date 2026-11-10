Logarithmic-depth rational Fourier generation: a paid algebraic interface, not physical uniform control
ROOT research,10November2026. The local identities are established Nersesyan machinery; this note supplies a uniform balanced construction and keeps its algebraic versus physical costs distinct. No novelty assertion or PDE experiment.

1. Definitions and exact source contract.
On the unit3-torus write B(u,v)=P[(u.grad)v] and Q(u)=B(u,u)/(2pi). All fields are real divergence-free finite Fourier sums. Let E(k) contain both sine/cosine phases and both polarizations perpendicular to the integer wavevector k. E(e1)+E(e2)+E(e3) is exactly the twelve fundamental shear space.

For k nonzero choose an axis e_a not parallel to k, and the integer polarization basis
 h1(k)=k cross e_a,
 h2(k)=k cross h1(k).
Its coordinates are O((1+|k|)^2). These are unnormalized rational directions; no square roots or real-number oracle is introduced. Any rational perpendicular vector can be expanded in this basis by a fixed-size rational linear solve. A nonzero cleared integer minor has absolute value at least1.

Nersesyan1403.5369v2, Proposition4.3 and identities(4.6)--(4.13), proves full E(m+n) can be generated in at most THREE quadratic saturation layers from E(m),E(n) and any third independent direction r. This is an algebraic statement, not a physical force-replacement rate. It is valid without imposing unequal lengths on m,n. The source uses normalized vectors; the proof below keeps the same spans with rational unnormalized ones.
Source actually read: https://arxiv.org/pdf/1403.5369v2, pages20--23. No held original is recovered.

2. A constant-size rational three-layer gate.
Let m,n be nonparallel integer vectors, k=m+n, with |k|^2!=1. Choose r from the THREE unit coordinate vectors such that d=(m cross n).r!=0. At least one works; d is a nonzero integer. Set delta=m cross n. Then delta is perpendicular to m,n,k.

For any two nonparallel modes l,h and a perpendicular to l, b perpendicular to h, phase isolation of Q(a cos(l.x)+b sin(h.x)) and Q(b cos(h.x)+a sin(l.x)) gives the pure sum-frequency field with polarization
 P_(l+h)[(a.h)b+(b.l)a].
Here the argument of each trig function is2pi times the displayed integer phase. Difference and sine versions follow from the same signed identities. Each pure-frequency divergence-free field has zero self-advection, so both signs of every cross interaction are available by replacing one of the two fields by its negative.

Layer1: put a=delta and
 b=(|n|^2m-(m.n)n)/|m cross n|^2.
Then b.n=0,b.m=1 and a.n=0. The isolated sum interaction is exactly delta cos(2pi k.x); the sine phase is obtained similarly. All coefficients are rational, with nonzero integer denominator |m cross n|^2. This constructs the one polarization delta at k.

Layer2: put t=k+r. For b in r-perp the interaction of delta at k and b at r has polarization
 P_t T(b), T(b)=d b+(b.k)delta.
The linear map T:r-perp ->(k-r)-perp is injective: T(b)=0 makes b a multiple of delta, and b.r=0 while delta.r=d!=0 forces b=0. Its range is the whole2-plane(k-r)-perp. Projection P_t on that plane is injective because
 t.(k-r)=|k|^2-1!=0.
Thus two rational basis vectors in r-perp give a rational basis of the FULL t-perp after this interaction/projection. Fixed-size rational elimination converts them to h1(t),h2(t), in both phases. No singular angular denominator is left uncharged.

Layer3: t and r are nonparallel because r is not in the span of m,n. Apply the layer1 construction to t and -r. It supplies delta2=t cross r=k cross r at k. Delta2.r=0, whereas delta.r!=0, so delta,delta2 are independent in k-perp. Another rational2-dimensional solve gives the full h1(k),h2(k) and both phases.

Every rational linear combination of signed quadratic cross interactions can be written in the signed-cone form eta-sum_j d_j Q(xi_j), d_j>=0 rational: each xi_j combines two individually single-frequency divergence-free fields, whose individual Q is zero, so negating one summand reverses Q. This is a LOCAL certificate over the previous layer. It is not a claim that nonlinear nested formulas collapse into one quadratic expression over the initial twelve fields.

For |m|,|n|<=C N and unit r, every displayed numerator, denominator, cleared minor and finite solve has size <=(C'(N+1))^c for universal computable constants. Indeed all are fixed-degree integer/rational formulas in at most six integer coordinates, and fixed-size determinant inverses; a nonzero integer determinant is at least1. Thus local bit lengths are O(log(N+1)), local field coefficients/norms are polynomial in N, and the local number of quadratic gates is an absolute constant. A declared finite Sobolev order adds only the corresponding power of frequency. These local bounds make no assertion about a physical time or control amplitude after composing layers.

3. Balanced decomposition of ALL integer target frequencies.
Let N=|k|infinity>=5. Put m0_j=floor(k_j/2), n0=k-m0. If m0 cross k!=0, take m=m0,n=n0. Otherwise choose a coordinate unit e_a not parallel to k and take
 m=m0+e_a, n=n0-e_a.
Then m cross n=m cross k!=0. In either case both m,n are nonzero and
 |m|infinity,|n|infinity<=ceil(N/2)+1.
For N>=5 this is less than N. All k in this regime have |k|^2>1, so Section2 applies with a unit r selected by at most three determinant tests. Intermediate sum frequencies k+r have infinity radius<=N+1. They are generated by the local three-layer gate; they do not require a separate recursion up to N+1.

For the fixed base box |k|infinity<=4, an explicit finite upper depth is96. Initially unit modes are available. One application of the three-layer gate gives full signed face diagonals; another gives full signed body diagonals, hence the radius1 box in depth6. Given the entire radius(q-1) box, obtain each axis q e_i from
 [(q-1)e_i+e_j]+[e_i-e_j], i!=j,
in3 layers. All other vectors in the radius q box follow by increasing l1-length, subtracting a signed coordinate unit while retaining another nonzero coordinate. Each batch costs at most3 layers and the l1-length is at most3q. Therefore depth grows by at most3+9q for q=2,3,4, giving6+21+30+39=96. All source vectors are present before the relevant batch; nonparallelness is explicit. Unit targets themselves are already in the initial space.

For general N define D(N) as a sufficient maximum quadratic depth. The construction gives
 D(N)<=D(ceil(N/2)+1)+3 for N>=5,
 D(N)<=96 for N<=4.
Since ceil(N/2)+1-3 <=(N-3)/2,
 D(N)<=96+3 ceil(log2(max(1,N-3))).
The minimum possible depth in ANY purely quadratic Fourier-generation circuit from unit frequencies is at least ceil(log2 N): radius can at most double in one layer. Thus the constructed depth has the optimal logarithmic ORDER, without claiming an optimal constant.

4. Description length, sharing and what is actually output.
For all target k in a radius N box, store the generated pure-mode fields as a directed acyclic certificate graph. Each frequency uses a constant-size three-layer gate with rational2-plane solves. Recursion visits radii N,ceil(N/2)+1,...,4. Even retaining redundant gates gives a conservative O(N^3 log(N+1)) graph size; deduplication can improve the count. Intermediate polarizations and phases have constant multiplicity per target. Frequency coordinates and LOCAL rational coefficients have O(log(N+1)) bits, with computable universal constants. Building this graph uses polynomial bit work/memory in N and a complete target coefficient encoding. A large binary frequency need not be visited if an independently proved H1 truncation already removes it.

This bound uses shared stored intermediate fields and per-layer certificates. It does not assume that repeatedly expanding a nested polynomial into the initial twelve fields preserves local coefficient sizes, small physical norm, or quadratic degree. Nor does it provide a PDE trajectory or ordinary-force control from the graph by itself.

5. Physical cost boundary remains.
The completed fixed-catalogue physical lowering theorem uses
 H_j=K H_(j-1)^32,
 H_D=K^((32^(D+1)-1)/31)rho^(160*32^D).
Even a logarithmic algebraic depth does not make this physical bound polynomial in the combined variable input. With the sufficient upper depth above,32^D<=C(N+1)^15; with the radius-doubling lower depth,32^D>=N^5. These statements bound the depth-dependent exponent for this implementation; they do NOT lower-bound all possible physical controls. Catalogue/operator constants K must also be paid and cannot be silently frozen when N varies.

Consequently the algebraic reachability/description operation now has a uniform polynomial-size logarithmic-depth construction, while the central LIVE question remains uniform polynomial physical forcing with exactly twelve fields for variable targets and all admitted unknown H1 inputs/weak realizations. A different multiscale synthesis, representation or nonlinear stability mechanism may be required. No new scientist prompt, live steering, completed target-compiler claim or universal no-go follows from this preparation.
