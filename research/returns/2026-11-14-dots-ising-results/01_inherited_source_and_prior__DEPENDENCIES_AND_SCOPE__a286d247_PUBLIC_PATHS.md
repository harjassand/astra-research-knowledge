# Source dependencies, assumptions and limitations

## Authorized source used

N1722 card:
https://github.com/harjassand/astra-research-knowledge/blob/main/cards/N1722-rare-ising-transition-capacity-and-unfinished-full-mean-construction.txt

P2 complete visible repository return:
https://github.com/harjassand/astra-research-knowledge/blob/main/research/2026-11-04-ordered-ising-current-and-full-residence/source/P2_DIRECT_CURRENT_COMPLETE_RETURN.txt

The repository return explicitly supplies:

* One rate-one proposal clock per site; four-neighbor Hamiltonian with theta=beta J and phi=theta/R.
* A fixed zero-coupling diagonal per plaquette used only for contour topology, not physical rates.
* Core A=C_r, acquired normalizer/conditional sampler and reflected-core gap interface.
* Actual soft-source edges kappa*w(x), x in A, with target B={M>=0} grounded. Core and target may overlap.
* M5 defined by augmented plus components having nonwinding lifts and embedded filled outer disks of area<=5R². Filled disks include holes, nested contours and their spins.
* Full-disk spin-flip weight bound exp(-2theta P+2theta V/R), physical isoperimetry P>=4sqrt(V), contour count<=6n4^P, and ZM5/ZA<=1/(1-u_r).

The inherited core interface reports its own prior internal review, but its complete construction archive was not recovered or reverified for this package. This package is CONDITIONAL on that interface and the displayed source conventions. It does not pretend that the inherited acquisition theorem was reconstructed here.

## Exact conditions

Main reduction: theta>=4, R>=32, L>=8R, n=L², 1<=r, r+2<=R/3, r<L/4, u_r<1. Source source-clock kappa is explicit. The executable finite examples use theta=4, L=8R, epsilon=.01 and kappa=epsilon/(64D0), with D0 from the inherited reflected-core interface. Tests never substitute kappa=1 for this actual-source claim.

The r+2 condition is conservative and pays box-width convention ambiguity in the thermal-core Peierls estimate. Cases violating it are not silently accepted.

## Topology convention and what was proved

The reduction interprets the source's embedded filled outer disk in its fixed planar triangulation: add the bounded complementary regions of an embedded component's planar lift, with the source's contact resolution. Boundary separation, laminarity and hull idempotence are proved for that convention in04. Physical perimeter omits the zero-coupling diagonals, exactly as in the source.

No new connectedness or simple-shape condition is imposed on the source configurations. Connectedness refers only to an actual augmented plus component. Thermal holes and nested islands are retained. Pairwise disjointness of the JOINED predecessor filled domains is derived for actual structural exits, rather than assumed for the entire configuration.

The primitive source definition was available as prose and contour interfaces, not as an executable canonical geometry library. Consequently the provided topology tests exercise an explicitly implemented fixed triangulation and its planar graph-fill convention. A reviewer should check that convention against any later-supplied source geometry implementation. If a different fill/contact convention is intended, the classification lemma must be rechecked; it is not licensed for arbitrary definitions called a 'filled droplet'. Under the stated standard convention, no additional unproved planar lemma is being assumed by this package.

## Dependency graph

Inherited source interfaces ->01 thermal-core capacity lower ->02 two-macro merger bounds and03 porous/gap bounds ->04 complete small-precursor and winding classification -> final current reduction.

The thermal capacity lower is itself an internally derived theorem here, not an independently reviewed source result. Its proof includes the field-tilted core Peierls bound and injective first-target prefix-flow accounting. The tiny flow enumeration verifies algebra, not the full acquired-core implementation.

## Computational and scientific limits

* Exact rational certificates evaluate explicit scalar bounds; they do not enumerate the large-volume current or acquire the unknown committor.
* Explicit bounds are finite and binary-representable; logarithms of tiny bounds are used rather than underflowing floating-point probabilities.
* This package does not supply a fast conditional sampler for the surviving dense precursor class.
* A C_kappa-normalized exceptional-current bound does not bound residence by itself. A rare family may have a long excursion time; the weighted residence operation remains required.
* No uniform native physical growth/coalescence theorem is proved for the surviving class. No full predictor or polynomial physical trajectory simulation is obtained.

## Prior comparison

The capacity variational principle, Peierls erasure, planar contour topology and current weighting are established machinery. GMV (Gaudilliere, Milanesi and Vares), arXiv:1809.07044, Lemma4.5, already proves normalized soft-capacity lower bounds with sharp asymptotic barriers in its tailored Wulff-box sectors; Lemma4.3 provides related reflected-sector gap machinery. Therefore neither capacity normalization nor thermal growth is claimed as a new concept.

The package's contribution is the explicit finite thermal-source normalization and its combination with actual-source, topology-aware current coverage. Its novelty relative to the entire literature is not established. Related existing GMV results have not been shown to provide the missing direct native-time transfer to this periodic source-conditioned dense class.
