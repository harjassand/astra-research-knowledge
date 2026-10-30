# A local-stochastic initializer can enter the continuous-noise memory basin
2026-10-30. Root derivation candidate; not independently reviewed. This supplies an interface, not a preparation algorithm.

## 1. Actual input contract
Use the accepted constant-rate Tanner simple compiler and its exact frame/ideal logical gauge. Suppose a preparation procedure supplies a decoded target logical state/channel with residual error described by a local-stochastic support set E on O(N) physical sites: for every prescribed S, Pr(S subset E)<=p^|S|. Conditional on E the error may be an arbitrary CPTP operation on those sites and a retained environment, independent of the logical input at the support-sampling level. Auxiliary initialization is the specified ready state before these faults. Every initialized bath is initially logical-independent before preparation; correlations produced by preparation are retained, not erased at the handoff.

A bounded-depth initialization circuit or frame inverse enlarges each fault support by a fixed factor and incidence. Absorb that enlargement into the following footprint constants. This is NOT permission to treat an arbitrary globally correlated or only logically correct preparation output as local stochastic.

## 2. Initial weighted moment from explicit support incidence
Each physical fault site can change at most k augmented syndrome/energy/actual-flag vertices. Each such vertex can be affected by at most b fault sites. Let Gamma(E) be their union. Relative to encoded/ready vacuum, any DATA-Pauli/controller operator term supported on E changes occupancy only inside Gamma(E). Hence for every animal A and every conditional quantum output,

    expectation(f_A) <= exp(a|A|) theta^(|A|-|A intersect Gamma(E)|).

This bound keeps coherent Pauli terms: the whole conditional output lies in the joint-label subspace whose occupied labels are contained in Gamma(E). It is not a Pauli-mixture assertion.

For any S subset A, choosing one incident faulty site per hit vertex gives at most b^|S| choices, with at least |S|/k distinct faults. Local stochasticity therefore gives

    Pr(S subset Gamma(E)) <= b^|S| p^(|S|/k).

Expanding the positive product yields

    E f_A <= [exp(a)(theta+b(1-theta)p^(1/k))]^|A|.

If the rooted animal count is at most A0^m and p is sufficiently small that

    A0 exp(a)(theta+b(1-theta)p^(1/k))<1,

then E V_+<=C N and E W_+<=C' N. The CP-dressed F<=V_+ inherits the initial O(N) moment. Constants may be extremely poor.

## 3. Component and logical safety at the initial handoff
This section uses the LINEAR Tanner cutoff ell=c_*N, not the sqrt(N) HGP cutoff. On a support event with |E|<=alpha N, every Pauli term in the dressed preparation error has DATA weight <=s_f alpha N, where s_f is the fixed support-expansion factor. Choose alpha so 2s_f alpha N is below both the code distance and a fixed fraction of ell. Every sectorwise minimum representative then has weight below ell, hence safe components, and the actual Pauli and canonical representative differ by a stabilizer, not a logical operator. The whole common error span factors as identity on the logical subsystem in the canonical gauge.

For M_f<=c_f N possible fault sites, a union bound gives

    Pr(|E|>=alpha N) <= binom(M_f,ceil(alpha N)) p^ceil(alpha N)
                     <= (e c_f p/alpha)^(alpha N)

(up to harmless integer rounding). Taking p small makes this exponentially small. No independence of faults is required. This conservative total-weight argument is sufficient for the linear-cutoff family; it must NOT be reused for fixed-density errors with a sqrt(N) cutoff.

## 4. Initial raw-potential cutoff and subsequent evolution
Restrict first to the preceding good support events, without measuring a quantum syndrome. In canonical logical coordinates their aggregate CP preparation map has identity logical action, with arbitrary syndrome/controller/environment state independent of the logical input. Let P be the accepted raw-potential/component basin projector. Since F>=V_0 and the initial moment is O(N),

    Tr((I-P)rho_good)<=C N/M,

where M=exp(cN) is the raw barrier cutoff; component safety has already been ensured by the support event. Gentle projection bounds the initial full-versus-P-compressed state difference by O(sqrt(N/M)), uniformly with a reference. The initial killed state still factors as logical input tensor ancilla, because P acts only on the canonical syndrome/controller factor.

Apply the accepted continuous-noise drift and killed-process theorem from this unnormalized initial state. Its initial F moment remains O(N), so the time-dependent comparison is unchanged up to constants. Combining initial support failure, initial projection and later evolution gives

    logical diamond error <= C N^(3/2)(1+t) exp(-c' N),

with an additional preparation logical-error term if the preparation only approximates the desired encoded target/channel. The fixed constants can absorb polynomial factors and exponent reductions. Correlations retained from preparation are allowed; replacing them by a fresh bath is unnecessary.

## 5. Consequence and limit
A preparation theorem supplying an actual local-stochastic residual (or the stronger support-CPTP contract above), with explicit feedforward/control and resource costs, can feed the continuous-noise finite-controller memory without an ideal cleanup step. A theorem certifying only success after its own ideal final recovery does NOT supply this interface automatically. In particular the exact residual basin structure, classical decoding latency, data errors during that latency, and initial controller setting must still be constructed/accounted for.

This note does not prove noisy Bell-resource preparation, efficient syndrome inference, an autonomous preparation/readout mode switch, or a practical threshold. It is an explicit initialization robustness extension conditional on an independently established preparation output contract.
