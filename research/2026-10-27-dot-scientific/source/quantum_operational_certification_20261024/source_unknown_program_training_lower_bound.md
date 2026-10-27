# Finite-program obstruction and the remaining training-resource gap

Status: new exact source-native lower bounds, pending independent receipt. The bounds concern the stated program/access tasks, not the optimality of every recovery protocol. In particular they do NOT justify importing a Hamiltonian-simulation lower bound into a different heralded decoder task.

## 1. The SAME discarded-label programs contain a binary hard pair

Take output dimension3 and the actual channel family
 E_U(rho)=p U rho U*+(1-p)Tr(rho)I3/3,
with U0=I3 and U1=diag(1,exp(2pi i/3),exp(4pi i/3)). Their normalized Choi vectors Phi_U0 and Phi_U1 are orthogonal. The output marginal sigma=I3/3 and the omega program=I9/9 are identical in both cases.

The exact ordinary12-label program from the received construction is
 T_i=(J_i+3omega)/4=a Phi_Ui+b I9,
 a=p/4, b=(1-a)/9.
These two program states commute. In their common eigenbasis their probability vectors differ only by swapping a+b and b; the other seven entries are b. Their root fidelity (classical affinity) is
 r=7b+2sqrt[b(a+b)]
  =1-[sqrt(a+b)-sqrt(b)]², 0<r<1.                       (1)
A batch of n IID T programs has affinity r^n. Additional omega programs or known ancillas contain no information about i.

## 2. Exact approximate-programming lower bound

Suppose a single fixed processor, given n such T programs, approximates the sharp positive-projector instrument for Phi_U to COMPLETE diamond error at most zeta uniformly for U=U0,U1. Feed its data register the fixed KNOWN state Phi_U0 and read the accepted/rejected bit. The ideal bit distinguishes the two hypotheses perfectly. The full diamond convention bounds the resulting equal-prior discrimination error by zeta/2.

For the actual n-program distributions P,Q, Cauchy-Schwarz gives
 TV(P,Q)<=sqrt[1-(sum sqrt(PQ))²]=sqrt(1-r^(2n)).
Therefore every quantum processor/measurement has Bayes error at least
 [1-sqrt(1-r^(2n))]/2 >=r^(2n)/4.
(The programs commute, so the classical optimal discrimination bound is also the quantum one.) For0<zeta<1/2, necessarily

 n>=log[1/(2zeta)]/[-2log r].                            (2)

The same conclusion applies to a processor approximating the deterministic inverse channel U*(.)U: use the fixed input |+>=(1,1,1)/sqrt3, whose two ideal inverse outputs are orthogonal. In particular it applies to the full received-system nine-Bell inverse target in dimension3. It does not automatically apply to a much weaker inverse with arbitrarily small accepted probability; its success charge must be kept in that separate task.

As p->0,
 r=1-(9/64)p²+O(p³), -2log r=(9/32)p²+O(p³).
Thus these actual discarded-label programs require Omega[p^-2 log(1/zeta)] copies for the sharp projector or deterministic inverse task. Quadratic dependence on weak signal is not merely an artifact of the QPE upper bound. Exact uniform programming with finite n is impossible since r>0. At p=1, r=11/12 still gives the finite-program obstruction: the underlying channel is noiseless, but discarding the chosen training labels into T produces faithful mixed program states.

This is NOT a lower bound for every way of retaining labels or adaptively preparing training inputs. The current upper bound O[p0^-2 log²(1/zeta)/zeta] remains substantially above(2) in accuracy dependence. Removing that gap or beating it with different source-native programs is genuinely open here; no optimality or practical efficiency claim is made.

## 3. A broader fixed-budget noisy-training obstruction

For0<p<1, consider any fixed-budget n-query training procedure for the same E_U family, possibly adaptive and with quantum memory, completed before an independent data input is supplied. Expand each channel as p U(.)U*+q R_I/3. The all-reset history has probability q^n and produces a program state INDEPENDENT of U, even with adaptive choices: on that history every response is the same replacement channel. Consequently the two final program states have a common positive component q^n rho_common. Their trace distance is at most1-q^n, and their equal-prior discrimination error is at least q^n/2.

For either perfect-distinguishing target of section2, uniform complete diamond error zeta must therefore satisfy
 zeta>=q^n.
This proves impossibility of finite EXACT uniform sharp-projector or deterministic-inverse programming under noisy fixed-budget training, without assuming the particular T programs. It gives only a weaker signal dependence than(2), and is not a claim about unbounded stopping rules, prior knowledge of U, data-dependent additional channel calls, or postselection at an arbitrarily reduced success rate.

## 4. Comparison with known sample-simulation limits

Kimmel et al. study sample-based Hamiltonian simulation and extensions to several program states [arXiv:1608.00281](https://arxiv.org/abs/1608.00281). The later detailed non-asymptotic analysis of Go et al. gives a matching-order sample lower bound for that simulation task and discusses an incompleteness in the older analysis [arXiv:2412.02134v3](https://arxiv.org/abs/2412.02134v3). Those results concern simulating the unitary evolution generated by an unknown density operator; they do not alone prove optimality of our projector or recovery construction. The received upper construction uses an explicit elementary collision-error proof, and the lower bounds above are independently acquired from the actual channel/program pair rather than transplanted from a different oracle model.

## 5. CP domination closes the heralded-abort loophole for finite noisy training

A common component alone does not rule out every exact heralded strategy, since it might simply be rejected. For the WHITE full-rank reset hard family, a stronger two-sided CP domination pays the statement.

Let R be the qutrit completely mixed replacement channel. Its normalized Choi matrix is I9/9, while J_EU=pPhi_U+qI9/9. For q>0,
 q R <=_CP E_U <=_CP (9p+q) R.                          (3)
For ANY fixed-n adaptive training procedure completed before the independent data arrives, replace each channel slot using(3). Positivity of CP composition, including intermediate instruments and retained classical records, yields for the resulting program operators
 q^n rho_R <=rho_U<=(9p+q)^n rho_R.                     (4)
These may be subnormalized if program preparation itself is heralded. Thus their supports are exactly the SAME; this conclusion does not rely on counting only one latent history.

Let a fixed accepted retrieval operation act on the program and independent data. Apply it to half of a known maximally entangled DATA state. The resulting accepted data-channel Choi operators inherit(4). If the protocol implemented an exact inverse on acceptance, they would be s_U Phi_(U inverse), with nonzero s_U for some U. For two unitaries with nonparallel inverse Choi vectors, the common reference operator must be supported in both distinct rank-one lines, hence must vanish. The UPPER domination in(4) then forces every accepted Choi operator to vanish too. Therefore no such protocol has nonzero exact success.

The same proof applies to exact accepted sharp-projector maps P_U(.)P_U: their Choi vectors vec(P_U) are distinct rank-one lines. This rules out a finite exact positive-success storage-and-retrieval implementation even with heralded abort and adaptive finite training. It does NOT rule out approximate programming, source-known gates, noiseless q=0 programs, or algorithms allowed new data-dependent channel queries during retrieval. Nor does it assert that a composed noisy recovery map could be used to expose a hidden pure-success branch.

## 6. Noiseless inversion literature is a different legitimate comparator

Exact probabilistic black-box unitary inversion with charged queries is established by Quintino et al. [arXiv:1810.06944](https://arxiv.org/abs/1810.06944); their adaptive query model should not be silently replaced by discarded mixed programs. Yoshida, Soeda and Murao give probabilistic exact unknown-isometry decoders with success independent of the output dimension [arXiv:2110.00258](https://arxiv.org/abs/2110.00258). Those noiseless black-box results show why a blanket no-programming claim would be false. Our two-Choi antisymmetric receiver is only an explicit elementary noiseless construction, not a claim of novelty or optimality over those protocols. The present obstruction instead acquires the full-rank NOISY finite-storage support constraint, and the quantitative(2) concerns the precise discarded-label program family used in our learned receiver.

### Quantitative charged-success version of the CP-support bound

Two-sided domination also gives rho_U0>=kappa rho_U1 with kappa=[q/(9p+q)]^n. Suppose the desired retrieval instruments have a specified common accepted inverse weight a>0 (or a uniform lower target weight a), and their COMPLETE diamond errors are at most zeta. Choose a fixed data input whose two ideal inverse outputs are orthogonal. Let E1 be the event 'accepted and in the second ideal output'. Under U0 its probability is at most zeta/2; under U1 it is at least a-zeta/2. Program domination survives retrieval, so
 zeta/2>=kappa(a-zeta/2),
and consequently
 zeta>=2a kappa/(1+kappa).
For zeta<2a this implies
 n>=log[(2a-zeta)/zeta]/log[(9p+q)/q].
The same argument uses input Phi_U0 and the acceptance bit for the sharp-projector task, with the hypotheses interchanged as needed. Thus reducing the heralded success weight is explicitly priced; an arbitrarily tiny a can weaken the approximate bound, but no a>0 permits zeta=0 at finite n and q>0. This remains a retrieval-task bound, not a lower bound on error only after the unknown noisy channel has already acted on the data.
