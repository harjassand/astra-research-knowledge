# Independent check of the frozen-history grain diagnostic

## Finding and decision boundary

The radial operator's spherical normalization, flux signs, capacity conversion, and analytical spherical harmonic admittance are correct. A separately assembled full-volume/full-area frequency operator converges to the exact harmonic result at second order.

The diagnostic establishes that treating the grain surface as its volume-mean temperature misses a roughly 27.75 K surface–mean separation under the stated uniform-start, one-blow forcing. It does **not**, on its own, establish that a lumped heat-exchange model is unfit for every intended output. A criterion or error budget must distinguish surface temperature, grain mean temperature, transferred heat, and coupled chemical output. It cannot reject or qualify the physical device.

A material reporting issue was identified in the original harmonic diagnostic: it used arithmetic means on nonuniform BDF output samples. The parent has now corrected this to time-weighted means and retained the rejected sample-mean script/report separately. The main frozen radial diagnostic was unaffected; no radial rerun was needed. Even time-weighted one-blow mean properties do not constitute a complete periodic operating point.

## Independent derivation

Let R be grain radius, a = 3(1−por)/R the outer area per bed volume, and cv = CS/(1−por) the solid-material volumetric heat capacity. Thus CS/a = cv R/3, here 6614.583333 J m−2 K−1. This is the capacity per grain outer area, not per bed cross-sectional area.

For shell faces r−, r+, its volume divided by the outer sphere area is v = (r+³−r−³)/(3 R²), and the face area divided by the outer area is (r/R)². Their sums give R/3. The parent radial finite-volume equation uses precisely these normalizations. Midpoint radii and shell-average unknowns are an ordinary second-order finite-volume approximation for smooth profiles.

The original solid equation is CS dTs/dt = a h(Tg−Ts) − div(qs). Therefore the extracted nonfilm source per grain area must be g = −div(qs)/a. A direct reconstruction from the original stored solid states and original intercell flux formula agrees with g_other to 4.01e−11 W m−2.

With outward heat flux f, f = h(Tsurface−Tg) − g. The last-half-cell conduction relation gives Tsurface = Tlast − f δ/k, hence f = (Tlast−Tg−g/h)/(1/h+δ/k). This is the parent's boundary expression and has the correct heating/cooling sign. Harmonic face conductivity inside the grain is a valid series-resistance approximation; use of the final cell's k for the boundary half-cell is an approximation that vanishes on refinement.

For exp(iωt) forcing with constant properties and no independent harmonic g source, λ² = iωcv/k and the regular spherical solution gives q_in = Z Tsurface, with Z = (k/R)[λR coth(λR)−1]. Combining q_in = h(Tgas−Tsurface) yields Y = hZ/(h+Z). The lumped result uses Z_lumped = iωcv R/3. These match the parent formula. If a harmonic g is included, it enters as Tgas + g/h in this constant-h response; the reported Y is specifically a gas-temperature-to-heat-flux admittance, not the full nonlinear reacting-system transfer function.

## Numerical findings that decide interpretation

1. Independently assembled shell operator: full physical shell volumes 4π(r+³−r−³)/3 and face conductances 4πk r²/Δr; complex linear solve at period 2 s, no time trajectory. Across the 18 selected local parameter pairs, maximum complex relative heat-admittance error is 0.0585%, 0.0146%, and 0.00366% at 32, 64, and 128 radial cells. The 64-cell surface response error is 0.491% and falls by four under doubling. This supports the normalization, sign, and harmonic implementation without recycling the parent's transient solver.

2. Mean-property bias: 406 of 674 saved samples occur in the first 20 ms of the 1 s blow. Arithmetic sample-mean h spans 97.36–133.71 W m−2 K−1, but time-weighted h spans 137.63–243.78, with up to 46.8% understatement. Sample-mean radial/lumped harmonic heat amplitude is 0.98033–0.98630; time-weighted parameters instead yield 0.96440–0.98068 and a 0.854–1.569° phase difference. The latter is an illustrative correction, not a periodic-cycle computation. Time-mean radius Biot numbers are 0.349–0.679. If using volume/area as the Biot length, divide by three. Length conventions must not be mixed in threshold comparisons.

3. Frozen lumped control: a short independent 18-scalar integration using exactly the same piecewise-linear Tg,h,g histories reproduces original Ts within 7.64e−5 K. Thus the radial mean's maximum 0.73381 K departure is not an interpolation-baseline error. In cumulative one-blow net heat, radial/lumped ratios are 0.94589–0.97053, i.e. roughly 2.95–5.41% attenuation. Small absolute mean-temperature differences should not be mistaken for equally small relative errors in the temperature swing or stored heat.

4. The maximum surface–mean split is 27.7483 K at the end of the blow. The 32-to-64-cell difference in final surface temperature is only 0.07544 K, making that end-of-blow split well supported by this refinement. In contrast, the overall 1.8785 K surface refinement difference occurs at 0.188 ms and is dominated by the initial-boundary incompatibility/rapid early forcing. At t=0, the 64-cell reconstructed surface already differs from the prescribed uniform bulk start by up to 1.608 K because of its algebraic half-cell correction. Do not interpret that reconstructed initial surface as an exact continuum initial condition or claim uniform convergence of the earliest boundary transient.

## Scope and possible biases

- Initial history: all radial grains are reset to the lumped temperature at the start of a saved late-time blow. The inherited lumped state does not determine a unique radial profile. The material diffusion scale R² cv/k is about 50.3–55.2 s and film capacity scale cvR/(3h) about 27.1–48.1 s. One second is too short to forget an arbitrary radial initial profile. Uniform initialization suppresses any pre-existing gradient but is not a bound on the subsequent actual periodic gradient; a prior opposite gradient could enhance, diminish, or reverse the apparent error. The exact harmonic calculation avoids uniform-start bias, but only for a sinusoid at fixed properties, not this flow-switched model.
- Source distribution: the original effective interparticle/radiative net source is imposed uniformly over each spherical surface, frozen from lumped neighbors. That is a consistent total-power embedding, not proof that actual contacts/radiative exchange distribute heat that way. There is no gas or neighbor feedback.
- Selection: only 18 of 48 solid indices are included. Twenty-four original solid cells exceed the 1700 K conductivity-table endpoint, reaching 2371.07 K. Four additional cells (solid indices 10,11,36,37) have solids inside the table but are excluded because their gas is outside it. The gas-table screen is conservative but not required by a solid-conductivity table. Both external end cells are omitted even when within range. The selected set cannot qualify all grains or bound the hottest-region error.
- Conductivity extrapolation: numpy.interp would clamp outside 300–1700 K, not physically extrapolate. In the reported selected transient run, computed temperatures remain 753.50–1430.87 K, so that clamp is not exercised. The same guard is not automatically valid for omitted hot cells or future profiles. cv remains an inherited assumption, not a measured qualification.
- Temporal sampling: saved step spacing reaches 0.35764 s. The excellent frozen-lumped reconstruction means interpolation is not responsible for the measured bulk departure for this history, but cannot establish fidelity to an unsaved gas boundary fluctuation. Pointwise extrema between stored times also are not proven by the sample-selection predicate.
- Harmonic meaning: the exact sphere's surface oscillation is about 4.36–4.54 times the lumped temperature oscillation at the original sample-mean parameter set, while heat admittance differs only a few percent because film resistance dominates the gas-temperature-to-heat response at this frequency. These are different observables, not contradictory diagnostics. One 2 s frequency is not an all-frequency or square-wave-switching validation.

## Supported next conclusion

A qualified statement is: “Finite grain conduction invalidates identifying surface temperature with the lumped mean at the tens-of-kelvin level in this frozen, uniform-start diagnostic, and changes selected grains' one-blow net heat by approximately 3–5%. Whether this invalidates lumped heat exchange for the process requires an output-specific tolerance and coupled or otherwise sensitivity-justified propagation. The hot excluded material region and actual radial operating history remain unqualified.”

If the next admission decision specifically requires resolving surface temperature or tighter-than-3% one-blow transferred heat, this test supplies a reason to withhold that admission for the tested assumptions. It supplies neither a universal rejection of lumped engineering models nor evidence for device infeasibility.

## Reproducibility

- check_response.py: independent full-geometry frequency solve, direct source reconstruction, and brief frozen-lumped control.
- independent_results.json: quantitative checks and input hash.
- lumped_reconstruction_control.npz: independent lumped baseline at stored times.
- selection_and_scales.json: original-cell range screen and characteristic scales.

Original parent scripts and trajectories were not changed. No coupled gas solve or long trajectory was run.
