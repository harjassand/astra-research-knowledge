# Certified qubit-flag projection inside a retained-memory receiver

2026-10-29 UTC. This is an implementation bridge for the existing compact-prequential theorem, not a new quantum advantage or an arbitrary-dimensional solver theorem. All v1 sources and old negative benchmarks remain intact. Independent review of new v2 outputs is separately recorded when completed.

## What changed

The formerly diagnostic floating projection now has a saved, independently replayable exact rational primal/dual certificate at every update. This closes the finite projection contract on the executed qubit-flag runs. It does not certify floating physical preparation, measurement, gate synthesis, or EXP3 arithmetic.

* `run_memory_v2.py 4096`: 12,288 actual conditional-memory-source calls, 12,288 certificates. Maximum exact upper gap represented numerically is 4.419753742770756e-15, below xi=1/4294967296. Three complete seed banks are saved separately as gzip JSON plus NPY records. The earlier interrupted v1 log had two finished-seed messages but no retained N4096 bank; it is not evidence of a completed run. The v2 run redid all seeds and saves each completed seed.
* Learned average scores .39705, .38969, .38370 still lose to identity .44759. These are conditional-path numerical diagnostics, not confidence intervals or a claim about the expected optimal occupation. The theorem's r=2,N=4096 excess-loss term is 4.5/64=.0703125, before additional physical implementation debit. A realized sample-path difference does not verify that expected guarantee.
* `run_certified_meta_v2.py 1024`: unchanged high-recoverability source, actual mixed shadow/evaluation measurement occupation, rational compressed learner updates, 733 certificates over3,072 calls. Largest gap3.34113e-14. Learner averages .79546/.80635/.80437, meta .59279/.57915/.61099, identity .50801/.49233/.51646. The informed fixed-X receiver score .989799972232867 is available only as a source-informed diagnostic and lower bound on the oracle, not granted to the learner. Source/control and EXP3 remain floating simulations. No statistical or practical advantage is established.
* `certified_projection_v2.py` additionally routes very large unseen multiplicity through a limiting dual proposal without converting K to a float. Interior stationarity polishing improves the proposal. The public interface now certifies a nontrivial test family at K=2^40 through2^2048 with xi=1e-12 and gap<5.26e-17. Two single-effect tests return exact gap zero. This is verified coverage of those inputs, not proof of arbitrary-input termination or polynomial running time.

## Exact certificate derivation

Write each Hermitian qubit matrix H=aI+xX+yY+zZ as a four-vector h. Then Tr(HG)=2 h.g and H>=0 iff a>=0 and a^2>=x^2+y^2+z^2. All these tests are rational.

For rational centers Y_i and weights w_i>0 minimize P(E)=sum_i w_i ||E_i-Y_i||_F^2 subject to E_i>=0,sum_i E_i=I. Observed labels have w_i=1; the common unseen aggregate has w_i=1/K. For any Hermitian multiplier L, completion of squares and spectral minimization over the PSD cone give

D(L)=-Tr L+sum_i w_i ||Y_i||_F^2-sum_i Tr[(2w_iY_i-L)_+^2]/(4w_i).

Weak duality gives D(L)<=P_min for every L, without any requirement that an optimizer converged. For V=aI+v.sigma, bound ||v|| between rational lo,hi using integer-square-root bracketing. Upper eigenvalue bounds a+hi and a-lo give an upper bound for the sum of positive-eigenvalue squares and hence a rigorous LOWER dual bound. Interval precision grows with log2 K; no coefficient1/w is dropped.

Primal repair rounds proposal coefficients to dyadics, shifts each scalar component upward by its exact rational spectral-radius upper bound as needed, and divides all effects by c=max(1,lambda_max_upper(sum H_i)). The exact residual I-sum H_i/c is PSD and is added to the final effect. Every returned effect is exactly PSD and their sum is exactly I. A successful result satisfies 0<=P(E)-D_lower(L)<=xi, so P(E)-P_min<=xi. Numerical iteration counts or optimizer statuses are never acceptance evidence.

The singleton case has unique E=I and multiplier L=2w(Y-I), yielding zero gap exactly. In the huge-K proposal only, L is shifted into the PSD cone to prevent a tiny negative dual eigenvalue being multiplied by K. The resulting debit is included in the exact gap. Failure to meet xi raises an exception; no silent tolerance relaxation or successful-status fallback is allowed. Proposal convergence on arbitrary inputs remains unproved.

## Acquisition and scaling boundaries

The learner receives only the actually observed Pauli label and flag-shadow record (plus public horizon/dimensions); it is not given source matrices or the environment state. The source simulator retains and conditions its memory after the actual chosen measurement. Source matrices appear only in simulation and diagnostic scoring. Rational primal repair resets denominators each update rather than recursively multiplying prior repair factors. Certificate integer sizes still depend on input bit length and log K.

The full16-label POVM expansion in the small two-data-qubit simulator is diagnostic execution, not a scalable implementation of an exponentially large catalogue. The rational learner stores observed effects plus one aggregate. Existing randomized pruning and terminal-resource teleportation manuscripts govern scalable receiver realization; this run does not itself execute their finite-control compiler. The private-terminal score in the pure-probe driver is evaluated on the corresponding prefix of an all-probe diagnostic trajectory; it is not a hardware teleportation experiment.

## Reproduction and dependencies

Python with NumPy/SciPy. Run the driver from any directory; outputs go alongside it. N4096 driver uses the unchanged v1 certificate kernel; meta and public huge-K tests use v2. Source imports are explicit dependencies on `compact_prequential_flag_recovery_20261028/quantum_memory_fixture_v1.py`; the new meta driver retains source definitions from `baseline_protected_flag_recovery_20261028/high_oracle_meta_fixture_v1.py`. Governing theorem: compact-prequential CONSTRUCTION_v1 and subsequent accepted correction/pruning/terminal addenda. Governing meta analysis: baseline-protected META_SELECTOR_v1 and scope corrections. No accepted theorem is superseded; this replaces the unexecuted solver-contract status only for the recorded qubit instances.

### Follow-on review and v3 boundary repair

Independent review recovered all12,288 N4096 projection chains and all733 meta chains. The new meta measurement records are **exactly identical** to the original floating fixture: this is a certified same-seed replay of that benchmark, not independent new acquisition or statistical replication. Source/instrument replay discrepancy was below5.6e-16. See independent_audit/REVIEW_v2.md.

Reviewer stress tests found two simple underloaded/boundary huge-K inputs for which v2 correctly refused a certificate (proposal gaps about1.8e-8 and1.1e-8). These failures are retained. New `certified_projection_v3.py` first recognizes exactly feasible centers, then tries the exact seen-PSD/residual construction with dual zero for underloaded huge-K centers; only the exact gap test can accept either. Both formerly failed cases now pass xi1e-12. The underloaded case has a strictly positive rational gap of order2^-2048; its diagnostic float gap underflows to0, so the stored exact fraction, not the float display, governs. The already-feasible boundary case has exactly zero gap. No arbitrary-input convergence theorem follows. v3 was not used to regenerate or replace either v2 benchmark.

### v4 finite weighted dual and retained failure cases

Moderate K also exposed ill-conditioning: v2's per-label Dykstra exhausted its cap at K=2^20,2^30,2^39 on the original overload family. `certified_projection_v4.py` changes mechanism: first the exact all-positive affine projection, then the seen-only proposal checked against the **finite** objective, then a four-real-variable finite-weighted dual semismooth Newton proposal using the divided-difference derivative of the positive matrix part. The exact rational acceptance kernel is unchanged. The original family now certifies from K=1 through2^2048 at xi1e-12. A predeclared60-case rational indefinite-center stress passes58 and refuses2; both failures and inputs are retained in check_finite_dual_v4.json. Thus generic successful termination remains unproved and is explicitly NOT claimed. Independent v4 review is still required; earlier receipts do not cover this new proposal or the finite meta arithmetic.
