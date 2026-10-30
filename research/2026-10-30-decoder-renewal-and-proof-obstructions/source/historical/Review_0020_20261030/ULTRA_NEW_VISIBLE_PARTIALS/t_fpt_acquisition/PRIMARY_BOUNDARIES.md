# Primary predecessors and exact access boundaries

Read 30 October 2026. These are selected theorem-level comparisons, not an
exhaustive priority survey. Historical novelty of the packed guard is UNKNOWN.
No established theorem is replaced by an approximate result with weaker access.

1. Samuel Mausberg, Learning Low-Logit-Rank Distributions from Conditional
   Samples,8October2026. Governing author TeX at commit
   78fa048d082b465f0925299958dfb1063f38668a, cached read-only in
   sol27/t_computation/source_cache/mausberg_low_logit_rank_distillation.tex.
   https://sammausberg.com/research/papers/low-logit-rank-distillation
   https://github.com/SamMausberg/low-logit-rank-distillation
   Re-read definitions/Sections 4--8, Appendices B/E/F and quantitative parameters.
   The native fixed-rank theorem and the previous growing-rank linear guard
   are adopted prior. The exact probability-rank separation in Section6 is
   not a constant-TV approximate-rank lower bound. The stated future-work
   FPT question is what this packet challenges, under a stronger quantitative
   premise, rather than pretending its previous PRF theorem already settled it.
   Source/cost/fair-bit conventions remain binding. No full learner run here.

2. Barrington, Bounded-width polynomial-size branching programs recognize
   exactly those languages in NC1, JCSS1989. The width-five permutation and
   strong accepting-coordinate construction is the consumed ordinary primitive.
   https://doi.org/10.1016/0022-0000(89)90037-8
   The pinned Mausberg source already spells out the public sweep needed
   when the read schedule depends on the key. This packet does not grant
   a width-five program's label at arbitrary inconsistent words as a native
   Boolean oracle: the squared-residual guard is what permits simulation.

3. Naor--Reingold, Number-Theoretic Constructions of Efficient Pseudo-Random
   Functions, JACM51(2),2004. Theorem4.1's quantitative reduction has time
   poly(n)*t and advantage e/n; Section4.2/Theorem4.5 gives preprocessed
   fixed-key TC0. The one-bit hash in Section10 is separately justified by
   its pairwise-independent bias calculation. The extra subexponential DDH
   premise is explicitly assumed, not established by this qualitative source.
   https://doi.org/10.1145/972639.972643
   Author listing:https://www.wisdom.weizmann.ac.il/~naor/topic.html
   Primary-paper read via full PDF mirror:
   https://static.aminer.org/pdf/PDF/000/951/256/number_theoretic_constructions_of_efficient_pseudo_random_functions.pdf

4. Ding--Jain--Komargodski, Pseudorandom Functions in NC1 from LWE/LPN/CDH,
   arXiv2608.25213v1. Re-read MainTheorem3/Corollaries2--3 and their displayed
   shattering constraint ell'_q<ell. Those prove the stated polynomial-time
   existence implication; they do NOT directly instantiate exponentially
   many membership queries. We do not promote polynomial LPN security to
   the quantitative premise E. https://arxiv.org/html/2608.25213v1

5. Mossel--O'Donnell--Servedio, Learning functions of k relevant variables,
   Section5.2: native Boolean membership queries give junta learning in
   poly(2^k,n,log1/delta). This FPT incumbent is retained. Our source is not
   a junta in O(d) original payload bits; p packed coordinates carry n bits,
   and repeated reads are part of a hidden program. The source's conditional
   membership access is faithfully simulated from PRF membership, so an
   unqualified transfer would contradict precisely the quantitative premise.
   Author full text:https://www.cs.columbia.edu/~rocco/Public/juntas4.pdf

6. Balle--Mohri, Learning Weighted Automata, Sections4.1--4.2/Theorem6.
   Exact active learning receives field-valued string memberships AND
   equivalence/counterexample queries. Its passive spectral guarantee also
   pays a Hankel singular value. Neither access/conditioning premise is
   present here. This packet retains all of those ordinary positive results,
   without identifying probability rank and logit rank.
   https://cs.nyu.edu/~mohri/pub/cai.pdf

7. Chen--Klivans--Meka, Learning Deep ReLU Networks Is Fixed-Parameter
   Tractable, Theorem1.2/Theorem5.2: fixed polynomial dependence on ambient
   Gaussian-input dimension, with nonpolynomial dependence on network size,
   Lipschitz/accuracy and weight/depth parameters. Its Gaussian input geometry
   is an actual premise; arbitrary native prefix state distributions and
   whole-trajectory logistic updates are not supplied by that theorem.
   https://arxiv.org/abs/2009.13512
   Full primary theorem:https://par.nsf.gov/servlets/purl/10334261

The two decisive constructions here are new in this workstream, not a claim
of public priority: packed squared-word guards for the parameterized reduction,
and the whole-law approximate-probability-rank obstruction. No cryptographic
assumption has been tested computationally, and no actual FPT learner has
been run or refuted unconditionally.
