# Connected essential pins: a paid mixed-boundary partition certificate

## Conditional premises, not yet proved for all proposed growth paths
Use any fixed zero-coupling triangulation of the physical square torus. Fix disjoint plus and minus pin sets D,N, each connected in this triangulation and containing an essential torus cycle. Every admissible spin assignment contains the same resolved wall gamma, of physical length p, whose crossed-edge endpoints remain pinned. Let the remaining free set be F.

Let z be the reference allplus-F assignment. Set m=P(z)-p and let Pmin be the actual minimum physical perimeter over all pin-compatible assignments. Suppose a certified gap g satisfies Pmin>=P(z)-g. This is a minimum-cut gap, NOT merely a maximum-path-barrier bound.

For the zero-field relative partition J=Z_pins/w_0(z), write q=3 exp(-2 theta),

    A=100 n q^4/(1-q),  b=100 n q^L/(1-q),
    M=max(L,ceil(m-g)).

Then

    J <= exp(A+2 theta m) * [100 n q^M/(1-q) + b^3 exp(b)/6].

The physical positive-field overwrite fiber is at most this zero-field ratio after dropping its nonpositive field penalty. All weights and clocks remain those of the original model; this is only a proof comparison.

## Proof
1. A contractible wall disk cannot contain any pinned vertex. Otherwise connectivity of that pin set, which contains an essential cycle, would force a path of identically pinned spins across the wall. Nor can the whole essential pin set lie in a contractible disk. Thus every contractible wall can be erased, including nested walls in succession, without violating either pin set or the fixed essential gamma.
2. After erasing all contractible walls, the remaining configuration is admissible. Therefore its total noncontractible perimeter is at least Pmin. With gamma deleted from the count, the remaining essential-wall total length is at least m-g.
3. Every embedded essential wall has primitive homology. Disjoint essential torus curves are parallel up to orientation. Their total mod-2 homology vanishes because the complete wall set is a spin-domain boundary; therefore their count is even. Besides fixed gamma there are either exactly ONE or at least THREE essential cycles.
4. In the one-cycle case its length is at least M. The certified physical contour count 100 n 3^s gives total activity at most 100 n q^M/(1-q).
5. Let b bound the total activity of every possible essential cycle (length at least L). Dropping compatibility, the total activity of sets with at least three such cycles is at most sum_(k>=3) b^k/k! <= b^3 exp(b)/6. No unproved lower bound on every separate cycle is imposed here.
6. All other contractible loops cost at most exp(A), by the ordinary low-temperature wall product. The fixed gamma factor cancels exactly between numerator and reference. The remaining reference factor is exp(2 theta m), proving the bound.

No factor 2 from global spin choice is needed: the nonempty plus pin set fixes it. If a convention retains that factor, it is a harmless additional paid constant.

## Where a useful gap might come from
During a deterministic prefix made exclusively of additions with at least two already-plus physical neighbors, the reference allplus-prefix assignment is an EXACT pinned perimeter minimizer: replay the remaining additions from any compatible initial subset, skipping existing plus sites. Every replayed addition still has at least two plus neighbors, so perimeter never increases. Thus g=0 for those prefixes.

After a genuinely straight moving front is formed, its perimeter is L or L+2. A retained fixed essential wall and connected essential opposite pins imply Pmin>=p+L, hence g<=2. Repeated one-neighbor seeds along the straight growth phase need not be bounded in number.

These arguments do not establish connectivity of the unprocessed minus pins. A two-neighbor addition can close a mouth and produce a contractible pinned-minus pocket. Such a pocket invalidates step1 above. A hole-first ordering, or a different pin/region decomposition, remains an explicit unproved prerequisite of the broader proposed application.

## Comparison with the raw short-wall bound
If g<=2 and m is at most about 2.45 L, the one-loop term scales as a polynomial times exp(2 theta g) 3^(m-g), rather than exp[2 theta(p-L)] 3^L. The >=3-loop remainder is suppressed by the extra essential perimeter. For theta4 and m<=2.45L+2, its main exponential is bounded by exp[-(4.4-3 log3)L+16], before the displayed polynomial factors. This improvement is conditional on the pin topology and mincut certificate above; no general-winding theorem or finite-parameter success is asserted here.

## Auxiliary encoding and frozen-region cancellation
The conditional inequality may choose a different fixed zero-coupling triangulation for each reference prefix, then MUST hold it fixed throughout that prefix's partition sum. A minus-biased reference triangulation converts maintained 8-connected minus pins to augmented-connected pins: any missing minus diagonal has a two-step minus NN alternative, unless the opposite diagonal has two plus ends, in which case the minus diagonal is selected. The retained gamma's local choices must be preserved. This is a representation choice, not a change to the original core or dynamics.

Frozen components not physically adjacent to F have no interaction or field term depending on erased variables; all their factors cancel in the ratio. Such components may be modified identically on numerator and denominator for the proof. In particular, bounded frozen holes may be filled plus and joined to the main plus pins, and isolated frozen-left extra plus bits may be removed. This cancellation must be established from the actual geometry; disconnected fixed spins cannot simply be declared essential-connected. If changing a frozen fourth plaquette bit, retain gamma's local auxiliary diagonal rather than rerunning a default rule there.

## Conditional finite numerical receipts, and a rejected scope extension
`conditional_scalar.py` considered p<2.45L and obtained a useful scalar only at R10000. Fluid identified a geometric completion obstruction for that wide range: a proper lift alone does not leave enough horizontal room to append a half-band before meeting the periodic collar. Those numbers remain conditional and are NOT an occupation theorem.

`short_conditional_scalar.py` instead assumes p<=2L-8, the proposed safer range for the separate completion proof. If that geometry, connected-pin cancellation, and actual visible-label reconstruction are established, the scalar portion yields

    N/ZA <= exp(-94), exp(-567), exp(-3858), exp(-41368)

at R=80,200,1000,10000 respectively. The numerical code explicitly retains its CONDITIONAL status. It uses theta4, L8R, the existing original-clock capacity upper bounds, and the following fully paid bound:

    J <= 202 n exp(16) 3^p exp[100 n (1/900)^4/(1-1/900)],
    N <= 4 n L J C_kappa.

The >=3-essential-loop remainder is bounded by one using exact rational exponential receipts; it has not been silently dropped. Actual visible walls number at most 2n/L=2L at a native edge, and two endpoint partition ratios and n coordinate-current cuts are paid. No free union over all geometrical contour words is used.
