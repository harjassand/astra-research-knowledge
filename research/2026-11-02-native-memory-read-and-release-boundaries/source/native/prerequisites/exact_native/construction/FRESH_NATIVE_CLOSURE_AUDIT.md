# Fresh adversarial audit of the native-clock thermal closure

2026-11-01. Independent review of `root_rod_audit.md`, `independent_constructor.md`, `ROOT_CONDITIONAL_THERMAL_TRANSFER.md`, and `dynamics_audit/CONDITIONAL_DAVIES_CONSUMER.md`. The rod addendum was read only after the main algebra and bounds were independently checked. No finite-size numerical result or prior PASS was used as evidence for a family theorem.

## Verdict

**The scalar ancillary free-energy lemma survives this audit, under the exact assumptions below. No fatal gap was found in the time-circle gas, ordered-prefix pair signs, signed continuum cluster theorem, or marked-winding local Fourier estimate.** This is a full-spectrum, sufficiently-low-temperature theorem, not an all-temperature theorem or a general physical-memory theorem.

Two consequential scope restrictions must remain explicit:

1. The result does **not** supply uniformity under arbitrary pinned excited boundary clocks. That stronger version of the constructor's original boundary-modification target is false without boundary corrections. The witness interface must use the original full trace, or separately justified free/deleted-check boundaries.
2. The support diameter is the distance inherited from the **ambient** overlap graph, not intrinsic distance inside the flux support: flux supports need not themselves be connected. Physical metric weights require a uniform bound on adjacent clock-center distance.

The trace-witness and dynamical consumers remain separate assumptions/results; this audit does not certify the actual-code witness injection.

## Exact assumptions certified

There are finitely many clocks in each volume, each of the same fixed dimension K>=3. The constants below are uniform over volumes. Checks S_g are mutually commuting Pauli operators; each is represented as a product of K mutually commuting single-site Hermitian Pauli/identity factors P_(g,i), with identity padding permitted. Their overlap graph has closed-neighborhood size at most D. The microscopic Hamiltonian is exactly

    H = Delta sum_g (1-|0><0|)_g
        - t sum_(g,i) (|i mod K><i-1|_g P_(g,i) + h.c.),

with Delta>0, t>0 and beta>0. No uncharged perturbations, pinning fields, extra links, or generic ancillary potentials are included. The dressing uses a fixed product order of controlled prefixes. Bounded check geometry and bounded coloring are additionally needed for the native locality/dynamical interface, not for the scalar gas identity itself.

For mu>=0 define

    r=t/Delta, Dbar=D exp(mu),
    a0=64 Dbar r^2, b=32 Dbar t^2/Delta,
    d=Delta-2t-b, B=beta Delta.

The sufficient inequalities are

    a0 <= log 2,
    2r+32 Dbar r^2 <= 1/2,
    (K-1) exp[-beta d+a0] <= r^2.

They imply d>=Delta/2 and r<1/2. They are sufficient, deliberately nonoptimal, and independent of volume. To obtain a chosen relative error epsilon, the explicit remainder bound below must additionally be <=epsilon. Small r alone at fixed B does not satisfy the thermal inequality.

## 1. Ordered Pauli algebra and genuine pair factors

Write U(q)=F_1(q_1)...F_M(q_M), with F_g(q)=P_(g,1)...P_(g,q) and F_g(0)=I. For a g-hop with physical factor P and closing-edge indicator c, cancellation of the earlier prefixes, followed by cancellation at g, gives

    U(q')^dagger P U(q)
      = [product_(h<g) chi(P,F_h(q_h))]
        [product_(h>g) chi(S_g^c,F_h(q_h))] S_g^c.

Here chi is the scalar Pauli commutator sign. This identity follows directly by conjugation; it does not assume that prefixes on different checks commute. The same g-edge in reverse has identical signs because other coordinates are unchanged and the reverse edge has the same c and P.

At each hop, every nontrivial sign involving another clock h can be assigned to the unique active rod on h and the rod whose endpoint or internal hop is occurring on g. Simultaneous hops have zero integration measure. A hop at an endpoint belongs to its own excursion. Multiplying all such contributions from both directions for an unordered pair of rods defines a symmetric factor. Its arguments retain the entire trajectories, not merely their lengths. It is independent of the scalar flux variables s. Disjoint-time or disjoint-support rods have factor one. Same-clock overlapping rods have factor zero. Consequently h in {0,+1,-1}; f=h-1 satisfies |f|<=2 and |h|<=1. There is no residual many-rod sign interaction.

## 2. The circle measure really recovers the trace

The ordered Duhamel expansion is first taken with a labelled time origin, including the sum over initial clock positions. A clock that ever visits zero has a unique decomposition into maximal nonzero intervals. Each is parametrized by its exit time u modulo beta, positive duration l<beta, endpoints adjacent to zero, and its ordered internal hops. This parametrization is unique even for an interval crossing the origin. The Jacobian is one on each ordering cell. The original interleaving of hops on different clocks is likewise unique away from collisions. The gas factor 1/n! removes only the arbitrary rod labels; it does not quotient by choices of zero visits.

The complementary histories never visit zero. They are exactly one full-circle rod per such clock, with a fixed-origin initial nonzero state and internal path returning to it. There is no extra start-time integral for this sector. Its zero-hop states are included. Histories remaining at zero contribute the vacuum term one. Thus no excited ancillary sector has been omitted, and no beta-l or cyclic-root correction is missing.

With T the path adjacency on K-1 vertices and v=e_1+e_(K-1), the absolute densities are

    A(l)=t^2 exp(-Delta l) v^T exp(t l T)v
        <=2t^2 exp[-(Delta-2t)l],
    W0=exp(-beta Delta) Tr exp(beta t T)
        <=(K-1)exp[-beta(Delta-2t)].

The first bound follows from ||v||^2=2 and ||T||<=2. Ordinary starts range over measure beta. Wraps have no such factor. At finite volume the complete weighted measure is finite.

## 3. The signed theorem applies, including its factorial normalization

I checked the primary [Ueltschi paper, Theorem 1 and equations (3)-(4)](https://arxiv.org/pdf/math-ph/0304003v3). It assumes a finite complex measure, a symmetric measurable f, |1+f|<=1, and an integral smallness condition using |f| exp(a). It proves convergence of the connected expansion and bounds the rooted series. These hypotheses do not require nonnegative pair weights.

In standard notation C_n=sum over connected graphs of product f, its rooted conclusion is

    sum_(n>=2) 1/(n-1)! integral product_(i=2)^n |dnu_i| |C_n|
        <= exp(a(root))-1.

This is the needed subtraction, not an unjustified stronger version of an unrooted estimate. Inflate nu by exp(mu), leaving f unchanged; the theorem then pays one exp(mu) for each nonroot rod. Multiplying f itself by exp(mu) would generally break |1+f|<=1 and is NOT the argument used here.

For a root of ordinary length l, circular overlap starts have measure min(beta,l+l')<=l+l'. The KP left side is bounded by

    4 Dbar exp(a0)t^2(l/d+1/d^2)
      +2 Dbar exp(a0+b beta) W0
    <=16 Dbar(t^2/Delta)l+34 Dbar r^2
    <=b l+a0.

The constants are correct: the length term uses exp(a0)<=2 and d>=Delta/2; the endpoint ordinary contribution is <=32 Dbar r^2; the wrap contribution is <=2 Dbar r^2. A wrap root sees ordinary start measure beta, so the same conservative expression at l=beta suffices. This checks the criterion pointwise in the complete trajectory label, including wrap roots.

## 4. Winding, Fourier grouping, and the local norm

An ordinary excursion enters and leaves the path graph on {1,...,K-1}. Its flux parity is odd exactly when these endpoints differ. There are no multiple full windings within a first-return excursion. A never-zero wrap cannot traverse the closing edge and has flux parity zero. Thus each rod carries either one s_g or no flux, and each connected cluster has precisely one Fourier character, with parity cancellations allowed. Pair factors contain no s.

For a Fourier support A containing g, the contributing cluster contains at least one winding rod on g. Summing over all such possible markings overcounts rather than undercounts. A cluster with n rods contributes with 1/n!; marking one of its n positions converts this to the rooted 1/(n-1)! above. This prevents an unnoticed factorial loss. Absolute convergence permits grouping by Fourier character on the entire formal cube before restriction to allowed syndromes.

The spatial clock set of a nonzero connected cluster is connected in the ambient overlap graph. Any two clocks in its flux support therefore have ambient distance at most n-1, even when intermediate clocks have no net flux. The exp(mu) factors on nonroot activities pay the desired diameter weight. The marked rod's start integration is beta, cancelling the free-energy factor beta^-1.

The winding densities are

    A_w(l)=2t^2 exp(-Delta l)[exp(t l T)]_(1,K-1),
    A_min(l)=2t^K exp(-Delta l)l^(K-2)/(K-2)!.

Their singleton contribution has coefficient -J0(1-Q), where

    J0=2t^K/Delta^(K-1),
    Q=exp(-B)sum_(j=0)^(K-2) B^j/j!.

It is correct to leave isolated-clock normalization and interacting wrap effects to multi-rod clusters. They are not absent merely because this raw one-rod coefficient is unnormalized.

It follows that F_beta(s)=c_beta-J0 sum_g s_g+sum_(A nonempty)r_A product_(g in A)s_g satisfies

    sup_g sum_(A containing g) exp(mu diam(A))|r_A|
      <= J0 Q + integral_0^beta(A_w-A_min)dl
                 +integral_0^beta A_w(l)[exp(a0+b l)-1]dl.

No division by the number of marks is needed for this upper bound. A singleton flux-dependent cluster is necessarily a winding rod; thus the separation of singleton and multiple-rod contributions is exhaustive.

## 5. Independent check of the final constants

Let L=K-2. A path from 1 to K-1 has L+2j steps. Its j=0 path is unique and the number at j>=1 is at most 2^(L+2j). Extending the positive duration integral to infinity gives

    integral(A_w-A_min)/J0 <= 2^K r^2/(1-4r^2).

For the charged integral, the count is also bounded by binomial(L+2j,j). Since

    L!(2j)!/[j!(L+j)!] <= binomial(2j,j) <=4^j,

the path-series bound yields

    A_w(l)<=2t^K exp[-(Delta-2t)l]l^L/L!.

Using exp(a0+b l)-1 <= exp(a0+b l)(a0+b l), extending to infinity, and evaluating the two gamma integrals yields the upper bound

    2[a0(Delta/d)^(K-1)
      +(b/Delta)(K-1)(Delta/d)^K]
       <=64 K 2^K Dbar r^2.

Thus the claimed explicit relative estimate is valid:

    sup_g sum_(A containing g) exp(mu diam(A))|r_A|/J0
      <= Q + 2^K r^2/(1-4r^2)+64 K 2^K Dbar r^2.

For fixed K,D,mu, r can first be chosen small, followed by B large. This establishes the volume-independent local premise, not merely a small extensive free-energy density difference.

## 6. Exact failure of the stronger pinned-boundary claim

Take commuting checks S_g=X_1 X_2 and S_h=Z_1 Z_2, each identity-padded to K>=3. Freeze clock h at a nonzero prefix F_h=Z_1, with no h-hops. Then a complete g-loop acquires chi(S_g,F_h)=-1. In the restricted g problem the flux is consequently -s_g rather than s_g, reversing its leading singleton free-energy term. An arbitrary excited pinned boundary therefore cannot obey the same uniform -J0 s_g reference plus o(J0) local remainder on adjacent checks.

This is not a counterexample to the full trace theorem: the corresponding excited histories in the unconstrained trace are wrap rods whose fugacity is explicitly paid by the third smallness inequality. It is a counterexample to extending that theorem to arbitrary pinned excited boundaries without charging boundary terms. Deletion of checks with reconstruction of the remaining specified clock model is different and retains the proof.

## Final interface statement

The audited free-energy theorem provides the weighted local influence bound for the exact unconstrained ancillary trace. At mu=0 it supplies the scalar premise in `ROOT_CONDITIONAL_THERMAL_TRANSFER.md`. Whether an actual trace deletion changes precisely the charged syndrome set, admits a valid injective decoder witness map, and preserves the required entropy estimate is a separate code-family proof. The Davies consumer additionally requires its stated enlarged-footprint correctability, bounded rates, Gibbs stationarity, exact thermal encoding and endpoint assumptions. Nothing here promotes that semigroup result to a finite-coupling microscopic bath theorem or robustness under generic native-Hamiltonian errors.

## 7. Extended audit of the integrated join

After writing the scalar audit above, I additionally reviewed `ROOT_NATIVE_THERMAL_MEMORY_JOIN.md` and `TRACE_WITNESS_TRANSFER_AUDIT.md`. **The stated joins are valid under the enumerated exact-model assumptions; I found no additional fatal chain-interface gap.** This does not independently reprove every code-family combinatorial lemma, and it does not certify the historical comparison paragraphs.

I checked the primary [actual-code source, Lemma 5.2, Lemma 5.8, and Theorem 5.13](https://arxiv.org/html/2605.10943v1). They supply, respectively, the sufficient vanishing-residual stability condition, validity of the removed witness as a coboundary, and the exponentially small residual-event probability. The witness receipt uses the sufficient stability implication in the correct direction. The conditional-sector translation argument changes only the Boltzmann ratio; it does not assume conditional independence of witness blocks. Its combinatorial counting step can therefore use the source's same witness enumeration.

### The weakest interface: enlarged contacts and ideal encoding

The main place where an incorrect upgrade could have entered is the passage from a rare syndrome event to protection against clock-containing, spectrally resolved contacts. That passage is valid here only because of four exact facts:

1. Fix the contact footprint bound b **after** conjugation by U. The good set excludes every translate of either CSS bad set by every data Pauli of weight at most b. Every Pauli prefix then stays outside the original bad set. Sequential application of the single-qubit decoder identity proves the identity for every b-supported Pauli, hence by linearity for arbitrary data operators on that footprint. The enlargement costs a fixed polynomial in n and an n-independent Boltzmann factor, not an exponential-in-n loss.
2. In this same fixed decoder frame, all energy projectors are identity on the logical factor within each syndrome. The algebra generated by footprint-supported data Paulis, syndrome projectors, and arbitrary ancillary coefficients is closed under multiplication and adjoints. Left and right spectral projection remain inside it. Consequently exact frequency resolution cannot add a different logical action; this is stronger than an assertion that it merely preserves the list of syndrome changes.
3. The full dissipator, not merely its jump, has two-sided support on the enlarged bad projector. In particular J^dagger J is in the same protected algebra. This makes the logical derivative bounded by bad probability even for ancillary coefficients with global support. The norm identity

       sum_omega A_omega^dagger A_omega
         =sum_E Pi_E A^dagger A Pi_E <= ||A||^2 I

   avoids an exponential count of frequencies. It requires coherent summation within each genuinely degenerate Bohr-frequency component.
4. The initial gauge/clock state is the **exact Gibbs marginal** tau_Ga, not a projected clock vacuum or an arbitrary data code state. Its system state satisfies omega(0)<=2rho_beta; Gibbs stationarity preserves this domination. The ensuing bound on bad probability is valid along the entire trajectory without a mixing theorem. Reference trace-norm duality then yields the quoted 12 Gamma T p_bad bound.

These are genuine hypotheses/identities, not robustness-by-continuity claims. Changing the Hamiltonian so that exact logical independence fails, changing endpoints to cold product clocks, or resolving logical degeneracies with separate rank-one bath jumps invalidates this chain and needs a new argument. Among the implementation gaps, the ideal Gibbs endpoint and exact Hamiltonian assumptions are particularly consequential; neither is provided by the free-energy theorem.

### Parameter compatibility and resource accounting

Choose r so that the r-dependent terms in epsilon are below a fixed epsilon_*<1. Then choose B large enough for the thermal inequality, the residual Q term, and the witness threshold

    2 beta J0(1-epsilon)=4 B r^K(1-epsilon).

All can hold simultaneously because the first thermal requirements improve as B grows and the witness expression grows linearly. Setting Delta=J0/(2r^K), t=r Delta, beta=B/Delta is consistent. There is no hidden volume-dependent coupling in this choice. Since both check incidence and check size are uniformly bounded, the number of clocks is O(n), so passing from data-qubit count to total native-site count changes no stretched-exponential exponent. Each clock is a fixed seven-level system; this is not a qubit-only two-body implementation.

### Conditions that must appear in the final theorem statement

- The particular source family and decoder supply the cited witness and single-qubit stability properties; enlarged contacts use the same decoder frame.
- Exact controlled-Pauli clock Hamiltonian, fixed K=7, bounded check geometry/incidence and the explicit thermal inequalities, with epsilon<1 and the inherited witness threshold.
- Full ancillary trace at sufficiently low nonzero temperature; free/deleted-check or periodic versions remain within the scalar theorem. Arbitrarily excited pinned boundaries are excluded. A changed boundary code also needs its own witness properties.
- Diameter uses ambient overlap-graph distance; physical distance incurs the fixed range factor.
- Arbitrary fixed-dimensional qubit-qudit couplings are allowed; no claim for restricted exchange interactions or qubit-only hardware follows.
- Bounded-support native bath contacts, bounded spectral rates, independent channels or explicitly bounded local correlation blocks, total charged strength O(n), and Gibbs stationarity at the same beta. A Lamb shift must be omitted or separately bounded.
- Exact coherent Davies frequency blocks, not a bath that additionally resolves logical degeneracy.
- Ideal Gibbs gauge/clock initialization and ideal dressed terminal decoding, including clock access; no efficient/noisy endpoint theorem.
- The retention bound is for the specified Davies semigroup. It is not a uniform finite-coupling microscopic bath result over stretched-exponential times, not generic calibration-error robustness, and not a historical novelty certification.

With these conditions, the final integrated mathematical statement is supported by the audited component interfaces. The broad physical capability remains conditional on implementation assumptions deliberately outside that statement.

### Reviewed-artifact binding

The integrated join reviewed in Section 7 has SHA256 `ef36d30269ac829b5006b795f937e162cf042673c915955e92a46dcf05ea73cb`. The scope of this verdict permits a subsequent status-only change from audit-pending to internally reviewed, and an explicit clarification that overlap distance means ambient overlap-graph distance. Neither changes the audited mathematics. A subsequent prior-art appendix is not certified by this audit and must not alter the claimed theorem's assumptions or proof.

Other audited inputs at review time:

- `root_rod_audit.md`: `43b847eddc40ed237bb31313e7623504413ddd60a369504cf612e24e7dafbf6f`.
- `independent_constructor.md`: `5c8200818c8cc3c1612fc0628c8181ad6ce99a0450af17e961f27008b01f4be1`.
- `ROOT_CONDITIONAL_THERMAL_TRANSFER.md`: `a598874f9d50b929f72f3ac5f3398f93bbe0d69c965d445fa26b28496c0d1c90`.
- `dynamics_audit/CONDITIONAL_DAVIES_CONSUMER.md`: `6090bf4f3135ea2ea7d25230f9e6ac22a17ca9b67282c085290abbfb91cef5c6`.
