# Optional twirl removal: exact corrected-span bound

2026-10-28. Addendum to GOVERNING_WRAPPER_v1.md; the earlier twirled protocol remains valid. This is the conventional exact quantum-error-correction span property applied to the explicit outer wrapper, not a new coding theorem.

Let T be the complete deterministic outer protocol, including both parties' decoding, measurements, forward classical messages, Bob's total syndrome decoder and correction, and discarding measured registers and any classical transcript. Its output consists of the prescribed logical pairs. All decoder failures remain actual CPTP branches; none is postselected. Let Phi_out be the rank-one projector onto the prescribed output Bell state and E=T^*(Phi_out). Then 0<=E<=I.

Let P_good project onto the span of the input Bell-basis vectors whose Pauli labels are nonidentity on at most t WHOLE inner blocks. The explicit syndrome/correction proof shows that every such vector |v> is sent to Phi_out, independently of syndrome outcomes. Therefore <v|E|v>=1. Positivity of I-E gives (I-E)|v>=0. By linearity E acts as identity on the entire good span. Hermiticity makes its off-diagonal blocks between good and bad spans zero; positivity on the bad span then proves

    E >= P_good,
    F_ent(T(rho)) = Tr(E rho) >= Tr(P_good rho)

for EVERY input state rho, including coherent superpositions of Pauli errors and correlations between blocks. This is an output-state fidelity assertion after classical records are discarded from the fidelity target. No assertion that the joint output-plus-record state has an ideal independent transcript is made.

For a product input rho=rho_1 tensor ... tensor rho_B, define p_i=1-Tr(Phi_m rho_i), where Phi_m is the full m-ebit projector of inner block i. The projectors onto the events 'inner block i is ideal Bell' and its complement commute on different blocks. Their virtual measurement distribution is independent Bernoulli(p_i), even when each rho_i has off-diagonal Bell-basis coherences. Consequently, if all p_i<=epsilon0,

    1-F_ent(T(rho)) <= Pr[sum_i Bernoulli(p_i)>t]
                         <= Pr[Binomial(B,epsilon0)>t].

Identical inner states are unnecessary; independence and the individual fidelity bounds suffice. Classical coupling to independent uniforms proves the last stochastic domination. A shared random seed whose conditional performance varies can invalidate productness after averaging; use independent inner seeds/apparatus or prove the required good-subspace weight directly. Marginal fidelity bounds alone do not imply a binomial tail for correlated blocks.

The same proof includes the small-field stripe implementation: if at most t whole m-ebit blocks are bad, all retained stripes have at most t bad sites. Every Bell-basis vector in P_good is therefore corrected simultaneously, and discarded leftover ebits do not affect the retained output. There is no stripe union factor.

Operational consequence: the actual bilateral Pauli twirl and its random keys can be omitted entirely for this reduced-output fidelity guarantee. The deterministic CSS circuit and forward syndrome messages remain necessary; this addendum does not make local control, acquisition, inner-block preparation or gate errors free. The original resource bounds can omit twirl gates/keys, without any claim of physical fault tolerance or superiority over conventional concentration plus the same outer code.
