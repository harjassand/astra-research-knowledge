# A noisy-boundary current compiler for arbitrary ferromagnetic assemblies

2026-11-04. Independently audited scoped construction; see AUDIT.md. No novelty or deployment claim. This document establishes a general-graph partition-response algorithm under its stated promises, not a spin sampler. The prior planar receiver remains unchanged.

## 1. Input, outputs, and exclusions

There are isolated zero-field ferromagnetic planar Ising blocks, each with a finite hidden graph. Their sizes are unknown and unbounded across problem instances. Hard-coupling limits on a fixed finite graph are allowed by the witness limit argument below; infinite-volume limits are not asserted. Block b exposes k_b spins in cyclic order on one face; its hidden graph and size need not be known. Independent equilibrium full-boundary observations are available for each isolated block. Its normalized boundary law P_b has odd moments zero and even moments

F_b(S) = E[product_(i in S) X_i] = Pf(C_b[S]).

The boundary Pfaffian identity and physical ferromagnetic origin are promises. This procedure does not test them. In particular 0<=F_b(S)<=1 for even S.

A known assembly identifies each block port with a distinct port variable belonging to a specified spin vertex. Known edges connect these vertices and any additional known spin vertices with factors 1+a_e x_u x_v, where rational 0<=a_e<=1. Multiple block ports at the same vertex mean hard equality/identification, and are allowed; they were distinct variables in the isolated training laws. Nonnegative fields 1+t_v x_v, 0<=t_v<=1, are represented by edges of activity t_v to a single additional ghost spin. Average this ghost uniformly. Since the unperturbed assembly is globally spin-flip symmetric, the resulting partition response is the same as fixing the ghost to +1. There is no planarity or cofacial-output restriction on the assembly.

For an unambiguous normalization, keep all original block port spins x distinct. Introduce one independent uniform assembly spin y_v per specified vertex, including the ghost if used, and attach every block port i to its assembly vertex v(i) with the equality factor 1+x_i y_(v(i)). Define

Z = E_(x~product_b P_b, y uniform) [ product_ports (1+x_i y_(v(i))) product_known_edges (1+a_e y_u y_v) ].

Every block is normalized by its isolated partition function. The equality factors are twice normalized equality indicators, so conversions to other hard-identification conventions involve known powers of 2. If each boundary variable is merely exposed once and connected by known edges, summing its assembly copy gives exactly the usual normalized response. All following claims refer to the displayed Z, which has empty-current term 1. Known Boltzmann cosh/scalar factors may be restored separately; the unknown blocks' absolute partition functions are not recovered.

We construct an FPRAS for Z from sufficiently accurate empirical pair matrices A_b. We also construct samples of the positive high-temperature/current configuration, including a version conditioned on having no wire defects. We do NOT infer spin samples from current samples: unknown internal cluster connectivity is not supplied by this construction. Arbitrary mixed-sign fields, antiferromagnetic couplings, internal-spin reconstruction, and absolute unknown-bulk free energies are excluded.

Let M=sum_b choose(k_b,2), counted with multiplicity if one trained interface is reused. Define
D=sum_b sum_(i<j) |(A_b)ij-(C_b)ij|.
The statistical precision required below depends polynomially on assembly size as well as the requested accuracy. A fixed training set is not promised to serve arbitrarily large assemblies.

## 2. Coarse high-temperature circuit and defects

There are two types of nodes on the active side of a bipartite factor graph:
- one node of arity k_b with signature F_b for each block;
- one two-leg node with signature diag(1,a_e) for each known edge, including ghost edges.

The other side has an even-parity signature at every known spin vertex. A wire joins each active incidence to its spin-parity incidence. Let H be the number of wires and L=2H the total incidences. The H=0 case has Z=1 and needs no work. There are H active incidences. A half-edge assignment consists of bits on all L incidences.

A defect is a wire whose two endpoint bits differ. Let Omega be the ambient assignments with either zero or exactly two defective wires. The factor weight is the product of all active signatures and all parity signatures. An assignment with a zero factor has weight zero. Let Omega_0 denote zero-defect assignments. A defect sector D_0 is a specified set of zero or two wires; do not confuse this set with the scalar pair error D. There are
R=1+choose(H,2)
sectors.

For tau in (0,1], multiply each ACTIVE incidence carrying bit 1 by tau; do not multiply parity-side incidences. Denote the resulting true weight w_tau(x), its total Z_total(tau), its zero-defect total Z_0(tau), and the normalized law pi_tau on Omega. The desired Z is Z_0(1).

### Lemma 1: source sectors and balance

For each sector D_0, its total is
Z_(D_0)(tau)=Z_0(tau) E_tau[product_(e in D_0) sigma_(v(e))],
where v(e) is the spin-parity endpoint of wire e and E_tau is expectation in a zero-field ferromagnet. Consequently
0<=Z_(D_0)(tau)<=Z_0(tau),
Z_total(tau)<=R Z_0(tau), and pi_tau(Omega_0)>=1/R.

Proof. After specifying active-side bits and D_0, all parity-side bits are determined. At each parity vertex the constraint becomes an even-source constraint, shifted by the number of incident defects. In the ordinary high-temperature expansion this is precisely insertion of the product of the listed spins, with repetitions canceling. The tau factors correspond to attaching a ferromagnetic edge of activity tau between each original block port and its assembly spin, and replacing a known edge activity a_e by a_e tau^2. This remains a zero-field ferromagnet, with ghost treated as an ordinary spin. Its source numerator is nonnegative, and the absolute value of a spin product is 1, proving both inequalities. No hidden graph is required to evaluate a coarse factor.

## 3. Exact winding structure and a quantitative true-chain gap

A nonnegative signature f is even-windable if f(x)f(y) has a nonnegative decomposition indexed by pairings of the differing coordinates, invariant under flipping any pair simultaneously in x and y. This is the definition in McQuillan, arXiv:1301.2880, Section 3.2.

### Lemma 2: exact true signatures are even-windable

Every F_b is even-windable, including arbitrarily high arity and zero entries. The full product signature on the L incidences, with the tau factors included, is even-windable.

Proof. The high-temperature expansion of the physical hidden block is a circuit of even-parity signatures and two-leg signatures diag(1,a), a>=0. Even parity is even-windable (McQuillan Lemma 8); every nonnegative even signature of arity at most three is even-windable (Lemma 7). Circuit contraction preserves even-windability (Lemma 10). The resulting external signature is the source partition function, hence a positive scalar times F_b. Positive scalar normalization preserves the witness. This proof does not require constructing the hidden circuit. Multiplication by unary nonnegative coordinate factors preserves even-windability because the product of the two unary weights is invariant when a differing coordinate is exchanged. Tensor products preserve it by taking unions of pairings. This proves the assertion for tau-scaled block and known factors and all parity nodes. Real-valued signatures obey the same finite nonnegative identities; rationality is not needed for the gap argument. Hard-coupling limits, if included in the block promise, preserve the assertion: each finite-dimensional witness entry is bounded by f(x)f(y), so convergent subsequences of witnesses give a nonnegative witness in the limit.

### Chain

On Omega propose flipping two distinct incidence bits with symmetric probability 1/L^2 for each unordered pair; the remaining proposal probability is a self-loop. Reject a proposal outside Omega. Accept a valid proposal x->y with probability min(1,w_tau(y)/w_tau(x)). On a zero-weight state define a self-loop. Starting on positive support never reaches a zero-weight state.

This is the one-half-lazy version of McQuillan's near-assignment chain in Section 3.5. Theorem 11 and its spectral proof give a gap at least
pi_tau(Omega_0)^2/(2 L^4) >= gamma := 1/(2 L^4 R^2)
on positive support. This includes support connectivity at zeros: the source theorem constructs the flow on the positive-support state space, rather than assuming all factors are strictly positive. Nothing in this bound depends on hidden volume, smallest positive factor, or a winding witness supplied as input.

In particular, if mu<=3 pi_tau pointwise, then the standard reversible L2 bound gives
TV(mu P_tau^T,pi_tau)<=exp(-gamma T).
The chain itself uses only the values of its factors, not the winding witness. This is an application of an established winding theorem, not a new mixing theorem for exact inputs.

## 4. Empirical factors may be non-windable

Evaluate each empirical even moment by a rational Pfaffian and clip it:
Fhat_b(S)=min(1,max(0,Pf(A_b[S]))) for even S;
Fhat_b(S)=0 for odd S.
The empty value is 1. Use these factors, unchanged known factors, and the same tau factors to define v_tau on Omega. It is a nonnegative, exactly evaluable weight function. Its Metropolis chain is defined as above with v instead of w. We DO NOT assert that this chain is rapidly mixing.

Indeed clipping need not preserve windability. On four ports take A13=A24=d>0 and all other entries zero. The clipped signature has f(empty)=1, f(13)=f(24)=d, and all other nonempty values zero. For x=13, y=24, every pairing of their four differing coordinates has a flip leading to a zero product, so invariance would force every witness term to vanish, contradicting f(x)f(y)=d^2. Thus the naive argument 'clip and invoke the winding theorem' is invalid.

### Lemma 3: sectorwise unnormalized weight error

For every defect sector D_0 and every tau in (0,1],
sum_(x in sector D_0) |v_tau(x)-w_tau(x)| <= Z_0(tau) (exp(D)-1).
Consequently E_tau:=sum_Omega |v_tau-w_tau| <= R Z_0(tau)(exp(D)-1), and E_tau/Z_total(tau)<=R(exp(D)-1).

Proof. A mixed derivative of a Pfaffian with respect to pair entries vanishes unless those pairs form a matching. For a matching with endpoint set U, the derivative at C, in any larger even subset S containing U, has absolute value F_b(S\U). The crossing sign may depend on S but disappears in the absolute value. At tau-scaled factors this absolute derivative is tau^|S| F_b(S\U).

Fix matching derivatives in any collection of blocks. Their contribution to the nonnegative sector sum therefore fixes all legs in U active and replaces each affected block's remaining signature by its genuine marginal moment signature, with spin flips discarded. This restricted source sum is bounded by Z_0(tau). Here is a spin/Fourier proof that also covers repeated boundary identifications. Keep original port spins x distinct and set

W_tau(x)=E_(y uniform)[ product_ports (1+tau x_i y_(v(i))) product_known_edges (1+a_e tau^2 y_u y_v) ].

Set V_tau(x) to the same expectation with the product of defect-source spins y_(v(e)) inserted. Then |V_tau(x)|<=W_tau(x). Both have nonnegative Fourier coefficients: expansion uses nonnegative activities, and averaging y merely enforces unshifted or shifted parity. Also Z_0(tau)=E_(product_b P_b) W_tau.

Write U for the union of all selected derivative endpoints, with U_b its subset in block b. After summing known edge bits, the absolute derivative contribution is exactly

sum_(T disjoint U) FourierCoeff(V_tau,T union U) product_b F_b(T intersection block_b),

where odd block subsets give zero. This sum is nonnegative and equals
E_(x_rest in the true independent block marginals) E_(x_U uniform)[V_tau(x) product_(i in U) x_i].

Its absolute value is at most the analogous expectation of W_tau without the spin product. Finally this last expectation is <=E_(product_b P_b)W_tau=Z_0(tau): uniformizing U removes Fourier terms meeting U, and every remaining or removed coefficient and true block moment is nonnegative. This proves the derivative-sum bound, including all tau factors already present in V_tau. The sign of a Pfaffian derivative can depend on T; taking its absolute value is justified because the remaining true block moment is nonnegative.

For each block, expand Pf(A[S])-Pf(C[S]) by its exact finite multilinear Taylor formula. Clipping to [0,1] cannot increase its distance to F_b(S) in [0,1]. Expand the difference of products over blocks around the true nonnegative factors, and bound each selected factor difference by the sum of the absolute Taylor terms. Each resulting term is one of the matching derivatives just bounded. Summing its products of |Delta_ij| over all nonempty choices is at most sum_(r>=1) D^r/r! = exp(D)-1. This uses the combined entry-error sum over all block occurrences. It does not require any intermediate empirical matrix or clipped factor to be physical. Summing the R sectors gives the last assertion.

## 5. A robust-kernel lemma, not perturbation of spectral gaps

Let w,v be nonnegative weights on a common finite ambient space, with Z=sum w>0 and E=sum|w-v|. Let P,Phat be their Metropolis kernels with the same symmetric substochastic proposal q, completed by self-loops, and self-loops on zero-weight states. Let pi=w/Z. Then
sum_x pi(x) TV(P(x,.),Phat(x,.)) <= 3E/Z.

Proof. For positive w_x,v_x and off-diagonal y,
w_x |Pxy-Phatxy|
<=qxy ( |min(w_x,w_y)-min(v_x,v_y)| + |w_x-v_x| )
<=qxy (2|w_x-v_x|+|w_y-v_y|).
If v_x=0<w_x, the left side is qxy min(w_x,w_y)<=qxy|w_x-v_x|, so the same bound holds. Terms with w_x=0 carry no pi mass. Symmetry and row sums <=1 imply the total off-diagonal bound 3E. The diagonal difference is bounded by the off-diagonal sum, canceling the factor 1/2 in TV.

If mu<=B pi, then mu P^s<=B pi for every s. A telescoping comparison, using stochastic-kernel contraction on all later Phat factors, yields
TV(mu Phat^T,mu P^T)<=3 B T E/Z.
An approximate starting distribution adds its TV discrepancy without multiplication by B. The domination is used only for the TRUE trajectory. No claim is made about pointwise transition accuracy, mixing of Phat, or its warmness.

For our chains, a 3-warm start therefore contributes at most
9 T R (exp(D)-1)
trajectory error in one annealing stage.

## 6. Initialization and warm-start annealing

Let 0<zeta<=1/4 be the requested TV accuracy for the near-current sampler. Set
 tau_start = zeta/(16 R H).
At tau=0, positive support consists of all active bits zero, and either no defects or two defects incident to the same parity vertex. Every such state has weight 1. Their number is
B0=1+sum_v choose(deg(v),2)<=R.
They can be explicitly enumerated in polynomial time. Start uniformly on this set.

For each active bit pattern there are at most R choices of a defect sector, and each parity-side assignment is then determined. All unscaled true factors are <=1. Thus weight outside the tau=0 support at tau_start is at most
R((1+tau_start)^H-1)<=2 R H tau_start=zeta/8.
The normalized starting law is within zeta/8 of pi_(tau_start).

Increase tau by factors at most 1+1/H, stopping exactly at target tau_target<=1. If target is smaller than tau_start, initialize instead with tau_start replaced by target and no annealing; the same estimate holds. For target>=tau_start let S be the actual number of stages. It satisfies S=O(H log(RH/zeta)). For a zero-stage call initialization alone suffices. Otherwise let
T=2 L^4 R^2 ceil(log2(16 S/zeta)).
At consecutive stages each unnormalized weight ratio lies in [1,(1+1/H)^H] subset [1,3]. Therefore pi_old<=3 pi_new. The true chain mixes from pi_old to accuracy zeta/(16S) after T steps.

Assume training ensures
D <= zeta/(288 S T R).
Then exp(D)-1<=2D<=zeta/(144 S T R), and each empirical stage adds trajectory error at most zeta/(16S). Induction over the stages, carrying prior TV error additively, shows the ideal-rational implementation has final TV error at most
zeta/8 + S(zeta/(16S)+zeta/(16S))=zeta/4.
Reserve another zeta/4 for all capped random-number/coin operations. The resulting bounded-runtime sampler is within zeta of the true near-current law. The displayed D requirement is sufficient, not optimized. One may use worst-case S and T for target 1 uniformly across all calls.

To sample a perfect current to TV accuracy xi, make J>=R log(2/xi) independent near-current calls of accuracy at most xi/(4J), return the first zero-defect sample, and on total failure return the all-zero perfect current. Under exact calls rejection fails with probability <=xi/2, and the J-call coupling error is <=xi/4. Thus the output is within xi. This does not sample physical spins.

## 7. Relative partition-response estimation

Fix requested 0<epsilon<=1/2 and failure probability beta. Build a counting schedule from
s0=epsilon/(64 R H)
to 1, with ratios at most 1+1/H. Let its number of stages be K. Write r_j(x)=(s_j/s_(j-1))^(number of active 1 bits). Then 1<=r_j<3 and
Z_total(s_j)/Z_total(s_(j-1))=E_(pi_(s_(j-1))) r_j.
Also q=pi_1(Omega_0)>=1/R and Z=Z_total(1)q.
The initial total satisfies B0<=Z_total(s0)<=B0+epsilon/32, so replacing it by B0 incurs relative error at most epsilon/32.

Set a=epsilon/(16 R(K+1)) and zeta=a/12. Use independent near-current sampler calls of accuracy zeta to estimate each of the K ratio expectations and q. For each quantity use
N_count >= (18/a^2) log(2(K+1)/beta)
independent draws. Hoeffding's inequality and the TV bias bound (range at most 3) imply that, except with probability beta, every empirical expectation differs from its true value by at most a. Ratios have true mean >=1; q>=1/R. Hence the product
Zhat=B0 (product_j rhat_j) qhat
has logarithmic relative error less than epsilon/2 using |log(1+u)|<=2|u| for |u|<=1/2. In particular (1-epsilon)Z<=Zhat<=(1+epsilon)Z. If any estimate is zero, return a fixed fallback; that case lies outside the successful estimation event.

All sampler calls use the same trained A and worst-case training precision for zeta. Conditional on the training event, their random bits are independent. Statistical concentration therefore applies despite shared training data. Overall success probability is at least 1-alpha-beta if the training event fails with probability at most alpha. The costs of fresh calls and their full annealing runs are counted, rather than treating correlated successive chain states as independent.

## 8. Data, representation, and bit complexity

For M>0, let d_target be the displayed D budget for the near-current accuracy zeta used by the intended algorithm. Set h=d_target/M. N>=2h^(-2) log(2M/alpha) independent full-boundary observations per distinct block suffice by Hoeffding and a union bound. Reused summaries count their error per occurrence in M; the union bound may instead use the smaller number of distinct measured pairs. M=0 needs no training. The bound is polynomial, with large unoptimized exponents, in assembly size and inverse requested accuracy. It is not a practical-speed claim.

Empirical entries are rational with denominator N. A Pfaffian of a k-by-k submatrix is an integer polynomial of degree k/2 in those entries. Its exact numerator/denominator bit length is polynomial in k and log N, and fraction-free elimination or exact rational elimination evaluates it in polynomial bit time. Clipping uses exact comparisons. The known activities are supplied rationally, and their encoding lengths are charged. Arbitrarily large binary-encoded physical fields are not implicitly converted to exponentially long activities. Products of at most polynomially many factor values and powers of rational tau have polynomial bit length. The rational schedule tau_start(1+1/H)^j, capped at its target, has polynomial bit length because j is polynomial.

A Metropolis step needs only a polynomial number of exact factor evaluations and one rational acceptance coin. Probabilities 0 and 1 are handled deterministically. Other a/b coins use unbiased integers on ceil(log2 b) bits, rejecting integers >=b; one trial succeeds with probability at least 1/2. The proposal and uniform-base draws can be implemented by the same bounded-rejection method. Cap each draw at a number of attempts logarithmic in the deterministic total draw budget divided by its allocated failure probability. On a cap, stay in the current state (or select a fixed base state at initialization). A union-bound coupling charges at most the reserved TV error. Thus runtime, storage and random-bit use are bounded polynomially, not merely in expectation.

The true physical factors may contain arbitrarily tiny positive numbers. They enter only the proof, not the implementation. Warm starts remove log(1/min pi) from the required runtime; the gap bound uses only R and L. This is the purpose of the global-weight-error and annealing argument.

## 9. Tests and strongest baseline

Exact rational test instance: four observed leaves coupled to one hidden center, each tanh coupling 1/10, assembled with all six K4 edges of activity 1/2 among the leaves. The full physical graph is K5, genuinely nonplanar, with all its ten couplings positive. Empirical A increases crossing entries A13 and A24 by 1/50. Its fourth Pfaffian is -7/10000 and is clipped to zero. For tau=1,1/2,1/10, enumerate all 121 zero/two-defect sectors and compare coarse current sums with direct five-spin source enumeration. All sectors agree exactly and satisfy Z_sector<=Z0. The sectorwise and total absolute clipped-weight error bounds pass exactly using the finite Taylor envelope (1+1/50)^2-1. A separate exact finite-state test checks the kernel-error inequality for 676 pairs of three-state nonnegative integer weight vectors, including deleted and newly created support. These tests are checks, not proofs of uniform assertions.

Established components must not be relabeled as new:
- Boundary Pfaffian identities: Groeneveld–Boel–Kasteleyn (1978), https://doi.org/10.1016/0378-4371(78)90214-5.
- Exact physical boundary characterization and inversion: Galashin–Pylyavskyy (2020), https://doi.org/10.1215/00127094-2019-0086; nonrecursive inversion: Elmaazouz–George (2026), https://arxiv.org/abs/2606.15082.
- Winding closure and near-assignment chain: McQuillan, Sections 3.2–3.5, especially Lemmas 7,8,10 and Theorem 11, https://arxiv.org/abs/1301.2880.
- Explicit arbitrary-graph consistent-field ferromagnet approximation is established by Jerrum–Sinclair (1993), https://doi.org/10.1137/0222066. Later samplers may be much faster on explicitly supplied graphs.
- Bounded-genus matchgate contraction is established by Bravyi (2008), https://arxiv.org/abs/0801.2989; the present algorithm does not expand over genus.
- Approximate-kernel MCMC and finite-time perturbation bounds are established subjects; see Alquier–Friel–Everitt–Boland, https://arxiv.org/abs/1403.5496. The elementary kernel comparison here is proved in full and is not claimed as a new general perturbation principle.

The matched input here is passive noisy boundary data plus a known assembly, not the original hidden graphs. With exact valid boundary-factor access, the winding algorithm already supplies the exact-factor baseline. The proposed extra operation is tolerance of nonphysical signed empirical Pfaffian matrices without positive realization or assuming their clipped factors mix. The central new argument within this document is the sectorwise error certificate plus true-trajectory warm-start simulation. Whether this combination is novel requires separate literature review. Practical advantage, physical experimental validation, and civilization-scale consequence have not been demonstrated.
