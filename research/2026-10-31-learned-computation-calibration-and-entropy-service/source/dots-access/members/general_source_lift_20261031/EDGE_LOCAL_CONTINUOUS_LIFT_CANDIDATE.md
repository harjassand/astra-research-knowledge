# Edge-local continuous-time pure lift: construction and dimension penalty

31 October 2026. Root construction, pending independent review. Finite positive stationary law only. This is an existence/explicit-matrix construction; succinct efficient preparation and a favorable gap are not supplied.

Let q_yx >=0 be directed classical rates x to y, x != y, with positive stationary pi. All rate sums exclude y=x, equivalently q_xx=0 in these edge-rate formulas. Set psi=sum_x sqrt(pi_x)|x>, Pi=|psi><psi|, Q=I-Pi. Define

L_yx=sqrt(q_yx)|y>(<x|-sqrt(pi_x/pi_y)<y|),
H_xy=-(i/2)[q_yx sqrt(pi_x/pi_y)-q_xy sqrt(pi_y/pi_x)] for x!=y, H_xx=0.

H is Hermitian. Each L_yx psi=0. Stationarity gives
(H psi)_x=-(i/2)[sqrt(pi_x) sum_y q_yx -(1/sqrt(pi_x))sum_y q_xy pi_y]=0.
Hence the Lindblad generator -i[H,.]+sum D[L_yx] fixes Pi exactly.

For diagonal D=diag(d_x), one edge contributes the usual classical backward diagonal entry q_yx(d_y-d_x) at x; its offdiagonal xy entry is q_yx sqrt(pi_x/pi_y)(d_x-d_y)/2. The reverse edge has the opposite coefficient q_xy sqrt(pi_y/pi_x). The Hamiltonian adjoint i[H,D] cancels this net offdiagonal term. Therefore the diagonal observable algebra is invariant and its restriction is exactly the original classical continuous-time generator. This gives the same classical label process, including controls whose adjoints preserve the algebra of source-diagonal, system-operator-valued observables and have the prescribed classical restriction. Merely preserving diagonal INPUT states is not sufficient: an X-basis measurement recorded in a Z-basis register has that weaker property but can reveal source coherences. This is not an identification of arbitrary original source coherences.

## Paid return rate

Because all jumps and H annihilate psi,

L^dagger(Q)=-C,
C=sum_(x!=y) L_yx^dagger Pi L_yx
 =sum_(x!=y) q_yx (sqrt(pi_y)|x>-sqrt(pi_x)|y>)(sqrt(pi_y)<x|-sqrt(pi_x)<y|).

If the directed graph is irreducible, its underlying undirected graph is connected. Thus ker C=span(psi); the finite-dimensional smallest eigenvalue c_* on Q is positive. Then L^dagger Q <= -c_* Q and positivity of the adjoint semigroup implies exp(tL^dagger)Q <= exp(-c_*t)Q. This is a genuine pure-return estimate, without supposing that a classical eigenvalue gap alone bounds an unrelated quantum lift.

For an explicit comparison, let g be the gap of the additive symmetrization in L2(pi), defined by

(1/2)sum_(x!=y) pi_x q_yx |f_x-f_y|^2 >= g sum_x pi_x |f_x|^2

for mean-zero f. Write v_x=sqrt(pi_x) f_x. Then

<v,Cv>=sum_(x!=y) q_yx pi_x pi_y |f_x-f_y|^2
 >=2 pi_min g ||v||^2.

Thus c_*>=2 pi_min g, a potentially exponentially small guarantee in the number of source bits. Computing c_* or g by a dense eigensolver pays the full dimension; a certified succinct bound requires additional structure.

## Exact complete-refresh contrast

For d labels, pi_x=1/d and q_yx=1/d for x!=y, the classical generator is uniform reset minus identity, with gap g=1. The edge-local lift has H=0 and

C=(1/d^2)sum_(x!=y)(|x>-|y>)(<x|-<y|)=(2/d)Q.

Its pure-state absorption rate is exactly 2/d. This is not an intrinsic obstruction to lifting the same classical law. The quantum reset generator rho -> Pi Tr(rho)-rho has exact pure return rate one and the same classical restriction. Its Kraus jumps may be J_j=|psi><j|. An equivalent dark-jump gauge is J'_j=|psi><j|-sqrt(pi_j)I; the gauge Hamiltonian correction vanishes because sum_j sqrt(pi_j)J_j=Pi is Hermitian. For these dark jumps sum_j J'_j^dagger Pi J'_j=Q.

The difference is the coherent common destination psi. It must be prepared or otherwise implemented, not treated as a free consequence of a classical sampler. This contrast shows failure of the edge-local construction to inherit the best classical rate, not a lower bound on every quantum realization.

## Resource and claim boundary

The formula uses every directed rate and stationary ratio, and a current-dependent Hamiltonian. Small pi_y can enlarge coefficients and precision requirements. Listing d^2 edges, synthesizing jumps, preparing psi, implementing the Hamiltonian, and obtaining a return certificate are separate paid operations. A succinct classical transition routine does not automatically provide these operations.

The construction does not establish historical novelty. Pure-state reservoir engineering, gauge freedom of Lindblad jumps, and classical embeddings are established machinery; a primary comparison is required before claiming originality. The candidate's purpose is to distinguish existence of a law-preserving pure lift from an efficient acquired return mechanism.
