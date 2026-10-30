# Natural all-order boundary: a real active cell fails by data loss

The actual circuit reuses P1 before and after its payload-correlated
source call, interacts with the fresh source output, transfers through
P2, and keeps only one known controller qubit. This is a genuine escape
from mere holding-time relabeling, and it was analysed at ALL horizons.

At the fixed active port a11/14,b5/14, the exact coherent distinct-live-
tag walk has dimension12. A positive rational G satisfies

    G-S*(G)=I,   G<16I,   Tr(G rho_(M+))<15.

Thus the original data-bearing tag has a finite no-collision lifetime.
The source's causal3/r live-set collision hazard then pays the rare
event BEFORE data loss. For the explicitly frozen-Pauli-frame source
ensemble, every final known full-throughput decoder satisfies

    average Fe<=min(1,1/4+36/r)

at EVERY finite horizon. This is a worst-unknown-source obstruction,
not a pointwise upper for every U. It even allows arbitrary final
physical processing, so no free exponential decoder could repair the
cell. Complete worst-case error is at least max(0,3/4-36/r).

The ellipse (delta a)^2+3(delta b)^2<=1/64^2 around this port has an
explicit2G certificate, initial lifetime<30, uniform<32 and average
Fe<=min(1,1/4+279/(4r)). Returning dead labels keep the SAME frame;
they are not silently made independent. r-dependent tuning outside
this region, including toward a=+/-b, is NOT excluded.

One exact compilation took0.041535s, with no source/quantum/trajectory,
rank case or optimization. The simpler newest-only conveyor obstruction
is preserved separately. Generic high-fidelity three-carrier recovery
remains OPEN. A successful next controller must preserve an original-
tag algebra at zero collision rate and make its1/r effective transfer
a useful logical pump; this cell demonstrably loses the data first.

Root's full independent acceptance is saved separately in
root_controller_intake/WHOLE_REVIEW.md, including its literal circuit
rebuild and the physical sorting/collision/Pauli-average bridge. The
numeric certificate's field saying that bridge was pending is retained
as its original execution record; PROOF.md and the later whole review
close that analytical step without pretending a second execution occurred.
