# Reward-weighted acquisition of moving-token exchange bounds

30 October 2026. New local construction, NOT a whole-network extension. Reviewed fixed-pool sources are unchanged.

## Why an exchange has only one ordinary-label displacement

Suppose one particle is distinguished as a protected token. At entry to a finite hidden excursion its physical type leaves D and follows a token phase p. Ordinary labels retain their types throughout the excursion, except possibly at its terminal restoration. If an ordinary label of type i restores D, protect that restored particle and give its ordinary label identity to the old token, whose terminal type is p. The ordinary population has undergone exactly i -> p. If the old token restores D itself, the ordinary population is unchanged. This is an identity convention, not alteration of a physical reaction. It preserves every physical count. It requires exactly one token and the stated frozen-ordinary-phase structure; general ordinary rearrangements cannot be silently included.

Thus the obstacle is not intrinsically a multi-label simultaneous reset. It is the intensity of this single-label exchange in the traced clock.

## A stopped reward-potential certificate

Fix the ordinary configuration y and an entry channel e into token phase p_e. Its trace-clock rate is lambda_e(y). During the deleted excursion let J be its finite phase process, stopped at its ACTUAL first restoration or other terminal exit tau. Ordinary counts y_i are frozen up to tau. Let an ordinary type-i restoration have physical intensity y_i h_i(J,y); marks that restore the token itself are separate. Let Q_y be the killed generator on the transient token phases, including all actual exit rates.

For each ordinary type i acquire a nonnegative finite function psi_i(p,y) satisfying

    -Q_y psi_i(p,y) >= h_i(p,y),
    sum_e lambda_e(y) psi_i(p_e,y) <= b_i,

uniformly over admitted y, with b_i a fixed finite constant. Set psi_i=0 at every actual exit. Localize before applying Dynkin if needed. Nonnegativity and Fatou give

    E_p integral_0^tau h_i(J_s,y) ds <= psi_i(p,y).

The ordinary-i restoration counter has at most one mark before the stopping event. Its compensator therefore gives the exact terminal probability

    P_p(ordinary-i restoration) = y_i E_p integral_0^tau h_i(J_s,y) ds.

Consequently the FULL trace exchange rate out of type i, summed over all terminal old-token types and all entrances, is bounded by b_i y_i. At y_i=0 there is no such exchange. This proves a source-label bound, rather than a bound on total excursion count.

Split this aggregate exchange uniformly among current type-i labels. Its per-label total intensity is <=b_i. Destination may depend arbitrarily on the current configuration, entry history and terminal phase. A potential residual clock of rate max_i b_i per label, with predictable thinning, realizes the exact trace exchange kernel. Added to existing baseline residual clocks, the no-residual-ring event suppresses these exchanges. The independent progress-clock forcing proof is then unchanged. This is a SUFFICIENT local forcing interface; no adversarial turning-off of fixed physical channels is used.

Assumptions for this trace representation: the deleted excursions terminate a.s.; the underlying process and the trace are nonexplosive after localization; all entry/exit kernels retain their actual state metadata. An infinite physical holding time, a projected non-Markov state, or deletion of a terminal seed/connector output is not allowed. If hidden phases remain relevant after exit, retain them as part of the trace state. Finite total trace rates on each finite state set suffice for the localized construction; a separate global nonexplosion proof is still needed.

## Exact finite acquisition, and what ordinary occupation fails to prove

For a fixed finite transient Q_y, the minimal reward potential is

    psi_i(y)=(-Q_y)^(-1) h_i(y).

For rational mass-action parameters it is a rational function of frozen counts. Verify nonnegativity, the killed-generator equation, and the aggregate entrance inequality on the admitted integer domain. The matrix inversion itself does not prove uniformity in y. Certificate synthesis must verify that inequality, not sample it.

Ordinary holding-cost acquisition corresponds to h=1. It supplies no bound for an unbounded h_i. This explains precisely why bounded face occupation and bounded ingress cost alone do not resolve moving-token reassignment.

For example a one-phase excursion with token-own exit rate mu s, ordinary-i exit rate beta y_i, and entry rate s (s>=1), has

    psi_i=beta/(mu s+beta y_i),
    s psi_i <= beta/mu.

Its trace exchange rate is exactly s beta y_i/(mu s+beta y_i), hence source-label bounded despite an unbounded entry rate. This algebra is an abstract kernel example, not an assertion that current raw chemical guards realize it.

In contrast, entry rate s, token-own exit mu s and ordinary-i exit beta s y_i yield psi_time=1/[s(mu+beta y_i)], so s psi_time<=1/mu; yet the exchange rate is s beta y_i/(mu+beta y_i). At y_i=1 it diverges with s. Thus even a perfect occupation/ingress certificate does not imply bounded exchange. The stronger reward certificate correctly rejects it.

## Exact scope of the consequence

This construction can acquire a moving-token exchange bound from an actual finite killed phase kernel. Combined with baseline reachability it restores the local deterministic-time forcing and cohort argument if all other label motions have their previously required exact splitting. It does NOT establish the positive-D reset, connector Green, signed cycle, physical cost or complementary-direction drift for a new network. Those depend on actual terminal outputs, conservation, birth/deletion accounting and the old phase interfaces and must be checked separately. It does not remove the fixed-pool assumption from any existing global theorem by declaration.
