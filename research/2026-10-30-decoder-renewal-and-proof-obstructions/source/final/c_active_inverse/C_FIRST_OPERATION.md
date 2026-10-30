# First independent operation: a filled exterior frame with one logical hole

30 October2026. C's first mechanism before sharing root/A's new ROOT28
constructions. This is a serious candidate and an exact admission failure,
not an asserted new universal decoder or a general impossibility.

For a qubit input, write d=2r. Prepare2r-1 logical query inputs as r-1
singlet pairs and one half of a Bell pair whose other half R is retained.
Use the unknown flat mixed encoder on ALL these logical inputs. They are
entangled across calls. The initial inference that this alone gave an
operational advantage over Choi programmes is SUPERSEDED by the known-
block scope correction below. Keep the physical outputs.
When the unknown encoded payload arrives, measure the known projector
onto the totally antisymmetric subspace of the2r physical outputs.

The projector commutes with U^tensor(2r), for arbitrary unknown U and
ambient D>=2r. On the occupied2r-dimensional code its exterior power is
one-dimensional, so the unknown frame disappears from the successful
contraction. Schur--Weyl duality for the logical/junk split gives

  Tr_junk[P_antisym (I_r/r)^tensor(2r)]
       = P_logical_total_spin0 / [r^(2r) Catalan_r].

The logical singlet query pairs already have total spin zero. Thus the
remaining Bell-program input and payload are projected onto their
singlet, teleporting the payload to R up to one known Pauli. This is an
EXACT heralded all-input/reference decoder with2r-1 physical source calls.
Its success probability is, however,

       p_success=1/[4 r^(2r) Catalan_r].

The1/r signal is not freely amplified: the flat junk has to occupy an
extremely atypical antisymmetric representation. The raw success factor
is superexponentially small in r. The failed branch has not been proved
to preserve the unknown payload, so repeat-until-success is not allowed.
Nor may amplitude amplification reflect through the discarded source
environment or call an unknown adjoint. Full throughput is NOT achieved.

This exposes a concrete difference between determinant/isometry inversion
and the mixed encoder. The exact contraction and its all-r admission
factor will be checked computationally at small r, then compared with
the strongest ordinary isometry/comb/program inversion constructions.
Possible repair: an adaptive restoring exterior-frame growth operation
with a paid successful replacement rule. Merely naming antisymmetry,
postselection, a quantum switch, or a generic Schur transform does not
supply that operation. No source, circuit or physical device is run here.

## Known-block scope correction

A known b-input joint pure probe is obtained from b independent normalized
Choi programmes by a reference-side Kraus filter F, with Tr F*F=1 and
||F||<=1. Its success probability is exactly2^-b; conditional on success
it is the exact requested N^tensor b probe state. Since the starting
probe is known and fresh, failure consumes no unknown payload/memory and
can be retried. Each singlet pair here is a FIXED b=2 block, so it costs
only a constant expected number of Choi programmes; the lone Bell query
is already a Choi programme. Thus the entire first exterior bank has an
O(r)-copy iid-Choi implementation at a fixed cap/error overhead. Its bad
admission is consistent with the accepted quadratic-copy lower; this
candidate did NOT pay an escape from that access class merely by naming
pair entanglement. The later spin-Q programme has a growing coherent
block and is treated independently. The final causal feedback cell
instead couples its second query to the already UNKNOWN payload, where
this retry argument is explicitly unavailable.
