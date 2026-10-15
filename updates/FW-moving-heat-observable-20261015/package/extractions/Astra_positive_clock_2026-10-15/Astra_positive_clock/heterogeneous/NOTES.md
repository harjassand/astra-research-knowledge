# Heterogeneous rare-clock experiment and reusable-law compiler

Synthetic mathematical test only; no physical interpretation, canonical edits, or priority claim.

## Family

Independent binary reversible components with stationary target probability 1/2 and relaxation rates lambda_i=5^(-i)(1+i/(10n)), i=0,...,n-1. All rates are distinct. The count-of-target-components process is not Markov/lumpable by exchangeability. This does not exclude other structure or approximate reductions. q=2^-n.

At n=128, moment diagnostic q B/A^2 is about .416 and the mean-matched atom-preserving exponential has a roughly .145 Laplace-transform discrepancy on the tested scaled arguments. Direct Brown costs 2^128-1 marks on average. The stationary product-ODE closure from the previous experiment uses hazard q*(sum lambda_i)/2, hence predicts a mean of order 2^n rather than the exact scale of order 5^n. This closure fails dramatically on the hitting-time scale here.

## Exact positive rate compiler

For epsilon=.05 choose b=ceil(1+log2((n+1)/log(1+epsilon))). First round each rational input rate down to b significant binary bits, then perform exact positive distribution convolution, rounding every resulting positive sum down to b significant bits. Keep zero distinct. Integer probability counts are exact (common denominator 2^n). All dyadic rate numerators use a single power-of-two denominator.

Every tuple's rounded total obeys Lambda_hat <= Lambda <= g^(n+1) Lambda_hat, g=1+2^(1-b). Use the same geometric count and same exponential numerator for every Brown mark. Consequently H <= H_hat <= g^(n+1) H, deterministically, including H=0. There is no q^-1 error amplification for this pathwise rate error. At n=128 the bound is 3.1991362%; 5,561 occupied positive rates use at most 308-bit integer numerators and an overall 2^307 denominator. Exact compilation took about .1 second.

This avoids geometric-grid rational powers. A worst-case binary component update takes O(K) integer operations; K <= O((n/epsilon) log(n lambda_max/lambda_min)). Local distributions with more support require the corresponding extra convolution factor. Bit complexity must charge rate numerator and probability denominator lengths, not just arithmetic counts.

For native algebraic spectral weights, approximate each local categorical law to TV O(delta*q/n), preserving its zero mass. The same geometric-mark coupling then loses at most delta. This needs precision proportional to log(1/q), polynomial in the rational input length, but cannot be omitted. This experiment instead uses exact binary probabilities.

## Interlacing mixture and exact certificate

For compiled positive rates lambda_j with masses w_j, set D(s)=q+s sum_j w_j/(s+lambda_j). H_hat has atom q and exponential-mixture components with rates r_j, one in (0,lambda_1), then one in each (lambda_(j-1),lambda_j). Their weights are a_j=q/[r_j sum_l w_l lambda_l/(lambda_l-r_j)^2]. These formulas are classical renewal/interlacing machinery, not a novelty claim.

Floating secular root finding only proposes candidates. certify.py verifies bracket signs and residue enclosures with integer divisions, not trusted floating signs. Because w_j=c_j/2^n and q=2^-n, the secular equation is 1-r sum_j c_j/(lambda_j-r)=0. For dyadic r=a/D, sum the exact rational terms a*c_j/(D*lambda_j-a) with outward fixed-point intervals. At P=228 fractional bits, each integer division gives a rigorous floor, and the total rounding width is at most K units. Signs are accepted only when the entire interval lies to one side of one.

Given a root bracket [a/D,b/D], bound each positive derivative term r*c_j*lambda_j/(lambda_j-r)^2 by replacing its numerator and pole-distance denominator by interval extrema. Reciprocal summed bounds enclose the mixture mass. No estimate of uncomputed roots is necessary: subtract the certified retained lower masses from 1-q to obtain an exact total residual mass bound. Assigning that residual arbitrarily costs at most that mass in coupling/TV. Preserve q separately.

mixture_certificate.json contains the dyadic brackets and weight intervals; dyadic128_exact.json supplies the exact compiled rates/counts. The first low-accuracy run retained 141 roots with certified residual <=8.421e-5 in 2.33 seconds. Higher accuracy results are recorded separately. The retained root locations can be sampled using rational categorical masses and finite-bit exponentials; the benchmark floating draw loop does not by itself certify those transcendental draws.

## Comparators and limits

Keeping only the final 10 slow physical gates gives a Laplace gap below 8.6e-5 at the seven tested points, but changes the zero atom to 2^-10. Thus its multiplicative-coupling failure is at least 2^-10-2^-128, independently of Laplace agreement. Failure tolerance 1e-6 requires retaining at least 20 half-probability gates even for this necessary atom test. Direct enumeration then has at least 2^20 states. This is not a lower bound for a clever hybrid that preserves the fast atom or compresses slow spectra.

The positive compiler is itself a structured approximation and should be entered in the comparator ladder. It removes repeated per-draw Monte Carlo acquisition of stratum means and permits reuse of a positive mixture. It does not establish superiority over every possible slow-gate or hybrid method. Exact subset transforms at n<=18 are useful validation; agreement of finitely many Laplace points is not a full distribution certificate.

The prior work boundary includes positive distribution convolution/rounding (e.g. Li-Shi's relative-CDF sum FPTAS), Brown stationary renewal, and Fill-Lyzinski interlacing. The potentially useful construction is their contract-specific composition into an acquired reusable hitting-law sampler. No claim of historical originality follows.
