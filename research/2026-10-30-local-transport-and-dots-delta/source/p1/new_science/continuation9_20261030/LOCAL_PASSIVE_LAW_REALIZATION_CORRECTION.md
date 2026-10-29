# Carry the out-of-band supplier into the measurement bound

30 October 2026. Root correction after the actual-file receiving review by the
existing record-geometry role. Read this with `LOCAL_PASSIVE_LAW_REALIZATION.md`;
the original reviewed version is preserved unchanged.

The original native bounds (2) are only in the declared band. The measurement
bound (18) is valid as printed only if `A_out=0`, or if the **global coercivity
alternative** from Section 5 is actually warranted outside the band as well.
Section 6's phrase "under the bounds above" did not carry that condition
explicitly enough. No out-of-band spectrum is certified by in-band passivity
and norm bounds alone.

With a separately warranted outside-band envelope

    ||S_v(omega)-S_*(omega)|| <= E_out(omega),

the correct covariance error is instead

    delta_Sigma <= 2T Delta A_in
       + int_outside ||F(omega)||_op^2 E_out(omega) d omega/(2pi).

Then the same finite-record Gaussian KL/TV calculation applies if the resulting
relative covariance error is below one. Without such a supplier, (18)-(19)
are asserted only for an exactly in-band observation. A real finite-duration
filter generally has spectral leakage; its acquisition and noise objective
must therefore carry the extra information. A passive narrow RLC resonance
outside the measured band is a concrete reason an uncontrolled extrapolation
can fail. No fixed finite calibration grid rules it out by itself.

In the scaling statement after (13), a is fixed and strictly positive as in
Section 2, or has a warranted uniform positive lower bound. An upper bound on
a alone is insufficient if a is allowed to vary with N. With a tending to zero,
both the allowed observation band and Delta must be evaluated from (10)-(11)
without the stated fixed-a simplification.

These changes do not alter the Schur bound, exact response/noise identity,
actual local operation, or the singular-record warning. They restrict the
information that can support a finite-precision measurement claim.
