# Processed-clock lifetime investigation — reading order and current status

The intended BOTH-current/full-common-form question has a positive answer.

1. `COMMON_FORM_UNIFORM_MEAN_ROOT.md` proves the gap-free bound

       E_{m(.|A_set)} tau <=4 Q_D/M <=4 B_total/M,
       Q_D=<1_D,A^(-1)1_D>.

   It explicitly receives positive sub-Markov propagation in both directions
   and the full constant-source forward/reversed-backward common-energy
   estimates. The proof is not a consequence of absolute CDF accuracy.
   SHA-256: adaf0b1ee53aa7560eee70e696b5100a1382801dbcd72cf2c01ae3997167690d.

2. The root's separate corollary
   `neutral_processing_clock_pending_20261101/SHARP_MEAN_FROM_COMMON_FORM_ROOT.md`
   combines the entire reference heat-content tail envelope with actual and
   reference absolute clock errors. It proves convergence of processed means
   to 1/k when the full-current excess and both CDF errors vanish.
   SHA-256: 5402b158d789c169535bf5007c21f575db4c3275bb810a09ed711ad83c82c4bf.
   I rechecked its exact tail identity and constants against this theorem.

3. `EXACT_REVERISBLE_LIFETIME_COUNTERMODEL.md` is an exact actual-chain
   counterexample only for the WEAKER interface of fixed trial a,q_h,rho with
   no uniform whole-domain source bound. Its B_S diverges. Its final paragraph
   referring to the full-source case as a harder open question is HISTORICAL
   AND SUPERSEDED by item 1; the frozen original was intentionally not edited.
   SHA-256: 4ccfb5f8e077c91855395667f8c1523411b4bada660853641ad78c3164a96a93.

4. `TIME_DEPENDENT_MIXING_CAN_STRICTLY_INCREASE_MEAN.md` gives a fixed actual
   three-state reference chain for which a predetermined finite-rate symmetric
   mixing pulse raises mean above Q_D. It does not make the ratio unbounded;
   it shows the autonomous constant-one inequality cannot simply replace
   the proved nonautonomous constant-four upper bound.
   SHA-256: c6d797b8a9a8d6ac9ca9ed4bff8afa52a9d0f4120cb291bcca8bd71874361484.

## Near-clock embedding of the strict-increase example

Without changing the three-state proof, take a disjoint ordinary Exp(1) state
of measure 1-eta and multiply each gadget atom's measure by eta. Now total
measure is 1, h=1_D, rho=0, and

    a=1+(98/3)eta,
    Q_D=1-(73/150)eta.

Thus a Q_D-1 tends to zero as eta tends to zero, while the scheduled pulse
increases mean by eta times the strict positive gain proved in item 4. This is
consistent with item 2: the gain vanishes in the sharp-mean limit. It merely
shows constant-one failure can occur arbitrarily near the clock regime.

## Receiving, verification and scope

The base theorem's source originals were read and left immutable. The
three-state formulas were checked both symbolically in the proof and by a
small floating-point consistency run; the theorem itself uses no numerical
fixture or numerical acceptance claim. Fresh independent mathematical review
was requested by the root and is tracked in its separate audit receipt, not
self-certified here.

No external state was changed. One short web search examined neighboring
primary literature on time-inhomogeneous random walks, but no external
result or novelty claim is used. No external retrieval denial, uncertainty
about mutation, or blocked authorization occurred. The only remaining check
at the time of writing is the independent proof audit; no source acquisition,
physical control implementation, feedback admission, or quantum consequence
has been claimed.
