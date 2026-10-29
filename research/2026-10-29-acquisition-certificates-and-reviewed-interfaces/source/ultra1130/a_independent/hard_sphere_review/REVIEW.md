# Whole mathematical review: uniform-time hard-sphere finite observations

29 October 2026. **ACCEPTED at the declared ideal-real, radial supplied-model and finite-observation scopes.** I found no substantive mathematical obstruction after reconstructing the full chain. The only requested change was to define the cell consumer's mark explicitly as H_t=D Z_t; that clarification is now actually present in Section7 and was already implemented by the code. No new kinetic run or operator-row grid was required.

This review is independent of the producer's derivations. It comprises a whole analytic/source-code intake, direct primary normalization checks, read-only exact source/cover/hash inspection, and an independently written small scalar consumer. It is not a second independently implemented row-grid certificate, sampler replay, finite-bit implementation, physical validation or novelty/advantage review.

## 1. Governing primary normalization

I read Radtke--Hadjiconstantinou--Wagner's primary PDF, equations6--9, and visually inspected its printed third page. With the native hard-sphere exponent1, unit angular mass means their constant is C_1=1/(4pi). A variance-one Gaussian integrated over the plane normal to v-w gives `(2pi)^(-1/2) exp[-(v dot n)^2/2]`. Thus their 2K1-K2 divided by M(v) becomes exactly

`4 exp(|v_perp|^2/2)/|v-w|-|v-w|`.

The deletion rate is nu(v)=E_M|v-W|, including nu(0)=2sqrt(2/pi). No extra4pi, diameter or collision-rate exponent was imported. The producer's reference power beta=3/4 is distinct from that native exponent.

The primary Huber paper [arXiv:1308.1562v2](https://arxiv.org/html/1308.1562v2), Section2.2 and Theorem1, was read directly. Its general linear factory has the declared Cp<=1-epsilon premise and 9.5C/epsilon expected input-coin bound. Its pseudocode sets the threshold BEFORE capping epsilon at0.644, exactly as the implementation does. That ordering was examined and is not a discrepancy.

The producer does not consume an unstated quantitative Mouhot relaxation constant. Its comparison to equilibrium is derived from its own branching construction. Wagner/LVDSMC and isotropic deterministic methods remain strong ordinary comparisons, not rejected by the exact-output distinction.

## 2. Angular cancellation and the complete continuum row

I independently reconstructed the radial average. If r=|v-w| and d=V^2-s^2, then

`|v_perp|^2/2=(V^2+s^2)/4-r^2/8-d^2/(8r^2)`.

Changing the uniform incoming cosine to r yields the displayed Gaussian primitive. At r=V+s and |V-s|, its plus-argument terms cancel and its minus-argument terms give2erf(min(V,s)/sqrt2). This gives the exact gain4F(min(V,s)^2)/max(V,s). The averaged loss is max(V,s)+min(V,s)^2/[3max(V,s)]. Consequently k=A(min)/max-max has precisely the claimed form.

The positive series for A has constant4, quadratic coefficient1 and positive higher coefficients. Thus the rectangle enclosure is valid even when V=s crosses the rectangle. The singular origin is NOT left inside a numerical quadrature bin: A(delta)/s bounds the positive A/min component, its inverse-radius Gaussian moment is integrated explicitly, and the remaining loss/control bound is conservative. Calling this component a “gain” is harmless here; the actual enclosed object is the combined k.

The certificate's0..8 head cover has51 contiguous exact rational intervals. The independent read-only inspector checked every endpoint and every saved row bound against99/100. The maximum is the exact Fraction retained in STATIC_VERIFICATION.json, about0.98374. The interval routine's512 radial bins cover0..16; its first cell and four Gaussian tail moments are analytic. The coefficients are exact dyadic proposals; optimization accuracy is not an assumption.

I checked each tail-moment formula and the monotonicity of D(V)/nu(V). At V>=8, the two gain envelopes sum to at most4/[beta(1-beta)V^2] after dividing by nu>=V; the absolute loss is bounded by the stated Gaussian tail. Both decrease, so the tail value at8 covers the entire half-line, not a target cutoff. The saved upper is about0.33397.

I also checked the installed Arb API's upper/lower conversion: upper() returns an exact finite dyadic endpoint, and man_exp rejects an inexact ball. Thus serializing the upper endpoint does not silently serialize a midpoint. All absolute-interval endpoints and Gaussian bin probabilities are used in the outward direction in certify_radial_rows.py. I did NOT regenerate its integral grid; acceptance here is whole mathematical/code review of that computer-assisted proof plus separate coverage inspection.

## 3. Deflation, nonlinear fixed point and physical identification

For g=M^beta h, the weighted linear factor is `M(v)^(1-beta) Z_beta`, exactly D(V) in the row proof. Subtracting a(V)+c(V)s^2 therefore changes the ORIGINAL density equation only by

`-M(v)[a(V)m0+c(V)m2]`.

This verifies the units/weights of the moment deflation rather than merely naming a projection. The physical collision term conserves mass and energy for signed Gaussian-dominated densities by absolutely integrable collision symmetry. The two controlled moments hence solve a finite homogeneous linear ODE with zero initial value. They vanish identically. Radial invariance supplies momentum matching, so the controlled equation is the original homogeneous hard-sphere equation.

For the nonlinear term, collision energy conservation gives the exact M^beta product identity. The partner ratio is bounded by Z_beta/sqrt(beta): Gaussian scaling reduces it to nu(sqrt(beta)V)/nu(V), at most1 by radial convexity. This gives the2C_beta D^2 ball bound and4C_beta D Lipschitz bound. With eta=.99,D=1/3200,C_beta<4, the mild map preserves the D-ball and contracts with constant at most199/200 on EVERY time horizon. No future norm or mixing oracle is assumed.

Positivity is not inferred from that signed construction alone. I reconstructed the separate positive Picard argument with lambda=(1+8D)nu. On the2D-ball, lambda>=nu_f. The raw compact-head row is paid by48*34*T<1/100 at T=1/200000; the V>=32 raw tail is below1/40. The added diagonal and nonlinear Lipschitz costs sum to at most40D. Thus the contraction is at most3/80<1/16 and the image remains in the2D-ball. Starting with a positive iterate keeps the physical gain/loss Picard iterates positive. Local uniqueness identifies this with the zero-moment controlled solution. Repeating from each endpoint proves all finite-time positivity without assuming an evolved Gaussian domination theorem for a separately supplied solution.

## 4. Bounded tree and the late-time bound

Scaling z=h/D gives exactly the three branch weights in the proof. The linear branch contributes one child, each nonlinear event two, and kill contributes zero. Conditional expected offspring is at most eta+4D C_beta<199/200, independently of state/time. Summing expected generations gives at most200 visited nodes and almost-sure finite total tree; unbounded native clock rates do not create an explosion. The multiplicative signed mark is bounded by1 and first-event conditioning yields the controlled mild equation, whose uniqueness has already been proved.

The implementation returns D times this scaled product. The source density bound is sufficient, and the exact ball/shell mixture's mass and energy were independently checked. The prescribed nonlinear tape is only a branch-word implementation control, not an iid cohort.

For the equilibrium comparison, expected alive population has drift at most `-nu0(1-199/200)` times its size. The full tree already has finite total progeny. Localization and Fatou justify the stated survival estimate without a uniform upper clock bound. A nonzero mark requires a lineage reaching the initial-time boundary. This gives the claimed pointwise h decay and paid total-variation comparison to M. The very cheap Maxwellian alternative is therefore correctly admitted at its DIFFERENT tolerance contract.

## 5. Kernel, partner and factory acquisition

The low/high gain envelope masses were independently integrated. They are exactly E_low and E_high in the proof. The remaining components are Gaussian radial chi3, speed-biased chi4 and squared-speed-biased chi5, with known moments. The candidate acceptance ratio is the absolute combined signed row divided by the FULL positive envelope. The code's residual/inverse-gain representation is algebraically the same ratio, not a separate approximate angular average.

The all-speed envelope scalar bound is also paid. For V>=1, E_low/nu<=16/V^2; for V<=1, 1-exp(-x)<=x gives E_low/nu<=2V/nu<=2. The high envelope obeys E_high/nu<=2/beta=8/3 by erf(x)<=2x/sqrt(pi) and nu>=nu0. The Gaussian loss contribution is at most `beta^(-3/2)(1+beta^(-1/2))<4`. The controls cost at most `beta^(-3/2)(max|a|+4max|c|)/nu0`. The scalar consumer independently certifies that this exact expression is strictly less than48; the full-speed bound is not inferred from its table values alone.

The base coin mean is L/(E+2nu(1-pQ)); its general Huber multiplier produces L/[nu(1-pQ)]. Taking the nonlinear event first restores the unconditional linear probability L/nu. Since pQ<=1/400, the margin is at least3/400 and multiplier below51. The primary theorem therefore pays64,600 base coins. The auxiliary geometric law has mean C/(C-1)<=2. All these are known-kernel operations; L is NOT an input integration oracle.

After branch selection, conditional child rejection costs E/L, but its unconditional weighted cost is E/nu<=48. Thus a small or zero L is not hidden infinite expected work. Nonlinear partners use a V-Gaussian/speed-Gaussian mixture and accept |v-w|/(V+|w|). Radial convexity gives acceptance at least1/2. The outgoing squared-speed formula in the code is exactly the elastic sphere law, retaining the native incoming rate and collision angle.

The independently written scalar receiver verified C_beta, the envelope bound, factory constants, source moments and positive cell/cube margins without importing producer functions or rerunning the row grid. It took0.01786s after imports, with zero new kinetic samples.

## 6. Positive normalized output and arbitrary finite resolution

The scaling clarification is now explicit: `H_t=D Z_t`, with |H_t|<=D and E H_t=h_t. For W drawn from M^beta restricted to C_i, the expected numerator `A_i+B_i H_t(W)` is exactly the physical cell mass. Its realized value lies in[0,A_i+D B_i] by A_i>D B_i. Proposal q_i=(A_i+D B_i)/(1+D Z_beta) therefore yields the exact accepted cell law, with total acceptance1/(1+D Z_beta). Fresh ideal randomness supplies independent accepted outputs; no self-normalization or cancellation of negative final samples is used.

For ANY finite Cartesian grid inside[-4,4]^3, the pointwise ratio M/M^beta is at least `(2pi)^(-3/8)exp(-6)>D`. This proves every positive-volume cell margin independent of N, not merely on tested cells. The separately certified overflow margin is positive. Proposing a point from the KNOWN M/D M^beta mixture acquires the label weights without an N^3 dynamic table. Inside-box conditional sampling by three uniform rejection steps has at least exp(-6) acceptance per coordinate. For overflow, the potentially large conditional rejection cost is weighted by its actual proposal chance and has the stated bound<=1. Including outer rejection multiplies expected work by1+D Z_beta.

I checked the exact finite-grid theorem and its distinction between a proposal point and the physical label output. Y itself is not output as a physical velocity. Bit length, CDF-difference precision and encoding depend on N. No countable unbounded grid or continuous full-velocity law is inferred.

## 7. Implementation and accepted limits

I read the full governing programs certify_radial_rows.py, certify_completion.py, radial_query.py and run_uniform_consumer.py, plus the two main proofs, radial operator proof, source construction and prior/cost record. The saved kernel source and every original FINAL_RECEIPT hash matched the first read-only inspection. The only subsequent proof edit is the explicit D Z scaling, which does not change the code or science; final source bindings are saved separately.

The tree stack computes products correctly, the chi laws and actual hard-sphere kinematics match the formulas, and the cell rule uses the correctly scaled mark. The executed paths are floating diagnostics. They do not establish exact finite-bit output, fair-bit independence, a global numerical error bound or physical model validity. In particular the three128-output cohorts resolved no tiny transient signal and had zero nonlinear random events; the separate forced nonlinear path does not change that fact.

**Accepted:** the whole source-qualified ideal-real uniform-time bounded query, its all-speed computer-assisted operator admission, the positive normalized finite-instrument construction, and the arbitrary FINITE cube-grid-with-overflow theorem. The read-only/source-code intake is substantive scientific review, not merely manifest checking.

**Not accepted as accomplished:** continuous full-velocity iid sampling; an end-to-end validated finite-bit/floating runtime; empirical source/symmetry/moment calibration; a physical gas implementation; historical priority; or practical advantage over all equally informed LVDSMC, radial deterministic and paid-equilibrium alternatives. Those limits are already correctly retained by the producer.
