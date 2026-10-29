# Primary predecessors actually consulted in continuation 5

29 October 2026. Source-based comparison, not an exhaustive priority review.
No external review or new discovery priority is claimed. Mathematical
derivations in the companion files are independently written; the ordinary
receiving principles below must retain their established attribution.

## 1. Relative energy gives a gap-free semigroup comparison already

Krešimir Veselić, *Bounds for contractive semigroups and second order
systems*, 2004 preprint; published in *Operator Theory: Advances and
Applications* 162 (2005), 293–308.

- Original preprint: <https://arxiv.org/pdf/math/0404120>
- Author-hosted version: <https://www.fernuni-hagen.de/MATHPHYS/veselic/downloads/dissip.pdf>
- Author publication list: <https://www.fernuni-hagen.de/MATHPHYS/veselic/radovi.html>

Read the introduction, Theorem 1 and its full proof, Corollary 2, and the
discrete-semigroup Theorem 2. Theorem 1 bounds the difference of contraction
semigroups by half a symmetric cross-energy form constant. Its proof uses
a weak Duhamel identity and integrated dissipation. The discrete version
uses the defect forms I-T*T. This directly precedes the uncompressed
receiver in GAP_FREE_RELATIVE_KINETIC_RECEIVER.md. No spectral gap is
required there. Root's proposed **compressed second-order** bound is a
more specific statement, but this read does not establish its novelty.

## 2. Local comparison already uses average coupling errors

Patrick Rebeschini and Ramon van Handel, *Comparison Theorems for Gibbs
Measures*, 2014, arXiv:1308.4117.

<https://web.math.princeton.edu/~rvan/dobrushin130819.pdf>

Read the local-update interface, Theorem 2.4, the one-sided Theorem 2.12,
and Proposition 3.2 with its telescoping proof. The comparison separates
an influence matrix from an **averaged** local coupling error. General
block updates enlarge the applicability of the original Dobrushin
condition. This is a direct ordinary predecessor for turning a local
error into a marginal or local-observable bound. Our physical issue is
how an actual acquired hidden conditional Gram defect supplies that
error under the deployment law. Merely presenting another influence
matrix or removing the total-volume factor is not, by itself, a new
physical principle.

## 3. Local dissipative perturbation stability under rapid mixing

Angelo Lucia, Toby S. Cubitt, Spyridon Michalakis and David Pérez-García,
*Rapid mixing and stability of quantum dissipative systems*,
*Physical Review A* 91, 040302 (2015).

<https://arxiv.org/html/1409.7809v3>

Read the model, rapid-mixing definition, Theorem 1 and its proof sketch.
The result bounds local-observable perturbation errors uniformly in
time and system size, under rapid mixing and a unique fixed point.
The paper explicitly includes classical Markov dynamics as a special
case. Its strategy combines locality with decay to equilibrium. Its
norm premise is a local superoperator perturbation bound, stronger than
a measured equilibrium L2 closure defect. The accompanying longer paper
was located, but a failed retrieval is not counted as a full read.

## 4. Uniform-in-time averaging for sparse many-body networks

Julien Barré, Paul Dobson, Michela Ottobre and Ewelina Zatorska,
*Fast non-mean-field networks: Uniform in time averaging*,
*SIAM Journal on Mathematical Analysis* 53 (2021), 937–972.

<https://arxiv.org/pdf/2003.14230>

Read the introduction, Theorem 2.1, the distinction between its two parts,
and hypotheses H.1/H.2. It combines fast-network averaging with a
many-particle limit. The uniform-in-time part uses sufficiently strong
convex confinement. This is an important direct comparator to any broad
claim of uniform-in-time, large-system averaging. It does not, in the
read statement, supply root's gap-free reversible compressed-energy
certificate or its finite local acquisition interface.

## 5. A general contractivity route to uniform time

Katharina Schuh and Iain Souttar, *Conditions for uniform in time
convergence: applications to averaging, numerical discretisations and
mean-field systems*, arXiv:2412.05239 (2024).

<https://arxiv.org/pdf/2412.05239>

Read the introduction and General assumptions 1. Their framework combines
a local-in-time approximation estimate, contraction of one process, and
uniform control for the other. It addresses averaging and other common
approximations. This is a clear ordinary alternative when contraction
is available. It does not justify inserting contraction for a critical
or nonmixing visible receiver.

## 6. Projected memory estimates are established machinery

Yuanran Zhu, Jason M. Dominy and Daniele Venturi, *On the estimation of
the Mori–Zwanzig memory integral*, arXiv:1708.02235.

<https://arxiv.org/pdf/1708.02235>

Read the projected evolution identity and Theorems 3.1–3.3 with the
first proof. They give memory growth and approximation estimates under
specified semigroup bounds. The bounds have explicit time dependence;
the difficult orthogonal-dynamics constants are not supplied by a mere
visible fit. These results directly precede the use of off-diagonal
projected dynamics as a source of memory. The read theorems do not settle
the priority of root's relative-energy, compressed uniform bound.

## 7. Fast hidden modulation is an old physical mechanism

P. W. Anderson, *A Mathematical Model for the Narrowing of Spectral Lines
by Exchange or Motion*, *Journal of the Physical Society of Japan* 9
(1954), 316–339.

<https://www.jstage.jst.go.jp/article/jpsj1946/9/3/9_3_316/_article/-char/en>

The original publisher abstract was read. It develops a random frequency-
modulation model and identifies narrowing controlled by fluctuation
strength divided by the modulation rate. This is a physical predecessor
to the idea that rapid hidden dynamics can suppress the effects of
disorder. It concerns spectral-line modulation, not our positive local
Markov control interface or the stated many-body error certificate.
The full paper was located but is not recorded here as fully read.

## 8. Abstract fast-generator averaging predates the present program

Thomas G. Kurtz, *A limit theorem for perturbed operator semigroups with
applications to random evolutions*, *Journal of Functional Analysis*
12 (1973), 55–67.

<https://www.sciencedirect.com/science/article/pii/002212367390089X>

Read the original publisher abstract. It studies semigroups generated by
A+alpha B as alpha grows, with the fast semigroup converging to a
projection and an averaged generator on its range. This establishes the
ordinary conceptual ancestry of a fast bath producing a projected
dynamics. The abstract does not specify the present finite, gap-free,
volume-independent error constant or physical acquisition construction;
no stronger theorem-level comparison is asserted without reading the
full text.

## Priority boundary and research implication

Locality, projection, fast-bath averaging, moment estimators and energy
dissipation are established ingredients. The potentially useful addition
has to be a demonstrably new **physical supplier/completeness consequence**
or a genuinely stronger quantified bridge at its actual sensing/control
interface. The promising root construction now joins a compressed energy
bound to independent local mobility modulators and an actual hidden bath.
The finite score supplier in LOCAL_MOBILITY_MOMENT_ACQUISITION.md makes
the needed first two mobility moments observable using two chronological
visible flips. Its structural premises, bath gap, deployment conditioning
and real costs remain part of the statement.
