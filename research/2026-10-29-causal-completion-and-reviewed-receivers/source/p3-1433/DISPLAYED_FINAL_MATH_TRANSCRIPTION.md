# Visible final with displayed formula transcription

This is a deterministic text projection of the normally displayed final response, with mathematical annotations retained. It is not a transferred original proof, implementation or completed review. Original visible text and private DOM are preserved separately.

The strongest completed working result is a universal compiler for offline reproduction of unknown noisy quantum channels. At fixed dimension and a supplied positive Choi noise floor, its optimal acquisition-call dependence is $\boxed{N=\Theta_{d,\nu}\!\left(M+\log\frac1\epsilon\right)}$ 

for reproducing  $M$  future uses to joint operational error  $\epsilon$ .

The construction samples executable operations directly from experimental outcomes. It does not first produce a highly accurate estimate of the unknown channel. This is a broader opening than another encoding-family extension, while the earlier spectral exchange and many-data decoder remain useful under their different contracts.

This is a constructive working derivation with executed finite checks. Independent review and historical priority remain open.

1. What the operation accomplishes

Let  $\mathcal E$  be an unknown, fixed, memoryless channel on a known  $d$ -dimensional system. Its normalized Choi matrix satisfies the supplied promise $J_{\mathcal E}\ge \nu\,\frac{I_{d^2}}{d^2},
\qquad 0<\nu<1.$ 

Acquisition uses ordinary known input preparations and measurements of fresh outputs. It finishes before the future payloads are processed. Independent Choi programs also suffice, with all steering failures and waiting counted.

The compiler constructs a finite catalog of known physical channels $\{\Gamma_v\}_{v\in V}$ 

and samples an index  $V$  from the experimental records so that $\boxed{\mathbb E_{\mathcal E}[\Gamma_V]=\mathcal E.}$ 

The receiver subsequently applies the known channel  $\Gamma_V$  to the supplied input. This equality is equality of complete quantum channels, including an arbitrary entangled reference, after averaging the internal acquisition record.

There are two versions:

Exact, variable acquisition: the number of source experiments is unbounded but almost surely finite, with a uniform finite expectation.

Bounded acquisition: a fixed global budget gives an approximation. Using fast sampling machinery, the error decreases exponentially with the budget beyond the amount needed for the requested number of uses.

No source-dependent quantum training system needs to remain in storage. The retained instruction is classical—but it is an instruction for one sampled use, not an exact reusable description of  $\mathcal E$ .

2. The central construction

The positive Choi floor places every allowed channel inside a compact part of the channel body’s interior. I constructed a finite polytope of physical channels that contains that promised set, with a known positive distance from every facet.

Its vertices provide the executable catalog. Positive barycentric weights satisfy $J_{\mathcal E}
=\sum_v \lambda_v(J_{\mathcal E})J_{\Gamma_v}.$ 

The remaining problem is to sample  $v$  with exactly these unknown probabilities.

Each facet distance is a known affine function of experimentally accessible probabilities. A Bernoulli factory converts fresh observations into a coin with that facet-dependent probability, without learning the probability numerically. Huber’s linear factory supplies an explicit finite-mean implementation. arxiv.org

I then use a rejection sampler whose acceptance weights are products of these facet coins. Its accepted output has precisely the required barycentric law. The geometry uses established Wachspress coordinates; I supplied the physical sampling construction and a polar-volume proof of the needed mean identity. akgillette.github.io

The mechanism uses positive physical operations throughout. Signed tomography coefficients appear only in the classical construction of probability-generating routines.

For a polytope with  $F$  facets in an  $m$ -dimensional affine space, a conservative explicit bound is $\mathbb E[T]\le (F-m)B\,\gamma^{-(F-m)},$ 

where  $B$  bounds the cost of a facet coin and  $\gamma>0$  bounds its success probability. This exposes the potentially enormous dimension and geometry costs.

3. Why the acquisition law is  $M+\log(1/\epsilon)$ 

Nacu–Peres’ fast Bernoulli-factory theorem lets the facet routines be chosen with exponential tails. I checked the relevant compact-domain conditions and proved that the complete rejection sampler inherits a uniform exponential moment: $\sup_{\mathcal E}\mathbb E_{\mathcal E}e^{\theta T}\le A$ 

for constants  $A<\infty$ ,  $\theta>0$  determined by the dimensions, noise margin and compiler. arxiv.org

Acquire  $M$  independent instructions. If their total acquisition exceeds a global cap  $N$ , substitute a known fallback program. Coupling capped and uncapped constructions gives $\operatorname{dist}_{M,\mathrm{ad}}
\le A^M e^{-\theta N}.$ 

Thus $N\ge\frac{M\log A+\log(1/\epsilon)}{\theta}$ 

suffices. The guarantee includes entangled inputs and adaptive processing through the declared data-register interface.

I also derived both lower-bound terms.

The horizon term is necessary. A family of faithful replacer channels reduces acquisition to receiving independent classical samples. Producing  $M$  outputs with the correct joint law distinguishes parameters separated by order  $M^{-1/2}$ . Any acquisition procedure therefore requires  $\Omega(M)$  calls at fixed nontrivial error.

The precision term is necessary. For a procedure using at most  $N$  acquisition queries, its retrieved channel is polynomial of degree at most  $N$  in a source’s depolarizing strength. Chebyshev extrapolation transfers a uniformly tiny error on the noisy interval toward the clean-unitary boundary. An explicit offline unitary-programming argument then gives $\epsilon\ge
\frac{49}{512\pi^2N^2}
\left(\frac{1-\sqrt\nu}{1+\sqrt\nu}\right)^N.$ 

Consequently  $N=\Omega_\nu(\log(1/\epsilon))$ . The argument allows entangled and adaptive quantum acquisition before the payload arrives; it is not inferred from the earlier Choi-copy-only obstructions.

At  $\epsilon=0$ , the same argument rules out every deterministic finite acquisition cap for universal reproduction of the full interior class. This is consistent with the established unitary no-programming obstruction. arxiv.org

The upper and lower bounds give the stated  $\Theta_{d,\nu}(M+\log(1/\epsilon))$  law. The constants are not dimension independent or practically optimized.

4. A broader consequence: executing transformed processes

The construction also applies when the desired channel is a known affine function of the experimentally accessible description, provided its Choi matrix has a supplied interior margin.

This gives, for example:

Complex-conjugate execution: implement the channel with Choi matrix  $J_{\mathcal E}^{T}$ .

Adjoint execution: for a unital channel, implement  $\mathcal E^\dagger$ , whose Choi matrix is the swapped transpose of  $J_{\mathcal E}$ .

These are acquired operations from records. The protocol does not assume an inverse-query oracle.

For $\mathcal E_U(X)
=pUXU^\dagger+(1-p)\operatorname{Tr}(X)I_d/d,$ 

adjoint execution yields $\mathcal R_U(X)
=pU^\dagger XU+(1-p)\operatorname{Tr}(X)I_d/d.$ 

The reverse operation retains the same noise strength. Applying it after the noisy forward operation gives signal weight  $p^2$ . It does not remove depolarization, and it does not replace the earlier spectral decoder’s stronger noise-preservation property on its specified supplied-data task.

5. Comparators and the actual access contract

The strongest conventional route is central here: classical exact sampling supplies the new mechanism. I am not claiming a quantum advantage over equally informed classical processing.

 | Route | What it supplies | Main distinction

 | Direct future access to the source | Exact future executions | Requires the original device to remain callable

 | Ordinary process tomography | A reusable approximate model | Supports a conditional estimation guarantee

 | Earlier frozen decoder | Many-data recovery from one calibration record | Retains its source model, recovery scope and confidence contract

 | This operation factory | Sampled physical executions with the correct averaged channel | Requires fresh acquisition for independent uses

 | Port-based storage and retrieval | Direct quantum programming | Works under different program-access and noise promises

The new law measures source acquisition calls. Catalog construction, classical computation, known-channel synthesis, register width, storage and fault tolerance remain separate costs. In particular, the fast sampling theorem does not establish a comparable wall-clock bound.

Executing the catalog requires trusted synthesis of known channels. Source copies alone do not supply that control, and a restricted controller with only whole-register SWAP couplings need not suffice.

The Choi floor is a supplied promise. The compiler does not certify it from finitely many observations.

6. Records, timing and reuse are essential limitations

Exactness holds after averaging the internal instruction, measurement outcomes, rejection history and stopping time.

A sampled  $\Gamma_V$  generally differs from  $\mathcal E$ . Reusing the same instruction produces $\mathbb E[\Gamma_V^{\otimes M}],$ 

which generally differs from  $\mathcal E^{\otimes M}$ . Independent uses require independent sampled instructions.

Exposing the current acquisition record also changes the implemented instrument. In one executed scalar example, the unconditional output-one probability is  $2/5$ , but conditioning on termination after one source observation raises it to approximately  $0.999999144$ . Therefore a public stopping-time record cannot silently be included in the exact channel guarantee.

The exact version has genuinely unbounded waiting. A fixed cap gives the bounded-error version. Arbitrary payload references are allowed, but payload choices conditioned on the current internal factory record are outside the claim.

I also proved a separate support boundary: almost-surely finite processing of faithful quantum programs cannot produce a family of exact target channels whose Choi kernels move with the unknown parameter. Thus this machinery does not manufacture clean unknown unitary programs from full-rank noisy ones.

7. Evidence and remaining gaps

The work is saved in place under:

producer-workspace/p3_operational_factory_20261029

The executable passed 206 finite assertions, with maximum floating equality residual  $3.56\times10^{-15}$ . It checks rational sampling identities, the geometric weights, a full 12-parameter qubit-channel catalog containing 4,096 physical channels, known-channel Kraus synthesis, reference-entangled outputs, conjugation, adjoint reversal and the lower-bound algebra.

One executed rational simulation generated a complete 12-coordinate channel instruction using 391,178 simulated source observations. That large observed cost is a useful warning about the current implementation. It is not a hardware experiment or an optimized benchmark.

The general polytope precomputation and the fast-tail compiler have not been executed. The optimal asymptotic acquisition law is an analytical working result using the cited primary machinery. Independent proof review, priority assessment, useful dimension/noise constants and efficient implementation remain open.

The earlier spectral-exchange, source-weighted recovery, clean/noisy-data distinctions, resource laws and accepted N675 foundations are preserved. No files were exported or repackaged, and no new allocation was created.
