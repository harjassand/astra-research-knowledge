# Strand-order and cleavage audit: RNA recognition erasure

Scope: domain topology and state occupancy for the proposed `M`/`R`/`L`/`T`
operation in `../OWN_OPERATION.txt`. No sequence design, rate estimate, or
compatibility claim is made.

## A non-threaded candidate ordering

A possible local arrangement is:

```text
M (DNA):  ... — z — spacer — ... — a — ... — next assembly port — ...
R:        z* (DNA) — linker — t (RNA, exposed)
L:        a* (DNA), initially paired to M:a
T (DNA):  t* — flexible connector — a*
```

Place the orthogonal `z` anchor beside, but outside, the forward assembly
port `a` on the same solvent-exposed face. `R:z*` anchors the adapter to M;
its RNA `t` tail points outward. `T:t*` can then hybridize with `R:t`, while
the connected `T:a*` arm reaches the accessible initiation toe of the
`M:a:L` lock duplex and branch-migrates L off. This is a linear, open
association graph: no strand must pass through a closed DNA ring. This is a
topological possibility only. It assumes the lock exposes a usable toe and
that the tethered `a*` arm can reach it; neither follows just from the domain
list.

After that displacement, the occupancy ledger is `M:z::R:z*` and
`M:a::T:a*`, with L released. RNase H can cleave the RNA strand of the
`R:t::T:t*` hybrid. M's DNA backbone and its other alternating assembly
ports remain intact; once the next monomer uses the intended HMSD step to
displace T from `M:a`, the current port is also available again. Thus M can
remain assembly-competent in this graph, conditional on the adapter anchor
being orthogonal and non-occluding. The output is not bare M: the DNA `R:z*`
anchor remains attached, and a junction-proximal RNA stub may remain while
other RNA pieces become solution fragments. Product decoration and fragment
fate therefore stay in the material ledger.

## Exact early-cleavage loss path

The hybrid is already an RNase-H substrate immediately after
`T:t*::R:t` capture. A competing state path is:

1. `M:a::L:a*` remains locked while `T:t*::R:t` forms.
2. RNase H cleaves `R:t` before `T:a*` has displaced L.
3. T loses its only captured contact; L still occupies M:a; R remains on M
   only through z. The recognition tag is consumed before admission, so this
   input cannot proceed by the proposed recognition step.

This path conserves the named strands and needs no free invader. Enzyme
substrate specificity recognizes the RNA/DNA hybrid, not whether the second
DNA contact has completed. Preventing the path requires an acquired
admission-before-cleavage gate or a measured race favoring lock displacement;
the topology alone supplies neither. It is a concrete input-killing route,
not proof that every tuned implementation fails.

## Associative-activation comparator

Chen, “Expanding the Rule Set of DNA Circuitry with Associative Toehold
Activation,” *JACS* 134 (2012), [DOI 10.1021/ja206690a](https://doi.org/10.1021/ja206690a),
shows separately supplied toehold-carrying and branch-migration-carrying DNA
strands hybridizing at auxiliary domains to form an active invader; the
annealed pair, unlike either component alone, catalyzes the reporter
reaction. This supports association as a real way to assemble/activate
strand-displacement functionality. It does not establish this operation's
geometry: here T is first tethered through an RNA/DNA hybrid to an adapter
anchored on M, then its remote DNA arm must displace L from a different,
already occupied port on that same M. Nor does Chen test nuclease action
during that ordering. The comparator motivates the graph but does not
validate its reach, admission order, or post-cleavage turnover.

## Gate result

**Topology:** a non-threaded domain arrangement is possible, subject to
reach and an exposed lock-displacement toe.

**Post-cleavage:** the DNA monomer can remain assembly-competent in the graph,
but carries the DNA adapter anchor and potentially an RNA remnant; no source
demonstrates that decoration is harmless through later growth.

**Decisive obstruction:** cleavage can destroy an unadmitted input after
recognition capture but before lock displacement. This ordering is
chemically permitted by the stated substrate specificity and is not gated
by the associative strand-displacement precedent. The compatible
cleavage/admission race and buffer remain unacquired.
