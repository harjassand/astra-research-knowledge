# Acquiring the residual local quantum channels from the same whitening records

28 October 2026. **New candidate; separate review pending.** This closes a particular missing interface after positive Bloch whitening: a supplied finite code/controller library can be evaluated against acquired residual channels, rather than being given a free exact noise model. It does not discover optimal quantum codes, infer unseen memory effects, or make microscopic environment reconstruction necessary.

## 1. Scope and records

Use the ordinary XYZ preparation/product-Pauli output records and successful finite guards from `ordinary_unknown_axis_positive_bloch_whitening_20261028.md`. Restrict here to the stationary product-qubit CPTP family of `local_noise_polar_identifiability_extension_20261028.md`, with nonsingular orientation-preserving Bloch matrices. The canonical target is V_eff, which absorbs each local channel's proper orthogonal polar factor. The residual local affine map has a real symmetric positive definite Bloch matrix S_i and real translation t_i. The original pre-noise unitary decomposition is not separately identifiable.

For a containing local envelope J, exact contrasts have Delta_j=(sum_k S_kj B_k)R, with Tr R=1, R>=0 commuting with the own qubit algebra. Put c=Tr R² and G_jk=Tr Delta_j Delta_k=c(S²)_jk. Exact whitening F_j=B_j R/sqrt(c) therefore gives

    l=Tr|F_j|=1/sqrt(c),
    S=l sqrt(G).                                               (1)

The normalization Tr R=1 is essential here and holds for the product family; it is NOT imported into the wider varying-contrast class whose R can have another trace. For the same fully mixed physical input, let rho_J be the unsigned mean output. Then

    t_j=Tr(B_j rho_J).                                         (2)

Thus the positive Bloch contraction and affine translation are identified by observable local contrasts and the unsigned mean, without reconstructing environmental degrees of freedom.

## 2. Same-record simultaneous confidence, without a selection loophole

Alongside every signed fine-bank estimate, retain the ordinary UNSIGNED local shadow average rhohat_J. For fixed prior-selected envelopes its conditional expectation is rho_J; in this stationary product family rho_J is fixed. Its variance/increment bounds are no larger than the signed XYZ bounds. Allocate a separate beta_u over all n envelopes and all declared finite banks, or increase the existing logarithm so that signed and unsigned errors hold together. For a fresh bank N>=16*3^W*L/a0² with L covering these unsigned processes, obtain ||rhohat-rho||op<=a0. Use the larger of the signed and unsigned bank requirements; these are the SAME actual outcomes, not independent extra acquisitions.

Learned reflections and the eventual selected code can depend on this bank. That causes no independence assumption: every following implication is deterministic on one simultaneous event. If a record is chosen from several banks, their union was already charged. Reused source records are counted once. Actual control-induced record changes retain the complete-record discrepancy debit, and conditional-on-acceptance guarantees retain the acceptance denominator.

## 3. Finite contraction-matrix certificate

Use the whitening source's known quantities: Ghat, q=max(1,Tr Ghat), certified h>g, rational W0 approximating Ghat^(-1/2) with error u, and Ctilde_j=sum_k Deltahat_k W0_kj satisfying ||Ctilde_j-F_j||op<=E. All displayed bounds below can be replaced by outward-rounded rational upper bounds.

Compute a nonnegative rational lhat approximating Tr|Ctilde_X| with additive error v_l by finite rational Jacobi/trace-norm arithmetic. The trace-norm Lipschitz bound gives

    |lhat-l|<=e_l=d E+v_l,
    1<=l<=sqrt(d), |lhat|<=sqrt(d)+e_l.                         (3)

Use the explicitly rational symmetric H0=Ghat W0. Because W0 is a real polynomial in Ghat with rational coefficients, H0 is symmetric and

    ||H0-sqrt(Ghat)||op<=q u.

Set Shat=lhat H0. The positive-square-root Sylvester bound and G>= (h-g)I give

    ||sqrt(Ghat)-sqrt(G)||op<=g/[sqrt(h)+sqrt(h-g)].

Consequently a certified spectral error bound is

    ||Shat-S||op<=D_S,
    D_S=e_l sqrt(q) + sqrt(d)*g/[sqrt(h)+sqrt(h-g)]
                         +(sqrt(d)+e_l)q u.                   (4)

No unknown c is supplied. The small inverse-root/trace-norm computations and their precision are paid by the finite algorithms, not access to a spectral oracle. Shat need not itself be the Bloch matrix of a CPTP map; that is repaired below.

## 4. Finite affine-translation certificate

For this residual-model extension require successful operator certificates for ALL THREE learned reflection axes, ||Bhat_j-B_j||op<=delta. This adds finite local sign/control-description work; the third contrast was already measured for whitening and no extra source block is implicit. Alternatively the known matrix (i/2)(Bhat_X Bhat_Z-Bhat_Z Bhat_X) has norm<=1 and approximates B_Y within the sum of X/Z errors, but the all-three version avoids that extra bookkeeping.

Define that_j=Re Tr(Bhat_j rhohat), computed from the same records. On the joint event, using ||Bhat_j||1=d and Tr rho=1,

    |that_j-t_j|<=d a0+delta=:tau.                             (5)

No data-splitting or independence of Bhat and rhohat is asserted: the trace inequality holds uniformly for every actual fitted reflection on the event. Whole-process implementation and source-membership assumptions are unchanged.

## 5. Explicit rational CPTP repair with a local channel certificate

Construct the normalized Choi matrix of the affine estimate, output register first,

    Jhat=1/4 [I tensor I + sum_a that_a sigma_a tensor I
                      +sum_ab Shat_ab sigma_a tensor sigma_b^T].

It is exactly Hermitian and trace-preserving in the Choi sense, Tr_out Jhat=I/2, but may fail positivity. Choose a rational e satisfying

    e >= 3 tau + 3 sqrt(3) D_S.                               (6)

The true normalized Choi J obeys ||Jhat-J||1<=e and ||Jhat-J||op<=e/4: the coefficient l1 bound is <=3tau+3sqrt(3)D_S because the entrywise l1 norm of a 3-by-3 spectral-error matrix is <=3 times its Frobenius norm, which is <=3sqrt(3)D_S. Every tensor Pauli has operator norm one and trace norm four.

The following explicit repair is therefore physical without solving a free SDP:

    Jphys=(Jhat+(e/4)I4)/(1+e).                                (7)

On the simultaneous confidence event, positivity follows from Jhat>=-(e/4)I4, and partial trace remains I/2. Before outputting or using a channel description on ANY record, test all 15 nonempty principal minors of the rational Hermitian Jphys for nonnegativity. If any fails, return ABSTAIN before requesting an unknown payload (or a predeclared fixed depolarizing model if no accuracy claim is made on that branch). This exact finite PSD guard ensures physicality even on bad confidence records; on Good it always passes and adds no statistical debit. The resulting accepted rational qubit channel Nphys has

    (1/2)||Nphys-Ntrue||diamond
       <=min(1, 5e/[2(1+e)])=:eta.                            (8)

Indeed ||Jphys-J||1 <= [e+e||I4/4-J||1]/(1+e) <=5e/[2(1+e)], since any four-dimensional density matrix is within trace norm 3/2 of I4/4. The unnormalized Choi/diamond bound gives half-diamond <= normalized-Choi trace norm for input dimension two. The rational Choi is an executable known finite channel description, not a claim its Kraus control has already been compiled or physically implemented. Candidate evaluation only requires that description.

This repair is conservative and not proposed as the optimal estimator. A conventional constrained channel fit may improve it. Its value here is an explicit finite positivity operation and a complete error certificate tied to actual records.

## 6. What a supplied finite code/controller library can now do

Let a finite supplied library contain known CPTP encoders E_l and decoders R_l with finite rational/algebraic descriptions, or certified computable approximations whose actual channel-error and finite arithmetic budgets are explicitly paid for the SAME n-qubit physical block and k-dimensional logical payload. Their circuit costs, descriptions, preparation errors, service times and readout/reset controls are not assumed negligible. Define the model product channel Nhat= tensor_i Nphys_i and the true canonical residual product channel N=tensor_i Ntrue_i. Complete-norm telescoping gives

    (1/2)||Nhat-N||diamond<=min(1,sum_i eta_i)=:Eta.            (9)

This is a claim about the reduced physical PRODUCT channel, not a model of its complete retained environment. It does not approximate an arbitrary correlated multi-use memory channel.

For each candidate compute the ordinary entanglement infidelity of R_l Nhat E_l to additive v_eval, using its explicit matrices/Kraus circuits and the full normalized logical Bell input. These computations can be exponentially large in n and the number of candidates; no efficient generic code optimization is promised. Choose a candidate with computed score within v_sel of the smallest computed score. Uniform complete-norm control makes all model scores differ from their true reduced-channel scores by at most Eta, simultaneously, without another source or union over the library. Therefore its true reduced-channel loss is at most

    min_l loss(R_l N E_l) + 2 Eta + 2 v_eval + v_sel.           (10)

Composing the actual acquired V_eff inverse adds its separately certified complete error zeta, once, together with bad-certificate probability and the actual whole-process implementation allowances. The reference comparator uses the SAME library and exact canonical inverse. Source outcomes, finite code-evaluation arithmetic, library size, hardware routing, encoder/decoder faults and storage remain charged. This does not prove an advantage over an equally informed adaptive conventional learner, which may use this exact procedure.

For a single unknown logical payload introduced after acceptance, the reduced canonical-channel score is meaningful under the declared product-input/reference contract. Complete retained-memory outputs and arbitrary later coherent feedback remain governed by the independent inverse-comparison theorem, NOT by this product model or (10). Repeated-use performance needs its own full source/interface premises. No environment model is inferred from one-use channel parameters.

## 7. Remaining scientific obligation

The scoped addition is an acquired local residual-channel description plus finite same-record selection guarantee. It removes a free-noise-model assumption for supplied candidate-code evaluation. It leaves optimal code discovery, non-product/variable-factor noise, broad model membership, useful total calibration budgets and complete hardware qualification open. Exact algebraic or known-matrix fixtures are not sampled-source experiments, measurements, or a practical advantage.
