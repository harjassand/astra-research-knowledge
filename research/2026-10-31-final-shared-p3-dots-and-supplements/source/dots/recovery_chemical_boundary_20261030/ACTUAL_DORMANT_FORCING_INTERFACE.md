# Dormant forcing is a compensated occupation cost, not a return probability

30 October 2026. Exact stopped identity and a conditional bound. No complete return-cycle theorem.

Let the physical process be the nonbalanced extension in NONBALANCED_DORMANT_EXTENSION_V1.md. During a fast episode B=b>=q is fixed and total composition N is fixed until a connector event. Let r=N-H(b); fast reactions preserve r exactly. Let `w=exp(theta r)`.

Assume only for this calculation that the actual dormant continuation cost `G_D(A,C,b)` has been independently earned with the same-exponent bound

`0 <= G_D(A,C,b) <= M_theta w (1+A)^-m`, m=a0+2.

This is exactly the interface proposed, but not independently accepted, by DORMANT_WEIGHTED_GREEN_CANDIDATE.md. It is an assumption of the following receiving calculation, not a new proof of that Green.

Stop a positive-D episode at first connector event, first D=0 entry, or first A<K. The only D=0 entrance is `A'+D -> 2A'`, at D=1. Its physical rate is `k2 (A)_a0 a (b)_q`, and the output has A+1. The exact stopped compensator gives

`E[G_D(X_tau); D=0 exit] = E integral_0^tau 1_{D=1} k2 (A)_a0 a (b)_q G_D(A+1,C,b) dt`.

For A>=a0 and a=A-a0,

`(A)_a0 a (2+A)^-m <= C/(1+A)`.

Consequently

`E[G_D(X_tau); D=0 exit] <= C_theta (b)_q w E integral_0^tau (1+A)^-1 dt`

and, because A>=K before this stopping time,

`E[G_D(X_tau); D=0 exit] <= C_theta (b)_q K^-2 w U_tau`,

where `U_tau=E integral_0^tau A dt`.

The crucial factor is TWO inverse powers relative to actual A-occupation. A small unweighted dormant-return probability is unnecessary on this stopped high-A region. The extra reaction `2D->A'+D` cannot enter D=0 because its rate vanishes at D=1, so it contributes no hidden boundary term.

## Exact limitations

1. This is not a bound uniform in an unbounded catalyst count b: the explicit `(b)_q` must be retained. At the section b=q it is a fixed constant. Histories with arbitrarily many high-phase activations require their actual weighted enumeration.
2. The low-A stopping boundary is NOT paid. Its omitted term is `E[G_+(X_tau); A<K before other exits]`, where G_+ must be the true continuing cost. Setting it to zero would incorrectly prove a global coupling result.
3. The same-exponent dormant Green bound is still a candidate input. Product-Poisson finiteness from each finite input does not alone establish its uniform incoming-profile norm.
4. Multiplying separate probability and output-moment estimates would miss this occupation comparison. The compensator retains their dependence exactly.

This identifies the real remaining coupling problem more sharply: earn the low-A positive-D continuation cost relative to the SAME occupation margin, rather than replacing it by a scalar `n^-delta` bound. The earlier scalar estimate can be much larger than U when C grows at fixed A, so it does not close the omitted term.
