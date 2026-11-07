# Thermal protected service from bounded local DATA descent

Joint constructive follow-up, 7 November 2026, Brisbane. This consolidates the principal's thermal-descent route, constructor's release/pulse/service proofs, auditor's canonical-projector/killing checks and positive repair, and machinery researcher's source/interface checks. Frozen independent initials remain unchanged.

The theorem is proved at explicit accepted DATA and physical-model premises. It defines a NEW DATA-only Hamiltonian and engineered local Davies-form Markovian cooling: no native controller clocks, history weights, proof pullback or forest access. Cooling and the same perturbation bath remain present during finite gates. No Gibbs state is supplied at entry. A thermal Markov reservoir is an explicit primitive, not a derivation from a finite exact bath. Quantum I/O uses the declared joint gateway contract; noisy bare ports retain their error floors. No elementary-qubit 3D implementation, universality from CNOT, or practical advantage is claimed.

## 1. Accepted DATA and fixed physical frame

Use the accepted N1388 CSS/Tanner DATA family, its actual local distance tables, BOTH sectors and common safe radius. For a fixed number of blocks, N means combined DATA size; rescale relative distance/radius constants accordingly.

The distance is d_N>=delta N. For EVERY valid syndrome sigma choose minimum same-syndrome X and Z representatives once, fixing ties, order and phases. Their product is E_sigma, with summed sector weight r(sigma) and wt(E_sigma)<=r(sigma). This minimizes over the same syndrome, not an unknown actual history/logical class; it is also stabilizer-minimal. Fix Enc and the full physical frame

    W(|psi>_L tensor |sigma>_G)=E_sigma Enc|psi>.

This is independent of input, noise, time and target gate. A q-supported Pauli has r(target)<=r(source)+c_r q; c_r=2 suffices for summed X/Z weight.

The ACTUAL integer commuting DATA energy is U=sum_v u_v, with <=c_U N nonnegative local raw-syndrome distance/unary terms, each <=u_*I and zero on the code. Read/changed-energy supports and incidence are fixed. Let D_E>=1 bound the sum of energy-term norms incident on one qubit. A w-supported operator on a codeword has output energy support U<=D_E w; a q-supported Pauli changes U by at most D_E q. This energy is not silently replaced by violated-check count.

Fixed h,kappa,r_dec>0 satisfy, for r(sigma)<r_dec N,

    U(sigma)>=h r(sigma).

At least kappa U(sigma) local hubs admit a bounded-support Pauli reducing U by an integer >=1. All possible updates/reverses lie in a finite bounded-incidence local catalog; sector updates preserve the opposite sector. Duplicate tagged Pauli labels may remain distinct charged reservoir channels.

These are accepted DATA inputs, not new code claims. N1388 compiler/interface pins are 0af0dc529eb96a359f9f5d0f9f00972ec90f1817dc2cb4753d95f196bd3f4f18 and 59c71b1c154457a0092b07610637eeb9a4f660c506f5277b43dbdd63d7b07155. The preserved whole reviews are copied under ../constructor/sources/ with hashes. They do not supply unlisted couplers, geometric embedding or a numerical threshold.

## 2. Exact Hamiltonian and thermal jump catalog

If R_v is the bounded set of commuting checks S_j read by u_v, set

    Pi_(R_v,sigma)=product_(j in R_v)(I+sigma_j S_j)/2,
    u_v=sum_sigma u_v(sigma)Pi_(R_v,sigma).

Invalid dependent-check strings have zero projector. The exact Walsh expansion is

    u_v=sum_(A subset R_v)uhat_v(A)product_(j in A)S_j,
    uhat_v(A)=2^(-|R_v|)sum_sigma
                        u_v(sigma)product_(j in A)sigma_j.

Define H_N=J U, J>0. Its coefficients are exact dyadic rationals times J. Each table has <=2^|R_v| Pauli terms, bounded support contained in its read-check union, and absolute coefficient sum <=J2^|R_v|u_*. Thus H has O(N) terms with possibly huge fixed locality/degree constants. Three-body or Euclidean locality does not follow.

For every Hermitian catalog Pauli P_a and every energy change d, define

    Pi_(a,d)=sum_(sigma:U(P_a sigma)-U(sigma)=d)Pi_sigma,
    A_(a,d)=P_a Pi_(a,d).

Only energy terms meeting supp(P_a) determine d. The spectral component has bounded FULL support: update plus affected check neighborhoods. It is not a global physical projector. There are <=M_0N update labels, |d|<=D, and <=MN positive-d components. Body sizes/incidences are fixed and table-computable. Moreover

    A_(a,d)^dagger=A_(a,-d),
    [H_N,A_(a,d)]=Jd A_(a,d).

Choose rates gamma<=r_a(-d)<=Gamma and

    r_a(d)=exp(-beta Jd)r_a(-d), d=1,...,D;
    0<=r_a(0)<=Gamma.

For example r_a(-d)=gamma, r_a(d)=gamma exp(-beta Jd) is simultaneous. Include only a bounded-incidence local diagonal Lamb shift. Let

    L_beta(rho)=-i[H_N+H_LS,rho]
         +sum_(a,d)r_a(d)D[A_(a,d)](rho),
    D[A](rho)=A rho A^dagger-(1/2){A^dagger A,rho}.

This is an exact local GKLS model at the declared reservoir primitive. Paired syndrome fluxes prove Gibbs stationarity; the diagonal Lamb shift commutes with it. No stationary input is presumed.

## 3. Same actual perturbation bath and physicality

Retain one bath B with its actual normal bath-only CPTP propagators T_B(t,s). Its self-Hamiltonian need not have bounded norm. During HOLD,

    L_t=L_beta tensor id_B+id_S tensor L_B(t)+sum_Z N_Z(t).

Each N_Z is normal HP, N_Z^*(I)=0, supported on <=q_noise DATA qubits and arbitrary B, with pointwise

    sup_i sum_(Z containing i)||N_Z^*(t)||_cb<=eta.

Bath-only terms belong to L_B. No fixed partner graph is required. Complete norms retain B and arbitrary inert references. The FULL interval evolution must be CPTP and the compression below well-defined CP/TNI. Finite bounded GKLS models supply this directly; unbounded baths retain actual integrability/normality/common-domain premises. Signed HP summands alone do not establish physicality.

## 4. Physical basin and full-module canonical neutrality

Choose strict fixed margins

    r_0<r_dec, 2r_0<delta, 0<u_c<h r_0/4.
    P=sum_(sigma:r(sigma)<r_0N,U(sigma)<u_cN)Pi_sigma.

P is a genuine physical projector, I_L tensor P_G in W. Confinement alone does not justify deleting its radius condition.

Let q bound the full system supports of nominal Hamiltonian/jump/loss legs and perturbations; set K_edge=D_Eq. On C=P1_(U<u_cN-K_edge), confinement gives r_source<=U/h<r_0N/4. A q-supported Pauli has target r<=r_source+c_rq<r_0N/2 and <r_decN for N>=N_0; its energy stays below u_cN. Hence every such leg A obeys A C=P A C. No radius-only exit occurs away from the energy boundary.

For retained source/target sigma,tau in P, E_tau^dagger A E_sigma has zero syndrome and Pauli weight <=2r_0N+q<d_N. Every coefficient is a stabilizer up to scalar. Consequently the compressed Hamiltonian, jump, complete-loss and arbitrary finite-system/bath legs are identity on L on the ENTIRE promised operator module, including syndrome coherences, bath coefficients, L-gauge correlations and references.

## 5. Exact drift, positive killing and nonstationary HOLD

Fix s>0 and V_s=exp(sU). Exact spectral action gives

    L_beta^*V_s=V_s sum_(a,d)r_a(d)(exp(sd)-1)Pi_(a,d).

Each active hub contributes a negative term of magnitude >=gamma(1-exp(-s)); discard additional negative terms by sign. Thus on P,

    L_beta^*V_s<=[-a U+b_th N]V_s,
    a=gamma kappa(1-exp(-s)),
    b_th=M Gamma exp(-beta J)(exp(sD)-1).

One improving move alone would not supply kappa U. For a q-supported N_Z split U into affected and unaffected commuting terms. The unaffected exponential is a bimodule factor. Affected energy lies in [0,D_Eq]; complete norm control and N_Z^*(I)=0 give

    +/-N_Z^*V_s<=C_s||N_Z^*||_cb V_s,
    C_s=exp(sD_Eq)-1.

Outside system qubits are references, with no bath-dimensional Kraus coefficient sum. Therefore

    L_t^*V_s<=[-a U+b N]V_s,
    b=b_th+C_s eta, nu_eq=s b/a.

Compress the FULL physical generator, K_t(rho)=P L_t(P rho P)P. For GKLS dynamics it has jumps PAP and positive extra loss PA^dagger(I-P)AP, hence CP/TNI propagation. Since P commutes V_s, deleting outgoing gains only decreases its positive-observable drift. This is not compression of an HP similarity transform.

For arbitrary positive subnormalized killed rho_P, possibly correlating L,G,B and R, put x=Tr V_s rho_P. Scalar spectral Jensen with mass <=1 gives Tr U V_s rho_P>=x log x/s. Consequently

    log x(t)<=nu_eq N+
                 [log x(0)-nu_eq N]exp(-at/s).           (5.1)

If x(0)<=exp(nu_0N+O(1)) and Delta_H=s u_c-max(nu_0,nu_eq)>0, the boundary mass is <=exp(sK_edge)exp(-Delta_H N+O(1)). The full/compressed difference vanishes on C rho_P C. Gentle compression bounds each residual by 4||L_Z^*||_cb sqrt(boundary mass). Nominal norms sum to O(N), perturbations to <=eta N; bath-only terms have no boundary difference.

A conservative per-cell norm budget is

    A_H=2Jc_Uu_*+2M_0(2D+1)(Gamma+Lambda_LS)+eta,

enlarged for the actual catalog. Duhamel with actual full CPTP propagation gives

    ||rho_full(t)-rho_P(t)||_1
      <=C_H N t exp(-Delta_H N/2+O(1)),                  (5.2)
    C_H=4A_H exp(sK_edge/2).

This holds uniformly with reference for every P-supported actual input satisfying the moment. Uniform writer moment bounds therefore give the corresponding complete channel guarantee.

By Section 4 the killed process is id_L tensor K_GB on the FULL promised module. Logical independence of the bath/gauge is unnecessary in THIS changed architecture. For arbitrary initial rho_LGBR, its initial LR marginal minus its killed final LR marginal is positive and has trace equal to lost mass: if R_GB=I-K_GB^*(I)>=0, that difference is Tr_GB[(I_LR tensor sqrt(R_GB))rho(I_LR tensor sqrt(R_GB))].

Thus (5.2), plus its survival deficit, gives half-trace logical error at most its right-hand side relative to the ACTUAL initial LR state. A uniform reference guarantee gives half-diamond preservation of the actual decoded writer channel. No Gibbs domination, logical/bath product approximation or writer dilation estimate is used. This stronger correlated-state conclusion is specific to the proved full-module thermal generator, not retroactively asserted for the older exact-bath theorem.

## 6. Explicit pre/post thresholds and thermal parameters

For two identical CSS blocks the physical bitwise CNOT is depth one and implements the fixed logical CNOT layer. Its support spread is B=2. The same proof applies to any separately supplied code-preserving bounded-depth gate with its ACTUAL partial/suffix spread B. Universal computation does not follow.

Put C_0=max(1,1/h) and choose fixed

    0<u_post<=min[u_c/4,
                 delta/(16(C_0+1/D_E)),
                 D_E r_0/(16c_r)],
    u_pre=u_post/(4D_E B C_0),
    alpha=u_post/(4D_E B q).                             (6.1)

Choose beta J and eta, after code constants, so

    b/a<=u_pre/4, equivalently nu_eq<=s u_pre/4.

For instance impose separately

    M Gamma exp(-beta J)(exp(sD)-1)<=a u_pre/8,
    C_s eta<=a u_pre/8.                                  (6.2)

These are explicit sufficient constant inequalities, not useful-temperature claims. If r<=floor(alpha N) pulse insertions occur, a pre-gate canonical representative has weight <=C_0 u_pre N. Its ideal-gate image and insertions have support

    w_post N<=B C_0 u_pre N+Bq r<=u_post N/(2D_E).         (6.3)

Output energy is <=u_post N/2 and canonical r<=c_r w_post N<r_0N. Confinement then bounds its fixed canonical correction weight by C_0 u_post N. Equation (6.1) makes w_post+C_0u_post<delta; the actual error and canonical correction differ only by a stabilizer. This verifies the SAME decoder convention at the completed gate.

## 7. Noisy release and the writer contract

The preferred general input assumption is only: the ACTUAL decoded writer channel has half-diamond error <=epsilon_in, and its actual joint DATA/bath output has an admitted P-supported positive subchannel with a uniform moment bound. Gauge/bath/L/reference correlations are allowed by Section 5. An actual physical quantum gateway must earn these two properties; a hypothetical ideal encoder does not.

A concrete supported-fault contract suffices. Let the physical writer have a positive instrument W=sum_F W_F with <=c_WN final fault locations. Its output fault legs have DATA support <=b_W|F| relative to codeword preparation; bath coefficients may be arbitrary. Require the reference-uniform intensity inequalities

    sum_(F containing A)W_F^*(I)<=p_W^|A| I               (7.1)

for every location subset A. A compatible verified quantum-I/O/gateway can supply an additional complete error epsilon_W. The writer's actual decoded accuracy epsilon_in includes its bare/protected input-port error; it need not be inferred from a joint product resource.

Choose

    zeta_W<min[r_0/(8c_r b_W),
               u_post/(4D_E b_W),
               delta/(8b_W(1+C_0D_E))].                 (7.2)

Every |F|<=m_W=floor(zeta_WN) branch is P-supported, has U<=u_postN/4, and is in the fixed correctable span. Its joint state can remain correlated with L and R. The discarded branch is CP and its complete mass obeys

    delta_W<=inf_(z>1)
      exp[c_WN log(1+p_W(z-1))-m_W log z].               (7.3)

To prove this, expand z^|F| as the product of 1+(z-1) times its fault indicator and use (7.1). The same expansion gives the UNNORMALIZED admitted moment

    x_W<=exp(nu_WN),
    nu_W=c_W log[1+p_W(exp(sD_Eb_W)-1)].                 (7.4)

For sufficiently small FIXED p_W>0, delta_W decays exponentially and nu_W<=s u_post. No conditioning-induced local-stochastic assumption is made. No proof state is normalized. The CP discarded writer branch costs delta_W, not its square root. An arbitrary coherent energy tail without a CP admitted-subchannel decomposition instead requires an explicitly proved tail treatment; plain gentle clipping would cost its square root. Exact P support needs no writer clipping at all.

This final-release contract must be proved by the actual noisy gateway, including idles, output spread and hardware exposure. The complete polynomial-depth bare encoder does not have bounded final cones merely because its ideal circuit exists. Actual quantum-I/O workspace, routing, reset, classical processing, timing and port floors are charged.

## 8. Finite-duration pulse with all cooling retained

Let the ideal control Hamiltonian generate the bounded-depth circuit in duration tau. Every partial/suffix circuit has spread <=B. The reference propagator is ideal system control times the ACTUAL bath-only CPTP evolution; no bath map is inverted.

Count ALL other physical terms during the pulse as disturbances: H_N, diagonal Lamb shift, full cooling jumps and anticommutators, actual perturbation bath, and control calibration/fault terms. Let their integrated complete-norm budget be <=mu N and their full system body <=q. A sufficient budget is

    mu=A_H tau+c_cal epsilon_cal+2c_loc p_gate,           (8.1)

where calibration denotes actual integrated local generator error. For the displayed discrete-fault term assume <=c_locN pulse locations have independent Bernoulli fault flags of rate <=p_gate, independent of input, bath and continuous-noise history; conditional faulty channels may act on the local DATA patch and the common bath. A faulty channel minus its ideal channel has complete norm <=2. More general correlated flags require an explicit reference-uniform all-subset joint intensity/fault-expansion bound, not merely marginal failure probabilities. All O(N) locations failing together with probability p_gate would not suffice. Enlarge q/B for actual control cones.

The joint time-ordered Duhamel/fault expansion has coefficientwise bounds

    Gamma_tau=sum_(r>=0)Gamma_r,
    ||Gamma_r||_diamond<=(mu N)^r/r!.

Bath-only maps have complete norm one and do not enlarge system support. Each insertion adds <=Bq support after ideal suffixes. These norms retain the actual common bath, not a reduced averaged channel. Discrete fault expansions combine coefficientwise with the continuous exponential bound.

For m=floor(alpha N), the signed high-order tail satisfies

    delta_g:=||Gamma_tau-sum_(r<=m)Gamma_r||_diamond
      <=(e mu/alpha)^(alpha N)/(1-mu/alpha).              (8.2)

Impose mu<=alpha/(8e). Then delta_g<=2exp(-alpha N log8). Allocate each of the three terms in (8.1) <=alpha/(24e), for example. All choices are independent of N and total runtime. Peak local control is O(d/tau), hence O(dA_H/alpha) at this sufficient point, with potentially huge fixed ratios. A fixed fractional calibration error proportional to pulse strength is NOT suppressed by reducing tau; it must satisfy (8.1).

The ideal partial gate path may leave P. Storage is not invoked during it: the entire intervening H/cooling/bath action is included in mu, and correctability is checked at the completed endpoint.

## 9. Positive same-environment gate map with error 2delta_g

Use the fixed input canonical module with U<=u_preN and output Q=P1_(U<=u_postN). The low-order signed map is

    Gamma_le_m=Ad_(U_L) tensor C_signed.                  (9.1)

C_signed need not be CP. This is FULL module factorization: for each input E_sigma Enc basis, every low-order system leg after the ideal suffix has support (6.3). For each Pauli coefficient P, E_eta^dagger P has zero syndrome and weight <d_N by (6.1). Thus

    W_out^dagger A_path G_phys W_pre=U_L tensor a_path.

It holds for all syndrome off-diagonals, arbitrary bath coefficients and L-G-B-R correlations. A one-state test would not establish (9.1).

Compress the ACTUAL CPTP channel and define on the ACTUAL gauge/bath algebra

    C_g(theta)=Tr_L[Q Gamma_tau(I_L/d_L tensor theta)Q].   (9.2)

This is CP/TNI and Q-supported. Applying these same complete contractions to (9.1) gives ||C_g-C_signed||_diamond<=delta_g. The direct triangle therefore gives

    ||Gamma_tau-Ad_(U_L) tensor C_g||_diamond<=2delta_g.   (9.3)

No gentle square root is needed for the pulse. C_g acts linearly on the SAME environment and is a valid complete comparison even for initially correlated logical/gauge/bath/reference states. Its trace deficit is <=delta_g. Optional CP completion to a fixed good state gives a CPTP surrogate at error <=3delta_g; it is only an analytical comparison on a charged branch, not a physical bath reset. The TNI version is preferred and never normalized.

## 10. Constant dwell and repeated-service theorem

Every positive post-gate state has trace <=1 and x(0)<=exp(su_postN). Choose

    tau_c=(s/a)log(4u_post/u_pre).                        (10.1)

By (5.1) and (6.2), after this dwell and all longer HOLD times, log x<=s u_preN/2. The pre-gate energy tail is <=exp(-s u_preN/2). A proof-only gauge filter to U<=u_preN is CP/TNI, commutes V_s, never increases its moment, and has joint trace-norm cost

    epsilon_pre=2exp(-s u_preN/4).                       (10.2)

This is not a physical recovery/reset. No proof state is normalized, so no normalization bias enters logical-gauge correlations.

The ACTUAL service is the noisy writer, a cooling/HOLD dwell >=tau_c, a finite CNOT burst with cooling still on, another dwell >=tau_c, and repetition, followed by the declared readout. Let G count bursts and T sum HOLD/dwell durations, excluding pulses/I/O. Total physical time also includes Gtau and actual gateway durations.

The good comparison composes only CP/TNI maps: admitted writer, killed dwells, gauge filters and (9.2). Every post-gate state has U<=u_postN and moment <=exp(su_postN) times its trace. All maps act on the SAME bath. Full-module factorization applies to arbitrary initial L-G-B-R correlations.

Set Delta_*=s(u_c-u_post)>0. Telescoping complete contractions gives

    E_service <=delta_W+2epsilon_W
       +C_H N T exp(-Delta_*N/2+O(1))
       +G[2exp(-s u_preN/4)+2delta_g].                  (10.3)

Here 2epsilon_W conservatively covers an optional full-joint writer model approximation and its decoded marginal; omit it for an exact positive instrument. An initially P-supported writer needs no delta_W. A CP discarded writer branch costs its mass, not its square root.

The final comparison is (Ad_(U_total) tensor C_total)(rho_initial), with C_total CP/TNI and rho_initial the ACTUAL admitted correlated writer state. Its LR marginal differs from Ad_(U_total) of the initial LR only by positive lost mass. For an exact positive writer instrument, adding removed writer branches preserves positivity of this deficit relative to the full actual writer marginal. Its trace is controlled by actual-versus-good error. Thus

    half-diamond logical error
      <=epsilon_in+E_service+epsilon_read,              (10.4)

where epsilon_in is ACTUAL immediate decoded writer error and epsilon_read is physical readout error/floor. Uniform reference/intensity/moment bounds make this a channel statement; the statewise statement needs no logical-independent bath.

With fixed physical constants, T and G may be exponential in N below the positive exponents in (10.3). Protected ports have their declared errors; fixed noisy bare ports retain O(p) floors. No physical decoding/reinitialization is inserted after short HOLD intervals.

## 11. Quantum ports and promised decoding

For k bare unknown inputs a permitted dephasing fault before redundancy gives the sharp floor >=1-(1-p)^k; a final bare noisy output also has a fixed floor. The gateway must declare protected ports or retain these floors.

A verified compatible quantum-I/O model may provide reference-entangled inputs, supported noisy output, actual auxiliary channels, protected classical processing or encoded classical packets, and charged conversion/routing/reset/timing. A reduced-system writer estimate may certify epsilon_in, but ACTUAL energy support/moment must still be proved. No inaccessible resource is substituted. Known-state preparation alone is not unknown-state quantum I/O.

Promised-efficient recovery scans O(N) local hubs, applies an active decreasing move and repeats. Integer U falls each time; density supplies a move while U>0. The basin source/target argument prevents radius exit, and each move is canonically neutral. At most O(N) accepted moves and O(N^2) table evaluations suffice, with a fixed cap/arbitrary output outside the promise; finish by the Clifford code decoder. Its physical FT gateway implementation and all costs/noise are charged.

Readout input faults use a final low-energy proof filter and a strict support margin for canonical error plus gateway faults. Complete-span correctability handles correlations. The physical gateway must verify this robustness; an ideal decoder appended to (10.3) is not a noisy-device claim.

## 12. Resources, work and net heat

The literal model uses O(N) DATA cells, exact local-table Pauli couplers, O(N) full-support cooling channels and O(N) physical control gates per fixed-depth burst. Local dimensions, support sizes, rate/control ratios and required low-temperature constants can be enormous. Dwell time (10.1), pulse duration and peak local strength are fixed independently of N,T,G. Charge O(NG) control locations, O(NT) cooling-interaction opportunities, actual calibration/selection/timing hardware, and the supplied quantum gateway's full workspace, routing, reset and duration. Bounded degree does not prove a bounded-density Euclidean layout.

O(NT) interaction opportunities are NOT O(NT) net heat. In unforced HOLD with time-independent bounded H_N and only its nominal cooling, net energy into the system is

    Q_into_system=Tr H_N rho(T)-Tr H_N rho(0)=O(N).

Equilibrium can have O(NT) gross jump/energy-exchange events but zero mean net heat flow. With additional noise/driving baths, a cooling reservoir may remove sustained energy supplied by another source. System-level accounting reads Delta E=Q_cooling+Q_other+W_control. During fixed-H unforced HOLD, TOTAL signed net system-energy exchange remains O(N). A cooling current of order eta NT requires compensating input; it does not follow from counting generator terms. Arbitrary HP perturbations do not alone define a unique thermodynamic heat/work split.

Gate controls can perform work. For a specified smooth cyclic control Hamiltonian, work is integral Tr rho(t) times its explicit time derivative; its variation bound may scale O(NG) times fixed pulse-strength constants. Microscopic refrigerator efficiency, fuel and drive energy are not supplied. The engineered Markov reservoir is an explicit resource, not a free exact interacting Gibbs state.

An active comparator gets the SAME fast controls, cooling/reset, routing, calibration, classical hardware and quantum ports. For exponential T it can use O(log N) concatenation levels and polynomial resources, or stronger qLDPC schemes at their hypotheses. No favorable full-cycle space, work, net heat, threshold or practical comparison is proved.

## 13. Separate audited two-sector non-Clifford corollary

This corollary uses the exact stable-duality construction in ../machinery/dual_sector_local_energy_v1.md and its algebra audit ../challenges/auditor_stable_duality.md. It does not alter the Tanner theorem or claim raw transpose-syndrome descent.

For a compatible fixed-dimensional GJ cosheaf F, its anchored double complex has exact horizontal and vertical local normal forms. The finite filtered perturbation inverses are polynomials; the basis change and inverse have bounded row/column incidence and spread. With the CORRECT product ancillas inherited from those normal forms, an exact Clifford C=P_linear H_all maps original Q_k(F) to Q_(t-k)(K) plus target product ancillas. Temporary work used to realize this Clifford is not part of its abstract pulled-back memory operators.

In the ORIGINAL DATA coordinates define

    U_F=F cochain Z-syndrome BLOCK energy
                    +original Z-ancilla defects,
    U_K=C^dagger[K cochain Z-syndrome BLOCK energy
                    +target Z-ancilla defects]C,
    U=U_F+U_K.

Use Li's physical X/Z convention: GJ labels delta^k as H_X, whereas Li labels it H_Z. The abstract GJ imports are X/Z-swapped when necessary; the actual Li cubic DATA gate is not replaced by a Hadamard-conjugated gate.

U_F is purely original Z-stabilizer functions and U_K purely original X-stabilizer functions. They commute and enforce the COMPLETE original stabilizer group plus the fixed product ancillas. The ground code is exactly original DATA code tensor those ancillas, with no auxiliary logical modes. Absolute distance is unchanged; constant-factor memory enlargement preserves positive relative distance.

An F X-correction lowers U_F and commutes U_K. A K X-correction pulls back to original Z, lowers U_K and commutes U_F. The audited active-vertex refinement applies in syndrome degrees k+1 and t-k+1, both below t for 2<=k<=t-2. Along with product-ancilla corrections it yields >=min(kappa_F,kappa_K)U active bounded-support labels at low linear energy. No weighting is needed: the actual cross-energy change is ZERO.

Greedily repair F then K. Neither energy rises and at most initial U bounded-support moves suffice. If each move has support <=L, every sufficiently low-energy valid syndrome has a physical Pauli correction of weight <=L U into the EXACT common ground code. Thus the canonical correction bound is GLOBAL at low energy, not merely confinement within a promised radius. This earns an energy-only P at a small cutoff: choose it so two canonical corrections plus a local leg remain below distance. Sections 2-10 apply with C_0>=L and no radius filter.

For the exact Li three degree-two sheaves (k=2,t=6), use the simultaneous primal/actual-dual product-expansion hypotheses checked in the machinery import. Retain the original bounded-incidence cubic DATA circuit and extend it by identity on added memory ancillas. Its bounded-overlap hyperedges are colorable in fixed depth. Omit the optional repetition step: it is unnecessary for bounded-depth service and would require a new energy transfer.

The original code-preserving non-Clifford logical operation therefore obeys the SAME finite-pulse/cooling theorem and error bound. No physical duality circuit is performed during a pulse. Global low-energy repair also makes correlated writer admission more direct. Precisely, Li equations (3.226)-(3.227) identify the selected CCZ product on selected binary 1-components when the other binary components and complementary logical coordinates are initialized to zero. The physical U_xiS preserves the FULL code, so the generic service theorem applies to its full logical unitary; the literal selected-port CCZ claim retains that zero-initialization premise. The address/program choice needs a protected local control contract; one unprotected global bit cannot set O(N) strong gates reliably for free. No addressed Hadamard, full universal gate set, practical geometry, exact microscopic bath or advantage follows.

For clarity, the energy-only specialization replaces Section 4 by P=1_(U<u_cN), with C_0>=L and u_c<min(u_descent,delta/(8C_0)). Local energy changes are bounded by K_edge. Canonical representatives have weight <=C_0U; retained local edges have total weight <=2C_0u_cN+q<d_N. In (6.1) delete the r_0 term, retain the other two bounds, and delete the radius term in (7.2). All drift, boundary, pulse, positivity and TNI induction proofs are then literally the same. This is a separate changed Hamiltonian/product-ancilla instantiation, not a claim about raw transpose energy.

## 14. Primary sources, predecessors and remaining physical scope

Hong–Guo–Lucas, arXiv:2403.10599v3, Sections 3-4 and Appendices B/E, already gives thermal qLDPC memory and finite-depth measurement-free Gibbs-sampling/rate modifications. These are substantive predecessors, not renamed discoveries. https://arxiv.org/html/2403.10599v3

Balasubramanian–Davydova–Lin, arXiv:2605.10943v1, Theorems 3.16,5.13/Corollary 5.14, gives 3D thermal memory with thermal encoding; initialization is separate. https://arxiv.org/html/2605.10943v1

Duennweber–Styliaris–Trivedi, arXiv:2601.20818v3, formal Theorem 1, already gives discrete-time 2D autonomous universal computation under its local fault-path model. Its continuous-time extension is explicitly an outline. https://arxiv.org/html/2601.20818v3

Zhao–Yuan–Han–Liu, arXiv:2609.39965v3 Theorem 1, distinguishes local-stochastic residuals under soundness from logical success after ideal recovery under confinement. Its known-state preparation is not unknown-input quantum I/O. https://arxiv.org/html/2609.39965v3

Christandl–Fawzi–Goswami, arXiv:2408.05260v3 Theorem 43/Lemmas 41-42, is the verified quantum-I/O predecessor for compatible stochastic gateway models. Its actual auxiliary/noise/port premises and full overhead must be retained; no generic retained-bath gateway theorem is imported merely from its title. https://arxiv.org/html/2408.05260v3

Cubitt–Montanaro–Piddock, DOI10.1073/pnas.1804949115, full arXiv:1701.05182v4 Proposition29/Section8.5/Theorem32, has time error 2epsilon t+4eta and leakage/local-encoding premises. Approximate simulation cannot provide lifetime-scale fixed hardware accuracy for free. https://arxiv.org/html/1701.05182v4

Gay–Granha Jeronimo, arXiv:2609.20780v1, Sections6-8, supplies the actual local cochain/descent/anchored-array ingredients for the audited new stable-duality energy. Li–Li–Han–Liu, arXiv:2609.26691v3 equations(3.20),(3.31)-(3.33), Proposition3.3/Section3.4 and equations(3.223)-(3.227), supplies the actual three degree-two code and cubic DATA gate inputs. The stable-normal-form/energy synthesis is explicitly derived and audited in the linked research notes; the optional repetition reduction is omitted. https://arxiv.org/html/2609.20780v1 ; https://arxiv.org/html/2609.26691v3

The exact-H consumer's inverse-rarity ideal-access storage and Bell/channel criterion remain distinct prior capital. N1694's three-body all-number clock Hamiltonian and specified microscopic correlated thermal start remain a DIFFERENT contract; their noisy loading and actual-bath preparation are not closed by this change of architecture.

PROVED at stated accepted DATA/code, reservoir, actual physicality, joint-noise and gateway premises: exact finite-table Hamiltonian, thermal local descent drift, nonstationary correlated-state warm protection, supported noisy release, finite same-environment code-preserving gates with 2delta positive repair, and repeated gate/cooling service. The audited two-sector energy supplies the separate compatible non-Clifford specialization.

Not supplied: useful numerical thresholds, literal three-body/3D hardware, microscopic finite-bath derivation, arbitrarily accurate noisy bare ports, universal gates beyond supplied compatible operations, historical priority, experimental validation, or favorable complete-resource comparison.
