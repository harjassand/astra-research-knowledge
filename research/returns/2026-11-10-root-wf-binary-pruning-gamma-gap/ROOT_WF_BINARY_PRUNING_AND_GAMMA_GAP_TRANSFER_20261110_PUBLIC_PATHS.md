ROOT MATHEMATICAL PREPARATION: BINARY PRUNING AND A DIMENSION-FREE GAMMA-COUNT GAP TRANSFER
10 November 2026 Brisbane. Two mathematical interfaces for the actual known-parameter WF observation question. No historical novelty claim, unrestricted all-K polynomial sampler, universal gap, or boundary-start L2-to-TV shortcut is asserted.

MODEL AND SOURCE BINDINGS
Use exactly the generator and whole ordered r-row observation contract in P1_FULL_WF_FINITE_OBSERVATION_AFTER_CAC733_WARM_XI_20261110.txt, 8955 ASCII/SHA25689d7a085d18689bb98bded5304b12c0ad7d5d6f7a8636afa035876535283054d. Set alpha0=sum alpha_i, sigma_i=s_i-min s>=0, S=max sigma_i, A(x)=diag(x)-xx^T. P1's entire 13a08d35-c627-478e-82ff-6a8a1966f483 return was read: raw 17081 UTF8/SHA25610ff57b7e8fe8825ec3d337adb67516dae2e489d3703fc45cdf9978ad0694dee. Its ASG uses lineage birth Sn/2, coalescence n(n-1)/2, mutation n alpha0/2. Its finite-horizon rational uniformisation is inherited, not rediscovered here. The all-K unpruned-extinction bound is exponential in S; its lower bound is a mechanism obstruction, not a true mixing lower bound.

A. ALL-TIME POLYNOMIAL OBSERVATION SAMPLING FOR K=2 AT ARBITRARY SELECTION
Let '+' be an allele of greatest fitness and '-' the other. For S>0, sigma_+=S, sigma_-=0. In the P1 ASG, an incoming '+' always replaces the continuing parent and an incoming '-' never does. Therefore every selection branch is the Boolean OR of its two parents, coding '+' as 1. At S=0 there are no selection branches and either allele may be designated '+'. Mutation sets a lineage to 1 at rate alpha_+/2 and to 0 at rate alpha_-/2.

At any backward time, each requested root is either already constant or is the OR of a nonempty subset of currently unresolved ancestral variables. This exact invariant starts with singleton subsets. A selection replaces a variable by two variables with the same root memberships; a coalescence identifies variables and unions memberships; a '-' mutation deletes that variable from every OR; a '+' mutation makes every root containing that variable equal to 1. Empty OR is the constant 0. Once constant, a root stays resolved. This is an explicit finite set-valued pruning rule, including shared ancestors between roots.

Fix a root. While unresolved it has at least one active ancestor, so mutation to '+' resolves it at predictable total rate at least alpha_+/2. Other transitions cannot make a resolved root unresolved. Localising the nonexplosive ASG and applying the elementary compensator/Gronwall inequality gives
 P(root unresolved at backward time u)<=exp(-alpha_+ u/2).
The ASG is nonexplosive: its birth rate is linear in n and its downward events cannot increase n; finite-time lineage count is bounded by a linear pure-birth process. The localised survival inequality therefore passes to the process. A union bound gives
 P(some root unresolved at u)<=r exp(-alpha_+ u/2).
Couple starts x and an independent stationary latent start Z through the same graph and the same ancestral random choices. If every root has resolved before u, the two entire rows agree. Consequently, for every r,x (including boundaries),
 TV(O_(u,x)^r,O_infinity^r)<=min(1,r exp(-alpha_+ u/2)).             (A1)
This controls the entire row, not just a moment or each separate label. Importantly it is independent of S. A '+' mutation kills an entire OR expression, whereas extinction of EVERY unpruned potential ancestor is unnecessary.

An explicit rational large-time cutoff is
 T_bin=8r/(alpha_+ epsilon), r>=1.
Since exp(-z)<=1/z for z>0, (A1) at this time is <=epsilon/4. For t>=T_bin use the accepted stationary observation compiler at tolerance epsilon/4. For 0<t<T_bin use P1's finite-horizon ASG directly; implementing pruning is not required for this algorithm. At t=0/r=0 return the exact initial/empty row.

Here is a fully paid polynomial finite-horizon choice. Let B=1+L+V as in the issued full question. Then T_bin<=8B^3, r<=B, S<=B, alpha0<=B and epsilon^-1<=B. The original unpruned chain satisfies sup E N_u<=max(r,S+1)<=2B, hence expected births by t<=B^2 t<=8B^5. Put
 H_line=2^12 B^8, Lambda=2 H_line^2=2^25 B^16,
 M=2^70 B^40, mu=Lambda*t<=2^28 B^19.
The original ASG crosses H_line only after at least H_line-r>=H_line/2 births. Markov gives a cap-failure probability <=16B^5/H_line<=epsilon/64. Lambda dominates its whole event rate below the cap, since S,alpha0<=B and H_line>=2B. Replace its Poisson(mu) proposal count by M independent exact rational Bernoulli(mu/M) proposals. Le Cam gives
 2mu^2/M<=2^-13 B^-2<=epsilon/64.
At a cap crossing return any valid fallback row, charging that event to the error. Each successful proposal has the exact rational uniformised graphical transition; unresolved ancestral labels are exact Cat(x). The whole finite-time graph-law, hence whole output-law, TV error is <=epsilon/32. The large-time branch has error <=epsilon/2 by (A1) plus the accepted stationary error.

All integers/probabilities here have polynomial bit length in B. There are deterministically M proposal iterations and at most M recorded graph nodes, each with O(log M+log H_line+L+r) bits using even a deliberately inefficient representation. Rational Bernoulli and finite categorical choices use fair-bit rejection with fewer than two rounds in expectation. One explicit loose choice is
 expected total bit work, expected fair bits, peak memory and output work <=2^600 B^256.     (A2)
To see that the constants can be chosen independently of every input, use schoolbook arithmetic and arrays with linear search. Every finite-horizon probability numerator/denominator, index and graph entry has <=2^12 B^2 bits: the input factors contribute <=O(L), and log2 M=70+40log2 B; no accumulated path-probability product is stored. Allow even M full scans, each of length M, and <=2^40 B^8 bit operations per visited entry, including rational/categorical preparation. This bounds the finite-horizon expected work by 2^180 B^88, with the rejection factor included by another factor below 2^10. Graph space and fair bits are smaller. Backward graph propagation by a full scan per node also fits this bound. For the stationary branch, the accepted exact integer convolution/urn implementation has degree cutoff <=32B at K=2 and tolerance epsilon/4. Its displayed factor products have <=2^14 B^3 bits and at most 2^16 B^4 schoolbook operations, plus at most 2B exact selections. A bound 2^100 B^16 therefore suffices there. Both are below (A2). Rejection rounds reuse their buffers, so their unbounded count does not create unbounded peak memory. Numeric t or t^-1 is never used as a resource bound; S is paid numerically rather than only through log S. Thus the actual full resource contract is now constructed for EVERY K=2 input, even strong selection, tiny positive mutation and arbitrary binary times.

For K>2 the P1 acceptance probability sigma_incoming/S can overwrite a fitter continuing parent with an intermediate type. The OR invariant fails. Even a 'choose fitter at rate (fitness difference)/S' graphical rule needs an independently proved multi-type pruning/coupling contract. Do not import (A1) to arbitrary K, silently treat unknown type assignments as free, or infer a universal complexity obstruction from that failure.

B. DIMENSION-FREE VARIANCE TRANSFER FROM THE EXPLICIT GAMMA-COUNT CHAIN
Let
 mu(dx)=Z^-1 exp(sigma dot x) Dir_alpha(dx),
 pi(n)=Z^-1 [product_i (alpha_i)_(n_i) sigma_i^n_i/n_i!]/(alpha0)_(|n|),
 nu(n,dx)=pi(n) Dir_(alpha+n)(dx).
Coordinates with sigma_i=0 have n_i=0. Direct cancellation shows that, conditional on x under nu, the n_i are independent Poisson(sigma_i x_i). In particular total count conditional on x is Poisson(sigma dot x)<=st Poisson(S). All count moments are finite. No sampling or integration oracle is needed for this identity.

On the support of pi use the continuous-time chain
 q(n,n+e_i)=sigma_i(alpha_i+n_i)/2,
 q(n,n-e_i)=n_i(alpha0+|n|-1)/2.
Detailed balance follows by the displayed pi ratio. Birth rate is <=S(alpha0+|n|)/2, so the chain is nonexplosive by linear immigration-birth domination. Its invariant probability is pi. Let lambda_D>0 be ANY actually proved Poincare gap for its closed reversible Dirichlet form
 E_D(F)=sum_n pi(n) sum_i sigma_i(alpha_i+n_i)/2 [F(n+e_i)-F(n)]^2.
For S=0 the support is a singleton and the following count-variance term vanishes. No polynomial lower bound for lambda_D is assumed proved.

Define E_mu(f)=1/2 int grad f^T A grad f dmu. For a continuously differentiable smooth ambient function on the closed simplex, let b=alpha+n, b0=sum b, D_b=Dir_b, and F(n)=D_b f. The neutral Dirichlet WF Poincare inequality is
 Var_(D_b) f <= (2/b0) E_b(f),
 E_b(f)=1/2 D_b[grad f^T A grad f].
For completeness: the neutral self-adjoint generator has degree-m eigenvalue -m(m-1+b0)/2 on the orthogonal polynomial layer of total degree m. Its highest-degree coefficient gives that eigenvalue, symmetry removes lower orthogonal layers, and polynomial density in L2(Dir_b) gives the gap b0/2. The inequality extends by form closure for every positive b, including b_i<1; no log-concavity hypothesis is required.

Dirichlet integration by parts (equivalently apply symmetry to the coordinate x_i under the neutral generator) gives
 F(n+e_i)-F(n)=b0 Cov_(D_b)(x_i,f)/b_i
                    =D_b[(A grad f)_i]/b_i.                      (B1)
Write u=D_b[A grad f], Q=D_b[grad f^T A grad f]=2E_b(f), and B_d=diag(sigma_i/b_i). The covariance matrix identity is
 D_b A = [diag b-bb^T/b0]/(b0+1).
For every vector v, Cauchy-Schwarz in L2(D_b;A) gives
 |v^T B_d^(1/2)u|^2
 <=Q v^T B_d^(1/2)(D_b A)B_d^(1/2)v
 <=[S Q/(b0+1)] |v|^2,
because B_d^(1/2)(D_b A)B_d^(1/2) is (diag sigma minus a positive rank-one matrix)/(b0+1), bounded above by S I/(b0+1). Taking the supremum over unit v yields the dimension-free vector estimate
 sum_i (sigma_i/b_i) u_i^2 <=2S E_b(f)/(b0+1).
Together with (B1),
 E_D(F)<=sum_n pi(n) S E_b(f)/(b0+1)
        <=[S/(alpha0+1)] E_mu(f).                              (B2)
This sharpens a coordinatewise sum_i sigma_i bound without assuming uniform fitness or mutation.

The exact conditional variance decomposition under nu is
 Var_mu f=sum_n pi(n) Var_(D_b) f+Var_pi F.
Use the neutral fibre gap, the actually available count gap lambda_D and (B2):
 Var_mu f <= [2/alpha0+S/((alpha0+1)lambda_D)] E_mu(f).          (B3)
F belongs to the count form domain: smooth f is bounded and pi has finite total birth moment; general f follows by ordinary form approximation when the displayed right side is finite. Thus (B3) is an actual conditional comparison theorem, not an analogy. It composes the positive Dirichlet-mixture representation with a precisely defined missing count-chain operation.

What remains: lambda_D itself could still be difficult, and even a polynomial stationary L2 gap does NOT by itself pay uniform deterministic-boundary-start total variation, a transient mixture initialisation, or a finite-bit simulator of the actual observation row. An arbitrarily singular point mass has no free finite L2 density. No circular appeal from an assumed selected WF gap back to the same count gap closes the question.

C. GOVERNING PRIMARY COMPARATORS AND CONTRARY TRANSFER CONDITIONS
1. Sant-Jenkins-Ruggiero https://arxiv.org/pdf/2611.08623v1, model2.1/Definition3.1/Proposition3.6/Theorem4.1 and stationary Section4.3, already read: the explicit gamma-dual and positive mixture are existing premises; practical finite initialisation/Gaussian approximations do not give the issued uniform bit theorem. N1795's complete positive-convolution/urn compiler is inherited once.
2. Baake-Esercito-Hummel https://arxiv.org/pdf/2011.08888v3, current version checked 10 November2026, actual model2.1, killed ASG2.2/Theorem2.3, diffusion generator2.19, killed process2.20/Theorem2.16 and pruned-lookdown2.5.2 read. This paper has TWO types, a precise killed moment dual, and a DIFFERENT ancestral-type pruned process. Its limiting generator has coefficient 1 rather than our 1/2, requiring a factor-two time conversion. A killed all-unfit moment or ancestral type is not automatically a joint multi-allele row sampler. The OR/root-membership argument and finite-bit all-time consequence above state their own complete K=2 contracts. Published pruning, rather than universal extinction of an unpruned graph, is an available representation; no universal multi-type theorem is attributed to this source.
3. Kim-Sau https://arxiv.org/pdf/2412.01489v2, current version checked; actual symmetric-conductance SIP model, Theorem2.2/2.4, open-SIP Theorem6.1/Corollary6.4 read. Fixed-level conditional count weights here are proportional to product_i (alpha_i)_(n_i) sigma_i^n_i/n_i!. Reversible swap rates n_j(alpha_i+n_i)sigma_i would require generally NONSYMMETRIC conductances c_ji=sigma_i. They do not meet the paper's c_ij=c_ji condition unless the active fitness values coincide. Absorbing fitness into alpha changes rising factorials and is invalid. Its reservoir death is linear in n_i; our count death also depends on total N. A gamma-count gap is therefore NOT supplied by the SIP spectral identity, nor by an unverified nonsymmetric extension. The paper also has a real alpha_min<1 gap-identity failure; no alpha_i>=1 assumption is imported into our full problem.

All known/unknown source/access/transfer/resource holds remain. No held original was retried, recovered or substituted. Native Astra retrieval remains unverified; no new build/index/query probe, worker, model, spending, installation or experiment is requested. Exact existing scientific source bytes are preserved. These are mathematical constructions and transfer limitations, not scores or model/policy performance claims.
