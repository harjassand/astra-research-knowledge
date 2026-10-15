# Independent adversarial review: incoming theorems and sharper Cartesian elimination

Date: 2026-10-15. Repository HEAD independently checked at b7cada92d2eb304578be5ed974f1e44b10a89928. This is a scoped same-team reconstruction, not an external proof certificate, formalization, novelty review or physical validation. Initial closure/transport and translation deductions preceded reading other current worker scratch. The sharper Cartesian proof and root forward certificates were then supplied for independent reconstruction.

## 1. Incoming direction results

The mathematical source is `sources/direction/DIRECTION_REDUCTION_LIMITS.md`, read in full. Its principal conclusions survive this review.

* Lines 22–74: fixed-direction scalar convexity and the perspective in ρ=r⁴ follow because normalized gradient differences have rank one. Global quartic convexity along that line yields the μ/3 Bregman remainder. This is conditional amplitude convexity, not joint direction-density convexity or energy positivity.
* Lines 84–238: the explicit density 1−8εcos(x+y), ε=1/100, is positive and normalized. The three numerator averages and denominator bound give a strict trial energy below1. The translation symmetry identifies the two global endpoint values, while the midpoint value is exactly1. An upper competitor bound suffices; the trial need not be the exact global minimizer. The Hessian argument additionally needs the stated positive-carrier elliptic implicit-function branch; the exact trial counterexample does not.
* Lines 243–307: stationarity implies every positive-center radial global comparison by testing with ω_c(s⁴/r_c³−r_c) and using Picone. Conversely, signed compact radial variations at three centers with spanning differences recover each component of the vectorial Euler equation. This concerns the mass-free radial class. It does not prove that a nonglobal stationary point exists in the undecided cone, or supply a global minimum certificate.
* Lines 313–464: the exact affine-boundary translation chart preserves compatibility. Products in W1,4 on the planar Lipschitz extension domain are legitimate. Uniform O(R⁻¹) energy perturbation and scalar coercivity give bounded minimizers; compact uniform convergence handles the lower-order term in weak lower semicontinuity. Their amplitudes are eventually uniformly positive because R dominates the bounded Cartesian component. The source's O(R⁻¹/4) rate is valid but nonsharp.
* Lines 474–512: the scaled exact fourth mass tends to the Cartesian mean. A fixed compact bump of integral1 gives an exact O(R⁻¹) mass correction by the scalar inverse-function/monotonicity argument. Correcting the lower competitor's mean is also necessary; the source does this. The exact trace and chart survive.
* Lines 518–550: a hypothetical negative compatible test is preserved after global amplitude minimization along arbitrarily flat directions. This is a conditional transfer theorem, not a constructed negative gap, hardness theorem or proof that no reduced representation can help.

The remaining actual task is a coupled global inequality for the scalar-eliminated value, or an exact compatible counterexample with a certified rank-one-convex integrand. Neither small phase nor solved scalar minimization alone resolves it.

## 2. Sharper Cartesian theorem: independently reconstructed

Reviewed `workers/cartesian_elimination/PROOF.txt` at SHA256 d3f319390f756259cd545b15cdf691971b0a55b8b90490942da25527cc4da034, principally Sections3–8, with Sections1–2 for assumptions and residual constants. Line numbers below refer to those bytes. The following derivation does not take worker agreement as a premise.

Let X=W0¹,⁴, I₀(a)=∫F([∇a;∇v]), ε=R⁻¹ and Iε the exact translation-chart energy. The rank-one quartic remainder gives

    (DI₀(a)−DI₀(b))[a−b] ≥ (2μ₁/3)∥a−b∥_X⁴.

Uniform W1,4 multiplication and the quartic Taylor polynomial give, on bounded sets,

    Iε=I₀+εJ₁+O(ε²) in C¹,
    J₁(a)=∫F₂([∇a;∇v])·∇[(a−g₁)v].

This proves lines 139–171. The first derivative estimate is the decisive strengthening over a mere energy comparison. Positivity is inactive at all actual small-ε minimizers by the previously proved uniform L∞ bound; therefore DIε(aε)=0 on X. The residual of aε for I₀ is O(ε). Monotonicity gives

    ∥aε−a*∥_X³≤Cε,

and the reverse Bregman inequality gives Cartesian excess O(ε⁴/³). Substituting the Lipschitz J₁ then gives

    mε=I₀(a*)+εJ₁(a*)+O(ε⁴/³).

No quadratic ellipticity, regular optimizer branch or differentiable optimizer map is needed. This reconstructs Section4.

For the exact mass, the normalization in lines 229–247 is essential:

    Cε(a)=L(a−a_ref)+εH₁(a)+O(ε²),
    L(a)=∫a, H₁(a)=(3/2)∫(a²−a_ref²),
    DCε=L+εDH₁+O(ε²).

At a constrained minimizer, DCε(ζ)=1+O(ε) for ∫ζ=1, so the multiplier is legal and bounded. Write DIε(aε)=λεDCε(aε) and DI₀(a*)=λ*L. If t=∥aε−a*∥_X, then |L(aε−a*)|≤Cε and |λε−λ*|≤C(t+ε). Monotonicity gives

    (2μ₁/3)t⁴≤Cεt+Cε²,

which again yields t=O(ε¹/³). The exact constraint gives L(aε−a*)=−εH₁(a*)+O(ε⁴/³), fixing the first value correction as

    J₁(a*)−λ*H₁(a*).

Thus the sign and factor in Section5 are correct for its declared DI₀=λ*L convention. A phase fourth-mass multiplier with a different normalization cannot be substituted.

## 3. Envelope regularity without minimizer differentiation

For fixed mean or no mean, a_v is bounded on bounded v sets by scalar coercivity. The Euler residual of a_z in the v problem is O(∥z−v∥_X) on the appropriate tangent. Fourth monotonicity gives a_v locally Hölder1/3. Quartic derivative growth then makes F₂([∇a_v;∇v]) locally Hölder1/3 in L4/3.

For the value derivative, use a_v as a competitor at v+w for the upper bound, and a_(v+w) as a competitor at v for the lower bound. Taylor expansion only in the second row makes both bounds equal

    ∫F₂([∇a_v;∇v])·∇w+O(∥w∥_X⁴/³).

This proves global Fréchet C¹ and local C1,1/3 exactly as Section6 claims, without taking a derivative of a_v. It does not prove C² or justify a Schur Hessian at every degenerate point.

Precision note for lines350–355: the unqualified reduced-critical ⇒ weak vectorial Euler statement is the **no-mean** version. With a fixed first-component mean, the first Euler equation retains its spatially constant multiplier; only the second Euler equation is zero. This is a wording scope correction, not a failure of the envelope theorem.

## 4. Sharp family and fractional variational development

For v=x(1−x)y(1−y), F_c([ξ;η])=|ξ−cη|⁴+|η|⁴ is convex, μ₁=1, and its exact scalar minimizer is a*=cv. The rescaling a=cv+ε¹/³b gives

    [Iε(a)−E₀−cεB]/ε⁴/³ = H(b)+O(ε²/³),
    H(b)=∫|∇b|⁴+ℓ_v(b),
    ℓ_v(b)=4∫|∇v|²∇v·∇(vb), B=ℓ_v(v)>0.

The expansion follows by writing the transformed first row as ε¹/³∇b−c²ε∇(v²)−cε⁴/³∇(vb), and second row as ∇v+cε∇(v²)+ε⁴/³∇(vb). The displayed remainder is uniform on bounded b sets. H has a unique nonzero minimizer with minH<0. Bounded actual rescaled optimizers come from the general1/3 estimate; weak lower semicontinuity, weak continuity of ℓ_v, fixed-b recovery, and fourth convexity then give strong convergence and the4/3 value coefficient. The proof does not need blanket equicoercivity of arbitrary rescaled sublevels.

For exact mass with a_ref=cv, rescaled optimizer means are O(ε), and the mean-zero limiting problem is H restricted to T={∫b=0}. A recovery competitor in T has mass error O(ε⁴/³); a bump correction of that order repairs the **exact** mass. The energy derivative on bounded rescaled sets is O(ε), so this correction costs O(ε⁷/³), which is negligible.

Small completion for Section8 strong convergence: actual rescaled minimizers bε need not be exactly in T. Define b̃ε=bε−L(bε)ζ, with L(ζ)=1. This correction is strongly O(ε) in X, and H(b̃ε)−H(bε)→0 on the bounded set. Apply H_T's constrained fourth remainder to b̃ε, then return to bε. This supplies the tangent legality implicit in the phrase “exactly as before.”

The sharpness scope is accurately declared: F_c is generally not left-SO2 invariant. These examples establish optimal exponents for the incoming general quartic theorem, not for every narrower invariant cone. The negative correction is to a positive convex energy minimum; it is not a negative quasiconvexity gap.

## 5. Root task-complete forward certificates

`root/TASK_COMPLETE_FORWARD_CERTIFICATES.md` was reconstructed after the independent initial note `FINITE_CONTROL_INFORMATION.md` was saved. Its Sections1–3 survive.

The all-real response fiber requires c in the acquired source span, q outside it, full fixed response columns, and no acquired global norm/coercivity bound. Completing the unmeasured lower block as CᵀS⁻¹C+I preserves strict accretivity for arbitrary unmeasured upper block Z. It leaves all measured columns fixed and realizes any cᵀKq. Static indistinguishability does not imply identical transients or physical realization. The root file states these limits.

For D≥0, S=D¹/² and K_r=VᵀA⁻¹V, the middle resolvent M=I+SK_rS has sym(M)≥I, hence ∥M⁻¹∥₂≤1, including singular D. With simultaneous input errors, expand using the true inverse for both vector errors and the inverse difference for the matrix error. This gives exactly the root radius, including the cross vector term. No independent-noise assumption is needed. The certificate remains conditional on the actual global update law and the paid joint error event.

External VNA/intertwiner comparisons in its Section4 were not independently checked here; this review covers the mathematical certificates and declared interfaces.

## 6. Empirical scope correction

The closure source's lines138–150 report a manually transcribed published trace, not a new experiment. Parent subsequently reported an independent raw CSV fetch that found an extra final invisibility row: source prefix39 rows versus raw40; raw final1.7068097484292658e−5 and final/best about1.6293038. I have **not** independently fetched that CSV in this review. The original source transcription is therefore not promoted as an exact complete raw-data reproduction. Parent's separate raw/prefix audit is the authority for that correction. No empirical observation enters any proof above.

## 7. Final Cartesian precision corrections reviewed

The initially reviewed bytes are preserved as `workers/cartesian_elimination/PROOF_v0001.txt` at the hash above. I subsequently read `CORRECTIONS_v0002.json` and the changed final proof ranges340–375 and450–483, pinning final `PROOF.txt` SHA256 **8d5b981880042e64de1c6e35f92b81471d1968a8cd47f2bb6ee6dc68025171ab**. The fixed-mean Euler multiplier and exact mean-zero projection are now explicit. The final proof also correctly states that the sharp example's non-C1 optimizer/non-C2 value behavior concerns the translation parameter ε; it does not prove optimality of the v-envelope Hölder modulus. In fact its unperturbed map a_v=cv is linear. These corrections preserve the reviewed rate, coefficient and Γ-development conclusions.
