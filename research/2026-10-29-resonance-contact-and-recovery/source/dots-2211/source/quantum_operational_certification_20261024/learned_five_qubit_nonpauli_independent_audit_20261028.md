# Independent receiving: acquired frame followed by standard five-qubit recovery

28 October2026. Reviewer `producer-workspace/review_effect_only_acquisition`. PASS at the receipt-bound source. This is a complete LOGICAL-channel bridge conditional on an actually acquired inverse, not a new code or complete-bath recovery theorem.

## Actual code operation and first-order cancellation

The four listed stabilizers commute and the projector gives the standard two-dimensional code. The two stated columns are orthonormal. The16 I/single-site-Pauli images form mutually orthogonal two-dimensional syndrome sectors exhausting the32-dimensional physical space. Consequently R_a=Cdagger F_a dagger are genuine CPTP recovery Kraus operators, and stacking them gives an explicit unitary syndrome/logical-coordinate map. Its inverse with initialized syndrome ancillas implements encoding. The source does not hide an unknown recovery oracle inside this step.

Every Kraus operator of an arbitrary one-site channel expands in that site's I,X,Y,Z basis. Syndrome orthogonality removes cross coefficients and sends each branch to a scalar multiple of the logical identity; TP normalizes their squared weights. This proves exact correction on arbitrary logical/reference entanglement, not just computational basis states. The code and this mechanism are standard.

Expanding the actual PRODUCT of E_i=id+Delta_i is an exact multilinear identity. Recovery kills every first-order R Delta_i C term, while diamond submultiplicativity bounds each remaining subset by product_i(2p_i). Half the sum gives exactly the displayed product expression and coefficients20,40,40,16 for equal p. The same proof works for nonunital and coherent local channels. It is not a probability-of-Pauli-errors argument. The learned inverse's complete-norm discrepancy adds zeta by pre/post CPTP contraction; no fidelity-to-diamond shortcut occurs.

For amplitude damping, ||K0-I||=1-sqrt(1-gamma) and the jump CP map has diamond norm gamma. The two K0 difference terms plus jump give the conservative half-distance bound stated. Unitary rotation of its axis preserves the norm. This does not claim to compute the exact AD diamond distance.

## Acquisition, resources and scope

Unknown-axis AD has an SPD Bloch contraction, so the stated acquired-algebra interface can target the original fixed mixer. In the more general polar convention, both the inverse target and service residual channels must use the same canonical frame. An unidentifiable microscopic rotation is not recovered by convention.

The inverse must be constructed from actual operator certificates and the physical three-reflection circuit. Its15 controlled blocks, five mixed receiver ancillas, physical output disposal and subsequent syndrome decoder are part of the operation. Demanding zeta=O(p^2) under an inverse-square ordinary acquisition law gives the conservative p^-4 sample dependence; conditioning and finite optimization may dominate. The bad-certificate probability and complete nonlocal encoder/decoder/control errors must also be O(p^2), otherwise nominal quadratic noise suppression is masked. No noiseless control assumption is converted into an implementation claim.

The product-channel premise is for the actual service block initially independent of its environment. Bath and syndrome are discarded in the guarantee. Reusing the source with retained bath needs the explicitly stated process/initialization contract; a reduced product channel is not a product complete-memory instrument. The correlated XXXXX counterexample correctly defeats an inference from small single-site marginals alone. A latent mixture can only be averaged componentwise when its component promises hold. Calibration failure is charged once under same-abort comparison; accepted conditional risk needs its denominator.

## Independent direct checks and source replay

`five_qubit_patch_bridge_independent_check_20261028.py` independently constructs the code/decoder and verifies all256 Knill--Laflamme pairs and decoder TP EXACTLY in dyadic matrix arithmetic. Five non-Pauli single-site AD cases are corrected to floating precision. Three actual product AD channel cases obey the complete-logical Choi upper diagnostic and analytic expansion bound. These checks do not rely on a fitted unitary simplification.

I also copied and replayed the author's complete learned-receiver program separately. All223 floating values across that program and the interleaved companion, plus every nonfloat field, matched exactly. The author curve really propagates the noisy contrasts through whitening/signs and mixed-ancilla controlled-reflection extraction before code decoding. Its bounded deterministic perturbations are NOT Born samples, its guards are not interval-certified, and its numerical Choi bounds are diagnostic. Those limitations remain explicit.

## Conventional baseline

I read the primary standard-code paper's correction/syndrome discussion and Knill--Laflamme's Theorems3.1--3.5/recovery section: https://arxiv.org/html/quant-ph/9602019v1 and https://arxiv.org/html/quant-ph/9604034v1 . These establish the conventional foundation, not novelty of this bridge. The strongest equally informed conventional implementation is this same standard code with the same acquired inverse and identical costs/performance. An uncalibrated no-inverse curve is only a missing-frame diagnostic. No threshold, superiority, practical resource advantage or civilisation-scale completion is received.
