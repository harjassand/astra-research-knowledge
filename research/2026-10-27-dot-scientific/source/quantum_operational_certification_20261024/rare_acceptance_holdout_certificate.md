# Rare-acceptance holdout: linear-in-inverse-signal validation attempts

2026-10-27. New self-contained statistical refinement, independent audit requested. It applies to the same fixed decoder, fresh program batches, six-state holdout and stationary trusted-interface setting as `programmed_decoder_holdout_operational_certificate.md`. It certifies the effective instrument, not the source model or stationarity assumptions.

## Fixed experiment and observed test

For each of N independently repeated attempts let A indicate acceptance and B indicate acceptance AND matching the prepared six-state qubit. Let

 z=Pr(A=1), f=Pr(B=1), theta=f/z if z>0.

The six-state identity is f=(z+2w)/3 for the subnormalized qubit Choi singlet weight w. Consequently theta>=7/8 implies w/z>=13/16, exactly the existing assisted hashing threshold.

Fix0<p0<=1 and confidence failure0<delta<1 BEFORE collecting any data. Set

 N=ceil[16000 p0^(-1) log(4/delta)],
 k_min=N p0/20.

Let K=sum A and J=sum B. PASS precisely if

 K>=k_min and J/K>=15/16.

On passing, report z_L=K/(2N). With probability at least1-delta the following implication is valid simultaneously:

 PASS => z>=z_L>0 and theta>=7/8.

Thus the actual effective decoder has the certified asymptotic two-way-assisted entanglement rate

 z_L h0/(n_train+1), h0=[13log2(13)-48]/16>0.

No source-isometry/reset assumption is needed for this validity statement. The choice p0 is merely a preselected test tuning parameter; it need not truly lower-bound any physical decomposition for the confidence implication to remain sound.

## 1. Soundness of acceptance lower bound

K is binomial(N,z); put mu=Nz. Its moment generating function obeys E[2^K]=(1+z)^N<=exp(mu). The event K>=k_min and z<K/(2N) requires K>2mu and K>=k_min. Markov's inequality at exponent log2 therefore gives

 Pr(K>=k_min and K>2mu)
 <=exp[mu-(log2) max(2mu,k_min)]
 <=exp[-(log2-1/2)k_min]
 <=exp[-k_min/6].

This bound is uniform in the unknown z, including tiny z. It justifies the data-dependent lower bound K/(2N) on the pass event without an invalid optional-stopping argument.

## 2. Soundness of conditional fidelity test

The pairs(A,B) have the three outcomes reject, accepted mismatch, accepted match. Conditional on K=k>0, J is exactly binomial(k,theta), even when acceptance depends on the prepared input state. For theta<7/8,

 Pr(J/K>=15/16 | K=k)<=exp(-k/128)

by elementary Hoeffding. Summing over all k>=k_min bounds the bad-fidelity pass probability by exp(-k_min/128). Since k_min>=800log(4/delta), the sum of both soundness failures is less than delta. If z=0, K=0 almost surely and passing is impossible. No assumption of input-independent acceptance was introduced.

## 3. Discovery for the noise-adapted receiver

Suppose now, only to establish discovery, that the complete effective qutrit instrument is within unhalved diamond error nu p of accepted identity weight p/9, with p>=p0 and0<nu<=1/270. After the trusted qubit embedding/projection,

 z>=p/9-nu p/2>=59p/540>p/10,
 theta>= (1/9-nu/2)/(1/9+nu/2)>=59/61,
 59/61-15/16=29/976>1/40.

A binomial lower-tail bound gives Pr(K<mu/2)<=exp(-mu/8)<=exp(-Np0/80). On its complement, K>=mu/2>=Np0/20=k_min. Conditional Hoeffding then bounds the probability J/K<15/16 by exp(-k_min/800)<=delta/4. The count-tail bound is also at most delta/4. Therefore the decoder passes with probability at least1-delta. On this discovery event,

 z_L=K/(2N)>=z/4>=59p/2160>p/40.

Combining the two concentration arguments if both soundness and discovery are desired simultaneously costs at most their sum; each is individually stated at confidence1-delta, or run the construction with delta/2 for joint confidence1-delta.

## Resource consequence and restrictions

The number of validation ATTEMPTS is O(p0^-1 log(1/delta)), not the additive-Hoeffding O(p0^-2) budget. Every attempt still consumes n_train+1 original channel calls. Using the received quadratic-training receiver gives total startup validation cost O(p0^-3 polylogarithms) for fixed relative accuracy, not O(p0^-2). Subsequent data attempts continue to consume fresh program batches.

Under the discovery promise the reported asymptotic rate is at least p h0/[40(n_train+1)] on the discovery event; its validity rests on the soundness event as just distinguished. No finite-block hashing theorem, reusable learned device, unassisted capacity, device independence, adaptive repeated peeking, or entropy-model certification is claimed. Any equally informed fixed generic decoder can use this same statistical test.

## Elementary validation-attempt lower bound (black-box effective-instrument scope)

The inverse-signal exponent in validation attempts cannot be removed in the model-free black-box effective-instrument setting. Compare the null instrument that always erases with the alternative that transmits the input perfectly with probability a=p/9 and otherwise erases. On N independent attempts the alternative produces only erasures with probability(1-a)^N, independent of the chosen data inputs. Conditioned on this event the observed effective-instrument transcript is identical to the null transcript. Even allowing randomized decisions, any test passing the null with probability at most delta must therefore fail the alternative with probability at least(1-delta)(1-a)^N. Completeness at least1-delta requires

 N>=log[(1-delta)/delta]/[-log(1-a)], for0<delta<1/2.

For a<=1/2, -log(1-a)<=2a, so this is Omega(a^-1 log(1/delta)). It matches the sufficient signal exponent above.

This lower bound concerns validation from the effective instrument's data/acceptance outputs. It is NOT a minimax lower bound on all physical-channel calls when the validator is additionally allowed to inspect training systems, exploit a source promise, redesign the decoder, or use a different physical experiment. In particular it does not prove the p0^-3 startup resource product is globally optimal.
