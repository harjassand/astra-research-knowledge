# Physical program gauge, target readout and correlated suffix seam
2026-10-30. Construction/interface proof for one asynchronous transversal layer. The whole gate theorem still requires a simultaneously earned strong raw memory moment and the stated canonical-edge inputs.

## 1. Physical support accounting
Take two identical CSS blocks jointly, with one product-code logical/reference factor. Pair the ENTIRE corresponding native resource qudits, including both DATA factors and both resource lock/monitor factors, and adjoin one three-state program register. This is one fixed-dimensional column. Private hub qudits may remain separate. Thus a native hub/resource term remains a two-site hub/column term. This paired column is a NEW declared physical site: its two DATA resources must be colocated or supplied with the stated joint onsite Hamiltonian capability, including DATA_A/DATA_B/program control. A regrouping of symbols does not supply a missing coupler or preserve two-body locality on the original elementary-qubit graph. Remote LOCC-separated halves are excluded. The overhead is a fixed local-dimension/site-grouping factor within the native grouped-qudit model. Onsite program conjugation does not add an all-lock interaction or an elementary-qubit locality assertion.

Let U_i be CNOT between the two corresponding DATA factors in column i, U_*=product_i U_i, and G_i=I P0+U_i(Pe+P1). Define the actual nominal generator to be Ad_G (L_mem+sum L_prog,i) Ad_Gdagger. In particular ALL native memory terms, not just program terms, are conjugated. Its program edge is Omega(U_i|e><0|+U_i^dagger|0><e|), and its actual dissipative e->1 jump is clock-only. Native complete resets/monitors remain onsite under the same onsite conjugation. This is exact, not simulation over a finite time window.

Physical local perturbations become local joint perturbations of the same cb norm in the G frame. The support graph and all program/forest cones must be declared before choosing memory animal parameters. Program clocks stay PHYSICAL column factors counted in the same bounded-body/per-column incidence decomposition for BOTH memory and program estimates. They cannot be reclassified as an unconstrained bath to invoke storage robustness. The external retained bath is separate; adding the known nominal program generator is harmless because it commutes with memory observables and their basin. Cross-block column noise is allowed; it is not justified by treating the other arbitrary logical input as a fixed bath. Instead use the joint two-block code factorization and sum the sector observables, retaining all logical references.

## 2. Total frame order and a program-blind target inverse
Let F=F_mem be the two-block native forest unitary, independent of program labels. In program-plus-forest coordinates write the joint state sigma, including DATA, native controllers, program registers and retained bath. The physical state is

    G F sigma F^dagger G^dagger.

Set the FIXED target native frame F_*=U_* F U_*^dagger. Its inverse is independent of the actual program phases. Exactly,

    F_*^dagger G F=U_* E,
    E=F^dagger(U_*^dagger G)F.

For a computational program label z let S(z)={i:z_i=0}. Then

    E=sum_z |z><z| tensor E_z,
    E_z=F^dagger [product_(i in S(z)) U_i^dagger] F.

Label e already carries the full U_i; treating both 0 and e as unfinished only enlarges the error envelope. The dressed factors E_i=F^dagger U_i^dagger F commute with one another, because the bare onsite U_i do, and each has fixed finite structural support. Their support is NOT generally just the bare DATA column.

For any program-blind output, tracing program registers removes all off-diagonal z,z' blocks EXACTLY:

    Tr_prog E sigma E^dagger = sum_z E_z sigma_zz E_z^dagger.

Each sigma_zz is positive and can remain arbitrarily correlated with stored DATA errors, native controllers and bath. No factorization sigma_zz=p_z sigma_mem is asserted. This reduction is a mathematical partial trace, not a physical program measurement or bath reconstruction.

## 3. Fixed target decoder and the time-zero test
Let Enc be the fixed two-block code embedding and U_L its known logical transversal CNOT, so U_* Enc=Enc U_L. A base canonical decoder D fixes the code. A fixed target recovery isometry may be defined by

    J_*=U_* J (U_L^dagger tensor I_aux),

where J is the base canonical error-space isometry. Its zero-error column is the SAME Enc, not a relabeled logical code. Equivalently, the corresponding ideal target decoder is

    D_*=Ad_(U_L) D Ad_(U_*^dagger),
    D_* Enc=Id.

It is fixed once for this target code/error frame and uses no actual program label. The displayed covariance is a way to specify the mathematical decoder; it is not an assumed ability to apply a protected U_L during physical readout. If an application insists on an externally prescribed unchanged product decoder instead, one must additionally verify correction of the U_* image of the allowed error family. That stronger decoder specification is not automatic.

The total specified readout is D_* after F_*^dagger, with native controllers/programs discarded in the indicated fixed frame. It gives

    output = Ad_(U_L) D(Tr_prog E sigma E^dagger).

At time zero, the program is all0 and native controllers are in the declared ready state. F is identity on that input; E=U_*^dagger there. Therefore the actual readout returns

    Ad_(U_L) D(Ad_(U_*^dagger) Enc(rho))=rho,

not U_L rho U_L^dagger. The decoder alone cannot create the target gate on an unchanged code state. At completed program labels E=I, the physical transversal U_* produces the desired logical channel. This distinction prevents a fictitious decoded gate.

## 4. Full occupation footprint and operator envelope
Let the raw potential have commuting occupation projectors P_v for unary local DATA-energy vertices and physical-history token vertices, and

    f_A=e^(a|A|) product_(v in A) theta^(I-P_v),  0<theta<1.

For each dressed E_i fix its ENTIRE bounded structural support C_i and let D_i contain EVERY raw occupation projector whose full physical support intersects C_i. Use the full analytical token bundle for every such history flag. Do NOT prune this set merely because the exact E_i commutes with one occupation projector: coherent cancellation can make an exact unitary commute while its separate DATA-Pauli coefficients do not. The conservative structural rule ensures that EACH DATA-Pauli times controller coefficient of E_i commutes every occupation projector outside D_i. F acts on workspace, so conjugating a DATA-only missing CNOT can affect history predicates too. Counting only raw syndrome bits, exact-unitary changes or bare DATA-energy changes is insufficient for the common-span proof. There are constants k,d independent of N such that |D_i|<=k and every occupation vertex is in at most d sets D_i.

For S subset columns put D(S)=union_(i in S)D_i. E_S is supported within their structural union and commutes all occupation factors outside D(S). Split f_A into unaffected factors and the m=|A intersect D(S)| affected factors. The latter product lies between theta^m I and I. Hence, on the FULL Hilbert space,

    E_S^dagger f_A E_S <= theta^(-m) f_A.            (4.1)

This is an operator bound for arbitrary nonmonomial coherent local action, not a probabilistic Pauli expansion. With program projectors retained, (4.1) gives

    E^dagger V E <= V_env,
    V_env=sum_z |z><z| tensor sum_A
                    theta^(-|A intersect D(S(z))|) f_A.

The same label envelope covers every prefix of the dressed missing-gate product and every DATA Pauli coefficient path, because the STRUCTURAL definition above makes each coefficient commute all occupation projectors outside D(S). For any fixed source occupation sector, each nonzero target component of such a coefficient path agrees on every outside label; arbitrary changes inside D(S) are paid by the Boolean envelope. This is a support/sector statement, not a false norm bound on each unnormalized coefficient. Those path statements supply logical common-span closure; no factor counting Pauli coefficients is introduced.

## 5. Correlated expectation: explicit double Cauchy–Schwarz
Let B_i=P0+Pe and assume the actual finite-clock bound

    Tr[rho product_(i in R) B_i] <= q_tail^|R|

for all R, where rho can be the UNNORMALIZED killed joint memory state. Define I_A={i:D_i intersects A}, b_i=|D_i intersect A|<=k; |I_A|<=d|A|. Since the actually missing indicator P0_i<=B_i,

    theta^(-2|A intersect D(S)|)
      <=product_(i in I_A)[1+(theta^(-2b_i)-1)B_i].

Expansion into positive coefficients and the inclusion bound give

    Tr[rho theta^(-2|A intersect D(S)|)]
      <=product_(i in I_A)[1+q_tail(theta^(-2b_i)-1)]
      <=exp[q_tail d(theta^(-2k)-1)|A|].            (5.1)

For a subnormalized rho the empty-set term is Tr rho<=1, so the same inequality holds. No memory/program independence occurs anywhere.

Let epsilon_gate=(q_tail d/2)(theta^(-2k)-1). Commuting raw memory factors and program factors obey state Cauchy–Schwarz:

    Tr[rho f_A theta^(-missing)]
       <=exp(epsilon_gate |A|) sqrt(Tr rho f_A^2).

Suppose the SAME physical generator and SAME killed basin earn the strong RAW moment

    sum_A Tr rho f_s,A <= C N,
    f_s,A=e^(a_s|A|) theta^(2(|A|-occupied(A))).

Then f_A^2=e^(-(a_s-2a)|A|) f_s,A. A second Cauchy–Schwarz over all animals gives

    Tr rho V_env
      <=sqrt[sum_A exp(-(a_s-2a-2epsilon_gate)|A|)]
         sqrt[sum_A Tr rho f_s,A]
      <=C' N,

provided a_s-2a-2epsilon_gate exceeds the logarithmic rooted-animal growth rate. This explicitly pays the full animal count; a bound on the square of a DRESSED expectation is not a substitute for the strong raw moment.

## 6. Why the clock bound survives analytic killing
The storage basin projector P depends only on native DATA/controller raw labels, not program registers. Therefore [P,M_S]=0 for every positive product of program Gramian factors used in FINITE_PROGRAM_CLOCK_MOMENTS.md. Complete-loss killed compression satisfies

    L_killed* M_S <= P L_full* M_S P

on P: the difference is the negative of positive outgoing gains. Hamiltonian compression introduces no extra term because M_S commutes P. The product-moment hierarchy therefore applies unchanged to the subnormalized killed state, with its zeroth moment <=1. The backward-test alternative has the same property. One must not condition/renormalize the killed branch or assume CP domination of the unmeasured evolution.

## 7. Remaining gate implication
On a commuting source projector with V_env below the canonical local-edge barrier, and the imported safe-component conditions, all local Pauli coefficient paths of E remain in the base correctable canonical span. The code-edge identity then makes their logical action identity, including retained program/controller/bath coefficients. Linear closure handles all coherent branches at once. E is unitary; on this safe input span its ancillary action is isometric and cannot depend on logical/reference input.

The complement has killed mass O(N/M) from Section 5. Gentle projection gives an O(sqrt(N/M)) channel error on this suffix, reference-stably, while the prior full-versus-killed storage bound is added separately. The fixed target readout then produces the desired logical CNOT, not identity. This argument still requires the simultaneous strong raw-memory moment and a full common-span review. It does not establish repeated programmable gates, live handoff, noisy physical retrieval or non-Clifford universality.
