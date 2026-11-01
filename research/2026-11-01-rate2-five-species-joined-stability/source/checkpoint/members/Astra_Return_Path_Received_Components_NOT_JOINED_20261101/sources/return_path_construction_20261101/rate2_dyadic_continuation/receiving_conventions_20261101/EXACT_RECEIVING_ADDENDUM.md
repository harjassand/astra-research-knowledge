# Exact receiving conventions for the unchanged dyadic-stage source

The independent receipt `../audit_stage_20261101_0422/SOURCE_BOUND_ACCEPTANCE.md`
(SHA256 b96a909e99ed17b463bca5bacaf4ed340a4b65109c3ad41c1fdad09887487dd0)
is received unchanged. Its controlling derivation is `MATHEMATICAL_REVIEW.md`
(SHA256 46e2267d5a64ee29709998f4fbe220f2a7671793c05714fd6bc28f7a54940272),
and its audit manifest SHA256 is
9ed6e2b42e125858062732de73373290f63ca7d95be5cc9ebc579000f870950a.
The exact original stage source remains unchanged at SHA256
0ddcfb78c068ae58c2e5ddae1da015ba70d76acae67a2b0e9104f7358775e0a2.

The independent 1,393-assertion audit accepts the conditional full-chain stage
and its carefully stopped composition, subject to these controlling conventions:

1. **Actual total-count band exit has priority over a simultaneous L hit.**
   Only an L hit whose post-jump total remains in the band supplies the next
   stage entrance. Immigration can hit both boundaries on one actual jump.
   Auxiliary events include the common stop's terminal jump.
2. A final dyadic-stage endpoint is bounded above by `2 delta N+1`, not
   necessarily `2 delta N`. For the literal positive-fraction interface, stop
   instead at the first actual `L>=delta N`, giving
   `L in [delta N,delta N+1] subset [delta N,2 delta N]`.
   This does not add time or failure probability.
3. An upper total-band exit is not service. A consumer must separately receive
   starting headroom and charge immigration over the paid horizon; permitted
   stage entrances may already be at the upper band edge.
4. A lower exit is relative to fixed reference N. It is not automatically a
   fixed fractional decrease from each allowed entrance total.

Under these conventions the original deadline `16sqrt(Nm)/m^2`, stage failure
bound `16exp[-m/(3*10^12)]`, geometric deadline sum and composed failure bound
`32exp[-m0/(3*10^12)]` are unchanged. The state and reference N are never reset.
Only analysis clocks restart at genuinely received continuing-state entrances.

No initial phase, arbitrary-state entrance, interior service, recurrence or
stationary moment is granted by this addendum. The earlier mesoscopic source's
brief entrance sentence is not received as a separate theorem by this audit.
No deterministic source or numerical check is used as a stochastic service.
This addendum changes no existing frozen or audit payload.
