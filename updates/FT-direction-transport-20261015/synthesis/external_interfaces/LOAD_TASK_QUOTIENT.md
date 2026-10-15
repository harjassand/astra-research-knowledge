# An acquired load-control quotient instead of a completed adjoint

Date: 15 October 2026. Status: internally derived, not externally reviewed; historical novelty UNKNOWN. No new experiment or technological advantage is claimed. This note reconstructs a task-sufficient part of existing Virtual VNA machinery, with an explicit rectangular observation contract and exact finite-load recovery. The primary source itself already contains the diagonal scaling equivalence; the broader operation of learning a compact tunable-wave model is established prior art.

## 1. Exact target and acquired inputs

At one fixed frequency or in a real static linear regime, suppose an unknown fixed plant belongs to the family

    A(q) = A0 + V diag(q) V^T,
    M(q) = C^T A(q)^(-1) B,                         (1)

where A0 is invertible, V has m columns, B has a source columns, and C has b readout columns. Matrices may be complex; T is the algebraic transpose in this network formula, not the Hermitian adjoint. There is no reciprocity assumption on A0. The state dimension may be arbitrarily larger than m,a,b.

The accessible measurement is the coherent b-by-a transfer block M(q). Its columns require a linearly independent settled source profiles at each load setting. The controls are calibrated scalar load increments q_i relative to a common reference q=0. The physically chosen B,C and their gains must stay the same throughout. The unknown local state fields and V need not be numerically supplied to the estimator, but the physical loading law (1) must be independently justified. A single lumped element or a qualified conductance edge is a possible realization. Arbitrary changes of unknown components do not automatically satisfy (1).

We target only decisions whose outputs depend on M(q), including a fixed accessible input u, a measured output M(q)u, and a known objective F(M(q)u,q). We do not target hidden state fields, unknown component derivatives, or a full physical adjoint. This target matches finite load-setting decisions even if all nonreciprocity is distributed throughout the hidden plant.

For a real strictly accretive A0 and real V, every q>=0 preserves strict accretivity, hence invertibility. This supplies an algebraic safe set under a justified premise; it is not an experimental certification of that premise or a dynamical stability proof. Complex frequency-domain admissible loads need their actual passivity and stability contract.

Set

    M0 = C^T A0^(-1) B,
    U  = C^T A0^(-1) V,       W = V^T A0^(-1) B,
    H  = V^T A0^(-1) V.

Woodbury, with its usual invertibility assumptions, gives

    M(q) = M0 - U (I+QH)^(-1) Q W,   Q=diag(q).      (2)

This form allows some q_i=0. For nonzero q_i it equals M0-U(Q^(-1)+H)^(-1)W. Formula (2) is standard inverse-update algebra, not a new identity.

## 2. Why the full hidden matrix is unnecessary

Let D be any nonsingular diagonal complex m-by-m matrix and replace

    U -> U D,       W -> D^(-1) W,       H -> D^(-1) H D.    (3)

Because D commutes with every Q=diag(q), substitution into (2) leaves M(q) unchanged at every stable diagonal load setting. Thus the entire task, every finite setting comparison, and every derivative in calibrated q coordinates are invariant under (3).

The equivalence class (M0,U,W,H)/(3) is enough. Its representative may fail physical passivity tests as an internal matrix because arbitrary hidden coordinate scales need not preserve the standard power normalization. Only its predicted accessible transfer and the justified physical family are used here. Internal reciprocity or individual hidden couplings cannot be certified merely by selecting a representative.

This cancellation is the operational meaning of the correlated row/column scaling in Virtual VNA 3.0, Eq. (25). Coupled loads are used there to lift the remaining scalings for the stronger goal of full unambiguous DUT characterization. They are not needed for the diagonal-load task once a correct representative has been acquired. For a general coupled load Q, DQ need not equal QD, so the cancellation does not apply; cross-port control can require the additional calibration.

## 3. Exact finite-setting reconstruction

Assume m>=2, a,b>=2 and the following observability conditions:

1. For every i, U_i W_i is nonzero, where U_i is column i and W_i is row i.
2. For each pair i!=j, [U_i,U_j] has column rank two and [W_i;W_j] has row rank two.
3. Two known nonzero distinct increments t_i,s_i are available for each i. The baseline, all selected one-load settings and all selected pair settings are invertible.

The pair conditions are explicit. They do not follow solely from having two ports, from low algebraic rank, or from observing one dominant differential singular value. They are generic algebraic conditions in broad model classes; finite noise requires a quantitative singular-value margin, not merely nonzero determinants.

Unlike microscopic support, these pair conditions can be checked from the acquired single-load rank-one factors below: independent nonzero rescaling leaves their ranks unchanged. Thus exact data can establish the observable pair-rank gate before the pair measurements. In an experiment, its finite-precision counterpart needs calibrated uncertainty for the joint measurements and a resolved lower singular-value margin. This check does not certify the assumed loading family or background constancy.

### Theorem 1: two-by-two measurements suffice under pair observability

The following coherent measurements determine a representative of (3), and hence M(q) for every stable diagonal q:

    M(0),
    M(t_i e_i), M(s_i e_i)          for i=1,...,m,
    M(t_i e_i+t_j e_j)              for 1<=i<j<=m.        (4)

There are

    Nload = 1+2m+m(m-1)/2                            (5)

load settings. With a=b=2 this means 2 Nload settled source profiles and 4 Nload calibrated scalar transfer readings, before repeats, settling, gain/phase calibration and load characterization. In a complex experiment each scalar reading is a complex amplitude and phase measurement. Neither the count nor exact algebra is a noise guarantee.

### Proof: recover each diagonal and rank-one product

Holding all other loads at zero, (2) becomes

    Delta_i(t) := M(t e_i)-M0
               = -t/(1+t h_i) * C_i,
    h_i=H_ii,     C_i=U_i W_i.                       (6)

Choose a matrix entry or known linear functional ell for which d_t=ell(Delta_i(t_i)) is nonzero. Under the assumptions d_s is also nonzero, and d_t-d_s is nonzero because t_i!=s_i and C_i!=0. Direct elimination gives

    h_i = (t_i d_s-s_i d_t)/(t_i s_i(d_t-d_s)),
    C_i = -(1+t_i h_i) Delta_i(t_i)/t_i.              (7)

No infinitesimal perturbation or local constitutive derivative is used. Factor the acquired rank-one C_i as u_i w_i, with nonzero column u_i and nonzero row w_i. Any exact rank-one factorization is permitted. There is a nonzero scalar d_i such that

    u_i=d_i U_i,      w_i=d_i^(-1) W_i.

Collect these into Utilde, Wtilde and D=diag(d_i). Set Htilde_ii=h_i. The two settings do not determine d_i, and the task does not require them.

### Proof: recover directional interaction for each pair

Fix i<j. Let Utilde_ij=[u_i,u_j] and Wtilde_ij=[w_i;w_j]. Choose a left inverse L_ij of Utilde_ij and a right inverse R_ij of Wtilde_ij, which exist by pair observability. Define

    Z_ij = -L_ij [M(t_i e_i+t_j e_j)-M0] R_ij.       (8)

Only this pair is loaded, so Woodbury in its two-dimensional active subspace gives

    Z_ij = (diag(1/t_i,1/t_j)+D_ij^(-1)H_ij D_ij)^(-1). (9)

The matrix in (9) is invertible because the corresponding selected loaded plant is invertible. Therefore

    Htilde_ij = [Z_ij^(-1)]_12,
    Htilde_ji = [Z_ij^(-1)]_21.                      (10)

The diagonal entries provide redundant checks against 1/t_i+h_i and 1/t_j+h_j. The separately chosen single-load factors fix a common diagonal gauge across all pairs, so repeating (10) recovers Htilde=D^(-1)HD on the whole m-by-m matrix. Together Utilde=UD and Wtilde=D^(-1)W. Section 2 proves exact prediction at every stable diagonal q. QED.

For m=1, a single nonzero input/output transfer coefficient and the baseline plus two finite increments suffice by (7); the rank-two pair condition is absent. For m>=2, two inputs and two outputs are the minimum dimensions for this particular two-sided pair-inversion construction. No universal information-theoretic optimality claim against all other acquisition protocols is made.

The third setting for m=1 cannot generally be replaced by observing one frozen differential mode. For example, take one accessible coordinate, one coordinate load, and the two reciprocal positive-definite inverse plants

    T0=[[2,1],[1,1]],       T1=[[2,2],[2,7]],
    A0=T0^(-1),            A1=T1^(-1).

Their accessible scalar transfers under load q e2 e2^T are respectively

    M0(q)=2-q/(1+q),       M1(q)=2-4q/(1+7q).

Both give M(0)=2 and M(1)=3/2, but their derivatives at zero are -1 and -4. All q>=0 are admissible. One reference and one finite toggle therefore fail to determine even the sign-independent derivative magnitude, despite exact rank-one difference and reciprocity. A second nonzero load value supplies the missing feedback scalar h in (7). This is a sharp three-setting statement for this load-response data interface, not a lower bound against extra local sensors, independent compliance measurements or a physical adjoint.

## 4. Derivatives and actual finite decisions

After acquiring the representative, let

    Lq=(I+Q Htilde)^(-1),   Rq=(I+Htilde Q)^(-1).

Differentiating (2) gives the exact measured-coordinate derivative

    partial M / partial q_j
       = -Utilde Lq e_j e_j^T Rq Wtilde.             (11)

It has rank at most one. Equation (11) is independent of D. For a real objective of complex measured fields the usual real chain rule, including conjugation of the objective derivative, is still required. If physical knob p_j changes q_j by a calibrated function q_j(p_j), multiply (11) by q_j'(p_j). Unknown knob/load response is not supplied by the theorem. For finite settings with known q, no derivative of the knob response is needed.

A finite menu of allowed q values can be evaluated directly through (2) and the declared objective. For a continuous nonconvex objective, exact evaluation and gradients do not provide a free global optimizer or finite-step improvement guarantee. Final candidate settings should be tested physically, since drift/model error can invalidate open-loop prediction.

## 5. What is acquired and what is still assumed

This protocol acquires the entire relevant finite-load response modulo a task-invisible gauge. It does not need the closure note's assumption that every nonreciprocal component lies in known accessible source ports. Nonreciprocity of A0 may be extensive.

The replacement assumptions are substantial: calibrated individual loads, fixed background and source/readout loading, coherent two-channel access, a valid one-coordinate loading model, stable selected settings, and pair observability. A low-rank observed Delta M does not certify that the microscopic perturbation was one-coordinate or that no unobserved component drifted. Predicted responses should be checked on held-out load settings. Passing finitely many held-out checks is a measured model-validation result at its declared tolerance and regime, not a theorem excluding all other plants.

If a single-load product vanishes, the control is not automatically globally irrelevant. It may become observable after another load changes. If two coupling columns or rows are collinear, the pair inversion loses information even though each single-load measurement can be nonzero. More accessible channels, other baselines, extra joint load configurations, or a different identification procedure may repair those cases; Theorem 1 supplies none of those repairs for free.

### All diagonal-load data can still fail to certify hidden reciprocity

This is stronger than a failure of a particular finite protocol, and follows directly from the same gauge. Let the first two coordinates be accessible and the last two be load ports. Define

    A0 = 4I + (1/10) [[0,1,2,3],
                      [1,0,4,5],
                      [2,4,0,6],
                      [3,5,6,0]],
    Dhat=diag(1,1,2,3),   A1=Dhat^(-1)A0 Dhat,
    B=C=[e1,e2],          V=[e3,e4].                 (12)

A0 is symmetric positive definite. A1 is not symmetric; its symmetric part is positive definite by strict diagonal dominance (each diagonal is 4 and the largest absolute off-diagonal row sum is 119/60<4). Both are therefore strictly accretive admissible real plants. For every diagonal Q, the coordinate load update commutes with Dhat, and

    A1+VQV^T = Dhat^(-1)(A0+VQV^T)Dhat.

Because B,C lie in the coordinates where Dhat=I,

    C^T(A1+VQV^T)^(-1)B = C^T(A0+VQV^T)^(-1)B     (13)

whenever the inverse exists, in particular for every q>=0. Thus arbitrary adaptive sequences, complete coherent accessible readout, unlimited diagonal-load settings and zero measurement noise still cannot distinguish these plants. One is reciprocal and the other is not. All target diagonal-load decisions nevertheless agree exactly.

Consequently target identification should not be promoted to a certificate of hidden reciprocity or of the support of its defect. A known load coupling two differently scaled coordinates fails to commute with Dhat and can distinguish this example; this is precisely why the stronger Virtual VNA characterization problem adds coupled-load measurements. Merely collecting additional diagonal-load examples cannot lift this ambiguity.

## 6. Matched-cost comparator and prior-art boundary

For a single fixed-operating-point gradient, the incoming known-port completion costs k+2 settled profiles and sensed rows at local derivative supports. A known applicable physical intertwiner can cost only one extra run after the ordinary forward run, but requires transformed source access and transformed readout. Direct tangent-source probes cost the number of needed source directions when those sources are synthesizable. Tuned multiplexed/random-direction or finite-action tests remain strong comparators for making one useful decision.

The quotient identification costs (5) load settings and a profiles per setting. It changes control settings during calibration, but requires no local state sensing and no objective-source injection at a hidden coordinate. It is reusable for multiple objectives, source choices in the calibrated input span, and updates of the same m loads, while the background remains fixed. Amortization can matter; there is no unconditional dominance. With m=30, a=b=2, the count is 496 settings, 992 source profiles and 1984 scalar transfer readings. Against six profiles per freshly calibrated port-completion operating point, the source-profile-only crossover is 166 operating points; this comparison omits different instrumentation, sensing, settling, energy, drift and optimization costs and is not a speedup claim. Against direct evaluation of a small candidate menu, this calibration can be much more expensive.

The strongest prior method is not an untreated plant or coordinate finite differences. Virtual VNA 3.0 already provides nonreciprocal load-based reconstruction, and its existing intermediate Eq. (25) supplies the gauge used here. Earlier experimentally calibrated physical models already support open-loop control in unknown programmable scattering media; their parameter nonuniqueness is explicitly acknowledged. Thus the meaningful integration gain is recognizing a task-sufficient acquired interface and charging its actual costs. It is not the invention of forward-only model-free control, low-rank scattering, Woodbury, or a new adjoint principle.

## 7. Primary sources read and the exact scope of transfer

[Virtual VNA 3.0, arXiv:2503.07239v1](https://arxiv.org/html/2503.07239v1): Sections III, IV-A2--IV-A6 and IV-B1; Eqs. (1), (11)--(25), and cost line surrounding Eq. (1). Its intermediate scaling statement underpins Section 2. Theorem 1 above is a self-contained reconstruction with explicit rectangular pair-rank hypotheses, not a quoted theorem about all plants.

[Frozen differential scattering, arXiv:2509.09506v1](https://arxiv.org/html/2509.09506v1): Sections 2.2.1--2.2.2 and supporting coupled-dipole derivation. The exact rank-one update for one qualified lumped perturbation is prior machinery. The measured differential mode does not identify or certify the support of all nonreciprocity.

[Experimentally realized physical-model-based frugal wave control, Nature Communications 15,2841 (2024)](https://doi.org/10.1038/s41467-024-46916-2): physical model, calibration, discussion and data/code availability. Existing calibrated-model open-loop wave control is the prior operational comparator. No experimental numbers are imported into the reconstruction.

[Unifying Physical Backpropagation, arXiv:2608.11585v2](https://arxiv.org/html/2608.11585v2): Section 9 theorem, Eqs. (79),(84)--(89), and implementation requirements. Known fixed invertible intertwining plus transformed source/readout access is a cheaper exact comparator in applicable systems. Its theorem does not acquire an unknown intertwiner.

[In-situ time-domain physical adjoint optimization, arXiv:2608.19456v1](https://arxiv.org/abs/2608.19456v1): actual PDF pp.3--4,6--8,14--15, including the stated H=Theta H^T Theta^(-1) transformation and RLC hardware scope. The paper exists and reports an RLC experiment; no replication, raw-data reanalysis, or universal physically accessible Theta is asserted here.

Source version, hashes, actual read ranges, access failures and OpenAI/math current-pin relevance check are recorded separately. Downloaded manuscripts are scratch only and excluded from the final authored packet.
