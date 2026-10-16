# Independent audit: optimal single-use phase-noise recovery

## Scope and conventions

Let the physical basis be ordered by S_z eigenvalues (-3/2,-1/2,1/2,3/2), let theta be Gaussian with mean zero and variance v >= 0, and let N_v average conjugation by exp(-i theta S_z). Thus a matrix element separated by d receives exp(-v d^2/2). Set x=exp(-v/2), so nearest-neighbor, separation-two, and separation-three factors are x, x^4, and x^9.

The encoder maps logical basis vectors to L0=(1/2,0,sqrt(3)/2,0) and L1=(0,sqrt(3)/2,0,1/2). Recovery is any CPTP map from the physical four-dimensional system to a logical qubit. Fidelity below is entanglement fidelity for the maximally mixed logical input, equivalently overlap with a maximally entangled reference pair. Average pure-state fidelity is (2 F_e + 1)/3. These are single-use statements; they do not authorize composition of averaged maps for temporally correlated noise.

## 1. Unrestricted recovery: the claimed bound is exact

Write A=span{|0>,|2>} and B=span{|1>,|3>}. The noisy logical populations rho_i=N_v(|Li><Li|) are density matrices supported on A and B respectively. The noisy logical cross operator C=N_v(|L0><L1|), regarded as a map B to A, is

C = (1/4) [[sqrt(3) x, x^9], [3 x, sqrt(3) x]].

For any recovery R,

4 F_e = <0|R(rho_0)|0> + <1|R(rho_1)|1> + 2 Re Tr[ |1><0| R(C) ].

Each population term is at most 1. The adjoint R* is unital and completely positive and therefore is an operator-norm contraction. Hence

|Tr[R*(|1><0|) C]| <= ||R*(|1><0|)||_infinity ||C||_1 <= ||C||_1.

For completeness, contraction follows from Kadison-Schwarz: R*(X)^dagger R*(X) <= R*(X^dagger X) <= ||X||_infinity^2 I. Consequently F_e <= (1+||C||_1)/2.

The bound is attained. Take the polar decomposition C=U|C|, extending its partial polar isometry to a unitary B -> A when necessary. Choose an environment identified with B and define an isometry V by

V a = |0> tensor U^dagger a for a in A,
V b = |1> tensor b for b in B.

The map R(X)=Tr_env[V X V^dagger] is CPTP. It maps every normalized population in A to |0><0| and every normalized population in B to |1><1|, so both population terms equal 1. Its cross coherence is Tr(U^dagger C)=Tr|C|. This establishes the optimum without assuming a particular recovery apparatus, bath dimension, measurement scheme, or Kraus rank in the upper bound.

For a 2x2 matrix, ||C||_1^2=Tr(C^dagger C)+2|det C|. Here det C=3(x^2-x^10)/16 >= 0, so

||C||_1 = sqrt(21 x^2 - 6 x^10 + x^18)/4,
F_e,opt = 1/2 + sqrt(21 x^2 - 6 x^10 + x^18)/8.

The construction works also at v=0 and in the x -> 0 limit, with arbitrary unitary polar extensions.

## 2. Exact code-space fixing: the claimed restricted optimum is exact

Here “fixes the code space” means R(|Li><Lj|)=|i><j| for all i,j, not merely that the two logical basis populations are fixed. The latter weaker requirement would not impose the following conclusion.

Let E0=(-sqrt(3)/2,0,1/2,0), E1=(0,-1/2,0,sqrt(3)/2), which are (2/sqrt(3)) S_z Li. Then {L0,L1,E0,E1} is orthonormal. Let W be any Stinespring isometry of an exactly code-fixing recovery. Purity of the two recovered basis states gives W Li=|i> tensor e_i for normalized environment vectors. Preservation of |L0><L1| forces <e_1|e_0>=1, so e_0=e_1=e. Orthogonality of W E_j to both W L_i then puts every W E_j in logical tensor e-perpendicular. Taking the environmental trace therefore annihilates every operator |Li><Ej| and its adjoint.

This proves, rather than assumes, that exact code fixing discards all code/error cross blocks, even for an arbitrary recovery environment. The induced channel on span{E0,E1} can otherwise be any CPTP qubit channel: it can be implemented in an environmental sector orthogonal to e.

Projecting the noisy population rho_i onto its code and error directions gives

p = <Li|rho_i|Li> = (5+3 x^4)/8,
q = <Ei|rho_i|Ei> = 3(1-x^4)/8,
p+q=1.

The surviving noisy logical cross coefficients are

c_L = <L0|C|L1> = (15 x + x^9)/16,
c_E = <E0|C|E1> = 3(x-x^9)/16 >= 0.

The fixed code branch contributes (2p+2c_L)/4 to F_e. On the error branch, the two correctly decoded population terms are each at most q, and the recovered cross coefficient has magnitude at most c_E by the same adjoint contraction argument. All these bounds are simultaneously attained by mapping E0 to logical 0 and E1 to logical 1 coherently within that branch. Thus

F_e,fix = (p+q+c_L+c_E)/2 = (1+r)/2,
r=(9x-x^9)/8.

Explicit optimal decoded Kraus operators are

K_L=|0><L0|+|1><L1|,
K_E=|0><E0|+|1><E1|.

If the recovery instead outputs the encoded physical qubit, postcompose with the encoding isometry: its Kraus operators are P_L and |L0><E0|+|L1><E1|. The sum of their adjoint products is I_4. Thus the familiar recovery is optimal under exact code-space fixing; no attribution to a publication is needed for this mathematical conclusion.

The unrestricted norm and fixed-space coherence satisfy

||C||_1^2-r^2 = 3 x^2 (1-x^8)^2/64.

Accordingly the unrestricted optimum is strictly better for every finite v>0, and equal at v=0 or in the infinite-dephasing limit. The strict gap is compatible with restricted optimality: the unrestricted polar recovery generally does not fix the noiseless code exactly.

## 3. Mirror-code family: both proposed optimizations check out

For 0<=u<=1, take L0(u)=(sqrt(u),0,sqrt(1-u),0), L1(u)=(0,sqrt(1-u),0,sqrt(u)). The Li code corresponds to u=1/4. Use E0(u)=(-sqrt(1-u),0,sqrt(u),0) and E1(u)=(0,-sqrt(u),0,sqrt(1-u)). Set y=x^8.

The cross matrix is

C_u = [[sqrt(u(1-u)) x, u x^9], [(1-u) x, sqrt(u(1-u)) x]].

The same unrestricted proof and construction apply because the supports A and B remain disjoint. Its norm is

||C_u||_1^2 = x^2 [1+2u(1-y)-u^2(1-y)(3+y)].

For 0<x<1 this is a concave quadratic in u with maximum at u=1/(3+y), yielding ||C_u||_1=2x/sqrt(3+y). At v=0 all u give norm 1; in the x=0 limit all give norm 0, so the displayed u is a maximizing choice, not a unique optimum at these endpoints.

For exact code-space fixing, the same Stinespring argument applies. The two branch coherences are

c_L(u)=(1-u^2)x+u^2 x^9,
c_E(u)=u(1-u)(x-x^9)>=0.

The population weights are p=u^2+(1-u)^2+2u(1-u)x^4 and q=2u(1-u)(1-x^4), again summing to 1. Therefore

r_fix(u)=c_L(u)+c_E(u)=x[1+u(1-2u)(1-y)],
F_e,fix(u)=(1+r_fix(u))/2.

For 0<x<1 this has its unique family maximum at u=1/4. Thus optimizing unrestricted recovery and encoder within this family moves u away from 1/4, while optimizing exact-code-fixing recovery leaves u=1/4 optimal.

## Limits of the conclusions

- No global optimality claim is established over all possible four-dimensional encoders; the encoder optimization above is only within the specified mirror family.
- The unrestricted construction is a mathematical CPTP recovery. It does not establish improved performance under specific hardware controls, finite gate errors, operation times, or environment restrictions.
- Exact code-space fixing is a strong linear channel identity on the entire code algebra, including coherences.
- Gaussian single-use phase averaging is specified explicitly. Multiple uses with a persistent random phase require a joint temporal noise model. Composing N_v as though the phase were independently redrawn can give a different physical channel.
