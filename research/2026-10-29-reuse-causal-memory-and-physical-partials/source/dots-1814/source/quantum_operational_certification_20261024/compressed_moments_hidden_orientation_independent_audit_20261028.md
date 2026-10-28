# Independent receiving: compressed moments and physical orientation acquisition

28 October 2026. **PASS for the specified stationary flagged family and finite acquisition interface.**

Reviewed source: `compressed_moments_hidden_orientation_bridge_20261028.md`, SHA-256 `86bedf2c311caa38e8066d99e51b240b056734f67381d86d7d53a11e16ed7502`. The reviewer did not edit the source. Before receiving, the author added the requested explicit scope: integer N>=1 calibration calls precede a fresh independent payload/reference, with exactly one payload source call and no payload-dependent cross-use encoding. The original source remains preserved separately.

## 1. Primary-source interface and attribution

I independently inspected Chowdhury's [arXiv:2610.33607v1](https://arxiv.org/html/2610.33607v1), especially Sections 3.4, 5.1 and 7.5. The paper assumes a known generator and encoding. Section 3.4 expresses boundary data through compressed moments; Section 5.1's finite-angle channel uses the physical images `P_a V`, not just their compressed overlaps. Section 7.5 itself discusses the significance of optical-axis calibration. The reviewed construction changes the supplied physical-orientation information. It neither contradicts those results nor establishes priority over them.

The example's Krylov chain closes because H^2=I; it has no harmful first boundary. A nondegenerate-boundary coefficient theorem is not being applied at a nonexistent boundary. The relevant conclusion is an operation-identifiability distinction: an informed zero loss does not supply an unknown physical inverse. Conventional quaternion fitting is credited through the received on-site construction and its Horn attribution. No new generic Krylov theorem, new rotation-fitting principle, or historical-novelty claim is received.

## 2. All moments and the exact physical channel

The block matrix H_W is Hermitian and squares to identity for every unitary W. Its even powers are I and odd powers are H_W. Compression by `V=(I,0)^T` therefore gives I at every even degree and zero at every odd degree. This establishes equality of the entire compressed-moment sequence, not merely the finite degrees tested by code.

Moreover `exp(-i xi theta H)=cos(theta)I-i xi sin(theta)H`. Averaging xi=+1,-1 cancels the cross terms exactly, yielding the two orthogonal flag branches in equation (1), with p=sin^2(theta). The channel remains stationary and reset across the declared calls. The informed receiver reads the flag and applies I or W-dagger; it recovers every input, including entanglement with a reference. The true full-CPTP oracle loss is consequently zero.

Compressed spectral weights are also independent of W: `V^dagger P_± V=I/2`. The physical images `P_± V=(V±H_W V)/2` do depend on W. This is exactly where orientation is absent from the specified moment-only information.

## 3. Moment-only minimax statement covers every CPTP decoder

Let D be any common CPTP map from the known flag/logical output to the logical register, with arbitrary fixed ancillas. Restricting its input to flag f defines a CPTP map D_f. Since the source output is block diagonal in the flag, off-diagonal decoder action cannot improve the objective; no assumption that the general decoder itself first measures the flag is needed.

Average W over the d^2 Weyl unitaries. Their conjugation average sends every input operator A to `(Tr A)I/d`. After D_1 this is a replacement channel with some state sigma. Its normalized Choi state is `I_ref/d tensor sigma`, whose Bell overlap is exactly 1/d^2. The flag0 contribution is at most one. Hence the averaged loss, and therefore the worst-W loss, is at least `p(1-1/d^2)` for every full CPTP decoder.

Passing flag0 unchanged and replacing flag1 by a fixed state attains this uniformly in W. The exact minimax equality is therefore correct, including p=0 and p=1. This is a no-additional-orientation-data statement, not a lower bound against the later paid calibration procedure.

## 4. Ordinary estimator, risk transfer, and the p=0 endpoint

For uniformly chosen independent input axis j, input sign s, and output measurement axis a, the flag1 outcome has conditional mean `E[b|f=1,j,s,a]=s R_aj`. Since its probability is p independent of the input, the matrix observation `9 f s b e_a e_j^T` has mean pR. Its squared Frobenius norm is exactly 81f. Therefore its second moment is 81p and its centered variance is `81p-3p^2`.

Independence of the N source calls gives the stated exact matrix-mean MSE divided by N. No observed leakage count is substituted for its expectation and no successful-trial stopping rule is used. The estimator never divides by p or by an observed rare count.

For a delta-inexact proper-rotation maximizer, comparison with the true R yields

    (p/2)t^2 <= t ||E||_F+delta,

because `3-<Rhat,R>=t^2/2`. Young's inequality gives `t||E||<=p t^2/4+||E||^2/p`, proving the manuscript's squared-error bound. The composed qubit unitary's entanglement loss is exactly t^2/8, irrespective of the SU(2) representative's global sign. Multiplication by the actual leakage probability p then proves

    E ell <= (81-3p)/(2N)+delta/2 <=81/(2N)+delta/2.

With delta=1/N this is at most 41/N. Independently, the physical controlled-unitary decoder has loss at most p on every record. These two unconditional bounds give `E ell<=min(p,41/N)`. When p=0 the source and deployed receiver are exactly identity on the always-occurring flag0 branch; no limiting division is needed.

The expectation is over actual ideal-interface training outcomes. It is not a posterior guarantee for each exposed record, a confidence certificate for p, or a high-probability rotation-estimation guarantee. Very inaccurate estimates on the rare branch remain compatible with the result.

## 5. The imported finite fit really remains physical and gap-free

I read Section 5 of `ordinary_onsite_two_axis_frozen_memory_recovery_20261028.md` at SHA `7df4d169cc544b79456e7410da7ac3ec991482311a0d3831569efc573455dd53`, its statistics audit/receipt, and Section 2 of the rational Jacobi primitive `ordinary_one_sided_effect_finite_positive_cost_rounding_20261028.md` at SHA `8b5859b44e398d5d97d5b14580041bd9232b9fe59188a9c090634d6a4dbab0b6`. All fourteen bindings in the on-site receipt were reverified. Only the known-matrix fitting primitive is imported, not that theorem's source-memory or on-site-noise promises.

Here every record has `||Mhat||_F<=9`. For the standard real quaternion K(M), `u^T K(M)u=<R(u),M>` on the unit sphere, so

    ||K(Mhat)||_op<=sqrt(3)||Mhat||_F<=9sqrt(3)<16.

The explicit replacement for the old normalization is

    A=K/64+I_4/4,    eta=delta/32.

A is positive with operator norm below 1/2. Apply the received real exactly rational Jacobi procedure so that the off-diagonal Frobenius residual of A is at most eta/4. Unscaling gives a K residual at most `64eta/4=delta/2`. Select the largest diagonal label of `Q^T KQ`; the corresponding exactly rational unit column q has Rayleigh deficit at most delta/2 and thus satisfies the required delta objective bound.

The associated `q0 I-i(qx X+qy Y+qz Z)` is exactly unitary with determinant one. Zero data, repeated maximal eigenvalues and all statistically bad records remain physical. No empirical eigenvalue separation, source eigengap, O(3) reflection, or ideal irrational eigenvector is assumed. Matrix size is fixed at four, rational count entries have O(log N) bits, and the primitive uses polynomially many arithmetic/precision bits in log N. Its runtime has no hidden 1/p factor.

Finite gate synthesis and imperfect preparation/readout are separate from this exactly physical reference control. The source explicitly allows a whole-experiment discrepancy nu; its implemented expected-loss conclusion is therefore `min(p,41/N)+nu`, not the unqualified ideal bound under arbitrary control errors. In an unhalved complete-norm convention, even nu/2 would suffice for a single Bell probability, so the stated debit nu is conservative.

The whole process must include the classical axis sampler as well. A bounded B-bit approximate sampler for a uniform three-valued axis can make each total-variation error O(2^-B); choose B=O(log(N/nu)) and debit the full N-call discrepancy, with no unbounded rejection loop. All N inputs, both axis choices, flags, readouts, stored counts, the finite fit, the controlled inverse, and one payload are paid. None of these precision requirements changes the N source-call cap or introduces 1/p.

## 6. Lower bound survives coherent and adaptive calibration

This requires an all-strategy argument, not merely checking fidelity for the identity decoder. Restrict the hidden W to I and X with equal prior. In each channel call, the flag0 CP branch is the same map for both worlds and has probability 1-p independent of every input, including an entangled input. For an arbitrary causal calibration strategy with quantum memory and adaptive controls, expand its comb over the source branch labels. The all-zero branch is a common subnormalized strategy output of trace `(1-p)^N` in both worlds. This follows inductively because each inserted flag0 map is the same scalar multiple of the identity embedding. The labels need not be exposed or measured by the learner for this mathematical CP-branch decomposition.

On this branch, the retained program, classical data and any ancillas are independent of W. The fresh unknown payload/reference is independent of that calibration/program by the clarified protocol. Incorporating the common program into the final CPTP map therefore produces one common effective decoder for the payload.

On the payload leakage branch, averaging W=I,X gives complete dephasing in the X basis. Its Bell Choi state is

    (|++><++|+|--><--|)/2.

It is separable, and every local CPTP decoder with a payload-independent program preserves separability across the reference/output cut. Every separable two-qubit state has Bell overlap at most 1/2. Thus even the optimal full CPTP leakage decoder has fidelity at most 1/2. The flag0 service fidelity is at most one. Nonnegative loss on all other calibration histories now yields the Bayesian bound

    E ell >= (p/2)(1-p)^N.

Taking the worst of I,X is at least their prior average, so this proves a minimax lower bound. It remains valid if p and all compressed moments are supplied. It does not permit generator queries, coherent access to a dilation/environment, extra payload-dependent source calls, a protected payload bypass, or cross-use payload coding.

For `p=1/(N+1)`, use `(1+1/N)^N<=sum_(j>=0)1/j!<3`. The lower bound is greater than `1/[6(N+1)]>=1/(12N)` for N>=1. Thus the claimed worst-p Omega(1/N) order follows with an explicit absolute constant. This is an expected Bell-risk lower bound in the declared calibration-then-one-use interface, not a general quantum communication lower bound.

## 7. Independent evidence and receiving scope

`compressed_moments_hidden_orientation_independent_check_20261028.py/.json/.log` were written without importing or executing the author's check code. They verify exact moment identities, random-sign channel identities, complete Born-law expectations, unitary/Bloch loss identities, modified-scale rational physical fitting, curvature budgets, and small retained-entangled-probe/adaptive no-leak maps. General-d Weyl matrix units are also checked deterministically in floating arithmetic. All-round all-CPTP conclusions rest on the analytic arguments above, not those finite fixtures.

The independent evidence contains zero RNG draws, source calls or sampled trial outcomes. Four exact rational fits are actually executed: floating angles propose rational two-plane factors, while their unitarity, energy recurrence, final backward residual and physical quaternion certificates are checked exactly. Production gate synthesis, the source-acquisition protocol and hardware are not executed.

The separately authored `hidden_orientation_ordinary_pilot_20261028.py/.json` was inspected only for evidence-class clarity. It reports 768 numerical runs and 688,128 individually RNG-simulated calls using binary64 SVD. It is NOT this receipt's independent evidence, not a rational-Jacobi execution, and not physical-source data. Its empirical performance is excluded from this mathematical receiving.

**Received:** exact complete-moment orientation nonidentifiability and full-CPTP minimax loss; fixed-N ordinary qubit acquisition with expected reference loss `min(p,41/N)` plus the explicit finite-implementation debit; and the coherent/adaptive calibration lower bound for the clarified fresh one-payload interface. The received result is narrow, conventional-control, stationary and genuinely flagged. Unknown flags, retained-memory noise, generic unflagged geometry, practical performance, historical priority and external peer review are not established. No unresolved correction remains.
