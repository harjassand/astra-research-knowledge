# Passive streaming erasure with minimum retained Gaussian memory

Author: `producer-workspace/causal_erasure`, 29 October 2026 Australia/Brisbane.

Status: constructed theorem, independent review pending. This is a finite-bin ideal-receiver result, not a device, noise threshold, numerical bath certificate, or established priority claim.

## Contract and theorem

There are n source qubits with commuting labels z_i=+1 or -1 and accessible bosonic output batches E_1,...,E_T in fixed input order. Batch t has m_t modes and known one-particle features f_{i,t}. After absorbing a common background into the environment state,

    U = G_S sum_z |z><z| tensor W(F_z),
    F_z = direct_sum_t sum_i z_i f_{i,t}.

G_S is a fixed diagonal source unitary to be preserved. Retained mediator displacement must be closed or explicitly accessible to the receiver. A small memory representation or one source observable does not establish closure.

Conventions: Q=a+a†, P=i(a†−a), [Q,P]=2i; Phi(f)=Re(f)^T Q+Im(f)^T P; W(f)=exp(i Phi(f)); omega(f,g)=Im<f,g>. Thus W(f)W(g)=exp(−i omega(f,g))W(f+g).

The receiver uses calibrated passive interferometers, ideal destructive homodyne, retained bosonic modes, and classical records. Its controls depend on known features, not unknown input states. Product local source Z feedback may be accumulated and deferred. There is no added source-to-field coupling. Every quantum ancilla or delay line crossing a cut counts as memory.

The actual record may refine the minimal joint measurement of the n feature quadratures. The comparison preserves the entire refined record of the SAME receiver on the common environment state. It does not claim equality to a smaller-record instrument, return measured modes to their original states, or prepare quadrature eigenstates.

Define Omega_t[i,j]=Im<f_{i,t},f_{j,t}> and K_t=sum_{s<=t}Omega_s. Assume global isotropy K_T=0 exactly.

**Theorem.** An explicit passive receiver and local Z feedback remove W(F_z), preserve G_S, and preserve the complete source/reference/actual-record instrument relative to the common-state receiver for every normal joint input. After batch t, exactly

    r_t=rank(K_t)/2

canonical bosonic modes remain. Peak between-batch memory is max_t r_t <= floor(n/2), with r_0=r_T=0. Incoming modes while being processed are additional; live width at batch t is at most r_{t−1}+m_t.

The count is minimal within the declared exact linear Gaussian receiver class: retained canonical modes and commuting classical homodyne records must reconstruct the required feature observables linearly, without extra coherent source coupling. Arbitrary non-Gaussian encodings, modular Weyl measurements, and approximate state-restricted recovery are outside this lower bound.

## Passive compression lemma

For a family f_i in C^m, let V be its real span and d=dim_R V. Choose a basis orthonormal for Re<.,.>. Orthogonally block-diagonalize the restricted imaginary Gram form. This yields real-orthonormal pairs u_j,v_j, j=1,...,r, and radical vectors c_k, where

    <u_j,u_l>=<v_j,v_l>=delta_jl,
    <u_j,v_l>=i sigma_j delta_jl,  0<sigma_j<=1,

and the c_k are complex-orthonormal and complex-orthogonal to all pairs. There are d−2r radical vectors. The source-coordinate Gram form has the same rank as the restricted form on V because the source-coordinate map surjects onto V. Cauchy–Schwarz gives sigma_j<=1.

For sigma_j<1 define w_j=(v_j−i sigma_j u_j)/sqrt(1−sigma_j^2). For sigma_j=1, v_j=i u_j and omit w_j. Direct inner-product calculation gives

    <u_l,w_j>=0,
    <w_j,w_l>=delta_jl,
    <w_j,v_l>=sqrt(1−sigma_j^2)delta_jl.

Thus all u_j, defined w_j, and c_k together are complex-orthonormal. Complete them to a physical one-particle orthonormal basis: this is a passive interferometer.

Write f_i=sum_j(alpha_ij u_j+beta_ij v_j)+sum_k gamma_ik c_k with real coefficients. Then

    f_i=sum_j(alpha_ij+i sigma_j beta_ij)u_j
       +sum_{j:sigma_j<1}sqrt(1−sigma_j^2)beta_ij w_j
       +sum_k gamma_ik c_k.

Only r modes u_j have complex coefficients. Retain them; homodyne Q on the real-coefficient w_j and c_k modes; trace dark modes. Measured modes contribute known local source phases. They can refine the minimal feature measurement because w_j need not lie in V. The retained imaginary Gram matrix is unchanged: measured coefficients are real and measured/retained sectors are complex-orthogonal.

No squeezing occurs. The normalized residual w_j is not a physical gain; exact saturation is handled separately. Floating rank/tolerance decisions do not certify physical accuracy.

## Streaming proof and complete record

After batch t−1 let g_i be retained features. Apply the lemma to h_i=g_i direct_sum f_{i,t}. Its imaginary Gram matrix is K_t because previously measured coefficients were real. Exactly r_t modes remain. Newly measured modes are disjoint from all future receiver operations. Their quadratures commute with the target feature operators, and local Z feedback can be deferred until the declared controlled-Weyl operation is complete. Immediate source feedback additionally requires commutation with the actual intermediate controls; a final diagonal dilation alone does not establish that condition.

More explicitly, for a receiver stage with measurement amplitude K_x, the spectral-measure version of the intertwining relation is

    K_x W(sum_i z_i h_i)
       = exp(i sum_i z_i theta_i(x))
         W(sum_i z_i g_i') K_x.

It holds as an instrument identity; no bounded point density for ideal homodyne is presumed. Because the split sectors are complex-orthogonal, it introduces no source cocycle. Composing stages accumulates only local Z phases. At K_T=0 no feature memory remains, so feedback cancels every source-dependent Weyl factor.

Equivalently, the complete receiver is one common passive transformation followed by commuting homodyne measurements and a trace over dark modes. Its actual recorded quadratures Y_l obey Phi(F_i)=sum_l b_il Y_l with real b_il, and every Y_l commutes with every Phi(F_i). The local correction is

    C_y=product_i exp(−i Z_i sum_l b_il y_l).

Writing g_z for the diagonal entries of G_S and E_0(dy) for the common receiver POVM, each corrected source block and full actual record are

    g_z conjugate(g_z') Tr_E[E_0(dy) rho_zz'].

This holds for every normal source/reference/environment input block rho_zz', even when correlated. The common record can then be correlated with the source; the identity preserves that assemblage. No independent thermal-output assumption is used. Extra records are explicitly retained; coarsening them, if desired, is a further common channel.

## Matching lower bound in the linear receiver class

At cut t, suppose q canonical modes remain and all other past quantum modes are inaccessible. Noiseless linear reconstruction of each final feature observable requires its past component to lie in the real span of already measured commuting variables and retained canonical quadratures:

    A_{<=t}=B_t Y_{<=t}+L_t R_mem.

A component on a discarded unknown input quadrature would be unavailable to later operations; an independent finite-noise ancilla component would add measurement noise. Neither is compatible with all-input equality of the target characteristic functions. The measured variables commute mutually and with memory. Therefore

    K_t=L_t J_q L_t^T,
    rank(K_t)<=2q.

The passive construction attains q=rank(K_t)/2. More general deterministic Gaussian observables have a Gaussian noise multiplier; equality to the required modulus-one Weyl phases forces zero variance in their directions, recovering this noiseless linear sector. Holevo's classification provides this standard Gaussian-observable ingredient.

This argument does not grant the linear reconstruction premise to arbitrary adaptive non-Gaussian receivers, abstract encodings of many modes into one Hilbert space, or approximate energy-constrained recovery. Nonzero Weyl-lattice modular measurements are a concrete excluded case. All retained quantum bypasses and ancillas must be counted.

## Two-bin example and completion tradeoff

For two sources, f_A=(a,a), f_B=(ib,−ib), a,b>0. The first-bin K is [[0,ab],[-ab,0]], while total K is zero. Exactly one between-bin mode is necessary and sufficient in the linear class. Store bin 1; a balanced beam splitter with bin 2 produces sum and difference modes. Homodyne Q_sum and P_difference, obtaining the commuting observables a(Q_1+Q_2), b(P_1−P_2); apply local Z corrections. This is a standard continuous-variable Bell measurement used as a temporal erasing instrument, not a new Bell primitive.

Direct time-bin homodyne cannot erase both conjugate quadratures in each bin. A different oscillator phase or delayed classical feedback alone does not supply coherent cross-time interference. For a single source, every K_t vanishes and matched homodyne needs no quantum memory.

For comparison, the separate isotropic-completion optimization gives minimum added source-coupled squared-feature budget Tr|i Omega|, attained by H_*=|i Omega|−i Omega, and rank(Omega)/2 added modes. Ordinary detector vacuum ancillas without source coupling do not perform that operation. With no coherent retention across bins, the isotropic-homodyne completion cost is sum_t Tr|i Omega_t|; with coherent blocks B it is sum_B Tr|i sum_{t in B}Omega_t|. Coarsening blocks never increases this budget. For maximum block length L, the optimum in this particular independent-block architecture is

    D(j)=min_{1<=ell<=min(L,j)}[D(j−ell)+Tr|i(K_j−K_{j−ell})|], D(0)=0.

This is not a universal optimum over all causal architectures. In the two-bin example, global completion costs zero, zero-memory completion costs 4ab, and one stored mode replaces that added source coupling. Globally nonisotropic features can append a final coherent completion batch, paying its physical source coupling, phase ledger, preparation, and source waiting time.

## Resource ledger and useful failure

The result identifies which emitted information still requires quantum storage. It converts a global erasing measurement into a causal passive receiver with immediate classical retirement, with a matching lower bound in the linear Gaussian class. This can guide the choice between quantum storage and extra coherent completion ports.

Small mode count does not imply low total cost. Features must be acquired from the actual accessible dilation. The interface needs calibrated mode capture and interference, phases, collection, homodyne readout, source coherence until feedback, and reset/fresh receiver modes for reuse. Memory decay, missed ports, finite local oscillator power, mode mismatch, resolution, gain/phase drift, source preparation/readout/leakage, and scheduling remain separate channels. Ideal sharp homodyne must be replaced by a state/energy-restricted finite-receiver contract for operational claims.

The compiler is passive and does not amplify total photon number. It can concentrate incoming energy into memory; workload energy and storage lifetime still matter. A finite photon cutoff needs actual state/moment bounds. The preceding finite causal-memory bath construction does not automatically certify this receiver, although its full-instrument and moment machinery can be applied after matching the new interface.

**Failed representation, corrected.** An initial Darboux-only compression attempted to preserve an unrefined record. For f_1=(1,0), f_2=(i epsilon,1), it generated a 1/epsilon coefficient. Measuring Q_2 immediately and retaining mode 1 is passive and exact. The divergence was a method cost, not a physical lower bound. The passive-refinement lemma repairs it; the divergent-control claim is discarded.

## Primary ancestry and Astra conditions

1. Holevo, [arXiv:2007.02340](https://arxiv.org/abs/2007.02340), Theorem 1 and Sec. 4: Gaussian-observable structure, noiseless homodyne sector, opposite-symplectic Naimark ancillas and minimal ancilla dimensions. These ingredients are prior work.
2. Guo, Mueller, Liu, [arXiv:2609.05250](https://arxiv.org/abs/2609.05250), Sec. III and Appendix A: optimal sequential realization of a prescribed full symplectic transformation, fixed output emission order, flexible input injection, arbitrary Gaussian register operations, arbitrary inputs. This is the strongest close conventional starting point. Here the target is a commuting measurement/erasure instrument in fixed input order; classical retirement/refinement permit conjugate output quadratures to be discarded. The invariant is the restricted prefix commutator K_t, and a passive compiler attains it. No advantage over an equally informed conventional receiver optimized for this same measurement objective is asserted without comparison.
3. Hofer et al., [arXiv:1303.4976](https://arxiv.org/abs/1303.4976): primary Bell-measurement and continuous-feedback ancestry. The two-bin example uses this established operation.
4. Astra N939 current capsule, retained proof and local-only addendum, saved at `../comparator/ASTRA_N939_*`: already includes exact operator-block homodyne erasure, correlated physical outputs, deferred commuting feedback, preserved entangling phase, and gain/LO caveats. Its current capsule preserves the adverse matched hot/receiver versus cold/no-receiver comparison and unacquired native-output interface. This theorem does not upgrade those physical claims or erase their cross-response; it supplies a causal criterion for globally isotropic accessible features.

The named primary sections and the three named Astra source files were read. Historical priority, hardware capability, and independent acceptance are not inferred from this authored derivation.

Resource clarification: the rank is canonical-mode count, not finite Hilbert dimension, photon number, lifetime or record precision. Unconditional retained energy is bounded by total arriving energy plus ancillas; conditional branches can be larger. Grouping arrivals can lower between-block rank while increasing live capture/storage width.

Scheduling clarification: an emitted mode must not return to the device before its declared retirement. Receiver operations on departed modes then commute with subsequent device operations. Feedback can always be deferred until the full declared operation and record delivery are complete. Early feedback needs the additional microscopic commuting-control condition. The earlier noncommuting contact or sine-contact leakage does not automatically have the controlled-Weyl dilation assumed here.
