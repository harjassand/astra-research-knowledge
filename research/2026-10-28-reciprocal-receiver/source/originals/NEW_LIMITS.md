# Limits of the new three-load reference interface

28 October 2026. These are bounded-error/information limits, not photon or
statistical lower bounds.

## Matched plus one known load does not suffice in general

Even exact complex returns for every input cannot determine absolute target
power from only the matched state and one known nonzero state. For r=1/2,
take reciprocal passive scalar sources

    S1=[[0,1/4],[1/4,0]], S2=[[0,1/5],[1/5,18/25]].

Their symmetric absolute row sums are at most 1/4 and 23/25, so both are
contractions. At z=0 both return zero; at z=1/2 both return 1/32. All
downstream phase-stepped reference intensities therefore agree. Their matched
target powers differ: 1/16 and 1/25. Embedding along one controlled basis
direction gives the same all-input ambiguity in any dimension. Adaptive
inputs and coherent full-field detection at these two loads do not help.

The third state z=-1/2 distinguishes the sources, returning -1/32 and -1/68.
Thus the new construction removes remote phase circles without assuming
arbitrary two-state switching already supplies absolute normalization. This
is not a minimality claim for every conceivable alternative instrument/prior.

## A sharp linear bounded-error exponent with a bounded reference

Assume |z|<=rmax<1, reference amplitudes R<=Rmax, and physical raw intensity
I=|h+R exp(i theta)|^2/2. For unit v and 0<epsilon<=1 choose S0=s=0,
t=sqrt(epsilon)v. This reciprocal source is passive; ||G||=epsilon and
h=z epsilon(v^T u)^2. Relative to the zero source, for every unit/subunit u,
load and reference phase,

    |I-I_zero| <= Rmax rmax epsilon+rmax^2 epsilon^2/2
                 <= C epsilon,
    C=Rmax rmax+rmax^2/2.

For C>0 and 0<delta<=C set epsilon=delta/C. The zero-source transcript is
compatible with both sources under raw errors bounded by delta, regardless
of the number of adaptive queries. Every Gram estimator has worst-case error
at least delta/(2C) on one source. For deterministic control in dimension>=2,
choose v bilinearly orthogonal to the returned command on the common
transcript; its regret is delta/C.

This matches the new linear exponent, up to constants/dimension, for bounded
reference power. It neither changes the original intensity-only square-root
theorem nor supplies a photon lower bound. Unbounded free reference power is
outside this contract; calibration, dynamic range and photons remain charged.

## Load-dependent reference phase can counterfeit a target

The exact mechanism tests retain identical twelve-power transcripts for a
zero-target background A=1/10 with load-dependent reference phase and a
passive source with residue 2ikA, pole ik, k=1/5 and target power 1/25.
At z=+-1/2 the unit-modulus phase factors are (99+-20i)/101. A common
reference phase is harmless; relative phase across states must be bounded.
Fitting the load response cannot detect this unrestricted calibration gauge.
