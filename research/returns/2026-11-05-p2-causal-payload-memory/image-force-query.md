# One calibrated optical moment permits a translational-force query

This independent [complete measurement construction](package/companions/image_force/force_query_theory.txt) changes the admitted raw-image query by calibrating the **start-image radial PSF second moment**. It then acquires a force-carrying Stokes quadratic displacement functional without reconstructing a velocity field, particle identities or full PSF. It uses classical mean-value/moment correction, image covariance and reciprocal-force machinery; historical priority and performance superiority are not established.

## Exact finite blur correction and image operation

For an auxiliary Stokes field `div v=0`, `Delta v=grad pi`, let `S=sym grad v`, `D=y-x` and `f(x,y)=D^T S(x)D`. Then `Delta_y f=0`, `Delta_x^2 f=0` and `Delta_x f=D^T Hess(pi)D-2grad(pi).D`. With calibrated `mu=E|xi|^2/(2d)`, define

```text
k_mu=f-mu Delta_x f
    =D^T[S-mu Hess(pi)]D+2mu grad(pi).D.
```

A centered radial start PSF supported inside the valid Stokes neighborhood and an independent centered endpoint PSF of isotropic covariance give `E k_mu(x+xi,y+eta)=f(x,y)`. Endpoint radiality is sufficient but stronger than necessary. Calibration error is exactly `(mu-mu_hat)Delta_x f`; no infinite deconvolution is required. Higher finite PSF-moment hierarchies and a scoped converse for smooth linear radial-blur queries are also proved in the full note, not extended to every nonlinear/active estimator.

In two dimensions k separates into **five numerator cross-image covariance terms**, plus the positive total-intensity covariance normalizer. Processing uses six real start-image sums, five endpoint sums and six covariance accumulators, `O(P)` arithmetic per P-pixel pair and constant accumulation memory; a coordinate table can instead be stored or streamed. This relies on the declared matched-pair Poisson imaging law, brightness moments, linear images, full capture and independent electronics. Arbitrary particle populations, random-flow/Cox mixtures or common electronic noise do not inherit that covariance identity without additional conditions.

The normalized output is the finite-lag displacement current, not automatically hydrodynamic force. An explicit annular Stokes field has nonzero translational virtual load, crossing the earlier unknown-radial-blur harmonic zero-resultant boundary by spending the new calibration resource. Its exact source geometry and weights are supplied. A transparent/index-matched body with a full aperture is one stated optical contract; an ordinary opaque wall or arbitrary crop mask does not supply it.

## Mechanical conversion and its omitted terms

For the declared incompressible Newtonian flow, constant density/viscosity, known body/outer boundaries and auxiliary v, reciprocal mechanics expresses fluid-on-body force as the acquired `rho integral E(uu):S`, **plus** boundary-velocity, body-force and unsteady-momentum terms. They vanish only under their stated stationary/no-slip conditions or must be separately acquired/bounded. A planar view does not supply out-of-plane or endcap loads; the literal annulus gives force per axial length under its full two-dimensional/extruded contract.

Uniform seeding and lag h convert the measured normalized current to the inertial integral with factor `rho|Omega|/h^2`. Speed U and material acceleration A0 bound finite-lag bias by `rho|Omega| ||S|| [U A0 h+A0^2 h^2/4]`. Brownian tracers, finite-exposure motion blur, particle inertia and projection need their own models. A direct force balance is a strong simpler baseline when that access is available.

## Calibration, normalization and exposure

A finite point-emitter procedure can estimate mu with bounded photon exposure, but emitter size/centroid, tails, background, camera response and spatial radial invariance remain assumptions or paid errors. Seeing no exterior photons does not certify compact support. Optical PSF balls must lie in a certified Stokes continuation; masks/omitted strips need explicit current/shear bounds. Endpoint independence and isotropic covariance also require a physical model.

Pixel/geometry/weight errors propagate through bounded derivative or interval calculations. Admit the ratio only when its denominator interval is positive. A negative empirical normalizer does not permit an arbitrary replacement or sign flip. The earlier N1199 failed normalization record stays a failed record; no free improvement is imported.

Under a justified iid reset/mixing protocol and known fourth moments, two-record covariance blocks and median-of-means give finite simultaneous confidence. Every block pays two paired images, resets/reseeding, illumination, readout and lag. Correlated time series cannot use the iid radius by assertion. At fixed optical noise, individual covariances need not shrink as the final signed numerator does; the direct estimator can require **O(h^-4) image records** at fixed force accuracy, with tightening pixel/arithmetic tolerances. Linear pixel processing is not low acquisition cost. Closed uniform marginals can improve the mu-bias bound, but that cancellation is not a variance guarantee.

The [original symbolic/quadrature program](package/companions/image_force/force_query.py) and [recorded receipt](package/companions/image_force/receipt.json) verify Stokes/correction identities and a manufactured-flow reciprocal-force example. Reported blur residuals are below `2e-17`; reciprocal force `1.9000352368911049` agrees with integrated wall stress `1.9000352368911066`. Finite-lag errors decrease at the predicted first-order scale. These are algebra and deterministic quadrature, **not observed images, an optical experiment or a certified statistical force measurement**; Capital did not rerun them.

Pizzetti formulas, blur-invariant moments, reciprocal hydrodynamic-force methods, PIV and direct image-correlation stress inference are established comparators. An equally informed query-specific implementation can use the same constant set of covariances and `O(P)` arithmetic. The [selection/prior comparison](package/companions/image_force/selection.txt) retains why this is a completed conditional companion rather than a demonstrated civilisation-scale capability. [Original proof package and provenance](SOURCES.json).
