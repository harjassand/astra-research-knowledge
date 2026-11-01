# Finite-local-oscillator erasure for the three-value bus observable

Status: root candidate, independent review pending; OUTSIDE the accepted six-file
bus freeze. Ordinary beam-splitter/coherent-state photon counting is a component,
not a new erasure principle. No hardware feasibility claim is made.

Assume the received vacuum gate produces collected signal mode |b A>, with
A>=0 and data observable B=Z1+Z2 having eigenvalues b in{-2,0,2}. Introduce a
coherent local oscillator |i L>, L>0, in the same temporal mode. A balanced
beam splitter gives amplitudes (bA+iL)/sqrt(2) and (bA-iL)/sqrt(2).
Perfect number measurements of these TWO output modes yield integers m,n.

The corresponding diagonal Kraus amplitude at b is

 exp[-(L^2+b^2 A^2)/2]
 ((bA+iL)/sqrt(2))^m ((bA-iL)/sqrt(2))^n /sqrt(m! n!).

Let theta=atan(2A/L)/2. Exactly on the declared three eigenvalues,
atan(bA/L)=b theta. The phase above equals (m-n)pi/2-(m-n)b theta.
The global first term is irrelevant; the LOCAL correction exp[i(m-n)theta B]
removes the second. It factors into single-data-qubit Z rotations.

After summing all counts, the corrected coherence multiplier between b,c is

 K_LO(b,c)=exp[-(sqrt(L^2+b^2 A^2)-sqrt(L^2+c^2 A^2))^2/2].

Proof: the positive corrected amplitudes have port means lambda_b/2, where
lambda_b=L^2+b^2 A^2. The two independent exponential power series give
exp[-(lambda_b+lambda_c)/2+sqrt(lambda_b lambda_c)]. No homodyne limit or
large-L expansion is used. The output state is generally NOT perfectly erased:
total photon number carries information about B^2.

In particular the b=-2 to b=2 coherence is unchanged; the 0-to-+/-2 factor is

 v=exp[-(sqrt(L^2+4A^2)-L)^2/2].

With additional inaccessible vacuum signal displacement energy ell, put
a=exp(-2ell), d=exp(-8ell). The three-sector correlation matrix has adjacent
entries av and extreme entry d. Under the separately proved diamond formula,
if 2av>=1+d, the complete error remains 1-d: finite-LO which-B^2 information
does not exceed the already dominant extreme-pair loss error. This statement
must be checked at the actual parameters, not assumed for every finite L.

## Finite resources and remaining physical obligations

The local oscillator supplies mean L^2 photons; it is not free or infinite.
Detector loss can be modeled as passive attenuation before number measurement,
reducing both observed signal and LO amplitudes and adding lost SIGNAL energy
to ell. Equal loss on both output ports cancels LO cross terms in that lost-field
overlap. Unequal/mode-dependent losses need their actual received instrument.

The total recorded count is Poisson(lambda_b), with lambda_b<=lambda_max=L^2+4A^2.
If the finite counter receives all outcomes m+n<=M and uses arbitrary fallback
on overflow, a conservative complete-channel penalty is at most2p_over, where

 p_over <= min(1, lambda_max^(M+1)/(M+1)!).

This follows from the falling-factorial moment and is uniform over data and
references. It is an unconditioned failure budget; postselecting/renormalizing
success would need separate receiving because the count law depends on B^2.
Sharper ordinary Poisson tails may replace this bound.

Finite number-resolving measurement accuracy, maximum accepted count, detector
rearm/dead time or calorimetric response, mode matching, LO preparation, beam
splitter phase, timing, correction angle precision/strength/exposure, storage
noise and actual release remain costs. A finite photon budget does NOT construct
a faithful number detector. A one-click-per-bin detector would incur a further
multi-count probability, not magically implement this number measurement.
All these resources must be given equally to conventional alternatives.

The exact finite-LO calculation is VACUUM/coherent-signal-specific. It does not
inherit the arbitrary-warm-apparatus theorem of ideal conjugate-quadrature
erasure. Nor does the special three-eigenvalue phase identity hold for general
many-body B with additional distinct eigenvalues.
