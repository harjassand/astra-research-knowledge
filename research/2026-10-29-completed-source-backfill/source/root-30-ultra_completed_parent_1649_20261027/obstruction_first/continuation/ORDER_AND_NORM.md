# Supporting interfaces: positive gates, relative order and norm-aware lifting

The final lead is the actual source-kernel compression in CONSTRUCTION.md.
These earlier constructions are preserved at their real scope; none acquires
the missing cold uniform-chain seed.

## Actual positive gate and CP map

In the real spin-two representation, exact algebra gives

    g_d=I−dh+d^2h^2/2=sum_(r=0)^8 A_r tensor A_r,
    A0=sqrt(1+6d^2)I, A_alpha=sqrt(d+d^2/4)G_alpha,
    A_a=d T_a/sqrt2,
    T_a=sum_(i,j)e_a,ij({G_i,G_j}/2+2delta_ij I).

Here e_a are the five orthonormal symmetric traceless3x3 tensors. The checked
coefficient identity is h^2/2=6I+(sum G_i tensor G_i)/4+(sum T_a tensor T_a)/2.
The physical polynomial is strictly positive. With c=1+6d+18d^2,
Phi(R)=sum A_r R A_r^T obeys Phi(I)=Phi*(I)=cI and Phi−Id is CP.

For N history letters put K_N(x,y)=Tr product_t(A_y_t A_x_t), Q_N=K_N K_N^T.
Their virtual dimensions are5 and25. The local matrices of Q are
B_xy=g_d(A_x tensor A_y). Its norm map E=Ad_g o(Phi tensor Phi) has order25
and Tr E^N=Z_(4),N. For Q_N^m the uncompressed virtual dimension is25^m;
the norm superoperator dimension is5^(4m). Equal power traces with the
physical4m-site checkerboard step imply equal spectra by Newton identities.
Thus its first-order Perron log-gap/d tends to the physical finite-ring gap.
Dimension-uniform first-order contraction would itself prove the target gap.
The four-site complete-spectrum/index diagnostic agrees to1.87e−14.

The actual quadratic norm map is not automatically in a strong-noise/EB
sufficient family. ||g||=c, ||g−I||<=c−1 and the CP difference
Phi tensor Phi−Id has diamond norm c^2−1. Hence ||E−Id||_diamond<=c^4−1.
An antisymmetric Schmidt-rank-two PT Choi witness has identity value−1 and
perturbation at most(25/2)(c^4−1). At d.001 its directed upper is below
−0.6963728618. E is NPT/not EB. This excludes that sufficient route only,
not every invariant cone. The peer's ordinary Marshall sign-free construction
is a distinct positive representation.

E*(I)<=c^4I, so B_xy/c^2 are a trace-decreasing instrument with retained
scalar kappa=c^4. Its Bell-return probability after N steps is exactly
Tr E^N/(25^2*kappa^N). A beta50,d.001,N50000 dominant-mode numerical
diagnostic has log10 probability about−89.65. It is not a rigorous asymptotic
or a universal sampling lower bound. A useful Doob metric must be acquired.

The exact pair exp(−dh) also has a real reflection-positive factorization,
rank25 for d>0: its vectorized map is exp[d sum G_i(·)G_i^T]. After dividing
by exp(6d) this is the standard SU(2) heat channel, with multipole eigenvalues
exp[−d*j(j+1)/2], j0–4. Its positive word expansion spans real5x5 matrices.
This eliminates Taylor error but increases the history alphabet. The exact
gate budget below is never combined with a rank9 quadratic factorization.

## Relative order actually acquired for an uncompressed Strang step

The ordinary comparison principle is valid: if A(t)>0, A(0)=I and
E=A'+(HA+AH)/2 satisfies −epsilon A<=E<=epsilon A, then

    exp(−omega)e^(−tH)<=A(t)<=exp(omega)e^(−tH),
    omega=integral epsilon.

Differentiate exp(tH/2)A exp(tH/2) and apply scalar matrix Gronwall. The
principle alone supplies neither a generalized residual nor an inverse.
For matching sums H=A+B and S_t=e^(−tA/2)e^(−tB)e^(−tA/2)=M_t M_t*,
M_t=e^(−tA/2)e^(−tB/2), direct differentiation gives

    M_t^−1 E M_t^−*=Herm(e^((t/2)ad_B)e^((t/2)ad_A)B)−B.

The first-order commutator is skew. The two remainders have coefficients
t^2/8 and t^2/4 multiplying [A,[A,B]] and [B,[A,B]], with conjugations.
For C4=[h01+h23,[h01+h23,h12]], both nested norms are at most(n/2)||C4||,
by grouping the central odd/even bond. Centering h at h+I gives norm5 without
changing commutators. Conjugations touch at most two A bonds and three B
bonds, so their combined factor is at most exp(25t).

`relative_order_bridge.py` acquires ||C4||<=165: C4=C0+sqrt6 C1 has integer
sparse625x625 coefficients. For rational sqrt6 endpoints the symmetric
entrywise upper U passes Uw<=165w for a positive rational w, in every row.
The Schur test proves the bound; numerical eigenvectors only produced w.
The resulting order error is omega<=165*n*d^3*exp(25d)/16. Min-max and
eigenvalue powers give

    |log Tr S_d^N−log Z_n(beta)|
        <=165*n*beta*d^2*exp(25d)/16, beta=Nd.

This needs589043 exact-gate slices at n128,beta64 for error.001, with history
dimension25^N. It is an uncompressed representation budget, not a practical
contraction or a speedup. The earlier quadratic compiler separately pays
Taylor error and is retained as a weaker sufficient budget.

Relative order can also be unnecessarily strong. The known all-up projector
P has energy4n. A_beta=e^(−betaH)−(1−e^(−Kbeta))e^(−4nbeta)P is positive,
A_0=I, and needs generalized residual epsilon>=K. Yet for every p>=2 its
relative Schatten error is at most exp(−4nbeta), and its HS error at most
exp(−4nbeta)5^(−n/2), by TrH=0. At n128,beta64,K16 the order log error is1024
while HS error is below10^(−14275). Removing that tiny weight entirely
defeats every finite two-sided order bound. This is a mathematical accuracy
boundary, not an acquisition of the unknown Gibbs operator.

## Weaker acquired norm control supports positive temperature lifting

Let Y=e^(−beta(H+an))>0. Suppose e>=||M−Y||_2 is acquired and normalized v
gives r=Re<v,Mv>, L=r−e>0. Then for every p>=2,

    ||M−Y||_p<=e<=eta||Y||_p, eta=e/L,

because ||Y||_p>=||Y||_op>=<v,Yv>>=L. No ground fidelity/gap is needed.
For integer q>=1, eta<=1, Holder plus a telescoping sum gives

    ||(M*M)^q−Y^(2q)||_p/||Y^(2q)||_p
       <=q*eta*(2+eta)*(1+eta)^(2q−2)
       <=3eta*q*exp(3eta*q).

Use the input norm2pq, then the difference M*M−Y^2 in normpq and q Holder
factors per telescoping term. Only p>=2 is needed for HS-square partition
functions. A normalized MPS Rayleigh contraction may supply r, but its norm
and length-specific acquisition are costs. Stage1's64-site certificate is
not transferred to other n. At common relative HS error eta the S/T point
norm ratio has factors[(1−eta)^4/(1+eta)^2,(1+eta)^4/(1−eta)^2].

Unqualified HS control fails on the actual uniform model. With D=5^n,
TrH=0 and H>=−6n, ||Y||_2>=sqrtD and ||Y^2||_2<=sqrtD exp(12beta n), a0.
For any known product projector P, M=Y+epsilon sqrtD P is positive and has
HS-relative error<=epsilon, but squared relative error at least

    epsilon^2 exp[n(log5/2−12beta)].

At n400,beta1/96,epsilon1e−6 this exceeds10^106.079. This is an HS-only
guarantee obstruction, not a no-go for structured algorithms or an efficient
representation of Y. A physical dimer model supplies a small-MPO version:
at the same parameters squared relative error exceeds10^127.566. Conversely
at beta20 its known ground projector has exact discard<5.049e−8, Rayleigh1;
q8 lifting to beta320 has error<1.212e−6 for all p>=2. The directed control is
executed in `norm_temperature_bridge.py`, without transfer to the uniform
chain. All-Schatten positive-power methods are prior KAA machinery.
