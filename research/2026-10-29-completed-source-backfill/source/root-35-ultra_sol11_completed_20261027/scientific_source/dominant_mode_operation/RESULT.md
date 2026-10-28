# Internal-relative-time source executed; precise mode ratio not acquired

This bounded attack constructed and executed a different spin1 boundary
operation: a globally averaged pair of spin insertions with fixed internal
time separation. It also derived its first contact jet and the necessary
shared-dimer contact term. The operation retains zero total Matsubara
frequency while adding internal time structure beyond the old single
insertion/fugacity source. Its complete numerical test gives a small gain,
insufficient to justify costly source validation.

The required later connected thermal input remains **NOT_ACQUIRED**. This is
a failure of the tested two-separation family and contact-jet trial, not a
general exclusion of internal-time sources or a thermal gap obstruction.

## Mathematical output

[RELATIVE_TIME_SOURCE.md](RELATIVE_TIME_SOURCE.md) derives the source,
normalization, rotation covariance, domain bounds and exact contraction.

* Spin1 coupling is antisymmetric in its two spin labels. After global time
  averaging, g_delta=-g_(1-delta), so a constant/even relative-time kernel and
  the half-period separation give zero. The one-sided delta0 limit is P0 f.
* The physical insertion is i[S+(delta)S-(0)-S-(delta)S+(0)]/2. Two boundary
  sources give (-1)^(p+1)/5^p times an UNNORMALIZED physical trace integral.
  There is one relative-center integral and no extra beta or Gibbs quotient.
* The first jet becomes the Kubo endpoint observable
  D=6 beta Sz_neighbor-{Sz_endpoint,beta h_edge}/2, up to a total-time
  commutator. On the shared dimer its squared form also needs
  K=beta[36-6(SzL^2+SzR^2)+{SzL,{SzR,h}}/4].
* At beta3 the naive dimer jet squared form is -1.46931e9. Adding the required
  contact gives +3.63671e9. Nine exact generator identities, the exact D/K
  matrix identities, literal-history controls and finite-separation limits
  support the derivation. The thermal exponentials themselves are numerical.

## Completed matched preview

Two fixed separations, delta=1/8 and 1/4, were tested. The frozen ten-vector
P0 span, including its five existing fugacities, was preserved exactly. Only
these two new temporal sources were adjoined. The identical unprojected
source span was evaluated from the same physical eigensystems.

| Source span | Leading Rayleigh | Minimum residual variance | Moment target upper | Gram condition |
|---|---:|---:|---:|---:|
| Frozen ten-vector P0 control | 308459.6492 | 8.419603e8 | 328883.7488 | 2.65376e5 |
| Same control + two bilocals | 308608.2361 | 8.194104e8 | 328880.6850 | 4.44189e5 |
| Frozen ten-vector unprojected control | 291895.2591 | 5.593038e9 | 328883.6959 | 3.86111e4 |
| Same unprojected control + two bilocals | 293846.5910 | 5.085280e9 | 328876.9082 | 3.91820e4 |

The P0 minimum variance drops 2.68%, a factor of 1.0275. Its Rayleigh-vector
coefficient amplification (l1 squared over G norm) grows from 3.58 to 51.33.
The zero-frequency projection remains substantially stronger than the
matched unprojected control, while the new internal-time features add little.
The separate contact-jet span raises uniform P0 Rayleigh303807.73 to303931.94
and barely changes minimum variance; its full matrix receipt is retained.

There were 49 distinct new time-integrated correlations: 17 for the bounded
bilocal span, then 32 cross forms against the unchanged frozen span. New
four-point forms need at most four physical sites; new three-point forms
need five. Every signed magnetization sector and every intermediate ladder
sector was retained. The six-site source is needed only for the existing
control/contact-jet second form. Gauss16 versus32 on all49 correlations
differs by at most3.03e-15 relative. This is a numerical convergence check,
not a rigorous quadrature or eigenpair enclosure.

## Honest ratio and full-mode readout

Combining the strongest preview bounds from the tested controls gives

    scalar mode: [334515.0299,338972.0535],
    spin1 mode:  [308608.2361,328876.9082],
    ratio:       [.9104238326,.9831453859].

Both scalar endpoints are used. A ratio of Rayleigh lower bounds is never
treated as an enclosure. The same true ratio is used at n256 and n512.
All other spin lists, spin-list complements, assigned Ritz modes and
nonzero time-frequency modes remain in the full sixth-moment tail accounting.
The n256 remainder is1.39116e-18, while the connected interval has width

    .07536514056 = 101297 times the7.44e-7 target.

At the current ratio upper the local relative-ratio tolerance is about
3.96e-8; the preview interval has relative width7.99%. Finer tail bounds are
not the missing operation.

One useful conditional target follows from this complete readout: with the
current lower/rest bounds held fixed, spin upper314367.17 would suffice for
the7.44e-7 width. At the current minres Rayleigh308542.29 and positive-rest
upper271620.19, a Temple route would require variance at most2.15067e8,
a further factor3.810 below the acquired numerical proposal. This is target
arithmetic, not an acquired residual or a lower bound on other methods.

## Scope and preservation

The new proof/source operations, exact small spin algebra and numerical
previews are the deliverables. There is no certified later connected input,
precise dominant-mode ratio, gap, general computational advantage or physical
capability. Ordinary observable-response and Galerkin methods receive the
same source information in the matched control; no historical-priority
claim is made for time averaging, multipoint correlations or contact algebra.

[COSTS_AND_REPLAY.md](COSTS_AND_REPLAY.md) charges all completed stages and
validation debts. [INPUT_RECEIPTS.json](INPUT_RECEIPTS.json) records frozen
dependencies and verifies all41 old sol10 thermal files unchanged. Code,
matrices, all source values, controls, logs and full ratio accounting are in
this directory and hashed by its manifest. No further source-family expansion
or expensive validation was launched after the completed negative preview.
