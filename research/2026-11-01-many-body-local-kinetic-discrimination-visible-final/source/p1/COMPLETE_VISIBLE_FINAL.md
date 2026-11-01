## The collective gap now has a many-body law

I obtained a bulk dissipation law that covers **arbitrary interactions, shared physical records and collective control**, provided the unknown species enters through finite local kinetic multipliers. A separate proof covers a feed with an **exactly known target count**, including one target among arbitrarily many background particles.

That second result matters: knowing the total composition creates dependencies between all labels, so the independent-label argument does not apply. The new proof works on exchanges between possible material assignments and charges each physical transition once.

The constructive work also identifies a precise possible escape. A machine supplied with a native rate that directly depends on a joint predicate of many unknown labels can outperform the local-kinetic bound, with its records, rejected material and reset included. **Acquiring that joint physical operation economically remains unresolved.** Passive pooling, common motion and a resolved competitive amplifier did not acquire it.

The complete deliverables are:

- :chatgpt-content-reference{index="5"}[collective_kinetic_discrimination.pdf](producer-workspace/collective_kinetic_discrimination.pdf) — the 14-page research note, including ordinary proofs, constructions, comparisons and limitations.
- :chatgpt-content-reference{index="6"}[collective_kinetic_discrimination_research.zip](producer-workspace/collective_kinetic_discrimination_research.zip) — runnable calculations, numerical results, independent audits, source records and the unchanged predecessor archive.

The previous finite-contrast law, finite-jump proof, physical-history construction and accounted reset are preserved byte for byte, together with their independent-tracer boundary and the earlier research.

## 1. The consequential question and the resource model

The question I pursued was:

> Can a collective apparatus recover most of a dilute valuable component, produce a useful concentrate, discharge the rejected material and return to service, with dissipation scaling approximately with the amount recovered rather than with the entire feed?

To make “collective” substantial, the physical state includes all particles, memories, ancillary coordinates and control states. An elementary event may change many of those coordinates together. Interactions and feedback can be arbitrarily strong.

The restriction concerns **where the unknown identity enters the dynamics**. For conserved labels \(S_i\in\{0,1\}\), the resolved generator is

\[
L_S(t)=L_0(t)+\sum_{i=1}^{N}c_{S_i}L_i(t),
\qquad c_1=a>0,\quad c_0=b>0.
\]

Each \(L_i\) can act on the entire shared state. Its forward and reverse rates receive the same species multiplier. Thus the species changes kinetic activity, while the affinities and available controls are common.

This includes complicated cooperative machines. It excludes a supplied species-selective force, an initially informative memory, or a native event whose rate directly recognizes several unknown labels. Those are different resources whose acquisition must be examined.

I use dimensionless total entropy production \(\Sigma\), so physical entropy production is \(k_B\Sigma\). Define

\[
K=\frac{(a-b)^2}{ab}.
\]

Every particle ends in product or reject. Purity \(P\) and recovery \(R\) are ratios of expected material counts; they are not guarantees for every individual batch. Initial apparatus states are independent of the unknown labels.

The results concern finite-state classical jump machines, with no fixed limit on their size. Matching upper constructions use the operational closure of finite common-control protocols; they do not establish a device with economical fabrication, autonomous timing or a prescribed throughput.

## 2. The strongest new theorem: known composition still costs the bulk

Suppose exactly \(M\) of the \(N\) particles are targets, with their locations uniformly unknown. Write \(f=M/N\).

For any complete collective protocol in the resource class above, achieving \(P>f\) and \(R>0\),

\[
\boxed{
\Sigma\ \ge\
\frac{27NR}{8K}\,
\frac{(1-f/P)^2}{1-2f+f/P}.
}
\]

At fixed useful purity and recovery, as \(f\to0\),

\[
\Sigma\ge \frac{27R}{8K}N[1+o(1)],
\qquad
\frac{\Sigma}{MR}\ge \frac{27}{8Kf}[1+o(1)].
\]

**Even an exactly known target count does not remove the inverse-abundance dissipation cost per recovered target.** This includes the promise “there is exactly one target.”

The coefficient is not claimed optimal. The order is matched: an ordinary physical sequential sorter, including records and restoration, achieves \(O(N)\) total dissipation at fixed \(P,R,K\).

### Why this is a different many-body proof

The proof represents uncertainty by the graph of possible target sets. Two configurations are adjacent when one target and one background particle exchange roles. This is the Johnson graph \(J(N,M)\), with degree

\[
D=M(N-M).
\]

For a posterior distribution \(q\) over those configurations, define

\[
F(q)=
\frac12\sum_{\{s,t\}\in E}
\frac{(q_s-q_t)^2}{q_s+q_t}.
\]

It starts at zero for the uniform prior. It measures how well the physical state distinguishes nearby material assignments, including the correlations imposed by the known count.

The proof has three concrete steps.

1. **Exact finite transitions.** Interpolating between the forward and reverse probability fluxes gives an exact expression for the change of \(F\), alongside the entropy production. No small-jump approximation is used.

2. **One physical charge per event.** A channel belonging to particle \(i\) partitions the possible assignments into those where \(i\) is target and those where it is background. A positive-matrix certificate gives

   \[
   \Sigma\ge \frac{27}{4KM}\,\mathbb E F(q_T).
   \]

   This is one global functional. It does not charge a shared event separately for every particle that benefits from it.

3. **Product and reject together.** The actual outlet constraints imply

   \[
   \mathbb E F(q_T)\ge
   \frac{MR}{2}
   \frac{(N-M/P)^2}{N-2M+M/P}.
   \]

   Combining the two inequalities gives the theorem. No unobserved subset of successful targets or omitted reject stream is used.

For a nonuniform initial promise, the initial value of \(F\) must be subtracted. That qualification is physically meaningful: **supplied organization can already contain discrimination work.**

## 3. The independent-feed result becomes sharp for collective machines

For independently distributed labels with target fraction \(f\), the previous exact endpoint function now bounds the entire interacting apparatus:

\[
\Sigma\ge N B_K(f,R,P).
\]

The preserved independent physical-history construction attains this infimum in the stated operational closure. Consequently, collective control cannot improve the ideal dissipation optimum within this resource class.

The new allocation argument conditions, for each label, on all the other labels. Under that conditioning, every other-label channel is common to the remaining two hypotheses and contracts a convex posterior value. Only the channel carrying the selected label can create that value, and its contribution is bounded by its own entropy production. Summing charges each channel once. Endpoint convexity then removes the fictitious conditioning.

The other labels are **a proof device**, never information supplied to the machine.

In the dilute limit,

\[
B_K(f,R,P)\longrightarrow
\frac{4}{K}\log\frac{1}{1-R},
\]

so

\[
\frac{\Sigma}{NfR}
\sim
\frac{4\log[1/(1-R)]}{KfR}.
\]

For a twofold kinetic ratio, \(P=R=0.95\), and \(f=10^{-6}\), the sharp iid result is approximately:

| Quantity | Dimensionless cost per recovered target |
|---|---:|
| Irreversible entropy production | \(25.23\) million |
| Retained mixing free energy | \(14.45\) |

These are theoretical model values, not measured separator performance. Their significance is the enormous separation between the usual mixing requirement and the extra cost imposed by weak kinetic discrimination.

The complete work accounting remains

\[
\beta W=\Sigma+\beta\Delta F_{\rm blind}+I(S;X_T).
\]

Returning the apparatus to service does **not** by itself set \(\Delta F_{\rm blind}=0\): material volumes, energies and other unconditional free-energy changes also matter. The iid complete-work optimum is matched when those terms are appropriately controlled. For fixed composition, I have proved the dissipation bound and matching order, not the exact optimal work coefficient.



::chatgpt-content-reference{index="7"}



## 4. The physical interface: passive pooling has a finite sensitivity budget

A useful collective separator would like one rare particle to change a shared observable substantially. I derived an exact obstruction for a broad passive implementation.

Consider a reversible network with common equilibrium,

\[
L_d=L_{\rm blind}+\sum_i d_iL_i.
\]

Let \(C_0\) be its terminal capacity when every \(d_i=b\). Change a subset \(J\) to \(a\), and put \(r=a/b\). The baseline committor allocates nonnegative sensitivity weights \(w_i\), with total weight at most one. If \(W_J=\sum_{i\in J}w_i\), then

\[
\boxed{
\frac{1}{1+(r^{-1}-1)W_J}
\le
\frac{C_J}{C_0}
\le
1+(r-1)W_J .
}
\]

These are exact finite-contrast bounds. They survive eliminating arbitrary passive hidden states. The derivation uses the established Dirichlet and Thomson variational principles; the finite sensitivity budget is the application developed here. :chatgpt-content-reference{index="0"}

For a symmetric pool of \(m\) particles, one particle receives at most \(1/m\) of the budget. Its effect on capacity is therefore \(O(1/m)\), even if the network contains a complicated cooperative structure. Series and parallel organizations attain the harmonic and arithmetic sides of the bound.

Capacity is not automatically an escape rate. The report gives the precise preparation under which a related reciprocal mean-first-passage result follows, rather than identifying every observed transition rate with capacity.

This supplies a practical audit:

> An effective joint rate is insufficient evidence of an escape. Resolve how it is implemented. If its preparation, intermediate dynamics and restoration use only the local channels above, the complete apparatus still obeys the bulk law.

## 5. What the positive constructions actually achieved

The constructors pursued different mechanisms. Their strongest results were brought back to explicit physical interfaces and ordinary comparators.

| Construction | What the calculation established | Consequence |
|---|---|---|
| Shared event counter | One target changes a pool’s rate by \(O(1/m)\); fixed-quality discrimination requires observation time \(O(m)\) and activity \(O(m^2)\) in the tested counting model. | Pooling counts does not preserve single-target influence. A trajectory likelihood also does not supply a physical recorder. |
| Rigid collective motion | Frictions add. With one target, the rate ratio is \(m/(m-1+1/r)\). | Mechanical coordination retains \(O(1/m)\) dilution. |
| Concerted barrier | A postulated barrier can produce a rate \(\kappa_k=\kappa_0r^k\), retaining constant sensitivity to one target. | The barrier introduces species-dependent transition-state forces. Its baseline waiting time grows exponentially with pool size in the construction. |
| Competitive token amplifier | A fully resolved common-affinity machine successfully amplifies a target, with all channel entropy production counted. | The tested amplifier paid a growing background cost. Ordinary sequential discrimination already matches the proved \(O(N)\) order. |

The competitive amplifier is a positive construction: it uses physical tokens and reversible transitions, includes background degeneracy, and routes the selected particle to product. At \(N=32\), the tested setting reached recovery \(0.8\), purity above \(0.999999999\), and entropy production about \(610.36\). Clock, readout and restoration add cost. The finite results do not establish its asymptotic optimum.

The concerted-barrier comparison was especially instructive. Once repeated species-recognizing contacts are admitted, an ordinary separator can apply those same contacts to one particle. It gains contrast \(r^q\) after \(q\) contacts, with \(q\) of order \(\log(1/f)\). The proposed collective gate therefore has to compete with that informed conventional construction, rather than with a weak single-contact sorter.

## 6. A constructive boundary: direct many-label queries can beat the law

I also developed a counterresource with an explicit recorder and reset.

Its supplied elementary operation is a two-state sensor whose symmetric rate is \(a\) or \(b\) according to a parity of selected unknown labels,

\[
q_j(S)=\bigoplus_i G_{ji}S_i.
\]

The sensor is a physical terminal-state register. Decoding, routing, rejected material and record restoration are included in the ideal common-control model.

For one finite certified instance:

- \(N=1024\), iid target fraction \(10^{-6}\);
- 768 supplied parity sensors;
- kinetic ratio \(a/b=4\);
- recovery at least \(0.99535\);
- purity at least \(0.99722\);
- cycle entropy production at most \(533.34\);
- local-kinetic lower bound for the same certified task at least \(9776.92\).

Thus this stipulated extra operation beats the local bound by more than a factor of 18. The calculation conservatively accounts for feeds containing multiple targets and includes a finite implementation-error allowance.

**The parity-dependent native rates have not been constructed from local material interactions.** They are the additional resource. Wiring, fabrication and an economical autonomous controller are also not demonstrated. The result is a fully accounted countermodel within a supplied operation class, not an invented physical gate.

This distinguishes two propositions:

- Common affinities and finite per-label contrast alone do not imply a universal bulk law.
- Finite **local** kinetic dependence does imply it, despite arbitrary subsequent cooperation.

For iid labels, a broader necessary resource tradeoff makes this quantitative. If channel \(e\) has conditional contrast at most \(\overline K_{e,i}\) when label \(i\) changes, define

\[
\mathcal C=\sup_e\sum_i\overline K_{e,i}.
\]

Then the report proves

\[
\mathcal C\,\Sigma\ge 4N D_f(R,P),
\]

where \(D_f\) is an explicit binary-divergence endpoint function. At fixed useful purity and recovery, achieving dissipation per recovered target of order \(\log(1/f)\) requires

\[
\boxed{
\mathcal C=
\Omega\!\left(\frac{1}{f\log(1/f)}\right).
}
\]

A bounded number of label dependencies per event, each with bounded contrast, cannot provide that escape. This is a necessary condition, not a recipe for building the operation. I have not transferred this general multi-label inequality to the fixed-count ensemble.

## 7. What failed, what existing work contributed, and what is established

A useful failed proof exposed why multiplying one-label bounds is unsafe. After preparing a paid noisy parity record, a local measurement can increase the **sum of ordinary marginal posterior values** by more than the measurement’s entropy production. In a reproduced example, the ratio was \(1.640\). The conditioned construction gave \(0.981\) and correctly retained the earlier acquisition cost. That failure led to the conditional allocation argument; the known-count failure then required the exchange graph.

The literature helped identify the appropriate interfaces:

- Conditional information contraction and mechanism-resolved thermodynamics have established predecessors. The report credits them; no historical-priority claim is made for the assembled results. :chatgpt-content-reference{index="1"}
- Hasegawa’s arXiv:2610.26617 supplies decision inequalities for a complete trajectory and dynamical activity. Its entropy-production interpretation uses a specific forward/backward comparison. It does not itself construct the physical recorder, outlet routing or reset needed here. :chatgpt-content-reference{index="2"}
- The constrained-control constructions are serious competitors. Their independent kinetic controls and supplied measurement channels must be compared at the resource level; the feedback treatment explicitly separates measurement-apparatus costs. The ordinary physical-history sorter remains the strongest comparator within our complete iid task. :chatgpt-content-reference{index="3"}
- I followed the current Astra retrieval route to the governing native-event/shared-bit operation. Its atomic shared-memory update is substantive. When the unknown label only multiplies its own native event, the complete material-plus-bit process remains inside the new law. The retrieved governing sources and revision are preserved in the archive.

Verification includes 2,352 Johnson-graph channel checks, 441 finite-edge checks, 630 correlated output policies, 2,560 passive-network perturbations, independent proof audits, and the constructed machines. These are finite floating-point evidence supporting ordinary proofs, not formal verification or external peer review.

**The achieved advance is a discrimination law with a sharper physical boundary.** It explains why a large shared apparatus cannot turn finite local kinetic differences into cheap rare-material recovery merely by coordinating more degrees of freedom. It also identifies what a successful new organization must earn: substantial joint recognition in a native physical operation, growing contrast, useful pre-existing organization, or a species-dependent thermodynamic interaction—with acquisition and restoration included.

The strongest next scientific object is therefore an interaction that implements such joint recognition and survives comparison with ordinary repeated-contact separation. The present work gives that search a quantitative requirement and a complete-task test.

*Persistent saving remains blocked by the earlier automatic approval review, which required explicit authorization to transfer unpublished research. The complete downloadable files are provided above.*