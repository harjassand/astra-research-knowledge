# Ancilla-free binary receiver from acquired qubit flags
29 October 2026. Author derivation; independent review pending. No novelty claim.

## Dependency and scope
Governing dependency: `../compact_quantum_flag_recovery_20261028/COMPACT_QUANTUM_FLAG_RECOVERY_v1.md`, especially Sections 1–6 and 7, with its received independent review. Use its actual Bell-label/flag acquisition, not an environmental-model oracle. Let sigma_x be positive 2x2 Bell blocks with sum tr(sigma_x)=1 and let F* be optimal complete flag-POVM discrimination success. This equals full-CPTP recovery fidelity for the Pauli-plus-flag source ONLY; for coherent sources it is the measure-flag/conditional-Pauli class optimum. Stationary independent complete calls and trusted acquisition are inherited; arbitrary retained memory is not covered here. The whole logical payload has n qubits.

## 1. Binary hardware and known-coefficient optimum
For labels a,b, define Delta=sigma_a-sigma_b and P=1_(Delta>0). Effects (P,I-P) maximize the binary objective and give

 B_ab = [p_a+p_b+||Delta||_1]/2.

Proof: objective=p_b+tr(P Delta); maximizing over 0<=P<=I retains exactly the positive eigenspaces. This is standard Helstrom discrimination of subnormalized states. A zero eigenvalue can be assigned arbitrarily. For qubit flags, a rank-one P needs one known single-qubit basis rotation and computational readout; P=I or 0 is a constant correction and requires no flag measurement. Each outcome selects one of two actual n-qubit Pauli words (at most n local nonidentity gates). There is no Naimark ancilla. A general complex Bloch direction requires an arbitrary one-qubit unitary, not necessarily a single native-axis pulse. Flag preparation/access, readout, feedforward latency and all data Pauli controls remain physical costs. If implementation perturbs the final recovered channel by diamond norm <=epsilon_impl, the conservative fidelity loss <=epsilon_impl is valid. Sharper half-diamond conventions must be stated separately.

## 2. Top-prior pair and its sharp obstruction
Let a,b have the two largest priors and t=1-p_a-p_b. Complete the corresponding two effects of any full POVM by assigning all omitted effects to either retained label. Positivity makes the retained success at least F* minus the omitted success, which is at most t. Hence

 B_ab >= F* - t >= 2F* - 1.

The second inequality uses the received top-two-prior ceiling F*<=p_a+p_b. This top-prior bound is asymptotically sharp: for epsilon>0, eta>0 sufficiently small, take priors (1-2epsilon-eta, epsilon+eta, epsilon), flags (|0>,|0>,|1>). The unique two leading priors yield B=1-2epsilon-eta, while F*=1-epsilon-eta. Thus B-(2F*-1)=eta can approach zero. The obstruction is choosing labels by prior rather than useful flag distinction, not necessarily needing a generalized measurement.

If empirical counts satisfy max_x |phat_x-p_x|<=gamma, choosing their leading pair loses at most 4gamma in retained true mass. For a fixed selected pair, the uniform matrix event max_x ||Shat_x-sigma_x||op<=delta implies plug-in binary regret <=4delta (Section 3). Consequently the count-selected plug-in receiver obeys

 F_learned >= 2F* - 1 - 4gamma - 4delta - epsilon_impl.

All ties use a fixed deterministic rule. Uniform events cover data selection; no rare-label normalization occurs.

## 3. State-aware pair search removes the count penalty
Let S be observed labels, with raw Hermitian coefficients Shat_x from the received acquisition; all unseen coefficients are exactly zero. Add one actual unseen label z if any exists. Search every unordered pair of distinct labels in T=S union {z}, and every constant receiver, by the analytic formula in Section 1, applied to Shat. Pick the greatest empirical score. Neither positivity of Shat nor normalization is needed. Two distinct unseen labels both have zero coefficient, so their empirical binary score is zero, already achievable by the constant dummy. A pair with one unseen label is represented by z. Thus this is the exact empirical optimum over the complete binary receiver class, despite the exponential underlying alphabet.

Each candidate is a complete qubit POVM (with all other effects zero). On the uniform event,

 |score_hat(M)-score(M)| <= delta sum_x tr(M_x) = 2delta.

Let B* be the true best binary receiver score. Empirical optimization, or optimization within certified additive eta_alg, therefore gives

 F_learned >= B* - 4delta - eta_alg - epsilon_impl
           >= 2F* - 1 - 4delta - eta_alg - epsilon_impl.

The first inequality is often much stronger. The same uniform-event argument applies simultaneously to pair selection and measurement construction. If the known matrix calculation is approximate, certify the empirical optimizer error; ideal real arithmetic is not a paid implementation. There are O(|T|^2) constant-size eigenvalue problems, O(|T|) coefficient storage and O(n|T|) label bits, with |T|<=N+1. This is polynomial in acquired sample count and logical block length. It is not claimed to be the fastest pair search. For the displayed general acquisition the inherited sample bound remains O(epsilon^-2[n+log(1/beta)]) at fixed flag dimension, with its explicit constants; no extra source calls are required.

## 4. Data-dependent full-oracle certificate without a general SDP
For an exactly evaluated selected pair A=Shat_a, B=Shat_b set

 Y=(A+B+|A-B|)/2,
 s=max(0, max_(x in T) lambda_max(Shat_x-Y)).

Y>=A,B and tr(Y) equals this pair's empirical Helstrom optimum. Y+sI dominates every known coefficient, including the zero unseen dummy, and is therefore a feasible dual for the full empirical discrimination problem. Its objective exceeds the selected pair's by exactly 2s. Thus, with exact candidate implementation,

 F* - F_learned <= 4delta + 2s + epsilon_impl.

This holds for ANY selected pair, not just the best one. With approximate calculation, use certified primal value l and certified feasible dual U instead: regret <=4delta+[tr(U)-l]+epsilon_impl. Interval-enclosed square roots and rational PSD minor checks can provide such a certificate, as already done in the received compact pilot. This note does not supply a new arbitrary-precision compiler or recertify the prior pilot. Floating-point s from the accompanying program is diagnostic only.

Consequently a useful automatic workflow is binary search, then dual-gap certificate; only if the certified gap matters should the general <=4-outcome qubit POVM optimizer be invoked. The final hardware still has two outcomes if its certificate is adequate. This is an explicit cost/fidelity choice, not a separation from strong conventional adaptive discrimination.

## 5. Limits and conventional alternatives
The best binary receiver need not attain F*. Equal-prior pure trine flags give F*=2/3 whereas B*=(2+sqrt(3))/6, strictly smaller. Equal-prior tetrahedral flags give F*=1/2 and B*=(1+sqrt(2/3))/4. Thus the exact full-oracle four-outcome result is not replaced universally. No sharp universal function B*(F*) beyond the inherited 2F*-1 lower bound is claimed here. The sharp example in Section 2 applies to top-prior selection, not to state-aware best-pair selection (which solves that example exactly).

An equally informed conventional learner can use exactly these Helstrom formulas, pair enumeration, matrix concentration and dual checks. This is a hardware simplification and auditable selection rule inside the accepted flag architecture, not a new state-discrimination principle, asymptotic quantum speedup, new channel capacity, hardware experiment, or general unknown-noise solution. It does not acquire a helpful flag port, discover a useful coherent encoder, remove Bell references, or solve inter-call memory. It preserves the earlier source and comparator boundaries.

## 6. Strictly nonbinary optima arbitrarily near fidelity one
A further exact boundary strengthens the low-fidelity trine/tetrahedron warnings. Fix 0<q<1/4 and 0<c<1. Put P0=1-2q, s0=sqrt(1-c^2), and use three labels with

 sigma_0=P0 (I+Z)/2,
 sigma_+=q (I+s0 X-c Z)/2,
 sigma_-=q (I-s0 X-c Z)/2.

Define

 z=P0(P0-q)/[2P0-q(1-c)], y=P0-z,
 R=y-q/2, u_z=-(z+qc/2)/R,
 u_+=(q s0/(2R),0,u_z), u_-=(-q s0/(2R),0,u_z).

The defining quadratic identity R^2=(q s0/2)^2+(z+qc/2)^2 makes u_± unit Bloch vectors. Here z>0, R>0 and -1<u_z<0. The dual Y=yI+zZ obeys Y>=sigma_i for all three labels. For sigma_0 its kernel is |0>; for sigma_± the kernels are the pure states E_±=(I+u_±·sigma)/2. The effects

 M_0=[-2u_z/(1-u_z)] |0><0|,
 M_+=[1/(1-u_z)] E_+,
 M_-=[1/(1-u_z)] E_-

are positive and sum to I. Complementary slackness therefore proves exactly

 F*=tr(Y)=2P0(P0+qc)/[2P0-q(1-c)].

All three effects are necessary for any optimum: each effect must be supported on its respective one-dimensional dual kernel; the three kernel projectors are linearly independent in the real span of I,X,Z, and completeness uniquely fixes the three strictly positive coefficients above. Thus NO binary correction receiver reaches F*, even as q→0 and F*→1.

For q<1/4, the best binary pair consists of label 0 and either rare label: its score is at least P0>2q, whereas the rare/rare pair scores at most 2q. Its exact value is

 B*=[P0+q+sqrt(P0^2+2P0 q c+q^2)]/2 < F*.

For example q=.02,c=.5 gives F*=.9750785340314135 and B*=.9750773134253960. This is a small but strictly positive optimum gap, not a practically significant advantage claim. The family rules out any universal assertion that sufficiently high fidelity makes the exact optimal receiver projective. It does not preclude stronger approximate universal bounds than Section 3.

### Primary-source provenance for Section 6
The three-state family is the established mirror-symmetric discrimination family of E. Andersson, S. M. Barnett, C. R. Gilson and K. Hunter, *Minimum-error discrimination between three mirror-symmetric states*, Physical Review A 65, 052308 (2002), DOI https://doi.org/10.1103/PhysRevA.65.052308 ; arXiv https://arxiv.org/abs/quant-ph/0201074 . Governing author manuscript inspected 29 October 2026: https://strathprints.strath.ac.uk/2857/5/Andersson_etal_PRA_2002_Minimum_error_discrimination_between_three_mirror_symmetric_states.pdf . Equations (5)–(7), (11)–(14), pp.1–2 provide the ensemble and optimal regimes. Set their p=q and cos(2theta)=-c; their Eq.(14) becomes the F* formula above. Section 6 is an independently derived recovery-boundary application of that conventional result, not a new discrimination solution. Binary optimality conditions are standard Helstrom theory, also credited in that paper (reference 1); the trace-positive-part proof is supplied here so the present bounds need no uninspected external proof.
