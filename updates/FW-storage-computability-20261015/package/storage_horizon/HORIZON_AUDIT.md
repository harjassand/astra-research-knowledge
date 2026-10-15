# Independent audit of finite-horizon storage surgery

15 October 2026. Local analytic review of `FINITE_HORIZON_STORAGE.md` against `SOURCE_QC_REPORT.md`. This audit accepts the source quasiconvexity, coercivity constant and polynomial growth estimates as hypotheses; it does not independently recertify their algebra, external analytic inputs, or historical novelty.

## Verdict

The finite-horizon theorem and its numerical coefficients 1440, 6240 and 6960 are correct under those hypotheses. The direct-slice argument is preferable to the initially proposed low-energy-slab/trace-theorem argument: it has explicit constants and needs no critical trace constant at the cut. Passing from eta-minimizers to E_* = 2M/gamma is legitimate, including E_*=0. No minimizer or finite-dimensional solver follows merely from this truncation argument.

## Detailed checks

### Incoming coercivity with a moving mean

Let the endpoint be U=m+V_U, where V_U has zero transverse mean, and let M be the certified unit-entry action bound in the theorem. For any incoming path, append the reflected entry at mean m and a constant reset m to zero over a duration Q. The entire finite concatenation has zero outer traces, so source coercivity applies. Dropping the nonnegative gradient energies of the added pieces and using the upper bound M for the return gives

J_B(Phi) >= gamma ||D Phi||_4^4 - M - J_B(reset).

The source growth estimate makes the reset action tend to zero as Q tends to infinity. Thus incoming coercivity holds even when m is nonzero. The upper bound p_B(U)<=M can also be established directly, without first invoking mean invariance: concatenate a slow 0-to-m ramp and the shifted endpoint extension, then let its ramp length tend to infinity in the bound on the unrestricted infimum. Hence an eta-minimizer has gradient energy at most (2M+eta)/gamma.

This limiting argument only establishes inequalities for the unrestricted value and for a fixed prefix. It does not present an infinite ramp as an admissible finite-horizon competitor and does not assume the finite-horizon theorem being proved.

### A good interior slice and matching traces

For a path of duration T>H, Fubini on its terminal interval (T-H,T) supplies a slice t with

q = E_y |Phi_y(t,y)|^4 <= E/H.

Choose t from the full-measure set where the slice is W^(1,4) in y and agrees with the Sobolev traces of the restrictions to both sides. This ensures that all subsequent gluing is valid. No control of the original endpoint's W^(1,4) norm is used.

Writing Phi(t)=c+V, with mean V=0, the periodic Poincare constant used in the theorem is valid for vector-valued functions. Averaging translated differences over h in [-pi,pi], followed by Minkowski, gives

||V||_4 <= (pi/2)||V_y||_4 < 2||V_y||_4.

Equivalently, the periodic inverse-derivative sawtooth kernel has normalized L1 norm pi/2. For the unit entry Q(s,y)=sV(y), squared Minkowski on the two gradient columns gives

||DQ||_4^2 <= ||V||_4^2 + (1/sqrt(5))||V_y||_4^2
              <= (4+1/sqrt(5))sqrt(q) <= 5sqrt(q).

Consequently its quartic gradient energy is at most 25q, and its quadratic gradient energy is at most 5sqrt(q), since the normalized unit-slab measure is one. Reflection preserves these norm bounds. The claimed action budget

M_cut = 120[5|B|^2 sqrt(E/H) + 25E/H]

therefore bounds the absolute action of either entry or return. In particular, the nonzero-background quadratic contribution has not been omitted. Any cubic contribution is already absorbed by the source growth bound.

### Prefix removal and the actual cut mean

Append the shifted unit return and a slow reset to the discarded prefix. Zero-endpoint quasiconvexity gives the prefix lower bound -M_cut after the reset duration tends to infinity. This avoids any circular dependency on a previously established finite-horizon mean invariance.

The transverse average a(x) is absolutely continuous, with derivative E_y Phi_x. On the retained suffix of duration r<=H, Holder gives

|c-m| <= r^(3/4) E^(1/4) <= H^(3/4) E^(1/4).

Thus the replacement ramp must reach the actual c, not merely the oscillation V. Its cost is bounded by

120[|B|^2 C^2/L + C^4/L^3],
C=|m|+H^(3/4)E^(1/4).

A duration-L constant ramp, the unit shifted entry and the unchanged suffix have total duration at most H+1+L and match the original endpoint exactly. Their excess over the original action is bounded by the ramp budget plus 2M_cut. If the original duration is at most H, no surgery is necessary. Exact duration N is obtained by prepending the zero profile, which has zero adjusted action; a nonzero stationary profile must not be used as free padding.

### Eta tends to zero, including E_*=0

For each eta>0 the construction bounds the same finite-horizon infimum by p_B(U)+eta plus the explicit continuous error function evaluated at E_eta=(2M+eta)/gamma. H and L remain fixed while eta tends to zero. This proves the stated formula at E_*=2M/gamma; no convergence of the selected paths, cuts or cut means is necessary.

When E_*=0, M=0 and the endpoint extension has zero gradient, so its centered endpoint V_U is zero. For m=0 the zero path gives both values exactly zero, consistent with the formulas. For m nonzero, the general estimate retains C=|m| and a nonzero finite-ramp cost. It does not erroneously claim that a nonzero constant endpoint is free at a fixed horizon.

## Coefficient audit

For centered U, the general error equals

1200|B|^2 sqrt(E_*/H) + 6000E_*/H
+120|B|^2 H^(3/2)sqrt(E_*)/L +120H^3E_*/L^3.

Set n=N-1.

- With H=sqrt(n) and L=n/2, admissibility holds for n>=4. The quadratic coefficients are 1200+240=1440, multiplying |B|^2 sqrt(E_*) n^(-1/4). The quartic terms are 6000E_*n^(-1/2)+960E_*n^(-3/2). Since n>=4, their sum is at most (6000+240)E_*n^(-1/2)=6240E_*n^(-1/2).
- At B=0, H=n^(3/4) and L=n/2 are admissible for n>=16. The quartic coefficients are 6000+960=6960, both multiplying E_*n^(-3/4).
- The stated sufficient all-background horizon allocates half the error to each term, giving 2880 and 12480 inside the fourth and second powers. The stated B=0 horizon follows by raising 6960E_*/epsilon to the power 4/3. All these substitutions are correct.

For the mean-fixed restricted class, c=0 and the mean ramp disappears. The displayed 1200 and 6000 coefficients follow directly with H=N-1. Its comparison remains about the restricted infimum, which is not shown equal to the unrestricted one.

## Essential scope caveats

Uniform convergence bounds using only a centered critical norm apply to centered endpoint representatives. The general formula correctly includes the endpoint mean m. They are not uniform over arbitrarily large additive constants at a fixed horizon. For example, at B=0, quasiconvexity around the affine path with derivative (c/T|0) gives the lower bound G(c|0)/T^3 for a path to constant c in duration T; this grows quartically in c. For duration at most N it is at least G(c|0)/N^3. Thus removing m from the general finite-horizon error would be false.

The unadjusted action differs from the adjusted action by the exact endpoint affine term DG(B):(m|0), at every duration, so the truncation error is unchanged.

The endpoint extension budget M still needs certification. Numerical constants at the cut do not provide a universal numerical endpoint-extension constant that was never supplied. The theorem gives a horizon once that budget is known, or uniformly on a ball with a certified common budget.

Finally, effectiveness is not practicality. With B=0 and extension gradient L4 norm one, E_*=600,000,000. The stated sufficient horizons of roughly 3.13e19 for error 0.01 and 6.73e20 for error 0.001 are consistent with the exact formula and are astronomically large. This removes the duration-truncation obstruction in principle. It neither supplies effective spatial discretization or global optimization nor contradicts the source's uniform finite-Fourier observation obstruction.


Integration evidence status: `source_derived_unreviewed`. Audit verdicts and primary-source reading statements above are attributed to the supplied research, not new external review. This intake replays only its three own exact verification scripts. The conclusion applies to the particular certified Heat18 quartic G, not the full quartic cone, PR97’s newly exposed ROC ray, or general Morrey questions.
