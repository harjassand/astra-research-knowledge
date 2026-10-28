# Constructed loss-only access to hidden return dynamics

**Outcome: a conditional finite acquisition operation was constructed. The
foundational-discovery mission remains NOT_ACHIEVED.** No physical specimen,
selective pulse system, detector or experiment was acquired; novelty and
practical advantage remain UNKNOWN/NOT_ESTABLISHED.

The strongest finished operation uses one selectable kinetic state, four scalar
survival settings and an unknown fixed strictly increasing detector. At each
of two predeclared delays, measure late-only loss and early+late loss. A
crossed ordering—both-pulse signal rises while late-only signal falls—forces
a return revival. A fixed reversible conservative classical CTMC cannot have
that revival. Initial preparation need not be stationary or known; early and
late efficiencies may be different and unknown. All other states can be
unobserved and unaddressable. This is a sufficient witness, not a universal
irreversibility detector, a generator reconstruction, an entropy-production
bound or a new reversibility theorem.

The exact construction, proof and physical boundaries are in
`ONE_STATE_OPERATION.md`, especially its final monotone-detector repair.

## What was actually executed

`construct.py` builds a declared 32-state driven ring with one addressed state
and 31 hidden intermediate states. It generates synthetic scalar binomial
records under the nonlinear detector h(s)=1/100+(49/50)s^2. The analysis is
not supplied that detector law. It uses only the shared increasing direction.
The lag pair and balanced transient preparation were chosen from the supplied
model; discovery/preparation of a real specimen is not charged as completed.

Each of the four settings has 100,000 trials. Raw counts, in the order late3,
both3, late6, both6, are **73,587; 42,764; 70,284; 45,372**. The two measured
positive order differences are 3,303/100,000 and 2,608/100,000=0.02608.
Subtracting d=3/400 from each gives exact positive margins

    2553/100000 = 0.02553,
    929/50000   = 0.01858.

The analytic bounded-independent-trial confidence error is at most
2 exp(-45/8)<0.007214. Its strict upper bound is checked with exact rational
positive Taylor terms; both signs are checked with exact integer-count
arithmetic. This is a conditional finite-confidence theorem, not a claim that
a finite-bit sampler establishes its own exact IID premise.

Full declared acquisition cost is **400,000 fresh preparations, 400,000
terminal readouts and 600,000 elementary loss pulses**, plus unacquired reset,
state selectivity, survivor-law preservation, timing, energy, preparation and
detector validation. A real lag/preparation search also has acquisition and
multiple-testing costs. These are not four acquired trials.

`uniformization_check.py` independently bounds the declared model using exact
rational stochastic uniformization and explicit exponential-series tails.
It certifies P00(6)-P00(3)>0.2102068365 and two positive ideal detector-order
margins >0.0346129206 and >0.0269414577. The floating forward means used to
generate the synthetic record differ from those exact-model intervals by at
most 5.081e-15. This verifies the declared model computation, not its physics.

## Matched ordinary comparison

The ordinary comparator receives exactly the same four raw records, the same
unknown detector and preparation premises, and no hidden rates or detector law.
The reversible ordinal null is contained in a union of two nonpositive-order
halfspaces. Its binomial maximum likelihood is the better of two standard
pooled-mean fits. The component deviances are 270.3198 and 137.9921, so the
ordinary comparator also rejects. Its displayed likelihood p values are
asymptotic. No statistical/computational advantage over that comparator is
claimed. The constructed object is the access operation and cancellation.

## Essential limits that were preserved

- Natural population loss can fake the four-setting revival even for a
  one-state reversible decay. The affine eight-setting inclusion-exclusion
  repair is derived and demonstrated; it does not automatically repair an
  arbitrary nonlinear detector.
- A spectrally unresolved group can show a false revival from a transient
  microscopic preparation despite a symmetric reversible generator. The code
  preserves a three-state example and an exact six-state false-cycle ratio 16/5.
  A label must resolve a kinetic state, satisfy acquired lumpability, or use
  the different acquired stationary-group preparation contract.
- Unknown state-dependent detection, off-target removal, pulse-induced state
  transitions, altered survivor dynamics and drift can invalidate the result.
  In the monotone synthetic record an independently acquired per-setting mean
  bias strictly below 929/100000=0.00929 would preserve both confidence signs;
  this is a tolerance, not a measured bound.
- Coherent quantum evolution, external time dependence or memory can violate
  the null without constituting the claimed classical nonequilibrium mechanism.
- Many irreversible generators have no selected-state return revival. No
  universal finite horizon or guarantee of finding one has been derived.

## Supporting constructions

`PROOF.md` derives exact full hidden-transition reconstruction and detector/
pulse self-calibration from n^2+2n+1 scalar loss configurations under a stronger
all-state access contract. Eighteen independent rational fixtures recover P,
p, a, gamma and beta exactly, plus a rank-deficient stacked-constraint example.

`CYCLE_OPERATION.md` derives a 4k+1-setting selected k-cycle invariant under
unknown nonstationary populations and separate early/late pulse efficiencies.
The triangle example has three unaddressed intermediates. Its exact synthetic
finite-confidence sign gives A>1.43847 with error<0.008723, but costs 13 million
preparations and 18 million pulses. Thirty reversible control models, half
with diagonal killing, give numerical |A|<9.184e-13. The same-record ordinary
likelihood succeeds too. These are supporting model constructions, not
separate discovery claims.

## Primary credit and Astra scope

The work started from the current task-first entry point pinned to Astra
revision `a03ba7fe433815b80f2c71ddd8bcf599486d7557`; current projection searches
and N1037 packet are retained in `sources/` and `outputs/`. No archive was
preloaded and no shared repository, Capital intake, external publication or
physical interface was changed.

The reversible-return principle is prior art, including [Chen Yong (2009),
On the Monotonicity of Autocorrelation Function for Finite State Markov
Processes](https://xbna.pku.edu.cn/EN/Y2009/V45/I1/11). State-selective removal
for temporal correlations is prior art, including [Robens et al., PRX 5,
011003 (2015)](https://doi.org/10.1103/PhysRevX.5.011003). Correlation asymmetry
and thermodynamic affinity theory are established, including [Ohga, Ito and
Kolchinsky, PRL 131, 077101 (2023)](https://doi.org/10.1103/PhysRevLett.131.077101).
Physical depletion spectroscopy is established, e.g. [Schenk, MPQ317
(2007)](https://www.mpq.mpg.de/7062849/MPQ317.pdf), without thereby acquiring
our complete kinetic-state and detector premises. Current Astra N507/N508/
N588 surfaced stronger reversible-process mathematics; none is rebranded as
this worker's invention. Historical originality of the finite acquisition
design is UNKNOWN after this bounded screen.

## Files and reproduction

Main proof: `ONE_STATE_OPERATION.md`.
Primary record: `outputs/ordinal_one_state_record.json`.
Independent exact model bound: `outputs/uniformization_certificate.json`.
All results: `outputs/RESULTS.json`.
Physical failure fixtures: `outputs/essential_premise_falsifiers.json` and
`outputs/one_state_record.json`.

Run from the workspace root:

    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol9_frontier_20261028/inversion/construct.py
    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol9_frontier_20261028/inversion/uniformization_check.py

The next consequential step would be an acquired classical specimen satisfying
the exact operation contract, followed by this same-data ordinary analysis.
No such acquisition or practical advantage was completed here.
