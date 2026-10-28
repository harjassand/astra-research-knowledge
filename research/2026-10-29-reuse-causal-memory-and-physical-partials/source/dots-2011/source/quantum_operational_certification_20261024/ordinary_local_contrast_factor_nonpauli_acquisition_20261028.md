# Local inverse acquisition from positive own-qubit contrasts: a nonunital amplitude-damping opening

28 October 2026. **New candidate; independent receiving pending.** This is NOT an automatic use of the Pauli/gauge theorem. A separate reduced-contrast contract is proved sufficient for the actual finite algorithm, then realized by product amplitude damping before an unknown local mixer, with arbitrary compatible coherent source completion. The service comparison uses the slower unframed operator-norm fallback, not CP domination or a native identity-channel claim.

## 1. Actual conditional contrast contract

Use the full physical n-input port, independent ordinary product X/Z preparation axes/signs, product-Pauli output readout and finite local controls. A fixed unknown n-qubit V defines exact generators

    B_(i,X)=V X_i Vdagger, B_(i,Z)=V Z_i Vdagger,

jointly supported in an unknown interval S_i of supplied maximum width w on a known output line. Distinct input-qubit algebras commute. The source can retain arbitrary coherent memory; no reset or Pauli-instrument representation is assumed.

Given the COMPLETE PRIOR classical record, average all other current input labels. Let rho_(i,j,+),rho_(i,j,-) be the two actual reduced physical output states for the selected i,j preparation. Their signed contrast is Delta_(i,j)=(rho_+-rho_-)/2. Require the following identity at EVERY allowed conditional source-memory state/history, before any current readout is conditioned on:

    Delta_(i,j)=B_(i,j) R_(i,j),
    R_(i,j)>=0,
    [R_(i,j),B_(i,X)]=[R_(i,j),B_(i,Z)]=0.                     (1)

The positive factors may be unknown, different for each i,j, history-dependent, rank deficient and noncommuting with OTHER qubits' logical generators. No numeric margin or floor is supplied. This is a trusted reduced-observation contract, not a finite transcript test of all inaccessible memory states. The two axes need not share an R. Current input/readout coins are independent of the selected source map except through their actual quantum inputs.

By physicality of rho_±, ||Delta||1<=1. Since B is a reflection commuting with R>=0, ||Delta||1=Tr R, so the actual contrast mass lambda_(i,j)=Tr R lies in [0,1]. Averaging the current sign gives the source output on the same globally maximally mixed INPUT for every selected axis; its OUTPUT rho_h need not be maximally mixed or unital.

## 2. Why the finite support/sign learner remains valid

If J contains S_i, partial trace gives Delta_J=B_(i,j,J) R_J with R_J>=0 and commuting with both own generators. Consequently ||Delta_J||1=Tr R. If J is disjoint from S_i, conjugation by the complementary own generator flips Delta, commutes with R, and occurs entirely in the traced subsystem; therefore Delta_J=0. Commutation with other qubits' generators is unnecessary for either argument.

Every reached bank's predictable average still factors through the SAME fixed B with a positive averaged R. Therefore the received margin-free algorithm's paired-axis coarse scores, permanent support certificates, envelope expansion and independent raw-sign guards have the same deterministic soundness proofs. Fine gaps are learned from the actual local Delta; a maximally mixed marginal is no longer asserted.

The matrix-martingale proof also remains valid. The ACTUAL outputs are positive normalized states from a CP complete source. Fresh sign averaging makes the same rho_h occur for each selected axis; ordinary product shadows give conditional second moment <=2*3^W I and centered increment <=4*2^W for the signed records. These bounds do not require output unitality, Pauli noise, CP signed memory maps or commutation with all other logical factors. All finite unions, rational Jacobi residuals, strict gap comparisons and capped acceptance decisions are unchanged. This is a specific hypothesis audit of the algorithm, not an expansion of earlier sources by citation alone.

Run its reflection guards at delta<=zeta/(3n), as in the separate coherent-memory fallback. On the simultaneous good accepted event every learned S_(i,j) obeys ||S-B||op<=delta. The actual 3n-block coherent SWAP receiver then has

    ||W_hat-W_*||op<=3n delta<=zeta,
    half-diamond(Dhat,Ad_Vdagger)<=zeta.                        (2)

Thus it transfers to arbitrary future coherent source completions and any supplied known decoder, comparing the PARTICULAR fixed Vdagger process. No service frames are needed for this unframed complete-norm bound. Finite causal reuse pays at most J*zeta plus one bad-record and whole-process implementation debit. It does not claim an identity-logical native channel, oracle recovery, quadratic error suppression or fault tolerance.

## 3. An explicit non-Pauli, nonunital source family

Let the reduced pre-mixer physical channel be a product of computational-basis amplitude-damping channels AD_(gamma_k), with unknown 0<=gamma_k<1. Its ordinary single-qubit Bloch action is

    (x,y,z) -> (sqrt(1-gamma)x, sqrt(1-gamma)y,
               (1-gamma)z+gamma).

This is nonunital for gamma>0 and is not a Pauli channel. Write

    rho_k=AD_(gamma_k)(I/2)=(I+gamma_k Z)/2,
    lambda_(i,X)=sqrt(1-gamma_i), lambda_(i,Z)=1-gamma_i.

The actual signed responses after the SAME fixed V are exactly

    Delta_(i,j)=V[(lambda_(i,j) sigma_(i,j)/2)
                    tensor product_(k!=i) rho_k]Vdagger,
    R_(i,j)=V[(lambda_(i,j) I_i/2)
                    tensor product_(k!=i) rho_k]Vdagger.        (3)

They satisfy (1). The affine translation gamma_i Z cancels between the two signed input labels. R can fail to commute with another qubit's X generator; that does not invalidate this new argument. The damping basis is the specified computational basis; no claim is made here for arbitrary unknown rotated damping axes.

More generally a prior memory POVM/instrument can select a product-rate vector gamma_(a,k). On every conditional memory state, suppose the REDUCED physical channel is a mixture of these products with weights Tr(E_a omega), E_a>=0 and sum E_a=I. Positive convex combinations of (3) satisfy (1). Any complete channel compatible with this reduced channel is allowed: it may retain coherent jump/no-jump environments, rate labels and arbitrary future-accessible memory. The proof never reconstructs that completion. Uniform reduced-contrast validity at every reached memory state remains a premise; a one-time process-tomography fit would not establish it.

## 4. Locality prevents an artificial global product floor

A naive full-output bound would multiply (1-gamma_k) over ALL n sites and suggest exponentially small excitation. For this local-mixer interface that is unnecessary.

Fix a physical output interval J of length at most W that contains S_i. Let K(J) be the input-qubit indices k whose true support interval S_k intersects J. If k is outside K, every output operator O_J commutes with BOTH B_(k,X),B_(k,Z). Hence Vdagger O_J V commutes with X_k,Z_k and acts as identity on that input qubit. Therefore the entire reduced output on J depends only on the reduced INPUT on K. There exists a CPTP reduction map Lambda_(K->J), independent of all input states outside K, with

    Lambda(I_K/2^|K|)=I_J/2^|J|.                               (4)

The normalized-unital identity follows by inserting the globally maximally mixed input into the unitary V. This locality statement concerns the true V, not access to its inverse.

Every S_k intersecting J lies inside J expanded by w-1 sites on each side. Those input qubits' independent full Pauli algebras are all represented on that expanded output region. Dimension packing therefore gives

    |K(J)|<=min(n, |J|+2(w-1)).                                (5)

In particular i is in K when J contains its nontrivial support. Suppose a uniform physical class bound gamma_(a,k)<=gamma_max<1 holds on every reached branch/history. Put a0=1-gamma_max. For each product component, the restriction of the positive PRE-V factor in (3) to K obeys

    R_pre,K >= a0^|K| I_K/2^|K|,

since each other rho_k>=a0 I/2 and both own lambda choices are >=a0. Apply the positive map Lambda and (4); convex mixtures preserve the inequality. Thus the local positive factor has

    R_J>=a0^|K| I_J/2^|J|.                                    (6)

With the algorithm's conservative W=min(n,3w-2), set L=min(n,W+2(w-1)). All reached fine-envelope signed gaps are therefore at least

    gamma_gap=a0^L/2^W.                                       (7)

The coarser own-axis masses are at least a0. The learner need not know gamma_max or these gaps; finite direct guards acquire them. For fixed w and fixed gamma_max<1, sufficient funded stages of the slower unframed learner use

    O_tilde(n²12^W/[a0^(2L) zeta²]) fine source blocks,          (8)

plus coarse discovery. This is polynomial in n at fixed width, not a product-of-all-n excitation assumption. It remains potentially enormous and is not a practical-budget or optimality claim. If gamma_max tends to one or the true mixer width grows, the bound deteriorates. Without a uniform bound, sound finite acceptance/abstention still holds but fast completion is not promised.

## 5. Limits and physical accounting

All calibration source blocks contain n actual product preparations and n actual readouts; they are not protected references. The known physical port, unknown but fixed local mixer, finite local controls, all elapsed stages, rational sign synthesis, routing, n extraction ancillas, complete service holding/errors and any known encoder/decoder are paid. Actual finite controls transfer the declared exact-operator guarantee in complete norm, not by preserving an exact CP-order identity. No unknown payload is held during training; acceptance precedes its request.

This construction removes the Pauli/unital restriction for a genuine aligned amplitude-damping family and a stated wider positive-own-contrast class. It still does NOT learn an arbitrary channel, choose an optimal new code, validate the structural contract from finite data, eliminate the inverse-square-accuracy complete-norm cost, or establish a threshold. The equally informed conventional learner can use exactly this procedure.
