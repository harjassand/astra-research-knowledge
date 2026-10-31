# Rate-independent source-model perturbations for centered classical–quantum dynamics

31 October 2026. Full mathematical receiving proof; pending independent review. This concerns a classical source with operator-valued quantum state blocks, not unrestricted quantum source coherences. It does not acquire an unknown stationary law or a uniform transition-error certificate from samples.

## 1. Assumptions and norm

Let P0 and P1 be finite column-stochastic matrices on the SAME observed label space. They share a known stationary probability vector pi. Write Pi=pi 1^T and Q=I-Pi. Assume an integer m>=1 and

    P0^m=Pi,       eta=||P1-P0||_1 <= 1/(4m),

where the matrix norm is the maximum column sum of absolute values. Strict positivity of pi is not required. Define Delta=P1-P0. Column stochasticity and common stationarity imply

    Pi Delta=0, Delta Pi=0, Delta=Q Delta Q.

On a system with any finite reference, a CQ operator is a tuple X=(X_x)_x with norm ||X||=sum_x ||X_x||_1. Pi acts by (Pi X)_x=pi_x sum_y X_y, so ||Pi||=1 and ||Q||<=2. Every stochastic matrix acts contractively, and Delta has induced norm at most eta, uniformly in the reference dimension. Q's range consists of tuples summing to the ZERO OPERATOR, not merely tuples of total scalar trace zero.

The two physical generators are

    L_i X = lambda(P_i-I)X + H0_super X + sqrt(lambda) V X,
    (H0_super X)_x=-i[H0,X_x],   (V X)_x=-i[H_x,X_x].

H0 is the same system Hamiltonian in both models. The same source-diagonal Hermitian couplings obey

    ||H_x||<=b,       sum_x pi_x H_x=0.

Thus ||V||<=2b and Pi V Pi=0. The label model is exogenous: no unobserved quantum backaction or unknown system-source interaction is inferred from classical transition samples. Each E_i(t)=exp(tL_i) is a physical CQ CPTP map, contractive in the stated complete norm. All estimates below hold on arbitrary joint CQ inputs, not only stationary product inputs.

## 2. Acquired fast-sector decay, with a dimension-free norm

Telescoping stochastic powers gives ||P1^m-P0^m||_1<=m eta<=1/4. Hence for q in range Q,

    ||P_i^m q|| <= ||q||/4,       i=0,1.

For each source separately introduce the analysis norm

    |q|_i = max_(0<=r<m) 4^(r/m) ||P_i^r q||.

Then ||q||<=|q|_i<=4||q|| and |P_i q|_i<=4^(-1/m)|q|_i. The last step of this inequality uses the m-step contraction, rather than assuming one-step mixing. Poissonization implies

    |exp[lambda t(P_i-I)]q|_i
       <= exp[-lambda(1-4^(-1/m))t]|q|_i.

The scalar bound 1-4^(-1/m)>=3/(4m) follows from concavity of 1-exp(-x). H0_super commutes with all source matrices and generates isometries for |.|_i, independently of ||H0||. Meanwhile

    |Q V q|_i <=4||Q V q|| <=16b |q|_i.

Let S_i(t) be the QQ propagator generated ON range Q by

    lambda(P_i-I) + H0_super + sqrt(lambda) Q V Q.

The bounded-perturbation/Dyson estimate in |.|_i gives decay exponent at least 3lambda/(4m)-16b sqrt(lambda). In the high-rate branch

    sqrt(lambda)>=64bm,

this is at least lambda/(2m). In particular the weaker convenient bound

    ||S_i(t)||_(Q to Q) <=4 exp(-beta t),    beta=lambda/(4m)

holds. No diagonalization, source dimension or pi_min factor enters. These are mathematical analysis norms, not operations assumed executable by the compiler.

## 3. Full-to-fast and fast-to-full bounds

Put a=32bm/sqrt(lambda), assuming lambda>0 in this section. There is an important domain distinction: the first estimate below takes an input ALREADY in range Q with its ordinary CQ norm. It is not a bound with the same constants for the full-space operator E_i(t)Q.

For q in range Q, a block variation-of-constants identity gives

    E_i(t)q = S_i(t)q
       + sqrt(lambda) integral_0^t E_i(t-s) Pi V S_i(s)q ds.

It can be verified by subtracting the block Pi sqrt(lambda)V Q from L_i; the resulting generator leaves range Q invariant and equals S_i there. Since the physical E_i is contractive and ||Pi V||<=2b,

    ||E_i(t)|_(range Q)|| <=4 exp(-beta t)+a.                 (A)

On a general input X, the other block equation is

    Q E_i(t)X = S_i(t)QX
       + sqrt(lambda) integral_0^t S_i(t-s)Q V Pi E_i(s)X ds.

Centering makes Q V Pi=V Pi. Also ||Pi E_i(s)||<=1. Consequently

    ||Q E_i(t)|| <=8 exp(-beta t)+a.                         (B)

The factor eight includes ||Q||<=2. If (A) is instead written as a full-space E_i(t)Q bound, multiply its right side by at most two. That extra factor is unnecessary in the perturbation integral because Delta maps its input into range Q.

Neither argument assumes the full coupled process mixes to a unique state. The system may preserve arbitrary information. Positivity is used through the physical full-channel contraction, not through an unjustified positivity of S_i or of Q.

## 4. Exact two-sided Duhamel bound

Because Delta=Q Delta Q and L1-L0=lambda Delta,

    E1(t)-E0(t)=lambda integral_0^t E1(t-s) Delta E0(s) ds.

Apply (A) to Delta's output and (B) to its input. This gives

    ||E1(t)-E0(t)||_CQ,complete
       <=lambda eta integral_0^t
           [4 exp(-beta(t-s))+a][8 exp(-beta s)+a] ds
       =lambda eta [32 t exp(-beta t)
           +12a(1-exp(-beta t))/beta+a^2 t].                (C)

For the high-rate threshold, t exp(-beta t)<=1/(e beta) and a<=1/2. Hence

    ||E1(t)-E0(t)||_CQ,complete
       <=eta [72m+1024 b^2 m^2 t].                         (D)

Indeed the first constant is 128m/e, the middle term is at most 24m, and 128/e+24<72. The final term is exactly 1024 b^2 m^2 t. The bound may always be capped at two for channels; (C) is tighter at very short times.

If sqrt(lambda)<64bm, the elementary full-channel Duhamel estimate is

    ||E1(t)-E0(t)||_CQ,complete <=lambda t eta
                               <=4096 b^2 m^2 t eta.

Together, for all lambda>=0,

    ||E1(t)-E0(t)||_CQ,complete
       <= min{2, eta[72m+4096 b^2 m^2 t]}.                  (E)

For lambda=0 the two channels are identical. For b=0 and lambda>0 the high-rate calculation applies with a=0 and yields the source-only mixing sensitivity. There is no division by b. The result is finite-rate, not a limiting homogenization statement.

## 5. Prescribed instruments and the simulation consumer

Take p common prescribed instrument slots, total evolution time T, and the same H0/H_x model on the intervals. Each instrument, including its classical outcome register, must be a CPTP map preserving the CQ input/output algebra. It may act jointly on source labels and system and may retain records/reference memory. Arbitrary source coherence is outside this normed task.

Such SOURCE instruments need not commute with Pi or preserve |.|_i. No such claim is needed: telescope the complete physical interval channels around the same instrument maps, each of which is contractive. Applying (D) per interval in the high-rate branch, or the elementary estimate in the low-rate branch, yields

    controlled-process error
       <= min{2, eta[72(p+1)m+4096 b^2 m^2 T]}.             (F)

System-only instruments do commute with source projections, but that stronger property is not assumed for (F). Outcome-dependent operations at these prescribed slots are allowed through the retained classical record. Any interval-dependent coupling still has to satisfy the SAME centering and uniform norm premises; it is not inferred from data.

If an acquired simulator for the exact-reset model P0 has error epsilon_sim for this same classical controlled task, triangle inequality adds epsilon_sim to (F). This prices a certified model error eta at the macroscopic scale m(p+1)+b^2m^2T rather than lambda T. It does NOT supply eta, guarantee efficient uniform-TV estimation on an enormous label space, estimate an unknown pi or event rate, or identify an unknown physical coupling. Coupling circuits, source acquisition, arithmetic and consumer operations remain paid.

The finite-source compiler may implement a quantum realization of P0, but receiving (F) uses ONLY its already established diagonal-process equivalence. A diamond bound on arbitrary quantum source coherences is not obtained by relabeling the complete CQ norm.

## 6. Why common stationarity and centering matter: an explicit failure

There is no comparable rate-independent bound for arbitrary small mean-changing perturbations. Let labels be signs xi=+/-1, H_x=xi Z on a system qubit, H0=0, and T=1/128. P0 refreshes the sign uniformly. P_epsilon refreshes with stationary mean epsilon, namely probabilities (1+epsilon)/2 and (1-epsilon)/2. Both are one-step reset kernels, and

    ||P_epsilon-P0||_1=epsilon.

Use the SAME initial uniform sign law in both experiments and start the system in |+>. Signs refresh at rate lambda. Its coherence multiplier is f=E exp[-i phi], phi=2 sqrt(lambda) integral_0^T xi(s) ds. Under P0, E phi=0. Under P_epsilon,

    E phi =2 sqrt(lambda) epsilon
            [T-(1-exp(-lambda T))/lambda].

For either process, conditional expectation across a refresh interval gives

    Cov(xi(s),xi(t))=exp[-lambda(t-s)] Var(xi(s)),  t>=s.

Therefore Var(phi)<=8T=1/16, and |f-exp(-i E phi)|<=sqrt(Var(phi))<=1/4. Choose epsilon=pi/(2T sqrt(lambda))=64pi/sqrt(lambda), which tends to zero and is <=1 for sufficiently large lambda. Then E phi under the biased source differs from pi by at most pi/(lambda T). The difference of system coherence multipliers is at least

    |f_epsilon-f_0| >=3/2-pi/(lambda T),

and hence at least one for sufficiently large lambda. For these qubit outputs this is exactly their trace-norm distance. Any claimed bound C epsilon[1+T] with C independent of lambda would tend to zero, a contradiction.

This example violates common pi and the shared centering condition; it does not contradict (F). It shows why simply calling a small transition bias harmless is false. A changed nontrivial mean produces a real sqrt(lambda) Hamiltonian drift. Scalar system identities remain the trivial commutator-zero exception. If coupling error itself is not centered, the same deterministic drift issue already occurs with an unchanged source.

## 7. Ordinary primary perturbation and homogenization comparison

[Mitrophanov, Sensitivity and convergence of uniformly ergodic Markov chains, 2005](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/26A9854BCB8D103B3A63A9B272616EC0/S0021900200001066a.pdf/sensitivity_and_convergence_of_uniformly_ergodic_markov_chains.pdf), already bounds perturbation sensitivity through convergence/ergodicity of iterated kernels. Rate cancellation for a rapidly mixing source alone is therefore ordinary perturbation theory, not a new principle. The input norm is a uniform transition-kernel error, not a sample-estimation guarantee.

[Szehr–Wolf, Perturbation Bounds for Quantum Markov Processes and their Fixed Points, 2013](https://arxiv.org/html/1210.1171), Theorem 6 and equations (24)–(26), gives continuous-time finite-state perturbation bounds using a Duhamel integral and convergence to a unique stationary state. In that setting the generator perturbation is multiplied by an integrated mixing envelope. Our full source-plus-system need not have a unique stationary state or decay on the source timescale; a spectator system already violates that hypothesis. The present argument instead bounds the two specific Q-facing factors and exploits Delta Pi=Pi Delta=0. This is a structured use of standard semigroup perturbation machinery, not an obstruction to other ordinary methods or a novelty conclusion.

Fast/slow effective-generator and homogenization approaches offer another constructive route: compare the averaged drift and Poisson-equation/effective-diffusion terms, then price finite-rate remainders. The common mean condition is precisely where an unscaled drift would otherwise appear. The present proof avoids taking a limit and retains initial CQ correlations and prescribed instruments, but does not establish that existing broader perturbation machinery cannot yield the same estimate.

The primary publisher record for Kurtz's 1973 'A limit theorem for perturbed operator semigroups with applications to random evolutions' was bibliographically relevant, but https://www.sciencedirect.com/science/article/pii/002212367390089X returned 403. No retry or alternate copy was attempted. Its uninspected theorem is not used as evidence for or against exact overlap. Prior denied-source restrictions remain unchanged. This is a bounded comparator check, not a comprehensive priority search.

## 8. Status and remaining acquisition burden

This theorem makes a specific calibration tolerance independent of microscopic rate under common-stationary centered perturbations. It does not repair arbitrary model misspecification. Exact common pi, exact or separately controlled centering, and a certified uniform eta are load-bearing inputs. Acquiring those efficiently for realistic structured perturbations is a separate task. The proof itself uses no biological or operational chemistry action and claims no implementation or practical resource advantage.
