# Explicit high-reset local forgetting for guarded qubit clocks

Model on the FULL qubit tensor product: H=sum_z g X_z product_{y~z}(I-n_y), jumps sqrt(kappa) sigma^-_z. Maximum degree D. Legal independent-set space is invariant, so the conclusions apply there too. No stationary full-rank assumption.

## Coefficient norm

Use tensor strings of the single-site basis (I,n,sigma+,sigma-). Write A=a_empty I+sum_{alpha!=empty} a_alpha B_alpha and q(A)=sum_{alpha!=empty}|a_alpha|. Let M_1(A)=sum |support(alpha)| |a_alpha|. Every basis string has operator norm <=1, hence distance from A to scalars in operator norm <=q(A).

The damping adjoint is diagonal: n has rate -kappa; sigma+/- rate -kappa/2. A string therefore decays at rate >=kappa |support|/2.

On one site, left or right multiplication by X or by P=I-n has coefficient l1 operator norm <=2. Hence multiplication by H_z on a basis string has coefficient sum <=g 2^(D+1), and i[H_z,.] has sum <=g 2^(D+2). The commutator vanishes if its star misses the string support. At most (D+1)|support| stars can meet that support.

Set C_D=2^(D+2)(D+1), lambda=kappa/2-C_D g. For the coefficient ODE of T_t(A), the upper Dini derivative obeys

 d+ q(T_t A)/dt <= -lambda M_1(T_t A) <= -lambda q(T_t A).

Identity inputs generate nothing, so quotienting by identity is exact. Consequently if lambda>0,

 q(T_t A)<=exp(-lambda t)q(A),
 |Tr[(rho-sigma)T_t A]|<=2 exp(-lambda t)q(A)

for ANY pair of global states, uniformly in total graph size. For m-local A one may use the crude estimate q(A)<=5^m ||A||: the single-site coefficient functionals have norm bounds 1,2,1,1, and their tensor products have multiplicative trace norms.

The same column bound counted ALL Hamiltonian outputs, including identity. Therefore the full coefficient l1 logarithmic norm is <=0: identity columns vanish and every nonidentity column has diagonal damping loss exceeding its total Hamiltonian column bound. Thus

 ||T_t A||_coeff <= ||A||_coeff.

On every finite graph, existence of a stationary state plus contraction gives uniqueness and convergence. The prefactor for a genuinely global observable can grow exponentially in N, so this calculation alone should be called uniform LOCAL forgetting, not a proven O(log N) global trace-norm mixing theorem.

## Distance-weighted version

Fix initial support X. Give each nonidentity string the weight exp(a r_X(S)), where r_X(S)=max_{v in S}dist(v,X), and a>0. A Hamiltonian star changes this radius by at most two. The same proof gives

 d+ q_a(T_t A)/dt <= -lambda_a M_{1,a}(T_t A),
 lambda_a=kappa/2-C_D g exp(2a).

If lambda_a>0, q_a(T_t A)<=exp(-lambda_a t)q(A), and integral_0^infinity M_{1,a}(T_t A)dt<=q(A)/lambda_a. Thus coefficient mass reaching distance R is <=exp(-aR-lambda_a t)q(A). This is a constructive killed-branching/cluster estimate for observable propagation, not yet for the full jump-record probability measure.

## Important boundary

Uniform local forgetting is real, but it does NOT by itself imply a product upper bound for simultaneous missing-event faults. Future-record conditioning changes the generator. A separate record-instrument or tilted-generator cluster estimate is required.
