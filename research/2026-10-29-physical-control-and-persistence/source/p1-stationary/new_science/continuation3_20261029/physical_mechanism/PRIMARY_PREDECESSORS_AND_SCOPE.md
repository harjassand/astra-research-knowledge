# Primary predecessors and the precise remaining comparison

29 October2026. Complementary physical-mechanism search within Astra P1.
Read scopes are explicit. These comparisons do not establish priority or
absence of a closer predecessor. The ordinary supplier note contains direct
proofs, not results attributed wholesale to the papers below.

## Closest concrete predecessor: Rejection Markov chain

Charly Andral, Randal Douc, Hugo Marival, Christian P. Robert (2024),
**The Importance Markov Chain**, Stochastic Processes and their Applications,
DOI10.1016/j.spa.2024.104316, arXiv2207.08271.

Primary accepted manuscript:
https://wrap.warwick.ac.uk/id/eprint/184924/1/WRAP-The-Importance-Markov-Chain-24.pdf

Read the introduction and Sections3--4 through the explicit augmented-kernel
definition. Section3, Proposition1 and Theorem2 give exactly the marked
endpoint incumbent: use a native stationary Markov chain, accept successive
endpoints with known state-dependent probabilities, and obtain a kernel with
the weighted invariant law. Their proof uses the same augmented independent
uniform mark and first return to the accepted set. This does not require
reversibility. Later importance-chain steps permit repeated recorded samples;
those repetitions are not automatically new physical endpoints or holds.

Comparison inferred here: the root finite counter replaces independent
acceptance marks by a correlated finite controller, obtains a deterministic
native-call cap, and returns the actual physical state. Unknown-kinetic
invariant-law reweighting or the augmented watched-set proof alone is not
the new part. The stationary mean can equal the ordinary rejection chain's
mean; the distinction is the maximum call count and the declared physical
operation/record contract.

## Watched chains and positive return kernels

David Aldous and James Allen Fill, **Reversible Markov Chains and Random Walks
on Graphs**, author manuscript, Chapter2.7:
https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch2.S7.html

Read the complete short section. The chain watched on a set has stationary
law given by conditioning the original stationary law on that set; it
inherits reversibility when the native chain is reversible. The section
carefully distinguishes watched, restricted, and collapsed chains. This is
the direct predecessor for the positive-return kernel and for projecting a
watched augmented controller. The root's specific bounded controller still
requires a separate actual construction and analysis.

Carl D. Meyer (1989), **Stochastic complementation, uncoupling Markov chains,
and the theory of nearly reducible systems**, SIAM Review31,240--272,
DOI10.1137/1031050:
https://epubs.siam.org/doi/10.1137/1031050

Author PDF: https://carlmeyer.com/pdfFiles/StochasticComplementation.pdf

Read publisher abstract and indexed author-PDF excerpts, not the full PDF:
two direct opens timed out. The first-return block formula is a conventional
stochastic-complement construction. Do not claim a detailed result from an
unread passage of that source.

## Slice augmentation and correlated acceptance uniforms

Radford M. Neal (2003), **Slice Sampling**, Annals of Statistics31,705--767:
https://glizen.com/radfordneal/slice-aos.abstract.html

Primary preprint: https://glizen.com/radfordneal/ftp/slc-samp.pdf

Read author abstract and opened the full primary preprint; the comparison
here uses the abstract's precise standard principle. Introducing a uniform
auxiliary variable underneath a density and then preserving the augmented
law is established slice sampling. The root counter's accepted set
{(x,c):c<=w(x)} is a finite version of that under-graph augmentation. The
root subsequently uses a different actual transition/return mechanism; this
similarity is a structural predecessor, not an assertion of algorithmic
identity or bounded physical runtime in Neal's sampler.

Radford M. Neal (2020), **Non-reversibly updating a uniform [0,1] value for
Metropolis accept/reject decisions**, arXiv2001.11950:
https://arxiv.org/html/2001.11950v1

Read Sections1--2, including the wrapped translation in equations1--2.
Neal keeps an acceptance uniform as part of the Markov state and updates
it by a translated/reflected uniform-preserving motion. This is a close
predecessor for replacing independent acceptance randomness by correlated
auxiliary dynamics. His Metropolis step can retain the previous state after
rejection, and his auxiliary rescaling enforces its own invariant law.
The reviewed passages do not give the root's coarse native-kernel,
mandatory-positive-call, bounded first-return reweighting theorem.

## Physical clocks and importance sojourn times

Andrea Bertazzi and Giorgos Vasdekis (2025), **Sampling with time-changed
Markov processes**, arXiv2501.15155v2:
https://arxiv.org/html/2501.15155v2

Read introduction, framework, Theorem2.3 and related discussion. Their
stationary-law relation under a state-dependent speed is the ordinary
time-change predecessor. Their introduction explicitly relates importance
weights, semi-Markov sojourns, and the Andral et al. construction. Therefore
general state-dependent clock reweighting is not a candidate new principle.
An actual physical hold or rate-control supplier is an additional interface
question that the mathematical speed function does not provide.

Sonia Malefaki and George Iliopoulos (2008), **On convergence of properly
weighted samples to the target distribution**, JSPI,
DOI10.1016/j.jspi.2007.05.030:
https://oldsite.unipi.gr/faculty/geh/abstracts/abstract14.htm

Read the primary author abstract. It treats weights as sojourn times and
obtains a semi-Markov process targeting the desired distribution from an
ergodic Markov sample. It is direct prior art for the clock interpretation.
Only the abstract was read; detailed assumptions beyond it are not attributed.

## Pathwise detailed balance and exact stopping are established

David Aldous and James Allen Fill, author manuscript, Chapter2.2.1,
Proposition2.4:
https://www.stat.berkeley.edu/users/aldous/RWG/Book_Ralph/Ch2.S2.html

The primary author exposition gives exactly the occupation identity for a
positive stopping time that returns the starting distribution in law. It
proves proportionality of the occupation measure to the unique stationary
law by the Markov property and telescoping. The root's mean lower bound
adds the mandatory-first-call domination to this established identity; the
occupation theorem itself is not a new contribution.

J. W. Pitman (1977), **Occupation measures for Markov chains**, Advances in
Applied Probability9,69--86, DOI10.2307/1425817:
https://www.cambridge.org/core/journals/advances-in-applied-probability/article/abs/occupation-measures-for-markov-chains/59E05999FA6DEA0F4D241327144705AC

Read the primary publisher abstract, which identifies the basic occupation
identity as a unified route to Markov-chain moment identities. Its issue
date is1977; the webpage's2016 online date is not its original publication.
No unseen result from its body is asserted here.

Jerome P. Nilmeier, Gavin E. Crooks, David D. L. Minh and John D. Chodera
(2011), **Nonequilibrium candidate Monte Carlo is an efficient tool for
equilibrium simulation**, PNAS108,E1009--E1018, DOI10.1073/pnas.1106094108:
https://threeplusone.com/pubs/Nilmeier2011.pdf

Read introduction and NCMC construction through the pathwise detailed-balance
and accept/reject equations. Pairing trajectories with their reversed
protocols is established. The algorithm explicitly uses the candidate or
the initial configuration (with the stated momentum treatment) after
acceptance/rejection. That simulation access is not a physical rollback
supplier for an unknown hidden device. A published correction exists; this
note uses no corrected numerical formula from the paper.

Laszlo Lovasz and Peter Winkler (1995), **Exact Mixing in an Unknown Markov
Chain**, Electronic Journal of Combinatorics2,R15:
https://www.combinatorics.org/ojs/index.php/eljc/article/download/v2i1r15/pdf/

Read abstract, introduction, definitions and the initial tree stopping
construction. Exact stationary stopping without knowing transition
probabilities is long established for an observed irreducible finite chain.
Their stopping algorithm observes states and is not a deterministic
native-call-deadline compiler from an unobserved microscopic state. It targets
an exact stationary sample, whereas the root kernel targets an invariant law
without itself proving preparation from arbitrary starts.

Dwija Kakkad and Dootika Vats, **Exact MCMC for Intractable Proposals**,
arXiv2410.10282v2 (2026 revision):
https://arxiv.org/html/2410.10282v2

Read abstract and opened full text. Bernoulli-factory MCMC for unknown
normalizing quantities is a relevant broader predecessor. The abstract
does not establish the root's physical terminal-state/no-rollback interface;
this note makes no algorithm-level novelty comparison beyond that scope.

## Search conclusion and obligations

Focused searches covered stationary reweighting by stopping, state-dependent
thinning, rejection Markov chains, correlated acceptance uniforms, finite
counters, systematic sampling, and bounded-gap rejection. They located the
direct ordinary rejection-chain predecessor and the correlated-uniform/
slice literature. They did not establish whether the precise bounded
counter rule, sharp native-call budget, or stationary-cost optimality result
has already appeared. Absence of a matching search result is not evidence
of priority. A report should name these mechanisms and keep the candidate
addition narrow until a deeper literature comparison is complete.

The root research role personally developed its bounded compiler. This
complementary note supplied ordinary alternatives, constructive challenges,
and primary-source comparisons inside the existing allocation.
