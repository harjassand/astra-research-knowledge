# Exact primary sources and scientific use

Common Astra access revision: `63867607218adef378d727987fd92aa7dc42eb5c`.
The complete cleared-access note was read before selection; no peer's new
folder or developing choice was read. Archive search used the task-first
catalog and only the relevant lexical shards/packets, not a corpus preload.

1. **OpenAI, The periodic spin-one Haldane gap**, September24,2026.
   [Pinned paper](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-periodic-spin-one-Haldane-gap-September-24-2026/paper.pdf).
   Local `sources/haldane_primary.pdf`, SHA256
   `989f14096403897c693467f4007eb8997899648fd50029d5bee50ca9f8471ba6`.
   Live GitHub API resolved main to the pin; the directory's only listed commit
   is `adc7f1241b42e322a6451854ab7e4b4c146bf78a` on October6.
   Read: theorem/scope, spatial transfer construction, group sectors, purity
   bootstrap, both finite initializations, arithmetic/variational appendices,
   verification README and source manifest. The supplied original full verifier
   was not executed. The source already owns the spin-one proof and analytic
   criterion; it is not this branch's new result.

2. **Hal Tasaki, primary exposition**, published October18, revised October19.
   [Author page](https://haltasaki.github.io/writings/AI/OpenAI_Haldane.html),
   [discrete-time PDF](https://haltasaki.github.io/writings/AI/OpenAI_Haldane_DT.pdf),
   [continuous-time PDF](https://haltasaki.github.io/writings/AI/OpenAI_Haldane_CT.pdf).
   Preserved page and both PDFs. Actual acquired DT PDF has35 pages, CT34;
   the landing page describes both as34. DT SHA256
   `54ee3d765a70194b1162409718cd3d35d95bf339b34882f059993b2b35ddec4e`;
   CT SHA256 `5bc1b8f29d8892f2e723395a198d626a3ac555e2cb49a40e37846fae684ad9b9`.
   Read the scope/discussion and AppendixC.1 all-spin extension. It explicitly
   proposes spin two as a further computational target. This prevented the
   false novelty claim that the criterion's all-spin extension was new here.
   Tasaki distinguishes his analytic reading from unperformed independent
   verification of the original computer estimates.

3. **H. Nakano and T. Sakai**, Precise estimation of the S=2 Haldane gap by
   numerical diagonalization, [arXiv:1809.01393v1](https://arxiv.org/abs/1809.01393v1).
   Local `sources/spin2_precision.pdf`, six pages. Read full text and numerical
   scope. This is an important ordinary comparator: much larger twisted rings
   and sophisticated extrapolation already exist, but their extrapolation is
   not a uniform-gap certificate. Its20-site M=0 dimension is5976636799745.

4. **U. Schollwöck, O. Golinelli and T. Jolicœur**, S=2 antiferromagnetic
   quantum spin chain, Phys.Rev.B54,4038(1996),
   [DOI](https://doi.org/10.1103/PhysRevB.54.4038),
   [author-hosted full PDF](https://homepages.physik.uni-muenchen.de/~Schollwoeck/prbaug96a.pdf).
   Preserved `sources/spin2_1996.pdf`. Read introductory/algorithm/energy scope;
   established long-chain DMRG and QMC confirmation precede this construction.
   Their physical estimates are not used as rigorous energy or tail premises.

5. **S. Todo and K. Kato**, Cluster algorithms for general-S quantum spin
   systems, [arXiv:cond-mat/9911047v2](https://arxiv.org/abs/cond-mat/9911047v2),
   Phys.Rev.Lett.87,047203(2001). Preserved `sources/todo_kato.pdf`.
   Established high-spin cluster QMC is a strong numerical comparator, with a
   spin-two gap estimate0.08917(4). No QMC result is promoted to a deterministic
   trace enclosure or a rigorous infinite-ring lower gap here.

6. **G. Vidal**, Classical simulation of infinite-size quantum lattice systems
   in one spatial dimension,
   [arXiv:cond-mat/0605597v2](https://arxiv.org/abs/cond-mat/0605597v2),
   Phys.Rev.Lett.98,070201(2007). Preserved four-page PDF, SHA256
   `e4be597ad9986661654f750a06dcc0b674f7e71c63e8e38daa052f9f9427b199`.
   Read the Schmidt/two-site update construction. The trial search uses this
   ordinary algorithm, with charge blocks. Exact finite contractions, not
   imaginary-time convergence or truncation heuristics, certify the final input.

7. **X. Xu et al.**, The bulk spectral gap is semi-decidable: a convergent family
   of certified upper bounds,
   [arXiv:2606.03836v1](https://arxiv.org/abs/2606.03836v1).
   Preserved30-page source. Read abstract/introduction/scope. The orientation
   of the bound matters: an upper-gap hierarchy is not a lower-gap certificate.
   No claimed equivalence with finite periodic-boundary gaps is imported.

8. **I. Kull, N. Schuch, B. Dive and M. Navascués**, Lower Bounding Ground-State
   Energies of Local Hamiltonians Through the Renormalization Group,
   [arXiv:2212.03014v3](https://arxiv.org/abs/2212.03014v3),
   Phys.Rev.X14,021008(2024). The current primary abstract/version was read.
   This is a stronger ordinary compression comparator than bare finite-cluster
   bounds. No theorem is asserted that its energy relaxation counts omitted
   low states, certifies the needed thermal trace, or fails on spin two.
   The 2024 certified-equilibrium-state article was located, but its Nature
   page failed direct retrieval; no uninspected theorem or complexity constant
   from it is used.

9. **Astra N778/N779**, exact pinned task packets, and N779's governing thermal
   comparison plus sharper entropy-penalty note, preserved here. They concern
   environment-uniform energy/free-energy comparisons with explicit channel
   penalties. Their packets retain source-derived/unreviewed status. They
   are not assumed to give a spectral-count/thermal-normalization oracle.

10. **OpenAI, Exponential decay in two-dimensional classical O(n) models**,
    [pinned primary PDF](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/Exponential-decay-in-two-dimensional-classical-On-models-September-23-2026/paper.pdf).
    Preserved20-page source. Its statement and analytic opening were read as
    a possible alternative mass-generation bridge. The paper explicitly treats
    classical spin two-point decay, not a full transfer gap. No controlled
    reduction from the quantum spin-two lattice chain is supplied here, so this
    source is not a shortcut used in the present result.

`sources/file_hashes.json` records preserved bytes for the primary local files.
Hashes establish which source was read; they are not correctness or priority
certificates. No exhaustive novelty, referee, formalization, or physical audit
is claimed by this register.
