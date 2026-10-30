# Full-animal confinement yields a globally correctable output radius
2026-10-30. Root derivation candidate. The intended consequence is a FIXED ordinary decoder/recipient interface, not merely another memory constant.

## 1. An analytical connected graph, not a physical coupler
Use one of the accepted per-block CSS-sector animal graphs H. If necessary add a fixed simple cycle through its vertices, increasing degree by at most two. This is only an ANALYTICAL choice in the sum of proof observables. It adds no Hamiltonian, communication or measurement.

All actual conditions used by the weighted proof survive: each move set remains a clique; each component container remains connected and pairwise disjoint; support sizes/incidences are unchanged; active-hub assignment and DATA confinement are unchanged. Only the rooted-animal counting constant increases by a fixed factor. The canonical DATA component graph need not be altered. Rechoose the proof/rate constants for this graph rather than claiming an arbitrary previously fixed device automatically satisfies a stronger bound.

The graph has M_H<=C_H N vertices and now contains the full vertex set as ONE connected animal. Its weight is

    f_full=exp[L(Omega-(1-c)M_H)],  L=log(1/theta),

where Omega is the total occupied energy/history-token count in that sector.

## 2. Global reduced weight from componentwise confinement
Inside the accepted component-safe region, the sectorwise canonical representative E is a disjoint union of reduced components C. Their energy containers are disjoint, so confinement SUMS:

    U(E)=sum_C U(E_C)>=h sum_C |E_C|=h|E|.

No global small-weight confinement theorem is being applied beyond its radius; each individual component is below the imported cutoff. Since Omega=U(E)+R times the number of occupied history flags,

    Omega>=h|E|,
    Omega>=R number_of_bad_flags.

For a desired fixed fraction alpha>0, choose c sufficiently near1 that (1-c)C_H<h alpha/2, within all existing strict admissible margins. Then |E|>=alpha N implies

    V>=f_full>=exp(L h alpha N/2).

The accepted killed raw moment therefore gives an exponentially small TOTAL-weight tail, without a local-stochastic residual distribution or independence assumption:

    Tr(1_{|E|>=alpha N} rho_killed)<=C N exp(-L h alpha N/2).

A finite union handles the four per-block CSS sectors. Bad-controller flag counts have the analogous bound. For a product-code output choose the sum of the sector fractions below the desired fixed ordinary recovery radius.

## 3. Stronger option: make the killed basin itself globally correctable
Choose alpha small enough that the new cutoff

    M_small=exp(L h alpha N/2)

lies below the existing local-edge barrier, and choose (1-c)C_H<h alpha/4. Intersect component safety with V<M_small. Every state of this basin then has total reduced sector weight <alpha N by the full-animal inequality. The usual CP proof branches still preserve it, and its exponential boundary gives the same kind of decoded error bound with a smaller positive exponent.

Thus one can DESIGN the same architecture/rate family so its positive killed channel is supported in a fixed small total Pauli-error span. The physical first-initiation/noise constants may need to be reduced; the conclusion is not a free post-hoc strengthening for any arbitrary existing parameter choice.

## 4. Consequence for asynchronous transversal CNOT
Use the two-block physical program construction, but retain ONE ordinary fixed product-code recovery D_base at output, rather than the operation-dependent covariant recovery.

After the fixed target forest inverse, the physical DATA operator is U_* E_z applied to the canonical memory state. A memory canonical Pauli has total weight <=alpha N on the good projector. If at most beta N program columns are unfinished, every DATA Pauli coefficient of the dressed missing-gate product E_z has support <=r_gate beta N. The Clifford U_* increases ordinary DATA Pauli weight by at most a fixed spread s_U. Therefore every final coefficient has weight at most

    s_U(alpha+r_gate beta)N.

Choose alpha,beta so twice this is below code distance and, if using the efficient ideal decoder, below its accepted correction radius. ONE fixed ordinary product recovery corrects the entire coherent span and yields the actual logical CNOT, with no program-label input and no U_L inserted in the recovery map.

The unfinished-set moment bound gives exp-small probability of |unfinished|>beta N. It holds jointly with the killed memory state; no independence is needed. The reduced-weight tail above and a gentle projection give the same exponential gate error form after fixed latency. This is a proposed stronger endpoint awaiting review; the already accepted covariant-decoder gate theorem remains unchanged.

The target forest inverse remains an explicitly declared ideal bounded-depth controller operation. A physical/noisy live handoff is not proved merely by improving the core decoder.

## 5. Main audit points
- Verify that adding analytical H edges does not enter a hidden physical locality assumption or invalidate container charging.
- Sum confinement only on the actual component-safe canonical state; do not infer it for arbitrary distant logical sectors.
- Choose N>=N0 and a strictly exponential M_small below the local-edge barrier; preserve vacuum initialization.
- Keep reduced DATA weight distinct from controller excitation. Dressed missing gates must use their FULL fixed DATA support bound.
- Use the common correctable linear span, not branch probabilities of individual Pauli terms.
