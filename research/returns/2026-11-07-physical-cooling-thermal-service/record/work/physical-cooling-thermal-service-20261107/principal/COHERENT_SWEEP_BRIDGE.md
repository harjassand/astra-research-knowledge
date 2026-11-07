# Direct finite-collision service under coherent retained-bath errors

7 November 2026. Constructive challenge following frozen initials. This note develops the principal's finite-depth local-observable route using the auditor's deterministic density/sweep combinatorics. It does not modify the initials. Status: theorem candidate pending challenge.

## 1. Abstract data and quantum module

Let S_N be a stabilizer DATA family with distance >=delta N, a commuting nonnegative integer syndrome function U=sum local u_v, bounded term size/incidence/norm. Let D_E bound incident energy per qubit. Suppose every valid syndrome with U<u_des N has a canonical Pauli representative of weight <=C0 U and >=kappa U labels in a bounded-incidence local lowering catalog. A catalog update is an energy-resolved Pauli (full local read support included). Each decreases integer U by at least1 when active. Supports, label count <=cN and dependency degree are uniform. Pick u_c<min(u_des,delta/(8C0)). On P_c=1_(U<u_c N), every local leg with safe endpoints acts id_L on the full fixed canonical operator module, including arbitrary bath/reference and syndrome coherence coefficients. Prior capital establishes this for the chosen two-sector energy. Let R be a uniform upper bound on initially active label predicates that one lowering operation or one local fault can change, enlarged to include its own label.

Ground-ancilla full-exchange collision for label (a,d>0): A=P_a Pi_(a,-d), H_ex=kappa(A tensor sigma_plus+A dagger tensor sigma_minus), ancilla gap Jd. It commutes with JU+Jd n_A. At angle pi/2, the ground-ancilla channel is the deterministic lowering map with Kraus I-Pi_(a,-d) and -i A. Full unitary evolution with ground ancilla is nonincreasing in memory energy at each intermediate collision time. Apply all labels in a fixed constant-depth coloring of full support neighborhoods.

## 2. Ideal whole sweep

For an initial eigen-syndrome of energy u and no faults, let S be successful decreases during the sweep. Each initially active label either succeeds or was spoiled by an earlier successful decrease. Therefore kappa u<=R S. With a=min(1/2,kappa/(2R)) the output energy is <=(1-a)u. The same support inclusion extends linearly to coherent inputs supported below a cutoff: nominal Kraus legs follow syndrome paths and all output energies satisfy the bound. Ideal memory energy never exceeds its input value. Thus the ideal ground sweep W0, retaining its O(N) ancillas, is a logical identity isometry on P_c, with a strict energy contraction at the endpoint. Ground ancillas discarded only at the end.

All collision layers have fixed duration. The free commuting Hamiltonian JU+sum Jd n_A commutes with every exchange. Its evolution is a bounded-depth product of commuting local gates for any fixed interval. Consequently W0(t2,t1) has bounded DATA/ancilla causal cones uniformly during one sweep, even though it is not Clifford.

## 3. Local coherent errors and finite-depth pull-through

Retain an arbitrary environment B and arbitrary bath-only unitary/CPTP propagation. Assume actual full interval dynamics is CPTP and admits a Duhamel expansion around W0 tensor bath with local HP/trace-annihilating perturbations N_Z(t). Their full DATA-plus-current-ancilla support is at most q, while their B support can be unrestricted. Complete norm budget sum_Z int ||N_Z||cb <=mu N per sweep; each ideal suffix enlarges finite system support by at most a fixed factor b. Nominal B propagation never couples strongly to future fresh sources; any returning bath-to-DATA interaction is included in N_Z.

After moving an error insertion through the ideal suffix, its DATA/ancilla support is <=q_eff=bq, with arbitrary B coefficients. An r-insertion term is therefore a superoperator on <=q_eff r physical system positions following ideal W0. Low-order terms cannot create output memory energy above (1-a)u+D_E q_eff r and, at those endpoints, are logically neutral on the full canonical module when the total correction/error support stays below distance. This argument uses finite-depth cones of W0, not a global approximation of a macroscopic bath.

The high-order complete norm tail is bounded by sum_(j>m)(mu N)^j/j! <=2(e mu N/(m+1))^(m+1) if m+1>=2mu N. For m=floor(alpha N), choose fixed mu<alpha/(8e), giving exp(-cN). No parameter needs to improve with N or service duration. Physicality/CPTP of the full map and complete norms are essential. Signed perturbation summands alone do not establish them.

## 4. Thermal and imperfect source inputs

Each fresh ancillary qubit of gap Jd is thermal, excitation r_d<exp(-beta J). Its mixed state is an exact independent convex mixture of ground and excited branches. A set F of excited cells is equivalent to input X faults. Pull them through W0 to the output; each has a bounded output cone. The all-subset intensity <=p_src^|F| gives an exponential tail for |F|>zeta N at fixed p_src<zeta/(e c). A local approximate thermal reset can be converted to an exact reference-safe CP mixture using full-rank Choi minorization, but joint common-bath renewal must be proved separately.

For each retained source pattern |F|<=zeta N and each insertion term r<=alpha N, output energy <=(1-a)u+D_E q_eff(alpha+zeta)N after adjusting q_eff to include source cones. The underlying ideal ground sweep has input supported below u_c N. The entire low-order term has output canonically equivalent to the same logical state if (2C0 u_c+q_eff(alpha+zeta))N<delta N.

Choose a reset operating cutoff u_s<u_c with D_E q_eff(alpha+zeta)<a u_s/4 and strict canonical margins. Output lies strictly below u_s N when input does. A warm input below a larger u_w<u_c returns to u_s after a fixed number of sweeps, provided the same source term and distance margins hold; output energy recurrence is v_next=(1-a)v+e, e=D_E q_eff(alpha+zeta), and v_infty=e/a<u_s.

## 5. Positive repair operation to audit

Let Gamma be an actual CPTP sweep, Q=P_(U<u_s N), and restrict the input to I_L tensor G_s tensor B. The CP compression Gamma_Q=Q Gamma Q is TNI. The signed low-order approximation T factors id_L tensor C_signed and has endpoint support in Q. If ||Gamma-T||diamond<=delta (uniform on the promised module), define the physical positive repair

    C_good(theta)=Tr_L[Gamma_Q(I_L/d_L tensor theta)].

C_good is CP/TNI and differs from C_signed by <=delta, hence ||Gamma-id_L tensor C_good||diamond<=2delta (including Gamma-vs-compression bookkeeping, to verify). This is the same full-module positivity mechanism as the previous finite-gate theorem, now with energy-restoring blocks. No normalization is used. Independent sweep errors accumulate linearly even for arbitrary retained common B, since the good map acts id_L on all L/G/B/reference correlations.

Potential sharper route: use a truncated Stinespring amplitude (CP but not TNI), then contract its gauge factor. The map construction above is simpler if compression constants are checked.

## 6. Intended conclusion and unearned claims

If the proof closes, the hypothesis is established for a specified finite collision architecture: fixed beta, fixed local source/control/coherent-bath imperfections and fixed local strength/time ratios give exponential logical protection for exponentially many bounded-duration service rounds, after admitting a warm state and with paid encoded ports/gates. It is a powered correction service with a one-use thermal source, not a passive material.

It does not derive a fresh-source/renewal contract from marginal reset accuracy. It does not reduce geometry/body sizes or show a practical resource advantage. Finite collisions compile to matched active circuits, and selected CCZ operations alone are not universal. Those limitations must remain in the final ledger.
