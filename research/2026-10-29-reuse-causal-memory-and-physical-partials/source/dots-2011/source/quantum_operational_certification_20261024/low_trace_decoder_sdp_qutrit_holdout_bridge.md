# Direct SDP utility loss pays full-qutrit holdout mismatch

27 October 2026. Local post-cutoff. Dependency: independently received `low_trace_decoder_sdp_relative_learning_root.md` and the received full-qutrit holdout theorem. Separate receiving requested.

Use the SDP receiver's genuine/reset decomposition, with genuine signal weight p. Write a_s,f_s for genuine accepted mass and entanglement overlap, and a_n,f_n for reset. The reset is input independent, so f_n=a_n/9. Set

 L=(2/3)(p-a_s)+(a_s-f_s)+(2/9)a_n>=0.

For the complete qutrit accepted map, a=a_s+a_n, f=f_s+f_n and b=3(a-f)/4. Positivity gives

 a_s-f_s<=L, a_n<=9L/2, p-a_s<=3L/2.

Consequently

 b<=(3/4)[L+(8/9)(9L/2)]=15L/4,
 |a-p|<=a_n+(p-a_s)<=6L.                            (1)

These deliberately loose constants suffice; no Stinespring square-root bound is needed. The utility identity and these estimates remain valid with overlapping reset, provided the actual L is controlled.

For the received exact orthogonal-reset source, relative learning and exact SDP optimization give L<=10eta p. Given target holdout relative accuracy theta in (0,1], choose the SAME training accuracy parameter theta, hence

 eta=theta²/100000.

Then b<=(75/2)eta p and a>=p-60eta p>=3p/4. Therefore

 b/a<=50eta=theta²/2000<theta²/1536.                  (2)

This is the explicit completeness margin for `full_qutrit_unentangled_holdout_verification.md`. Supply its acceptance floor p0/2, not the source signal floor p0. The actual a>=3p/4>=p0/2 meets its premise, and its issued throughput lower confidence is at least p0/4.

For the learned-throughput reference-channel addendum, set theta=nu/2. Its certificate then specifies the classical estimated throughput ahat and complete target G_ahat with error<=nu ahat. Training accuracy nu/2 is enough for this SDP construction; no nu/16 reduction from the sequential-projector construction is needed. This changes constants, not exponents.

Training confidence and fresh holdout confidence are separate events. Conditional on good training, (2) gives completeness. Soundness of an issued holdout certificate remains uniform over every fixed CP accepted decoder, even if training was bad. The one-off training failure need not be observable. An additive SDP optimization error must be charged in L via the received optimization-tolerance bound before applying (1); no uncharged numerical optimizer accuracy is assumed.

Training retains O(sr/(p0 theta^4) polylogs) source uses, and holdout adds expected/high-probability O(log(1/beta)/(a theta²)) uses with deterministic p0-based cap. Both accepted and rejected holdout calls are charged; all learned quantum programs can be discarded. No structural certification or nonstationary-future guarantee is implied.
