# Growing-selector active effect acquisition: full statistics audit

28 October 2026. **PASS**, subject to the explicit physical quadratic Bernoulli interface and received common-algebra family contract. Reviewed final source: `ordinary_growing_selector_active_effect_acquisition_20261028.md`, SHA256 `136c4f8a83c81ad28f097f3f35adaf1299b0113d4435e860be119ca0668ed202`.

This is an analytic finite-count construction review, NOT a sampled acquisition experiment. Zero source calls, Bernoulli samples, RNG draws or source-actor reads were used. Prior received sources and pilots remain unchanged. The companion receipt binds the final manuscript, independent controls/envelope reviews, our detailed statistical derivation and deterministic exact checks.

## 1. Canonical implementation and conditional law

The receiver is frozen before this module. Each actual ordinary global test gives one Bernoulli y of unknown mean x^T A x, with real0<=A<=I; its entries are not supplied. The preconditioning matrix at each stage is known from past integer records only. Fresh resets and fresh design labels make batches independent conditional on that PAST history.

The canonical source uses the rational BINOMIAL polynomial in Q=I-B/4, with its predetermined K. Explicit commutation with B is essential and is present. Its bounds CBC<=I, C^(-2)<=2B and ||C||^2<=1/tau give F=CAC<=I on prior-good histories. The source does not incorrectly infer CBC<=I from a noncommuting inequality C<=B^(-1/2). Our separate derivation discusses an optional Newton construction, but neither this source nor the canonical check substitutes that alternative or assumes an exactly synthesized inverse square root.

The even/projective design has the needed second and fourth vector moments. The coordinate branch need not have Haar odd moments, as the manuscript explicitly acknowledges. Sampling signs takes O(m) bits and does not enumerate its exponentially many possible vectors. For the actual normalized query x=Cz/||Cz||, the rational matrix Y=y||Cz||^2 T(z) has EXACT conditional mean F. Finite state-synthesis discrepancy is charged globally, not folded into an unproved exact-mean assertion.

The variance proof is elementary and correct:

    T^2=m^3(m+2)zz^T/4+m^2 I/4,
    ||T||_F^2=L_m=m^3(m+3)/4,
    E||Y-F||_F^2<=L_m/tau.

It uses y^2=y; no scalar expectation oracle or separately resampled matrix entries are introduced.

## 2. Batch confidence, exact medoid, and adaptive union

At r=c/12 and c=gamma/16, a batch of

    n_j=ceil[2304 L_m/(tau_(j-1)c^2)]

has Frobenius error at most r except with probability1/16. For an odd b, the first batch matrix with at least(b+1)/2 neighbors INCLUDING ITSELF at squared distance<=4r^2 exists when a strict majority are good. Its neighborhood intersects the good set, so its Frobenius and operator error are at most3r=c/4.

Every matrix and squared distance is rational. The inclusive comparison and fixed first-index tie rule supply a finite deterministic decision even at equality; no empirical separation margin is assumed. If no qualifying neighborhood exists, the fixed e_1 fallback counts as a failure history, not as rejected training data. The check preserves the counterexample {-r,+r,3r}, target0, where changing <= to < can remove every eligible neighborhood despite a strict good majority.

The sharper elementary stage failure bound is2^(-b-2); the source's weaker2^(-b) is safe. Its smallest odd b>=ceil log2(2J/beta) makes the conditional union over J stages at most beta (in fact at most beta/8 with the sharper bound). This does not assert that learned B matrices are independent. The variance/confidence statement is conditioned on previous good histories; the rational PSD guard maintains valid finite controls and the same worst-case cap even on failed histories.

## 3. Envelope transfer and finite arithmetic interface

From ||Fhat-F||<=c/4 and C^(-2)<=2B, exact reconstruction Ahat=C^(-1)Fhat C^(-1) has Loewner error at most(c/2)B. The explicitly largest dyadic mesh bounds whole-update rounding error by c tau/4<=cB/4. Thus the combined error is at most3cB/4 and adding cB preserves domination.

I checked the stated invariant arithmetic against the canonical constants: a=1/(1-2c), A+tau_j I<=B_j<=aA+2tau_j I; the upper recurrence closes since1+2ca=a and8c+1<=2. Good histories pass the PSD guard B_j<=4I. The separately received main review supplies full finite arithmetic and gap-free final eigensolver details. No noncommuting spectral clipping is used to assert an unknown Loewner inequality.

The final certified Rayleigh slack tau_J/2, combined with the lower A+tau_J I bound, yields p(x)<=a lambda_min(A)+(3/2)tau_J. Since a<=1+gamma/7 and tau_J<=epsilon/8, equation(13)'s additive3epsilon/16 is correct. An unqualified exact eigenvector or fitted spectral gap is not supplied.

## 4. Fixed resource cap and physical randomness

For tau_(j-1)=2^(-(j-1)) and J=ceil log2(8/epsilon),

    sum_j tau_(j-1)^(-1)=2^J-1<16/epsilon.

Therefore the exact training ceiling is bounded by

    b[J+36864L_m/(c^2 epsilon)]
     =b[J+9437184L_m/(gamma^2 epsilon)].

The bJ term retains all ceiling costs. All attempted calls count, including abort histories. The primitive cap does not include the final payload; the end-to-end cap adds it explicitly. L_m<=m^4 gives the claimed polynomial-m, inverse-epsilon rate, not optimality.

The rejection sampler has at most two uniform-integer draws per primitive query and a declared attempt cap. Exhaustion is charged inside the ONE linked operational discrepancy. Accepted labels are exactly uniform under the ideal coupling; no source outcome is rejected or reused. Its displayed bit formula is correctly primitive-only. The final source now explicitly charges extra uniform m-anchor draws, probe signs and global-Clifford sampling in the full acquisition ledger, with the same finite capped-sampler policy and no second unreported discrepancy budget.

All states, source calls, classical rational operations, memory, routing and arbitrary selector amplitude synthesis are paid. A selector uses ceil log2 m qubits but generally O(m) known rotations, not poly(log m) control. The largest-dyadic update mesh gives a finite stored-envelope bit cap; bad batch inputs remain bounded and exact PSD tests have known finite rational input sizes. The source's conventional active-effect tomography interpretation is appropriate; it is not unrestricted circuit-encoder optimization or an algorithmic separation.

## 5. Section7: m-anchor transfer and end-to-end error

The new average is Gbar=(1/m)sum_b G(e_b). Positive scalar quadratics v^dagger G(x)v give G(x)<=mGbar, hence uniform receiver regret is at most m ell0_joint, NOT the former factor4. The stated witness shows this factor can be attained. The operator margin remains a supplied promise. In a fixed-gauge scalar nonnegative-quadratic special case, a perfect encoder implies visibility at least1/m; a merely useful encoder contributes its actual visibility divided bym. Arbitrary matrix-valued gauges do not inherit a positive operator margin merely from a perfect branch.

The final source explicitly defines the NEW rho from this m-anchor Gbar. Both weighted proxy errors and margins refer to that state; an old four-anchor weighted promise is not silently reused. The exact antithetic bank law still gives each individual estimator its correct iid marginal with own-bank-only policies and correlated joint banks. The changed anchor distribution does not add a joint-product assumption.

With eta=epsilon/(4096m q A_geom), the acquired virtual decoder bound yields

    uniform decoder regret <=F_dec+(225/8192)epsilon,
    F_dec=1980m q A_geom tau^2/kappa.

Its approximation floor does not shrink with extra selector samples. Let alpha=2^q/(2^q+1). Passing primitive tolerance alpha*epsilon/8 converts its scalar additive tolerance to at most epsilon/8 in the actual GLOBAL Bell loss, while preserving the relative multiplier1+gamma. The selector uses fresh data after the physical decoder is frozen; its confidence guarantee is valid conditional on any such frozen receiver history.

On combined decoder/selector success,

    ell_selected <=(1+gamma)ell_star+(1+gamma)F_dec
                     +(1+gamma)(225/8192)epsilon+epsilon/8.

The declared decoder failure<=epsilon/16, selector failure<=epsilon/16 and whole-process discrepancy<=epsilon/8 add at most epsilon/4 by bounded loss. Hence

    E ell_selected <=(1+gamma)ell_star+(1+gamma)F_dec
                        +(3/8+225/4096)epsilon,

which is strictly below the manuscript's conservative +epsilon. The factor1+gamma on F_dec is essential and present. All selector-stage quantities must use its passed primitive tolerance alpha*epsilon/8 and confidence epsilon/16, not the unscaled global epsilon.

The full cap correctly REPLACES the old fixed-dimension N_count by T_max, rather than running both, and includes one final payload. The literal source consumes(q+ceil log2 m) input qubits per call and n output qubits, with all selector/global-test controls paid. If a physical tail bound requires width growth with m q A_geom, the full4^w cost must be substituted; no automatic fixed-width linear-m/q claim follows.

## Evidence and final disposition

`growing_selector_whitened_design_statistics_check_20261028.py/.json` performs only exact prescribed algebra: six finite design/moment cases, four canonical BINOMIAL-C cases (including noncommuting A,B), twelve odd-b binomial tails, and the inclusive-threshold witness. It checks exact mean CAC, variance, CBC bounds, backward tail, commutation and the2304 batch size without generating a single Bernoulli record. Finite cases support, not replace, the general derivation.

No remaining statistical or resource-accounting correction is requested for the final source. Any subsequent matrix-Bernstein or staged-gamma improvement is a NEW theorem requiring its own attribution, constants and receipt; it is not part of this frozen m^4/gamma^2 construction.
