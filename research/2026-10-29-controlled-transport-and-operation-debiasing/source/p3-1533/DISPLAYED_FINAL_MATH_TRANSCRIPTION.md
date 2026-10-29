# Normally displayed final: formula text projection

Deterministic text projection of the normally displayed final, preserving its mathematical annotations. This is not an acquired original proof, implementation, or independent review document. Raw visible text and private formula DOM are preserved separately.

I developed a constructive route to exact averaged Petz recovery from forward experiments, and obtained a stronger limitation on the entire classical-compilation programme: its dimension-and-noise cost cannot generally be amortized across a batch.

The central construction is positive matrix debiasing: correct the statistical bias of an experimentally acquired instruction while ensuring that every instruction actually executed is a valid quantum channel. The accompanying resource result is $\boxed{
\sup_{\mathcal E:\,J_{\mathcal E}\succeq \nu I/d^2}
\mathbb E_{\mathcal E}T
\;\ge\;
M\left(1+\frac d\nu\right).
}$ 

That bound applies to exact reproduction acquired through separately measured source outputs, even when the resulting classical programs are correlated and their execution can prepare entangled batch outputs.

These are completed local mathematical constructions with separate internal checks. External acceptance and comprehensive priority review remain open. The general recovery compiler has not been physically implemented.

1. The selected investigation: execute a nonlinear recovery operation

I chose a stronger target than reproducing the forward channel: acquire, using forward experiments, a classical instruction whose average implements its Petz recovery channel relative to a supplied faithful prior  $\sigma$ .

Writing  $\tau=\mathcal E(\sigma)$ , the target is $\mathcal R_{\sigma,\mathcal E}(Y)
=
\sigma^{1/2}
\mathcal E^\dagger
\!\left(
\tau^{-1/2}Y\tau^{-1/2}
\right)
\sigma^{1/2}.$ 

This is a standard recovery operation. Existing implementation work includes algorithms using block encodings and access to a Stinespring unitary for the source channel and its inverse. Those are materially stronger controls than ordinary forward input/output experiments. arxiv.org

The investigated interface is:

The source is an unknown, fixed, memoryless channel with the supplied Choi floor.

Acquisition uses known inputs and fresh output measurements.

Only a classical instruction survives acquisition.

A supplied trusted catalogue implements the selected known channel.

The later payload may be unknown and entangled with a reference.

Exactness averages the current instruction and acquisition record. Independent future uses require independent instructions.

The construction targets the whole recovery channel. Checking only that it returns the known prior would be insufficient: a device that simply prepares  $\sigma$  could pass that test.

Also, Petz recovery is not an inverse that restores arbitrary states after arbitrary noise. The operation itself is implemented exactly in the mathematical average; its recovery performance remains the performance of the Petz map.

Why the previous factory does not immediately solve this

From $\mathbb E[\Gamma_V]=\mathcal E$ 

one generally cannot conclude $\mathbb E[\mathcal R_{\sigma,\Gamma_V}]
=
\mathcal R_{\sigma,\mathcal E}.$ 

The inverse square root makes the target nonlinear. Applying a recovery formula separately to the old random instructions therefore does not establish the desired operation.

The new construction addresses that bias directly.

2. Central mechanism: physical corrections whose mean telescopes

Let  $p=(p_1,\ldots,p_m)$  denote probabilities of informationally complete ordinary source experiments. Let  $F(p)$  be the normalized Choi matrix of the desired operation.

The sufficient theorem uses a computable  $C^4$  extension $F:[0,1]^m\longrightarrow\{\text{normalized channel Choi matrices}\}$ 

with a known uniform interior margin $F(q)\succeq \kappa\,\frac{I}{d^2}.$ 

The extension over the entire probability cube is necessary: empirical frequencies need not themselves describe a physical channel.

Correct the leading sampling bias

Define $G(q)=\sum_i q_i(1-q_i)\,\partial_{ii}F(q),
\qquad
H_n(q)=F(q)-\frac{G(q)}{2n}.$ 

After acquiring  $2n$  observations of each experiment, let  $k$  be the vector of total counts. The distribution of counts in a uniformly selected half-sample is known exactly: it is a product of hypergeometric distributions.

Use that distribution to compute the deterministic correction $\Delta_n(k)
=
H_{2n}\!\left(\frac{k}{2n}\right)
-
\mathbb E\!\left[
H_n\!\left(\frac K n\right)\,\middle|\,k
\right].$ 

The second term is a finite classical calculation. It does not require more source experiments.

I obtained the uniform bound $\boxed{
\|\Delta_n(k)\|_{\mathrm{op}}\le \frac{C}{n^2},
\qquad
\operatorname{Tr}_{\mathrm{out}}\Delta_n(k)=0.
}$ 

The proof uses half-sample symmetry to cancel odd Taylor terms, the exact hypergeometric variance, and fourth-derivative bounds. The bound holds for every possible count vector, which is what allows a physicality guarantee.

Make every correction executable

Set  $J_0=I/d^2$ , choose dyadic levels  $n_j=2^j n_0$ , and choose known probabilities $w_j=\frac{A}{n_j^2},
\qquad
S=\sum_jw_j.$ 

The constants are chosen so the following matrices remain positive: $J_{\mathrm{base}}
=
\frac{H_{n_0}-S J_0}{1-S},
\qquad
J_j
=
J_0+\frac{\Delta_{n_j}}{w_j}.$ 

Select the base branch with probability  $1-S$ , or correction level  $j$  with probability  $w_j$ . Every selected matrix is a normalized CPTP channel. No signed quantum operation is executed.

If $b_n(p)=\mathbb E_p H_n(\widehat p_n),$ 

then hypergeometric conditioning gives $\mathbb E_p\Delta_n=b_{2n}(p)-b_n(p).$ 

Consequently, $\begin{aligned}
\mathbb E_p J_{\mathrm{program}}
&=
b_{n_0}(p)
+
\sum_{j\ge0}
\left[b_{2n_j}(p)-b_{n_j}(p)\right]\\
&=F(p).
\end{aligned}$ 

This establishes equality of the complete channel, including its action on an entangled payload.

Resources and synthesis

The acquisition terminates almost surely, with $\mathbb E T
\le
m n_0+\frac{4mA}{n_0}.$ 

Its displayed tail is polynomial,  $O(t^{-2})$ . The earlier exponential-tail complexity law has not been transferred to this construction.

I also removed a potentially hidden synthesis assumption. The construction can use a finite supplied catalogue consisting of:

At most  $(n_0+1)^m$  base channels.

 $2(d^4-d^2)+1$  fixed channels around the depolarizing channel, whose known mixtures implement all correction branches.

Thus arbitrary on-demand channel synthesis is unnecessary for the existence theorem. The catalogue can nevertheless be enormous. This replaces the general polytope/Wachspress preprocessing with an explicit grid and local directions; it does not establish efficient storage.

There is an important computational limitation: directly computing a correction can require  $(n+1)^m$  terms. Finite expected source calls do not establish finite expected total classical computation under this particular schedule.

Applying the theorem to Petz recovery

I constructed a smooth physical extension of affine tomography by clipping unphysical Choi eigenvalues and restoring the trace-preserving marginal. It agrees with the source throughout the promised floor class.

For a channel  $\Phi$  satisfying  $J_\Phi\succeq\eta I/d^2$ , the Petz channel obeys $J_{\mathcal R_{\sigma,\Phi}}
\succeq
\eta
\frac{\lambda_{\min}(\sigma)}
{\lambda_{\max}(\Phi(\sigma))}
\frac{I}{d^2}
\succeq
\eta\lambda_{\min}(\sigma)\frac{I}{d^2}.$ 

This supplies the positive margin required by the correction theorem. The inverse square root is smooth because  $\Phi(\sigma)$  remains uniformly positive.

The resulting working theorem is therefore:

A supplied Choi floor and a known faithful prior permit exact averaged physical Petz execution from forward experimental observations, classical acquisition memory, and supplied synthesis of a finite known catalogue, with almost-sure finite acquisition and finite expected source calls.

The derivative certificates and catalogue for a general instance remain unexecuted.

Priority correction

Bounded debiasing itself has a direct predecessor. Koskela, Karvonen, Łatuszyński and Spanò construct bounded scalar unbiased estimators using a random sample count independent of the observations. Their work must be credited. The contribution investigated here is the explicit positive matrix construction and its physical recovery-channel application; I am not claiming to have invented bounded debiasing or nonadaptive Bernoulli factories. arxiv.org

3. A stronger resource law: batch correlations cannot remove the floor penalty

The complementary resource investigation obtained $\boxed{
\sup_{\mathcal E:\,J_{\mathcal E}\succeq\nu I/d^2}
\mathbb E_{\mathcal E}T
\ge
M\left(1+\frac d\nu\right).
}$ 

Exact scope

Acquisition measures each source output separately, with adaptive choices permitted. It may stop at an unbounded, almost-surely finite time. Only classical information survives acquisition.

Execution can be much more general:

Programs can be correlated across the batch.

Their conditional outputs can be entangled.

Independent catalogue labels are not assumed.

Exact reproduction is required on the entire promised channel class. The proof does not establish the same bound for approximate reproduction or collective quantum acquisition.

Proof mechanism

Replacer channels suffice: $\mathcal E_\rho(X)=\operatorname{Tr}(X)\rho,
\qquad
\rho\succeq \nu I/d.$ 

Every acquisition call supplies one copy of  $\rho$ . A classical record  $V$  must subsequently prepare states  $\sigma_V$  satisfying $\mathbb E_\rho[\sigma_V]=\rho^{\otimes M}.$ 

Two established information constraints meet here. The Gill–Massar bound limits the information obtainable from separately measured copies. Matsumoto’s reverse-estimation framework constrains the classical information needed to prepare a quantum statistical family. These are direct predecessors of the argument. arxiv.org+1

For an interior state with eigenvalues  $\lambda_1,\ldots,\lambda_d$ , their combination gives the local bound $\mathbb E_\rho T
\ge
M\left[
1+\frac{1}{d-1}
\sum_{i<j}
\frac{\lambda_i+\lambda_j}
{\min(\lambda_i,\lambda_j)}
\right].$ 

Choose spectrum $(1-(d-1)a,a,\ldots,a).$ 

The expression becomes  $M(1+1/a)$ . Taking  $a\downarrow\nu/d$  through interior states proves the worst-case bound.

The proof explicitly handles the random stopping time. A finite-prefix hybrid experiment justifies differentiating the terminal-record distribution using finite expected acquisition cost; an exponential tail is unnecessary.

Consequence for the programme

For an  $n$ -qubit system,  $d=2^n$ , so the bound is $\mathbb E T
\gtrsim
M\,\frac{2^n}{\nu}$ 

in the worst case under this interface.

For example, with  $\nu=0.1$ :

 | Dimension | Exact worst-case expected source-call lower bound

 |  $d=2$  |  $21M$ 

 |  $d=256$  |  $2561M$ 

These are necessary costs, not achievable rates.

This closes a specific possibility: correlating the classical batch cannot turn the entire dimension-and-floor cost into a one-time acquisition overhead. The earlier fixed- $d,\nu$  linear-horizon law remains compatible with this result, but a scalable many-qubit consequence must exploit structure or change the acquisition/storage interface.

4. Exactness cannot generally be exposed through public timing

The timing investigation also reached a stronger theorem than the original caution.

For the entire Choi-floor class, no almost-surely finite classical compiler can satisfy $\mathbb E_{\mathcal E}[\Gamma_V\mid T=n]=\mathcal E$ 

for every positive-probability finite stopping count.

The proof handles the difficult case where a finite successful event has probability zero at every unitary channel. Along $\mathcal E_z=(1-z)\mathcal U+z\mathcal D,$ 

finite-query exactness is a polynomial identity. Expanding acquisition into positive mixtures of unitary and depolarizing source slots, the first nonzero coefficient would have to prepare precisely the unknown unitary. A common depolarizing reference measure then rules out the required uncountably many disjoint successful classical identifications.

Finite random padding does not repair this exact conditional contract.

There are two important qualifications:

Full rank alone is insufficient for the obstruction. A known nonorthogonal random-unitary simplex admits a timing-neutral exact sampler, constructed in the accompanying notes. The universal family’s geometry matters.

Timing visibility does not automatically imply an  $\epsilon^{-2}$  cost. That estimation-type cost belongs to revealing the complete executable instruction. A hidden instruction with a fixed public acquisition cap can still be approximately correct under the earlier truncation contract.

The new debiasing construction illustrates the distinction particularly clearly: its acquisition length is selected before observing data, so its distribution reveals nothing about the unknown parameter. Nevertheless, conditioning on that length changes the delivered mean channel. Absence of parameter information in timing does not guarantee correct joint timing-and-output behaviour.

5. What actually ran

The strongest execution checked a noncommuting qubit Petz family with a faithful, non-diagonal prior. It enumerated every hypergeometric correction at four finite levels.

 | Check | Result

 | Finite assertions | 39,679 passed

 | Distinct parameter points | 4,225

 | Enumerated levels |  $n=4,8,16,32$ 

 | Maximum telescoping discrepancy |  $2.21\times10^{-15}$ 

 | Hessian versus independent derivative check |  $1.19\times10^{-13}$ 

 | Minimum Choi eigenvalue in the finite positive mixture |  $0.03642$ 

The observed values of  $n^2\max_k\|\Delta_n(k)\|_{\mathrm{op}}$  were $0.005693,\quad 0.005273,\quad 0.005089,\quad 0.005001,$ 

consistent with the proved correction order.

The finite mixture averages to  $b_{64}(p)$ , not exactly to the infinite-hierarchy target  $F(p)$ . At five tested points, its normalized Choi trace distance from the target was at most  $2.34\times10^{-6}$ . That is finite-point evidence, not a uniform error certificate.

A separate simulation of 20,000 instructions consumed 320,544 synthetic coin observations. Those coins were supplied directly as parameters of the test family. The run did not acquire a general unknown channel’s tomography coordinates or implement physical synthesis.

The resource-bound script separately passed 435 checks covering the information identities[Truncated]
