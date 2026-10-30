# Clarifications of the first root circulation theorem

30 October 2026. The original `NONLINEAR_CIRCULATION_OPERATION_AND_PATH_LAW.md`
is preserved byte-for-byte at SHA256
`53db4609d6b9a127c2898988a2f50684f4de7643d05c2156af516c19802a0c20`.
The actual receiving review in `record_geometry/receiving_review/` prompted
the following binding clarifications. They do not alter the physical path map
or its proof.

## 1. A large-deviation current map does not itself prove a central limit

The original Section 8 phrase that an always-active linear operation has
"leading current noise Q M Q" is too broad if read as a central-limit theorem.
The proved o(N^2) tracking estimate does not by itself control errors on the
N^(3/2) central-limit scale. A delayed sign servo can have a larger error on
that finer scale for some choices of capacity and delay.

The justified statement there is: the macroscopic mean response is Q M,
and the contracted *quadratic large-deviation action* at a fixed homogeneous
profile has the form associated with Q M Q. A separate finer tracking
theorem is needed to identify central-limit noise with Q M Q. The ordinary
calibrated linear governor can provide such a theorem at specified times
under its stronger response/precision premises; it is not silently part of
the main nonlinear result.

The armed controller's preservation of ordinary fluctuations is established
independently by its explicit full-record coupling and total-variation bound
in `RARE_LAW_TYPICAL_LAW_AND_FORCE_LIMITS.md`. Its nonzero ordinary noise can
coexist with a degenerate macroscopic rate. This correction reinforces that
distinction.

## 2. Topology and localization

The weak-measure and negative-Sobolev comparison is on **total-variation
bounded spatial sets**, not arbitrary bounded sets in an unspecified norm.
Conservation bounds the nonconstant integrated current; exponential tightness
of the harmonic coordinate supplies the required bounded sets. The exact
uniform auxiliary bound directly dominates the joint Skorokhod distance.

The main theorem as proved uses globally bounded derivatives of phi. Its
optional localization sentence requires stopping on a domain |h|<=L,
proving the fixed-L result, and then taking N to infinity followed by L to
infinity using exponential tightness. A single domain with a merely
exp(-cN) failure probability is not superexponentially negligible and cannot
be dropped. The explicit rational and linear examples have global bounds
and need no localization.

## 3. Which information is retained

The joint path map retains the auxiliary macroscopic current, so subtraction
recovers the native macroscopic current. It does not reconstruct every fine
sensor, apparatus or hidden-state log. Those records remain actual physical
records, whose laws are not identified with a hypothetical transformed
apparatus by the exponential-equivalence theorem. The rare-arming comparison
uses a separate coupling of the same actual record space before activation.

## 4. Small-trigger sensing for the mechanical supplier

The finite-response local detector's conservative error bound is O(R_N N)
when its relative-energy envelope and bounded sampling skew are used. This
is o(N^2) for tracking, but need not be o(N^(3/2)log N) for the smaller trigger.
An integrated example is R_N=ceil(N^(1/3)), a_N=N^(-1/6): capacity diverges,
mass vanishes, O(N log N) delay is admissible, and the detector error is
o(N^(3/2)log N). A larger carrier population needs a sharper detector estimate
or a stronger actual synchronization/readout port before invoking the rare
arming work theorem. The root rare-arming theorem already demands the
smaller observation envelope; this paragraph makes one supplier explicit.
