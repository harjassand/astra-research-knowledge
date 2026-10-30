# Independent whole review: one asynchronous transversal logical CNOT
2026-10-30. Reviewer: audit_topology_free_noise. This is a mathematical proof/interface audit, not numerical evidence for a physical threshold or a novelty assessment.

## 0. Finding and exact scope
**PASS for the composed one-layer encoded-gate theorem at the final frozen sources identified in SOURCE_SHA256.txt**, conditional on the same reviewed code/confinement/active-density/canonical-edge and actual native-controller hypotheses as the accepted native memory theorem. The simultaneous-moment/common-basin argument is reviewed below, not assumed as an additional oracle.

The earned bound is

    ||Out_u - Ad_(U_L)||_diamond
       <= min{2, C N^(3/2)(1+u) exp(-b ell)},    u>=tau, N>=N0,

with fixed positive constants, one fixed finite latency tau, and one fixed positive joint local-noise budget. It becomes exponential in N only when the imported cutoff ell is at least c_*N. The output is the specified fixed TARGET forest inverse and ideal target-code decoder. All initialization and regularity/noise restrictions of native memory are retained.

The actual hardware has colocated paired resource columns with the stated joint DATA_A/DATA_B/program capability; arbitrary local operators on these fixed-dimensional columns are not elementary two-qubit gates. A fixed support family, declared before proof geometry, is retained. This does not import the topology-free corollary, unbounded bath couplings, noisy retrieval, an unchanged externally prescribed decoder, remote LOCC, reusable gate sequencing, non-Clifford universality, or a live-controller handoff.

A substantive initial defect was repaired: a footprint defined merely by which occupations fail to commute with the EXACT dressed missing unitary does not cover its separate Pauli coefficients. The frozen construction now uses the entire structural footprint, including every intersecting unary-energy projector and complete history-token bundle. The initial and repaired bytes are preserved in reviewed_sources/.

## 1. Physical instance and joint product-code convention
Let U_i be the actual onsite CNOT on the two DATA factors of paired column i. The physical program register has states 0,e,1 and finite positive Omega,kappa. In the reference program frame,

    H_i=Omega(|e><0|+|0><e|),  J_i=sqrt(kappa)|1><e|.

With G_i=P0+U_i(Pe+P1), the declared physical generator is exactly

    Ad_G (L_mem,A+L_mem,B+sum_i L_prog,i) Ad_(G dagger).

Every nominal memory term must be conjugated; adding only the gate drive to unchanged memory would not prove this theorem. The actual program Hamiltonian becomes Omega(U_i|e><0|+U_i dagger|0><e|). Its e->1 reset is DATA identity because both endpoints have the same U_i gauge. The transformation is onsite in the NEW paired-column hardware, so hub/column terms remain two-site and onsite resets remain onsite. There is no elimination, simulated-channel approximation or error growing from a finite-time effective-generator replacement.

Both blocks comprise one logical/reference channel. In particular a physical perturbation touching both DATA halves is not treated as coupling to a fixed state of the other logical block. For each of the four CSS-sector observables take the restriction of every declared local support to that sector's block, enlarge the bounded geometry as required, and use common worst-case constants. Equivalently, the product-code local edge is checked in each sector. Expand DATA operators on BOTH blocks when invoking canonical logical factorization. All remaining coefficients are genuinely auxiliary controller/program/bath operators. Joint correlated logical inputs and references are retained throughout.

Onsite G conjugation preserves joint cb norms and physical column support. The accepted bounded-depth native forest transformation only enlarges structural cones/incidence by fixed constants. Program registers remain physical column factors counted in the SAME support/incidence model for both estimates; they are never absorbed into an unconstrained bath. Actual program noise, including coherent 1-to-0 reinfection, remains in the sustained perturbation budget. The physical normalization assumptions are not weakened to state-average strengths.

## 2. Actual coherent clocks: independent derivation
On the active 0/e corner the killed adjoint is K*R=i[H,R]-(kappa/2){Pe,R}. Direct multiplication gives

    R=[[2/kappa+kappa/(4 Omega^2), -i/(2 Omega)],
       [i/(2 Omega),              2/kappa]],
    K*R=-I_active,
    det R=4/kappa^2+1/(4 Omega^2)>0.

Extend R by zero on 1. Writing A=R/||R||, a=lambda_min(R)/||R|| and r=1/||R|| gives aB<=A<=B and L_prog*A=-rB<=-rA, where B=P0+Pe. This retains the actual 0/e coherences. No dephasing approximation or classical jump-clock assumption is used.

For S a selected set of clocks set M_S=product A_i. Nominal memory and bath-only maps annihilate it; the program generator supplies -r|S|M_S. For a local joint Hermiticity-preserving perturbation N_Z* annihilating identity, put K=S intersect program_support(Z). If K is empty its action vanishes. Otherwise bimodularity outside the physical program support and the local norm bound give

    N_Z*M_S <= ||N_Z*||cb M_(S minus K).

The same bath may appear in every term: the untouched clock factors still commute its operators. This is a full-joint operator inequality, not a reduced Markov approximation. With at most q affected clocks per term and per-clock summed norm at most eta, induction over |S| closes against p(t)^|S|, where

    p'=-r p+eta p^(1-q), p(0)=1,
    p(t)^q=e^(-qr t)+(eta/r)(1-e^(-qr t)).

For eta<r, 0<p<=1; |K|<=q gives p^(|S|-|K|)<=p^(|S|-q), including |S|<q. The smaller-set induction is legitimate because K is nonempty. Initial moments are at most one for EVERY joint initial state. Finally product B_i<=a^(-|S|)M_S, so unfinished-set inclusion is at most (p/a)^|S|. Missing gates use label 0 only, whereas 0/e is a conservative unfinished set.

Choosing a desired tail p_tail, then fixed tau and eta sufficiently small, gives the same p_tail^|S| bound for all u>=tau. The clocks need not all finish; a constant small unfinished density may leave extensively many unfinished columns. There is no factor exp(eta u) growing with the total storage/gate time.

The root's alternative backward-test proof is also valid. Its factors lie between vI and I, v>0, so local factor ratios give N*M_s<=C(v,q)eta|S|M_s. The test solves the nominal backward equation. Starting anew on the last fixed tau interval yields a uniform late-time bound, with no independence or product-state assumption.

## 3. The same clock hierarchy after analytic killing
Let P be the memory basin in program-frame coordinates. It can be conjugated by the native forest without changing any program test. Since P acts only on native memory degrees of freedom, [P,M_S]=0.

For the full physical generator and its complete-loss compression,

    L_P*(P M_S P)=P L*(P M_S P)P <= P L*(M_S)P.

Indeed M_S-PM_SP=Q M_S Q is positive, and conditional positivity gives P L*(Q M_S Q)P>=0. In a GKLS representation these are exactly outgoing positive gain terms; Hamiltonian and loss contributions to this difference vanish. This comparison concerns the FULL physical generator. It is not a claim that every signed perturbation summand remains a generator after killing or that killed noise annihilates identity.

The positive killed state is subnormalized, with zeroth moment <=1. The identical hierarchy/induction therefore holds for it. One must not renormalize on survival or assume that the killed evolution is dominated by the unmeasured evolution in CP order. Neither is used here. Well-defined normal joint interval propagators and CP trace-nonincreasing compression remain hypotheses in the possible infinite-bath setting.

## 4. Earning two raw moments on one apparatus
The new simultaneous-moment addendum correctly uses the open parameter region of the native proof. Let theta=e^(-L). Choose interior fractions c_low<c_hi<c_top<1 obeying all per-move, sparse-animal, component and bad-token margins. Set a_low=c_low L, a_hi=c_hi L. Then

    sum_A f_(a_hi,theta)(A)^2 = V_(2a_hi,theta^2).

The strong test has log temperature 2L and fractional exponent c_hi, not 2c_hi. Thus it lies in the same admissible open interval. The difference 2(c_hi-c_low)L can exceed the rooted-animal entropy by an arbitrary fixed margin.

The proof-credit lower comparison loses a fixed per-animal exponent from the dirty no-jump coefficients and a bounded small exponent from useful interpolation. These losses are independent of L once the actual finite dirty matrices and common coefficients are fixed. Choose internal proof exponents above a_low and 2a_hi by the required fixed losses, and upper comparison exponents below c_top L and 2c_top L respectively. Increasing L makes both choices possible without taking c_top to one. Vacuum summability holds for both upper raw bounds.

The physical orbit-minimizer corrections, gate list, native resets/monitors and controller resolvents do not depend on the animal exponent. As in accepted native V1, fresh bad coefficients are chosen before zeta; the actual isolated matrices and activity witnesses are recomputed for this fixed physical instance. Token multiplicity and structural geometry are common. The finite collection of strict weighted inequalities is satisfied by taking worst-case constants, then choosing proof scale constants, ONE physical epsilon below both allowed bounds and ONE positive joint-noise budget below both margins. No limiting family or infimum over all exponents is involved. No old dirty resolvent is transplanted to a different physical reset instance.

This proves existence of an apparatus selected for both tests. It does not assert that arbitrary already-fixed native rates automatically earn every stronger moment.

## 5. One common low-potential basin, not two postselections
Take P to be component safety in the four sectors intersected with the lower raw potential sublevel V_low<M. Choose N>=N0 so the encoded/ready state lies in it. The pre-pullback drift for either weight holds on the component-safe region; its proof does not require a sublevel of that weight's own dressed observable.

Each positive proof circuit preserves THIS P branchwise. Its Kraus components either preserve raw DATA syndrome/history labels, erase a flag without DATA action, or implement the same accepted deterministic local correction with a good-controller virtual reset. The last action decreases V_low by the all-animal completion theorem, independent of which test chose its coefficient. The lower-potential local edge barrier then preserves minimum-representative component safety. Erasure cannot increase V_low; controller-only no-jump coefficients preserve the labels. Activity factors commute P.

This is stronger than expectation monotonicity and is exactly what restricted-order positive pullback needs: if rho is P-supported, T_j,*rho remains P-supported. Both final F_j separately preserve the raw-syndrome/history block algebra, so [F_j,P]=0. That commutation is not inferred merely from basin invariance.

The SAME actual killed state rho_P(u), not two differently conditioned processes, consequently satisfies

    d Tr(F_j rho_P)/du <= -lambda_j Tr(F_j rho_P)+b_j N Tr rho_P,
    Tr(F_j rho_P(u)) <= C_j N.

The strong proof's lower comparison is chosen to dominate V_(2a_hi,theta^2), giving the needed sum of squared RAW summands. This does not square F_j, square its expectation, or demand independence of the two tests. Program generators act trivially on F_j and P; coupled program/common-bath noise is already in the local joint-norm estimate.

## 6. Structural suffix envelope and the repaired defect
In program-plus-native-forest coordinates, the physical state is G F sigma F dagger G dagger. For the fixed target forest F_*=U_* F U_* dagger,

    F_* dagger G F = U_* E,
    E=F dagger(U_* dagger G)F.

For basis program label z, E_z is the product of E_i=F dagger U_i dagger F over z_i=0. These dressed factors commute since their bare onsite gates commute, and bounded-depth F gives each a fixed structural support C_i. Their support includes native controllers/workspace and is not just the bare DATA column.

Choose Gamma_i to contain ALL raw occupation projectors whose physical supports intersect C_i, with full analytical copies of any affected history flag. Then every DATA-Pauli times auxiliary coefficient in a local expansion of E_i commutes all occupations outside Gamma_i. The set sizes and vertex incidences are bounded independently of N. Repeated flag tokens are fully correlated projectors, not independently noisy ancillas.

The original commutator-only footprint criterion was insufficient. For example SWAP commutes two-qubit total excitation, but its XX and YY Pauli summands separately connect |00> and |11>. Cancellation of exact-unitary transitions does not eliminate paths in a Pauli expansion. The frozen structural criterion repairs this and is explicitly regression-tested.

For H the conservative unfinished set, let Gamma(H)=union Gamma_i and

    V_env=sum_A f_low(A) theta^(-|A intersect Gamma(H)|).

For a fixed source raw-label sector, every nonzero component of every coefficient path agrees outside Gamma(H). Arbitrary Boolean changes inside are paid by the displayed factor. Thus the same envelope bounds the raw potential of every prefix and every Pauli coefficient path. This is a support/sector statement, not a norm bound for an unnormalized coefficient. One never sums norms over exponentially many Pauli paths.

Independently, splitting f_A into unaffected factors and affected factors between theta^m I and I proves E_H dagger f_A E_H<=theta^(-m)f_A. The unitary expectation bound is valid, but alone would not have supplied the missing coefficient-path closure; the structural argument is load-bearing.

## 7. Correlated envelope expectation pays all animals
The moment input is the unnormalized inclusion inequality Tr(rho_P product_(i in S) B_i)<=p_tail^|S|. Neither memory nor program independence is assumed. If each Gamma_i has size at most k and each vertex has at most d incident clocks, assigning a covering unfinished clock to each selected vertex gives

    Pr(S subset Gamma(H)) <= d^|S| p_tail^(|S|/k).

Equivalently, the component manuscript expands a product over incident clocks and obtains the useful direct bound

    Tr rho_P theta^(-2|A intersect Gamma(H)|)
       <= exp[c_prog |A|],
    c_prog = p_tail d(theta^(-2k)-1).

The empty expansion term is Tr rho_P<=1. Both forms are valid; choose a sufficiently small p_tail after theta and geometry. They are not estimates for a normalized survival-conditioned distribution.

Memory raw labels and program labels commute. State Cauchy–Schwarz therefore gives

    Tr rho_P f_low(A) theta^(-missing)
      <= exp[-(a_hi-a_low-c_prog/2)|A|]
                       sqrt(Tr rho_P f_hi(A)^2).

A SECOND Cauchy–Schwarz over all nonempty animals, with rooted count at most A0^m, gives

    Tr rho_P V_env
      <= sqrt[sum_A e^(-(2(a_hi-a_low)-c_prog)|A|)]
         sqrt[sum_A Tr rho_P f_hi(A)^2]
      <= C N,

provided 2(a_hi-a_low)-c_prog>log A0. The first square root is O(sqrt N) and the second is O(sqrt N). This explicitly pays animal entropy. Parameters are noncircular: choose the common memory weights with an entropy margin, then the tail, latency and the smaller of memory/program noise budgets. Every choice is fixed independently of N and u.

## 8. Common canonical span and logical/reference closure
Let Pi be the commuting projector onto envelope below a fixed fraction of the LOW canonical edge barrier, intersected with the killed memory basin. It is an identity on the canonical logical factor. Markov's inequality gives bad killed mass delta<=C N/M_edge.

Starting from any source label in Pi, the envelope bounds every intermediate raw potential below the local-edge barrier. Expand each dressed factor on BOTH DATA blocks with its controller coefficients retained. At every prefix, the imported local-edge theorem says each retained Pauli edge has identity canonical logical action and preserves component safety. Inductively every path ends in the same base canonical correctable span. The statement holds for off-diagonal source coherences and retained program/controller/bath coefficients, not merely for a classical trajectory distribution. Linearity sums the paths without a coefficient count. Since E is unitary, its restriction is an ancillary isometry tensored with identity logical.

The killed native-plus-program evolution already factors as identity logical times an auxiliary CP map: all retained native/noise edges are canonical identities, and nominal program terms are DATA identity in this frame. Fixed logical-independent initialization then gives rho_LR tensor an auxiliary killed state in the canonical representation. Pi only filters that auxiliary state. Hence the good suffix has exactly scalar times the correct logical channel, with a scalar independent of arbitrary logical/reference input.

Program tracing is exact: E is diagonal in program basis and any program-blind output satisfies Tr_prog(E sigma E dagger)=sum_z E_z sigma_zz E_z dagger. Each sigma_zz is positive but may have arbitrary memory/bath correlations. No physical program measurement or reconstruction of a fresh bath is inserted.

## 9. Fixed target decoder and quantitative endpoint
Let D be the base canonical decoder, and U_* Enc=Enc U_L. Set

    D_*=Ad_(U_L) D Ad_(U_* dagger).

This is a fixed target-code decoder and D_* Enc=Id. Its canonical recovery isometry has the SAME zero-error column Enc, not a relabeled logical code. The specified output after F_* dagger equals Ad_(U_L) D(Tr_prog E sigma E dagger). When clocks are completed E=I; the actual physical U_* supplies the logical CNOT. At time zero the native ready frame is identity and E=U_* dagger, so the specified output is identity, not a free CNOT.

An unchanged externally prescribed product decoder would need a separate proof that it corrects the U_* image of the error family. The accepted criterion instead uses this explicit ideal target decoder. The equation defining it is not an available protected logical gate during noisy physical retrieval.

For a reference-entangled input let epsilon_mem bound the full-versus-killed joint channel difference, a the killed trace and b the good projected trace. The accepted native argument gives epsilon_mem<=C N^(3/2)u exp(-b0 ell) and 1-a<=epsilon_mem. The envelope gives a-b<=delta. Gentle projection gives trace distance at most 2sqrt(delta) from the killed state to its Pi compression. Unitary suffix and ideal readout are contractions, so

    gate error <= 2 epsilon_mem + 2sqrt(delta) + delta.

This yields the bound in Section 0, uniformly with references and the common bath. The same low basin and edge threshold are used throughout; no transition to a different postselected memory process is hidden here.

## 10. Independent checks and limitations
check_killed_clock_and_suffix.py uses a 36-dimensional memory/two-clock/common-bath model with correlated reinfection, a program-conditioned memory exit, correlated initial programs/bath, and actual complete-loss killed compression. It checks the Gramian identity, positivity of deleted outgoing contributions and the full subset hierarchy at multiple times. The maximum sampled violation is zero. It separately verifies the SWAP structural-footprint counterexample and the exact target-frame identity with a noncommuting controller forest. These are algebra regressions only, not simulations of the protected native code.

No remaining mathematical blocker was found at the frozen set within the stated imported native/code hypotheses. The earned consequence is one fixed transversal entangling layer without synchronized local completion, still with supplied encoded input/program initialization and ideal framed output. A finite external readout latency remains. The receipt does not certify practical constants, arbitrary programs, repeated use, a Euclidean layout, passive protection, thermodynamic cost, or historical novelty. No external state was mutated.
