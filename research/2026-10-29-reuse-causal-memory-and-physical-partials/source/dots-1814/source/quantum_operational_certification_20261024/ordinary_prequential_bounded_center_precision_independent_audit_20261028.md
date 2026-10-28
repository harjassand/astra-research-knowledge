# Independent audit: bounded centers, original log-det, and finite precision

28 October 2026. Reviewer: `producer-workspace/review_bounded_center_precision`.

**PASS / receive as a finite-precision refinement of the construction theorem, not a learning-performance improvement.** Reviewed final candidate SHA-256: `35efeef37e8ae0ed38b0b8d6a049cd98c15c8143b81e79565921fdfdf1333f4c`. The intermediate clarification version was `ab4b0c6e17c3595486fcfe4550d80f865703629a3a7d76e9bbb9226d2bfb138b`, preserved as `ordinary_prequential_bounded_center_precision_20261028_pre_repair_symbol.md`; its only subsequent change distinguished repair rho from learner delta. The original submitted version was `cd891307be95358ee5102394c259c2c30717813d084e7d75d03f2f6ff04e2ef5`, preserved as `ordinary_prequential_bounded_center_precision_20261028_initial.md`. The received small-loss source remains SHA `6edb6a3af1118947c1a864113a24d77eef437386eafb7d8694a4aa651dc8d1dc`.

No unresolved load-bearing mathematical objection remains. The original proposal survived review; the owner clarified its changed occupation law, unnormalized repair convention, fixed post-repair denominator family, and slack in the dual acceptance threshold. These are important implementation/scope clarifications, not a changed learning rate or claimed positive pilot result. This auditor did not edit the candidate, base theorem, or pilot files.

## 1. The constraint and the actual played domain

The new center set is precisely the set of normalized TP Choi matrices satisfying `C>=mu I`, because `mu=zeta/k` and `Z=(C-mu I)/(1-zeta)` then has partial trace `I_d/d`. The old shrunk comparator `(1-zeta)C_D+zeta C0` is already in this set. No extra comparator debit is needed.

The regularizer is the original `phi=-log det C`, smooth even at the **center-domain** boundary. It is not `-log det(C-mu I)`. The center constraint need not contain the Dikin plays. The exact whitening certificate implies `Cplay>=C/2>=mu I/2`, so they remain physically TP/positive in the original Choi set. Their two-sign average is exactly C. The acquired-bit unbiasedness, inverse-dual identity and loss-weighted variance proof are therefore unchanged.

Changing the center update changes the actual retained-memory occupation law. The result has the same comparator **definition** and source-cap/risk **form**, not the same numerical `R_N` as the old learner or pilot. The final candidate states this explicitly.

## 2. Constrained minimizer and the local-radius bound

The constrained objective is continuous on a compact set and strictly convex; it has a unique minimizer `x*`. Write `x` for the old center, `h=x*-x`, and `p*=eta g+grad phi(x*)-grad phi(x)`. Optimality gives

`<p*,x*-u><=0` for all feasible u.

Putting `u=x` yields

`<grad phi(x*)-grad phi(x),h><=-eta<g,h><=a r`,

where `r=||h||_H` and `a=eta||g||_(H^-1)`. If the eigenvalues of `C(x)^(-1/2)(C(x*)-C(x))C(x)^(-1/2)` are `x_b`, then each is greater than -1 and

`<grad phi(x*)-grad phi(x),h>=sum_b x_b^2/(1+x_b)>=r^2/(1+r)`.

The last inequality follows from `x_b<=r`, not from an unconstrained stationarity equation. Thus either r=0 or `r<=a/(1-a)`. The received estimate gives `a<=sqrt(8)/(64D)<1/16`; hence `r<1/15`. This remains valid when the minimizer is on the center floor and its tangent gradient is nonzero.

For a returned x', let `p'=eta g+grad phi(x')-grad phi(x)`. The exact three-point identity is

`eta<g,x'-u>=B(u,x)-B(u,x')-B(x',x)+<p',x'-u>`.

An upper VI certificate at most delta therefore supplies exactly the old `+delta` regret debit. The radius guard supplies the same `B(x',x)>=r^2/3`, and every remaining first-order, second-moment, shrink and terminal-transfer step goes through. The favorable normal-cone sign has not been discarded or reversed.

## 3. Objective gap implies a uniform VI certificate

For trace-one centers, `C<=I` and `C>=mu I`. The Pauli isometry gives

`k I<=H(C)<=k mu^-2 I`.

Also `||grad phi||_2<=k/mu` and `eta||g||_2<=sqrt(k)a/mu`, so `||grad f||_2<=3k/mu`. Its Hessian bound is `L=k/mu^2`. The center-coordinate diameter is at most one.

For a feasible x' with objective gap xi, constrained strong convexity gives `h=||x'-x*||_2<=sqrt(2xi/k)`: the linear term at x* is nonnegative, not assumed zero. For every feasible u,

`<grad f(x'),x'-u>`
`= <grad f(x')-grad f(x*),x'-u> + <grad f(x*),x'-x*> + <grad f(x*),x*-u>`
`<= (L+3k/mu)h <=4 sqrt(2k xi)/mu^2`.

Thus the proposed `xi<=delta^2 mu^4/(512k)` gives VI residual at most `delta/4`. The second bound `xi<=mu^2/512` gives local distance from the exact minimizer at most `sqrt(2xi)/mu<=1/16`. Adding `1/15` remains below 1/2 with considerable slack. These bounds correctly account for a nonzero gradient at a constrained optimum.

## 4. Finite weak optimization and exact repair: explicit closure

The known normalized Z-body has center `I_k/k`, affine-coordinate outer radius at most one, and, for example, a rational inner radius `1/(2k^2)`. This follows from `||Delta Z||_op<=sqrt(k)||Delta theta||_2`. Its separation is a known rational Hermitian PSD test. The smooth objective has a known Lipschitz bound, range bound and Hessian bound whose logarithms are polynomial in the declared parameter bit lengths. Thus the already imported rational weak-convex-optimization machinery applies with a polynomial **bit-operation** cap; a gradient-descent iteration bound proportional to an inverse spectral gap is neither needed nor being claimed.

A fully specified way to interpret the small feasibility/rounding slack is as follows. Denote the repair residual by **rho**, to distinguish it from the learner's fixed delta. Set

`0<rho<=xi mu/(1000k)`.

Use the received unnormalized variable `K=dZ`, require pre-rounding eigenvalue/TP residuals at most rho/2, and round Hermitian real/imaginary entries on a fixed dyadic mesh at most `rho/(64d)`. The inherited matrix and marginal rounding bounds leave residuals at most rho. Then apply

`Khat=Ktilde+(I_2/2) tensor (I_d-Tr_out Ktilde)`,
`Kphys=(Khat+2rho I_k)/(1+4rho)`,
`Zphys=Kphys/d`, and `Cphys=mu I_k+(1-zeta)Zphys`.

The imported exact proof gives TP, positive Zphys and `||Zphys-Ktilde/d||_F<=9rho`; hence Cphys is certainly in the new center domain.

For completeness, small non-TP solver residuals do not invalidate the objective estimate. Extend the affine objective to positive Hermitian C by its explicit formula

`F(C)=eta Tr(GC)-log det C+Tr(C_t^-1 C)+constant`,
`G=(1/k)sum_a g_a E_a`.

This equals the intended objective on the TP affine space. The solver, rounded point and repair segment can be kept above `mu I/2`, since `rho/d<=mu/2`. There

`||grad_C F||_F <= (3sqrt(k)+1/16)/mu <=4sqrt(k)/mu`.

The repair changes F by at most `36sqrt(k)rho/mu <=36xi/(1000sqrt(k))<xi/32`. The same grid has more than sufficient rounding slack. An initial objective gap xi/4, and even an additional xi/4 known-center allowance, therefore leaves final gap below xi. This makes the note's finite repair prescription explicit without changing its algorithm or constants.

The final center need not be dyadic: it belongs to a fixed rational denominator family obtained from the dyadic mesh, d, mu, zeta and `(1+4rho)^-1`. These parameters do not inherit the previous iterate's denominator. Therefore exact inverses, Hessian entries and the next fixed-grid rounding do not create recursive denominator growth.

Positive rational determinants and rational matrix inverses provide the objective/gradient oracle. A scalar logarithm can, if desired, be certified entirely by rational arithmetic: scale its argument to `[1,2]`, use `log x=2 sum_{j>=0} z^(2j+1)/(2j+1)` with `z=(x-1)/(x+1)` and `|z|<=1/3`, and bound the geometric tail; compute log 2 the same way. The number of terms is polynomial in requested accuracy bits and input bits. This is not an unbounded numerical accuracy search.

## 5. Finite rational linear-SDP upper certificate

For rational `p=grad f(x')`, set `B=(1/k)sum p_a E_a`. Each E_a is traceless, so for C in the affine set `p·theta=Tr(BC)`. The residual is

`R=p·theta'-(1-zeta) min_{Z>=0, Tr_out Z=I_d/d} Tr(BZ)`.

The corresponding dual maximizes `Tr(Y)/d` subject to `B-I_2 tensor Y>=0`. Therefore every rational dual-feasible Y gives the **exact rational upper certificate**

`U=p·theta'-(1-zeta)Tr(Y)/d >= R`.

This is a genuine upper certificate, not a primal objective estimate of the wrong sign. The candidate accepts `U<=delta`. If the true residual is at most delta/4 and the dual objective error contributes at most delta/4, it obtains `U<=delta/2`, so there is strict acceptance slack.

This secondary SDP has bounded finite conditioning. Choose a rational `L>=max(1,||B||_op)`. The primal has the known strictly positive center; `Y0=-(L+1)I` is strictly dual feasible with matrix slack at least I. Dual optimal attainment follows from this strictly feasible, bounded primal problem. For any optimal Y, feasibility gives `lambda_max(Y)<=L`; comparison with feasible `Y=-LI` gives `Tr(Y)>=-dL`, hence `lambda_min(Y)>=-(2d-1)L`. A box `-M I<=Y<=M I`, `M=4d(L+1)`, therefore contains an optimum and the strict center with explicit margins.

The same bounded weak optimization machinery yields a rational approximate dual witness. Round it on a prescribed finite mesh and subtract the certified PSD residual times I; this makes `B-I tensor Y` exactly PSD while decreasing `Tr(Y)/d` by only that residual. Choose objective/residual/rounding budgets totaling at most `delta/[4(1-zeta)]`. All bounds have polynomial bit descriptions. Exact rational PSD tests then verify the witness. No unavailable support-function oracle has been inserted into the learner.

## 6. Whitening, bit/control bill, and scope

The old rational Cholesky target `(3/4)H^-1/2` in factor form and its mesh `mu/(128kD)` now use uniform `mu=zeta/k`, rather than the conservative `2^(-(N+2))/k`. The exact interval certificate is unchanged. The **exact rational inverse dual** is retained; separately rounded dual columns would destroy exact unbiasedness. Rational determinant/minor bounds show that matrix inverses of prescribed-bit entries have polynomial bit size in their dimension and entry bits. The uniform Hessian bounds allow the Cholesky/inverse approximation to be found with a finite polynomial precision cap.

Consequently the old artificial O(N)-bit learner conditioning requirement is removed. Per-round classical precision and weak-solve bit complexity are polynomial in d, declared rational input lengths, and logarithms of accuracy parameters. Quantum synthesis across N calls additionally pays `log(N/nu)` accuracy; the total number N of iterations and total classical/control operations remain charged. A fixed-grid theoretical precision cap is not a measured production-solver runtime.

Every probe still requires the general CPTP decoder's paid Kraus/Stinespring construction and dense control. Full source-port privacy, padded preparation/compilation duration, fresh finite random bits, trusted held-payload storage, and the one whole-process implementation allowance remain essential. The base theorem yields one privately timed terminal payload, averaged expected Bell loss and a fixed decoder comparator on this algorithm's own occupation law. Any separately justified broader service protocol must retain its separate authorization and proof. This review does not add high-probability per-record risk, future deployment, resets, a source eigenvalue floor, free dense control, or an advantage over the equally informed conventional learner.

## 7. Independent exact adversarial fixtures and version history

`bounded_center_precision_independent_check_20261028.py` is an independently written SymPy rational test, not a reused author's pilot. It verifies two particularly diagnostic d=2 examples with epsilon=gamma=1, mu=1/64, eta=1/9216 and delta=1/589824.

* At `theta_ZI=15/64`, a valid actual-bit estimator has `eta g_ZI=-1/3`. The unique constrained prox remains at that center with **nonzero** gradient -1/3 but exact VI residual zero. A rational dual witness proves it. Requiring the old tangent gradient residual would incorrectly reject the point.
* Starting instead at `theta_ZI=15/64-2^-20`, the unique constrained prox lands on the floor with gradient `-27992149017/85993903435`. Its exact displacement and VI sign pass. This is not merely a zero-displacement boundary fixture.
* A common rational whitening V, exact inverse-dual identity, full TP and spectral tests pass in both cases. The outward Dikin play has eigenvalue below the center floor but above mu/2; restricting plays to the center set would incorrectly reject this physical action.
* Fixed-dyadic feasible approximations, with objective-gap upper bounds from the proved Lipschitz estimate, retain a nonzero gradient much larger than delta yet have an exact dual-certified VI below delta/4 and exact locality guards.
* A deliberately nonpositive/non-TP rational Ktilde is repaired to exact TP/PSD, with the imported Frobenius bound and center floor checked. A formal three-point identity is checked symbolically. Exact parameter tables exhibit logarithmic precision scaling while the unchanged source horizon grows.

The first source-bound run passed at the original hash. During the owner's clarification edit, the test's hash guard correctly refused a rerun against the changed source. After reviewing both clarification diffs, it was explicitly rebound and rerun at the intermediate and final hashes; all checks passed. The intermediate JSON is also preserved as `bounded_center_precision_independent_check_20261028_pre_repair_symbol.json`. The initial JSON is preserved as `bounded_center_precision_independent_check_20261028_initial.json`. Its illustrative old-floor field recorded the power-of-two denominator **exponent** but was named bit length; the final output corrects that off-by-one label/value. This did not affect any mathematical check or algorithm claim.

No generic ellipsoid implementation, sampled acquisition, new trajectory, elementary gate execution or hardware experiment was run. These deterministic exact fixtures support, but do not replace, the universal arguments above.

The adverse pilot is unchanged. Its governing `FINDINGS.md` remains SHA `54c88de6bda4384ba6720f00e17faa59087de78099b4f76416c3f305f5e6a24a`; `ANALYSIS.json` remains SHA `8307d9d94b23ffb82977e0ca812777953e9ad76a067caba79ae89fd18656075e`. The recorded N512 bandit played-policy loss remains approximately 0.749659 versus 0.13450 for the independently seeded ordinary comparator on its own occupation. The new precision theorem does not turn that negative learning/control result into positive evidence.
